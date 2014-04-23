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
# @file:   solBrd.py
# @author: Hugh Spahr
# @date:   4/23/2014
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
# This is the class that keeps information about the solenoid boards. 
#
#===============================================================================

vers = '00.00.01'

import rs232Intf
from rulesData import RulesData

class SolBrd():
    numSolBrds = 0
    
    #Used for switch input processing.  A '1' means it is a state input bit and
    #  the latest value is used.  A '0' means is an edge triggered input, and it
    #  is automatically cleared after being used.
    solCfgBitfield = []
    
    #Current data read from card
    currSolData = []
    
    def add_card(self):
        brdNum = self.numSolBrds
        self.numSolBrds += 1
        bitField = 0
        for bit in range(rs232Intf.NUM_SOL_PER_BRD):
            cmdOffset = rs232Intf.CFG_BYTES_PER_SOL * bit
            holdOffset = cmdOffset + rs232Intf.DUTY_CYCLE_OFFSET
            if (RulesData.SOL_BRD_CFG[brdNum][cmdOffset] == rs232Intf.CFG_SOL_AUTO_CLR) or \
                   (ord(RulesData.SOL_BRD_CFG[brdNum][holdOffset]) != 0):
                bitField |= (1 << bit)
        self.solCfgBitfield.append(0)
        self.currSolData.append(0)
    
    def update_status(self, card, data):
        self.currSolData[card] &= ~self.solCfgBitfield[card]
        self.currSolData[card] |= data
        
    def get_status(self, card):
        #Clear all the edge triggered bits
        data = self.currSolData[card]
        self.curSolData &= self.solCfgBitfield[card]
        return data
    