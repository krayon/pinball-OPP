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
 * @file:   main.c
 * @author: Hugh Spahr
 * @date:   11/30/2012
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
 * This is the main file for the display driver firmware.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#define DISPG_INSTANTIATE
#include "dispglob.h"

#include "version.h"  
#define INTERRUPT_INSTANTIATE
#define PROD_ID             1008
#include "interrupt.h"

#define STDL_FILE_ID        1

U8                          initDisp[DISPG_NUM_DISP][CHARS_PER_DISP] = {
  { CHAR_BLANK1, CHAR_0, CHAR_P, CHAR_E, CHAR_N, CHAR_BLANK1 },
  { CHAR_P, CHAR_1, CHAR_N, CHAR_8, CHAR_L, CHAR_L },
  { CHAR_P, CHAR_A, CHAR_0, CHAR_J, CHAR_C, CHAR_7 },
  { (MAJ_VERSION/10), (MAJ_VERSION - ((MAJ_VERSION/10)*10)),
    (MIN_VERSION/10), (MIN_VERSION - ((MIN_VERSION/10)*10)),
    (SUB_VERSION/10), (SUB_VERSION - ((SUB_VERSION/10)*10)) },
  { CHAR_BLANK1, CHAR_8, CHAR_8, CHAR_BLANK1, CHAR_8, CHAR_8 } };

/*
 * ===============================================================================
 * 
 * Name: main
 * 
 * ===============================================================================
 */
/**
 * Main entrance to the application.
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
  U8                        *srcU8_p;
  U8                        *destU8_p;
  
#define INIT_SOPT1          0x46        /* Set up debug pins, COP timer is 32ms */
#define INIT_SOPT2          0x04        /* COP enable, TPM2 on port A */
#define INIT_SPMSC1         0x5d        /* Low voltage resets MCU, enable bandgap */
#define INIT_SPMSC2         0x04        /* Low voltage warn bits, 2.56V resets */

/* SCL low at bootup means no pullups, force into bootloader */
#define MAGIC_NUM           0xa5
#define MAGIC_NUM_ADDR      0x80
#define PB7_SCL             0x80
#define PA7_BOOT_LED        0x80

  /* Look if should jump back to bootloader and stay there */
  stdldigio_config_dig_port(STDLI_DIG_PORT_B, PB7_SCL, 0);
  if ((PTBD & PB7_SCL) == 0)
  {
    /* Turn on status LED, send magic num, jump to beginning of bootloader.
     *  Jump instead of reset so LED stays on.
     */
    stdldigio_config_dig_port(STDLI_DIG_PORT_A | STDLI_DIG_OUT, PA7_BOOT_LED, 0);  
    *(U8 *)MAGIC_NUM_ADDR = MAGIC_NUM;
    asm ldhx  #$fffe
    asm jmp   ,x
  }
  
  EnableInterrupts; /* enable interrupts */    
  
  SOPT1 = INIT_SOPT1;
  SOPT2 = INIT_SOPT2;
  SPMSC1 = INIT_SPMSC1;    
  SPMSC2 = INIT_SPMSC2;
  
  /* Initialialize global data */
  dispg_glob.state = DISP_STATE_INIT;
  for (destU8_p = &dispg_glob.curDisp[0][0], srcU8_p = &initDisp[0][0]; 
    destU8_p < &dispg_glob.curDisp[0][0] + sizeof(dispg_glob.curDisp);)
  {
    *destU8_p++ = *srcU8_p++;
  }
  
  /* Mark all displays as needing updating */
  dispg_glob.updDispBits = UPD_ALL_MASK;
  
  /* Start the clock running, then start the sys tick timer for 10ms */
  stdltime_start_timing_clock(TIMER_FAST_OSC);
  stdltime_start_tick(10);
  stdlser_ser_module_init();
  
  /* Start event log at the Flash log sector  */
  (void)stdlevt_init_log_event((STDLI_EVENT_LOG_T *)LOG_SECTOR_ADDR,
    (U8 *)(BOOT_SECTOR_ADDR - 1), (U8 *)0);
    
  /* Initialization functions */
  digital_init();
  i2cproc_init_i2c();
  
  /* Put initial msg up for 5 seconds */
  stdltime_get_curr_time(&dispg_glob.elapsedTime.startTime);
  
  for(;;)
  {
    /* Check if in init state */
    if (dispg_glob.state == DISP_STATE_INIT)
    {
      /* If so check if more than 5 seconds elapsed.  If so,
       *  move to normal state.
       */
      stdltime_get_elapsed_time(&dispg_glob.elapsedTime);
      if (dispg_glob.elapsedTime.elapsedTime.sec >= 5)
      {
        dispg_glob.state = DISP_STATE_NORM;
      }
    }
    
    i2cproc_task();
    digital_task();
    
    __RESET_WATCHDOG(); /* feeds the dog */
  } /* loop forever */
  
  /* please make sure that you never leave main */
} /* End main */
