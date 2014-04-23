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
# @file:   rulesData.py
# @author: Hugh Spahr
# @date:   1/18/2014
#
# @note:   Open Pinball Project
#          Copyright 2014, Hugh Spahr
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
# This is the rules data.  This include sound files, general illumination, and
# feature lights.
#
#===============================================================================

vers = '00.00.02'
import rs232Intf

class RulesData:
    #sound file list, note:  must be wav files
    SND_FILES = ["sounds/wah_wuh.wav", "sounds/ding_ding.wav", "sounds/opendoor.wav",
               "sounds/jump.wav", "sounds/wfall1.wav", "sounds/wfall2.wav", "sounds/wfall3.wav"]
    
    BALLS_PER_GAME = 3
    MAX_NUM_PLYRS = 4
    
    #feature lights list
    #located using actual screen x,y coordinates (auto scaled to simulation)
    LGHT_RADIUS = 20
    FEATURE_LGHT_POS = [[200,200], [300,300], [400,300], [500,300],
                      [600,300], [700,300], [800,300], [900,300],
                      [1000,300], [1100,200]]
    
    #General illumination lights list
    #located using actual screen x,y coordinates (auto scaled to simulation)
    GI_LGHT_POS = [[200,100], [300,100], [400,100], [500,100],
                 [600,100], [700,100], [800,100], [900,100],
                 [1000,100], [1100,100]]
    
    #Switch input point values
    #just simple values to add to the active player's score
    SCORE_INC = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    #Number of LED boards in the system and inventory list
    NUM_LED_BRDS = 1
    INV_ADDR_LIST = [0x10, 0x00]

    #Input board bit names
    INP_BRD_BIT_NAMES = [["CoinDrop", "StartBtn", "TiltSwitch", "Spinner",
                    "LftOutln", "RghtOutln", "LftFlipLn", "RghtFlipLn",
                    "BallAtPlunger", "InlaneLft", "InlaneCtr", "InlaneRght",
                    "LftTrgt1", "LftTrgt2", "RghtTrgt1", "RghtTrgt2"]]

    INP_BRD_CFG = [ [ rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
         rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, \
         rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, \
         rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE ] ]


    #Solenoid board bit names
    SOL_BRD_BIT_NAMES = [["LftFlip", "RghtFlip", "LftSlingshot", "RghtSlingshot",
                    "BallInPlay", "PopBumper1", "PopBumper2", "KickoutHole"]]

    SOL_BRD_CFG = [ [ rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
         rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', \
         rs232Intf.CFG_SOL_AUTO_CLR, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', \
         rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00' ] ]

    #LED board bit names
    LED_BRD_BIT_NAMES = [["InlaneLft", "InlaneCtr", "InlaneRght", "LftTrgt1",
                    "LftTrgt2", "RghtTrgt1", "RghtTrgt2", "Special"]]

    #State name strings.  Must match State enumeration
    STATE_STR = ["Init", "Attract", "Press_Start", "Start_Game",
                    "Start_Ball", "Ball_in_Play", "Normal_Play", "Special_Play",
                    "Error", "Tilt", "End_of_Ball", "Inlane_Complete",
                    "Mode_Targets_Complete"]

class State:
    INIT = 0
    ATTRACT = 1
    PRESS_START = 2
    START_GAME = 3
    START_BALL = 4
    BALL_IN_PLAY = 5
    NORMAL_PLAY = 6
    SPECIAL_PLAY = 7
    ERROR = 8
    TILT = 9
    END_OF_BALL = 10
    INLANE_COMPLETE = 11
    MODE_TARGETS_COMPLETE = 12

#Top most nibble is the input card index base 0
class InpBitNames:
    COIN_DROP = 0x00001
    START_BTN = 0x00002
    TILT_SWITCH = 0x00004
    SPINNER = 0x00008
    LFT_OUT_LN = 0x00010
    RGHT_OUT_LN = 0x00020
    LFT_FLIP_LN = 0x00040
    RGHT_FLIP_LN = 0x00080
    BALL_AT_PLUNGER = 0x00100
    INLANE_LFT = 0x00200
    INLANE_CTR = 0x00400
    INLANE_RGHT = 0x00800
    INLANE_MSK = 0x00e00
    LFT_TRGT_1 = 0x01000
    LFT_TRGT_2 = 0x02000
    RGHT_TRGT_1 = 0x04000
    RGHT_TRGT_2 = 0x08000
    TRGT_MSK = 0x0f000

#Top most nibble is the solenoid card index base 0
class SolBitNames:
    LFT_FLIP = 0x00001
    RGHT_FLIP = 0x00002
    LFT_SLINGSHOT = 0x00004
    RGHT_SLINGSHOT = 0x00008
    BALL_IN_PLAY = 0x00010
    POP_BUMPER_1 = 0x00020
    POP_BUMPER_2 = 0x00040
    KICKOUT_HOLE = 0x00080

#Top most nibble is the LED card index base 0
class LedBitNames:
    INLANE_LFT = 0x00001
    INLANE_CTR = 0x00002
    INLANE_RGHT = 0x00004
    INLANE_MSK = 0x00007
    LFT_TRGT_1 = 0x00008
    LFT_TRGT_2 = 0x00010
    RGHT_TRGT_1 = 0x00020
    RGHT_TRGT_2 = 0x00040
    TRGT_MSK = 0x00078
    SPECIAL = 0x00080

class Timers:
    KICKOUT_TIMER = 0x0001
    BALL_LOCATE = 0x0002
    SPECIAL_TIMER = 0x0004

class Sounds:
    WAH_WUH = 0
    DING_DING_DING = 1
    OPEN_DOOR = 2
    JUMP = 3
    WATERFALL1 = 4
    WATERFALL2 = 5
    WATERFALL3 = 6
