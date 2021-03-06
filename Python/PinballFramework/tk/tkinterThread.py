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

from Tkinter import Tk, Canvas, Scrollbar, Y, FALSE, TRUE, NW, LEFT, BOTH, RIGHT, VERTICAL
from ttk import Frame

from threading import Thread
from tk.tkCmdFrm import TkCmdFrm
from tk.tkInpBrd import TkInpBrd
from tk.tkSolBrd import TkSolBrd
from tk.tkLedBrd import TkLedBrd
from hwobjs.ledBrd import LedBrd
from hwobjs.solBrd import SolBrd
from hwobjs.inpBrd import InpBrd
import time
import rs232Intf
from gameData import GameData
from globConst import GlobConst

## Tkinter thread class.
#  Create tk frame instances for all the configured hardware.
#  Update the command frame.
class TkinterThread(Thread):
    doneInit = False
    GameData = None
    
    #private members
    _runTkinterThread = True
    
    ## The constructor.
    def __init__(self):
        super(TkinterThread, self).__init__()
        self.blinkOn = True
        
    ## Init the tkinter thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def init(self, gameData):
        TkinterThread.GameData = gameData
    
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
        dummy_count = 0
        root = Tk()
        root.wm_title("Debug Window")
        bgndFrm = VerticalScrolledFrame(root)
        cmdFrm = TkCmdFrm(bgndFrm.interior)
        bgndFrm.pack()
        numInpWing = 0
        numSolWing = 0
        currFrameRow = 1
        for card in xrange(len(TkinterThread.GameData.RulesData.INV_ADDR_LIST)):
            for wing in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
                if (TkinterThread.GameData.RulesData.INV_ADDR_LIST[card][wing] == rs232Intf.WING_INP):
                    # Check if there is no configuration which indicates it is an empty wing board
                    if (len(TkinterThread.GameData.InpBitNames.INP_BRD_CFG[card]) != 0):
                        GameData.tkInpBrd.append(TkInpBrd(card, wing, bgndFrm.interior, currFrameRow))
                        currFrameRow += 1
                        numInpWing += 1
                elif (TkinterThread.GameData.RulesData.INV_ADDR_LIST[card][wing] == rs232Intf.WING_SW_MATRIX_IN):
                    # Check if there are any bit names that aren't unused indicating it is valid
                    if (len(TkinterThread.GameData.InpBitNames.INP_BRD_MTRX_BIT_NAMES[card]) != 0):
                        validCols = 0
                        for index in xrange(rs232Intf.NUM_G2_MATRIX_INP):
                            if (TkinterThread.GameData.InpBitNames.INP_BRD_MTRX_BIT_NAMES[card][index] != "Unused"):
                                validCols |= (1 << ((index & 0x38) >> 3))
                        for col in xrange(rs232Intf.NUM_MATRIX_COL):
                            if (validCols & (1 << col) != 0):
                                GameData.tkInpBrd.append(TkInpBrd(card, rs232Intf.NUM_G2_WING_PER_BRD + col, bgndFrm.interior, currFrameRow))
                                currFrameRow += 1
                                numInpWing += 1
                elif (TkinterThread.GameData.RulesData.INV_ADDR_LIST[card][wing] == rs232Intf.WING_SOL):
                    GameData.tkSolBrd.append(TkSolBrd(card, wing, bgndFrm.interior, currFrameRow))
                    currFrameRow += 1
                    numSolWing += 1
                elif ((TkinterThread.GameData.RulesData.INV_ADDR_LIST[card][wing] == rs232Intf.WING_INCAND) or \
                      (TkinterThread.GameData.RulesData.INV_ADDR_LIST[card][wing] == rs232Intf.WING_HI_SIDE_INCAND)):
                    GameData.tkLedBrd.append(TkLedBrd(card, wing, bgndFrm.interior, currFrameRow))
                    currFrameRow += 1
        root.update()
        TkinterThread.doneInit = True
        
        while TkinterThread._runTkinterThread:
            root.update()
            cmdFrm.Update_Cmd_Frm()
            
            # Copy the current LED state
            self.blinkOn = not self.blinkOn
            ledData = list(LedBrd.currLedData)
            if self.blinkOn:
                ledBlink = list(LedBrd.currBlinkLeds)
                for i in xrange(len(TkinterThread.GameData.RulesData.INV_ADDR_LIST)):
                    ledData[i] |= ledBlink[i]
            for ledInst in xrange(len(LedBrd.dataRemap)):
                card = LedBrd.dataRemap[ledInst] >> 16
                wingShift = (LedBrd.dataRemap[ledInst] & 0xffff) << 3
                data = (ledData[card] >> wingShift) & 0xff
                GameData.tkLedBrd[ledInst].updateLeds(data)
            for i in xrange(numSolWing):
                remapCard = SolBrd.dataRemap[i] >> 16
                remapWing = SolBrd.dataRemap[i] & 0xffff
                GameData.tkSolBrd[i].update_status_field(SolBrd.lastData[remapCard][remapWing] & 0x0f)
            for i in xrange(numInpWing):
                remapCard = InpBrd.dataRemap[i] >> 16
                if (InpBrd.dataRemap[i] & InpBrd.SWITCH_MATRIX_WING) == 0:
                    remapWing = InpBrd.dataRemap[i] & 0xffff
                else: 
                    remapWing = (InpBrd.dataRemap[i] & 0xf) + rs232Intf.NUM_G2_WING_PER_BRD
                GameData.tkInpBrd[i].update_status_field(InpBrd.lastData[remapCard][remapWing] & 0xff)
            dummy_count += 1
            time.sleep(float(GlobConst.TK_SLEEP)/1000.0)

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)           

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        # I don't know why this works.  Seems like it is a maximum height for window
        canvas.config(height = 800)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

