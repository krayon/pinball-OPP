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
# @file    procSolCards.py
# @author  Hugh Spahr
# @date    7/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process SOLENOID_CARDS section.

#===============================================================================

import os
import time
from procChains import ProcChains
import rs232Intf

## Proc Solenoid Cards class.
#
#  Contains functions for SOLENOID_CARDS section.
class ProcSolCards():

    ## Initialize the ProcSolCards class
    #
    #  Initialize solenoid cards to zero
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        self.out = 0
        ProcSolCards.hasData = False
        ProcSolCards.solCfgBits = []
        ProcSolCards.name = []
        ProcSolCards.cardNum = []
        ProcSolCards.pinNum = []
        ProcSolCards.flagStr = []
        ProcSolCards.initKick = []
        ProcSolCards.dutyCycle = []
        ProcSolCards.minOff = []
        ProcSolCards.desc = []
        ProcSolCards.hasSolWingMask = 0
        
        # Constants
        ProcSolCards.NUM_SOL_BITS = 16

    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procSection(self, parent):
        if (ProcSolCards.hasData):
            parent.consoleObj.updateConsole("!!! Error !!! Found multiple SOLENOID_CARDS sections, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (200)
        ProcSolCards.hasData = True
        parent.consoleObj.updateConsole("Processing SOLENOID_CARDS section")
        if (parent.tokens[parent.currToken] != "SOLENOID_CARDS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected SOLENOID_CARDS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (201)
        parent.currToken += 1
        for _ in xrange(parent.procSimple.numGen2Cards):
            ProcSolCards.solCfgBits.append(0)
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (203)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        if errVal == 0:
            self.createSolBitNames(parent)
        parent.currToken += 1
        return (errVal)

    ## Process line
    #
    # Line consists of name, cardNum, pinNum, flags, intialKick, dutyCycle, minOff,
    # and description string.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):
        VALID_FLAGS = ["USE_SWITCH", "AUTO_CLR", "USE_MTRX_INP", "ON_OFF_USE_SW", "USE_MTRX_AUTO_CLR"]
        GEN_FLAGS = ["rs232Intf.CFG_SOL_USE_SWITCH", "rs232Intf.CFG_SOL_AUTO_CLR", \
            "rs232Intf.CFG_SOL_USE_MTRX_INP", "rs232Intf.CFG_SOL_ON_OFF_USE_SW", \
            "rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR"]
        MAX_INIT_KICK = 255
        MAX_DUTY_CYCLE = 15
        MAX_MIN_OFF = 7
        MIN_MATRX_INP = 0
        MAX_MATRX_INP = 63

        name = parent.tokens[parent.currToken]
        ProcSolCards.name.append(name)
        ProcChains.addName(parent.procChains, name, ProcChains.SOLENOID_BIT)
        
        # Verify card num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (210)
        # Card num is now 0 based
        cardNum = parent.helpFuncs.out
        if (cardNum < 0) or (cardNum >= parent.procSimple.numGen2Cards):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal solenoid card num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (211)
        ProcSolCards.hasSolWingMask |= (1 << cardNum)
        ProcSolCards.cardNum.append(cardNum)
        
        # Verify pin num
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 2]):
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (212)
        # Pin num is now 0 based
        pinNum = parent.helpFuncs.out
        if (pinNum < 0) or (pinNum >= ProcSolCards.NUM_SOL_BITS):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal solenoid pin num, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (213)
        if (ProcSolCards.solCfgBits[cardNum] & (1 << pinNum)) != 0: 
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid pin configured multiple times, at line num %d." %
               (parent.lineNumList[parent.currToken + 2]))
            return (214)
        ProcSolCards.solCfgBits[cardNum] |= (1 << pinNum)
        ProcSolCards.pinNum.append(pinNum)
        
        # Verify flagStr
        if not parent.helpFuncs.isValidString(parent.tokens[parent.currToken + 3], VALID_FLAGS):
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid illegal flags, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 3], parent.lineNumList[parent.currToken + 3]))
            return (215)
        
        flagStr = GEN_FLAGS[parent.helpFuncs.out]
        inpFlagStr = VALID_FLAGS[parent.helpFuncs.out]
        ProcSolCards.flagStr.append(flagStr)
        
        # Verify init kick
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 4]):
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid initKick, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 4], parent.lineNumList[parent.currToken + 4]))
            return (216)
        initKick = parent.helpFuncs.out
        # Verify init kick is not out of range
        if (initKick < 0) or (initKick > MAX_INIT_KICK):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal initKick value, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 4], parent.lineNumList[parent.currToken + 4]))
            return (217)
        ProcSolCards.initKick.append(initKick)
        
        # Verify dutyCycle
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 5]):
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid dutyCycle, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 5], parent.lineNumList[parent.currToken + 5]))
            return (218)
        dutyCycle = parent.helpFuncs.out
        # Verify dutyCycle is not out of range
        if (dutyCycle < 0) or (dutyCycle > MAX_DUTY_CYCLE):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal dutyCycle value, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 5], parent.lineNumList[parent.currToken + 5]))
            return (219)
        ProcSolCards.dutyCycle.append(dutyCycle)
        
        # Verify minOff
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 6]):
            parent.consoleObj.updateConsole("!!! Error !!! Solenoid minOff, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 6], parent.lineNumList[parent.currToken + 6]))
            return (220)
        minOff = parent.helpFuncs.out
        # Verify minOff is not out of range
        if ((inpFlagStr != "USE_MTRX_INP") and (inpFlagStr != "USE_MTRX_AUTO_CLR")):
            if (minOff < 0) or (minOff > MAX_MIN_OFF):
                parent.consoleObj.updateConsole("!!! Error !!! Illegal minOff value, read %s, at line num %d." %
                   (parent.tokens[parent.currToken + 6], parent.lineNumList[parent.currToken + 6]))
                return (221)
        else:
            # It is a matrix input so must be within range
            if (minOff < MIN_MATRX_INP) or (minOff > MAX_MATRX_INP):
                parent.consoleObj.updateConsole("!!! Error !!! Illegal minOff (matrix input) value, read %s, at line num %d." %
                   (parent.tokens[parent.currToken + 6], parent.lineNumList[parent.currToken + 6]))
                return (222)
        ProcSolCards.minOff.append(minOff)
        
        # Grab description
        desc = parent.tokens[parent.currToken + 7]
        ProcSolCards.desc.append(desc)
        
        # increment currToken
        parent.currToken += 8
        return (0)

    ## Create solBitNames.py file
    #
    # Create the solenoid bit names file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createSolBitNames(self, parent):
        HDR_COMMENTS = [
            "# @file    solBitNames.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2014, Hugh Spahr",
            "#",
            "# @brief These are the solenoid bit names.  It has a bitmask for each solenoid.",
            "",
            "#===============================================================================",
            "",
            "import rs232Intf",
            "",
            "## Solenoid bit name enumeration.",
            "#  Contains a bit mask for each solenoid.  Can also contain bitfield masks.",
            "#  Top most nibble contains the index of the solenoid card base 0.",
            "class SolBitNames:",
            "    def __init__(self):",
            "        pass",
            ""]

        # Open the file or create if necessary
        outHndl = open(parent.consoleObj.outDir + os.sep + "solBitNames.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                outHndl.write(line + "\n")
        # Write out the bit name enumerations
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            for bitIndex in xrange(ProcSolCards.NUM_SOL_BITS):
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    offset = bitIndex & 0x03;
                    wingBrdIndex = (bitIndex & 0x0c) >> 2;
                    # Look for any errors such as wing board being a different type
                    if ((parent.procSimple.cardWingInv[cardIndex][wingBrdIndex] != 0) and (parent.procSimple.cardWingInv[cardIndex][wingBrdIndex] != rs232Intf.WING_SOL)):
                        parent.consoleObj.updateConsole("!!! Error !!! Gen2 wing board previous configured as 0x{0:02x}.".format(ord(parent.procSimple.cardWingInv[cardIndex][wingBrdIndex])))
                        return (230)
                    parent.procSimple.cardWingInv[cardIndex][wingBrdIndex] = rs232Intf.WING_SOL
                    outHndl.write("    {0:48} = 0x{1:08x}\n".format(ProcSolCards.name[self.out].upper(),
                        ((cardIndex << 24) | (wingBrdIndex << 16) | (1 << offset))))

        # Write out the bit masks enumerations
        outHndl.write("\n");
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            for bitIndex in xrange(ProcSolCards.NUM_SOL_BITS):
                found = self.findBitIndex(cardIndex, bitIndex)
                if found:
                    offset = ((bitIndex & 0x0c) << 1) | (bitIndex & 0x03)
                    name = ProcSolCards.name[self.out].upper() + "_CRD{0}MSK".format(cardIndex)
                    outHndl.write("    {0:48} = 0x{1:08x}\n".format(name, (1 << offset)))

        # Write out the bit name strings
        outHndl.write("\n    ## Solenoid board bit names\n")
        outHndl.write("    # Indexed into using the [SolBitNames](@ref solBitNames.SolBitNames) class\n")
        outHndl.write("    SOL_BRD_BIT_NAMES = [ ")
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            if (ProcSolCards.hasSolWingMask & (1 << cardIndex) == 0):
                outHndl.write("[ ]")
            else:
                outHndl.write("[")
                for bitIndex in xrange(ProcSolCards.NUM_SOL_BITS):
                    if (bitIndex != 0):
                        if ((bitIndex % 4) == 0):
                            outHndl.write(",\n        ")
                        else:
                            outHndl.write(", ")
                    found = self.findBitIndex(cardIndex, bitIndex)
                    if found:
                        outHndl.write(ProcSolCards.desc[self.out])
                    else:
                        outHndl.write("\"Unused\"")
                outHndl.write("]")
        outHndl.write(" ]\n\n")

        # Write solenoid board configuration
        outHndl.write("    ## Solenoid board configuration\n")
        outHndl.write("    # Three bytes for each solenoid being configured\n")
        outHndl.write("    SOL_BRD_CFG = [ ")
        for cardIndex in xrange(parent.procSimple.numGen2Cards):
            if (cardIndex != 0):
                outHndl.write(",\n        ")
            if (ProcSolCards.hasSolWingMask & (1 << cardIndex) == 0):
                outHndl.write("[ ]")
            else:
                outHndl.write("[")
                for bitIndex in xrange(ProcSolCards.NUM_SOL_BITS):
                    if (bitIndex != 0):
                        if ((bitIndex % 2) == 0):
                            outHndl.write(",\n        ")
                        else:
                            outHndl.write(", ")
                    found = self.findBitIndex(cardIndex, bitIndex)
                    if found:
                        outHndl.write(ProcSolCards.flagStr[self.out] + ", ")
                        outHndl.write("'\\x" + hex(ProcSolCards.initKick[self.out])[2:].zfill(2) + "', ")
                        if (ProcSolCards.flagStr[self.out] != "rs232Intf.CFG_SOL_USE_MTRX_INP") and \
                            (ProcSolCards.flagStr[self.out] != "rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR"):
                            thirdByte = (ProcSolCards.minOff[self.out] * 16) + ProcSolCards.dutyCycle[self.out]
                        else:
                            thirdByte = ProcSolCards.minOff[self.out]
                        outHndl.write("'\\x" + hex(thirdByte)[2:].zfill(2) + "'")
                    else:
                        outHndl.write("rs232Intf.CFG_SOL_DISABLE, '\\x00', '\\x00'")
                outHndl.write("]")
        outHndl.write(" ]\n\n")
        outHndl.close()
        parent.consoleObj.updateConsole("Completed: solBitNames.py file.")
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
        for index in xrange(len(ProcSolCards.pinNum)):
            if (ProcSolCards.cardNum[index] == cardNum) and (ProcSolCards.pinNum[index] == bitNum):
                self.out = index
                return True
        return False
        
