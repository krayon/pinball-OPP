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
# @file    tkCmdFrm.py
# @author  Hugh Spahr
# @date    4/10/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the tk command frame.  It provides buttons to control the running
# of the rules thread, command thread, and lists the current state.

#===============================================================================

from Tkinter import Button as Btn
from Tkinter import Frame, StringVar, Canvas, SUNKEN, RAISED, CENTER
from ttk import Combobox, Label, Button
from rules.rulesData import RulesData
from gameData import GameData
from comms.commIntf import CommsState

## Tk command frame class.
#  The command frame contains the controls to run or single step the command, and
#  rules threads.  It also lists the current state of the machine for debug purposes.
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
    
    #private members
    _prevState = 0
    _prevCommState = 0

    
    ## The constructor.
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
        
        #Add rules state status
        tmpLbl = Label(self.cmdFrm, text="Rules State:")
        tmpLbl.grid(column = 2, row = 1)
        TkCmdFrm.rulesStateVar = StringVar()
        TkCmdFrm.rulesStateVar.set("No State")
        tmpLbl = Label(self.cmdFrm, textvariable=TkCmdFrm.rulesStateVar, relief=SUNKEN, width=20, anchor=CENTER)
        tmpLbl.grid(column = 3, row = 1, padx=8, pady=8)
        
        #Add comms state status
        tmpLbl = Label(self.cmdFrm, text="Comms State:")
        tmpLbl.grid(column = 2, row = 2)
        TkCmdFrm.commsStateVar = StringVar()
        TkCmdFrm.commsStateVar.set("No State")
        tmpLbl = Label(self.cmdFrm, textvariable=TkCmdFrm.commsStateVar, relief=SUNKEN, width=20, anchor=CENTER)
        tmpLbl.grid(column = 3, row = 2, padx=8, pady=8)
        
    ## Toggle function
    #
    #  Called when the button is pressed.  The button is either a toggle button
    #  or a push button depending on the combobox.
    #
    #  @param  self          [in]   Object reference
    #  @param  whichThread   [in]   Either RULES_THREAD_IDX or COMMS_THREAD_IDX
    #  @return None
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

            
    ## Combobox callback function
    #
    #  Called when the combobox is changed.  Set to either single step or run.
    #  If single step, the button is a pushbutton.  If run, the button is a
    #  toggle button.
    #
    #  @param  self          [in]   Object reference
    #  @param  whichThread   [in]   Either RULES_THREAD_IDX or COMMS_THREAD_IDX
    #  @return None
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

    ## Update command frame state string
    #
    #  Updates the state string which lists the current state of the machine.
    #  State string is grabbed from [STATE_STR](@ref rules.rulesData.RulesData.STATE_STR). 
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Update_Cmd_Frm(self):
        if TkCmdFrm._prevState != GameData.gameMode:
            TkCmdFrm.rulesStateVar.set(RulesData.STATE_STR[GameData.gameMode])
            TkCmdFrm._prevState = GameData.gameMode
        if TkCmdFrm._prevCommState != GameData.commState: 
            TkCmdFrm.commsStateVar.set(CommsState.STATE_STR[GameData.commState])
            TkCmdFrm._prevCommState = GameData.commState
