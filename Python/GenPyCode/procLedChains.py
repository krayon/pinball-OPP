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
# @file    procLedChains.py
# @author  Hugh Spahr
# @date    1/13/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Process LED_CHAINS section.

#===============================================================================

import os
import time
from procChains import ProcChains
from procLedCards import ProcLedCards

## Proc LED Chains class.
#
#  Contains functions for LED_CHAINS section.
class ProcLedChains:
    UNKNOWN = 0
    OPEN_PAREN = 1
    CLOSE_PAREN = 2
    WAIT_COMMAND = 3
    END_CHAIN_COMMAND = 4
    REPEAT_COMMAND = 5
    COMMA = 6
    LOGIC_OR = 7
    ZERO = 8
    
    PROC_MASK = 100
    PROC_LED_BIT = 101
    PROC_COMMAND = 102
    PROC_DONE_CHAIN = 103

    ## Initialize the ProcLedChains class
    #
    #  Initialize process LED chains class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcLedChains.nameSet = set()
        ProcLedChains.tokenLookup = {
            '(' : ProcLedChains.OPEN_PAREN,
            ')' : ProcLedChains.CLOSE_PAREN,
            ',' : ProcLedChains.COMMA,
            '|' : ProcLedChains.LOGIC_OR,
            '0' : ProcLedChains.ZERO,
            'WAIT' : ProcLedChains.WAIT_COMMAND,
            'END_CHAIN' : ProcLedChains.END_CHAIN_COMMAND,
            'REPEAT' : ProcLedChains.REPEAT_COMMAND }
        
    ## Add name
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @param  nameType      [in]   Type of the name
    #  @return None
    def addName(self, name, nameType):
        ProcLedChains.tokenLookup[name] = nameType
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing LED_CHAINS section")
        if (parent.tokens[parent.currToken] != "LED_CHAINS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected LED_CHAINS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1200)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1201)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createLedChainsClass(parent)
        while parent.currToken < closeSymb:
            errVal = self.procAllChains(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing LED_CHAINS.")
        ProcLedChains.outHndl.close()
        return (0)

    ## Process all chains
    #
    # Chain consists of mask, then set value and command repeated until a END_CHAIN or REPEAT command is read.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procAllChains(self, parent):
        # Create the lists to support multiple LED cards
        ledCard = [[] for _ in range(ProcLedCards.numLedCards)]
        
        # Copy name
        name = parent.tokens[parent.currToken]
        if (name in ProcLedChains.nameSet):
            parent.consoleObj.updateConsole("!!! Error !!! Name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1210)
        ProcLedChains.nameSet.add(name)
        ProcChains.addName(parent.procChains, name, ProcChains.LED_CHAIN_NAME)
        ProcLedChains.outHndl.write("    ## LED Chain {0}\n".format(name))
        ProcLedChains.outHndl.write("    #    - First entry is LED mask\n")
        ProcLedChains.outHndl.write("    #    - Next groups have a bitfield of LEDs to change and command\n")
        ProcLedChains.outHndl.write("    {0} = [".format(name))

        # Verify opening symbol
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1211)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        typeProc = ProcLedChains.PROC_MASK
        firstBit = True
        while parent.currToken < closeSymb:
            if parent.tokens[parent.currToken] in ProcLedChains.tokenLookup:
                tokenType = ProcLedChains.tokenLookup[parent.tokens[parent.currToken]]
            else:
                tokenType = ProcLedChains.UNKNOWN
            if (tokenType == ProcLedChains.OPEN_PAREN) or (tokenType == ProcLedChains.CLOSE_PAREN):
                # Opening and closing parenthesis are dropped since they aren't necessary
                # Move to next symbol
                parent.currToken += 1
            elif tokenType == ProcLedChains.WAIT_COMMAND:
                if typeProc != ProcLedChains.PROC_COMMAND: 
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT command in LED chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1212)
                # Next token should be wait timeout (ms) 
                if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT parameter should be integer, read %s, at line num %d." %
                       (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
                    return (1213)
                ProcLedChains.outHndl.write(" WAIT, " + parent.tokens[parent.currToken + 1] + "],\n          [ ")
                # If any close parenthesis exist eat them
                parent.currToken += 2
                while (ProcLedChains.tokenLookup[parent.tokens[parent.currToken]] == ProcLedChains.CLOSE_PAREN):
                    parent.currToken += 1
                # Next token must be a comma
                if (ProcLedChains.tokenLookup[parent.tokens[parent.currToken]] != ProcLedChains.COMMA):
                    parent.consoleObj.updateConsole("!!! Error !!! Comma missing after wait command, found %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1214)
                parent.currToken += 1
                typeProc = ProcLedChains.PROC_LED_BIT
                firstBit = True
            elif tokenType == ProcLedChains.END_CHAIN_COMMAND:
                if typeProc != ProcLedChains.PROC_COMMAND: 
                    parent.consoleObj.updateConsole("!!! Error !!! END_CHAIN command in LED chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1215)
                ProcLedChains.outHndl.write("END_CHAIN, 0] ] ]\n\n")
                parent.currToken += 1
                typeProc = ProcLedChains.PROC_DONE_CHAIN
            elif tokenType == ProcLedChains.REPEAT_COMMAND:
                if typeProc != ProcLedChains.PROC_COMMAND: 
                    parent.consoleObj.updateConsole("!!! Error !!! REPEAT command in LED chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1216)
                ProcLedChains.outHndl.write("REPEAT, 0] ] ]\n\n")
                parent.currToken += 1
                typeProc = ProcLedChains.PROC_DONE_CHAIN
            elif tokenType == ProcLedChains.COMMA:
                if typeProc == ProcLedChains.PROC_MASK:
                    ProcLedChains.outHndl.write("\n        [ ")
                    for card in xrange(ProcLedCards.numLedCards):
                        if (card != 0):
                            ProcLedChains.outHndl.write(", ")
                        if len(ledCard[card]) == 0:
                            ProcLedChains.outHndl.write("0")
                        else:
                            for bit in xrange(len(ledCard[card])):
                                if (bit != 0):
                                    ProcLedChains.outHndl.write(" | ")
                                ProcLedChains.outHndl.write(ledCard[card][bit])
                    ProcLedChains.outHndl.write(" ],\n        [ [ ")
                    parent.currToken += 1
                    typeProc = ProcLedChains.PROC_LED_BIT
                    firstBit = True
                    ledCard = [[] for _ in range(ProcLedCards.numLedCards)]
                elif  typeProc == ProcLedChains.PROC_LED_BIT:
                    ProcLedChains.outHndl.write("[ ")
                    for card in xrange(ProcLedCards.numLedCards):
                        if (card != 0):
                            ProcLedChains.outHndl.write(", ")
                        if len(ledCard[card]) == 0:
                            ProcLedChains.outHndl.write("0")
                        else:
                            for bit in xrange(len(ledCard[card])):
                                if (bit != 0):
                                    ProcLedChains.outHndl.write(" | ")
                                ProcLedChains.outHndl.write(ledCard[card][bit])
                    ProcLedChains.outHndl.write(" ], ")
                    parent.currToken += 1
                    typeProc = ProcLedChains.PROC_COMMAND
                    ledCard = [[] for _ in range(ProcLedCards.numLedCards)]
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Unexpected comma at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1217)
            elif tokenType == ProcLedChains.LOGIC_OR:
                if ((typeProc != ProcLedChains.PROC_LED_BIT) and (typeProc != ProcLedChains.PROC_MASK)) or firstBit: 
                    parent.consoleObj.updateConsole("!!! Error !!! Unexpected | at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1218)
                parent.currToken += 1
            elif tokenType == ProcLedChains.ZERO:
                if not firstBit:
                    parent.consoleObj.updateConsole("!!! Error !!! 0 not first bit in mask at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1219)
                if (typeProc == ProcLedChains.PROC_MASK):
                    ProcLedChains.outHndl.write(",\n        [ [ ")
                    parent.currToken += 1
                    typeProc = ProcLedChains.PROC_LED_BIT
                    firstBit = True
                elif (typeProc == ProcLedChains.PROC_LED_BIT):
                    parent.currToken += 1
                    typeProc = ProcLedChains.PROC_LED_BIT
                    firstBit = True
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Unexpected 0 at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1220)
            else:
                #This must be a bit name symbol
                if (ProcChains.checkNameExists(parent.procChains, parent.tokens[parent.currToken])):
                    if (ProcChains.getNameType(parent.procChains, parent.tokens[parent.currToken]) != ProcChains.LED_BIT):
                        parent.consoleObj.updateConsole("!!! Error !!! Symbol %s should only be an LED bit, at line num %d." %
                           (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                        return (1221)
                    else:
                        # HRS:  This could be improved to verify any set bits are in the mask
                        card = parent.procChains.findBit(parent.tokens[parent.currToken].upper()) >> 16
                        ledCard[card].append("LedBitNames.{0}".format(parent.tokens[parent.currToken].upper()))
                        firstBit = False
                        parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1222)
        if (typeProc != ProcLedChains.PROC_DONE_CHAIN):
            parent.consoleObj.updateConsole("!!! Error !!! LED chain did not end properly, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (1223)
        parent.currToken += 1
        return (0)

    ## Create ledChains.py file
    #
    # Create the LED chains function file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createLedChainsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    ledChains.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief These are the LED chains.  It includes chains to automatically change",
            "#    LEDs depending on the state.",
            "",
            "#===============================================================================",
            "",
            "from ledBitNames import LedBitNames",
            "",
            "## LED chains class.",
            "#",
            "#  Contains all the LED chains that are specific this this set of pinball rules.",
            "class LedChains():",
            "    def __init__(self):",
            "        pass",
            "",
            "    # LED chain commands",
            "    WAIT = 0",
            "    REPEAT = 1",
            "    END_CHAIN = 2",
            "",
            "    MASK_OFFSET = 0",
            "    CHAIN_OFFSET = 1",
            "",
            "    # Offsets into sublist",
            "    CH_LED_BITS_OFFSET = 0",
            "    CH_CMD_OFFSET = 1",
            "    PARAM_OFFSET = 2",
            ""]
    
        # Open the file or create if necessary
        ProcLedChains.outHndl = open(parent.consoleObj.outDir + os.sep + "ledChains.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcLedChains.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcLedChains.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcLedChains.outHndl.write(line + "\n")
        return (0)
