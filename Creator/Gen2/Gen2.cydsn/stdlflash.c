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
 * @file:   stdlflash.c
 * @author: Hugh Spahr
 * @date:   10/26/2015
 *
 * @note:    Copyright© 2015, Hugh Spahr
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
 * This is the flash utility file in the Standard Library.
 *  It contains erase and write functions for the Flash.
 *
 *===============================================================================
 */ 
#include "stdtypes.h"   /* include peripheral declarations */
#include "stdlintf.h"

#define CPUSS_CONFIG_REG         0x40100000
#define CPUSS_SYSREQ_REG         0x40100004
#define CPUSS_SYSARG_REG         0x40100008
#define LOAD_FLASH_SYS_CMD       0x0000d7b6
#define LOAD_FLASH_OP_CODE       0x80000004
#define ADDR_TO_ROW_NUM_SHFT     9
#define STATUS_MASK              0xf0000000
#define STATUS_GOOD              0xa0000000

U8                          *stdleeprom_addr_p;

/*
 * ===============================================================================
 * 
 * Name: stdlflash_sector_erase
 * 
 * ===============================================================================
 */
/**
 * Erase flash sector (in this case row)
 * 
 * Blocking erase sector (row)
 * 
 * @param   dest_p      [in]    ptr to Flash sector address to erase
 * @return  None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
BOOL stdlflash_sector_erase( 
   U8                         *dest_p)      /* ptr to sector addr in eeprom */
{
   U32                        stack[3];
   U32                        status;
   
#define WRITE_ROW_SYS_CMD     0x0000d8b6
#define WRITE_ROW_OP_CODE     0x80000005
#define NUM_BYTES             0

   /* Load one byte of data the page late buffer (NUM_BYTES + 1) */
   stack[0] = LOAD_FLASH_SYS_CMD;
   stack[1] = NUM_BYTES;
   stack[2] = 0;                             /* Data */
   
   *((R32 *)CPUSS_SYSARG_REG) = (U32)&stack[0];
   *((R32 *)CPUSS_SYSREQ_REG) = LOAD_FLASH_OP_CODE;
   status = *((R32 *)CPUSS_SYSARG_REG);
   if ((status & STATUS_MASK) != STATUS_GOOD)
   {
      return (TRUE);
   }
   
   /* Run the write row command which will erase (no program) if data is all 0 */
   stack[0] = WRITE_ROW_SYS_CMD | (((U32)dest_p & ~0x7f) << ADDR_TO_ROW_NUM_SHFT);
   *((R32 *)CPUSS_SYSARG_REG) = (U32)&stack[0];
   *((R32 *)CPUSS_SYSREQ_REG) = WRITE_ROW_OP_CODE;
   status = *((R32 *)CPUSS_SYSARG_REG);
   if ((status & STATUS_MASK) != STATUS_GOOD)
   {
      return (TRUE);
   }
   return (FALSE);
   
} /* End stdlflash_sector_erase */

/*
 * ===============================================================================
 * 
 * Name: stdlflash_write
 * 
 * ===============================================================================
 */
/**
 * Write to flash
 * 
 * Blocking call to write to flash.
 * 
 * @param   src_p       [in]    ptr to source of data
 * @param   dest_p      [in]    ptr to destination of data in flash
 * @param   numBytes    [in]    number of bytes to write
 * @return  None
 * 
 * @pre None 
 * @note User must insure that the data is erased.  Maximum 128 bytes can be
 *   written at a time.
 * 
 * ===============================================================================
 */
BOOL stdlflash_write( 
   U8                         *src_p,       /* ptr to source of data */
   U8                         *dest_p,      /* ptr to destination of data in flash */
   U8                         numBytes)     /* number of bytes */
{
   U32                        stack[(128/4) + 2];
   U32                        status;
   U8                         *stack_p;
   INT                        index;

#define PROGRAM_OP_CODE       0x80000006
   
   /* Create the load latch buffer command */
   stack[0] = LOAD_FLASH_SYS_CMD;
   stack[1] = numBytes;
   for (index = 0, stack_p = (U8 *)&stack[2]; index < numBytes; index++)
   {
      *stack_p++ = *src_p++;
   }
   
   /* Load bytes into the latch buffer */
   *((R32 *)CPUSS_SYSARG_REG) = (U32)&stack[0];
   *((R32 *)CPUSS_SYSREQ_REG) = LOAD_FLASH_OP_CODE;
   status = *((R32 *)CPUSS_SYSARG_REG);
   if ((status & STATUS_MASK) != STATUS_GOOD)
   {
      return (TRUE);
   }
   
   /* Run the program row command.  Row must previously have been erased */
   stack[0] = WRITE_ROW_SYS_CMD | (((U32)dest_p & ~0x7f) << ADDR_TO_ROW_NUM_SHFT);
   *((R32 *)CPUSS_SYSARG_REG) = (U32)&stack[0];
   *((R32 *)CPUSS_SYSREQ_REG) = PROGRAM_OP_CODE;
   status = *((R32 *)CPUSS_SYSARG_REG);
   if ((status & STATUS_MASK) != STATUS_GOOD)
   {
      return (TRUE);
   }
   return (FALSE);
   
} /* End stdlflash_write */
