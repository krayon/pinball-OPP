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
# @file    rulesThread.py
# @author  Hugh Spahr
# @date    1/18/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the rules thread file that is used to implement the rules for the
# pinball machine.

#===============================================================================

from threading import Thread
import time
from gameData import GameData
from tk.tkCmdFrm import TkCmdFrm
from rulesFunc import RulesFunc
from rules.procChains import ProcChain
from hwobjs.solBrd import SolBrd
from hwobjs.inpBrd import InpBrd
from tk.tkSolBrd import TkSolBrd
from tk.tkInpBrd import TkInpBrd


## Rules thread class.
#
#  Create thread the runs the rules.  This includes updating solenoid and input boards
#  state, figuring out which rules chain need to be run, and running it.
class RulesThread(Thread):
    _runRulesThread = True
    
    #Create rulesFunc instance
    rulesFunc = RulesFunc()

    ## The constructor.
    def __init__(self):
        super(RulesThread, self).__init__()
        
    ## Initialize rule thead
    #
    #  @param  self          [in]   Object reference
    def init(self):
        pass
        
    ## Start the rules thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def start(self):
        super(RulesThread, self).start()
    
    ## Process the rules thread
    #
    #  Grab status from solenoid and input boards and merge it with status from
    #  the tk interface.  If the mode has changed, run the INIT_CHAIN.  Otherwise
    #  run the NORM_CHAIN for the current mode.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
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
        
    ## Exit the rules thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def rulesExit(self):
        RulesThread._runRulesThread = False

    ## The rules thread
    #
    #  If debug is not set, just run the rules thread processing.  If debug is set,
    #  run debug processing if set to run the rules thread, or if a single step
    #  command has been received.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
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

