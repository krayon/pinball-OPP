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
# @file:   rulesThread.py
# @author: Hugh Spahr
# @date:   1/18/2014
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
# This is the rules thread file that is used to implement the rules for the
# pinball machine
#
#===============================================================================

vers = '00.00.02'

import rs232Intf
from threading import Thread
import time

class RulesThread(Thread):
    #game mode
    GAME_ATTRACT = 0
    GAME_PLAYING = 1
    
    #Game Parameters
    numCredits = 0
    numPlayers = 0
    gameMode = GAME_ATTRACT
    _runRulesThread = True
    
    #Comm thread states
    GAME_INIT           = 0
    GAME_OVER           = 1

    #Initialize rules thread
    def init(self):
        #Nothing to do currently
        pass
        
    def start(self):
        #Verify correct number of boards
        #Configure the boards
        super(RulesThread, self).start()
        
    def rulesExit(self):
        self._runRulesThread = False

    def run(self):
        count = 0
      
        while self._runRulesThread:
            count += 1
            time.sleep(1)
            print "Rules thread: %d" % count
            #Rules thread processing

