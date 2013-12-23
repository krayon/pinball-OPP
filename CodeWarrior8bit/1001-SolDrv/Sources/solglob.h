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
 * @file:   solglob.h
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

#ifndef SOLGLOB_H
#define SOLGLOB_H
 
#include "stdtypes.h"
#include "errintf.h"

#define SOLG_WARNING       0x000  /* Used to create 12 bit event IDs */
#define SOLG_ERROR         0xe00  /* Used to create 12 bit event IDs */

#define FLASH_SECT_SIZE     0x0200
#define SERNUM_ADDR         0xfc00
#define BOOT_SECTOR_ADDR    0xfc00
#define SAVE_CFG_ADDR       0xfa00

#define SOLG_SWITCH_THRESH  50    /* Switch threshold in usecs */

typedef enum
{
  SOL_STATE_INIT            = 0x00,
  SOL_STATE_NORM            = 0x01,
} SOL_STATE_E;

typedef struct
{
  RS232I_CFG_SOL_TYPE_E     type;
  U8                        initialKick;
  RS232I_DUTY_E             dutyCycle;
} SOLG_CFG_T;

typedef struct
{
  SOL_STATE_E               state;
  U8                        procCtl;
  U8                        validSwitch;
  U8                        stateMask;
  SOLG_CFG_T                solCfg[RS232I_NUM_SOL];
  U8                        cfgChecksum;
  STDLI_ELAPSED_TIME_T      elapsedTime;
} SOLG_GLOB_T;

#ifndef SOLG_INSTANTIATE
 extern
#endif
  SOLG_GLOB_T               solg_glob;

void rs232proc_init(void);
void rs232proc_task(void);

void digital_init(void);
void digital_task(void);

#endif
