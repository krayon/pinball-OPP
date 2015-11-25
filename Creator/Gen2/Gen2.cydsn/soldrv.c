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
 * @file:   soldrv.c
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
 * This file controls the solenoid driver wing board.  It is adapted from
 * digital.c in the previous 1001-SolDrv\Sources\digital.c
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
   SOL_STATE_IDLE             = 0x00,
   SOL_VERIFY_INPUT_VALID     = 0x01,
   SOL_INITIAL_KICK           = 0x02,
   SOL_SUSTAIN_PWM            = 0x03,
   SOL_VERIFY_SWITCH_CLR      = 0x04,
   SOL_MIN_TIME_OFF           = 0x05,
}  SOLDRV_STATE_E;

#define MIN_OFF_INC           0x10

typedef struct
{
   SOLDRV_STATE_E             state;
   U8                         cnt;
   BOOL                       foundClr;
   STDLI_ELAPSED_TIME_T       elapsedTime;
} SOLDRV_SOL_T;

typedef struct
{
   INT                        currInp;
   U16                        solMask;
   SOLDRV_SOL_T               sol[RS232I_NUM_GEN2_SOL];
} SOLDRV_GLOB_T;

SOLDRV_GLOB_T                 soldrv_info;

/*
 * ===============================================================================
 * 
 * Name: soldrv_init
 * 
 * ===============================================================================
 */
/**
 * Initialize the solenoid driver I/O port
 * 
 * Initialize digital I/O port, and other solenoid driver control signals.
 * 
 * @param   None
 * @return  None
 * 
 * @pre     None 
 * @note    Bits 0-3 are inputs, bits 4-7 are outputs.
 * 
 * ===============================================================================
 */
void soldrv_init() 
{
   SOLDRV_SOL_T               *sol_p;
   INT                        index;

#define INPUT_BIT_MASK        0x0f   
#define OUTPUT_BIT_MASK       0xf0
  
   for (sol_p = &soldrv_info.sol[0]; sol_p < &soldrv_info.sol[RS232I_NUM_GEN2_SOL]; sol_p++)
   {
      sol_p->state = SOL_STATE_IDLE;
   }
   
   /* Curr input to an invalid value to be filled out */
   soldrv_info.currInp = RS232I_NUM_GEN2_SOL;
   soldrv_info.solMask = 0;
  
   /* Set up digital ports, walk through wing boards */
   for (index = 0; index < RS232I_NUM_WING; index++)
   {
      /* Check if this wing board is a solenoid driver */
      if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL)
      {
         /* Setup inputs */
         stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, INPUT_BIT_MASK, 0);
         
         /* Setup outputs */
         stdldigio_config_dig_port(index | STDLI_DIG_OUT, OUTPUT_BIT_MASK, 0);
         soldrv_info.solMask |= (0x000f << (index << 2));
         if (soldrv_info.currInp == RS232I_NUM_GEN2_SOL)
         {
            soldrv_info.currInp = (index << 2);
         }
      }
   }
   
   /* Set the location of the configuration data */
   gen2g_info.solDrvCfg_p = (GEN2G_SOL_DRV_CFG_T *)gen2g_info.freeCfg_p;
   gen2g_info.freeCfg_p += sizeof(GEN2G_SOL_DRV_CFG_T);
   gen2g_info.solDrvProcCtl = 0;
   
} /* End soldrv_init */

