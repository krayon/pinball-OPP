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
# @file:   tkCmdFrm.py
# @author: Hugh Spahr
# @date:   4/10/2014
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
# This is the tk command frame.  It provides buttons to control the running
# of the rules thread, command thread, and list the current state.
#
#===============================================================================

vers = '00.00.01'

from Tkinter import Button as Btn
from Tkinter import *
from ttk import *
from rulesData import RulesData
from gameData import GameData

class tkCmdFrm():
    #indices for stuff
    RULES_THREAD_IDX = 0
    COMMS_THREAD_IDX = 1
    
    threadRun = [] 
    threadSendStep = []
    toggleState = []
    comboVar = []
    toggleBtn = []
    stateVar = 0
    btnCfgBitfield = 0x3                #Both button start as toggle buttons
    
    def __init__(self, parentFrm):
        #Create main frame
        self.cmdFrm = Frame(parentFrm, borderwidth = 5, relief=RAISED)
        self.cmdFrm.grid(column = 0, row = 0)
        
        #Add rules thread controls
        tmpLbl = Label(self.cmdFrm, text="Rules Thread")
        tmpLbl.grid(column = 0, row = 0)
        self.comboVar.append(StringVar())
        self.comboVar[tkCmdFrm.RULES_THREAD_IDX].set("Run")
        self.threadRun.append(True)
        self.toggleState.append(False)
        tmpCB = Combobox(self.cmdFrm, textvariable=self.comboVar[tkCmdFrm.RULES_THREAD_IDX], width=11, state="readonly")
        tmpCB["values"] = ("Run", "Single Step")
        tmpCB.grid(column = 0, row = 1, padx=8, pady=8)
        self.comboVar[tkCmdFrm.RULES_THREAD_IDX].trace("w", lambda name, index, op, tmp=tkCmdFrm.RULES_THREAD_IDX: self.comboboxcallback(tmp))
        tmpBtn = Btn(self.cmdFrm, text="Run", command=lambda tmp=tkCmdFrm.RULES_THREAD_IDX: self.toggle(tmp))
        tmpBtn.grid(column = 0, row = 2, padx=8, pady=8)
        self.toggleBtn.append(tmpBtn)
        
        #Add comms thread controls
        tmpLbl = Label(self.cmdFrm, text="Comms Thread")
        tmpLbl.grid(column = 1, row = 0)
        self.comboVar.append(StringVar())
        self.comboVar[tkCmdFrm.COMMS_THREAD_IDX].set("Run")
        self.threadRun.append(True)
        self.toggleState.append(False)
        tmpCB = Combobox(self.cmdFrm, textvariable=self.comboVar[tkCmdFrm.COMMS_THREAD_IDX], width=11, state="readonly")
        tmpCB["values"] = ("Run", "Single Step")
        tmpCB.grid(column = 1, row = 1, padx=8, pady=8)
        self.comboVar[tkCmdFrm.COMMS_THREAD_IDX].trace("w", lambda name, index, op, tmp=tkCmdFrm.COMMS_THREAD_IDX: self.comboboxcallback(tmp))
        tmpBtn = Btn(self.cmdFrm, text="Run", command=lambda tmp=tkCmdFrm.COMMS_THREAD_IDX: self.toggle(tmp))
        tmpBtn.grid(column = 1, row = 2, padx=8, pady=8)
        self.toggleBtn.append(tmpBtn)
        
        #Add state status
        tmpLbl = Label(self.cmdFrm, text="State")
        tmpLbl.grid(column = 2, row = 0)
        self.stateVar = StringVar()
        self.stateVar.set("No State")
        tmpLbl = Label(self.cmdFrm, textvariable=self.stateVar, relief=SUNKEN, width=20, anchor=CENTER)
        tmpLbl.grid(column = 2, row = 1, padx=8, pady=8)
        
    def toggle(self, whichThread):
        #If this is configured as a toggle button
        if (self.btnCfgBitfield & (1 << whichThread) != 0):
            self.toggleState[whichThread] = not self.toggleState[whichThread]
            if self.toggleState[whichThread]:
                self.toggleBtn[whichThread].config(relief=SUNKEN)
            else:
                self.toggleBtn[whichThread].config(relief=RAISED)
            
    def comboboxcallback(self, whichThread):
        if self.comboVar[whichThread].get() == "Single Step":
            #Create a new button that is pulse
            tmpCnvs = Canvas(self.cmdFrm, width=100, height=40)
            tmpCnvs.grid(column = whichThread, row = 2)
            tmpBtn = Button(self.cmdFrm, text="Single Step", command=lambda tmp=whichThread: self.toggle(tmp))
            tmpBtn.grid(column = whichThread, row = 2, padx=4, pady=12)
            self.toggleBtn[whichThread] = tmpBtn

            #Set the state variables            
            self.toggleState[whichThread] = False
            self.btnCfgBitfield &= ~(1 << whichThread)
        else:
            #Create a new button that is toggle
            tmpCnvs = Canvas(self.cmdFrm, width=100, height=40)
            tmpCnvs.grid(column = whichThread, row = 2)
            tmpBtn = Btn(self.cmdFrm, text="Run", command=lambda tmp=whichThread: self.toggle(tmp))
            tmpBtn.grid(column = 0, row = 2, padx=8, pady=8)
            print whichThread
            self.toggleBtn[whichThread] = tmpBtn
            
            #Set the state variables            
            self.btnCfgBitfield |= (1 << whichThread)
            self.toggleState[whichThread] = False

    def Update_Cmd_Frm(self):
        self.stateVar.set(RulesData.STATE_STR[GameData.gameMode])
