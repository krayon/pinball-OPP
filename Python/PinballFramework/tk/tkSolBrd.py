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
# @file    tkSolBrd.py
# @author  Hugh Spahr
# @date    4/1/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the tk solenoid board interface.  It allows switch inputs to be
# simulated, and the displays the current status.  It also allows solenoids
# to be test fired. 

#===============================================================================

import rs232Intf
from Tkinter import Button as Btn
from Tkinter import Frame, StringVar, Canvas, SUNKEN, RAISED
from ttk import Combobox, Label, Button
from gameData import GameData

## Tk solenoid board class.
#  The solenoid board frame contains the controls observe the current state of the
#  solenoid input bits, or simulate switch inputs.  It lists the bit string name to make
#  debugging easier.  If a bit is configured as a state input, the simulate
#  button is a toggle button.  If the bit is configured as an edge triggered
#  input, the button is a pushbutton.  It allows solenoids to be test fired.
class TkSolBrd():
    
    ## The constructor
    #
    #  Creates the TK frame interface for the solenoid board.  Creates a frame
    #  for each of the solenoid bits, and an overall frame for card information.
    #
    #  @param  self          [in]   Object reference
    #  @param  brdNum        [in]   Solenoid board instance index (base 0)
    #  @param  brdPos        [in]   Board position in comms chain (base 0)
    #  @param  addr          [in]   Board address
    #  @param  parentFrm     [in]   Parent frame
    #  @return None
    def __init__(self, brdNum, brdPos, addr, parentFrm):
        self.brdNum = brdNum
        self.brdPos = brdPos
        self.brdAddr = addr
        self.statLbl = StringVar()
        self.dispInpValue = 0
        self.indBitStatLbl = []
        self.indBitOptMenu = []
        self.toggleBtn = []
        self.toggleState = []
        self.bitFrms = []
        self.btnCfgBitfield = 0              #Set bits to 1 to default to toggle buttons
        self.simSwitchBits = 0
        self.pulseSolBits = 0
        
        #Create main frame
        self.solCardFrm = Frame(parentFrm, borderwidth = 5, relief=RAISED)
        self.solCardFrm.grid(column = 0, row = brdPos + 1)
        
        #Create card info frame
        solCardInfoFrm = Frame(self.solCardFrm)
        solCardInfoFrm.grid(column = 8, row = 0)
        
        #Add card info
        tmpLbl = Label(solCardInfoFrm, text="Sol Card %d" % (brdNum + 1))
        tmpLbl.grid(column = 0, row = 0)
        tmpLbl = Label(solCardInfoFrm, text="Addr = 0x%02x" % addr)
        tmpLbl.grid(column = 0, row = 1)
        tmpLbl = Label(solCardInfoFrm, text="Status")
        tmpLbl.grid(column = 0, row = 2)
        tmpLbl = Label(solCardInfoFrm, textvariable=self.statLbl, relief=SUNKEN)
        self.statLbl.set("0x%02x" % self.dispInpValue)
        tmpLbl.grid(column = 0, row = 3)

        for i in xrange(rs232Intf.NUM_SOL_PER_BRD):
            TkSolBrd.createBitFrame(self, i)

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
        print "Bits = 0x%04x" % self.simSwitchBits

    ## Pulse a solenoid bit
    #
    #  Post a bit to send a command to kick the solenoid
    #
    #  @param  self          [in]   Object reference
    #  @param  bit           [in]   Solenoid bit number
    #  @return None
    def pulsesol(self, bit):
        self.pulseSolBits |= (1 << bit)
            
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
    #  Called for each bit on a solenoid card.
    #  Uses [SOL_BRD_BIT_NAMES](@ref rules.rulesData.RulesData.SOL_BRD_BIT_NAMES) for names of bits.
    #  Uses [SOL_BRD_CFG](@ref rules.rulesData.RulesData.SOL_BRD_CFG) for initial cfg of bits.
    #
    #  @param  self          [in]   Object reference
    #  @param  bit           [in]   Input bit number
    #  @return None
    def createBitFrame(self, bit):
        solCardBitFrm = Frame(self.solCardFrm, borderwidth = 5, relief=RAISED)
        self.bitFrms.append(solCardBitFrm)
        solCardBitFrm.grid(column = rs232Intf.NUM_SOL_PER_BRD - bit - 1, row = 0)
        tmpLbl = Label(solCardBitFrm, text="%s" % GameData.SolBitNames.SOL_BRD_BIT_NAMES[self.brdNum][bit])
        tmpLbl.grid(column = 0, row = 0, columnspan = 2)
        
        #Read config and set btnCfg
        cmdOffset = rs232Intf.CFG_BYTES_PER_SOL * bit
        holdOffset = cmdOffset + rs232Intf.DUTY_CYCLE_OFFSET
        if (GameData.SolBitNames.SOL_BRD_CFG[self.brdNum][cmdOffset] == rs232Intf.CFG_SOL_AUTO_CLR) or \
               (ord(GameData.SolBitNames.SOL_BRD_CFG[self.brdNum][holdOffset]) != 0):
            self.btnCfgBitfield |= (1 << bit)
        
        #Combobox menu for button presses
        self.indBitOptMenu.append(StringVar())
        if (self.btnCfgBitfield & (1 << bit)):
            self.indBitOptMenu[bit].set("Toggle")
        else:
            self.indBitOptMenu[bit].set("Pulse")
        tmpCB = Combobox(solCardBitFrm, textvariable=self.indBitOptMenu[bit], width=6, state="readonly")
        tmpCB["values"] = ("Pulse", "Toggle")
        tmpCB.grid(column = 0, row = 1, columnspan = 2)
        self.indBitOptMenu[bit].trace("w", lambda name, index, op, tmp=bit: self.comboboxcallback(tmp))
        
        #Button code
        if (self.btnCfgBitfield & (1 << bit)):
            #Toggle button so use the old style so button can stay pressed
            tmpBtn = Btn(solCardBitFrm, text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, columnspan = 2, padx=8, pady=8)
        else:
            #Pulse button so use the new style
            tmpBtn = Button(solCardBitFrm, text="SimSwitch", command=lambda tmp=bit: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, columnspan = 2, padx=4, pady=12)
        self.toggleBtn.append(tmpBtn)
        self.toggleState.append(False)
        
        tmpLbl = Label(solCardBitFrm, text="Value")
        tmpLbl.grid(column = 0, row = 3)
        self.indBitStatLbl.append(StringVar())
        self.indBitStatLbl[bit].set("0")
        tmpLbl = Label(solCardBitFrm, textvariable=self.indBitStatLbl[bit], relief=SUNKEN)
        tmpLbl.grid(column = 1, row = 3)

        #Button for pulsing solenoid
        tmpBtn = Button(solCardBitFrm, text="PulseSol", command=lambda tmp=bit: self.pulsesol(tmp))
        tmpBtn.grid(column = 0, row = 4, columnspan = 2, padx=4, pady=12)

    ## Get Tk solenoid frame bit status
    #
    #  Read the solenoid frame bit status, and clear all the edge triggered inputs so they are
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
