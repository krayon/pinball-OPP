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
# @file    tkinterThread.py
# @author  Hugh Spahr
# @date    3/26/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the tkinter thread file that is used for the debug GUI.

#===============================================================================

from Tkinter import *
from ttk import *

from threading import Thread
from tkCmdFrm import TkCmdFrm
from tkInpBrd import TkInpBrd
from tkSolBrd import TkSolBrd
from tkLedBrd import TkLedBrd
from hwobjs.ledBrd import LedBrd
from hwobjs.solBrd import SolBrd
from hwobjs.inpBrd import InpBrd
import time
from rules.rulesData import RulesData
import rs232Intf
from gameData import GameData
from globConst import GlobConst

## Tkinter thread class.
#  Create tk frame instances for all the configured hardware.
#  Update the command frame.
class TkinterThread(Thread):
    doneInit = False
    
    #private members
    _runTkinterThread = True
    
    ## The constructor.
    def __init__(self):
        super(TkinterThread, self).__init__()
        
    ## Init the tkinter thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def init(self):
        pass
    
    ## Start the tkinter thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def start(self):
        super(TkinterThread, self).start()
    
    ## Exit the tkinter thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def tkinterExit(self):
        TkinterThread._runTkinterThread = False
    
    ## The tkinter thread
    #
    #  Create the tk frames based on
    #  [INV_ADDR_LIST](@ref rules.rulesData.RulesData.INV_ADDR_LIST) and
    #  [NUM_LED_BRDS](@ref rules.rulesData.RulesData.NUM_LED_BRDS).  Mark
    #  doneInit as True so debug inputs can be polled.  Update the current
    #  state string periodically.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def run(self):
        count = 0
        root = Tk()
        root.wm_title("Debug Window")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        bgndFrm = Frame(root)
        bgndFrm.grid()
        cmdFrm = TkCmdFrm(bgndFrm)
        numInpBrds = 0
        numSolBrds = 0
        for i in xrange(len(RulesData.INV_ADDR_LIST)):
            if ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_INP_CARD)): 
                GameData.tkInpBrd.append(TkInpBrd(numInpBrds, i, RulesData.INV_ADDR_LIST[i], bgndFrm))
                numInpBrds += 1
            elif ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_SOL_CARD)):
                GameData.tkSolBrd.append(TkSolBrd(numSolBrds, i, RulesData.INV_ADDR_LIST[i], bgndFrm))
                numSolBrds += 1
        for i in xrange(RulesData.NUM_LED_BRDS):
            GameData.tkLedBrd.append(TkLedBrd(i, numSolBrds + numInpBrds + i + 1, bgndFrm))
        root.update()
        TkinterThread.doneInit = True
      
        while TkinterThread._runTkinterThread:
            root.update()
            cmdFrm.Update_Cmd_Frm()
            for i in xrange(RulesData.NUM_LED_BRDS):
                GameData.tkLedBrd[i].updateLeds(LedBrd.currLedData[i])
            for i in xrange(numSolBrds):
                GameData.tkSolBrd[i].update_status_field(SolBrd.currSolData[i])
            for i in xrange(numInpBrds):
                GameData.tkInpBrd[i].update_status_field(InpBrd.currInpData[i])
            count += 1
            time.sleep(float(GlobConst.TK_SLEEP)/1000.0)
