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
# @date    02/02/2015
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
    COIN_DROP                        = 0x00001
    START_BTN                        = 0x00002
    TILT_SWITCH                      = 0x00004
    SPINNER                          = 0x00008
    LFT_OUT_LN                       = 0x00010
    RGHT_OUT_LN                      = 0x00020
    LFT_FLIP_LN                      = 0x00040
    RGHT_FLIP_LN                     = 0x00080
    BALL_AT_PLUNGER                  = 0x00100
    INLANE_RGHT                      = 0x00200
    INLANE_CTR                       = 0x00400
    INLANE_LFT                       = 0x00800
    LFT_TRGT_1                       = 0x01000
    LFT_TRGT_2                       = 0x02000
    RGHT_TRGT_1                      = 0x04000
    RGHT_TRGT_2                      = 0x08000

    ## Input board bit names
    # Indexed into using the [InpBitNames](@ref inpBitNames.InpBitNames) class
    INP_BRD_BIT_NAMES = [ ["CoinDrop", "StartBtn", "TiltSwitch", "Spinner",
        "LftOutln", "RghtOutln", "LftFlipLn", "RghtFlipLn",
        "BallAtPlunger", "InlaneRght", "InlaneCtr", "InlaneLft",
        "LftTrgt1", "LftTrgt2", "RghtTrgt1", "RghtTrgt2"] ]

    ## Input board configuration
    INP_BRD_CFG = [ [rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE,
        rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE] ]

