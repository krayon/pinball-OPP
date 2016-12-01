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
# @file    ledBitNames.py
# @author  AutoGenerated
# @date    11/20/2016
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief These are the LED bit names.  It has a bitmask for each LED.

#===============================================================================

## LED bit name enumeration.
#  Contains a bit mask for each LED.  Can also contain bitfield masks.
#  Top most nibble contains the index of the LED card base 0.
class LedBitNames:
    def __init__(self):
        pass

    LED0W0_ALL_BITS_MSK              = 0x000000ff
    LED0W1_ALL_BITS_MSK              = 0x000100ff
    LED_SPINNER                      = 0x00000001
    LED_JKPOT                        = 0x00000002
    LED_4X                           = 0x00000004
    LED_5X                           = 0x00000008
    LED_2X                           = 0x00000010
    LED_3X                           = 0x00000020
    LED_KO_PICK_JOB                  = 0x00000040
    LED_KO_DUEL                      = 0x00000080
    LED_INLN_RGHT                    = 0x00010001
    LED_INLN_CTR                     = 0x00010002
    LED_INLN_LFT                     = 0x00010004
    LED_POP_UPCTR                    = 0x00010008
    LED_POP_UPLFT                    = 0x00010010
    LED_ROLL_RGHT                    = 0x00010020
    LED_ROLL_CTR                     = 0x00010040
    LED_ROLL_LFT                     = 0x00010080
    LED1W0_ALL_BITS_MSK              = 0x010000ff
    LED_DT_7                         = 0x01000001
    LED_DT_6                         = 0x01000002
    LED_DT_5                         = 0x01000004
    LED_DT_4                         = 0x01000008
    LED_DT_3                         = 0x01000010
    LED_DT_2                         = 0x01000020
    LED_DT_1                         = 0x01000040
    LED2W0_ALL_BITS_MSK              = 0x020000ff
    LED2W1_ALL_BITS_MSK              = 0x020100ff
    LED_LFT_OUTLN                    = 0x02000001
    LED_LFT_INLN                     = 0x02000002
    LED_MODE_POSSE                   = 0x02000004
    LED_MODE_HUSTLEJIVE              = 0x02000008
    LED_MODE_TRGTPRAC                = 0x02000010
    LED_MODE_CHKHIDE                 = 0x02000020
    LED_MODE_SNIPER                  = 0x02000040
    LED_MODE_SHARPE                  = 0x02000080
    LED_MODE_RIDEHELP                = 0x02010001
    LED_MODE_DUEL                    = 0x02010002
    LED_MODE_BARFGHT                 = 0x02010004
    LED_MODE_KILLALL                 = 0x02010008
    LED_MODE_TRKBNDT                 = 0x02010010
    LED3W0_ALL_BITS_MSK              = 0x030000ff
    LED_SHOOT_AGAIN                  = 0x03000001
    LED_POP_BTMUP                    = 0x03000002
    LED_POP_BTMLOW                   = 0x03000004
    LED_MARSHAL                      = 0x03000008
    LED_SHERIFF                      = 0x03000010
    LED_DEPUTY                       = 0x03000020
    LED_ROOKIE                       = 0x03000040

    ## LED board bit names
    # Indexed into using the [LedBitNames](@ref ledBitNames.LedBitNames) class
    LED_BRD_BIT_NAMES = [ ["Spinner", "Jkpot", "Spin4x", "Spin5x",
        "Spin2x", "Spin3x", "KOPickJob", "KODuel",
        "InlnRght", "InlnCtr", "InlnLft", "PopUpCtr",
        "PopUpLft", "RollRght", "RollCtr", "RollLft",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused"],
        ["DT7", "DT6", "DT5", "DT4",
        "DT3", "DT2", "DT1", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused"],
        ["LftOutln", "LftInln", "Posse", "HustleJive",
        "TrgtPrac", "ChkHide", "Sniper", "Sharpe",
        "RideHelp", "Duel", "BarFght", "KillAll",
        "TrkBndt", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused"],
        ["ShootAgain", "PopBtmUp", "PopBtmLow", "Marshal",
        "Sheriff", "Deputy", "Rookie", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused",
        "Unused", "Unused", "Unused", "Unused"] ]

