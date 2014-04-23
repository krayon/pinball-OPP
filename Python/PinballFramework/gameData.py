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

vers = '00.00.01'

from rulesData import State
from rulesData import RulesData
from inpBrd import InpBrd
from solBrd import SolBrd
from ledBrd import LedBrd
import rs232Intf

class GameData():
    credits = 0
    creditsInRow = 0
    partCreditsNum = 0
    extraCredit = 0
    partCreditsDenom = 0
    
    gameMode = State.ATTRACT
    score = [0, 0, 0, 0]
    ballNum = 0
    currPlayer = 0
    numPlayers = 0
    inlaneLights = []
    scoreLvl = 0
    specialLvl = 0
    kick_retries = 0
    
    #Used for switch input processing.  Logical OR of debug data (simSwitchBits)
    #  and Comms data (switchInpData, switchSolData)
    currInpStatus = []
    currSolStatus = []
    
    expiredTimers = 0

    def __init__(self):
        self.credits = 0
        self.creditsInRow = 0
        self.partCreditsNum = 0
        self.extraCredit = 4
        self.partCreditsDenom = 2
        
        self.gameMode = State.ATTRACT
        self.score = [0, 0, 0, 0]
        self.ballNum = 0
        self.currPlayer = 0
        self.numPlayers = 0
        self.inlaneLights = []
        self.scoreLvl = 0
        self.specialLvl = 0
        self.kick_retries = 0
        
        self.currInpStatus = []
        self.currSolStatus = []
        self.expiredTimers = 0

    def add_inp_brd(self):
        self.currInpStatus.append(0)
        
    def add_sol_brd(self):
        self.currSolStatus.append(0)
        
    def init_brd_objs(self):
        for i in range(len(RulesData.INV_ADDR_LIST)):
            if ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_INP_CARD)): 
                InpBrd.add_card()
            elif ((RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_SOL_CARD)):
                SolBrd.add_card()
        for i in range(RulesData.NUM_LED_BRDS):
            LedBrd.add_card()
