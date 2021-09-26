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
 * @file:   stdlintf.c
 * @author: Hugh Spahr
 * @date:   6/10/2008
 *
 * @note:   Copyright© 2008-2015, Hugh Spahr
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
 * Interface file to the Standard Library.  It contains function
 *  prototypes and structures
 *
 *===============================================================================
 */
#ifndef STDLINTF_H
#define STDLINTF_H
 
#include "stdtypes.h"

/* 
 * API for serial functions
 */
void stdlser_init();
void stdlser_xmt_data(
   U8                         *data_p,       /* Ptr to data to xmt */
   INT                        numChar);      /* Num chars to xmt */
void stdlser_calc_crc8(
   U8                         *crc8_p,       /* Ptr to crc8 */
   INT                        length,        /* Num chars in data stream */
   U8                         *data_p);      /* Ptr to data stream */
void stdlser_get_xmt_info(
   U8                         **data_pp,
   U16                        *numChar_p);

/* 
 * API for digital I/O functions
 */

#define STDLI_NUM_DIG_PORT    3

/* Digital I/O interface structures/enumerations */
typedef enum
{
   STDLI_DIG_PORT_A           = 0x00,
   STDLI_DIG_PORT_B           = 0x01,
   STDLI_DIG_PORT_C           = 0x02,
   STDLI_DIG_PORT_MASK        = 0x03,
   STDLI_DIG_OUT              = 0x10,
   STDLI_DIG_OC_PULLDWN       = 0x20,
   STDLI_DIG_PULLUP           = 0x40,
   STDLI_DIG_PULLDWN          = 0x80,
} STDLI_DIG_PORT_INFO_E;

/* Digital I/O function prototypes */
U32 stdldigio_read_all_ports(
   U32                        mask);        /* mask of data bits to read */
void stdldigio_write_all_ports(
   U32                        data,         /* data bits to write */
   U32                        mask);        /* mask of bits to write */
U32 stdldigio_read_port(
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_A */
   U32                        mask);        /* mask of data bits to read */

/* 
 * API for erasing and writing to flash
 */
BOOL stdlflash_sector_erase( 
   U16                        *dest_p);     /* ptr to sector addr in flash */
BOOL stdlflash_write( 
   U16                        *src_p,       /* ptr to source of data */
   U16                        *dest_p,      /* ptr to destination of data in flash */
   INT                        numBytes);    /* number of bytes */

#endif

/* [] END OF FILE */
