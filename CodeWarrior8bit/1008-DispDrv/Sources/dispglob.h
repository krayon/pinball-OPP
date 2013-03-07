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

#define NUM_PLAYERS         4
#define CHARS_PER_DISP      6
#define MSTR_CHARS_PER_DISP 4

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
  DISP_STATE_CFG            = 0x00,
  DISP_STATE_INIT           = 0x01,
  DISP_STATE_NORM           = 0x02,
} DISP_STATE_E;

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
  CHAR_BLANK1               = 0x0a,   /* These can all be used for blank */
  CHAR_BLANK2               = 0x0b,   /* in BCD chips. */
  CHAR_BLANK3               = 0x0c,
  CHAR_BLANK4               = 0x0d,
  CHAR_BLANK5               = 0x0e,
  CHAR_BLANK6               = 0x0f,
  CHAR_P                    = 0x10,
  CHAR_E                    = 0x11,
  CHAR_N                    = 0x12,
  CHAR_L                    = 0x13,
  CHAR_A                    = 0x14,
  CHAR_J                    = 0x15,
  CHAR_C                    = 0x16,
  MAX_CHAR_ID
} DISPG_CHAR_E;

#define PLYR1_CHAR23        0x0001
#define PLYR1_CHAR56        0x0002
#define PLYR1_CHAR14        0x0004
#define PLYR2_CHAR23        0x0008
#define PLYR2_CHAR56        0x0010
#define PLYR2_CHAR14        0x0020
#define PLYR3_CHAR23        0x0040
#define PLYR3_CHAR56        0x0080
#define PLYR3_CHAR14        0x0100
#define PLYR4_CHAR23        0x0200
#define PLYR4_CHAR56        0x0400
#define PLYR4_CHAR14        0x0800
#define MSTR_CHAR23         0x1000
#define MSTR_CHAR56         0x2000
#define UPD_ALL_MASK        0x3fff
#define NUM_UPDATE_BITS         14

typedef struct
{
  DISP_STATE_E              state;
  U8                        curDisp[DISPG_NUM_DISP][CHARS_PER_DISP];
  U16                       updDispBits;
  STDLI_ELAPSED_TIME_T      elapsedTime;
} DISPG_GLOB_T;
/* Warning:  curDisp stores characters with index 0 being leftmost
 *  character.  This makes it easier to debug but adds a little code.
 */

#ifndef DISPG_INSTANTIATE
 extern
#endif
  DISPG_GLOB_T              dispg_glob;

void i2cproc_init_i2c(void);
void i2cproc_task(void);

void digital_init(void);
void digital_task(void);

#endif
