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
 * @file:   digital.c
 * @author: Hugh Spahr
 * @date:   12/02/2012
 *
 * @note:   Open Pinball Project
 *          Copyrightę 2012-2015, Hugh Spahr
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
 * This file controls the digital wing boards (inputs/solenoids).  It is
 * adapted from digital.c in the previous 1003-InpDrv\Sources\digital.c
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
   SOL_INITIAL_KICK           = 0x01,
   SOL_SUSTAIN_PWM            = 0x02,
   SOL_MIN_TIME_OFF           = 0x03,
} __attribute__((packed)) DIG_SOL_STATE_E;

typedef struct
{
   BOOL                       clearRcvd;
   DIG_SOL_STATE_E            solState;
   U8                         offCnt;
   STDLI_ELAPSED_TIME_T       elapsedTime;
} DIG_SOL_STATE_T;

typedef struct
{
   BOOL                       inpHigh;
   DIG_SOL_STATE_T            *solState_p;
   INT                        cnt;
} DIG_INP_STATE_T;

typedef struct
{
   U32                        inpMask;
   U32                        oldState;
   U32                        stateMask;
   DIG_INP_STATE_T            inpState[RS232I_NUM_GEN2_INP];
   DIG_SOL_STATE_T            solState[RS232I_NUM_GEN2_SOL];
} DIG_GLOB_T;

DIG_GLOB_T                    dig_info;

/* Prototypes */
void digital_set_init_state();

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
   DIG_INP_STATE_T            *inpState_p;
   DIG_SOL_STATE_T            *solState_p;
   INT                        index;
   BOOL                       foundSol = FALSE;

#define INPUT_BIT_MASK        0xff   
#define SOL_INP_BIT_MASK      0x0f  
#define SOL_OUTP_BIT_MASK     0xf0  
   
   if (gen2g_info.inpCfg_p == NULL)
   {
      for (inpState_p = &dig_info.inpState[0];
         inpState_p < &dig_info.inpState[RS232I_NUM_GEN2_INP]; inpState_p++)
      {
         inpState_p->solState_p = NULL;
      }
      for (solState_p = &dig_info.solState[0];
         solState_p < &dig_info.solState[RS232I_NUM_GEN2_SOL]; solState_p++)
      {
         solState_p->solState = SOL_STATE_IDLE;
      }
      dig_info.inpMask = 0;
     
      /* Set up digital ports, walk through wing boards */
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         /* Check if this wing board is a input driver */
         if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP)
         {
            /* Setup inputs */
            stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, INPUT_BIT_MASK, 0);
            
            /* Set up bit mask of valid inputs */
            dig_info.inpMask |= (INPUT_BIT_MASK << (index << 3));
         }
         /* Check if this wing board is a solenoid driver */
         else if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL)
         {
            foundSol = TRUE;
            
            /* Setup inputs/outputs */
            stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, SOL_INP_BIT_MASK, 0);
            stdldigio_config_dig_port(index | STDLI_DIG_OUT, SOL_OUTP_BIT_MASK, 0);
            
            /* Set up bit mask of valid inputs */
            dig_info.inpMask |= (SOL_INP_BIT_MASK << (index << 3));
         }
      }
      
      /* Set the location of the configuration data */
      gen2g_info.inpCfg_p = (GEN2G_INP_CFG_T *)gen2g_info.freeCfg_p;
      gen2g_info.freeCfg_p += sizeof(GEN2G_INP_CFG_T);
      if (foundSol)
      {
         gen2g_info.solDrvCfg_p = (GEN2G_SOL_DRV_CFG_T *)gen2g_info.freeCfg_p;
         gen2g_info.freeCfg_p += sizeof(GEN2G_SOL_DRV_CFG_T);
      }
      
      /* Set up the initial state */
      digital_set_init_state();
   }

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
   DIG_INP_STATE_T            *inpState_p;
   DIG_SOL_STATE_T            *solState_p;
   RS232I_SOL_CFG_T           *solCfg_p;
   U32                        inputs;
   U32                        changedBits;
   U32                        filtState;
   INT                        index;
   U8                         data;
   RS232I_CFG_INP_TYPE_E      cfg;
   INT                        shift;
   U32                        currBit;

