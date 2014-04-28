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
# @file:   ledThread.py
# @author: Hugh Spahr
# @date:   4/27/2014
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
# This is the LED thread file that is used to change LEDs on and off.  It needs
# a thread to support blinking and communication to the hardware.
#
#===============================================================================

import errIntf
from gameData import GameData
from tkCmdFrm import TkCmdFrm
from threading import Thread
from rules.rulesData import RulesData
from ledBrd import LedBrd
import time

class LedThread(Thread):
    #private members
    _runLedThread = True
    _threadlock = 0
    _prevLedState = []
    
    def __init__(self):
        super(LedThread, self).__init__()

    #Initialize the SPI hardware
    def init(self):
        for index in range(RulesData.NUM_LED_BRDS):
            index = index
            LedThread._prevLedState.append(0)
        return(errIntf.CMD_OK)
    
    def start(self):
        super(LedThread, self).start()
    
    def ledExit(self):
        LedThread._runLedThread = False

    def proc_leds(self):
        for index in range(RulesData.NUM_LED_BRDS):
            if GameData.debug:
                GameData.tkLedBrd[index].updateLeds(LedBrd.currLedData[index])
            
    def run(self):
        count = 0
      
        while LedThread._runLedThread:
            #Process LEDs if not running in debug mode
            if not GameData.debug: 
                self.proc_leds()
            #Process LEDs if run button is active
            elif GameData.debug and TkCmdFrm.threadRun[TkCmdFrm.RULES_THREAD_IDX] and \
                    TkCmdFrm.toggleState[TkCmdFrm.RULES_THREAD_IDX]:
                self.proc_leds()
            
            #Sleep until next rules processing time
            time.sleep(.1)
            count += 1
