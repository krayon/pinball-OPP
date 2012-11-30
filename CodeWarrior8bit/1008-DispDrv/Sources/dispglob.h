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
 * @file:   dispglob.h
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
 * Global file for the display controller.  It contains prototypes and enumerations
 * that are shared between files.
 *
 *===============================================================================
 */

#ifndef DISPGLOB_H
#define DISPGLOB_H
 
#include "stdtypes.h"
#include "errintf.h"

#define DISPG_WARNING       0x000 /* Used to create 12 bit event IDs */
#define DISPG_ERROR         0xe00 /* Used to create 12 bit event IDs */
#define DISPG_PROD_ID       1008

#define LOG_SECTOR_ADDR     0xf800
#define FLASH_SECT_SIZE     0x0200
#define SERNUM_ADDR         0xfc00
#define BOOT_SECTOR_ADDR    0xfc00

#define CHARS_PER_DISP      6

typedef enum
{
  DISPG_PLAYER1             = 0x00,
  DISPG_PLAYER2             = 0x01,
  DISPG_PLAYER3             = 0x02,
  DISPG_PLAYER4             = 0x03,
  DISPG_CREDIT_MATCH        = 0x04,
  DISPG_NUM_DISP
} DISPG_DISP_E;

typedef enum
{
  CHAR_0                    = 0x00,
  CHAR_1                    = 0x01,
  CHAR_2                    = 0x02,
  CHAR_3                    = 0x03,
  CHAR_4                    = 0x04,
  CHAR_5                    = 0x05,
  CHAR_6                    = 0x06,
  CHAR_7                    = 0x07,
  CHAR_8                    = 0x08,
  CHAR_9                    = 0x09,
  CHAR_P                    = 0x0a,
  CHAR_E                    = 0x0b,
  CHAR_N                    = 0x0c,
  CHAR_L                    = 0x0d,
  CHAR_A                    = 0x0e,
  CHAR_J                    = 0x0f,
  CHAR_C                    = 0x10,
  CHAR_BLANK                = 0x11,
  MAX_CHAR_ID
} DISPG_CHAR_E;

typedef struct
{
  U8                        curDisp[DISPG_NUM_DISP][CHARS_PER_DISP];
} DISPG_GLOB_T;

#ifndef DISPG_INSTANTIATE
 extern
#endif
  DISPG_GLOB_T              dispg_glob;

void i2cproc_init_i2c(void);
void i2cproc_task(void);

void digital_init(void);
void digital_task(void);

#endif
