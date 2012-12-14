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
#include "solglob.h"

#define STDL_FILE_ID        3

/* Port A bits */
#define PA_SOL_DRV1         0x01
#define PA_SOL_DRV2         0x02
#define PA_SOL_DRV3         0x04
#define PA_SOL_DRV4         0x08
#define PA_XTRA_1           0x40
#define PA_XTRA_2           0x80
#define PA_SOL_MASK         0x0f

/* Port B bits */
#define PB_SOL_DRV5         0x10
#define PB_SOL_DRV6         0x20
#define PB_SOL_DRV7         0x40
#define PB_SOL_DRV8         0x80
#define PB_XTRA_3           0x04
#define PB_XTRA_4           0x08
#define PB_SOL_MASK         0xf0

/* Port C bits */
#define PC_INP_SW1          0x01
#define PC_INP_SW2          0x02
#define PC_INP_SW4          0x04
#define PC_INP_SW3          0x08
#define PC_INP_SW6          0x10
#define PC_INP_SW5          0x20
#define PC_INP_SW8          0x40
#define PC_INP_SW7          0x80

typedef enum
{
  SOL_STATE_IDLE            = 0x00,
  SOL_VERIFY_INPUT_VALID    = 0x01,
  SOL_INITIAL_KICK          = 0x02,
  SOL_SUSTAIN_PWM           = 0x03,
  SOL_VERIFY_SWITCH_CLR     = 0x04,
  SOL_MIN_TIME_OFF          = 0x05,
} DIG_STATE_E;

#define MIN_OFF_INC         0x10

typedef struct
{
  DIG_STATE_E               state;
  U8                        cnt;
  BOOL                      foundClr;
  STDLI_ELAPSED_TIME_T      elapsedTime;
} DIG_SOL_T;

typedef struct
{
  DIG_SOL_T                 sol[RS232I_NUM_SOL];
} DIGITAL_GLOB_T;

DIGITAL_GLOB_T              dig_glob;

const U8                    SWITCH_LOOKUP[RS232I_NUM_SOL] =
  { PC_INP_SW1, PC_INP_SW2, PC_INP_SW3, PC_INP_SW4,
    PC_INP_SW5, PC_INP_SW6, PC_INP_SW7, PC_INP_SW8 
  };

const BOOL                  SOL_PORT_A[RS232I_NUM_SOL] =
  { TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE };

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
  DIG_SOL_T                 *sol_p;
  
  for (sol_p = &dig_glob.sol[0]; sol_p < &dig_glob.sol[RS232I_NUM_SOL]; sol_p++)
  {
    sol_p->state = SOL_STATE_IDLE;
  }
  
  /* Set up solenoid drivers */
  stdldigio_config_dig_port(STDLI_DIG_PORT_A | STDLI_DIG_OUT |
    STDLI_DIG_SMALL_MODEL, PA_SOL_MASK, 0);
  stdldigio_config_dig_port(STDLI_DIG_PORT_B | STDLI_DIG_OUT |
    STDLI_DIG_SMALL_MODEL, PB_SOL_MASK, 0);
  
  /* Set up digital/solenoid inputs */
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
 * Task for polling solenoid inputs
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
  DIG_SOL_T                 *sol_p;
  SOLG_CFG_T                *solCfg_p;
  U8                        inputs;
  U8                        index;
  BOOL                      switchAct;
  
