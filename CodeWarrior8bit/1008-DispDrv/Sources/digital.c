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
 * This file deals with digital I/O port to control the display driver.  It
 * includes the select mux and the BCD inputs.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"
#include "stdlintf.h"
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include for petting the watchdog */
#include "dispglob.h"
#include "errintf.h"

#define STDL_FILE_ID        3

/* Port A bits */
#define PA_SELECT_13        0x01
#define PA_BLANKING         0x02
#define PA7_BOOT_LED        0x80

/* Port B bits */
#define PB_1S               0x01
#define PB_10S              0x02
#define PB_100S             0x04
#define PB_1000S            0x08
#define PB_10000S           0x10
#define PB_100000S          0x20
#define PB_M1_M1000         0x40
#define PB_M01_M10000       0x80
#define PB_PLAYER_MASK      0x3f
#define PB_MAIN_CTL_MASK    0xc0

/* Port C bits */
#define PC_12BCD            0x0f
#define PC_34BCD            0xf0

typedef enum
{
  DIG_STATE_IDLE            = 0x00,
  DIG_STATE_FOUND_STROBE    = 0x01,
  DIG_STROBE_VALID          = 0x02,
  DIG_WAIT_STROBE_END       = 0x03,
  DIG_INIT_BLANK            = 0x04,
  DIG_BLANK_STATE           = 0x05,
} DIG_STATE_E;

typedef struct
{
  DIG_STATE_E               state;
  DISPG_LED_STATE_E         ledState;
  BOOL                      mux13;
  BOOL                      ledOn;
  U8                        currStrobe;
  U8                        currBcd;
  STDLI_ELAPSED_TIME_T      elapsedTime;
  STDLI_ELAPSED_TIME_T      ledElapsedTime;
} DIGITAL_GLOB_T;

DIGITAL_GLOB_T              dig_glob;

void digital_look_for_change(
  U8                        player,
  U8                        index,
  U8                        data);

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
  dig_glob.state = DIG_STATE_IDLE;
  dig_glob.ledState = LED_OFF;
  dig_glob.mux13 = FALSE;
  dig_glob.ledOn = FALSE;
  
  /* Set up input mux select and blanking input */
  stdldigio_config_dig_port(STDLI_DIG_PORT_A | STDLI_DIG_OUT,
    PA_SELECT_13 | PA7_BOOT_LED, PA7_BOOT_LED);
  stdldigio_config_dig_port(STDLI_DIG_PORT_A | STDLI_DIG_PULLUP, PA_BLANKING, 0);
  
  /* Set up strobe inputs */
  stdldigio_config_dig_port(STDLI_DIG_PORT_B, 0xff, 0);

  /* Set up BCD inputs */
  stdldigio_config_dig_port(STDLI_DIG_PORT_C, 0xff, 0);
} /* End digital_init */

/*
 * ===============================================================================
 * 
 * Name: digital_task
 * 
 * ===============================================================================
 */
