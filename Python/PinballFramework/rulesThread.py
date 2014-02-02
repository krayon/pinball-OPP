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

vers = '00.00.01'

import array
import thread
import rs232Intf
import errIntf
import commHelp

#sound file list, note:  must be wav files
sndFile = ["sounds/wah_wuh.wav", "sounds/ding_ding.wav", "sounds/opendoor.wav",
           "sounds/jump.wav", "sounds/wfall1.wav", "sounds/wfall2.wav", "sounds/wfall3.wav"]

#Game Parameters
BALLS_PER_GAME = 3

numCredits = 0
numPlayers = 0

#game mode
GAME_ATTRACT = 0
GAME_PLAYING = 1


#Data that is shared with the interface file
#List of boards needed to run the pinball machine
BRD_INVENTORY = ['\x00', '\x10']
INIT_SOL_CFG = [ [ rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
                   rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
                   rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x00', \
                   rs232Intf.CFG_SOL_USE_SWITCH, '\x64', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x64', '\x00' ] ]
INIT_INP_CFG = [ [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
                   rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
                   rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
                   rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ] ]

#Comm thread states
GAME_INIT           = 0
GAME_OVER           = 1

#Initialize rules thread
def init(portId):
    gameMode = GAME_ATTRACT

def start():
    #Verify correct number of boards
    #Configure the boards
    thread.start_new_thread(rulesThread, ("Rules Thread",))

def rulesExit():
    runRulesThread = False

def rulesThread():
    while runRulesThread:
        #Comm thread processing
        runTask = False
