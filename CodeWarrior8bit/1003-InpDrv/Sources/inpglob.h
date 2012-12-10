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
 * @file:   inpglob.h
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
 * Global file for the input driver.  It contains prototypes and enumerations
 * that are shared between files.
 *
 *===============================================================================
 */

#ifndef INPGLOB_H
#define INPGLOB_H
 
#include "stdtypes.h"
#include "errintf.h"

#define INPG_WARNING       0x000  /* Used to create 12 bit event IDs */
#define INPG_ERROR         0xe00  /* Used to create 12 bit event IDs */

#define FLASH_SECT_SIZE     0x0200
#define SERNUM_ADDR         0xfc00
#define BOOT_SECTOR_ADDR    0xfc00

#define INPG_SWITCH_THRESH  50    /* Switch threshold in usecs */

typedef enum
{
  INP_STATE_INIT            = 0x00,
  INP_STATE_NORM            = 0x01,
} INP_STATE_E;

typedef struct
{
  INP_STATE_E               state;
  RS232I_CFG_INP_TYPE_E     inpCfg[RS232I_NUM_INP];
  U16                       inpSwitch;
  U16                       stateMask;
} INPG_GLOB_T;

#ifndef INPG_INSTANTIATE
 extern
#endif
  INPG_GLOB_T               inpg_glob;

void rs232proc_init(void);
void rs232proc_task(void);

void digital_init(void);
void digital_task(void);

#endif
