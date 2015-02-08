#!/usr/bin/env python
#
#===============================================================================
## @mainpage
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

#===============================================================================
##
# @file    GenPyCode.py
# @author  Hugh Spahr
# @date    6/19/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Main entry point to Generate Python Code project.  Creates GUI window
# to output generate Python results.

#===============================================================================

from Tkinter import Frame, RAISED, RIGHT, Text, Y, WORD, END, Tk
from ttk import Button, Scrollbar
from parseRules import ParseRules
import time
import sys
import os

## GUI Frame
#
#  Create TK GUI frame.
#
#  @param  argv          [in]   Passed in arguments
#  @return None 
class GuiFrame():
  
    ## The constructor
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Root object reference
    #  @param  rulesFile     [in]   Rules file name
    #  @param  outDir        [in]   Location of output directory
    #  @return None
    def __init__(self, parent, rulesFile, outDir):
        self.exit = False
        self.parent = parent
        self.rulesFile = rulesFile
        self.outDir = outDir
        self.bgndFrm = None
        self.scrollbar = None
        self.log = None
        
        # Create the outdir if it doesn't exist
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        
        self.initUI()
        self.parseRules = ParseRules(self)
        self.parseRules.verifyParameters()            
    
    ## Close button press
    #
    #  Called when the close button is pressed.  
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def closeBtnPress(self):
        self.exit = True
        
    ## Init UI
    #
    #  Initialize the user interface.  Create the cmd panel at the
    #  top which contains the status and column headings.  Walk
    #  through the cardType array and create a panel for each card.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def initUI(self):
        self.parent.wm_title("Generate Python Code GUI")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.bgndFrm = Frame(self.parent)
        self.bgndFrm.grid()
        
        self.cmdPanel()
        self.consolePanel()
        
    ## Create command panel
    #
    #  Create the command panel.  It contains the close button.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def cmdPanel(self):
        tmpFrm = Frame(self.bgndFrm, borderwidth = 5, relief=RAISED)
        tmpFrm.grid()
        tmpFrm.grid(column = 0, row = 0)
        tmpBtn = Button(tmpFrm, width = 12, text="Close", command=self.closeBtnPress)
        tmpBtn.grid(column = 0, row = 0, padx=4, pady=8)
        
    ## Create console panel
    #
    #  Create the console panel.  It the console text box.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def consolePanel(self):
        tmpFrm = Frame(self.bgndFrm, borderwidth = 5, relief=RAISED)
        tmpFrm.grid()
        tmpFrm.grid(column = 0, row = 1)
        self.scrollbar = Scrollbar(tmpFrm)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.log = Text(tmpFrm, wrap=WORD, yscrollcommand=self.scrollbar.set)
        self.log.pack()
        self.scrollbar.config(command=self.log.yview)
        
    ## Update console
    #
    #  Update the console window with new text
    #
    #  @param  self          [in]   Object reference
    #  @param  text          [in]   Text to be added to the console window
    #  @return None
    def updateConsole(self, text):
        self.log['state'] = 'normal'
        self.log.insert('end', text + "\n")
        self.log['state'] = 'disabled'
        self.log.see(END)
        
    ## GUI exit
    #
    #  Set the exit flag.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def gui_exit(self):
        self.exit = True

## Main
#
#  Read passed in arguments.  Create TK window.
#
#  @param  argv          [in]   Passed in arguments
#  @return None 
def main(argv=None):

    end = False
    rulesFile = None
    outDir = "GenCode"

    if argv is None:
        argv = sys.argv
    for arg in argv:
        if arg.startswith('-rulesFile='):
            rulesFile = arg[11:]
        elif arg.startswith('-outDir='):
            outDir = arg[8:]
        elif arg.startswith('-?'):
            print "python GenPyCode.py [OPTIONS]"
            print "    -?                 Options Help"
            print "    -rulesFile=        Name of the rules file to use as input"
            print "    -outDir=           Output directory of generated code"
            end = True
    if end:
        return 0
    
    root = Tk()
    gui = GuiFrame(root, rulesFile, outDir)
    root.wm_protocol ("WM_DELETE_WINDOW", gui.gui_exit)
    while not gui.exit:
        root.update()
        time.sleep(.1)
    return (0)

if __name__ == "__main__":
    sys.exit(main())
