/*
 *===============================================================================
 *
 *          SSSS
 *        SSSSSSSs                 DDD
 *       SSS    SSS     TTT        DDD            Hugh Spahr
 *      SSS  LLL SSS    TTT        DDD            Standard
 *       SSS LLL      TTTTTTT      DDD            Library
 *         SSSSL      TTTTTTT      DDD  
 *          SSSSS       TTT        DDD
 *           LSSSS      TTT    DDDDDDD
 *           LLLSSS     TTT  DDDDDDDDD
 *      SSS  LLL SSS    TTT DDD    DDD
 *       SSS LLLSSS     TTT DDD    DDD
 *        SSSSSSSS      TTT  DDDDDDDDD
 *          SSSS        TTT    DDDD DD
 *           LLL
 *           LLL   I    BBB
 *           LLL  III   BBB
 *           LLL   I    BBB
 *           LLL        BBB
 *           LLL  III   BBB
 *           LLL  III   BBB
 *           LLL  III   BBBBBBB
 *           LLL  III   BBBBBBBBB
 *           LLL  III   BBB    BBB
 *           LLL        BBB    BBB
 *           LLLLLLLLL  BBBBBBBBB
 *           LLLLLLLLL  BB BBBB
 *
 * @file:   stdleeprom.c
 * @author: Hugh Spahr
 * @date:   8/28/2008
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
 * This is the EEPROM utility file in the Standard Library.
 *  It contains erase and write functions for the EEPROM and Flash.
 *
 *===============================================================================
 */ 
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"

#define EEPROM_SEC_PAGE     0x1800
#define LAUNCH_CMD          0x80
#define FSTAT_FCCF_BIT      0x40
#define FCNFG_EPGSEL_BIT    0x40
#define SECTOR_ERASE_CMD    0x40
#define BYTE_PROGRAM_CMD    0x20

U8                          *stdleeprom_addr_p;

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_init_eeprom_addr
 * 
 * ===============================================================================
 */
/**
 * Initialize EEPROM address
 * 
 * Initialize EEPROM address.  The EEPROM address allows the library to support
 * multiple processors.
 * 
 * @param   addr_p      [in]    ptr to first addr of eeprom
 * @return  None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void stdleeprom_init_eeprom_addr( 
  U8                        *addr_p)      /* ptr to first addr of eeprom */
{
  stdleeprom_addr_p = addr_p;
} /* End stdleeprom_init_eeprom_addr */

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_start_sector_erase
 * 
 * ===============================================================================
 */
/**
 * Start EEPROM sector erase
 * 
 * Initiate a sector erase in the EEPROM.
 * 
 * @param   addr_p      [in]    ptr to EEPROM sector address to erase
 * @return  None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void stdleeprom_start_sector_erase( 
  U8                        *addr_p)      /* ptr to sector addr in eeprom */
{
  /* Check if this is on the second page */
  if (addr_p >= (U8 *)EEPROM_SEC_PAGE)
  {
    FCNFG |= FCNFG_EPGSEL_BIT;
    addr_p = (addr_p - (U8 *)EEPROM_SEC_PAGE) + stdleeprom_addr_p;
  }
  else
  {
    FCNFG &= ~FCNFG_EPGSEL_BIT;
  }
  
  /* EEPROM erase sectors can be run out of Flash */  
  *addr_p = 0;
  FCMD = SECTOR_ERASE_CMD;
  FSTAT = LAUNCH_CMD;
} /* End stdleeprom_start_sector_erase */

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_check_cmd_done
 * 
 * ===============================================================================
 */
/**
 * Check if an EEPROM cmd is done
 * 
 * Check if the EEPROM cmd is done by checking if the FCCF bit is set.
 * 
 * @param   None
 * @return  None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
BOOL stdleeprom_check_cmd_done(void)
{
  if ((FSTAT & FSTAT_FCCF_BIT) == 0)
  {
    return(FALSE);
  }
  else
  {
    return(TRUE);
  }
} /* End stdleeprom_check_cmd_done */

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_start_write
 * 
 * ===============================================================================
 */
