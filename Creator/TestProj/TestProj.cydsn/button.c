/*
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
 * @file:   button.c
 * @author: Hugh Spahr
 * @date:   9/16/2015
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
 * This is the button function.  It looks for changes in the button.
 *
 *===============================================================================
 */
#include "stdtypes.h"
#include "neointf.h"
#include "stdlintf.h"

#define NUM_NEO_CMDS          5
const U8 neoCmds[] =
   { NEOI_CMD_LED_ON,      NEOI_CMD_BLINK_SLOW,    NEOI_CMD_BLINK_FAST, 
     NEOI_CMD_FADE_SLOW,   NEOI_CMD_FADE_FAST };

/* The default color table only has colors from 0 to 6 */
#define COLOR_TBL_ENTRIES   7

#define NEOI_CMD_LED_ON       0x80
#define NEOI_CMD_BLINK_SLOW   0x00
#define NEOI_CMD_BLINK_FAST   0x20
#define NEOI_CMD_FADE_SLOW    0x40
#define NEOI_CMD_FADE_FAST    0x60
    
/* Button is port 0, bit 7 */
#define BTN_STAT_MASK         0x00000080
#define BTN_NOT_PRESSED       0x00000080

#define GLITCH_TIME           3           /* Assume presses < 3 ms is a glitch */
#define LONG_PRESS_TIME       1000        /* Anything > 1000 ms is a long press */

typedef struct
{
   INT                  startCnt;
   INT                  numPxl;
   INT                  cmdIdx;
   INT                  colorIdx;
   U8                   prevBtn;
} BTN_INFO;

BTN_INFO btnInfo;

/* Prototypes */
INT timer_get_ms_count();

/*
 * ===============================================================================
 * 
 * Name: button_init
 * 
 * ===============================================================================
 */
/**
 * Initialize button
 * 
 * Set input up as input with a pullup resistor (pressed button is a low value).
 * 
 * @param   numPxl      [in]        Number of pixels
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void button_init(
   INT                  numPxl)
{
    /* Initialize the pin to be pulled up input */
   stdldigio_config_dig_port(STDLI_DIG_PORT_0 | STDLI_DIG_PULLUP,
      BTN_STAT_MASK, 0);
    
   btnInfo.prevBtn = BTN_NOT_PRESSED;
   btnInfo.numPxl = numPxl;
   btnInfo.colorIdx = 0;
   btnInfo.cmdIdx = 0;
}

/*
 * ===============================================================================
 * 
 * Name: button_task
 * 
 * ===============================================================================
 */
/**
 * Button task
 * 
 * Check to see if the button has changed state.  If just pressed, grab start time.
 * If just released, see how long the button has been pressed.  If pressed for a
 * short amount of time, change the pixels color.  If pressed for a long time,
 * change the pixel command.
 * 
 * @param   None
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void button_task()
{
   U8                   currBtn;
   INT                  length;
   INT                  index;
   INT                  cmd;
   BOOL                 updateVal = FALSE;
    
   currBtn = stdldigio_read_port(STDLI_DIG_PORT_0, BTN_STAT_MASK);
    
   /* Check if button has changed */
   if (currBtn ^ btnInfo.prevBtn)
   {
      /* Check if button just released */
      if (currBtn & BTN_NOT_PRESSED)
      {
         /* Button was released, grab current time and length of time pressed */
         length = timer_get_ms_count() - btnInfo.startCnt;
         if (length < GLITCH_TIME)
         {
            /* This is a glitch so just ignore. */
         }
         else if (length > LONG_PRESS_TIME)
         {
            /* Long press, change command */
            btnInfo.cmdIdx++;
            if (btnInfo.cmdIdx == NUM_NEO_CMDS)
            {
               updateVal = TRUE;
            }
            else if (btnInfo.cmdIdx > NUM_NEO_CMDS)
            {
               btnInfo.cmdIdx = 0;
            }
            cmd = neoCmds[btnInfo.cmdIdx];
            for (index = 0; index < btnInfo.numPxl; index++)
            {
               /* Update so each pixel gets its own command */
               if (updateVal)
               {
                  cmd = neoCmds[index % NUM_NEO_CMDS];
               }
               neo_update_pixel_cmd(index, cmd);
            }
         }
         else
         {
            /* Short press, change colors */
            btnInfo.colorIdx++;
            if (btnInfo.colorIdx == COLOR_TBL_ENTRIES)
            {
               updateVal = TRUE;
            }
            else if (btnInfo.colorIdx > COLOR_TBL_ENTRIES)
            {
               btnInfo.colorIdx = 0;
            }
            cmd = btnInfo.colorIdx;
            for (index = 0; index < btnInfo.numPxl; index++)
            {
               /* Update so each pixel gets its own color */
               if (updateVal)
               {
                  cmd = index % COLOR_TBL_ENTRIES;
               }
               neo_update_pixel_color(index, cmd);
            }
         }
      }
      else
      {
         /* Button just pressed, save start time */
         btnInfo.startCnt = timer_get_ms_count();
      }
   }   
   btnInfo.prevBtn = currBtn;
}

/* [] END OF FILE */
