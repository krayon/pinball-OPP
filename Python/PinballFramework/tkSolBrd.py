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
# @file:   tkSolBrd.py
# @author: Hugh Spahr
# @date:   4/1/2014
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
# This is the tk solenoid board interface.  It allows switch inputs to be
# simulated, and the displays the current status.  It also allows solenoids
# to be test fired. 
#
#===============================================================================

vers = '00.00.01'

import rs232Intf
import Tkinter as tk
from rulesData import RulesData

class tkSolBrd():
    brdAddr = 0
    brdNum = 0
    brdPos = 0
    dispInpValue = 0
    statLbl = 0
    indBitStatLbl = []
    indBitOptMenu = []
    toggleBtn = []
    toggleState = []
    solCardFrm = 0
    btnCfgBitfield = 0              #Set bits to 1 to default to toggle buttons
    simSwitchBits = 0
    pulseSolBits = 0
    
    def __init__(self, brdNum, brdPos, addr, parentFrm):
        self.brdNum = brdNum
        self.brdPos = brdPos
        self.brdAddr = addr
        self.statLbl = tk.StringVar()
        
        #Create main frame
        self.solCardFrm = tk.Frame(parentFrm, padx = 5, pady = 5, borderwidth = 5, relief=tk.RAISED)
        self.solCardFrm.grid(column = 0, row = brdPos)
        
        #Create card info frame
        solCardInfoFrm = tk.Frame(self.solCardFrm)
        solCardInfoFrm.grid(column = 8, row = 0)
        
        #Add card info
        tmpLbl = tk.Label(solCardInfoFrm, text="Sol Card %d" % (brdNum + 1))
        tmpLbl.grid(column = 0, row = 0)
        tmpLbl = tk.Label(solCardInfoFrm, text="Addr = 0x%02x" % addr)
        tmpLbl.grid(column = 0, row = 1)
        tmpLbl = tk.Label(solCardInfoFrm, text="Status")
        tmpLbl.grid(column = 0, row = 2)
        tmpLbl = tk.Label(solCardInfoFrm, textvariable=self.statLbl, relief=tk.SUNKEN)
        self.statLbl.set("0x%02x" % self.dispInpValue)
        tmpLbl.grid(column = 0, row = 3)

        for i in range(rs232Intf.NUM_SOL_PER_BRD):
            tkSolBrd.createBitFrame(self, i)

    def toggle(self, bit):
        #If this is configured as a toggle button
        if (self.btnCfgBitfield & (1 << bit) != 0):
            self.toggleState[bit] = not self.toggleState[bit]
            if self.toggleState[bit]:
                self.toggleBtn[bit].config(relief=tk.SUNKEN)
                self.simSwitchBits &= ~(1 << bit)
            else:
                self.toggleBtn[bit].config(relief=tk.RAISED)
                self.simSwitchBits |= (1 << bit)
        #Else this is a pulsed button, set the bit and it will be auto cleared
        else:
            self.simSwitchBits |= (1 << bit)
        print "Bits = 0x%04x" % self.simSwitchBits

    def pulsesol(self, bit):
        self.pulseSolBits |= (1 << bit)
            
    def optmenucallback(self, bit):
        if self.indBitOptMenu[bit].get() == "Pulse":
            self.toggleBtn[bit].config(relief=tk.RAISED)
            self.toggleState[bit] = False
            self.btnCfgBitfield &= ~(1 << bit)
            self.simSwitchBits &= ~(1 << bit)
        else:
            self.btnCfgBitfield |= (1 << bit)
            if self.toggleState[bit]:
                self.simSwitchBits &= ~(1 << bit)
            else:
                self.simSwitchBits |= (1 << bit)
            
    def createBitFrame(self, bit):
        solCardBitFrm = tk.Frame(self.solCardFrm, padx = 5, pady = 5, borderwidth = 5, relief=tk.RAISED)
        solCardBitFrm.grid(column = bit, row = 0)
        tmpLbl = tk.Label(solCardBitFrm, text="Name: %s" % RulesData.SOL_BRD_BIT_NAMES[self.brdNum][bit])
        tmpLbl.grid(column = 0, row = 0, columnspan = 2)
        
        #Option menu for button presses
        self.indBitOptMenu.append(tk.StringVar())
        if (self.btnCfgBitfield & (1 << bit)):
            self.indBitOptMenu[bit].set("Toggle")
        else:
            self.indBitOptMenu[bit].set("Pulse")
        tmpOM = tk.OptionMenu(solCardBitFrm, self.indBitOptMenu[bit], "Pulse", "Toggle")
        tmpOM.grid(column = 0, row = 1, columnspan = 2)
        self.indBitOptMenu[bit].trace("w", lambda name, index, op, tmp=bit: self.optmenucallback(tmp))
        
        #Button code
        tmpBtn = tk.Button(solCardBitFrm, text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
        tmpBtn.grid(column = 0, row = 2, columnspan = 2)
        self.toggleBtn.append(tmpBtn)
        self.toggleState.append(False)
        
        tmpLbl = tk.Label(solCardBitFrm, text="Value")
        tmpLbl.grid(column = 0, row = 3)
        self.indBitStatLbl.append(tk.StringVar())
        self.indBitStatLbl[bit].set("0")
        tmpLbl = tk.Label(solCardBitFrm, textvariable=self.indBitStatLbl[bit], relief=tk.SUNKEN)
        tmpLbl.grid(column = 1, row = 3)

        #Button for pulsing solenoid
        tmpBtn = tk.Button(solCardBitFrm, text="PulseSol", command=lambda tmp=bit: self.pulsesol(tmp))
        tmpBtn.grid(column = 0, row = 4, columnspan = 2)
