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
# @file:   rulesThread.py
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
# This is the rules thread file that is used to implement the rules for the
# pinball machine
#
#===============================================================================

from threading import Thread
import time
from gameData import GameData
from tkCmdFrm import TkCmdFrm
from rulesFunc import RulesFunc
from rules.procChains import ProcChain
from solBrd import SolBrd
from inpBrd import InpBrd
from tkSolBrd import TkSolBrd
from tkInpBrd import TkInpBrd


class RulesThread(Thread):
    _runRulesThread = True
    
    #Create rulesFunc instance
    rulesFunc = RulesFunc()

    def __init__(self):
        super(RulesThread, self).__init__()
        
    #Initialize rules thread
    def init(self):
        pass
        
    def start(self):
        #Verify correct number of boards
        #Configure the boards
        super(RulesThread, self).start()
    
    def proc_rules(self):
        #Update the inputs from solenoid and input cards
        for index in range(SolBrd.numSolBrds):
            GameData.currSolStatus[index] = SolBrd.get_status(GameData.solBrd, index)
            if GameData.debug:
                GameData.currSolStatus[index] |= TkSolBrd.get_status(GameData.tkSolBrd[index])
        for index in range(InpBrd.numInpBrds):
            GameData.currInpStatus[index] = InpBrd.get_status(GameData.inpBrd, index)
            if GameData.debug:
                GameData.currInpStatus[index] |= TkInpBrd.get_status(GameData.tkInpBrd[index])
        
        if (GameData.gameMode != GameData.prevGameMode):
            GameData.prevGameMode = GameData.gameMode
            chain = ProcChain.PROC_CHAIN[GameData.gameMode][ProcChain.INIT_CHAIN_OFFSET] 
        else:
            chain = ProcChain.PROC_CHAIN[GameData.gameMode][ProcChain.NORM_CHAIN_OFFSET]
            
        #Iterate over the chain processing
        for proc in chain:
            proc(RulesThread.rulesFunc)
        
    def rulesExit(self):
        RulesThread._runRulesThread = False

    def run(self):
        while RulesThread._runRulesThread:
            
            #Process rules if not running in debug mode
            if not GameData.debug: 
                self.proc_rules()
            #Process rules if run button is active
            elif GameData.debug and TkCmdFrm.threadRun[TkCmdFrm.RULES_THREAD_IDX] and \
                    TkCmdFrm.toggleState[TkCmdFrm.RULES_THREAD_IDX]:
                self.proc_rules()
            #Process rules if send step was pressed
            elif GameData.debug and (not TkCmdFrm.threadRun[TkCmdFrm.RULES_THREAD_IDX]) and \
                    TkCmdFrm.threadSendStep[TkCmdFrm.RULES_THREAD_IDX]:
                TkCmdFrm.threadSendStep[TkCmdFrm.RULES_THREAD_IDX] = False
                self.proc_rules()
            
            #Sleep until next rules processing time
            time.sleep(.01)

