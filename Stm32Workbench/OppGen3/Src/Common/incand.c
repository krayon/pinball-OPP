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
 * a 40ms tick for the blinking.
 *
 *===============================================================================
 */
#include <stdlib.h>
#include "stdtypes.h"
#include "gen2glob.h"

#define INCAND_MAX_INCAND   32

const U32                   INCAND_FADE_MASK[32] =
{
   0x00000000, 0x00010001, 0x00010101, 0x01010101,
   0x01010111, 0x01110111, 0x01111111, 0x11111111,
   0x11111115, 0x11151115, 0x11151515, 0x15151515,
   0x15151555, 0x15551555, 0x15555555, 0x55555555,
   0x55555557, 0x55575557, 0x55575757, 0x57575757,
   0x57575777, 0x57775777, 0x57777777, 0x77777777,
   0x7777777f, 0x777f777f, 0x777f7f7f, 0x7f7f7f7f,
   0x7f7f7fff, 0x7fff7fff, 0x7fffffff, 0xffffffff
};

typedef struct
{
   U16              totTicks;
   U16              currTick;
} FADE_BYTE_INFO;

typedef struct
{
   BOOL              startProc;
   U8                validMask;
   U8                invertMask;  /* 1 if wing is high side incand */
   U32               currFadeBitMask[INCAND_MAX_INCAND];
   U32               ledCurrFadeBit;
   U32               ledBlinkSlowBitfield;
   U32               ledBlinkFastBitfield;
   U8                *currVal_p;          /* Ptr to array of current incand values */
   U8                *newVal_p;           /* Ptr to array of future incand values */
   FADE_BYTE_INFO    *fadeByte_p;         /* Current fade byte info being updated */
} INCAND_INFO;

INCAND_INFO incandInfo;

/* Prototypes */
void digital_upd_outputs(
   U32                        value,
   U32                        mask);
void incand_fade_proc(
   INT                  offset,
   U8                   newData);
void incand_end_fade_proc();
void fade_init_rec(
   INT               startOffset,
   INT               numFadeBytes,
   U8                **currPxlVal_pp,
   U8                **newPxlVal_pp,
   void              (*fadeProc_fp)(INT offset, U8 newData),
   void              (*endFadeProc_fp)());

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
   U8                         *currPxlVal_p;       /* Ptr to array of current pixel values */
   U8                         *newPxlVal_p;        /* Ptr to array of future pixel values */
   
   incandInfo.startProc = FALSE;
   incandInfo.validMask = 0;
   incandInfo.invertMask = 0;
   incandInfo.ledBlinkSlowBitfield = 0;
   incandInfo.ledBlinkFastBitfield = 0;
   incandInfo.ledCurrFadeBit = 0x00000001;
   for (index = 0; index < INCAND_MAX_INCAND; index++)
   {
      incandInfo.currFadeBitMask[index] = 0;
   }
   
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
      }
   }
   if (incandInfo.validMask != 0)
   {
      /* Malloc memory for support of fade commands */
      fade_init_rec(RS232I_FADE_INCAND_OFFSET, INCAND_MAX_INCAND,
         &currPxlVal_p, &newPxlVal_p, incand_fade_proc, incand_end_fade_proc);
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
        *currPxlVal_p++ = 0;
        *newPxlVal_p++ = 0;
      }
   }
} /* incand_init */

/*
 * ===============================================================================
 * 
 * Name: incand_10ms_tick
 * 
 * ===============================================================================
 */
/**
 * 10 ms tick function.
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
void incand_10ms_tick()
{
   incandInfo.startProc = TRUE;
} /* incand_10ms_tick */

/*
 * ===============================================================================
 *
 * Name: incand_fade_proc
 *
 * ===============================================================================
 */
/**
 * Incandescent fade processing
 *
 * Special processing for incandescents.  Used to fill out fade mask.
 *
 * @param   None
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void incand_fade_proc(
   INT                  offset,
   U8                   newData)
{
   incandInfo.currFadeBitMask[offset] = INCAND_FADE_MASK[newData >> 3];
}

/*
 * ===============================================================================
 *
 * Name: incand_end_fade_proc
 *
 * ===============================================================================
 */
