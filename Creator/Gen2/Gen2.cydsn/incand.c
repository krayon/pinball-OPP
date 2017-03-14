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
 * @file:   incand.c
 * @author: Hugh Spahr
 * @date:   12/17/2015
 *
 * @note:   Open Pinball Project
 *          Copyright© 2015, Hugh Spahr
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
 * This is the file for driving the incandescent wing boards.  It requires
 * a 40ms tick for the blinking.  The blinks should be synchronized across
 * all the boards so look nice.
 *
 *===============================================================================
 */
#include <stdlib.h>
#include "stdtypes.h"
#include "gen2glob.h"
    
typedef struct
{
   BOOL              startProc;
   U8                validMask;
   U8                invertMask;  /* 1 if wing is high side incand */
   U8                prevSynch;
   U32               ledOnBitfield;
   U32               ledBlinkSlowBitfield;
   U32               ledBlinkFastBitfield;
} INCAND_INFO;

INCAND_INFO incandInfo;

/*
 * ===============================================================================
 * 
 * Name: incand_init
 * 
 * ===============================================================================
 */
/**
 * Initialize the incandescent driver
 * 
 * @param   None
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void incand_init()
{
   INT                        index;
   
   incandInfo.startProc = FALSE;
   incandInfo.validMask = 0;
   incandInfo.invertMask = 0;
   incandInfo.ledOnBitfield = 0;
   incandInfo.ledBlinkSlowBitfield = 0;
   incandInfo.ledBlinkFastBitfield = 0;
   
   /* Set up digital ports, walk through wing boards */
   for (index = 0; index < RS232I_NUM_WING; index++)
   {
      /* Check if this wing board is a incandescent wing board */
      if ((gen2g_info.nvCfgInfo.wingCfg[index] == WING_INCAND) ||
         (gen2g_info.nvCfgInfo.wingCfg[index] == WING_HI_SIDE_INCAND))
      {
         /* If high side incandescent wing, invert outputs */
         if (gen2g_info.nvCfgInfo.wingCfg[index] == WING_HI_SIDE_INCAND)
         {
            incandInfo.invertMask |= (1 << index);
         }
         
         /* Initial setup blinks all the lights */
         incandInfo.validMask |= (1 << index);
         incandInfo.ledBlinkSlowBitfield |= (0xff << (index << 3));
#ifndef GEN2_DEBUG
         stdldigio_config_dig_port(index | STDLI_DIG_OUT, 0xff, 0);
#else
         stdldigio_config_dig_port(index | STDLI_DIG_OUT, 0xf3, 0);
#endif
      }
   }
} /* incand_init */

/*
 * ===============================================================================
 * 
 * Name: incand_40ms_tick
 * 
 * ===============================================================================
 */
/**
 * 40 ms tick function.
 * 
 * Starts the incand processing setting a flag.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void incand_40ms_tick()
{
   incandInfo.startProc = TRUE;
   
} /* incand_40ms_tick */

/*
 * ===============================================================================
 * 
 * Name: incand_task
 * 
 * ===============================================================================
 */
/**
 * Incandescent task
 * 
 * Check if a cycle needs to start.  Turn on LEDs as necessary.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    An incandescent bulb that is on supercedes all other states.
 * 
 * ===============================================================================
 */
void incand_task()
{
   U32                        ledOut;
   INT                        index;
   U8                         synch;
   
   if (gen2g_info.validCfg)
   {
      /* Check if new cycle needs to be started */
      if (incandInfo.startProc)
      {
         incandInfo.startProc = FALSE;
         
         if (gen2g_info.ledStatus & GEN2G_STAT_BLINK_SLOW_ON)
         {
            ledOut = incandInfo.ledBlinkSlowBitfield;
         }
         else
         {
            ledOut = 0;
         }
         if (gen2g_info.ledStatus & GEN2G_STAT_BLINK_FAST_ON)
         {
            ledOut |= incandInfo.ledBlinkFastBitfield;
         }
         ledOut |= incandInfo.ledOnBitfield;
         
         /* Write the new values */
         for (index = 0; index < RS232I_NUM_WING; index++)
         {
            if (incandInfo.validMask & (1 << index))
            {
               if (incandInfo.invertMask & (1 << index))
               {
                  stdldigio_write_port(index, 0xff, (U8)~((ledOut >> (index << 3)) & 0xff));
               }
               else
               {
                  stdldigio_write_port(index, 0xff, (U8)((ledOut >> (index << 3)) & 0xff));
               }
            }
         }
      }
      
      /* Synchronize cards */
      if (!gen2g_info.firstCard)
      {
         synch = stdldigio_read_port(STDLI_DIG_PORT_4, GEN2G_SYNCH_OUT);
         
         /* If synch signal changed and new value is set */
         if ((synch ^ incandInfo.prevSynch) && (synch == GEN2G_SYNCH_OUT))
         {
            gen2g_info.ledStateNum = 0;
            gen2g_info.ledStatus = 0;
         }
         incandInfo.prevSynch = synch;
      }
   }
}

/*
 * ===============================================================================
 * 
 * Name: incand_rot_left
 * 
 * ===============================================================================
 */
