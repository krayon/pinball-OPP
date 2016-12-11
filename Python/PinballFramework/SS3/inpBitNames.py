#!/usr/bin/env python
#
# Warning - This is an auto-generated file.  All changes to this file will
# be overwritten next time GenPyCode.py is re-run.  Do not change this file
# unless you want to start hand editing the files.
#
#===============================================================================
#
#                           OOOO
#                         OOOOOOOO
#        PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
#      PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#     PPP         PPP   OOO      OOO   PPP         PPP
#    PPP          PPP   OOO      OOO   PPP          PPP
#    PPP          PPP   OOO      OOO   PPP          PPP
#    PPP          PPP   OOO      OOO   PPP          PPP
#     PPP         PPP   OOO      OOO   PPP         PPP
#      PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#       PPPPPPPPPPPPP   OOO      OOO   PPP
#                 PPP   OOO      OOO   PPP
#                 PPP   OOO      OOO   PPP
#                 PPP   OOO      OOO   PPP
#                 PPP    OOO    OOO    PPP
#                 PPP     OOOOOOOO     PPP
#                PPPPP      OOOO      PPPPP
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
##
# @file    inpBitNames.py
# @author  AutoGenerated
# @date    12/05/2016
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief These are the input bit names.  It has a bitmask for each input.

#===============================================================================

import rs232Intf

## Input bit name enumeration.
#  Contains a bit mask for each input.  Can also contain bitfield masks.
#  Top most nibble contains the index of the input card base 0.
class InpBitNames:
    def __init__(self):
        pass

    INP_UPPER_RGHT_ROLLOVER                          = 0x00020001
    INP_UPPER_CTR_ROLLOVER                           = 0x00020002
    INP_UPPER_LFT_ROLLOVER                           = 0x00020004
    INP_UPPER_LFT_TOP_TRGT                           = 0x00020008
    INP_UPPER_LFT_BTM_TRGT                           = 0x00020010
    INP_CTR_RGHT_ROLLOVER                            = 0x00020020
    INP_CTR_CTR_ROLLOVER                             = 0x00020040
    INP_CTR_LFT_ROLLOVER                             = 0x00020080
    INP_UPPER_RUBBER                                 = 0x01020001
    INP_SPINNER                                      = 0x01020002
    INP_CTR_RGHT_RUBBER                              = 0x01020004
    INP_JKPOT_ROLLOVER                               = 0x01020008
    INP_BELOW_KICKOUT_RUBBER                         = 0x01020010
    SOL_TOP_DROP_RUBBER                              = 0x01020020
    INP_DROP_TRGT_1S                                 = 0x01030001
    INP_DROP_TRGT_2H                                 = 0x01030002
    INP_DROP_TRGT_3O                                 = 0x01030004
    INP_DROP_TRGT_4O                                 = 0x01030008
    INP_DROP_TRGT_5T                                 = 0x01030010
    INP_DROP_TRGT_6E                                 = 0x01030020
    INP_DROP_TRGT_7R                                 = 0x01030040
    INP_DROP_BANK_MISS                               = 0x01030080
    INP_BTM_LFT_INLN_ROLLOVER                        = 0x03020001
    INP_BTM_LFT_OUTLN_ROLLOVER                       = 0x03020002
    INP_CTR_LOW_ROLLOVER                             = 0x03020004
    INP_BTM_RGHT_RUBBER                              = 0x03020008
    INP_BTM_RGHT_LOW_RUBBER                          = 0x03020010
    INP_SLAM_TILT                                    = 0x03030001
    INP_TILT                                         = 0x03030002
    INP_COIN_DROP                                    = 0x03030004
    INP_START                                        = 0x03030008

    INP_UPPER_RGHT_ROLLOVER_CRD0MSK                  = 0x00010000
    INP_UPPER_CTR_ROLLOVER_CRD0MSK                   = 0x00020000
    INP_UPPER_LFT_ROLLOVER_CRD0MSK                   = 0x00040000
    INP_UPPER_LFT_TOP_TRGT_CRD0MSK                   = 0x00080000
    INP_UPPER_LFT_BTM_TRGT_CRD0MSK                   = 0x00100000
    INP_CTR_RGHT_ROLLOVER_CRD0MSK                    = 0x00200000
    INP_CTR_CTR_ROLLOVER_CRD0MSK                     = 0x00400000
    INP_CTR_LFT_ROLLOVER_CRD0MSK                     = 0x00800000
    INP_UPPER_RUBBER_CRD1MSK                         = 0x00010000
    INP_SPINNER_CRD1MSK                              = 0x00020000
    INP_CTR_RGHT_RUBBER_CRD1MSK                      = 0x00040000
    INP_JKPOT_ROLLOVER_CRD1MSK                       = 0x00080000
    INP_BELOW_KICKOUT_RUBBER_CRD1MSK                 = 0x00100000
    SOL_TOP_DROP_RUBBER_CRD1MSK                      = 0x00200000
    INP_DROP_TRGT_1S_CRD1MSK                         = 0x01000000
    INP_DROP_TRGT_2H_CRD1MSK                         = 0x02000000
    INP_DROP_TRGT_3O_CRD1MSK                         = 0x04000000
    INP_DROP_TRGT_4O_CRD1MSK                         = 0x08000000
    INP_DROP_TRGT_5T_CRD1MSK                         = 0x10000000
    INP_DROP_TRGT_6E_CRD1MSK                         = 0x20000000
    INP_DROP_TRGT_7R_CRD1MSK                         = 0x40000000
    INP_DROP_BANK_MISS_CRD1MSK                       = 0x80000000
    INP_BTM_LFT_INLN_ROLLOVER_CRD3MSK                = 0x00010000
    INP_BTM_LFT_OUTLN_ROLLOVER_CRD3MSK               = 0x00020000
    INP_CTR_LOW_ROLLOVER_CRD3MSK                     = 0x00040000
    INP_BTM_RGHT_RUBBER_CRD3MSK                      = 0x00080000
    INP_BTM_RGHT_LOW_RUBBER_CRD3MSK                  = 0x00100000
    INP_SLAM_TILT_CRD3MSK                            = 0x01000000
    INP_TILT_CRD3MSK                                 = 0x02000000
    INP_COIN_DROP_CRD3MSK                            = 0x04000000
    INP_START_CRD3MSK                                = 0x08000000

    ## Input board bit names
    # Indexed into using the [InpBitNames](@ref inpBitNames.InpBitNames) class
    INP_BRD_BIT_NAMES = [ ["Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "UpRghtRoll", "UpCtrRoll", "UpLftRoll", "UpLftTopTrgt",
        "UpLftBtmTrgt", "CtrRghtRoll", "CtrCtrRoll", "CtrLftRoll",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused"],
        ["Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "UpRbr", "Spinner", "CtrRghtRbr", "JkpotRoll",
        "BlwKickRbr", "TopDropRbr", "Unused", "Unused",
        "DrpTrgt1S", "DrpTrgt2H", "DrpTrgt3O", "DrpTrgt4O",
        "DrpTrgt5T", "DrpTrgt6E", "DrpTrgt7R", "DropBnkMiss"],
        [ ],
        ["Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "BtmLftInLnRoll", "BtmLftOutLnRoll", "CtrLowRoll", "BtmRghtRbr",
        "BtmRghtLowRbr", "Unused", "Unused", "Unused",
        "SlamTilt", "Tilt", "CoinDrp", "Start",
        "Unused", "Unused", "Unused", "Unused"] ]

    ## Input board configuration
    INP_BRD_CFG = [ [rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE],
        [rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE],
        [ ],
        [rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE] ]

