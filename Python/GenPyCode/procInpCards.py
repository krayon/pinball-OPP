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
# @file    procInpCards.py
# @author  Hugh Spahr
# @date    7/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process INPUT_CARDS section.

#===============================================================================

import os
import time
from procChains import ProcChains

# HRS:  Unimplemented - Support for ALL_BITS_MSK for each LED card

## Proc Input Cards class.
#
#  Contains functions for INPUT_CARDS section.
class ProcInpCards():

    ## Initialize the ProcInpCards class
    #
    #  Initialize input cards to zero
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        self.out = 0
        ProcInpCards.hasData = False
        ProcInpCards.numInpCards = 0
        ProcInpCards.inpCfgBits = []
        ProcInpCards.name = []
        ProcInpCards.cardNum = []
        ProcInpCards.pinNum = []
        ProcInpCards.flagStr = []
        ProcInpCards.desc = []

        # Constants
        ProcInpCards.NUM_INP_BITS = 16
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        if (ProcInpCards.hasData):
            parent.consoleObj.updateConsole("!!! Error !!! Found multiple INPUT_CARDS sections, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (300)
        ProcInpCards.hasData = True
        parent.consoleObj.updateConsole("Processing INPUT_CARDS section")
        if (parent.tokens[parent.currToken] != "INPUT_CARDS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected INPUT_CARDS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (301)
        parent.currToken += 1
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected number of input cards, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (302)
        ProcInpCards.numInpCards = parent.helpFuncs.out
        for _ in xrange(ProcInpCards.numInpCards):
            ProcInpCards.inpCfgBits.append(0)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (303)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        self.createInpBitNames(parent)
        parent.currToken += 1
        return (0)

    ## Process line
    #
    # Line consists of name, cardNum, pinNum, flags,
    # and description string.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):
        VALID_FLAGS = ["STATE_INPUT", "FALL_EDGE", "RISE_EDGE"]
        GEN_FLAGS = ["rs232Intf.CFG_INP_STATE", "rs232Intf.CFG_INP_FALL_EDGE", "rs232Intf.CFG_INP_RISE_EDGE"]

        name = parent.tokens[parent.currToken]
        if name in ProcInpCards.name:
            parent.consoleObj.updateConsole("!!! Error !!! Found %s name twice at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (310)
        ProcInpCards.name.append(name)
        ProcChains.addName(parent.procChains, name, ProcChains.INPUT_BIT)
        
        # Verify card num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
            parent.consoleObj.updateConsole("!!! Error !!! Input card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (311)
        # Convert from 1 base to 0 based card num
        cardNum = parent.helpFuncs.out - 1
        # Card number is base 1
        if (cardNum < 0) or (cardNum >= ProcInpCards.numInpCards):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal input card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (312)
        ProcInpCards.cardNum.append(cardNum)
        
        # Verify pin num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 2]):
            parent.consoleObj.updateConsole("!!! Error !!! Input pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (313)
        # Convert from 1 base to 0 based pin num
        pinNum = parent.helpFuncs.out - 1
        # Pin number is base 1
        if (pinNum < 0) or (pinNum >= ProcInpCards.NUM_INP_BITS):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal input pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (314)
        if (ProcInpCards.inpCfgBits[cardNum] & (1 << pinNum)) != 0: 
            parent.consoleObj.updateConsole("!!! Error !!! Input pin configured multiple times, at line num %d." %
               (parent.lineNumList[parent.currToken + 2]))
            return (315)
        ProcInpCards.inpCfgBits[cardNum] |= (1 << pinNum)
        ProcInpCards.pinNum.append(pinNum)
        
        # Verify flagStr
        if not parent.helpFuncs.isValidString(parent.tokens[parent.currToken + 3], VALID_FLAGS):
            parent.consoleObj.updateConsole("!!! Error !!! Input illegal flags, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 3], parent.lineNumList[parent.currToken + 3]))
            return (316)
        flagStr = GEN_FLAGS[parent.helpFuncs.out]
        ProcInpCards.flagStr.append(flagStr)
        
        # Grab description
        desc = parent.tokens[parent.currToken + 4]
        ProcInpCards.desc.append(desc)
        
        # increment currToken
        parent.currToken += 5
        return (0)

    ## Create inpBitNames.py file
    #
    # Create the input bit names file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createInpBitNames(self, parent):
        HDR_COMMENTS = [
            "# @file    inpBitNames.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2014, Hugh Spahr",
            "#",
            "# @brief These are the input bit names.  It has a bitmask for each input.",
            "",
            "#===============================================================================",
            "",
            "import rs232Intf",
            "",
            "## Input bit name enumeration.",
            "#  Contains a bit mask for each input.  Can also contain bitfield masks.",
            "#  Top most nibble contains the index of the input card base 0.",
            "class InpBitNames:"]

        # Open the file or create if necessary
        outHndl = open(parent.consoleObj.outDir + os.sep + "inpBitNames.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                outHndl.write(line + "\n")
        for cardIndex in xrange(ProcInpCards.numInpCards):
            for bitIndex in xrange(ProcInpCards.NUM_INP_BITS):
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    outHndl.write("    {0:32} = 0x{1:05x}\n".format(ProcInpCards.name[self.out].upper(),
                        ((cardIndex << 16) | (1 << bitIndex))))
                    
        # Write out the bit name strings
        outHndl.write("\n    ## Input board bit names\n")
        outHndl.write("    # Indexed into using the [InpBitNames](@ref rules.inpBitNames.InpBitNames) class\n")
        outHndl.write("    INP_BRD_BIT_NAMES = [ ")
        for cardIndex in xrange(ProcInpCards.numInpCards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            outHndl.write("[")
            for bitIndex in xrange(ProcInpCards.NUM_INP_BITS):
                if (bitIndex != 0):
                    if ((bitIndex % 4) == 0):
                        outHndl.write(",\n        ")
                    else:
                        outHndl.write(", ")
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    outHndl.write(ProcInpCards.desc[self.out])
                else:
                    outHndl.write("\"Unused\"")
            outHndl.write("]")
        outHndl.write(" ]\n\n")

        # Write input board configuration
        outHndl.write("    ## Input board configuration\n")
        outHndl.write("    INP_BRD_CFG = [ ")
        for cardIndex in xrange(ProcInpCards.numInpCards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            outHndl.write("[")
            for bitIndex in xrange(ProcInpCards.NUM_INP_BITS):
                if (bitIndex != 0):
                    if ((bitIndex % 4) == 0):
                        outHndl.write(",\n        ")
                    else:
                        outHndl.write(", ")
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    outHndl.write(ProcInpCards.flagStr[self.out])
                else:
                    outHndl.write("rs232Intf.CFG_INP_STATE")
            outHndl.write("]")
        outHndl.write(" ]\n\n")
        outHndl.close()
        parent.consoleObj.updateConsole("Completed: inpBitNames.py file.")
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
        for index in xrange(len(ProcInpCards.pinNum)):
            if (ProcInpCards.cardNum[index] == cardNum) and (ProcInpCards.pinNum[index] == bitNum):
                self.out = index
                return True
        return False
        