/**
 * Task for polling strobe inputs
 * 
 * Check to see if the strobes have been active for a while.  If so, grab the
 * BCD digits, and update the displays as necessary.  Wait for strobe to become
 * inactive.
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
  U8                        *destU8_p;
  U8                        tmpU8;
  
  if (dispg_glob.state == DISP_STATE_NORM)
  {
    /* Check for the blank signal */
    if ((PTAD & PA_BLANKING) == 0)
    {
      if (dig_glob.state == DIG_INIT_BLANK)
      {
        dig_glob.state = DIG_BLANK_STATE;
      }
      else if (dig_glob.state != DIG_BLANK_STATE)
      {
        digital_change_led_state(LED_BLINK_100MS);
        dig_glob.state = DIG_INIT_BLANK;
        for (destU8_p = &dispg_glob.curDisp[0][0]; 
          destU8_p < &dispg_glob.curDisp[0][0] + sizeof(dispg_glob.curDisp);)
        {
          *destU8_p++ = CHAR_BLANK1;
        }
        dispg_glob.updDispBits = UPD_ALL_MASK;
      }
    }
    else
    {
      if ((dig_glob.state == DIG_INIT_BLANK) || (dig_glob.state == DIG_BLANK_STATE))
      {
        dig_glob.state = DIG_STATE_IDLE;
      }
      if (dig_glob.state == DIG_STATE_IDLE)
      {
        /* Check if any of the strobes are active */
        tmpU8 = PTBD;
        if (tmpU8 != 0xff)
        {
          /* Switch to looking at the other strobes */
          dig_glob.mux13 = !dig_glob.mux13;
          if (dig_glob.mux13)
          {
            PTAD |= PA_SELECT_13;
          }
          else
          {
            PTAD &= ~PA_SELECT_13;
          }
        }
        else
        {
          /* Found a strobe, start a timer, and make sure it is valid for 200us */
          dig_glob.state = DIG_STATE_FOUND_STROBE;
          dig_glob.currStrobe = tmpU8;
          dig_glob.currBcd = PTCD;
          stdltime_get_curr_time(&dig_glob.elapsedTime.startTime);
        }
      }
      else if (dig_glob.state == DIG_STATE_FOUND_STROBE)
      {
        stdltime_get_elapsed_time(&dig_glob.elapsedTime);
        if (dig_glob.elapsedTime.elapsedTime.usec < 200)
        {
          /* Verify the inputs haven't changed */
          if ((PTBD != dig_glob.currStrobe) || (PTCD != dig_glob.currBcd))
          {
            dig_glob.state = DIG_STATE_IDLE;
          }
        }
        else
        {
          /* Strobe has been stable for 200us */
          dig_glob.state = DIG_STROBE_VALID;
        }
      }
      else if (dig_glob.state == DIG_STROBE_VALID)
      {
        dig_glob.state = DIG_WAIT_STROBE_END;
        
        /* Check if any changes to display, first ID strobe */
        for (tmpU8 = 0; tmpU8 < 8; tmpU8++)
        {
          if (((1 << tmpU8) & dig_glob.currStrobe) == 0)
          {
            break;
          }
        }
        /* Check if valid */
        if (tmpU8 != 8)
        {
          /* Convert all blanks to BLANK1 */
          if (((dig_glob.currBcd & 0x0f) >= CHAR_BLANK2) &&
            ((dig_glob.currBcd & 0x0f) <= CHAR_BLANK6))
          {
            dig_glob.currBcd = (dig_glob.currBcd & ~0x0f) | CHAR_BLANK1;
          }
          if (((dig_glob.currBcd & 0xf0) >= (CHAR_BLANK2 << 4)) &&
            ((dig_glob.currBcd & 0xf0) <= (CHAR_BLANK6 << 4)))
          {
            dig_glob.currBcd = (dig_glob.currBcd & ~0xf0) | (CHAR_BLANK1 << 4);
          }
          if (tmpU8 < CHARS_PER_DISP)
          {
            /* Change to player scores */
            if (dig_glob.mux13)
            {
              digital_look_for_change(DISPG_PLAYER1, tmpU8, dig_glob.currBcd & 0x0f);
              digital_look_for_change(DISPG_PLAYER3, tmpU8, (dig_glob.currBcd >> 4) & 0x0f);
            }
            else
            {
              digital_look_for_change(DISPG_PLAYER2, tmpU8, dig_glob.currBcd & 0x0f);
              digital_look_for_change(DISPG_PLAYER4, tmpU8, (dig_glob.currBcd >> 4) & 0x0f);
            }
          }
          else
          {
            /* Change to master display */
            tmpU8 -= CHARS_PER_DISP;
            if (dig_glob.mux13)
            {
              /* This updates either M1000 or M10000 */
              tmpU8 += 3;
            }
            digital_look_for_change(DISPG_CREDIT_MATCH, tmpU8, dig_glob.currBcd & 0x0f);
          }
        }
      }
      else if (dig_glob.state == DIG_WAIT_STROBE_END)
      {
        /* Wait for strobe to be disabled */
        if (PTBD != dig_glob.currStrobe)
        {
          dig_glob.state = DIG_STATE_IDLE;
        }
      }
    }
  }
  if (dig_glob.ledState == LED_BLINK_100MS)
  {
    stdltime_get_elapsed_time(&dig_glob.ledElapsedTime);
    if (dig_glob.ledElapsedTime.elapsedTime.msec >= 100)
    {
      stdltime_get_curr_time(&dig_glob.ledElapsedTime.startTime);
      if (dig_glob.ledOn)
      {
        dig_glob.ledOn = FALSE;
        PTAD |= PA7_BOOT_LED;
      }
      else
      {
        dig_glob.ledOn = TRUE;
        PTAD &= ~PA7_BOOT_LED;
      }
    }
  }
  else if (dig_glob.ledState == LED_BLINK_500MS)
  {
    stdltime_get_elapsed_time(&dig_glob.ledElapsedTime);
    if (dig_glob.ledElapsedTime.elapsedTime.msec >= 500)
    {
      stdltime_get_curr_time(&dig_glob.ledElapsedTime.startTime);
      if (dig_glob.ledOn)
      {
        dig_glob.ledOn = FALSE;
        PTAD |= PA7_BOOT_LED;
      }
      else
      {
        dig_glob.ledOn = TRUE;
        PTAD &= ~PA7_BOOT_LED;
      }
    }
  }
} /* End digital_task */

