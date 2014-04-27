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
# @file:   tkinterThread.py
# @author: Hugh Spahr
# @date:   3/26/2014
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
# This is the tkinter thread file that is used for the debug GUI.
#
#===============================================================================

from Tkinter import *
from ttk import *

from threading import Thread
from tkCmdFrm import TkCmdFrm
from tkInpBrd import TkInpBrd
from tkSolBrd import TkSolBrd
from tkLedBrd import TkLedBrd
import time
from rules.rulesData import RulesData
import rs232Intf
from gameData import GameData

class TkinterThread(Thread):
    doneInit = False
    
    def __init__(self):
        super(TkinterThread, self).__init__()
        
        #Some queue stuff to send data back and forth

        #private members
        self._runTkinterThread = True

    #Initialize comms to the hardware
    def init(self):
        pass
    
    def start(self):
        super(TkinterThread, self).start()
    
    def tkinterExit(self):
        self._runTkinterThread = False
    
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
        for i in range(len(RulesData.INV_ADDR_LIST)):
            if ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_INP_CARD)): 
                GameData.tkInpBrd.append(TkInpBrd(numInpBrds, i, RulesData.INV_ADDR_LIST[i], bgndFrm))
                numInpBrds += 1
            elif ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_SOL_CARD)):
                GameData.tkSolBrd.append(TkSolBrd(numSolBrds, i, RulesData.INV_ADDR_LIST[i], bgndFrm))
                numSolBrds += 1
        for i in range(RulesData.NUM_LED_BRDS):
            GameData.tkLedBrd.append(TkLedBrd(i, numSolBrds + numInpBrds + i + 1, bgndFrm))
        root.update()
        TkinterThread.doneInit = True
      
        while self._runTkinterThread:
            root.update()
            cmdFrm.Update_Cmd_Frm()
            count += 1
            time.sleep(.1)
