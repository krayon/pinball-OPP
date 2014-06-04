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
# @file    dispIntf.py
# @author  Hugh Spahr
# @date    1/22/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the display interface file that is used to send changes to the
# display thread.

#===============================================================================

import errIntf
import dispThread
from gameData import GameData

## Initialize display function
#
#  Call display thread init.  Return any errors from the init call.
#
#  @param  simWidth      [in]   Simulated screen width
#  @param  actWidth      [in]   Width of full sized screen
#  @param  fullScr       [in]   True if full screen mode.
#  @return Errors from display thread initialization.
def initDisp(simWidth, actWidth, fullScr):
    retVal = dispThread.init(simWidth, actWidth, fullScr)
    return (retVal)

## Start display function
#
#  Call display thread start.
#
#  @return CMD_OK
def startDisp():
    dispThread.start()
    return (errIntf.CMD_OK)

## Update display function
#
#  Or the update bit for the display
#
#  @param  disp          [in]   Display to be updated
#  @return None
def updateDisp(disp):
    GameData.updDisp |= (1 << disp)

## Update a feature light to on/off or blink
#
#  Add the update to the update feature list
#
#  @param  num           [in]   Index of the feature light
#  @param  value         [in]   on/off or blink
#  @return None
def updateFeatureLight(num, value):
    dispThread.updFeatList.append([num, value])
  
## Update a general illumination lights to on or off
#
#  Change general illumination lights on or off
#
#  @param  value         [in]   True to turn GI on
#  @return None
def updateGiLights(value):
    dispThread.updGiState = value

## Play a sound
#
#  @param  num           [in]   Index of sound to play
#  @return None
def playSound(num):
    dispThread.playSound(num)

## Update background
#
#  @param  num           [in]   Index of image to show
#  @return None
def updateBgnd(num):
    dispThread.updateBgnd(num)

## Stop display function
#
#  Call display thread exit.
#
#  @return None
def stopDisp():
    dispThread.dispExit()
