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
# @file    tkInpBrd.py
# @author  Hugh Spahr
# @date    4/10/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the tk input board interface.  It allows inputs to be simulated,
# and the displays the current status.

#===============================================================================

import rs232Intf
from Tkinter import Button as Btn
from Tkinter import Frame, StringVar, Canvas, SUNKEN, RAISED
from ttk import Combobox, Label, Button
from gameData import GameData

## Tk input board class.
#  The input board frame contains the controls observe the current state of the
#  input bits, or simulate switch inputs.  It lists the bit string name to make
#  debugging easier.  If a bit is configured as a state input, the simulate
#  button is a toggle button.  If the bit is configured as an edge triggered
#  input, the button is a pushbutton.
class TkInpBrd():
    BITS_IN_ROW = 8
    
    ## The constructor
    #
    #  Creates the TK frame interface for the input board.  Creates a frame
    #  for each of the input bits, and an overall frame for card information.
    #
    #  @param  self          [in]   Object reference
    #  @param  brdNum        [in]   Input board instance index (base 0)
    #  @param  wing          [in]   Wing number (base 0)
    #  @param  parentFrm     [in]   Parent frame
    #  @return None
    def __init__(self, brdNum, wing, parentFrm):
        self.brdNum = brdNum
        self.wing = wing
        self.brdAddr = brdNum + ord(rs232Intf.CARD_ID_GEN2_CARD)
        self.statLbl = StringVar()
        self.dispInpValue = 0
        self.indBitStatLbl = []
        self.indBitOptMenu = []
        self.toggleBtn = []
        self.toggleState = []
        self.bitFrms = []
        self.btnCfgBitfield = 0              #Set bits to 1 to default to toggle buttons
        self.simSwitchBits = 0
        
        #Create main frame
        self.inpCardFrm = Frame(parentFrm, borderwidth = 5, relief=RAISED)
        self.inpCardFrm.grid(column = 0, row = (brdNum * rs232Intf.NUM_G2_WING_PER_BRD) + wing + 1)
        
        #Create card info frame
        inpCardInfoFrm = Frame(self.inpCardFrm)
        inpCardInfoFrm.grid(column = TkInpBrd.BITS_IN_ROW, row = 0, columnspan = 2)
        
        #Add card info
        tmpLbl = Label(inpCardInfoFrm, text="Inp Card %d" % brdNum)
        tmpLbl.grid(column = 0, row = 0)
        tmpLbl = Label(inpCardInfoFrm, text="Wing Num %d" % wing)
        tmpLbl.grid(column = 0, row = 1)
        tmpLbl = Label(inpCardInfoFrm, text="Addr = 0x%02x" % self.brdAddr)
        tmpLbl.grid(column = 0, row = 2)
        tmpLbl = Label(inpCardInfoFrm, text="Status")
        tmpLbl.grid(column = 0, row = 3)
        tmpLbl = Label(inpCardInfoFrm, textvariable=self.statLbl, relief=SUNKEN)
        self.statLbl.set("0x%02x" % self.dispInpValue)
        tmpLbl.grid(column = 0, row = 4)

        #Configure btnCfgBitfield to initial value set by card cfg
        for i in xrange(rs232Intf.NUM_INP_PER_WING):
            TkInpBrd.createBitFrame(self, i)

    ## Toggle function
    #
    #  Called when the button is pressed.  The button is either a toggle button
    #  or a push button depending on the combobox.
    #
    #  @param  self          [in]   Object reference
    #  @param  bit           [in]   Input bit number
    #  @return None
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
        print "Card = %d, Wing = %d, Bits = 0x%02x" % (self.brdNum, self.wing, self.simSwitchBits)
            
    ## Combobox callback function
    #
    #  Called when the combobox is changed.  Set to either pulse or switch.
    #  If pulse, the button is a pushbutton.  If switch, the button is a
    #  toggle button.
    #
    #  @param  self          [in]   Object reference
    #  @param  bit           [in]   Input bit number
    #  @return None
    def comboboxcallback(self, bit):
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
            
    ## Create Bit Frame function
    #
    #  Called for each input bit on an input card.
    #  Uses [INP_BRD_BIT_NAMES](@ref rules.rulesData.RulesData.INP_BRD_BIT_NAMES) for names of bits.
    #  Uses [INP_BRD_CFG](@ref rules.rulesData.RulesData.INP_BRD_CFG) for initial cfg of bits.
    #
    #  @param  self          [in]   Object reference
    #  @param  bit           [in]   Input bit number
    #  @return None
    def createBitFrame(self, bit):
        inpCardBitFrm = Frame(self.inpCardFrm, borderwidth = 5, relief=RAISED)
        self.bitFrms.append(inpCardBitFrm)
        inpCardBitFrm.grid(column = TkInpBrd.BITS_IN_ROW - bit - 1, row = 0)
        tmpLbl = Label(inpCardBitFrm, text="%s" % GameData.InpBitNames.INP_BRD_BIT_NAMES[self.brdNum][bit + (self.wing * rs232Intf.NUM_INP_PER_WING)])
        tmpLbl.grid(column = 0, row = 0, columnspan = 2)
        
        #Read config and set btnCfg
        if (GameData.InpBitNames.INP_BRD_CFG[self.brdNum][bit + (self.wing * rs232Intf.NUM_INP_PER_WING)] == rs232Intf.CFG_INP_STATE):
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
        self.indBitOptMenu[bit].trace("w", lambda name, index, op, tmp=bit: self.comboboxcallback(tmp))
        
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

    ## Get Tk input frame status
    #
    #  Read the input frame status, and clear all the edge triggered inputs so they are
    #  only acted upon once.
    #
    #  @param  self          [in]   Object reference
    #  @return Input debug bit data
    def get_status(self):
        #Clear all the edge triggered bits
        data = self.simSwitchBits
        self.simSwitchBits &= self.btnCfgBitfield
        return data

    ## Update status field
    #
    #  If the data has changed, update the status label.
    #
    #  @param  self          [in]   Object reference
    #  @param  data          [in]   Current state
    #  @return None
    def update_status_field(self, data):
        if (self.dispInpValue != data):
            self.dispInpValue = data
            self.statLbl.set("0x%02x" % self.dispInpValue)
