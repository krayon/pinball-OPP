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
# @file:   gameData.py
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
# This is the game data.  It include data about the current state of the game.
#
#===============================================================================

from rules.rulesData import RulesData
from inpBrd import InpBrd
from solBrd import SolBrd
from ledBrd import LedBrd
import rs232Intf
import dispConstIntf

class GameData():
    credits = 0
    creditsInRow = 0
    partCreditsNum = 0
    extraCredit = 5
    partCreditsDenom = 2
    
    prevGameMode = 0xffffffff
    gameMode = RulesData.INIT_MODE
    score = [0, 0, 0, 0]
    ballNum = 0
    currPlayer = 0
    numPlayers = 0
    inlaneLights = [0, 0, 0, 0]
    scoreLvl = 0
    numSpinners = 0
    specialLvl = 0
    kick_retries = 0
    
    debug = False
    inpBrd = InpBrd()
    solBrd = SolBrd()
    ledBrd = LedBrd()
    
    #Filled out if debug frame is created
    tkInpBrd = []
    tkSolBrd = []
    tkLedBrd = []
    
    #Used for switch input processing.  Logical OR of debug data (simSwitchBits)
    #  and Comms data (switchInpData, switchSolData)
    currInpStatus = []
    currSolStatus = []
    
    expiredTimers = 0

    def __init__(self):
        pass

    def init_brd_objs(self):
        for i in range(len(RulesData.INV_ADDR_LIST)):
            if ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_INP_CARD)): 
                InpBrd.add_card(self.inpBrd)
                GameData.currInpStatus.append(0)
            elif ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_SOL_CARD)):
                SolBrd.add_card(self.solBrd)
                GameData.currSolStatus.append(0)
        for i in range(RulesData.NUM_LED_BRDS):
            LedBrd.add_card(self.ledBrd)
