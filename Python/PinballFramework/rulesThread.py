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
import rs232Intf
from gameData import GameData
from tk.tkCmdFrm import TkCmdFrm
from rulesFunc import RulesFunc
from rules.procChains import ProcChain
from hwobjs.solBrd import SolBrd
from hwobjs.inpBrd import InpBrd
from tk.tkSolBrd import TkSolBrd
from tk.tkInpBrd import TkInpBrd
from rules.rulesData import RulesData
from globConst import GlobConst
from rules.soundChains import SoundChains
from stdFuncs import StdFuncs

## Rules thread class.
#
#  Create thread the runs the rules.  This includes updating solenoid and input boards
#  state, figuring out which rules chain need to be run, and running it.
class RulesThread(Thread):
    _runRulesThread = True
    _chainIndex = 0
    _soundChTime = 0
    _soundCmdWaitTime = 0
    
    #Create stdFunc instance
    _stdFuncs = StdFuncs()
    
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
        for index in xrange(SolBrd.numSolBrds):
            GameData.currSolStatus[index] = SolBrd.get_status(GameData.solBrd, index)
            if GameData.debug:
                GameData.currSolStatus[index] |= TkSolBrd.get_status(GameData.tkSolBrd[index])
        for index in xrange(InpBrd.numInpBrds):
            GameData.currInpStatus[index] = InpBrd.get_status(GameData.inpBrd, index)
            if GameData.debug:
                GameData.currInpStatus[index] |= TkInpBrd.get_status(GameData.tkInpBrd[index])
        
        #Figure out the correct processing chain
        if (GameData.gameMode != GameData.prevGameMode):
            GameData.prevGameMode = GameData.gameMode
            chain = ProcChain.PROC_CHAIN[GameData.gameMode][ProcChain.INIT_CHAIN_OFFSET]
            GameData.ledChain = ProcChain.PROC_CHAIN[GameData.gameMode][ProcChain.LED_CHAIN_OFFSET]
            GameData.newLedChain = True
            GameData.soundChain = ProcChain.PROC_CHAIN[GameData.gameMode][ProcChain.SOUND_CHAIN_OFFSET]
            GameData.newSoundChain = True
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

    ## Process the sound chains
    #
    #  If no sound chain return.  If the sound chain is new, set the index to 0 and
    #  set updateCmd flag.  Otherwise increment sound chain time and if it is
    #  longer than the command wait increment the index and set updateCmd flag.
    #  If updating the command, clear the time, grab the new command.  If it
    #  is a repeat, move index back to 0.  If it is a wait, update the LEDs and
    #  grab the new wait time.  If it is the end of the chain, clear the chain.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_sound_chain(self):
        # Check if the sound chain is not empty
        if GameData.soundChain:
            updateSound = False
            updateCmd = False
            clearChain = False
            
            # New LED chain is being started
            if GameData.newSoundChain:
                GameData.newSoundChain = False
                RulesThread._chainIndex = 0
                updateCmd = True
            else:
                RulesThread._soundChTime += GlobConst.RULES_SLEEP
                if (RulesThread._soundChTime > RulesThread._soundCmdWaitTime):
                    RulesThread._chainIndex += 1
                    updateCmd = True
            if updateCmd:
                RulesThread._soundChTime = 0
                soundCmd = GameData.soundChain[RulesThread._chainIndex][SoundChains.CH_CMD_OFFSET]
                
                # If this is repeat command, move index back to beginning
                if (soundCmd == SoundChains.REPEAT):
                    RulesThread._chainIndex = 0
                    soundCmd = GameData.soundChain[RulesThread._chainIndex][SoundChains.CH_CMD_OFFSET]
                if (soundCmd == SoundChains.WAIT):
                    RulesThread._soundCmdWaitTime = GameData.soundChain[RulesThread._chainIndex][SoundChains.PARAM_OFFSET]
                    updateSound = True
                elif (soundCmd == SoundChains.END_CHAIN):
                    updateSound = True
                    clearChain = True
            if updateSound:
                StdFuncs.Sounds(RulesThread._stdFuncs, GameData.soundChain[RulesThread._chainIndex][SoundChains.SOUND_OFFSET])
            if clearChain:
                GameData.soundChain = []
                
    ## Process scoring
    #
    #  If no sound chain return.  If the sound chain is new, set the index to 0 and
    #  set updateCmd flag.  Otherwise increment sound chain time and if it is
    #  longer than the command wait increment the index and set updateCmd flag.
    #  If updating the command, clear the time, grab the new command.  If it
    #  is a repeat, move index back to 0.  If it is a wait, update the LEDs and
    #  grab the new wait time.  If it is the end of the chain, clear the chain.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_scoring(self):
        if GameData.scoring:
            for cardNum in xrange(SolBrd.numSolBrds):
                if GameData.currSolStatus[cardNum] != 0:
                    for bit in xrange(rs232Intf.NUM_SOL_PER_BRD):
                        if (GameData.currSolStatus[cardNum] & (1 << bit)) != 0:
                            GameData.score[GameData.currPlayer] += RulesData.SOL_SCORE[GameData.scoreLvl][cardNum][bit]
            for cardNum in xrange(InpBrd.numInpBrds):
                if GameData.currInpStatus[cardNum] != 0:
                    for bit in xrange(rs232Intf.NUM_INP_PER_BRD):
                        if (GameData.currInpStatus[cardNum] & (1 << bit)) != 0:
                            GameData.score[GameData.currPlayer] += RulesData.INP_SCORE[GameData.scoreLvl][cardNum][bit]
        
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
            
            #Process the sound chain
            self.proc_sound_chain()
            
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
            
            #Process the scoring
            self.proc_scoring()
            
            #Sleep until next rules processing time
            time.sleep(float(GlobConst.RULES_SLEEP)/1000.0)
