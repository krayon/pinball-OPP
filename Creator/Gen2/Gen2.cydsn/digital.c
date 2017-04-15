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
 * This file controls the digital wing boards (inputs/solenoids).  It is
 * adapted from digital.c in the previous 1003-InpDrv\Sources\digital.c
 *
 *===============================================================================
 */
 
#include <stdlib.h>
#include "stdtypes.h"
#include "stdlintf.h"
#include "rs232intf.h"
#include "gen2glob.h"
#include "procdefs.h"         /* for EnableInterrupts macro */

#define STDL_FILE_ID          3

#define NUM_MATRIX_INP        64
#define NUM_MATRIX_BYTES      8

typedef enum
{
   SOL_STATE_IDLE             = 0x00,
   SOL_INITIAL_KICK           = 0x01,
   SOL_SUSTAIN_PWM            = 0x02,
   SOL_MIN_TIME_OFF           = 0x03,
   SOL_WAIT_BEFORE_KICK       = 0x04,
   SOL_FULL_ON_SOLENOID       = 0x05,
} __attribute__((packed)) DIG_SOL_STATE_E;

typedef struct
{
   BOOL                       clearRcvd;
   DIG_SOL_STATE_E            solState;
   U8                         offCnt;
   U8                         port;
   U8                         bit;
   INT                        startMs;
   U32                        inpBits;
} DIG_SOL_STATE_T;

typedef struct
{
   INT                        cnt;
} DIG_INP_STATE_T;

#define MATRIX_FIRE_SOL       0x80
#define MATRIX_SOL_MASK       0x07

typedef struct
{
   U8                         cnt;
   U8                         sol;
} DIG_MTRX_BIT_INFO_T;

typedef struct
{
   U8                         index;
   U8                         prevVal[NUM_MATRIX_BYTES];
   DIG_MTRX_BIT_INFO_T        info[NUM_MATRIX_INP];
} DIG_MATRIX_DATA_T;

typedef struct
{
   U32                        inpMask;
   U32                        prevInputs;
   U32                        filtInputs;
   U32                        stateMask;
   DIG_MATRIX_DATA_T          *matrix_p;
   DIG_INP_STATE_T            inpState[RS232I_NUM_GEN2_INP];
   DIG_SOL_STATE_T            solState[RS232I_NUM_GEN2_SOL];
} DIG_GLOB_T;

DIG_GLOB_T                    dig_info;

/* Prototypes */
INT timer_get_ms_count();
void digital_set_solenoid_input(
   RS232I_SET_SOL_INP_E       inputIndex,
   U8                         solIndex);
void digital_upd_sol_cfg(
   U16                        updMask);
void digital_upd_inp_cfg(
   U32                        updMask);

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
   DIG_SOL_STATE_T            *solState_p;
   INT                        index;
   BOOL                       foundSol = FALSE;
   RS232I_CFG_INP_TYPE_E      *inpCfg_p;
   U16                        solMask = 0;
   U8                         data;
   RS232I_SOL_CFG_T           *solCfg_p;
   U32                        currBit;

#define INPUT_BIT_MASK        0xff   
#define SOL_INP_BIT_MASK      0x0f  
#define SOL_OUTP_BIT_MASK     0xf0  
   
   if (gen2g_info.inpCfg_p == NULL)
   {
      for (solState_p = &dig_info.solState[0], index = 0;
         index < RS232I_NUM_GEN2_SOL; index++, solState_p++)
      {
         solState_p->solState = SOL_STATE_IDLE;
         solState_p->port = index >> 2;
         solState_p->bit = 1 << ((index & 0x03) + 4);
         solState_p->inpBits = 0;
      }
      dig_info.inpMask = 0;
      dig_info.filtInputs = 0;
     
      /* Set up digital ports, walk through wing boards */
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         /* Check if this wing board is a input driver */
         if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_INP)
         {
            /* Setup inputs */
#if PIONEER_DEBUG == 0
            stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, INPUT_BIT_MASK, 0);
