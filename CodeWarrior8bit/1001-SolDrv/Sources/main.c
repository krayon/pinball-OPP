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
 * @date:   12/06/2012
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
 * This is the main file for solenoid driver board.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "rs232intf.h"
#define SOLG_INSTANTIATE
#include "solglob.h"

#include "version.h"
#define PROD_ID             1001
#define INTERRUPT_INSTANTIATE
#include "interrupt.h"

#define STDL_FILE_ID        1

/* Prototypes */
void rs232proc_init(void);

/*
 * ===============================================================================
 * 
 * Name: main
 * 
 * ===============================================================================
 */
/**
 * Main task
 * 
 * Initialize timer, digital lines and RS232.
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
#define INIT_SOPT1          0x46        /* Set up debug pins, COP timer is 32ms */
#define INIT_SOPT2          0x04        /* COP enable, TPM2 on port A */
#define INIT_SPMSC1         0x5d        /* Low voltage resets MCU, enable bandgap */
#define INIT_SPMSC2         0x04        /* Low voltage warn bits, 2.56V resets */

/* SCL low at bootup means no pullups, force into bootloader */
#define MAGIC_NUM           0xa5
#define MAGIC_NUM_ADDR      0x80
#define PB_XTRA_4           0x80

  SOLG_CFG_T                *solCfg_p;
  
  SOPT1  = INIT_SOPT1;
  SOPT2  = INIT_SOPT2;
  SPMSC1 = INIT_SPMSC1;    
  SPMSC2 = INIT_SPMSC2;

  /* Look if should jump back to bootloader and stay there */
  /* HRS currently disabled
  stdldigio_config_dig_port(STDLI_DIG_PORT_B | STDLI_DIG_PULLUP |
    STDLI_DIG_SMALL_MODEL, PB_XTRA_4, 0);
  if ((PTBD & PB_XTRA_4) == 0)
  {
    *(U8 *)MAGIC_NUM_ADDR = MAGIC_NUM;
    asm ldhx  #$fffe
    asm jmp   ,x
  } */

  EnableInterrupts; /* enable interrupts */
  
  solg_glob.procCtl = 0;
  solg_glob.validSwitch = 0;
  for (solCfg_p = &solg_glob.solCfg[0];
    solCfg_p < &solg_glob.solCfg[RS232I_NUM_SOL]; solCfg_p++)
  {
    solCfg_p->type = 0;
    solCfg_p->initialKick = 0;
    solCfg_p->dutyCycle = 0;
  }
    

  /* Start the clock running, then start the sys tick timer for 10ms */
  stdltime_start_timing_clock(0);
  stdltime_start_tick(10);
    
  /* Initialization functions */
  digital_init();
  stdlser_ser_module_init();
  rs232proc_init();
  
  for(;;)
  { 
    rs232proc_task();
    digital_task();
    
    __RESET_WATCHDOG(); /* feeds the dog */
  }/* loop forever */
  
  /* please make sure that you never leave main */
} /* End main */
