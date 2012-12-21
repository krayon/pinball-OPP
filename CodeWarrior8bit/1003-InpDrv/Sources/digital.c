/*
 *===============================================================================
 *===============================================================================
 *
 *                         OOOO
 *                       OOOOOOOO
 *      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP    OOO    OOO    PPP
 *               PPP     OOOOOOOO     PPP
 *              PPPPP      OOOO      PPPPP
 *
 * @file:   digital.c
 * @author: Hugh Spahr
 * @date:   12/02/2012
 *
 * @note:   Open Pinball Project
 *          Copyright© 2012, Hugh Spahr
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *===============================================================================
 */
/**
 * This file deals with digital I/O port to control the solenoid driver.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"
#include "stdlintf.h"
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "rs232intf.h"
#include "inpglob.h"

#define STDL_FILE_ID        3

/* Port A bits */
#define PA_INP9             0x01
#define PA_INP10            0x02
#define PA_INP11            0x04
#define PA_INP12            0x08
#define PA_XTRA_1           0x40
#define PA_XTRA_2           0x80

/* Port B bits */
#define PB_XTRA_3           0x04
#define PB_XTRA_4           0x08
#define PB_INP13            0x10
#define PB_INP14            0x20
#define PB_INP15            0x40
#define PB_INP16            0x80

/* Port C bits */
#define PC_INP1             0x01
#define PC_INP2             0x02
#define PC_INP3             0x04
#define PC_INP4             0x08
#define PC_INP5             0x10
#define PC_INP6             0x20
#define PC_INP7             0x40
#define PC_INP8             0x80

typedef enum
{
  INP_STATE                 = 0x00,
  INP_LOW                   = 0x01,
  INP_VERIFY_VALID_HIGH     = 0x02,
  INP_HIGH                  = 0x03,
  INP_VERIFY_VALID_LOW      = 0x04,
} DIG_STATE_E;

typedef struct
{
  DIG_STATE_E               state;
  STDLI_ELAPSED_TIME_T      elapsedTime;
} DIG_INP_T;

typedef struct
{
  U8                        currInp;
  DIG_INP_T                 inp[RS232I_NUM_INP];
} DIGITAL_GLOB_T;

DIGITAL_GLOB_T              dig_glob;

/*
 * ===============================================================================
 * 
 * Name: digital_init
 * 
 * ===============================================================================
 */
/**
 * Initialize the digital I/O port
 * 
 * Initialize digital I/O port, and the other digital control signals.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_init(void) 
{
  DIG_INP_T                 *inp_p;
  
  for (inp_p = &dig_glob.inp[0]; inp_p < &dig_glob.inp[RS232I_NUM_INP]; inp_p++)
  {
    inp_p->state = INP_STATE;
  }
  dig_glob.currInp = 0;
  
  /* Set up input lines */
  stdldigio_config_dig_port(STDLI_DIG_PORT_A | STDLI_DIG_PULLUP |
    STDLI_DIG_SMALL_MODEL, 0x0f, 0);
  stdldigio_config_dig_port(STDLI_DIG_PORT_B | STDLI_DIG_PULLUP |
    STDLI_DIG_SMALL_MODEL, 0xf0, 0);
  stdldigio_config_dig_port(STDLI_DIG_PORT_C | STDLI_DIG_PULLUP |
    STDLI_DIG_SMALL_MODEL, 0xff, 0);

} /* End digital_init */

/*
 * ===============================================================================
 * 
 * Name: digital_task
 * 
 * ===============================================================================
 */
