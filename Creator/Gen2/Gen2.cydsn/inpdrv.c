/*
 *===============================================================================
 *
 *                         OOOOOO
 *                       OOOOOOOOOO
 *      PPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP    OOO      OOO    PPP
 *               PPP     OOOOOOOOOO     PPP
 *              PPPPP      OOOOOO      PPPPP
 *
 * @file:   inpdrv.c
 * @author: Hugh Spahr
 * @date:   12/02/2012
 *
 * @note:   Open Pinball Project
 *          Copyright© 2012-2015, Hugh Spahr
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
 * This file controls the input driver wing board.  It is adapted from
 * digital.c in the previous 1003-InpDrv\Sources\digital.c
 *
 *===============================================================================
 */
 
#include "stdtypes.h"
#include "stdlintf.h"
#include "rs232intf.h"
#include "gen2glob.h"
#include "procdefs.h"         /* for EnableInterrupts macro */

#define STDL_FILE_ID          3

typedef enum
{
   INP_STATE                  = 0x00,
   INP_LOW                    = 0x01,
   INP_VERIFY_VALID_HIGH      = 0x02,
   INP_HIGH                   = 0x03,
   INP_VERIFY_VALID_LOW       = 0x04,
} INPDRV_STATE_E;

typedef struct
{
   INPDRV_STATE_E             state;
   STDLI_ELAPSED_TIME_T       elapsedTime;
} INPDRV_INP_T;

typedef struct
{
   INT                        currInp;
   U32                        inpMask;
   INPDRV_INP_T               inp[RS232I_NUM_GEN2_INP];
} INPDRV_GLOB_T;

INPDRV_GLOB_T                 inpdrv_info;

/*
 * ===============================================================================
 * 
 * Name: inpdrv_init
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
void inpdrv_init(void) 
{
   INPDRV_INP_T               *inp_p;
   INT                        index;

#define INPUT_BIT_MASK        0xff   
   
   for (inp_p = &inpdrv_info.inp[0]; inp_p < &inpdrv_info.inp[RS232I_NUM_GEN2_INP]; inp_p++)
   {
      inp_p->state = INP_STATE;
   }
   
   /* Curr input to an invalid value to be filled out */
   inpdrv_info.currInp = RS232I_NUM_GEN2_INP;
   inpdrv_info.inpMask = 0;
  
   /* Set up digital ports, walk through wing boards */
   for (index = 0; index < RS232I_NUM_WING; index++)
   {
      /* Check if this wing board is a solenoid driver */
      if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP)
      {
         /* Setup inputs */
         stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, INPUT_BIT_MASK, 0);
         
         /* Set up bit mask of valid inputs */
         inpdrv_info.inpMask |= (0xff << (index << 3));
         if (inpdrv_info.currInp == RS232I_NUM_GEN2_INP)
         {
            inpdrv_info.currInp = (index << 3);
         }
      }
   }
   
   /* Set the location of the configuration data */
   gen2g_info.inpCfg_p = (GEN2G_INP_CFG_T *)gen2g_info.freeCfg_p;
   gen2g_info.freeCfg_p += sizeof(GEN2G_INP_CFG_T);

} /* End inpdrv_init */

/*
 * ===============================================================================
 * 
 * Name: inpdrv_task
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
void inpdrv_task(void)
{
   INPDRV_INP_T               *inp_p;
   U32                        inputs;
   INT                        index;
   U8                         data;
   RS232I_CFG_INP_TYPE_E      cfg;
   BOOL                       foundNextBit;

#define SWITCH_THRESH         50
   
   if ((gen2g_info.typeWingBrds & (1 << WING_INP)) != 0)
   {
      /* Grab the inputs */
      inputs = 0;
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP)
         {
            data = stdldigio_read_port(index, INPUT_BIT_MASK);
            inputs |= (data << (index << 3));
         }
      }
      index = inpdrv_info.currInp;
      inp_p = &inpdrv_info.inp[index];
      cfg = gen2g_info.inpCfg_p->inpCfg[index];

      if (cfg == FALL_EDGE)
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
               if (inp_p->elapsedTime.elapsedTime.usec >= SWITCH_THRESH)
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
               if (inp_p->elapsedTime.elapsedTime.usec >= SWITCH_THRESH)
               {
                  inp_p->state = INP_LOW;
                  DisableInterrupts;
                  gen2g_info.validSwitch |= (1 << index);
                  EnableInterrupts;
               }
            }
            else
            {
               inp_p->state = INP_HIGH;
            }
         }
      }
      else if (cfg == RISE_EDGE)
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
               if (inp_p->elapsedTime.elapsedTime.usec >= SWITCH_THRESH)
               {
                  inp_p->state = INP_HIGH;
                  DisableInterrupts;
                  gen2g_info.validSwitch |= (1 << index);
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
               if (inp_p->elapsedTime.elapsedTime.usec >= SWITCH_THRESH)
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

      foundNextBit = FALSE;
      while (!foundNextBit)
      {
         index++;
         if (index >= RS232I_NUM_GEN2_INP)
         {
            index = 0;
         }
         if ((inpdrv_info.inpMask & (1 << index)) != 0)
         {
            foundNextBit = TRUE;
         }
      }
      inpdrv_info.currInp = index;

      DisableInterrupts;
      gen2g_info.validSwitch = (gen2g_info.validSwitch & ~gen2g_info.stateMask) |
         (inputs & gen2g_info.stateMask);
      EnableInterrupts;
   }
} /* End inpdrv_task */

/*
 * ===============================================================================
 * 
 * Name: inpdrv_set_init_state
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
void inpdrv_set_init_state(void)
{
   U16                        inputs;
   INT                        index;
   U8                         data;
   RS232I_CFG_INP_TYPE_E      cfg;
  
   /* Grab the inputs */
   inputs = 0;
   for (index = 0; index < RS232I_NUM_WING; index++)
   {
      if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP)
      {
         data = stdldigio_read_port(index, INPUT_BIT_MASK);
         inputs |= (data << (index << 3));
      }
   }
  
   gen2g_info.validSwitch = 0;
   gen2g_info.stateMask = 0;
   for ( index = 0; index < RS232I_NUM_GEN2_INP; index++)
   {
      cfg = gen2g_info.inpCfg_p->inpCfg[index];
      if (cfg == STATE_INPUT)
      {
         gen2g_info.stateMask |= (1 << index);
         inpdrv_info.inp[index].state = INP_STATE;
      }
      else if (cfg == RISE_EDGE)
      {
         if (inputs & (1 << index))
         {
            gen2g_info.validSwitch |= (1 << index);
            inpdrv_info.inp[index].state = INP_HIGH;
         }
         else
         {
            inpdrv_info.inp[index].state = INP_LOW;
         }
      }
      else if (cfg == FALL_EDGE)
      {
         if ((inputs & (1 << index)) == 0)
         {
            gen2g_info.validSwitch |= (1 << index);
            inpdrv_info.inp[index].state = INP_LOW;
         }
         else
         {
            inpdrv_info.inp[index].state = INP_HIGH;
         }
      }
   }
   gen2g_info.validSwitch |= (inputs & gen2g_info.stateMask);
} /* End inpdrv_set_init_state */