#else
            /* If using the Pioneer debugger, don't change SWDIO/SWDCLK */
            if (index == 3)
            {
               stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, 0xf3, 0);
            }
            else
            {
               stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, INPUT_BIT_MASK, 0);
            }
#endif
            
            /* Set up bit mask of valid inputs */
            dig_info.inpMask |= (INPUT_BIT_MASK << (index << 3));
         }
         /* Check if this wing board is a solenoid driver */
         else if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL)
         {
            foundSol = TRUE;
            
            /* Setup inputs/outputs */
#if PIONEER_DEBUG == 0
            stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, SOL_INP_BIT_MASK, 0);
#else
            /* If using the Pioneer debugger, don't change SWDIO/SWDCLK */
            if (index == 3)
            {
               stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, 0x03, 0);
            }
            else
            {
               stdldigio_config_dig_port(index | STDLI_DIG_PULLUP, SOL_INP_BIT_MASK, 0);
            }
#endif
            stdldigio_config_dig_port(index | STDLI_DIG_OUT, SOL_OUTP_BIT_MASK, 0);
            
            /* Set up bit mask of valid inputs */
            dig_info.inpMask |= (SOL_INP_BIT_MASK << (index << 3));
            solMask |= (SOL_INP_BIT_MASK << (index << 2));
         }
         /* Check if wing 2 is WING_SW_MATRIX_IN, and wing 3 is WING_SW_MATRIX_OUT */
         else if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SW_MATRIX_IN)
         {
            if (index == 2)
            {
               dig_info.matrix_p = malloc(sizeof(DIG_MATRIX_DATA_T));
               dig_info.matrix_p->index = 0;
               stdldigio_config_dig_port(STDLI_DIG_PORT_2 | STDLI_DIG_PULLDWN, 0xff, 0x01);
#if PIONEER_DEBUG == 0
               stdldigio_config_dig_port(STDLI_DIG_PORT_3 | STDLI_DIG_OUT, 0xff, 0);
#else
               /* If using the Pioneer debugger, don't change SWDIO/SWDCLK */
               stdldigio_config_dig_port(STDLI_DIG_PORT_3 | STDLI_DIG_OUT, 0xf3, 0);
#endif
            }
         }
         data = stdldigio_read_port(index, 0xff);
         dig_info.filtInputs |= (data << (index << 3));
      }
      dig_info.filtInputs &= dig_info.inpMask;
      
      /* Set the location of the configuration data */
      gen2g_info.inpCfg_p = (GEN2G_INP_CFG_T *)gen2g_info.freeCfg_p;
      gen2g_info.freeCfg_p += sizeof(GEN2G_INP_CFG_T);
      if (foundSol)
      {
         gen2g_info.solDrvCfg_p = (GEN2G_SOL_DRV_CFG_T *)gen2g_info.freeCfg_p;
         gen2g_info.freeCfg_p += sizeof(GEN2G_SOL_DRV_CFG_T);
      }
      
      /* Set up initial configuration of solenoids from NV config */
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_SOL)
         {
            /* Configure the inputs for the solenoids */
            for (inpCfg_p = &gen2g_info.inpCfg_p->inpCfg[index << 3];
               inpCfg_p < &gen2g_info.inpCfg_p->inpCfg[(index << 3) + 8];
               inpCfg_p++)
            {
               *inpCfg_p = STATE_INPUT;
            }
         }
      }

      /* If a matrix wing exists, set up the solenoid inputs */
      if ((gen2g_info.typeWingBrds & (1 << WING_SW_MATRIX_IN)) != 0)
      {
         /* Initialize the counts and solenoid info */
         for (index = 0; index < RS232I_SW_MATRX_INP; index++)
         {
            dig_info.matrix_p->info[index].cnt = 0;
            dig_info.matrix_p->info[index].sol = 0;
         }
         /* Set up the solenoids to autofire using the switch matrix */
         for (index = 0, currBit = 1, solCfg_p = &gen2g_info.solDrvCfg_p->solCfg[0];
            index < RS232I_NUM_GEN2_SOL; index++, currBit <<= 1, solState_p++, solCfg_p++)
         {
            if (solCfg_p->cfg & USE_MATRIX_INP)
            {
               dig_info.matrix_p->info[solCfg_p->minOffDuty].sol = MATRIX_FIRE_SOL | index;
            }
         }
      }
      
      /* Set up the initial state */
      digital_upd_sol_cfg(solMask);
      digital_upd_inp_cfg(dig_info.inpMask);
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
   DIG_MTRX_BIT_INFO_T        *matrixBitInfo_p;
   U32                        inputs;
   U32                        changedBits;
   U32                        updFilterHi;
   U32                        updFilterLow;
   INT                        index;
   U8                         data;
   U8                         chngU8;
   RS232I_CFG_INP_TYPE_E      cfg;
   INT                        shift;
   U32                        currBit;
   INT                        elapsedTimeMs;

