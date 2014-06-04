#!/usr/bin/env python
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
# @file    rulesData.py
# @author  Hugh Spahr
# @date    1/18/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the rules data.  It includes sound files, general illumination
# locations, and feature light locations, and string names for the debug window.

#===============================================================================

import rs232Intf
from rules.states import State

## Rule data class.
#  Contains most of the information for the configuration of the pinball machine
class RulesData:
    ## Sound file list
    # Indexed into using the [Sounds](@ref rules.sounds.Sounds) class
    SND_FILES = ["sounds/wah_wuh.wav", "sounds/ding_ding.wav", "sounds/opendoor.wav",
               "sounds/jump.wav", "sounds/wfall1.wav", "sounds/wfall2.wav", "sounds/wfall3.wav"]
    
    ## Background sound file list
    # Indexed into using the [BgndMusic](@ref rules.sounds.BgndMusic) class
    BGND_MUSIC_FILES = ["sounds/bgndtrack.mp3"]
    
    ## Background images
    # Indexed into using the [Images](@ref rules.images.Images) class
    BGND_GRAPHIC_FILES = ["graphics/full_bgnd_image.jpg", "graphics/left_guy.jpg",
                          "graphics/right_guy.jpg", "graphics/lftctr_guy.jpg"]
    
    ## Number of balls per game
    BALLS_PER_GAME = 3
    
    ## Maximum number of players per game
    MAX_NUM_PLYRS = 4
    
    ## Radius of feature and GI lights
    LGHT_RADIUS = 20
    
    ## Location of feature lights
    # Located using actual screen x,y coordinates.  Auto scaled in simulation.
    # Only used if backglass is in front of monitor
    FEATURE_LGHT_POS = []       #Ex:  [[200, 300], [300,300], [400,300]]
    
    ## Location of general illumination lights
    # Located using actual screen x,y coordinates.  Auto scaled in simulation.
    # Only used if backglass is in front of monitor
    GI_LGHT_POS = []            #Ex: [[200,100], [300,200], [400,100]]
    
    ## Switch input point values
    SCORE_INC = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    ## Number of LED boards in the system
    NUM_LED_BRDS = 1
    
    ## Board inventory list
    # Used to determine number of solenoid and input boards and order in chain.
    INV_ADDR_LIST = [0x10, 0x00]

    ## Input board bit names
    # Indexed into using the [InpBitNames](@ref rules.inpBitNames.InpBitNames) class
    INP_BRD_BIT_NAMES = [["CoinDrop", "StartBtn", "TiltSwitch", "Spinner",
                    "LftOutln", "RghtOutln", "LftFlipLn", "RghtFlipLn",
                    "BallAtPlunger", "InlaneRght", "InlaneCtr", "InlaneLft",
                    "LftTrgt1", "LftTrgt2", "RghtTrgt1", "RghtTrgt2"]]

    ## Input board scoring
    INP_SCORE = [ [ [ 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1 ] ],   # Normal scoring
                  [ [ 0, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2 ] ] ]  # Special scoring

    ## Input board configuration
    INP_BRD_CFG = [ [ rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_FALL_EDGE, \
         rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, \
         rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, \
         rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE, rs232Intf.CFG_INP_FALL_EDGE ] ]

    ## Solenoid board bit names
    # Indexed into using the [SolBitNames](@ref rules.solBitNames.SolBitNames) class
    SOL_BRD_BIT_NAMES = [["RghtFlip", "LftFlip", "RghtSlingshot", "LftSlingshot",
                    "BallInPlay", "PopBumper2", "PopBumper1", "KickoutHole"]]

    ## Input board scoring
    SOL_SCORE = [ [ [ 0, 0, 0, 0, 0, 1, 1, 0 ] ],   # Normal scoring
                  [ [ 0, 0, 0, 0, 0, 2, 2, 0 ] ] ]  # Special scoring
    
    ## Solenoid board configuration
    # Three bytes for each solenoid being configured
    SOL_BRD_CFG = [ [ rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
         rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', \
         rs232Intf.CFG_SOL_AUTO_CLR, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', \
         rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00' ] ]

    ## LED board bit names
    # Indexed into using the [LedBitNames](@ref rules.ledBitNames.LedBitNames) class
    LED_BRD_BIT_NAMES = [["InlaneRght", "InlaneCtr", "InlaneLft", "LftTrgt1",
                    "LftTrgt2", "RghtTrgt1", "RghtTrgt2", "Special"]]

    ## State name strings.
    # Indexed into using [State](@ref rules.states.State) enumeration
    STATE_STR = ["Init", "Attract", "Press_Start", "Start_Game",
                    "Start_Ball", "Ball_in_Play", "Normal_Play", "Error",
                    "Tilt", "End_of_Ball", "Mode_Targets_Complete"]
    
    ## Initial State
    INIT_MODE = State.INIT