#define SWITCH_THRESH         16
#define PWM_PERIOD            16
#define MIN_OFF_INC           0x10
   
   if ((gen2g_info.typeWingBrds & ((1 << WING_INP) | (1 << WING_SOL))) != 0)
   {
      /* Grab the inputs */
      inputs = 0;
      for (index = 0, shift = 0; index < RS232I_NUM_WING; index++, shift += 8)
      {
         /* Grab all 8 bits for both inputs and solenoids so solenoid
          * drive bits can also be read.
          */
         if ((gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP) ||
            (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL))
         {
            data = stdldigio_read_port(index, 0xff);
            inputs |= (data << shift);
         }
      }
      
      /* See what bits have changed */
      changedBits = dig_info.oldState ^ inputs;
      filtState = 0;
      
      /* Perform input processing for both input and solenoid boards */
      for (index = 0, currBit = 1, inpState_p = &dig_info.inpState[0];
         index < RS232I_NUM_GEN2_INP; index++, currBit <<= 1, inpState_p++)
      {
         if (currBit & dig_info.inpMask)
         {
            /* Check if this count has changed */
            if (changedBits & shift)
            {
               inpState_p->cnt = 0;
            }
            else
            {
               inpState_p->cnt++;
               if (inpState_p->cnt == SWITCH_THRESH)
               {
                  if (inputs & currBit)
                  {
                     inpState_p->inpHigh = TRUE;
                  }
                  else
                  {
                     inpState_p->inpHigh = FALSE;
                  }
                  solState_p = inpState_p->solState_p;
                  cfg = gen2g_info.inpCfg_p->inpCfg[index];
                  if (((cfg == FALL_EDGE) && ((inputs & currBit) == 0)) ||
                     ((cfg == RISE_EDGE) && ((inputs & currBit) != 0)))
                  {
                     DisableInterrupts;
                     gen2g_info.validSwitch |= currBit;
                     EnableInterrupts;
                  }

                  /* Check if this input is for a solenoid */
                  if (solState_p != NULL)
                  {
                     /* If falling edge, and state is idle */
                     if (((inputs & currBit) == 0) && (solState_p->solState == SOL_STATE_IDLE))
                     {
                        /* Start the solenoid kick */
                        solState_p->solState = SOL_INITIAL_KICK;
                        solState_p->clearRcvd = FALSE;
                        stdltime_get_curr_time(&solState_p->elapsedTime.startTime);
                        stdldigio_write_port(index >> 3, 1 << ((index & 0x03) + 4),
                           1 << ((index & 0x03) + 4));
                     }
                     /* Otherwise if rising edge */
                     else if ((inputs & currBit) != 0)
                     {
                        solState_p->clearRcvd = TRUE;
                     }
                  }
               }
            }
            if (inpState_p->inpHigh)
            {
               filtState |= currBit;
            }
         }
      }
      
      /* Perform solenoid processing */
      for (index = 0, currBit = 1, solState_p = &dig_info.solState[0],
         solCfg_p = &gen2g_info.solDrvCfg_p->solCfg[index];
         index < RS232I_NUM_GEN2_SOL; index++, currBit <<= 1, solState_p++, solCfg_p++)
      {
         /* Check if processor is requesting a kick */
         if ((solState_p->solState == SOL_STATE_IDLE) &&
            (gen2g_info.solDrvProcCtl & currBit))
         {
            /* Start the solenoid kick */
            solState_p->solState = SOL_INITIAL_KICK;
            stdltime_get_curr_time(&solState_p->elapsedTime.startTime);
            stdldigio_write_port(index >> 2, 1 << ((index & 0x03) + 4),
               1 << ((index & 0x03) + 4));
            if (solCfg_p->cfg & AUTO_CLR)
            {
               gen2g_info.solDrvProcCtl &= ~currBit;
               solState_p->clearRcvd = TRUE;
            }
            else
            {
               solState_p->clearRcvd = FALSE;
            }
         }
         else if (solState_p->solState == SOL_INITIAL_KICK)
         {
            /* Check if elapsed time is over initial kick time */
            stdltime_get_elapsed_time(&solState_p->elapsedTime);
            if (solState_p->elapsedTime.elapsedTime.msec >= solCfg_p->initKick)
            {
               /* In all cases turn off the solenoid driver */
               stdldigio_write_port(index >> 2, 1 << ((index & 0x03) + 4), 0);
           
               /* See if this has a sustaining PWM */
               if (solCfg_p->minOffDuty & DUTY_CYCLE_MASK)
               {
                  /* Make sure the input continues to be set */
                  if (solState_p->clearRcvd)
                  {
                     solState_p->solState = SOL_MIN_TIME_OFF;
                     solState_p->offCnt = 0;
                  }
                  else
                  {
                     solState_p->solState = SOL_SUSTAIN_PWM;
                  }              
               }
               else
               {
                  solState_p->solState = SOL_MIN_TIME_OFF;
                  solState_p->offCnt = 0;
               }
               stdltime_get_curr_time(&solState_p->elapsedTime.startTime);
            }
         }
         else if (solState_p->solState == SOL_SUSTAIN_PWM)
         {
            if (!solState_p->clearRcvd)
            {
               /* Do slow PWM function, initially off, then on for duty cycle */
               stdltime_get_elapsed_time(&solState_p->elapsedTime);
               if (solState_p->elapsedTime.elapsedTime.msec > PWM_PERIOD)
               {
                  /* PWM period is over, clear drive signal */
                  stdldigio_write_port(index >> 2, 1 << ((index & 0x03) + 4), 0);
                  stdltime_get_curr_time(&solState_p->elapsedTime.startTime);
               }
               else if (solState_p->elapsedTime.elapsedTime.msec >
                  PWM_PERIOD - (solCfg_p->minOffDuty & DUTY_CYCLE_MASK))
               {
                  stdldigio_write_port(index >> 2, 1 << ((index & 0x03) + 4),
                     1 << ((index & 0x03) + 4));
               }
            }
            else
            {
               /* Switch is inactive, turn off drive signal */
               stdldigio_write_port(index >> 2, 1 << ((index & 0x03) + 4), 0);
               solState_p->solState = SOL_STATE_IDLE;
            }
         }
         else if (solState_p->solState == SOL_MIN_TIME_OFF)
         {
            /* Check if an off time increment has happened */
            stdltime_get_elapsed_time(&solState_p->elapsedTime);
            if (solState_p->elapsedTime.elapsedTime.msec >= solCfg_p->initKick)
            {
               solState_p->offCnt += MIN_OFF_INC;
               if (solState_p->offCnt >= (solCfg_p->minOffDuty & MIN_OFF_MASK))
               {
                  solState_p->solState = SOL_STATE_IDLE;
               }
               else
               {
                  stdltime_get_curr_time(&solState_p->elapsedTime.startTime);
               }
            }
         }
      }

      DisableInterrupts;
      gen2g_info.validSwitch = (gen2g_info.validSwitch & ~dig_info.stateMask) |
         (filtState & dig_info.stateMask);
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
 * Set the initial input/solenoid state after a config command was received.
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
   DIG_INP_STATE_T            *inpState_p;
   DIG_SOL_STATE_T            *solState_p;
   RS232I_SOL_CFG_T           *solDrvCfg_p;
   RS232I_CFG_INP_TYPE_E      *inpCfg_p;
   U32                        inputs;
   INT                        index;
   U8                         data;
   INT                        currBit;
  
   /* Grab the inputs */
   inputs = 0;
   for (index = 0; index < RS232I_NUM_WING; index++)
   {
      if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP)
      {
         data = stdldigio_read_port(index, INPUT_BIT_MASK);
      }
      else if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL)
      {
         /* Configure the inputs for the solenoids */
         for (solDrvCfg_p = &gen2g_info.solDrvCfg_p->solCfg[index << 2],
            inpCfg_p = &gen2g_info.inpCfg_p->inpCfg[index << 3],
            inpState_p = &dig_info.inpState[index << 3],
            solState_p = &dig_info.solState[index << 2];
            inpCfg_p < &gen2g_info.inpCfg_p->inpCfg[(index << 3) + 4];
            solDrvCfg_p++, inpCfg_p++, inpState_p++, solState_p++)
         {
            if (solDrvCfg_p->cfg & USE_SWITCH)
            {
               *inpCfg_p = FALL_EDGE;
               inpState_p->solState_p = solState_p;
            }
            else
            {
               *inpCfg_p = STATE_INPUT;
               inpState_p->solState_p = NULL;
            }
         }
         /* Configure the outputs to the solenoids as state bits */
         for (inpCfg_p = &gen2g_info.inpCfg_p->inpCfg[(index << 3) + 4],
            inpState_p = &dig_info.inpState[(index << 3) + 4];
            inpCfg_p < &gen2g_info.inpCfg_p->inpCfg[(index << 3) + 8];
            inpCfg_p++, inpState_p++)
         {
            *inpCfg_p = STATE_INPUT;
            inpState_p->solState_p = NULL;
         }
         data = stdldigio_read_port(index, SOL_INP_BIT_MASK);
         stdldigio_write_port(index, SOL_OUTP_BIT_MASK, 0);
      }
      inputs |= (data << (index << 3));
   }

   /* Clear the solenoid state machines */
   for (index = 0, solState_p = &dig_info.solState[0], currBit = 1;
      index < RS232I_NUM_GEN2_SOL; index++, solState_p++, currBit <<= 1)
   {
      solState_p->solState = SOL_STATE_IDLE;
   }
   
   dig_info.stateMask = 0;
   for (index = 0, inpState_p = &dig_info.inpState[0],
      inpCfg_p = &gen2g_info.inpCfg_p->inpCfg[0], currBit = 1;
      index < RS232I_NUM_GEN2_INP;
      index++, inpState_p++, inpCfg_p++, currBit <<= 1)
   {
      /* validSwitch will get triggered when threshold is crossed in normal processing */
      inpState_p->cnt = 0;
      if (inputs & (1 << index))
      {
         inpState_p->inpHigh = TRUE;
      }
      else
      {
         inpState_p->inpHigh = FALSE;
      }
      
      if (*inpCfg_p == STATE_INPUT)
      {
         dig_info.stateMask |= (1 << index);
      }
   }
   gen2g_info.validSwitch = (inputs & dig_info.stateMask);
} /* End digital_set_init_state */