/**
 * Incandescent rotate left command
 * 
 * Rotate the incandescent bulbs that are "on" to the left using a mask.
 * 
 * @param   rotMask     [in]        Mask to rotate
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void incand_rot_left(
   U32                        rotMask)
{
   INT                        index = 0;
   INT                        prevIndex = 0;
   INT                        firstBit = 0;
   BOOL                       foundFirstBit = FALSE;
   BOOL                       dataBit;
   U32                        prevLedOn;
   
   prevLedOn = incandInfo.ledOnBitfield;
   
   for (index = 31; index >= 0; index--)
   {
      if ((1 << index) & rotMask)
      {
         if (!foundFirstBit)
         {
            foundFirstBit = TRUE;
            firstBit = index;
            if (prevLedOn & (1 << index))
            {
               dataBit = TRUE;
            }
            else
            {
               dataBit = FALSE;
            }
         }
      }
   }
   
   /* Clear all the bits that are in the mask */
   incandInfo.ledOnBitfield &= ~rotMask;
   
   if (foundFirstBit)
   {
      for (index = firstBit - 1, prevIndex = firstBit; index >= 0; index--)
      {
         if ((1 << index) & rotMask)
         {
            if ((1 << index) & prevLedOn)
            {
                incandInfo.ledOnBitfield |= (1 << prevIndex);
            }
            prevIndex = index;
         }
      }
      
      /* Fill out the bit that is rotated from the left most bit */
      if (dataBit)
      {
         incandInfo.ledOnBitfield |= (1 << prevIndex);
      }
   }
} /* end incand_rot_left */

/*
 * ===============================================================================
 * 
 * Name: incand_rot_right
 * 
 * ===============================================================================
 */
/**
 * Incandescent rotate right command
 * 
 * Rotate the incandescent bulbs that are "on" to the right using a mask.
 * 
 * @param   rotMask     [in]        Mask to rotate
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void incand_rot_right(
   U32                        rotMask)
{
   INT                        index = 0;
   INT                        prevIndex = 0;
   INT                        firstBit = 0;
   BOOL                       foundFirstBit = FALSE;
   BOOL                       dataBit;
   U32                        prevLedOn;
   
   prevLedOn = incandInfo.ledOnBitfield;
   
   for (index = 0; index < 32; index++)
   {
      if ((1 << index) & rotMask)
      {
         if (!foundFirstBit)
         {
            foundFirstBit = TRUE;
            firstBit = index;
            if (prevLedOn & (1 << index))
            {
               dataBit = TRUE;
            }
            else
            {
               dataBit = FALSE;
            }
         }
      }
   }
   
   /* Clear all the bits that are in the mask */
   incandInfo.ledOnBitfield &= ~rotMask;
   
   if (foundFirstBit)
   {
      for (index = firstBit + 1, prevIndex = firstBit; index < 32; index++)
      {
         if ((1 << index) & rotMask)
         {
            if ((1 << index) & prevLedOn)
            {
                incandInfo.ledOnBitfield |= (1 << prevIndex);
            }
            prevIndex = index;
         }
      }
      
      /* Fill out the bit that is rotated from the right most bit */
      if (dataBit)
      {
         incandInfo.ledOnBitfield |= (1 << prevIndex);
      }
   }
} /* end incand_rot_right */

/*
 * ===============================================================================
 * 
 * Name: incand_proc_cmd
 * 
 * ===============================================================================
 */
/**
 * Incandescent process a command
 * 
 * Process a command receeived on the serial port
 * 
 * @param   cmd         [in]        Command
 * @param   mask        [in]        Mask
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void incand_proc_cmd(
   U8                         cmd,
   U32                        mask)
{
   switch (cmd)
   {
      case INCAND_ROT_LEFT:
      {
         incand_rot_left(mask);
         break;
      }
      case INCAND_ROT_RIGHT:
      {
         incand_rot_right(mask);
         break;
      }
      case INCAND_LED_ON:
      {
         incandInfo.ledOnBitfield |= mask;
         break;
      }
      case INCAND_LED_OFF:
      {
         incandInfo.ledOnBitfield &= ~mask;
         break;
      }
      case INCAND_LED_BLINK_SLOW:
      {
         incandInfo.ledBlinkSlowBitfield |= mask;
         incandInfo.ledBlinkFastBitfield &= ~mask;
         break;
      }
      case INCAND_LED_BLINK_FAST:
      {
         incandInfo.ledBlinkFastBitfield |= mask;
         incandInfo.ledBlinkSlowBitfield &= ~mask;
         break;
      }
      case INCAND_LED_BLINK_OFF:
      {
         incandInfo.ledBlinkSlowBitfield &= ~mask;
         incandInfo.ledBlinkFastBitfield &= ~mask;
         break;
      }
      case INCAND_LED_SET_ON_OFF:
      {
         incandInfo.ledOnBitfield = mask;
         incandInfo.ledBlinkSlowBitfield = 0;
         incandInfo.ledBlinkFastBitfield = 0;
         break;
      }
      default:
      {
         if (cmd & INCAND_SET)
         {
            if (cmd & INCAND_SET_ON)
            {
               incandInfo.ledOnBitfield |= mask;
            }
            else
            {
               incandInfo.ledOnBitfield &= ~mask;
            }
            /* Setting a slow blink and a fast blink together doesn't make sense */
            if (cmd & INCAND_SET_BLINK_SLOW)
            {
               incandInfo.ledBlinkSlowBitfield |= mask;
               incandInfo.ledBlinkFastBitfield &= ~mask;
            }
            else if (cmd & INCAND_SET_BLINK_FAST)
            {
               incandInfo.ledBlinkFastBitfield |= mask;
               incandInfo.ledBlinkSlowBitfield &= ~mask;
            }
            else
            {
               incandInfo.ledBlinkSlowBitfield &= ~mask;
               incandInfo.ledBlinkFastBitfield &= ~mask;
            }
         }
         break;
      }
   }
} /* end incand_proc_cmd */


/* [] END OF FILE */
