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
# @file    ledThread.py
# @author  Hugh Spahr
# @date    4/27/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the LED thread file that is used to change LEDs on and off.  It needs
# a thread to support blinking and communication to the hardware.

#===============================================================================

import errIntf
from gameData import GameData
from tk.tkCmdFrm import TkCmdFrm
from threading import Thread
from rules.rulesData import RulesData
from hwobjs.ledBrd import LedBrd
from stdFuncs import StdFuncs
from rules.ledChains import LedChains
from globConst import GlobConst
import time

## LED thread class.
#
#  Updates LEDs on the LED boards and the debug interface periodically.
class LedThread(Thread):
    #private members
    _runLedThread = True
    _threadlock = 0
    _chainIndex = 0
    _ledChTime = 0
    _ledCmdWaitTime = 0
        
    #Create stdFunc instance
    _stdFuncs = StdFuncs()
    
    ## Holds previous LED state to see if there are changes
    _prevLedState = []
    
    ## The constructor.
    def __init__(self):
        super(LedThread, self).__init__()

    ## Initialize LED hardware
    #
    #  Initialize the SPI interface to the LED hardware.  Create
    #  previous LED state for each LED board using
    #  [NUM_LED_BRDS](@ref rules.rulesData.RulesData.NUM_LED_BRDS).
    #
    #  @param  self          [in]   Object reference
    #  @return CMD_OK
    def init(self):
        for index in xrange(RulesData.NUM_LED_BRDS):
            index = index
            LedThread._prevLedState.append(0)
        return(errIntf.CMD_OK)
    
    ## Start the comms thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def start(self):
        super(LedThread, self).start()
    
    ## Exit the LED thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def ledExit(self):
        LedThread._runLedThread = False

    ## Process the LED chains
    #
    #  If no LED chain return.  If the LED chain is new, set the index to 0 and
    #  set updateCmd flag.  Otherwise increment LED chain time and if it is
    #  longer than the command wait increment the index and set updateCmd flag.
    #  If updating the command, clear the time, grab the new command.  If it
    #  is a repeat, move index back to 0.  If it is a wait, update the LEDs and
    #  grab the new wait time.  If it is the end of the chain, clear the chain.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_led_chain(self):
        # Check if the LED chain is not empty
        if GameData.ledChain:
            updateLeds = False
            updateCmd = False
            clearChain = False
            
            # New LED chain is being started
            if GameData.newLedChain:
                GameData.newLedChain = False
                LedThread._chainIndex = 0
                updateCmd = True
            else:
                LedThread._ledChTime += GlobConst.LED_SLEEP
                if (LedThread._ledChTime > LedThread._ledCmdWaitTime):
                    LedThread._chainIndex += 1
                    updateCmd = True
            if updateCmd:
                LedThread._ledChTime = 0
                ledCmd = GameData.ledChain[LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedChains.CH_CMD_OFFSET]
                
                # If this is repeat command, move index back to beginning
                if (ledCmd == LedChains.REPEAT):
                    LedThread._chainIndex = 0
                    ledCmd = GameData.ledChain[LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedChains.CH_CMD_OFFSET]
                if (ledCmd == LedChains.WAIT):
                    LedThread._ledCmdWaitTime = GameData.ledChain[LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedChains.PARAM_OFFSET]
                    updateLeds = True
                elif (ledCmd == LedChains.END_CHAIN):
                    updateLeds = True
                    clearChain = True
            if updateLeds:
                StdFuncs.Led_Set(LedThread._stdFuncs, GameData.ledChain[LedChains.MASK_OFFSET], \
                    GameData.ledChain[LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedChains.CH_LED_BITS_OFFSET])
            if clearChain:
                GameData.ledChain = []
            
    ## Process the LEDs
    #
    #  Periodically update tk LED graphics.  Will eventually send SPI msg
    #  updates.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_leds(self):
        for index in xrange(RulesData.NUM_LED_BRDS):
            if (LedBrd.currBlinkLeds[index] != 0):
                LedBrd.currLedData[index] ^= LedBrd.currBlinkLeds[index]
            
    ## The LED thread
    #
    #  If debug is not set, just run the LED thread processing.  If debug is set,
    #  run debug processing if set to run the rules thread, or if a single step
    #  command has been received.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def run(self):
      
        while LedThread._runLedThread:
            #Process LED chain
            self.proc_led_chain()
            
            #Process LEDs if not running in debug mode
            if not GameData.debug: 
                self.proc_leds()
            
            #Process LEDs if run button is active
            elif GameData.debug and TkCmdFrm.threadRun[TkCmdFrm.RULES_THREAD_IDX] and \
                    TkCmdFrm.toggleState[TkCmdFrm.RULES_THREAD_IDX]:
                self.proc_leds()
                    
            #Sleep until next LED processing time
            time.sleep(float(GlobConst.LED_SLEEP)/1000.0)