/**
 * Task for polling inputs
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_task(void)
{
  DIG_INP_T                 *inp_p;
  U16                       inputs;
  U8                        index;
  
  if (inpg_glob.state == INP_STATE_NORM)
  {
    /* Grab the inputs */
    inputs = PTCD | (((U16)((PTAD & 0x0f) | (PTBD & 0xf0))) << 8);
    index = dig_glob.currInp;
    inp_p = &dig_glob.inp[index];

    if (inpg_glob.inpCfg[index] == FALL_EDGE)
    {
      if (inp_p->state == INP_LOW)
      {
        if (inputs & (1 << index))
        {
          inp_p->state = INP_VERIFY_VALID_HIGH;
          stdltime_get_curr_time(&inp_p->elapsedTime.startTime);
        }
      }
      else if (inp_p->state == INP_VERIFY_VALID_HIGH)
      {
        if (inputs & (1 << index))
        {
          stdltime_get_elapsed_time(&inp_p->elapsedTime);
          if (inp_p->elapsedTime.elapsedTime.usec >= INPG_SWITCH_THRESH)
          {
            inp_p->state = INP_HIGH;
          }
        }
        else
        {
          inp_p->state = INP_LOW;
        }
      }
      else if (inp_p->state == INP_HIGH)
      {
        if ((inputs & (1 << index)) == 0)
        {
          inp_p->state = INP_VERIFY_VALID_LOW;
          stdltime_get_curr_time(&inp_p->elapsedTime.startTime);
        }
      }
      else if (inp_p->state == INP_VERIFY_VALID_LOW)
      {
        if ((inputs & (1 << index)) == 0)
        {
          stdltime_get_elapsed_time(&inp_p->elapsedTime);
          if (inp_p->elapsedTime.elapsedTime.usec >= INPG_SWITCH_THRESH)
          {
            inp_p->state = INP_LOW;
            DisableInterrupts;
            inpg_glob.inpSwitch |= (1 << index);
            EnableInterrupts;
          }
        }
        else
        {
          inp_p->state = INP_HIGH;
        }
      }
    }
    else if (inpg_glob.inpCfg[index] == RISE_EDGE)
    {
      if (inp_p->state == INP_LOW)
      {
        if (inputs & (1 << index))
        {
          inp_p->state = INP_VERIFY_VALID_HIGH;
          stdltime_get_curr_time(&inp_p->elapsedTime.startTime);
        }
      }
      else if (inp_p->state == INP_VERIFY_VALID_HIGH)
      {
        if (inputs & (1 << index))
        {
          stdltime_get_elapsed_time(&inp_p->elapsedTime);
          if (inp_p->elapsedTime.elapsedTime.usec >= INPG_SWITCH_THRESH)
          {
            inp_p->state = INP_HIGH;
            DisableInterrupts;
            inpg_glob.inpSwitch |= (1 << index);
            EnableInterrupts;
          }
        }
        else
        {
          inp_p->state = INP_LOW;
        }
      }
      else if (inp_p->state == INP_HIGH)
      {
        if ((inputs & (1 << index)) == 0)
        {
          inp_p->state = INP_VERIFY_VALID_LOW;
          stdltime_get_curr_time(&inp_p->elapsedTime.startTime);
        }
      }
      else if (inp_p->state == INP_VERIFY_VALID_LOW)
      {
        if ((inputs & (1 << index)) == 0)
        {
          stdltime_get_elapsed_time(&inp_p->elapsedTime);
          if (inp_p->elapsedTime.elapsedTime.usec >= INPG_SWITCH_THRESH)
          {
            inp_p->state = INP_LOW;
          }
        }
        else
        {
          inp_p->state = INP_HIGH;
        }
      }
    }
    index++;
    if (index >= RS232I_NUM_INP)
    {
      index = 0;
    }
    dig_glob.currInp = index;
    DisableInterrupts;
    inpg_glob.inpSwitch = (inpg_glob.inpSwitch & ~inpg_glob.stateMask) |
      (inputs & inpg_glob.stateMask);
    EnableInterrupts;
  }
} /* End digital_task */

/*
 * ===============================================================================
 * 
 * Name: digital_set_init_state
 * 
 * ===============================================================================
 */
/**
 * Set initial input state
 *
 * Set the initial input state after a config command was received.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_set_init_state(void)
{
  U16                       inputs;
  U8                        index;
  
  /* Grab the inputs */
  inputs = PTCD | (((U16)((PTAD & 0x0f) | (PTBD & 0xf0))) << 8);
  
  inpg_glob.inpSwitch = 0;
  for ( index = 0; index < RS232I_NUM_INP; index++)
  {
    if (inpg_glob.inpCfg[index] == STATE_INPUT)
    {
      inpg_glob.stateMask |= (1 << index);
      dig_glob.inp[index].state = INP_STATE;
    }
    else if (inpg_glob.inpCfg[index] == RISE_EDGE)
    {
      if (inputs & (1 << index))
      {
        inpg_glob.inpSwitch |= (1 << index);
        dig_glob.inp[index].state = INP_HIGH;
      }
      else
      {
        dig_glob.inp[index].state = INP_LOW;
      }
    }
    else if (inpg_glob.inpCfg[index] == FALL_EDGE)
    {
      if ((inputs & (1 << index)) == 0)
      {
        inpg_glob.inpSwitch |= (1 << index);
        dig_glob.inp[index].state = INP_LOW;
      }
      else
      {
        dig_glob.inp[index].state = INP_HIGH;
      }
    }
  }
  inpg_glob.inpSwitch |= (inputs & inpg_glob.stateMask);
} /* End digital_set_init_state */
