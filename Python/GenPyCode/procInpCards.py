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
import rs232Intf

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
        ProcInpCards.matrixCfgBits = []
        ProcInpCards.name = []
        ProcInpCards.cardNum = []
        ProcInpCards.pinNum = []
        ProcInpCards.flagStr = []
        ProcInpCards.desc = []
        ProcInpCards.hasInpWingMask = 0
        ProcInpCards.hasMatrixWingMask = 0

        # Constants
        ProcInpCards.NUM_INP_BITS = 32
        ProcInpCards.MIN_MATRIX_INP = 32
        ProcInpCards.MAX_MATRIX_INP = 95
        
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
        for _ in xrange(parent.procSimple.numGen2Cards):
            ProcInpCards.inpCfgBits.append(0)
            ProcInpCards.matrixCfgBits.append([0,0])
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
        VALID_FLAGS = ["STATE_INPUT", "FALL_EDGE", "RISE_EDGE", "MATRIX"]
        GEN_FLAGS = ["rs232Intf.CFG_INP_STATE", "rs232Intf.CFG_INP_FALL_EDGE", "rs232Intf.CFG_INP_RISE_EDGE", "Matrix"]

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
        # Card num is now 0 based
        cardNum = parent.helpFuncs.out
        if (cardNum < 0) or (cardNum >= parent.procSimple.numGen2Cards):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal input card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (312)
        ProcInpCards.cardNum.append(cardNum)
        
        # Verify pin num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 2]):
            parent.consoleObj.updateConsole("!!! Error !!! Input pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (313)
        # Pin number is now base 0
        pinNum = parent.helpFuncs.out
        
        # Verify flagStr
        if not parent.helpFuncs.isValidString(parent.tokens[parent.currToken + 3], VALID_FLAGS):
            parent.consoleObj.updateConsole("!!! Error !!! Input illegal flags, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 3], parent.lineNumList[parent.currToken + 3]))
            return (316)
        flagStr = GEN_FLAGS[parent.helpFuncs.out]
        ProcInpCards.flagStr.append(flagStr)
        
        # Check if this is a normal input or a matrix input
        if (flagStr != "Matrix"):
            # It is a normal input
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
            ProcInpCards.hasInpWingMask |= (1 << cardNum)
        else:
            # It is a matrix input
            if (pinNum < ProcInpCards.MIN_MATRIX_INP) or (pinNum > ProcInpCards.MAX_MATRIX_INP):
                parent.consoleObj.updateConsole("!!! Error !!! Illegal matrix input pin num, read %s, at line num %d." %
                   (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
                return (316)
            if (ProcInpCards.inpCfgBits[cardNum] & (1 << pinNum)) != 0: 
                parent.consoleObj.updateConsole("!!! Error !!! Input pin configured multiple times, at line num %d." %
                   (parent.lineNumList[parent.currToken + 2]))
                return (317)
            ProcInpCards.hasMatrixWingMask |= (1 << cardNum)
            matrixIndex = pinNum - ProcInpCards.MIN_MATRIX_INP
            
            # Break into two 32 bit fields for storing bit mask for matrix
            if (pinNum - ProcInpCards.MIN_MATRIX_INP > 32):
                ProcInpCards.matrixCfgBits[cardNum][1] |= (1 << (pinNum - ProcInpCards.MIN_MATRIX_INP - 32))
            else:
                ProcInpCards.matrixCfgBits[cardNum][0] |= (1 << (pinNum - ProcInpCards.MIN_MATRIX_INP))
            ProcInpCards.pinNum.append(pinNum)
        
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
            "class InpBitNames:",
            "    def __init__(self):",
            "        pass",
            ""]

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
                
        # Write out the bit name enumerations for normal inputs
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            for bitIndex in xrange(ProcInpCards.NUM_INP_BITS):
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    offset = bitIndex & 0x07;
                    wingBrdIndex = (bitIndex & 0x18) >> 3;
                    # Look for any errors such as wing board being a different type
                    if ((parent.procSimple.cardWingInv[cardIndex][wingBrdIndex] != 0) and (parent.procSimple.cardWingInv[cardIndex][wingBrdIndex] != rs232Intf.WING_INP)):
                        parent.consoleObj.updateConsole("!!! Error !!! Gen2 wing board previous configured as 0x{0:02x}.".format(ord(parent.procSimple.cardWingInv[cardIndex][wingBrdIndex])))
                        return (330)
                    parent.procSimple.cardWingInv[cardIndex][wingBrdIndex] = rs232Intf.WING_INP
                    outHndl.write("    {0:48} = 0x{1:08x}\n".format(ProcInpCards.name[self.out].upper(),
                        ((cardIndex << 24) | (wingBrdIndex << 16) | (1 << offset))))

        # Write out the bit name enumerations for matrix inputs
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            if (ProcInpCards.hasMatrixWingMask & (1 << cardIndex) != 0):
                for bitIndex in xrange(ProcInpCards.MIN_MATRIX_INP, ProcInpCards.MAX_MATRIX_INP + 1):
                    found = self.findBitIndex(cardIndex, bitIndex)
                    if found:
                        offset = bitIndex & 0x07;
                        # Wing board indices have 0x80 to indicate matrix and byte offset
                        wingBrdIndex = 0x80 | (((bitIndex - 0x20) & 0x38) >> 3);
                        # Look for any errors such as wing board being a different type
                        if ((parent.procSimple.cardWingInv[cardIndex][2] != 0) and (parent.procSimple.cardWingInv[cardIndex][2] != rs232Intf.WING_SW_MATRIX_IN)):
                            parent.consoleObj.updateConsole("!!! Error !!! Gen2 wing board previous configured as 0x{0:02x}.".format(ord(parent.procSimple.cardWingInv[cardIndex][wingBrdIndex])))
                            return (331)
                        # Look for any errors such as wing board being a different type
                        if ((parent.procSimple.cardWingInv[cardIndex][3] != 0) and (parent.procSimple.cardWingInv[cardIndex][3] != rs232Intf.WING_SW_MATRIX_OUT)):
                            parent.consoleObj.updateConsole("!!! Error !!! Gen2 wing board previous configured as 0x{0:02x}.".format(ord(parent.procSimple.cardWingInv[cardIndex][wingBrdIndex])))
                            return (332)
                        parent.procSimple.cardWingInv[cardIndex][2] = rs232Intf.WING_SW_MATRIX_IN
                        parent.procSimple.cardWingInv[cardIndex][3] = rs232Intf.WING_SW_MATRIX_OUT
                        outHndl.write("    {0:48} = 0x{1:08x}\n".format(ProcInpCards.name[self.out].upper(),
                            ((cardIndex << 24) | (wingBrdIndex << 16) | (1 << offset))))

        # Write out the bit masks enumerations
        outHndl.write("\n");
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            for bitIndex in xrange(ProcInpCards.NUM_INP_BITS):
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    offset = (bitIndex & 0x1f)
                    name = ProcInpCards.name[self.out].upper() + "_CRD{0}MSK".format(cardIndex)
                    outHndl.write("    {0:48} = 0x{1:08x}\n".format(name, (1 << offset)))
                    
        # Write out the bit name strings
        outHndl.write("\n    ## Input board bit names\n")
        outHndl.write("    # Indexed into using the [InpBitNames](@ref inpBitNames.InpBitNames) class\n")
        outHndl.write("    INP_BRD_BIT_NAMES = [ ")
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            if (ProcInpCards.hasInpWingMask & (1 << cardIndex) == 0):
                outHndl.write("[ ]")
            else:
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
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            if (ProcInpCards.hasInpWingMask & (1 << cardIndex) == 0):
                outHndl.write("[ ]")
            else:
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
        
        # Write out the matrix bit name strings
        outHndl.write("\n    ## Input board matrix bit names\n")
        outHndl.write("    # Indexed into using the [InpBitNames](@ref inpBitNames.InpBitNames) class\n")
        outHndl.write("    INP_BRD_MTRX_BIT_NAMES = [ ")
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            if (ProcInpCards.hasMatrixWingMask & (1 << cardIndex) == 0):
                outHndl.write("[ ]")
            else:
                outHndl.write("[")
                for bitIndex in xrange(ProcInpCards.MIN_MATRIX_INP, ProcInpCards.MAX_MATRIX_INP + 1):
                    if (bitIndex != ProcInpCards.MIN_MATRIX_INP):
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
        
