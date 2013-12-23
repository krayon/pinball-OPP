#!/usr/bin/env python
#
#===============================================================================
#
#                         OOOO
#                       OOOOOOOO
#      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#     PPPPPPPPPPPPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP    OOO    OOO    PPP
#               PPP     OOOOOOOO     PPP
#              PPPPP      OOOO      PPPPP
#
# @file:   rs232Intf.py
# @author: Hugh Spahr
# @date:   12/20/2012
#
# @note:   Open Pinball Project
#          Copyright 2012, Hugh Spahr
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#===============================================================================
#
# This is the serial port interface file that is included for serial port
# command definitions.
#
#===============================================================================

testVers = '00.00.01'

#Public data
GET_SER_NUM_CMD     = '\x00'
GET_PROD_ID_CMD     = '\x01'
GET_GET_VERS_CMD    = '\x02'
GET_SET_SER_NUM_CMD = '\x03'
RESET_CMD           = '\x04'
GO_BOOT_CMD         = '\x05'
CFG_SOL_CMD         = '\x06'
KICK_SOL_CMD        = '\x07'
READ_SOL_INP_CMD    = '\x08'
CFG_INP_CMD         = '\x09'
READ_INP_BRD_CMD    = '\x0a'
SAVE_CFG_CMD        = '\x0b'
SAVE_CFG_CHECK_BYTE = '\xf4'
ERASE_CFG_CMD       = '\x0c'
ERASE_CFG_CHECK_BYTE= '\xf3'

INV_CMD             = '\xf0'
EOM_CMD             = '\xff'

CARD_ID_TYPE_MASK   = '\xf0'
CARD_ID_SOL_CARD    = '\x00'
CARD_ID_INP_CARD    = '\x10'

NUM_INP_PER_BRD     = 16
CFG_INP_STATE       = '\x00'
CFG_INP_FALL_EDGE   = '\x01'
CFG_INP_RISE_EDGE   = '\x02'

NUM_SOL_PER_BRD     = 8
CFG_SOL_USE_SWITCH  = '\x01'
CFG_SOL_AUTO_CLR    = '\x02'