/**
 * Incandescent end fade processing
 *
 * Special processing occurs when fade processing is completed.
 *
 * @param   None
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void incand_end_fade_proc()
{
}

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
         for (index = 0; index < INCAND_MAX_INCAND; index++)
         {
            if (incandInfo.currFadeBitMask[index] & incandInfo.ledCurrFadeBit)
            {
            	ledOut |= (1 << index);
            }
         }
         incandInfo.ledCurrFadeBit <<= 1;
         if (incandInfo.ledCurrFadeBit == 0)
         {
            incandInfo.ledCurrFadeBit = 0x00000001;
         }

         /* Write the new values */
         for (index = 0; index < RS232I_NUM_WING; index++)
         {
            if (incandInfo.validMask & (1 << index))
            {
               if (incandInfo.invertMask & (1 << index))
               {
            	  digital_upd_outputs(((~(ledOut >> (index << 3))) & 0xff) << (index << 3),
                     0x000000ff << (index << 3));
               }
               else
               {
             	  digital_upd_outputs(((ledOut >> (index << 3)) & 0xff) << (index << 3),
                      0x000000ff << (index << 3));
               }
            }
         }
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
   INT                        index;
   INT                        firstBit;
   BOOL                       foundFirstBit = FALSE;
   U32                        prevData = 0;
   U32                        data;
   
   for (index = 31; index >= 0; index--)
   {
      if ((1 << index) & rotMask)
      {
         if (!foundFirstBit)
         {
            foundFirstBit = TRUE;
            prevData = incandInfo.currFadeBitMask[index];
            firstBit = index;
         }
         else
         {
            data = incandInfo.currFadeBitMask[index];
            incandInfo.currFadeBitMask[index] = prevData;
            prevData = data;
         }
      }
   }
   
   if (foundFirstBit)
   {
      incandInfo.currFadeBitMask[firstBit] = prevData;
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
   INT                        index;
   INT                        firstBit;
   BOOL                       foundFirstBit = FALSE;
   U32                        prevData = 0;
   U32                        data;
   
   for (index = 0; index < INCAND_MAX_INCAND; index++)
   {
      if ((1 << index) & rotMask)
      {
         if (!foundFirstBit)
         {
             foundFirstBit = TRUE;
             prevData = incandInfo.currFadeBitMask[index];
             firstBit = index;
         }
         else
         {
             data = incandInfo.currFadeBitMask[index];
             incandInfo.currFadeBitMask[index] = prevData;
             prevData = data;
         }
      }
   }
   
   if (foundFirstBit)
   {
      incandInfo.currFadeBitMask[firstBit] = prevData;
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
   INT                        index;

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
         for (index = 0; index < INCAND_MAX_INCAND; index++)
         {
            if ((1 << index) & mask)
            {
               incandInfo.currFadeBitMask[index] = 0xffffffff;
            }
         }
         break;
      }
      case INCAND_LED_OFF:
      {
         for (index = 0; index < INCAND_MAX_INCAND; index++)
         {
            if ((1 << index) & mask)
            {
               incandInfo.currFadeBitMask[index] = 0x00000000;
            }
         }
         break;
      }
      case INCAND_LED_BLINK_SLOW:
      {
         incandInfo.ledBlinkSlowBitfield |= mask;
         incandInfo.ledBlinkFastBitfield &= ~mask;
         for (index = 0; index < INCAND_MAX_INCAND; index++)
         {
            if ((1 << index) & mask)
            {
               incandInfo.currFadeBitMask[index] = 0x00000000;
            }
         }
         break;
      }
      case INCAND_LED_BLINK_FAST:
      {
         incandInfo.ledBlinkFastBitfield |= mask;
         incandInfo.ledBlinkSlowBitfield &= ~mask;
         for (index = 0; index < INCAND_MAX_INCAND; index++)
         {
            if ((1 << index) & mask)
            {
               incandInfo.currFadeBitMask[index] = 0x00000000;
            }
         }
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
         for (index = 0; index < INCAND_MAX_INCAND; index++)
         {
            if ((1 << index) & mask)
            {
               incandInfo.currFadeBitMask[index] = 0xffffffff;
            }
            else
            {
               incandInfo.currFadeBitMask[index] = 0x00000000;
            }
         }
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
               for (index = 0; index < INCAND_MAX_INCAND; index++)
               {
                  if ((1 << index) & mask)
                  {
                     incandInfo.currFadeBitMask[index] = 0xffffffff;
                  }
               }
            }
            else
            {
               for (index = 0; index < INCAND_MAX_INCAND; index++)
               {
                  if ((1 << index) & mask)
                  {
                     incandInfo.currFadeBitMask[index] = 0x00000000;
                  }
               }
            }
            /* Setting a slow blink and a fast blink together doesn't make sense */
            if (cmd & INCAND_SET_BLINK_SLOW)
            {
               incandInfo.ledBlinkSlowBitfield |= mask;
               incandInfo.ledBlinkFastBitfield &= ~mask;
               for (index = 0; index < INCAND_MAX_INCAND; index++)
               {
                  if ((1 << index) & mask)
                  {
                     incandInfo.currFadeBitMask[index] = 0x00000000;
                  }
               }
            }
            else if (cmd & INCAND_SET_BLINK_FAST)
            {
               incandInfo.ledBlinkFastBitfield |= mask;
               incandInfo.ledBlinkSlowBitfield &= ~mask;
               for (index = 0; index < INCAND_MAX_INCAND; index++)
               {
                  if ((1 << index) & mask)
                  {
                     incandInfo.currFadeBitMask[index] = 0x00000000;
                  }
               }
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
