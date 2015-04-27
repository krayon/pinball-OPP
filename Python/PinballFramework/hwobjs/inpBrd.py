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
# @file    inpBrd.py
# @author  Hugh Spahr
# @date    4/23/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the class that keeps information about the input boards.

#===============================================================================

import rs232Intf

## Input board class.
#  Keep information about the input board including configuration and current
#  input status.
class InpBrd():
    numInpBrd = 0
    
    ## Used for switch input processing.  A '1' means it is a state input bit and
    #  the latest value is used.  A '0' means is an edge triggered input, and it
    #  is automatically cleared after being used.
    inpCfgBitfield = []
    
    ## Current data read from card
    currInpData = []
    
    ## Add input card function
    #
    #  Called to add an input card
    #
    #  @param  self          [in]   Object reference
    #  @param  GameData      [in]   Game Data Object reference
    #  @return None
    def add_card(self, GameData):
        brdNum = InpBrd.numInpBrd
        InpBrd.numInpBrd += 1
        bitField = 0
        for bit in xrange(rs232Intf.NUM_INP_PER_BRD):
            if (GameData.InpBitNames.INP_BRD_CFG[brdNum][bit] == rs232Intf.CFG_INP_STATE):
                bitField |= (1 << bit)
        InpBrd.inpCfgBitfield.append(bitField)
        InpBrd.currInpData.append(0)
    
    ## Update the input status.
    #
    #  Clear the state input bits, and OR the new data read from
    #  the card to get the current state.
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Input board instance index (base 0)
    #  @param  data          [in]   Data read from hardware card
    #  @return None
    def update_status(self, card, data):
        latchData = (InpBrd.currInpData[card] | data) & ~InpBrd.inpCfgBitfield[card]
        stateData = (data & InpBrd.inpCfgBitfield[card]) ^ InpBrd.inpCfgBitfield[card]
        InpBrd.currInpData[card] = latchData | stateData
        
    ## Get input status
    #
    #  Grab the stored input status and return it.  Clear all the edge
    #  triggered inputs so they are only acted upon once.
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Input board instance index (base 0)
    #  @return Input card status
    def get_status(self, card):
        #Clear all the edge triggered bits
        data = InpBrd.currInpData[card]
        InpBrd.currInpData[card] &= InpBrd.inpCfgBitfield[card]
        return data