/**
 * Start EEPROM write byte
 * 
 * Initiate a write byte to the EEPROM.
 * 
 * @param   addr_p      [in]    ptr to EEPROM sector address to write
 * @param   data        [in]    data to write
 * @return  None
 * 
 * @pre None 
 * @note User must insure that the data is erased.
 * 
 * ===============================================================================
 */
void stdleeprom_start_write( 
  U8                        *addr_p,      /* ptr to addr in eeprom to write */
  U8                        data)         /* data to write */
{
  /* Check if this is on the second page */
  if (addr_p >= (U8 *)EEPROM_SEC_PAGE)
  {
    FCNFG |= FCNFG_EPGSEL_BIT;
    addr_p = (addr_p - (U8 *)EEPROM_SEC_PAGE) + stdleeprom_addr_p;
  }
  else
  {
    FCNFG &= ~FCNFG_EPGSEL_BIT;
  }
    
  /* EEPROM writes can be run from Flash */
  *addr_p = data;
  FCMD = BYTE_PROGRAM_CMD;
  FSTAT = LAUNCH_CMD;
} /* End stdleeprom_start_write */

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_ram_flash_cmd
 * 
 * ===============================================================================
 */
/**
 * Run a flash command from ram.
 * 
 * This function is copied to the stack, and then run from there.
 * 
 * @param   addr_p      [in]    ptr to Flash sector address to erase
 * @return  None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void far stdleeprom_ram_flash_cmd(void)
{
  FSTAT = LAUNCH_CMD;
  do
  {
    __RESET_WATCHDOG(); /* feeds the dog */
  } while ((FSTAT & FSTAT_FCCF_BIT) == 0);
}
void far stdleeprom_copy_to_stack(
  U8                        *stack_p)
{
  U8                        *src_p;
  
  /* Copy the commands onto the stack */
  for (src_p = (U8 *)(U16)&stdleeprom_ram_flash_cmd;
    src_p < (U8 *)(U16)&stdleeprom_copy_to_stack;)
  {
    *stack_p++ = *src_p++;
  }
}

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_start_flash_sector_erase
 * 
 * ===============================================================================
 */
/**
 * Start Flash sector erase
 * 
 * Initiate a sector erase in the Flash.
 * 
 * @param   addr_p      [in]    ptr to Flash sector address to erase
 * @return  None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void stdleeprom_start_flash_sector_erase( 
  U8                        *addr_p)      /* ptr to sector addr in eeprom */
{
  U8                        stack[0x20];  /* Actually requires 0x16 bytes */

  stdleeprom_copy_to_stack(&stack[0]);

  /* Write to the addr to lock it */
  DisableInterrupts;
  *addr_p = 0;
  FCMD = SECTOR_ERASE_CMD;
  ((void (*)(void))(U16)&stack[0])();
  EnableInterrupts;
} /* End stdleeprom_start_flash_sector_erase */

/*
 * ===============================================================================
 * 
 * Name: stdleeprom_start_flash_write
 * 
 * ===============================================================================
 */
/**
 * Start Flash write byte
 * 
 * Initiate a write byte to the Flash.
 * 
 * @param   addr_p      [in]    ptr to Flash sector address to write
 * @param   data        [in]    data to write
 * @return  None
 * 
 * @pre None 
 * @note User must insure that the data is erased.
 * 
 * ===============================================================================
 */
void stdleeprom_start_flash_write( 
  U8                        *addr_p,      /* ptr to addr in eeprom to write */
  U8                        data)         /* data to write */
{
  U8                        stack[0x20];

  stdleeprom_copy_to_stack(&stack[0]);

  /* Write to the addr to lock it */
  DisableInterrupts; /* disable interrupts */    
  *addr_p = data;
  FCMD = BYTE_PROGRAM_CMD;
  ((void (*)(void))(U16)&stack[0])();
  EnableInterrupts; /* enable interrupts */    
} /* End stdleeprom_start_flash_write */
