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
# @file    startPin.py
# @author  Hugh Spahr
# @date    1/15/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Main entry point to start the pinball machine

#===============================================================================

import sys
import time
from comms.commThread import CommThread
from tk.tkinterThread import TkinterThread
from pygameFunc import Pygame_Data
from rulesThread import RulesThread
from ledThread import LedThread
from timerThread import TimerThread
import dispIntf
from gameData import GameData
from globConst import GlobConst

## Main
#
#  Read passed in arguments and set simWidth, actWidth, fullScr,
#  if tk debug window should be created, and the serial port id.
#  Initialize the display and start it.  Initialize pygame.  If
#  debug is set, create the tk window and thread.  Create comms,
#  rules and LED threads and start them.  In the main loop process
#  pygame events watching for an exit command.  If exited, close
#  down all threads.
#
#  @param  argv          [in]   Passed in arguments
#  @return None 
def main(argv=None):

    end = False
    actWidth = 1920
    actHeight = 1080
    simWidth = 0
    comPort = ""
    rulesDir = "rules"

    fullScreen = False
    debug = False
    if argv is None:
        argv = sys.argv
    for arg in argv:
        if arg.startswith('-simWidth='):
            simWidth = int(arg[10:])
        elif arg.startswith('-fullscr'):
            fullScreen = True
        elif arg.startswith('-port='):
            comPort = arg[6:]
        elif arg.startswith('-debug'):
            debug = True
        elif arg.startswith('-rulesDir='):
            rulesDir = arg[10:]
        elif arg.startswith('-?'):
            print "python startPin.py [OPTIONS]"
            print "    -?                 Options Help"
            print "    -simWidth=         Width of simulation screen in pixels (assumes HD format)"
            print "    -fullscr           Full screen mode"
            print "    -port=             COM port number (ex. COM1)"
            print "    -debug             Create debug window"
            print "    -rulesDir=         Directory that contains the rules"
            end = True
    if end:
        return 0
    
    GameData.debug = debug
    GameData.init_brd_objs(GameData(rulesDir))
    
    actWidth = GameData.GameConst.DISPLAY_RESOLUTION[GameData.GameConst.WIDTH_OFFSET]
    actHeight = GameData.GameConst.DISPLAY_RESOLUTION[GameData.GameConst.HEIGHT_OFFSET]
    
    #Set actual width if not entered
    if simWidth == 0:
        simWidth = GameData.GameConst.DISPLAY_RESOLUTION[GameData.GameConst.WIDTH_OFFSET]
    if (actWidth < simWidth):
        GameData.GameConst.DISPLAY_RESOLUTION[GameData.GameConst.WIDTH_OFFSET] = simWidth
    error = dispIntf.initDisp(GameData, simWidth, fullScreen)
    if error: exit()
    dispIntf.startDisp()
    
    #Initialize Pygame class
    pygame = Pygame_Data()
    
    #If Debugging created debug window
    if GameData.debug:
        tkinterThread = TkinterThread()
        tkinterThread.init(GameData)
        tkinterThread.start()
        while not TkinterThread.doneInit:
            time.sleep(.1)
    
    #Initialize the COMMs to the hardware
    commThread = CommThread()
    GameData.commThread = commThread
    commThread.init(comPort)
    commThread.start()
    
    #Initialize the timer thread
    timerThread = TimerThread()
    timerThread.init()
    timerThread.start()
    
    #Initialize the rules thread
    rulesThread = RulesThread()
    rulesThread.init(GameData)
    rulesThread.start()
    
    #Initialize the LED thread
    ledThread = LedThread()
    ledThread.init(GameData)
    ledThread.start()
    
    done = False
    while not done:
        done = pygame.Proc_Pygame_Events()
        pygame.Update_Displays()
        pygame.Update_Bgnd_Music()
        time.sleep(float(GlobConst.PYGAME_SLEEP)/1000.0)    
    if GameData.debug:
        tkinterThread.tkinterExit()
    commThread.commExit()
    dispIntf.stopDisp()
    rulesThread.rulesExit()
    ledThread.ledExit()
    timerThread.timerExit()

if __name__ == "__main__":
    sys.exit(main())
  