#define PWM_PERIOD          16

  if (solg_glob.state == SOL_STATE_NORM)
  {
    /* Grab the solenoid inputs */
    inputs = PTCD;    
    for (index = 0, sol_p = &dig_glob.sol[0], solCfg_p = &solg_glob.solCfg[0];
      index < RS232I_NUM_SOL; sol_p++, index++, solCfg_p++)
    {
      /* If using the switch as a trigger input, check it.  Note: switches active low */
      if ((solCfg_p->type & USE_SWITCH) && ((inputs & SWITCH_LOOKUP[index]) == 0))
      {
        switchAct = TRUE;
      }
      else
      {
        switchAct = FALSE;
      }
      /* Check if processor is requesting the solenoid to be kicked */
      switchAct = (switchAct || (solg_glob.procCtl & (1 << index)) ? TRUE : FALSE);
      if (sol_p->state == SOL_STATE_IDLE)
      {
        if (switchAct)
        {
          /* Switch just started to be pressed */
          stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
          sol_p->state = SOL_VERIFY_INPUT_VALID;
        }
      }
      else if (sol_p->state == SOL_VERIFY_INPUT_VALID)
      {
        if (switchAct)
        {
          /* Check if elapsed time is over threshold */
          stdltime_get_elapsed_time(&sol_p->elapsedTime);
          if (sol_p->elapsedTime.elapsedTime.usec >= SOLG_SWITCH_THRESH)
          {
            sol_p->state = SOL_INITIAL_KICK;
            DisableInterrupts;
            solg_glob.validSwitch |= (1 << index);
            EnableInterrupts;
            sol_p->foundClr = FALSE;
            if (SOL_PORT_A[index])
            {
              PTAD |= (1 << index);
            }
            else
            {
              PTBD |= (1 << index);
            }
            stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
            
            /* If this is an autoclear switch, clear the proc bit */
            if (solCfg_p->type & AUTO_CLR)
            {
              solg_glob.procCtl &= ~(1 << index);
            }
          }
        }
        else
        {
          /* Switch wasn't active long enough */
          sol_p->state = SOL_STATE_IDLE;
        }
      }
      else if (sol_p->state == SOL_INITIAL_KICK)
      {
        /* Look for switch to be inactive */
        if (!switchAct)
        {
          sol_p->foundClr = TRUE;
        }
      
        /* Check if elapsed time is over initial kick time */
        stdltime_get_elapsed_time(&sol_p->elapsedTime);
        if (sol_p->elapsedTime.elapsedTime.msec >= solCfg_p->initialKick)
        {
          /* In all cases turn off the solenoid driver */
          if (SOL_PORT_A[index])
          {
            PTAD &= ~(1 << index);
          }
          else
          {
            PTBD &= ~(1 << index);
          }
          
          /* See if this has a sustaining PWM */
          if (solCfg_p->dutyCycle & DUTY_CYCLE_MASK)
          {
            /* Make sure the input continues to be set */
            if (switchAct)
            {
              sol_p->state = SOL_SUSTAIN_PWM;
            }
            else
            {
              sol_p->state = SOL_MIN_TIME_OFF;
              sol_p->cnt = 0;
            }              
          }
          else
          {
            sol_p->state = SOL_MIN_TIME_OFF;
            sol_p->cnt = 0;
          }
          stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
        }
      }
      else if (sol_p->state == SOL_SUSTAIN_PWM)
      {
        if (switchAct)
        {
          /* Do slow PWM function, initially off, then on for duty cycle */
          stdltime_get_elapsed_time(&sol_p->elapsedTime);
          if (sol_p->elapsedTime.elapsedTime.msec > PWM_PERIOD)
          {
            /* PWM period is over, clear drive signal */
            if (SOL_PORT_A[index])
            {
              PTAD &= ~(1 << index);
            }
            else
            {
              PTBD &= ~(1 << index);
            }
            stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
          }
          else if (sol_p->elapsedTime.elapsedTime.msec >
            PWM_PERIOD - (solCfg_p->dutyCycle & DUTY_CYCLE_MASK))
          {
            if (SOL_PORT_A[index])
            {
              PTAD |= (1 << index);
            }
            else
            {
              PTBD |= (1 << index);
            }
          }
        }
        else
        {
          /* Switch is inactive, turn off drive signal */
          if (SOL_PORT_A[index])
          {
            PTAD &= ~(1 << index);
          }
          else
          {
            PTBD &= ~(1 << index);
          }
          sol_p->state = SOL_STATE_IDLE;
        }
      }
      else if (sol_p->state == SOL_VERIFY_SWITCH_CLR)
      {
        if (!switchAct)
        {
          sol_p->state = SOL_STATE_IDLE;
        }
      }
      else if (sol_p->state == SOL_MIN_TIME_OFF)
      {
        /* Look for switch to be inactive */
        if (!switchAct)
        {
          sol_p->foundClr = TRUE;
        }
        
        /* Check if an off time increment has happened */
        stdltime_get_elapsed_time(&sol_p->elapsedTime);
        if (sol_p->elapsedTime.elapsedTime.msec >= solCfg_p->initialKick)
        {
          sol_p->cnt += MIN_OFF_INC;
          if (sol_p->cnt >= (solCfg_p->dutyCycle & MIN_OFF_MASK))
          {
            if (sol_p->foundClr)
            {
              sol_p->state = SOL_STATE_IDLE;
            }
            else
            {
              sol_p->state = SOL_VERIFY_SWITCH_CLR;
            }
          }
          else
          {
            stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
          }
        }
      }
    }
  }
} /* End digital_task */
