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
 * @note:    Copyright� 2015, Hugh Spahr
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
#include "procdefs.h"

typedef struct
{
   BOOL                       locked;
} STDLFLASH_INFO_T;

STDLFLASH_INFO_T              stdltime_glob = { TRUE };

/*
 * ===============================================================================
 * 
 * Name: stdlflash_unlock_flash
 *
 * ===============================================================================
 */
/**
 * Unlock flash for erase/write
 *
 * @param   None
 * @return  None
 *
 * @pre None
 * @note None
 *
 * ===============================================================================
 */
void stdlflash_unlock_flash()
{

#define KEY1                  0x45670123
#define KEY2                  0xCDEF89AB

   /* Write key values to unlock flash erase/writes */
   flashBase_p->KEYR = KEY1;
   flashBase_p->KEYR = KEY2;
   stdltime_glob.locked = FALSE;

} /* End stdlflash_unlock_flash */

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
 * @return  FALSE if no error occurs
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
BOOL stdlflash_sector_erase( 
   U16                        *dest_p)      /* ptr to sector addr in flash */
{
#define FLASH_TIMEOUT   10000

   if (stdltime_glob.locked)
   {
      stdlflash_unlock_flash();
   }
   
   /* Verify flash isn't busy */
   if (flashBase_p->SR & FLSH_SR_BSY)
   {
      return TRUE;
   }
   
   flashBase_p->CR = FLSH_CR_PER;
   flashBase_p->AR = (U32)dest_p;
   flashBase_p->CR = FLSH_CR_PER | FLSH_CR_STRT;

   INT count = 0;
   while ((flashBase_p->SR & FLSH_SR_BSY) && (count < FLASH_TIMEOUT))
   {
      count++;
   }
   if ((count >= FLASH_TIMEOUT) ||
      ((flashBase_p->SR & (FLSH_SR_PGERR | FLSH_SR_WRPRTERR)) != 0))
   {
      return TRUE;
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
 * @return  FALSE if no error occurs
 * 
 * @pre None 
 * @note User must insure that the data is erased.  Maximum 128 bytes can be
 *   written at a time.
 * 
 * ===============================================================================
 */
BOOL stdlflash_write( 
   U16                        *src_p,       /* ptr to source of data */
   U16                        *dest_p,      /* ptr to destination of data in flash */
   INT                        numBytes)     /* number of bytes */
{
   if (stdltime_glob.locked)
   {
	   stdlflash_unlock_flash();
   }

   /* Verify flash isn't busy */
   if (flashBase_p->SR & FLSH_SR_BSY)
   {
      return TRUE;
   }

   flashBase_p->CR = FLSH_CR_PG;
   for (INT index = 0; index < numBytes; index += sizeof(U16))
   {
	   *dest_p++ = *src_p++;
	   // flashBase_p->CR = FLSH_CR_STRT;

	   INT count = 0;
	   while ((flashBase_p->SR & FLSH_SR_BSY) && (count < FLASH_TIMEOUT))
       {
          count++;
       }
       if ((count >= FLASH_TIMEOUT) ||
          ((flashBase_p->SR & (FLSH_SR_PGERR | FLSH_SR_WRPRTERR)) != 0))
       {
          return TRUE;
       }
   }
   return (FALSE);
} /* End stdlflash_write */
