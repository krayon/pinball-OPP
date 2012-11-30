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
  U8                        *tmpU8_p;
  
#define INIT_SOPT1          0x46        /* Set up debug pins, COP timer is 32ms */
#define INIT_SOPT2          0x04        /* COP enable, TPM2 on port A */
#define INIT_SPMSC1         0x5d        /* Low voltage resets MCU, enable bandgap */
#define INIT_SPMSC2         0x04        /* Low voltage warn bits, 2.56V resets */

  EnableInterrupts; /* enable interrupts */    
  
  SOPT1 = INIT_SOPT1;
  SOPT2 = INIT_SOPT2;
  SPMSC1 = INIT_SPMSC1;    
  SPMSC2 = INIT_SPMSC2;
  
  /* Initialialize global data */
  for (tmpU8_p =&dispg_glob.curDisp[0][0]; 
    tmpU8_p < &dispg_glob.curDisp[0][0] + sizeof(dispg_glob.curDisp);)
  {
    *tmpU8_p++ = 0;
  }
  
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
  
  /* Start functions */
  
  for(;;)
  {
    i2cproc_task();
    digital_task();
    
    __RESET_WATCHDOG(); /* feeds the dog */
  } /* loop forever */
  
  /* please make sure that you never leave main */
} /* End main */
