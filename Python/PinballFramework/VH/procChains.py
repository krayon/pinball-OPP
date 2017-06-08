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
# @file    procChains.py
# @author  AutoGenerated
# @date    04/27/2017
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief These are the processing chains.  It includes initial chains and normal
# processing chains that are run each time the rules thread runs.

#===============================================================================

from VH.rulesFunc import RulesFunc
from VH.states import State
from VH.ledChains import LedChains
from VH.soundChains import SoundChains
from VH.imageChains import ImageChains
from VH.sounds import Sounds

## Process chain lists.
#
#  Contains all the chains that are specific this this set of pinball rules.
class ProcChain():
    def __init__(self):
        pass

    INIT_CHAIN_OFFSET = 1
    NORM_CHAIN_OFFSET = 2
    IMAGE_CHAIN_OFFSET = 3
    SOUND_CHAIN_OFFSET = 4
    LED_CHAIN_OFFSET = 5
    VIDEO_CHAIN_OFFSET = 6

    ## Create process chain lists.
    #    - First entry is State number, only used to ease debugging
    #    - Second entry is initial processing functions, called only when first entering a state
    #    - Third entry are processing functions, called each time the rules thread runs
    #    - Fourth entry is the image chain
    #    - Fifth entry is the sound chain
    #    - Sixth entry is the LED chain
    #    - Seventh entry is the video chain
    PROC_CHAIN = [
        [State.STATE_INIT, [RulesFunc.Proc_Init], [], [], [], [], [] ],
        [State.STATE_ATTRACT, [RulesFunc.Init_Attract], [RulesFunc.Mode_Attract], ImageChains.ImageCh_Attract, SoundChains.SndCh_Attract, LedChains.LedCh_Attract, [] ],
        [State.STATE_INIT_GAME, [RulesFunc.Init_Init_Game], [RulesFunc.Mode_Init_Game], ImageChains.ImageCh_StartGame, [], [], [] ],
        [State.STATE_STARTBALL, [RulesFunc.Init_Start_Ball], [RulesFunc.Mode_Start_Ball], [], [], [], [] ],
        [State.STATE_NORMAL_PLAY, [RulesFunc.Init_Normal_Play], [RulesFunc.Mode_Normal_Play], [], [], [], [] ],
        [State.STATE_JUKEBOX, [RulesFunc.Init_Jukebox], [RulesFunc.Mode_Jukebox], [], [], [], [] ],
        [State.STATE_END_BALL, [RulesFunc.Init_End_Ball], [RulesFunc.Mode_End_Ball], [], [], [], [] ],
        [State.STATE_ERROR, [RulesFunc.Init_Error], [RulesFunc.Mode_Error], [], [], [], [] ],
        [State.STATE_TILT, [RulesFunc.Init_Tilt], [RulesFunc.Mode_Tilt], [], Sounds.SOUND_BALLDRAINNOGOOD, LedChains.LedCh_Tilt, [] ],
    ]
