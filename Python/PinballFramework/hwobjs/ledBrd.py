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
# @file    ledBrd.py
# @author  Hugh Spahr
# @date    4/23/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the class that keeps information about the LED boards.

#===============================================================================

import rs232Intf

## LED board class.
#  Keep information about the LED board including blinking LEDs and current
#  status.
#  @param  numBrds          [in]   Number of boards in the system
class LedBrd():
    numLedBrds = 0
    
    ## Used for blinking Leds at 500 ms.
    currBlinkLeds = []
    
    ## Current data output to the LEDs
    currLedData = []
        
    ## Mask of valid input bits on this card
    validIncandMask = []
    
    ## Data remapper
    dataRemap = []
        
    ## Initialize boards
    #
    #  Create an instance for each card in the system even if it doesn't
    #  contain leds
    #
    #  @param  numBrds          [in]   Number of boards in the system
    def init_boards(self, numBrds):
        for card in xrange(numBrds):
            LedBrd.currBlinkLeds.append(0)
            LedBrd.currLedData.append(0)
            LedBrd.validIncandMask.append(0)
        
    ## Add LED card function
    #
    #  Called to add an LED card
    #
    #  @param  self          [in]   Object reference
    #  @param  card          [in]   Index of the card (0 based)
    #  @param  wingMask      [in]   Bitmask of incandescent wings on this card
    #  @return None
    def add_card(self, card, wingMask):
        LedBrd.numLedBrds += 1
        incandBitsMask = 0xff
        mask = 0
        for wing in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
            if (wingMask & (1 << wing) != 0):
                mask |= (incandBitsMask << (wing << 3))
                LedBrd.dataRemap.append((card << 16) | wing)
        LedBrd.validIncandMask.append(mask)
