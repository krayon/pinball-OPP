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
# @file    procChains.py
# @author  Hugh Spahr
# @date    9/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process PROCESS_CHAINS section and create rulesFunc.py.

#===============================================================================

import os
import time
import re

## Proc Chains class.
#
#  Contains functions for PROCESS_CHAINS section.
class ProcChains:
    OPEN_PAREN = 1
    OPEN_CURLY = 2
    COMMAND = 3
    IF_STATEMENT = 4
    ELSE_STATEMENT = 5
    COMMA = 6
    INPUT_BIT = 7
    SOLENOID_BIT = 8
    LED_BIT = 9
    INDEXED_VAR = 10
    VARIABLE = 11
    CHAIN_NAME = 12
    LED_CHAIN_NAME = 13
    SOUND_CHAIN_NAME = 14
    VIDEO_CHAIN_NAME = 15
    SOUND_NAME = 16
    VIDEO_NAME = 17
    BGND_SOUND_NAME = 18
    
    PROC_STATEMENT = 100
    PROC_STD_FUNC = 101
    PROC_BOOL = 102
    PROC_CHAINS = 103

    ## Initialize the ProcChains class
    #
    #  Initialize process chains class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcChains.hasChains = False
        ProcChains.nameSet = set()
        ProcChains.tokenLookup = {
            '(' : ProcChains.OPEN_PAREN,
            '{' : ProcChains.OPEN_CURLY,
            ',' : ProcChains.COMMA,
            'DISABLE_SOLENOIDS' : ProcChains.COMMAND,
            'ENABLE_SOLENOIDS' : ProcChains.COMMAND,
            'LED_ROT_LEFT' : ProcChains.COMMAND,
            'LED_ROT_RIGHT' : ProcChains.COMMAND,
            'LED_OFF' : ProcChains.COMMAND,
            'LED_ON' : ProcChains.COMMAND,
            'LED_SET' : ProcChains.COMMAND,
            'LED_BLINK_100' : ProcChains.COMMAND,
            'VAR_ROT_LEFT' : ProcChains.COMMAND,
            'VAR_ROT_RIGHT' : ProcChains.COMMAND,
            'MODE' : ProcChains.COMMAND,
            'KICK' : ProcChains.COMMAND,
            'START' : ProcChains.COMMAND,
            'TIMEOUT' : ProcChains.COMMAND,
            'TEXT' : ProcChains.COMMAND,
            'IMAGE' : ProcChains.COMMAND,
            'SOUND' : ProcChains.COMMAND,
            'PLAY_BGND' : ProcChains.COMMAND,
            'STOP_BGND' : ProcChains.COMMAND,
            'WAIT' : ProcChains.COMMAND,
            'VIDEO' : ProcChains.COMMAND,
            'if' : ProcChains.IF_STATEMENT,
            'else' : ProcChains.ELSE_STATEMENT}
        ProcChains.possChainDict = dict() 
        
    ## Add name
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @param  nameType      [in]   Type of the name
    #  @return None
    def addName(self, name, nameType):
        ProcChains.tokenLookup[name] = nameType
        
    ## Check name exists
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @return True if name exists in dictionary
    def checkNameExists(self, name):
        if name in ProcChains.tokenLookup:
            return (True)
        else:
            return (False)

    ## Get name type
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @return True if name exists in dictionary
    def getNameType(self, name):
        return(ProcChains.tokenLookup[name])
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing PROCESS_CHAINS section")
        if (parent.tokens[parent.currToken] != "PROCESS_CHAINS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected PROCESS_CHAINS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1100)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1101)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createRulesFunc(parent)
        while parent.currToken < closeSymb:
            errVal = self.procAllFuncs(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing PROCESS_CHAINS.")
        ProcChains.outHndl.close()
        return (0)

    ## Process all functions
    #
    # Chain consists of name and group of statements.  This processing
    # is currently not implemented.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procAllFuncs(self, parent):
        # Copy name
        name = parent.tokens[parent.currToken]
        if (name in ProcChains.nameSet):
            parent.consoleObj.updateConsole("!!! Error !!! Name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1110)
        ProcChains.nameSet.add(name)
        ProcChains.outHndl.write("    ## Function {0}\n".format(name))
        ProcChains.outHndl.write("    #\n")
        ProcChains.outHndl.write("    #  @param  self          [in]   Object reference\n")
        ProcChains.outHndl.write("    #  @return None\n")
        ProcChains.outHndl.write("    def {0}(self):\n".format(name))
        ProcChains.outHndl.write("        pass\n\n")
        
        #Verify opening symbol
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1111)
        closeSymb = parent.helpFuncs.findMatch(parent)
        ProcChains.currDepth = 2
        parent.currToken += 1
        # Note:  This processing isn't done.  Just move to the end of the chain.
        parent.currToken = closeSymb
        while parent.currToken < closeSymb:
            tokenType = ProcChains.tokenLookup[parent.currToken]
            if tokenType == ProcChains.OPEN_PAREN:
                #Processing statement, statement could still be a std func call or chains
                #Look at next token to see
                typeProc = ProcChains.PROC_STATEMENT
                nextTokenType = ProcChains.tokenLookup[parent.tokens[parent.currToken + 1]]
                if (nextTokenType == None) or (nextTokenType == ProcChains.CHAIN_NAME):
                    #This could be an unknown chain name.  See if alpha, numeric,
                    #  underscores, and at least one character
                    isPossChain = re.match(r'[\w_]+$', parent.tokens[parent.currToken + 1])
                    if isPossChain:
                        typeProc = ProcChains.PROC_CHAINS
                        error = self.procChainList(parent)
                    else:
                        parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                            (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
                        return (1112)
                elif (nextTokenType == ProcChains.COMMAND):
                    print "Unknown"  
            elif tokenType == ProcChains.OPEN_CURLY:
                print "Not programmed"  
            elif tokenType == ProcChains.COMMAND:
                print "Not programmed"  
            elif tokenType == ProcChains.IF_STATEMENT:
                print "Not programmed"  
            elif tokenType == ProcChains.ELSE_STATEMENT:
                print "Not programmed"  
            elif tokenType == ProcChains.INPUT_BIT:
                print "Not programmed"  
            elif tokenType == ProcChains.SOLENOID_BIT:
                print "Not programmed"  
            elif tokenType == ProcChains.LED_BIT:
                print "Not programmed"  
            elif tokenType == ProcChains.INDEXED_VAR:
                print "Not programmed"  
            elif tokenType == ProcChains.VARIABLE:
                print "Not programmed"  
            else:
                #Can't understand symbol
                parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (1113)
            errVal = self.procFunc(parent)
            if errVal:
                parent.currToken = closeSymb
        
        # increment currToken
        parent.currToken += 1
        return (0)

    ## Create rulesFunc.py file
    #
    # Create the rules function file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createRulesFunc(self, parent):
        HDR_COMMENTS = [
            "# @file    rulesFunc.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2014, Hugh Spahr",
            "#",
            "# @brief These are the rules function names.  The rules functions can call",
            "#    other rules functions, or be called in chains.",
            "",
            "#===============================================================================",
            "",
            "from rules.inpBitNames import InpBitNames",
            "from rules.solBitNames import SolBitNames",
            "from rules.ledBitNames import LedBitNames",
            "from rules.timers import Timers",
            "from rules.rulesData import RulesData",
            "from rules.sounds import Sounds",
            "from rules.sounds import BgndMusic",
            "from rules.states import State",
            "from rules.images import Images",
            "from gameData import GameData",
            "from stdFuncs import StdFuncs",
            "",
            "## Rules functions class.",
            "#  Contains all the rules that are specific this this set of pinball rules.",
            "",
            "class RulesFuncs:"
            "    #Create stdFunc instance",
            "    stdFuncs = StdFuncs()",
            ""]

        # Open the file or create if necessary
        ProcChains.outHndl = open(parent.consoleObj.outDir + os.sep + "rulesFunc.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcChains.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcChains.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcChains.outHndl.write(line + "\n")
        return (0)

    ## Process function
    #
    # Process a single function.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procFunc(self, parent):
        return 0
    
    ## Write to output file
    #
    #  @param  self          [in]   Object reference
    #  @param  token         [in]   token to write
    #  @param  tokenType     [in]   token type
    #  @return none
    def writeToOutFile(self, token, tokenType):
        if (tokenType == ProcChains.CHAIN_NAME):
            tmpStr = '    '*ProcChains.currDepth
            ProcChains.outHndl.write(tmpStr + "self." + token + "()\n")

    ## Process chain list
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return none
    def procChainList(self, parent):
        #Find ending
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currentToken += 1
        while (parent.currToken < closeSymb):
            addChain = False
            error = False
            tokenType = ProcChains.tokenLookup[parent.tokens[parent.currToken]]
            if tokenType == None:
                #This could be an unknown chain name.  See if alpha, numeric,
                #  underscores, and at least one character
                isPossChain = re.match(r'[\w_]+$', parent.tokens[parent.currToken])
                if isPossChain:
                    #Store name to lookup later, and line number if it can't be found to give an error message
                    ProcChains.possChainDict[parent.tokens[parent.currToken]] = parent.lineNumList[parent.currToken]
                    addChain = True
                else:
                    #Can't understand symbol
                    error = True
            elif tokenType == ProcChains.COMMA:
                addChain = False
            elif tokenType == ProcChains.CHAIN_NAME:
                addChain = True
            else:
                error = True
            if addChain:
                self.writeToOutFile(parent.tokens[parent.currToken], ProcChains.CHAIN_NAME)
            if not error:
                parent.currToken += 1
            else:
                parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (1120)
        return (0)
