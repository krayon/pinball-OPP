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
class InpBrd():
    numInpBrd = 0
    
    ## Used to indicate switch matrix is on card
    HAS_MATRIX = 0x10

    ## Used as wing number for switch matrices
    SWITCH_MATRIX_WING = 0x10
    
    ## Number of switch matrix columns
    NUM_MATRIX_COLS = 8
    
    ##  Used for switch input processing.  A '1' means it is a state input bit and
    #  the latest value is used.  A '0' means is an edge triggered input, and it
    #  is automatically cleared after being used.
    inpCfgBitfield = []
    
    ## Last data read from card
    lastData = []
    
    ## Current data read from card
    currInpData = []
    
    ## Mask of valid input bits on this card
    validDataMask = []
    
    ## Data remapper
    dataRemap = []
    
    ## Has matrix
    hasMatrix = []
    
    ## Initialize boards
    #
    #  Create an instance for each card in the system even if it doesn't
    #  contain inputs
    #
    #  @param  numBrds          [in]   Number of boards in the system
    def init_boards(self, numBrds):
        for card in xrange(numBrds):
            InpBrd.hasMatrix.append(False)
            InpBrd.inpCfgBitfield.append([])
            InpBrd.currInpData.append([])
            InpBrd.lastData.append([])
            InpBrd.validDataMask.append([])
            for wing in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
                InpBrd.inpCfgBitfield[card].append(0)
                InpBrd.currInpData[card].append(0)
                InpBrd.lastData[card].append(0)
                InpBrd.validDataMask[card].append(0)
            
        
    ## Add input card function
    #
    #  Called to add an input card
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Index of the card (0 based)
    #  @param  wingMask      [in]   Bitmask of input wings on this card
    #  @param  GameData      [in]   Game Data Object reference
    #  @return None
    def add_card(self, card, wingMask, GameData):
        InpBrd.numInpBrd += 1
        if (wingMask & ((1 << rs232Intf.NUM_G2_WING_PER_BRD) - 1) != 0):
            for bit in xrange(rs232Intf.NUM_G2_INP_PER_BRD):
                if (GameData.InpBitNames.INP_BRD_CFG[card][bit] == rs232Intf.CFG_INP_STATE):
                    wing = (bit & 0x18) >> 3
                    if (wingMask & (1 << wing) != 0):
                        InpBrd.inpCfgBitfield[card][wing] |= (1 << (bit & 0x7))
            inputBitsMask = 0xff
            for wing in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
                if (wingMask & (1 << wing) != 0):
                    InpBrd.validDataMask[card][wing] = 0xff
                    InpBrd.dataRemap.append((card << 16) | wing)
        
        # Check if there is a switch matrix
        if ((wingMask & InpBrd.HAS_MATRIX) != 0):
            validCols = 0
            InpBrd.hasMatrix[card] = True;
            for index in xrange(rs232Intf.NUM_G2_MATRIX_INP):
                if (GameData.InpBitNames.INP_BRD_MTRX_BIT_NAMES[card][index] != "Unused"):
                    validCols |= (1 << ((index & 0x38) >> 3))
            for col in xrange(rs232Intf.NUM_MATRIX_COL):
                InpBrd.inpCfgBitfield[card].append(0)
                InpBrd.currInpData[card].append(0)
                InpBrd.lastData[card].append(0)
                InpBrd.validDataMask[card].append(0xff)
                if (validCols & (1 << col) != 0):
                    InpBrd.dataRemap.append((card << 16) | (InpBrd.SWITCH_MATRIX_WING + col))
    
    ## Update the input status.
    #
    #  Clear the state input bits, and OR the new data read from
    #  the card to get the current state.
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Input board instance index (base 0)
    #  @param  wing          [in]   Wing number (base 0)
    #  @param  data          [in]   Data read from hardware card
    #  @return None
    def update_status(self, card, wing, data):
        # If normal wing inputs
        if (wing < rs232Intf.NUM_G2_WING_PER_BRD):
            data &= InpBrd.validDataMask[card][wing]
            latchData = (InpBrd.currInpData[card][wing] | data) & ~InpBrd.inpCfgBitfield[card][wing]
            # If state inputs swap sense (active high vs active low)
            stateData = (data & InpBrd.inpCfgBitfield[card][wing]) ^ InpBrd.inpCfgBitfield[card][wing]
            InpBrd.currInpData[card][wing] = latchData | stateData
            InpBrd.lastData[card][wing] = data
        # Otherwise this is a switch matrix
        else:
            # Only report on rising edge transitions since matrices
            # are always state
            InpBrd.currInpData[card][wing] |= (data ^ InpBrd.lastData[card][wing]) & ~InpBrd.lastData[card][wing]
        InpBrd.lastData[card][wing] = data
        
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
        data = InpBrd.currInpData[card][wing]
        InpBrd.currInpData[card][wing] &= InpBrd.inpCfgBitfield[card][wing]
        return data