/*
 * ===============================================================================
 * 
 * Name: digital_look_for_change
 * 
 * ===============================================================================
 */
/**
 * Look for display changes
 * 
 * This function is passed the player number, index, and the value.  If there is
 * a change to the display change it, and mark the appropriate bits to be updated.
 * 
 * @param   player      [in]    player [0-3] or master [4]
 * @param   index       [in]    index [0-5]
 * @param   data        [in]    bcd value
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_look_for_change(
  U8                        player,
  U8                        index,
  U8                        data)
{
  U16                       updateBit;
  
  /* Remember, curDisp uses index 0 as leftmost character */ 
  if (dispg_glob.curDisp[player][CHARS_PER_DISP - index] != data)
  {
    dispg_glob.curDisp[player][CHARS_PER_DISP - index] = data;
    if ((index == 0) || (index == 1))
    {
      updateBit = PLYR1_CHAR56;
    }
    else if ((index == 3) || (index == 4))
    {
      updateBit = PLYR1_CHAR23;
    }
    else
    {
      updateBit = PLYR1_CHAR14;
    }
    
    /* Shift to account for player number */
    updateBit <<= (U8)(3 * player);
    DisableInterrupts;
    dispg_glob.updDispBits |= updateBit;
    EnableInterrupts;
  }
} /* End digital_look_for_change */

/*
 * ===============================================================================
 * 
 * Name: digital_change_led_state
 * 
 * ===============================================================================
 */
/**
 * Change the LED state
 * 
 * This function is passed a new LED state
 * 
 * @param   ledState    [in]    new state for the LED
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void digital_change_led_state(
  DISPG_LED_STATE_E         ledState)
{
  if (ledState == LED_OFF)
  {
    if (dig_glob.ledState < LED_BLINK_500MS)
    {
      dig_glob.ledState = ledState;
      dig_glob.ledOn = FALSE;
      PTAD |= PA7_BOOT_LED;
    }
  }
  else if (ledState == LED_ON)
  {
    if (dig_glob.ledState < LED_BLINK_500MS)
    {
      dig_glob.ledState = ledState;
      dig_glob.ledOn = TRUE;
      PTAD &= ~PA7_BOOT_LED;
    }
  }
  else if ((ledState == LED_BLINK_100MS) || (ledState == LED_BLINK_500MS))
  {
    if (ledState > dig_glob.ledState)
    {
      dig_glob.ledState = ledState;
    }
    stdltime_get_curr_time(&dig_glob.ledElapsedTime.startTime);
  }
} /* End digital_change_led_state */