#define SWITCH_THRESH         16
#define MATRIX_THRESH         4
#define PWM_PERIOD            16
#define MIN_OFF_INC           0x10
   
   if (gen2g_info.validCfg)
   {
      if ((gen2g_info.typeWingBrds & ((1 << WING_INP) | (1 << WING_SOL))) != 0)
      {
         /* Grab the inputs */
         inputs = 0;
         for (index = 0, shift = 0; index < RS232I_NUM_WING; index++, shift += 8)
         {
            data = stdldigio_read_port(index, 0xff);
            inputs |= (data << shift);
         }
         inputs &= dig_info.inpMask;
         
         /* See what bits have changed */
         changedBits = (dig_info.prevInputs ^ inputs) & dig_info.inpMask;
         updFilterHi = 0;
         updFilterLow = 0;
         
         /* Perform input processing for both input and solenoid boards */
         for (index = 0, currBit = 1, inpState_p = &dig_info.inpState[0];
            index < RS232I_NUM_GEN2_INP; index++, currBit <<= 1, inpState_p++)
         {
            if (currBit & dig_info.inpMask)
            {
               /* Check if this count has changed */
               if (changedBits & currBit)
               {
                  inpState_p->cnt = 0;
               }
               else
               {
                  if (inpState_p->cnt <= SWITCH_THRESH)
                  {
                     inpState_p->cnt++;
                  }
                  if (inpState_p->cnt == SWITCH_THRESH)
                  {
                     cfg = gen2g_info.inpCfg_p->inpCfg[index];
                     if (inputs & currBit)
                     {
                        updFilterHi |= currBit;
                        dig_info.filtInputs |= currBit;
                        if (cfg == RISE_EDGE)
                        {
                           DisableInterrupts;
                           gen2g_info.validSwitch |= currBit;
                           EnableInterrupts;
                        }
                     }
                     else
                     {
                        updFilterLow |= currBit;
                        dig_info.filtInputs &= ~currBit;
                        if (cfg == FALL_EDGE)
                        {
                           DisableInterrupts;
                           gen2g_info.validSwitch |= currBit;
                           EnableInterrupts;
                        }
                     }
                  }
               }
            }
         }
      }

      if ((gen2g_info.typeWingBrds & (1 << WING_SW_MATRIX_IN)) != 0)
      {
         data = stdldigio_read_port(STDLI_DIG_PORT_2, 0xff);
         chngU8 = data ^ dig_info.matrix_p->prevVal[dig_info.matrix_p->index];
         dig_info.matrix_p->prevVal[dig_info.matrix_p->index] = data;
         matrixBitInfo_p = &dig_info.matrix_p->info[dig_info.matrix_p->index * 8];
         for (index = 0, currBit = 1; index < 8; index++, currBit <<= 1, matrixBitInfo_p++)
         {
            /* If bit has changed, reset count */
            if ((currBit & chngU8) != 0)
            {
               matrixBitInfo_p->cnt = 0;
            }
            else
            {
               if (matrixBitInfo_p->cnt <= MATRIX_THRESH)
               {
                  matrixBitInfo_p->cnt++;
               }
               /* Just passed the threshold so update data byte */
               if (matrixBitInfo_p->cnt == MATRIX_THRESH)
               {
                  if (data & currBit)
                  {
                     gen2g_info.matrixInp[dig_info.matrix_p->index] |= currBit;
                     if (matrixBitInfo_p->sol != 0)
                     {
                        gen2g_info.solDrvProcCtl |=
                           (1 << (matrixBitInfo_p->sol & MATRIX_SOL_MASK));
                     }
                  }
                  else
                  {
                     gen2g_info.matrixInp[dig_info.matrix_p->index] &= ~currBit;
                  }
               }
            }
         }
         /* Move to next column */
         dig_info.matrix_p->index++;
         if (dig_info.matrix_p->index >= RS232I_MATRX_COL)
         {
            dig_info.matrix_p->index = 0;
         }
         stdldigio_write_port(STDLI_DIG_PORT_3, 0xff, (U8)(1 << dig_info.matrix_p->index));
      }
      
      if ((gen2g_info.typeWingBrds & (1 << WING_SOL)) != 0)
      {
        /* Perform solenoid processing */
         for (index = 0, currBit = 1, solState_p = &dig_info.solState[0],
            solCfg_p = &gen2g_info.solDrvCfg_p->solCfg[0];
            index < RS232I_NUM_GEN2_SOL; index++, currBit <<= 1, solState_p++, solCfg_p++)
         {
            /* Check if processor is requesting a kick, or an input changed */
            if ((solState_p->solState == SOL_STATE_IDLE) &&
               ((gen2g_info.solDrvProcCtl & currBit) ||
               (updFilterLow & solState_p->inpBits)))
            {
               /* Check if processor is kicking normal solenoid */
               if ((solCfg_p->cfg & (ON_OFF_SOL | DLY_KICK_SOL)) == 0)
               {
                  /* Start the solenoid kick */
                  solState_p->solState = SOL_INITIAL_KICK;
                  solState_p->startMs = timer_get_ms_count();
                  stdldigio_write_port(solState_p->port, solState_p->bit,
                     solState_p->bit);
               }
               else if ((solCfg_p->cfg & ON_OFF_SOL) != 0)
               {
                  solState_p->solState = SOL_FULL_ON_SOLENOID;
                  stdldigio_write_port(solState_p->port, solState_p->bit,
                     solState_p->bit);
               }
               else if ((solCfg_p->cfg & DLY_KICK_SOL) != 0)
               {
                  solState_p->solState = SOL_WAIT_BEFORE_KICK;
                  solState_p->startMs = timer_get_ms_count();
               }
               if ((solCfg_p->cfg & AUTO_CLR) &&
                  (gen2g_info.solDrvProcCtl & currBit))
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
               elapsedTimeMs = timer_get_ms_count() - solState_p->startMs;
               if (elapsedTimeMs >= solCfg_p->initKick)
               {
                  /* In all cases turn off the solenoid driver */
                  stdldigio_write_port(solState_p->port, solState_p->bit, 0);

                  /* If this is a normal solenoid */
                  if ((solCfg_p->cfg & (ON_OFF_SOL | DLY_KICK_SOL | USE_MATRIX_INP)) == 0)
                  {
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
                  }
                  else if ((solCfg_p->cfg & (DLY_KICK_SOL | USE_MATRIX_INP)) != 0)
                  {
                     solState_p->solState = SOL_MIN_TIME_OFF;
                     solState_p->offCnt = 0;
                  }
                  solState_p->startMs = timer_get_ms_count();
               }
            }
            else if (solState_p->solState == SOL_SUSTAIN_PWM)
            {
               if (((gen2g_info.solDrvProcCtl & currBit) == 0) &&
                 ((solState_p->inpBits & inputs) != 0))
               {
                  solState_p->clearRcvd = TRUE;
               }
               if (!solState_p->clearRcvd)
               {
                  /* Do slow PWM function, initially off, then on for duty cycle */
                  elapsedTimeMs = timer_get_ms_count() - solState_p->startMs;
                  if (elapsedTimeMs > PWM_PERIOD)
                  {
                     /* PWM period is over, clear drive signal */
                     stdldigio_write_port(solState_p->port, solState_p->bit, 0);
                     solState_p->startMs = timer_get_ms_count();
                  }
                  else if (elapsedTimeMs > PWM_PERIOD - (solCfg_p->minOffDuty & DUTY_CYCLE_MASK))
                  {
                     stdldigio_write_port(solState_p->port, solState_p->bit,
                        solState_p->bit);
                  }
               }
               else
               {
                  /* Switch is inactive, turn off drive signal */
                  stdldigio_write_port(solState_p->port, solState_p->bit, 0);
                  solState_p->solState = SOL_STATE_IDLE;
               }
            }
            else if (solState_p->solState == SOL_MIN_TIME_OFF)
            {
               /* Check if an off time increment has happened */
               elapsedTimeMs = timer_get_ms_count() - solState_p->startMs;
               if (elapsedTimeMs >= solCfg_p->initKick)
               {
                  solState_p->offCnt += MIN_OFF_INC;
                  if (solState_p->offCnt >= (solCfg_p->minOffDuty & MIN_OFF_MASK))
                  {
                     solState_p->solState = SOL_STATE_IDLE;
                  }
                  else
                  {
                     solState_p->startMs = timer_get_ms_count();
                  }
               }
            }
            else if (solState_p->solState == SOL_WAIT_BEFORE_KICK)
            {
               /* Check if elapsed time is over the wait time
                * (stored in duty cycle nibble * 2)
                */
               elapsedTimeMs = timer_get_ms_count() - solState_p->startMs;
               if (elapsedTimeMs >= ((solCfg_p->minOffDuty & DUTY_CYCLE_MASK) << 1))
               {
                  /* Start the solenoid kick */
                  solState_p->solState = SOL_INITIAL_KICK;
                  solState_p->startMs = timer_get_ms_count();
                  stdldigio_write_port(solState_p->port, solState_p->bit,
                        solState_p->bit);
               }
            }
            else if (solState_p->solState == SOL_FULL_ON_SOLENOID)
            {
               if (((gen2g_info.solDrvProcCtl & currBit) == 0) &&
                 ((solState_p->inpBits & inputs) != 0))
               {
                  /* Switch is inactive, turn off drive signal */
                  stdldigio_write_port(solState_p->port, solState_p->bit, 0);
                  solState_p->solState = SOL_STATE_IDLE;
               }
            }
         }
      }

      if ((gen2g_info.typeWingBrds & ((1 << WING_INP) | (1 << WING_SOL))) != 0)
      {
         DisableInterrupts;
         gen2g_info.validSwitch = (gen2g_info.validSwitch & ~dig_info.stateMask) |
            (dig_info.filtInputs & dig_info.stateMask);
         EnableInterrupts;
         dig_info.prevInputs = inputs;
      }
   }
} /* End digital_task */

