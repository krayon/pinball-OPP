/*
 *===============================================================================
 *
 *                          8888         999999
 *                        88888888     999999999
 *                       888    888   999    9999
 *                      888      888 999      999
 *                       888    888   999    9999
 *                        88888888     9999999999
 *     NNNNN      NNNNN    888888       999999999     TTT     HHHHH
 *      NNN        NNN    88888888        999 999     TTT      HHH
 *      NNNN       NNN   888    888           999     TTT      HHH
 *      NNNNN      NNN  888      888          999  TTTTTTTTT   HHH
 *      NNNNNN     NNN   888    888           999 TTTTTTTTTTT  HHH
 *      NNNNNNN    NNN    88888888            999     TTT      HHH
 *      NNNNNNNN   NNN      8888              999     TTT      HHH
 *      NNN  NNNN  NNN                                TTT      HHH
 *      NNN   NNNN NNN      OOOOOO     RRR RRRRR      TTT      HHH HHHHH
 *      NNN    NNNNNNN     OOOOOOOO    RRRRRRRRRR     TTT      HHHHHHHHHH
 *      NNN     NNNNNN    OOO    OOO   RRRR    RRR    TTT      HHHH    HHH
 *      NNN      NNNNN   OOO      OOO  RRR            TTT      HHH     HHH
 *      NNN       NNNN    OOO    OOO   RRR            TTT      HHH     HHH
 *      NNN        NNN     OOOOOOOO    RRR            TTT      HHH     HHH
 *     NNNNN      NNNNN      OOOO      RRR           TTTTT    HHHHH   HHHHH
 *
 * @file:   main.c
 * @author: Hugh Spahr, Mike Rogals
 * @date:   12/03/2009, 10/01/2011
 *
 * @note:   89 North, Inc.   Copyright© 2009
 *          1 Mill St., Unit 285
 *          Burlington, VT  05401
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
void rs232proc_force_boot_mode(void);

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
  stdldigio_config_dig_port(STDLI_DIG_PORT_B | STDLI_DIG_PULLUP, PB_XTRA_4, 0);
  if ((PTBD & PB_XTRA_4) == 0)
  {
    *(U8 *)MAGIC_NUM_ADDR = MAGIC_NUM;
    asm ldhx  #$fffe
    asm jmp   ,x
  }

  EnableInterrupts; /* enable interrupts */
  
  solg_glob.procCtl = 0;
  solg_glob.validSwitch = 0;
  for (solCfg_p = &solg_glob.solCfg[0];
    solCfg_p < &solg_glob.solCfg[SOLG_NUM_SOL]; solCfg_p++)
  {
    solCfg_p->type = 0;
    solCfg_p->initialKick = 0;
    solCfg_p->dutyCycle = 0;
  }
    

  /* Start the clock running, then start the sys tick timer for 10ms */
  stdltime_start_timing_clock(TIMER_FAST_OSC);
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
