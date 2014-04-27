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
# @file:   startPin.py
# @author: Hugh Spahr
# @date:   1/15/2014
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
# Start the pin
#
#===============================================================================

from sys import exit
import sys
import time
from commThread import CommThread
from tkinterThread import TkinterThread
from pygameFunc import Pygame_Data
from rulesThread import RulesThread
import dispIntf
from gameData import GameData

def main(argv=None):

    end = False
    simWidth = 1920
    comPort = ""
    GameData.debug = False
    GameData.init_brd_objs(GameData())

    actWidth = 0
    fullScreen = False
    if argv is None:
        argv = sys.argv
    for arg in argv:
        if arg.startswith('-simWidth='):
            simWidth = int(arg[10:])
        elif arg.startswith('-actualWidth='):
            actWidth = int(arg[13:])
        elif arg.startswith('-fullscr'):
            fullScreen = True
        elif arg.startswith('-port='):
            comPort = arg[6:]
        elif arg.startswith('-debug'):
            GameData.debug = True
        elif arg.startswith('-?'):
            print "python startPin.py [OPTIONS]"
            print "    -?                 Options Help"
            print "    -simWidth=         Width of simulation screen in pixels (assumes HD format)"
            print "    -actualWidth=      Width of final screen in pixels (assumes HD format)"
            print "                       Used for scaling.  If not set, assume simWidth is final"
            print "    -fullscr           Full screen mode"
            print "    -port=             COM port number (ex. COM1)"
            end = True
    if end:
        return 0
    
    #Set actual width if not entered
    if (actWidth < simWidth):
        actWidth = simWidth
    error = dispIntf.initDisp(simWidth, actWidth, fullScreen)
    if error: exit()
    dispIntf.startDisp()
    
    #Initialize Pygame class
    pygame = Pygame_Data()
    
    #If Debugging created debug window
    if GameData.debug:
        tkinterThread = TkinterThread()
        tkinterThread.init()
        tkinterThread.start()
        while not TkinterThread.doneInit:
            time.sleep(.1)
    
    #Initialize the COMMs to the hardware
    commThread = CommThread()
    commThread.init(comPort)
    commThread.start()
    
    #Initialize the rules thread
    rulesThread = RulesThread()
    rulesThread.init()
    rulesThread.start()
    
    done = False
    while not done:
        done = pygame.Proc_Pygame_Events()
        pygame.Update_Displays()
        time.sleep(.01)    
    commThread.commExit()
    rulesThread.rulesExit()
    if GameData.debug:
        tkinterThread.tkinterExit()

if __name__ == "__main__":
    sys.exit(main())
  
