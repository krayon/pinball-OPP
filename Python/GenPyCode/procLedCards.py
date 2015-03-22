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
# @file    procLedCards.py
# @author  Hugh Spahr
# @date    7/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process LED_CARDS section.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc LED Cards class.
#
#  Contains functions for LED_CARDS section.
class ProcLedCards():
    numLedCards = 0

    ## Initialize the ProcLedCards class
    #
    #  Initialize LED cards to zero
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        self.out = 0
        ProcLedCards.hasData = False
        ProcLedCards.ledCfgBits = []
        ProcLedCards.name = []
        ProcLedCards.cardNum = []
        ProcLedCards.pinNum = []
        ProcLedCards.desc = []
        
        # Constants
        ProcLedCards.NUM_LED_BITS = 8

    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        if (ProcLedCards.hasData):
            parent.consoleObj.updateConsole("!!! Error !!! Found multiple LED_CARDS sections, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (400)
        ProcLedCards.hasData = True
        parent.consoleObj.updateConsole("Processing LED_CARDS section")
        if (parent.tokens[parent.currToken] != "LED_CARDS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected LED_CARDS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (401)
        parent.currToken += 1
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected number of LED cards, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (402)
        ProcLedCards.numLedCards = parent.helpFuncs.out
        for _ in xrange(ProcLedCards.numLedCards):
            ProcLedCards.ledCfgBits.append(0)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (403)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        self.createLedBitNames(parent)
        parent.currToken += 1
        return (0)

    ## Process line
    #
    # Line consists of name, cardNum, pinNum, and description string.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):
        name = parent.tokens[parent.currToken]
        ProcLedCards.name.append(name)
        if ProcChains.checkNameExists(parent.procChains, name):
            parent.consoleObj.updateConsole("!!! Error !!! LED bit name already exists, read %s, at line num %d." %
               (name, parent.lineNumList[parent.currToken]))
            return (410)           
        ProcChains.addName(parent.procChains, name, ProcChains.LED_BIT)
        
        # Verify card num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
            parent.consoleObj.updateConsole("!!! Error !!! LED card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (411)
        # Convert from 1 base to 0 based card num
        cardNum = parent.helpFuncs.out - 1
        # Card number is base 1
        if (cardNum < 0) or (cardNum >= ProcLedCards.numLedCards):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal LED card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (412)
        ProcLedCards.cardNum.append(cardNum)
        
        # Verify pin num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 2]):
            parent.consoleObj.updateConsole("!!! Error !!! LED pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (413)
        # Convert from 1 base to 0 based pin num, bit 0 = 0x80, bit 7 = 0x01
        pinNum = 7 - (parent.helpFuncs.out - 1)
        # Pin number is base 1
        if (pinNum < 0) or (pinNum >= ProcLedCards.NUM_LED_BITS):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal LED pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (414)
        if (ProcLedCards.ledCfgBits[cardNum] & (1 << pinNum)) != 0: 
            parent.consoleObj.updateConsole("!!! Error !!! LED pin configured multiple times, at line num %d." %
               (parent.lineNumList[parent.currToken + 2]))
            return (415)
        ProcLedCards.ledCfgBits[cardNum] |= (1 << pinNum)
        ProcLedCards.pinNum.append(pinNum)
        
        # Grab description
        desc = parent.tokens[parent.currToken + 3]
        ProcLedCards.desc.append(desc)
        
        # increment currToken
        parent.currToken += 4
        return (0)

    ## Create ledBitNames.py file
    #
    # Create the LED bit names file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createLedBitNames(self, parent):
        HDR_COMMENTS = [
            "# @file    ledBitNames.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2014, Hugh Spahr",
            "#",
            "# @brief These are the LED bit names.  It has a bitmask for each LED.",
            "",
            "#===============================================================================",
            "",
            "## LED bit name enumeration.",
            "#  Contains a bit mask for each LED.  Can also contain bitfield masks.",
            "#  Top most nibble contains the index of the LED card base 0.",
            "class LedBitNames:"]

        # Open the file or create if necessary
        outHndl = open(parent.consoleObj.outDir + os.sep + "ledBitNames.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                outHndl.write(line + "\n")
                
        # Write out NUM_LED_CARDS
        outHndl.write("    ## Number of LED boards in the system\n")
        outHndl.write("    NUM_LED_BRDS = {0}\n\n".format(ProcLedCards.numLedCards))
        
        # Write out LED bit enumeration
        for cardIndex in xrange(ProcLedCards.numLedCards):
            allBitsName = "LED{0}_ALL_BITS_MSK".format(cardIndex + 1)
            outHndl.write("    {0:32} = 0x{1:05x}\n".format( allBitsName,
                (cardIndex * 0x10000) + 0x00ff))
            ProcChains.addName(parent.procChains, allBitsName, ProcChains.LED_BIT)
            parent.procChains.ledDict[allBitsName] = (cardIndex * 0x10000) + 0x00ff
            for bitIndex in xrange(ProcLedCards.NUM_LED_BITS):
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    outHndl.write("    {0:32} = 0x{1:05x}\n".format(ProcLedCards.name[self.out].upper(),
                        ((cardIndex << 16) | (1 << bitIndex))))
                    # Create the LED name dictionary
                    parent.procChains.ledDict[ProcLedCards.name[self.out].upper()] = ((cardIndex << 16) | (1 << bitIndex))
        
                    
        # Write out the bit name strings
        outHndl.write("\n    ## LED board bit names\n")
        outHndl.write("    # Indexed into using the [LedBitNames](@ref ledBitNames.LedBitNames) class\n")
        outHndl.write("    LED_BRD_BIT_NAMES = [ ")
        for cardIndex in xrange(ProcLedCards.numLedCards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            outHndl.write("[")
            for bitIndex in xrange(ProcLedCards.NUM_LED_BITS):
                if (bitIndex != 0):
                    if ((bitIndex % 4) == 0):
                        outHndl.write(",\n        ")
                    else:
                        outHndl.write(", ")
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    outHndl.write(ProcLedCards.desc[self.out])
                else:
                    outHndl.write("\"Unused\"")
            outHndl.write("]")
        outHndl.write(" ]\n\n")
        outHndl.close()
        parent.consoleObj.updateConsole("Completed: ledBitNames.py file.")
        return (0)

    ## Find bit index
    #
    # Find index of the bit.  If no bit is found (i.e. it is not
    # configured, it returns false.
    #
    #  @param  self          [in]   Object reference
    #  @param  cardNum       [in]   Card number
    #  @param  bitNum        [in]   Bit number
    #  @return True if found, False if not found.  Passes index
    #   in out 
    def findBitIndex(self, cardNum, bitNum):
        for index in xrange(len(ProcLedCards.pinNum)):
            if (ProcLedCards.cardNum[index] == cardNum) and (ProcLedCards.pinNum[index] == bitNum):
                self.out = index
                return True
        return False