/*
 * ===============================================================================
 * 
 * Name: digital_set_solenoid_input
 * 
 * ===============================================================================
 */
/**
 * Set a solenoid input
 *
 * Set a solenoid input.  To disable a solenoid, the input solenoid number can be
 * set to SOL_INP_CLEAR_SOL.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    If multiple inputs are used to fire a solenoid, the inputs are
 *    logically OR'd together.
 * 
 * ===============================================================================
 */
void digital_set_solenoid_input(
   U8                         inpIndex,
   RS232I_SET_SOL_INP_E       solIndex)
{
   DIG_SOL_STATE_T            *solState_p;
   
   if (inpIndex < RS232I_NUM_GEN2_INP)
   {
      solState_p = &dig_info.solState[solIndex & SOL_INP_SOL_MASK];
      if ((solIndex & SOL_INP_CLEAR_SOL) == 0)
      {
         solState_p->inpBits |= (1 << inpIndex);
      }
      else
      {
         solState_p->inpBits &= ~(1 << inpIndex);
      }
   }
   else
   {
      /* Inputs 32 to 96 are from the switch matrix, first verify
       * there is a switch matrix.
       */
      if ((gen2g_info.typeWingBrds & (1 << WING_SW_MATRIX_IN)) != 0)
      {
         if ((solIndex & SOL_INP_CLEAR_SOL) == 0)
         {
            dig_info.matrix_p->info[inpIndex - RS232I_NUM_GEN2_INP].sol = 0;
         }
         else
         {
            dig_info.matrix_p->info[inpIndex - RS232I_NUM_GEN2_INP].sol =
               MATRIX_FIRE_SOL | (solIndex & SOL_INP_SOL_MASK);
         }
      }
   }
} /* End digital_set_solenoid_input */

