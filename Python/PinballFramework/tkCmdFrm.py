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

from Tkinter import Button as Btn
from Tkinter import *
from ttk import *
from rules.rulesData import RulesData
from gameData import GameData

class TkCmdFrm():
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
        TkCmdFrm.comboVar.append(StringVar())
        TkCmdFrm.comboVar[TkCmdFrm.RULES_THREAD_IDX].set("Run")
        TkCmdFrm.threadRun.append(True)
        TkCmdFrm.toggleState.append(False)
        TkCmdFrm.threadSendStep.append(False)
        tmpCB = Combobox(self.cmdFrm, textvariable=TkCmdFrm.comboVar[TkCmdFrm.RULES_THREAD_IDX], width=11, state="readonly")
        tmpCB["values"] = ("Run", "Single Step")
        tmpCB.grid(column = 0, row = 1, padx=8, pady=8)
        TkCmdFrm.comboVar[TkCmdFrm.RULES_THREAD_IDX].trace("w", lambda name, index, op, tmp=TkCmdFrm.RULES_THREAD_IDX: self.comboboxcallback(tmp))
        tmpBtn = Btn(self.cmdFrm, text="Run", command=lambda tmp=TkCmdFrm.RULES_THREAD_IDX: self.toggle(tmp))
        tmpBtn.grid(column = 0, row = 2, padx=8, pady=8)
        TkCmdFrm.toggleBtn.append(tmpBtn)
        
        #Add comms thread controls
        tmpLbl = Label(self.cmdFrm, text="Comms Thread")
        tmpLbl.grid(column = 1, row = 0)
        TkCmdFrm.comboVar.append(StringVar())
        TkCmdFrm.comboVar[TkCmdFrm.COMMS_THREAD_IDX].set("Run")
        TkCmdFrm.threadRun.append(True)
        TkCmdFrm.toggleState.append(False)
        TkCmdFrm.threadSendStep.append(False)
        tmpCB = Combobox(self.cmdFrm, textvariable=TkCmdFrm.comboVar[TkCmdFrm.COMMS_THREAD_IDX], width=11, state="readonly")
        tmpCB["values"] = ("Run", "Single Step")
        tmpCB.grid(column = 1, row = 1, padx=8, pady=8)
        TkCmdFrm.comboVar[TkCmdFrm.COMMS_THREAD_IDX].trace("w", lambda name, index, op, tmp=TkCmdFrm.COMMS_THREAD_IDX: self.comboboxcallback(tmp))
        tmpBtn = Btn(self.cmdFrm, text="Run", command=lambda tmp=TkCmdFrm.COMMS_THREAD_IDX: self.toggle(tmp))
        tmpBtn.grid(column = 1, row = 2, padx=8, pady=8)
        TkCmdFrm.toggleBtn.append(tmpBtn)
        
        #Add state status
        tmpLbl = Label(self.cmdFrm, text="State")
        tmpLbl.grid(column = 2, row = 0)
        TkCmdFrm.stateVar = StringVar()
        TkCmdFrm.stateVar.set("No State")
        tmpLbl = Label(self.cmdFrm, textvariable=TkCmdFrm.stateVar, relief=SUNKEN, width=20, anchor=CENTER)
        tmpLbl.grid(column = 2, row = 1, padx=8, pady=8)
        
    def toggle(self, whichThread):
        #If this is configured as a toggle button
        if (TkCmdFrm.btnCfgBitfield & (1 << whichThread) != 0):
            TkCmdFrm.toggleState[whichThread] = not TkCmdFrm.toggleState[whichThread]
            if TkCmdFrm.toggleState[whichThread]:
                TkCmdFrm.toggleBtn[whichThread].config(relief=SUNKEN)
            else:
                TkCmdFrm.toggleBtn[whichThread].config(relief=RAISED)
        else:
            TkCmdFrm.threadSendStep[whichThread] = True

            
    def comboboxcallback(self, whichThread):
        if TkCmdFrm.comboVar[whichThread].get() == "Single Step":
            #Create a new button that is pulse
            tmpCnvs = Canvas(self.cmdFrm, width=100, height=40)
            tmpCnvs.grid(column = whichThread, row = 2)
            tmpBtn = Button(self.cmdFrm, text="Single Step", command=lambda tmp=whichThread: self.toggle(tmp))
            tmpBtn.grid(column = whichThread, row = 2, padx=4, pady=12)
            TkCmdFrm.toggleBtn[whichThread] = tmpBtn

            #Set the state variables            
            TkCmdFrm.toggleState[whichThread] = False
            TkCmdFrm.threadSendStep[whichThread] = False
            TkCmdFrm.threadRun[whichThread] = False
            TkCmdFrm.btnCfgBitfield &= ~(1 << whichThread)
        else:
            #Create a new button that is toggle
            tmpCnvs = Canvas(self.cmdFrm, width=100, height=40)
            tmpCnvs.grid(column = whichThread, row = 2)
            tmpBtn = Btn(self.cmdFrm, text="Run", command=lambda tmp=whichThread: self.toggle(tmp))
            tmpBtn.grid(column = whichThread, row = 2, padx=8, pady=8)
            TkCmdFrm.toggleBtn[whichThread] = tmpBtn
            
            #Set the state variables            
            TkCmdFrm.toggleState[whichThread] = False
            TkCmdFrm.threadSendStep[whichThread] = False
            TkCmdFrm.threadRun[whichThread] = True
            TkCmdFrm.btnCfgBitfield |= (1 << whichThread)

    def Update_Cmd_Frm(self):
        TkCmdFrm.stateVar.set(RulesData.STATE_STR[GameData.gameMode])
