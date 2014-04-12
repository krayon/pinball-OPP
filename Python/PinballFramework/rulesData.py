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

class RulesData:
    #sound file list, note:  must be wav files
    SND_FILES = ["sounds/wah_wuh.wav", "sounds/ding_ding.wav", "sounds/opendoor.wav",
               "sounds/jump.wav", "sounds/wfall1.wav", "sounds/wfall2.wav", "sounds/wfall3.wav"]
    
    BALLS_PER_GAME = 3
    
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

    #Number of boards in the system
    NUM_LED_BRDS = 1
    INV_ADDR_LIST = [0x10, 0x00]

    #Input board bit names
    INP_BRD_BIT_NAMES = [["CoinDrop", "StartBtn", "TiltSwitch", "Spinner",
                    "LftOutln", "RghtOutln", "LftFlipLn", "RghtFlipLn",
                    "BallAtPlunger", "InlaneLft", "InlaneCtr", "InlaneRght",
                    "LftTrgt1", "LftTrgt2", "RghtTrgt1", "RghtTrgt2"]]

    #Solenoid board bit names
    SOL_BRD_BIT_NAMES = [["LftFlip", "RghtFlip", "LftSlingshot", "RghtSlingshot",
                    "BallInPlay", "PopBumper1", "PopBumper2", "KickoutHole"]]

    #LED board bit names
    LED_BRD_BIT_NAMES = [["InlaneLft", "InlaneCtr", "InlaneRght", "LftTrgt1",
                    "LftTrgt2", "RghtTrgt1", "RghtTrgt2", "Special"]]
