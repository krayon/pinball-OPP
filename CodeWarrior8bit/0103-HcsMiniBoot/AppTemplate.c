/*
 *===============================================================================
 *
 *                          HHHHH            HHHHH
 *                           HHH     SSSS     HHH
 *                           HHH   SSSSSSSS   HHH 
 *                           HHH  SSS    SSS  HHH       Hugh Spahr
 *                           HHH SSS      SSS HHH       Utilities
 *                           HHH  SSS         HHH
 *                           HHH    SSSS      HHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHH         SSS  HHH
 *                           HHH SSS      SSS HHH
 *                           HHH  SSS    SSS  HHH
 *                           HHH   SSSSSSSS   HHH
 *                           HHH     SSSS     HHH
 *                          HHHHH            HHHHH
 *
 * @file:   AppTemplate.c
 * @author: Hugh Spahr
 * @date:   4/22/2008
 *
 * @note:    Copyright© 2008, Hugh Spahr
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
 * This is the main file in the test application.  It verifies that the
 *  bootloader is working and interrupt redirection is happening.  It sets.
 *  up timer 1 as a 1 ms overflow timer.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */

#include "version.h"  
#define INTERRUPT_INSTANTIATE
#include "interrupt.h"

void forceBootMode(void);

/*
 * ===============================================================================
 * 
 * Name: main
 * 
 * ===============================================================================
 */
/**
 * Main entrance function to the application.
 * 
 * Set up the timer 1 over flow interrupt.  Wait for the interrupt to occur while
 * petting the watchdog.
 * 
 * @param None 
 * @return None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void main(void) 
{

#define RDRF                0x20
#define BOOT_MODE_CHAR      'Z'         // Boot mode character (force back to boot)

  U8                        rcvChar;
  BOOL                      newChar;
  
  EnableInterrupts; /* enable interrupts */
  
  newChar = FALSE;
  
  TPM1SC = 0x48;  /* Use busclk, and no clk divide, enable ovfl int */
  TPM1MOD = 4000; /* Set clock tick to 1 ms */
  
  for(;;)
  {
    /* See if a serial character was received */
    if (SCI1S1 & RDRF)
    {
      rcvChar = SCI1D;
      newChar = TRUE;
    }
    if (newChar)
    {
      newChar = FALSE;
      if (rcvChar == BOOT_MODE_CHAR)
      {
        forceBootMode();
      }
    }
    __RESET_WATCHDOG(); /* feeds the dog */
  } /* loop forever */
  /* please make sure that you never leave main */
} /* End main */

/*
 * ===============================================================================
 * 
 * Name: timer1_isr
 * 
 * ===============================================================================
 */
/**
 * Timer 1 overflow interrupt
 * 
 * After getting the interrupt clear the overflow flag.
 * 
 * @param None 
 * @return None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
interrupt void timer1_isr(void)
{
  TPM1SC &= ~0x80;    /* Clear the overflow flag */
}

/*
 * ===============================================================================
 * 
 * Name: forceBootMode
 * 
 * ===============================================================================
 */
/**
 * Force boot loader
 *
 * Write a 0xa5 at the beginning of RAM and reset processor.
 *
 * @param   None
 * @return  None (resets processor)
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void forceBootMode(void)
{
#define MAGIC_NUM           0xa5
#define RAM_FIRST_ADDR      0x70

  /* Write the magic number */
  *(U8 *)RAM_FIRST_ADDR = MAGIC_NUM;

  /* Reset the processor */
  asm DCB 0x8D ;    /* Use illegal instruction to cause reset */
}