/*
 * ===============================================================================
 * 
 * Name: soldrv_task
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
void soldrv_task(void)
{
   SOLDRV_SOL_T               *sol_p;
   RS232I_SOL_CFG_T           *solCfg_p;
   U16                        inputs;
   INT                        index;
   BOOL                       switchAct;
   U8                         data;
   BOOL                       foundNextBit;
   INT                        port;
   INT                        bit;
  
#define PWM_PERIOD            16
#define SWITCH_THRESH         50

   if ((gen2g_info.typeWingBrds & (1 << WING_SOL)) != 0)
   {
      /* Grab the solenoid inputs */
      inputs = 0;
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL)
         {
            data = stdldigio_read_port(index, INPUT_BIT_MASK);
            inputs |= (data << (index << 2));
         }
      }
      index = soldrv_info.currInp;
      sol_p = &soldrv_info.sol[index];
      solCfg_p = &gen2g_info.solDrvCfg_p->solCfg[index];
    
      /* If using the switch as a trigger input, check it.  Note: switches active low */
      if ((solCfg_p->cfg & USE_SWITCH) && ((inputs & (1 << index)) == 0))
      {
         switchAct = TRUE;
      }
      else
      {
         switchAct = FALSE;
      }
      
      /* Check if processor is requesting the solenoid to be kicked */
      switchAct = (switchAct || (gen2g_info.solDrvProcCtl & (1 << index)) ? TRUE : FALSE);
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
            if (sol_p->elapsedTime.elapsedTime.usec >= SWITCH_THRESH)
            {
               sol_p->state = SOL_INITIAL_KICK;
               DisableInterrupts;
               /* HRS:  Convert to use 32 bits */
               gen2g_info.validSwitch |= (1 << index);
               EnableInterrupts;
               sol_p->foundClr = FALSE;
               port = index >> 2;
               bit = 1 << (index & 0x3);
               stdldigio_write_port(port, bit, bit);
               stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
          
               /* If this is an autoclear switch, clear the proc bit */
               if (solCfg_p->cfg & AUTO_CLR)
               {
                  gen2g_info.solDrv.procCtl &= ~(1 << index);
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
         if (sol_p->elapsedTime.elapsedTime.msec >= solCfg_p->initKick)
         {
            /* In all cases turn off the solenoid driver */
            port = index >> 2;
            bit = 1 << (index & 0x3);
            stdldigio_write_port(port, bit, 0);
        
            /* See if this has a sustaining PWM */
            if (solCfg_p->minOffDuty & DUTY_CYCLE_MASK)
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
         port = index >> 2;
         bit = 1 << (index & 0x3);
         if (switchAct)
         {
            /* Do slow PWM function, initially off, then on for duty cycle */
            stdltime_get_elapsed_time(&sol_p->elapsedTime);
            if (sol_p->elapsedTime.elapsedTime.msec > PWM_PERIOD)
            {
               /* PWM period is over, clear drive signal */
               stdldigio_write_port(port, bit, 0);
               stdltime_get_curr_time(&sol_p->elapsedTime.startTime);
            }
            else if (sol_p->elapsedTime.elapsedTime.msec >
               PWM_PERIOD - (solCfg_p->minOffDuty & DUTY_CYCLE_MASK))
            {
               stdldigio_write_port(port, bit, bit);
            }
         }
         else
         {
            /* Switch is inactive, turn off drive signal */
            stdldigio_write_port(port, bit, 0);
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
         if (sol_p->elapsedTime.elapsedTime.msec >= solCfg_p->initKick)
         {
            sol_p->cnt += MIN_OFF_INC;
            if (sol_p->cnt >= (solCfg_p->minOffDuty & MIN_OFF_MASK))
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
      DisableInterrupts;
      /* HRS:  Convert to use 32 bits */
      gen2g_info.validSwitch = (gen2g_info.validSwitch & ~gen2g_info.stateMask) |
         (inputs & gen2g_info.stateMask);
      EnableInterrupts;
         
      foundNextBit = FALSE;
      while (!foundNextBit)
      {
         index++;
         if (index >= RS232I_NUM_GEN2_SOL)
         {
            index = 0;
         }
         if ((soldrv_info.solMask & (1 << index)) != 0)
         {
            foundNextBit = TRUE;
         }
      }
      soldrv_info.currInp = index;
  }
} /* End soldrv_task */

/*
 * ===============================================================================
 * 
 * Name: soldrv_set_init_state
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
void soldrv_set_init_state(void)
{
   INT                        index;
                        
   for (index = 0; index < RS232I_NUM_GEN2_SOL; index++)
   {
      if ((gen2g_info.solDrvCfg_p->solCfg[index].cfg & USE_SWITCH) == 0)
      {
         /* HRS:  Convert to use 32 bits */
         gen2g_info.stateMask |= (1 << index);
      }
   }
} /* End soldrv_set_init_state */

/* [] END OF FILE */
