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
 * @date:   9/17/2015
 *
 * @note:   Copyright© 2015, Hugh Spahr
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
 
#include "stdtypes.h"   /* include peripheral declarations */

/* 
 * API for digital I/O functions
 */
/* Digital I/O interface structures/enumerations */
typedef enum
{
  STDLI_DIG_PORT_0          = 0x00,
  STDLI_DIG_PORT_1          = 0x01,
  STDLI_DIG_PORT_2          = 0x02,
  STDLI_DIG_PORT_3          = 0x03,
  STDLI_DIG_PORT_4          = 0x04,
  STDLI_DIG_PORT_MASK       = 0x07,
  STDLI_DIG_OUT             = 0x10,
  STDLI_DIG_OC_PULLDWN      = 0x20,
  STDLI_DIG_PULLUP          = 0x40,
  STDLI_DIG_PULLDWN         = 0x80,
} STDLI_DIG_PORT_INFO_E;

/* Digital I/O function prototypes */
void stdldigio_config_dig_port(
  STDLI_DIG_PORT_INFO_E     portInfo,     /* port, input/output, drive, and pullup */
  U8                        mask,         /* mask of data bits to change */
  U8                        data);        /* data if output bits, unused if input */
U8 stdldigio_read_port(
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        mask);        /* mask of data bits to read */
void stdldigio_write_port(
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        mask,         /* mask of data bits to write */
  U8                        data);        /* data to write */
#endif

/* [] END OF FILE */
