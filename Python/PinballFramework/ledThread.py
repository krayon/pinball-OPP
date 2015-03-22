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
from tk.tkCmdFrm import TkCmdFrm
from threading import Thread
from hwobjs.ledBrd import LedBrd
from globConst import GlobConst
import time
import platform
if platform.release() == "XP":
    import parallel

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
    _commsActive = False
    
    # Parallel port hardware control lines
    _CLK = 0x04
    _DATA = 0x01
    _LATCH = 0x02
    
    ## Holds previous LED state to see if there are changes
    _prevLedState = []

    GameData = None
    
    ## The constructor.
    def __init__(self):
        super(LedThread, self).__init__()
        self.blinkOn = False
        if platform.release() == "XP":
            self._pport = parallel.Parallel()
        else:
            self._pport = None        
        # HRS: Debug
        self.currVal = 0
        self.count = 0
        self.outData = [0] * 6
        self.sleep = 0

    ## Initialize LED hardware
    #
    #  Initialize the SPI interface to the LED hardware.  Create
    #  previous LED state for each LED board using
    #  [NUM_LED_BRDS](@ref rules.rulesData.LedBitNames.NUM_LED_BRDS).
    #
    #  @param  self          [in]   Object reference
    #  @return CMD_OK
    def init(self, gameData):
        LedThread.GameData = gameData
        for index in xrange(LedThread.GameData.LedBitNames.NUM_LED_BRDS):
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
        if LedThread.GameData.ledChain:
            updateLeds = False
            updateCmd = False
            clearChain = False
            
            # New LED chain is being started
            if LedThread.GameData.newLedChain:
                LedThread.GameData.newLedChain = False
                LedThread._chainIndex = 0
                updateCmd = True
            else:
                LedThread._ledChTime += GlobConst.LED_SLEEP
                if (LedThread._ledChTime > LedThread._ledCmdWaitTime):
                    LedThread._chainIndex += 1
                    updateCmd = True
            if updateCmd:
                LedThread._ledChTime = 0
                ledCmd = LedThread.GameData.ledChain[LedThread.GameData.LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedThread.GameData.LedChains.CH_CMD_OFFSET]
                
                # If this is repeat command, move index back to beginning
                if (ledCmd == LedThread.GameData.LedChains.REPEAT):
                    LedThread._chainIndex = 0
                    ledCmd = LedThread.GameData.ledChain[LedThread.GameData.LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedThread.GameData.LedChains.CH_CMD_OFFSET]
                if (ledCmd == LedThread.GameData.LedChains.WAIT):
                    LedThread._ledCmdWaitTime = LedThread.GameData.ledChain[LedThread.GameData.LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedThread.GameData.LedChains.PARAM_OFFSET]
                    updateLeds = True
                elif (ledCmd == LedThread.GameData.LedChains.END_CHAIN):
                    updateLeds = True
                    clearChain = True
            if updateLeds:
                LedThread.GameData.StdFuncs.Led_Set(LedThread.GameData.ledChain[LedThread.GameData.LedChains.MASK_OFFSET], \
                    LedThread.GameData.ledChain[LedThread.GameData.LedChains.CHAIN_OFFSET][LedThread._chainIndex][LedThread.GameData.LedChains.CH_LED_BITS_OFFSET])
            if clearChain:
                LedThread.GameData.ledChain = []
            
    ## Process the LEDs
    #
    #  Periodically update tk LED graphics.  Will eventually send SPI msg
    #  updates.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    #
    #  @Note:  List must be reversed since the contents of the last card in
    #  the chain must be written first.
    def proc_leds(self):
        # Copy the list and reverse the direction
        ledData = LedBrd.currLedData[::-1]
        self.blinkOn = not self.blinkOn
        if (self.blinkOn):
            blinkData = LedBrd.currBlinkLeds[::-1]
            for index in xrange(LedThread.GameData.LedBitNames.NUM_LED_BRDS):
                ledData[index] |= blinkData[index]
        if (self._pport != None):
            for index in xrange(LedThread.GameData.LedBitNames.NUM_LED_BRDS):
                ledData[index] &= 0xff
                ledData[index] ^= 0xff
            self.updateLights(ledData)
            
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
            if not LedThread.GameData.debug: 
                self.proc_leds()
            
            #Process LEDs if run button is active
            elif LedThread.GameData.debug and TkCmdFrm.threadRun[TkCmdFrm.RULES_THREAD_IDX] and \
                    TkCmdFrm.toggleState[TkCmdFrm.RULES_THREAD_IDX]:
                self.proc_leds()
                    
            #Sleep until next LED processing time
            time.sleep(float(GlobConst.LED_SLEEP)/1000.0)
            
    ## Update lights
    #
    #  Update all lights using byte list
    #
    #  @param  self          [in]   Object reference
    #  @param  byteList      [in]   List of bytes to send
    #  @return None 
    def updateLights(self, byteList):
        for data in byteList:
            self.sendByte(data)
        self.endWrite()

    ## Send byte
    #
    #  Bit banging the parallel port control/data lines to send a byte
    #
    #  @param  self          [in]   Object reference
    #  @param  data          [in]   Byte to send
    #  @return None 
    def sendByte(self, data):
        for i in xrange(8):
            if (data & (1 << i) != 0):
                #Data bit is set, so clear it
                dataOut = LedThread._DATA
            else:
                #Data bit is clear, so set it
                dataOut = 0
            #Set the data up, clock is low, and latch is low
            self._pport.setData(dataOut)
            if (self.sleep != 0):
                time.sleep(self.sleep)
            #Clock the data bit in
            self._pport.setData(dataOut | LedThread._CLK)
            if (self.sleep != 0):
                time.sleep(self.sleep)

    ## End write
    #
    #  End the write and latch the data
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def endWrite(self):
        #Bring the clock low, data doesn't matter, latch remains low
        self._pport.setData(0)
        if (self.sleep != 0):
            time.sleep(self.sleep)
        #Bring the latch high
        self._pport.setData(LedThread._LATCH)
        if (self.sleep != 0):
            time.sleep(self.sleep)
        #Bring the latch low to end the cycle
        self._pport.setData(0)
        if (self.sleep != 0):
            time.sleep(self.sleep)
