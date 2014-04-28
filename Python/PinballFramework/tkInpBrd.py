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
# @file:   tkInpBrd.py
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
# This is the tk input board interface.  It allows inputs to be simulated,
# and the displays the current status.
#
#===============================================================================

import rs232Intf
from Tkinter import Button as Btn
from Tkinter import *
from ttk import *
from rules.rulesData import RulesData

class TkInpBrd():
    BITS_IN_ROW = 8
    
    brdAddr = 0
    brdNum = 0
    brdPos = 0
    dispInpValue = 0
    statLbl = 0
    indBitStatLbl = []
    indBitOptMenu = []
    toggleBtn = []
    toggleState = []
    inpCardFrm = 0
    bitFrms = []
    btnCfgBitfield = 0              #Set bits to 1 to default to toggle buttons
    simSwitchBits = 0
    
    def __init__(self, brdNum, brdPos, addr, parentFrm):
        self.brdNum = brdNum
        self.brdPos = brdPos
        self.brdAddr = addr
        self.statLbl = StringVar()
        
        #Create main frame
        self.inpCardFrm = Frame(parentFrm, borderwidth = 5, relief=RAISED)
        self.inpCardFrm.grid(column = 0, row = brdPos + 1)
        
        #Create card info frame
        inpCardInfoFrm = Frame(self.inpCardFrm)
        inpCardInfoFrm.grid(column = TkInpBrd.BITS_IN_ROW, row = 0, columnspan = 2)
        
        #Add card info
        tmpLbl = Label(inpCardInfoFrm, text="Inp Card %d" % (brdNum + 1))
        tmpLbl.grid(column = 0, row = 0)
        tmpLbl = Label(inpCardInfoFrm, text="Addr = 0x%02x" % addr)
        tmpLbl.grid(column = 0, row = 1)
        tmpLbl = Label(inpCardInfoFrm, text="Status")
        tmpLbl.grid(column = 0, row = 2)
        tmpLbl = Label(inpCardInfoFrm, textvariable=self.statLbl, relief=SUNKEN)
        self.statLbl.set("0x%04x" % self.dispInpValue)
        tmpLbl.grid(column = 0, row = 3)

        #Configure btnCfgBitfield to initial value set by card cfg
        for i in range(rs232Intf.NUM_INP_PER_BRD):
            TkInpBrd.createBitFrame(self, i)

    def toggle(self, bit):
        #If this is configured as a toggle button
        if (self.btnCfgBitfield & (1 << bit) != 0):
            self.toggleState[bit] = not self.toggleState[bit]
            if self.toggleState[bit]:
                self.toggleBtn[bit].config(relief=SUNKEN)
                self.simSwitchBits |= (1 << bit)
            else:
                self.toggleBtn[bit].config(relief=RAISED)
                self.simSwitchBits &= ~(1 << bit)
        #Else this is a pulsed button, set the bit and it will be auto cleared
        else:
            self.simSwitchBits |= (1 << bit)
        print "Bits = 0x%04x" % self.simSwitchBits
            
    def optmenucallback(self, bit):
        if self.indBitOptMenu[bit].get() == "Pulse":
            #Create a new button that is pulse
            tmpCnvs = Canvas(self.bitFrms[bit], width=100, height=40)
            tmpCnvs.grid(column = 0, row = 2, columnspan = 2)
            tmpBtn = Button(self.bitFrms[bit], text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, columnspan = 2, padx=4, pady=12)
            self.toggleBtn[bit] = tmpBtn

            #Set the state variables            
            self.toggleState[bit] = False
            self.btnCfgBitfield &= ~(1 << bit)
            self.simSwitchBits &= ~(1 << bit)
        else:
            #Create a new button that is toggle
            tmpCnvs = Canvas(self.bitFrms[bit], width=100, height=40)
            tmpCnvs.grid(column = 0, row = 2, columnspan = 2)
            tmpBtn = Btn(self.bitFrms[bit], text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, columnspan = 2, padx=8, pady=8)
            self.toggleBtn[bit] = tmpBtn
            
            #Set the state variables            
            self.btnCfgBitfield |= (1 << bit)
            if self.toggleState[bit]:
                self.simSwitchBits |= (1 << bit)
            else:
                self.simSwitchBits &= ~(1 << bit)
            
    def createBitFrame(self, bit):
        inpCardBitFrm = Frame(self.inpCardFrm, borderwidth = 5, relief=RAISED)
        self.bitFrms.append(inpCardBitFrm)
        if (bit < TkInpBrd.BITS_IN_ROW):
            inpCardBitFrm.grid(column = TkInpBrd.BITS_IN_ROW - bit - 1, row = 0)
        else:
            inpCardBitFrm.grid(column = rs232Intf.NUM_INP_PER_BRD - bit - 1, row = 1)
        tmpLbl = Label(inpCardBitFrm, text="%s" % RulesData.INP_BRD_BIT_NAMES[self.brdNum][bit])
        tmpLbl.grid(column = 0, row = 0, columnspan = 2)
        
        #Read config and set btnCfg
        if (RulesData.INP_BRD_CFG[self.brdNum][bit] == rs232Intf.CFG_INP_STATE):
            self.btnCfgBitfield |= (1 << bit)
        
        #Combobox menu for button presses
        self.indBitOptMenu.append(StringVar())
        if (self.btnCfgBitfield & (1 << bit)):
            self.indBitOptMenu[bit].set("Toggle")
        else:
            self.indBitOptMenu[bit].set("Pulse")
        tmpCB = Combobox(inpCardBitFrm, textvariable=self.indBitOptMenu[bit], width=6, state="readonly")
        tmpCB["values"] = ("Pulse", "Toggle")
        tmpCB.grid(column = 0, row = 1, columnspan = 2)
        self.indBitOptMenu[bit].trace("w", lambda name, index, op, tmp=bit: self.optmenucallback(tmp))
        
        #Button code
        if (self.btnCfgBitfield & (1 << bit)):
            #Toggle button so use the old style so button can stay pressed
            tmpBtn = Btn(inpCardBitFrm, text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, columnspan = 2, padx=8, pady=8)
        else:
            #Pulse button so use the new style
            tmpBtn = Button(inpCardBitFrm, text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, columnspan = 2, padx=4, pady=12)
        self.toggleBtn.append(tmpBtn)
        self.toggleState.append(False)
        tmpLbl = Label(inpCardBitFrm, text="Value")
        tmpLbl.grid(column = 0, row = 3)
        self.indBitStatLbl.append(StringVar())
        self.indBitStatLbl[bit].set("0")
        tmpLbl = Label(inpCardBitFrm, textvariable=self.indBitStatLbl[bit], relief=SUNKEN)
        tmpLbl.grid(column = 1, row = 3)

    def get_status(self):
        #Clear all the edge triggered bits
        data = self.simSwitchBits
        self.simSwitchBits &= self.btnCfgBitfield
        return data