/*
 * ===============================================================================
 * 
 * Name: digital_upd_sol_cfg
 * 
 * ===============================================================================
 */
/**
 * Update solenoid configuration
 *
 * Update a solenoid configuration.
 * 
 * @param   updMask - Mask of solenoids to be updated. 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_upd_sol_cfg(
   U16                        updMask)
{
   INT                        index;
   INT                        currBit;
   DIG_SOL_STATE_T            *solState_p;
   RS232I_SOL_CFG_T           *solDrvCfg_p;
   DIG_INP_STATE_T            *inpState_p;
   
   /* Clear the solenoid state machines */
   for (index = 0, solState_p = &dig_info.solState[0], currBit = 1;
      index < RS232I_NUM_GEN2_SOL; index++, solState_p++, currBit <<= 1)
   {
      if ((updMask & currBit) != 0)
      {
         solState_p->solState = SOL_STATE_IDLE;
         solDrvCfg_p = &gen2g_info.solDrvCfg_p->solCfg[index];
         if (solDrvCfg_p->cfg & USE_SWITCH)
         {
            inpState_p = &dig_info.inpState[((index & 0x0c) << 1) + (index & 0x03)];
            inpState_p->cnt = 0;
            solState_p->inpBits |= (1 << (((index & 0x0c) << 1) + (index & 0x03)));
         }
         else
         {
            solState_p->inpBits &= ~(1 << (((index & 0x0c) << 1) + (index & 0x03)));
         }
      }
   }
} /* End digital_upd_sol_cfg */

/*
 * ===============================================================================
 * 
 * Name: digital_upd_inp_cfg
 * 
 * ===============================================================================
 */
/**
 * Update input configuration
 *
 * Update an input configuration.
 * 
 * @param   updMask - Mask of inputs to be updated. 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_upd_inp_cfg(
   U32                        updMask)
{
   INT                        index;
   INT                        currBit;
   DIG_INP_STATE_T            *inpState_p;
   RS232I_CFG_INP_TYPE_E      *inpCfg_p;
   
   /* Clear the input counts */
   for (index = 0, inpState_p = &dig_info.inpState[0],
      inpCfg_p = &gen2g_info.inpCfg_p->inpCfg[0], currBit = 1;
      index < RS232I_NUM_GEN2_INP;
      index++, inpState_p++, inpCfg_p++, currBit <<= 1)
   {
      if ((updMask & currBit) != 0)
      {
         inpState_p->cnt = 0;
         if (*inpCfg_p == STATE_INPUT)
         {
            dig_info.stateMask |= currBit;
         }
         else
         {
            dig_info.stateMask &= ~currBit;
         }
      }
   }
} /* End digital_upd_inp_cfg */
