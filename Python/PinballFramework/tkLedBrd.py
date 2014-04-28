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
# @file:   tkLedBrd.py
# @author: Hugh Spahr
# @date:   4/11/2014
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
# This is the tk LED board interface.  It displays the current status of the
# LEDs. 
#
#===============================================================================

import rs232Intf
from Tkinter import Button as Btn
from Tkinter import *
from ttk import *
from rules.rulesData import RulesData

class TkLedBrd():
    brdNum = 0
    brdPos = 0
    prevLedState = 0x00                  #1 is on, 0 is off
    bitFrms = []
    canvas = []
    ledCardFrm = 0
    statLbl = 0
    ledOffImage = 0
    ledOnWhtImage = 0
    ledOnGrnImage = 0
    
    def __init__(self, brdNum, frmRow, parentFrm):
        self.brdNum = brdNum
        self.brdPos = frmRow
        self.statLbl = StringVar()
        self.ledOffImage = PhotoImage(file="graphics/ledOff.gif")
        self.ledOnWhtImage = PhotoImage(file="graphics/ledOnWht.gif")
        self.ledOnGrnImage = PhotoImage(file="graphics/ledOnGrn.gif")

        
        #Create main frame
        self.ledCardFrm = Frame(parentFrm, borderwidth = 5, relief=RAISED)
        self.ledCardFrm.grid(column = 0, row = frmRow)
        
        #Create card info frame
        ledCardInfoFrm = Frame(self.ledCardFrm)
        ledCardInfoFrm.grid(column = 8, row = 0)
        
        #Add card info
        tmpLbl = Label(ledCardInfoFrm, text="LED Card %d" % (brdNum + 1))
        tmpLbl.grid(column = 0, row = 0)
        tmpLbl = Label(ledCardInfoFrm, text="Status")
        tmpLbl.grid(column = 0, row = 1)
        tmpLbl = Label(ledCardInfoFrm, textvariable=self.statLbl, relief=SUNKEN)
        self.statLbl.set("0x%02x" % self.prevLedState)
        tmpLbl.grid(column = 0, row = 2)

        for i in range(rs232Intf.NUM_LED_PER_BRD):
            TkLedBrd.createBitFrame(self, i)

    def createBitFrame(self, bit):
        ledCardBitFrm = Frame(self.ledCardFrm, borderwidth = 5, relief=RAISED)
        self.bitFrms.append(ledCardBitFrm)
        ledCardBitFrm.grid(column = rs232Intf.NUM_LED_PER_BRD - bit - 1, row = 0)
        tmpLbl = Label(ledCardBitFrm, text="%s" % RulesData.LED_BRD_BIT_NAMES[self.brdNum][bit])
        tmpLbl.grid(column = 0, row = 0)
        
        #Graphic of LED on
        self.canvas.append(Canvas(ledCardBitFrm, width=100, height=80))
        self.canvas[bit].grid(column = 0, row = 1)
        
        if ((self.prevLedState & (1 << bit)) == 0):
            self.canvas[bit].create_image(48, 40, image=self.ledOffImage)
        else:
            self.canvas[bit].create_image(48, 40, image=self.ledOnGrnImage)

    def updateLeds(self, data):
        if (self.prevLedState != data):
            for index in range(rs232Intf.NUM_LED_PER_BRD):
                if ((self.prevLedState ^ data) & (1 << index)):
                    if (data & (1 << index)) != 0:
                        self.canvas[index].create_image(48, 40, image=self.ledOnGrnImage)
                    else:
                        self.canvas[index].create_image(48, 40, image=self.ledOffImage)
            self.prevLedState = data
            self.statLbl.set("0x%02x" % self.prevLedState)
                        