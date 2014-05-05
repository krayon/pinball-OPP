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
# @file    procChains.py
# @author  Hugh Spahr
# @date    4/25/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief These are the processing chains.  It includes initial chains and normal
# processing chains that are run each time the rules thread runs.

#===============================================================================

from rulesFunc import RulesFunc
from rules.states import State
from rules.ledChains import LedChains

## Process chain lists.
class ProcChain:
    INIT_CHAIN_OFFSET = 1
    NORM_CHAIN_OFFSET = 2
    LED_CHAIN_OFFSET = 3
    
    ## Create process chain lists.
    #    - First entry is State number, only used to ease debugging
    #    - Second entry is initial processing functions, called only when first entering a state
    #    - Third entry are processing functions, called each time the rules thread runs
    #    - Third entry are processing functions, called each time the rules thread runs
    PROC_CHAIN = [ 
        [State.INIT, [RulesFunc.Proc_Init], [], []],
        [State.ATTRACT, [], [RulesFunc.Proc_Init, RulesFunc.Proc_Add_Coin], LedChains.LedCh_Attract],
        [State.PRESS_START, [RulesFunc.Proc_Press_Start_Init], [RulesFunc.Proc_Start_and_Coin], []],
        [State.START_GAME, [RulesFunc.Proc_Init_Game], [RulesFunc.Proc_Start_Game, RulesFunc.Proc_Start_and_Coin], []],
        [State.START_BALL, [RulesFunc.Proc_Start_Ball_Init], [RulesFunc.Proc_Start_Ball_Start, RulesFunc.Proc_Start_and_Coin], []],
        [State.BALL_IN_PLAY, [RulesFunc.Proc_Ball_In_Play_Init], [RulesFunc.Proc_Ball_In_Play_Start, RulesFunc.Proc_Start_and_Coin], []],
        [State.NORMAL_PLAY, [RulesFunc.Proc_Normal_Play_Init], [RulesFunc.Proc_Normal_Play], []],
        [State.SPECIAL_PLAY, [], [], []],
        [State.ERROR, [], [], []],
        [State.TILT, [RulesFunc.Proc_Tilt_Init], [RulesFunc.Proc_Tilt_State], []],
        [State.END_OF_BALL, [RulesFunc.Proc_End_Of_Ball], [], []],
        [State.INLANE_COMPLETE, [RulesFunc.Proc_Inlane_Comp], [], []],
        [State.TARGETS_COMPLETE, [RulesFunc.Proc_Targets_Comp_Init], [RulesFunc.Proc_Targets_Comp_State], []],
    ]
