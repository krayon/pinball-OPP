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
 * @file:   rs232intf.h
 * @author: Hugh Spahr
 * @date:   12/07/2012
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
 * RS232 Interface file for open pinball project
 *
 *===============================================================================
 */

#ifndef RS232INTF_H
#define RS232INTF_H

/* Each command starts with the Card ID except for inventory and EOM.  Next comes the
 *  command, then any data.
 */

typedef enum
{
  RS232I_GET_SER_NUM        = 0x00,
  RS232I_GET_PROD_ID        = 0x01,
  RS232I_GET_VERS           = 0x02,
  RS232I_SET_SER_NUM        = 0x03,
  RS232I_RESET              = 0x04,
  RS232I_GO_BOOT            = 0x05,
  RS232I_CONFIG_SOL         = 0x06,     /* For each solenoid, CFG_SOL_TYPE,
                                         *  Initial kick, and Duty Cycle.
                                         */
  RS232I_KICK_SOL           = 0x07,     /* Card ID, value, mask */
  RS232I_READ_SOL_INP       = 0x08,     /* Card ID, data */
  RS232I_READ_INP_BRD       = 0x09,     /* Card ID, data, data */
  RS232I_NUM_CMDS,
  
  RS232I_INVENTORY          = 0xf0,     /* Each card adds byte for card type */
  RS232I_EOM                = 0xff,
} RS232I_CMD_E;

#ifndef RS232I_INSTANTIATE
 extern
#endif
const U8                    CMD_LEN[RS232I_NUM_CMDS]
#ifdef RS232I_INSTANTIATE
 ={ 4,  /* RS232I_GET_SER_NUM */    4,  /* RS232I_GET_PROD_ID */
    4,  /* RS232I_GET_VERS */       4,  /* RS232I_SET_SER_NUM */
    0,  /* RS232I_RESET */          0,  /* RS232I_GO_BOOT */
    24, /* RS232I_CONFIG */         2,  /* RS232I_KICK_SOL */
    1,  /* RS232I_READ_SOL_INP */   2,  /* RS232I_READ_INP_BRD */
  }
#endif
;
/* Note:  This is the length of the cmd excluding card ID and cmd */

#ifndef RS232I_INSTANTIATE
 extern
#endif
const BOOL                  STRIP_CMD[RS232I_NUM_CMDS]
#ifdef RS232I_INSTANTIATE
 ={ FALSE,  /* RS232I_GET_SER_NUM */    FALSE,  /* RS232I_GET_PROD_ID */
    FALSE,  /* RS232I_GET_VERS */       TRUE,   /* RS232I_SET_SER_NUM */
    FALSE,  /* RS232I_RESET */          FALSE,  /* RS232I_GO_BOOT */
    TRUE,   /* RS232I_CONFIG */         TRUE,   /* RS232I_KICK_SOL */
    FALSE,  /* RS232I_READ_SOL_INP */   FALSE,  /* RS232I_READ_INP_BRD */
  }
#endif
;

typedef enum
{
  CARD_ID_CARD_NUM_MASK     = 0x0f,

  CARD_ID_TYPE_MASK         = 0xf0,
  CARD_ID_SOL_CARD          = 0x00,
  CARD_ID_INP_CARD          = 0x10,
  
} RS232I_CARD_ID_E;

typedef enum
{
  USE_SWITCH                = 0x01,
  AUTO_CLR                  = 0x02,
} RS232I_CFG_SOL_TYPE_E;

typedef enum
{
  DUTY_CYCLE_MASK           = 0x0f,   /* lsb 4 bits are duty cycle */
  MIN_OFF_MASK              = 0x70,
} RS232I_DUTY_E;
/* Min off time is 0-7 times the initial kick time.  If initial kick
 * is 20 ms and min off is 5, the solenoid will be forced off for 100 ms
 */
 
#endif
