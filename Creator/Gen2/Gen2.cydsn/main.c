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
 * @file:   main.c
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
 * This is main file.  It initializes the tasks, and runs them.
 *
 *===============================================================================
 */
#include <project.h>
#include <stdlib.h>
#include "stdtypes.h"
#define GEN2G_INSTANTIATE
#include "gen2glob.h"
#include "neointf.h"
#include "stdlintf.h"


/* HRS:  Debug */
void debug_save_nv_cfg();

/* Prototype declarations */
void neo_fifo_trigger_isr();

void timer_init();
void timer_overflow_isr();

void main_copy_flash_to_ram();
void main_call_wing_inits();

void digital_task(void);

void rs232proc_init();
void rs232proc_task();

void incand_task(void);

int main()
{
   CyGlobalIntEnable; /* Enable global interrupts. */

   appStart.codeVers = 0x00010100;
   
/* Used for forcing the standard configuration onto the board.  If this is left on,
 * the programmed configuration will always be overwritten.
 */
#if 0
   debug_save_nv_cfg();
#endif
   
   Clock_Start();
   Clock_1_Start();
   PWM_Start();
   PWM_1_Start();
   SPI_1_Start();
   UART_1_Start();

	
   main_copy_flash_to_ram();
   main_call_wing_inits();

   stdlser_ser_module_init();
   rs232proc_init();
   
   /* Initialize tasks */
   gen2g_info.error = neo_init(gen2g_info.nvCfgInfo.numNeoPxls);
   timer_init();

   isr_spi_Start();
   isr_uart_Start();

   for(;;)
   {
      timer_overflow_isr();
      neo_task();
      digital_task();
      rs232proc_task();
      incand_task();
   }
}

/*
 * ===============================================================================
 * 
 * Name: main_copy_flash_to_ram
 * 
 * ===============================================================================
 */
/**
 * Copy flash to RAM
 * 
 * Check if the flash settings are valid.  If so, copy the information into RAM.
 * 
 * @param   None
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void main_copy_flash_to_ram()
{
   U8                         crc;
   U32                        *src_p;
   U32                        *dst_p;
   
   /* Init gen2g structure */
   gen2g_info.typeWingBrds = 0;
   gen2g_info.crcErr = 0;
   gen2g_info.error = NO_ERRORS;
   gen2g_info.freeCfg_p = &gen2g_info.nvCfgInfo.cfgData[0];
   
   /* Test if wing cfg have valid settings */
   crc = 0xff;
   stdlser_calc_crc8(&crc, GEN2G_NV_PARM_SIZE, (U8 *)gen2g_nv_cfg_p->wingCfg);
   if (crc == gen2g_nv_cfg_p->nvCfgCrc)
   {
      gen2g_info.validCfg = TRUE;
      
      /* Copy the wing configuration */
      for (src_p = (U32 *)gen2g_nv_cfg_p, dst_p = (U32 *)&gen2g_info.nvCfgInfo;
         src_p < (U32 *)(GEN2G_CFG_TBL + sizeof(GEN2G_NV_CFG_T)); )
      {
         *dst_p++ = *src_p++;
      }
   }
   else
   {
      gen2g_info.validCfg = FALSE;
      for (dst_p = (U32 *)&gen2g_info.nvCfgInfo;
         dst_p < (U32 *)((U32)&gen2g_info.nvCfgInfo + sizeof(GEN2G_NV_CFG_T)); dst_p++)
      {
         *dst_p = 0;
      }
   }
} /* End main_copy_flash_to_ram */

/*
 * ===============================================================================
 * 
 * Name: main_call_wing_inits
 * 
 * ===============================================================================
 */
/**
 * Call wing board init functions
 * 
 * If the configuration is valid, create wing board type mask, and call init
 * functions.
 * 
 * @param   None
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void main_call_wing_inits()
{
   INT                        index;

   if (gen2g_info.validCfg)
   {
      /* Walk through the wing boards and create bit mask of wing board types */
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         if (gen2g_info.nvCfgInfo.wingCfg[index] != WING_UNUSED)
         {
            gen2g_info.typeWingBrds |= (1 << gen2g_info.nvCfgInfo.wingCfg[index]);
         }
      }
      
      /* Walk through types and call init functions using jump table */
      for (index = WING_UNUSED + 1; index < MAX_WING_TYPES; index++)
      {
         if (((gen2g_info.typeWingBrds & (1 << index)) != 0) &&
            (GEN2G_INIT_FP[index] != NULL))
         {
            GEN2G_INIT_FP[index]();
         }
      }
   }
} /* End main_call_wing_inits */

/* [] END OF FILE */
