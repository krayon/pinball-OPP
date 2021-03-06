#!/usr/bin/env python
#
# Warning - This is an auto-generated file.  All changes to this file will
# be overwritten next time GenPyCode.py is re-run.  Do not change this file
# unless you want to start hand editing the files.
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
# @file    states.py
# @author  AutoGenerated
# @date    04/27/2017
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief This is an enumeration of all the states.

#===============================================================================

## State enumeration.
#  Contains an entry for each state
class State():
    def __init__(self):
        pass

    STATE_INIT                       = 0
    STATE_ATTRACT                    = 1
    STATE_INIT_GAME                  = 2
    STATE_STARTBALL                  = 3
    STATE_NORMAL_PLAY                = 4
    STATE_JUKEBOX                    = 5
    STATE_END_BALL                   = 6
    STATE_ERROR                      = 7
    STATE_TILT                       = 8


    ## State name strings.
    # Indexed into using [State](@ref states.State) enumeration
    STATE_STR = [ "Init", "Attract", "InitGame", "StartBall",
        "NormalPlay", "JukeBox", "EndBall", "Error",
        "Tilt", ]

