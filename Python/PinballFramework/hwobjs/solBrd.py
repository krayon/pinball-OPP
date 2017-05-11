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
# @file    solBrd.py
# @author  Hugh Spahr
# @date    4/23/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the class that keeps information about the solenoid boards.

#===============================================================================

import rs232Intf

## Solenoid board class.
#  Keep information about the solenoid board including configuration and current
#  input status.
class SolBrd():
    numSolBrd = 0
    
    ## Used for switch input processing.  A '1' means it is a state input bit and
    #  the latest value is used.  A '0' means is an edge triggered input, and it
    #  is automatically cleared after being used.
    solCfgBitfield = []
    
    ## Last data read from card
    lastData = []
    
    ## Current including latched and state data
    currSolData = []
    
    ## Mask of valid input bits on this card
    validDataMask = []
    
    ## Data remapper
    dataRemap = []
        
    ## Initialize boards
    #
    #  Create an instance for each card in the system even if it doesn't
    #  contain inputs
    #
    #  @param  numBrds          [in]   Number of boards in the system
    def init_boards(self, numBrds):
        for card in xrange(numBrds):
            SolBrd.solCfgBitfield.append([])
            SolBrd.currSolData.append([])
            SolBrd.lastData.append([])
            SolBrd.validDataMask.append([])
            for wing in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
                SolBrd.solCfgBitfield[card].append(0)
                SolBrd.currSolData[card].append(0)
                SolBrd.lastData[card].append(0)
                SolBrd.validDataMask[card].append(0)
    
    ## Add input card function
    #
    #  Called to add an input card
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Index of the card (0 based)
    #  @param  wingMask      [in]   Bitmask of solenoid wings on this card
    #  @param  GameData      [in]   Game Data Object reference
    #  @return None
    def add_card(self, card, wingMask, GameData):
        SolBrd.numSolBrd += 1
        for bit in xrange(rs232Intf.NUM_G2_SOL_PER_BRD):
            cmdOffset = rs232Intf.CFG_BYTES_PER_SOL * bit
            holdOffset = cmdOffset + rs232Intf.DUTY_CYCLE_OFFSET
            if (GameData.SolBitNames.SOL_BRD_CFG[card][cmdOffset] == rs232Intf.CFG_SOL_AUTO_CLR) or \
                (GameData.SolBitNames.SOL_BRD_CFG[card][cmdOffset] == rs232Intf.CFG_SOL_DISABLE) or \
                (ord(GameData.SolBitNames.SOL_BRD_CFG[card][holdOffset]) != 0):
                wing = (bit & 0x0c) >> 2
                if (wingMask & (1 << wing) != 0):
                    SolBrd.solCfgBitfield[card][wing] |= (1 << (bit & 0x3))
        for wing in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
            if (wingMask & (1 << wing) != 0):
                SolBrd.dataRemap.append((card << 16) | wing)
                SolBrd.validDataMask[card][wing] = 0x0f
    
    ## Update the input status.
    #
    #  Clear the state input bits, and OR the new data read from
    #  the card to get the current state.
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Solenoid board instance index (base 0)
    #  @param  wing          [in]   Wing number (base 0)
    #  @param  data          [in]   Data read from hardware card
    #  @return None
    def update_status(self, card, wing, data):
        data &= SolBrd.validDataMask[card][wing]
        # Invert status bits
        latchData = (((SolBrd.lastData[card][wing] ^ data) & ~data) | SolBrd.currSolData[card][wing]) & ~SolBrd.solCfgBitfield[card][wing]
        stateData = (data & SolBrd.solCfgBitfield[card][wing]) ^ SolBrd.solCfgBitfield[card][wing]
        SolBrd.currSolData[card][wing] = latchData | stateData
        SolBrd.lastData[card][wing] = data
        
    ## Get input status
    #
    #  Grab the stored input status and return it.  Clear all the edge
    #  triggered inputs so they are only acted upon once.
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Input board instance index (base 0)
    #  @param  wing          [in]   Wing number (base 0)
    #  @return Input card status
    def get_status(self, card, wing):
        #Clear all the edge triggered bits
        data = SolBrd.currSolData[card][wing]
        SolBrd.currSolData[card][wing] &= SolBrd.solCfgBitfield[card][wing]
        return data
    
