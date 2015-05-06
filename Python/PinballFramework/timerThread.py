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
# @file    timerThread.py
# @author  Hugh Spahr
# @date    5/7/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the timer thread file that is used for timers.  It needs
# a thread to so the timers can run at a different rate than the rules thread.

#===============================================================================

from gameData import GameData
from threading import Thread
from globConst import GlobConst
import time

## Timer thread class.
#
#  Updates timers and marks if they have expired
class TimerThread(Thread):
    #private members
    _runTimerThread = True
    _threadlock = 0
        
    ## The constructor.
    def __init__(self):
        super(TimerThread, self).__init__()
        
        # Create the timer variables
        for i in xrange(len(GameData.Timers.timeouts)):
            # Every 32 timers requires another bitfield
            if (i & 0x1f) == 0:
                GameData.expiredTimers.append(0) 
                GameData.runningTimers.append(0) 
                GameData.reportExpOnce.append(0)
            GameData.timerCnt.append(0)
             
    ## Initialize timers
    #
    #  Nothing to do
    #
    #  @param  self          [in]   Object reference
    def init(self):
        pass
    
    ## Start the timer thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def start(self):
        super(TimerThread, self).start()
    
    ## Exit the timer thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def timerExit(self):
        TimerThread._runTimerThread = False

            
    ## Process timers
    #
    #  See if any timers are running
    #  updates.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_timers(self):
        for tmrGrp in xrange(len(GameData.runningTimers)):
            if (GameData.runningTimers[tmrGrp] != 0):
                numTmr = len(GameData.timerCnt) - (tmrGrp * GameData.Timers.TIMERS_PER_GROUP)
                if numTmr >= GameData.Timers.TIMERS_PER_GROUP:
                    numTmr = GameData.Timers.TIMERS_PER_GROUP
                for timer in xrange(numTmr):
                    if GameData.runningTimers[tmrGrp] & (1 << timer) != 0:
                        # Calculate the timer index, increment time
                        currTmr = (tmrGrp * GameData.Timers.TIMERS_PER_GROUP) + timer
                        GameData.timerCnt[currTmr] += GlobConst.TIMER_SLEEP
                        
                        # Check if timer has expired
                        if GameData.timerCnt[currTmr] >= \
                                GameData.Timers.timeouts[currTmr][GameData.Timers.TIMEOUT_OFFSET]:
                            GameData.expiredTimers[tmrGrp] |= (1 << timer)
                            GameData.runningTimers[tmrGrp] &= ~(1 << timer)
            
    ## The timer thread
    #
    #  Run the timer thread processing
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def run(self):
      
        while TimerThread._runTimerThread:
            #Process timers
            self.proc_timers()
                    
            #Sleep until next timer processing time
            time.sleep(float(GlobConst.TIMER_SLEEP)/1000.0)
