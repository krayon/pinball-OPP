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
# @file:   inpBrd.py
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
# This is the class that keeps information about the input boards. 
#
#===============================================================================

vers = '00.00.01'

import rs232Intf
from rulesData import RulesData

class InpBrd():
    numInpBrds = 0
    
    #Used for switch input processing.  A '1' means it is a state input bit and
    #  the latest value is used.  A '0' means is an edge triggered input, and it
    #  is automatically cleared after being used.
    inpCfgBitfield = []
    
    #Current data read from card
    currInpData = []
    
    def add_card(self):
        brdNum = self.numInpBrds
        self.numInpBrds += 1
        bitField = 0
        for bit in range(rs232Intf.NUM_INP_PER_BRD):
            if (RulesData.INP_BRD_CFG[brdNum][bit] == rs232Intf.CFG_INP_STATE):
                bitField |= (1 << bit)
        self.inpCfgBitfield.append(0)
        self.currInpData.append(0)
    
    def update_status(self, card, data):
        self.currInpData[card] &= ~self.inpCfgBitfield[card]
        self.currInpData[card] |= data
        
    def get_status(self, card):
        #Clear all the edge triggered bits
        data = self.currInpData[card]
        self.curInpData &= self.inpCfgBitfield[card]
        return data
    