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
# @file    tkLedBrd.py
# @author  Hugh Spahr
# @date    4/11/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the tk LED board interface.  It displays the current status of the
# LEDs.

#===============================================================================

import rs232Intf
from Tkinter import Frame, StringVar, Canvas, SUNKEN, RAISED, PhotoImage
from ttk import Label
from gameData import GameData

## Tk LED board class.
#  The LED board frame contains pictures of if each LED is on or off.
#  It lists the bit string name to make debugging easier.
class TkLedBrd():
    #Private data
    _ledOffImage = 0
    _ledOnWhtImage = 0
    _ledOnGrnImage = 0
    
    ## The constructor
    #
    #  Creates the TK frame interface for the input board.  Creates a frame
    #  for each of the input bits, and an overall frame for card information.
    #
    #  @param  self          [in]   Object reference
    #  @param  brdNum        [in]   Input board instance index (base 0)
    #  @param  wing          [in]   Wing number (base 0)
    #  @param  parentFrm     [in]   Parent frame
    #  @param  wingRow       [in]   Row on parent frame
    #  @return None
    def __init__(self, brdNum, wing, parentFrm, wingRow):
        self.brdNum = brdNum
        self.wing = wing
        self.statLbl = StringVar()
        self.brdAddr = brdNum + ord(rs232Intf.CARD_ID_GEN2_CARD)
        self.prevLedState = 0x00                  #1 is on, 0 is off
        self.bitFrms = []
        self.canvas = []
        
        if (TkLedBrd._ledOffImage == 0):
            TkLedBrd._ledOffImage = PhotoImage(file="graphics/ledOff.gif")
        if (TkLedBrd._ledOnWhtImage == 0):
            TkLedBrd._ledOnWhtImage = PhotoImage(file="graphics/ledOnWht.gif")
        if (TkLedBrd._ledOnGrnImage == 0):
            TkLedBrd._ledOnGrnImage = PhotoImage(file="graphics/ledOnGrn.gif")
        
        #Create main frame
        self.ledCardFrm = Frame(parentFrm, borderwidth = 5, relief=RAISED)
        self.ledCardFrm.grid(column = 0, row = wingRow)
        
        #Create card info frame
        ledCardInfoFrm = Frame(self.ledCardFrm)
        ledCardInfoFrm.grid(column = 8, row = 0)
        
        #Add card info
        tmpLbl = Label(ledCardInfoFrm, text="LED Card %d" % (brdNum))
        tmpLbl.grid(column = 0, row = 0)
        tmpLbl = Label(ledCardInfoFrm, text="Wing Num %d" % wing)
        tmpLbl.grid(column = 0, row = 1)
        tmpLbl = Label(ledCardInfoFrm, text="Addr = 0x%02x" % self.brdAddr)
        tmpLbl.grid(column = 0, row = 2)
        tmpLbl = Label(ledCardInfoFrm, text="Status")
        tmpLbl.grid(column = 0, row = 3)
        tmpLbl = Label(ledCardInfoFrm, textvariable=self.statLbl, relief=SUNKEN)
        self.statLbl.set("0x%02x" % self.prevLedState)
        tmpLbl.grid(column = 0, row = 4)

        for i in xrange(rs232Intf.NUM_INCAND_PER_WING):
            TkLedBrd.createBitFrame(self, i)

    ## Create Bit Frame function
    #
    #  Called for each bit on an LED card.
    #
    #  @param  self          [in]   Object reference
    #  @param  bit           [in]   Input bit number
    #  @return None
    def createBitFrame(self, bit):
        ledCardBitFrm = Frame(self.ledCardFrm, borderwidth = 5, relief=RAISED)
        self.bitFrms.append(ledCardBitFrm)
        ledCardBitFrm.grid(column = rs232Intf.NUM_INCAND_PER_WING - bit - 1, row = 0)
        tmpLbl = Label(ledCardBitFrm, text="%s" % GameData.LedBitNames.LED_BRD_BIT_NAMES[self.brdNum][bit + (self.wing * rs232Intf.NUM_INCAND_PER_WING)])
        tmpLbl.grid(column = 0, row = 0)
        
        #Graphic of LED on
        self.canvas.append(Canvas(ledCardBitFrm, width=100, height=80))
        self.canvas[bit].grid(column = 0, row = 1)
        
        if ((self.prevLedState & (1 << bit)) == 0):
            self.canvas[bit].create_image(48, 40, image=TkLedBrd._ledOffImage)
        else:
            self.canvas[bit].create_image(48, 40, image=TkLedBrd._ledOnGrnImage)

    ## Update LED states
    #
    #  If the LED state has changed, the graphics are updated.
    #
    #  @param  self          [in]   Object reference
    #  @param  data          [in]   New LED state
    #  @return None
    def updateLeds(self, data):
        if (self.prevLedState != data):
            for index in xrange(rs232Intf.NUM_INCAND_PER_WING):
                if ((self.prevLedState ^ data) & (1 << index)):
                    if (data & (1 << index)) != 0:
                        self.canvas[index].create_image(48, 40, image=TkLedBrd._ledOnGrnImage)
                    else:
                        self.canvas[index].create_image(48, 40, image=TkLedBrd._ledOffImage)
            self.prevLedState = data
            self.statLbl.set("0x%02x" % self.prevLedState)

    ## Remove images
    #
    #  Remove images so threads can be cleaned
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def removeImages(self):
        for index in xrange(rs232Intf.NUM_INCAND_PER_WING):
            self.canvas[index].create_image(48, 40, image="")
                        
