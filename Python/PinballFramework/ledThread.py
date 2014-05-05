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
import time

## LED thread class.
#
#  Updates LEDs on the LED boards and the debug interface periodically.
class LedThread(Thread):
    #private members
    _runLedThread = True
    _threadlock = 0
    
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
        for index in range(RulesData.NUM_LED_BRDS):
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

    ## Process the LEDs
    #
    #  Periodically tk LED graphics.  Will eventually send SPI msg
    #  updates.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_leds(self):
        for index in range(RulesData.NUM_LED_BRDS):
            if GameData.debug:
                GameData.tkLedBrd[index].updateLeds(LedBrd.currLedData[index])
            
    ## The LED thread
    #
    #  If debug is not set, just run the LED thead processing.  If debug is set,
    #  run debug processing if set to run the rules thread, or if a single step
    #  command has been received.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def run(self):
        chainIndex = 0
        ledChTime = 0
        ledCmdWaitTime = 0
        
        #Create stdFunc instance
        stdFuncs = StdFuncs()
      
        while LedThread._runLedThread:
            # Check if the LED chain is not empty
            if GameData.ledChain:
                updateLeds = False
                updateCmd = False
                
                # New LED chain is being started
                if GameData.newLedChain:
                    GameData.newLedChain = False
                    chainIndex = 0
                    updateCmd = True
                else:
                    ledChTime += 100
                    if (ledChTime > ledCmdWaitTime):
                        chainIndex += 1
                        updateCmd = True
                if updateCmd:
                    ledChTime = 0
                    ledCmd = GameData.ledChain[LedChains.CHAIN_OFFSET][chainIndex][LedChains.CH_CMD_OFFSET]
                    
                    # If this is repeat command, move index back to beginning
                    if (ledCmd == LedChains.REPEAT):
                        chainIndex = 0
                        ledCmd = GameData.ledChain[LedChains.CHAIN_OFFSET][chainIndex][LedChains.CH_CMD_OFFSET]
                    if (ledCmd == LedChains.WAIT):
                        ledCmdWaitTime = GameData.ledChain[LedChains.CHAIN_OFFSET][chainIndex][LedChains.PARAM_OFFSET]
                        updateLeds = True
                    elif (ledCmd == LedChains.END_CHAIN):
                        GameData.ledChain = []
                if updateLeds:
                    StdFuncs.Led_Set(stdFuncs, GameData.ledChain[LedChains.MASK_OFFSET], \
                        GameData.ledChain[LedChains.CHAIN_OFFSET][chainIndex][LedChains.CH_LED_BITS_OFFSET])
                    
            #Process LEDs if not running in debug mode
            if not GameData.debug: 
                self.proc_leds()
            #Process LEDs if run button is active
            elif GameData.debug and TkCmdFrm.threadRun[TkCmdFrm.RULES_THREAD_IDX] and \
                    TkCmdFrm.toggleState[TkCmdFrm.RULES_THREAD_IDX]:
                self.proc_leds()
                    
            #Sleep until next rules processing time
            time.sleep(.1)
