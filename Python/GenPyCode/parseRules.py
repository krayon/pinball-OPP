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
# @file    ParseRules.py
# @author  Hugh Spahr
# @date    7/1/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This creates the main parsing object which creates all calls functions
# to create the individual Python generated files.

#===============================================================================

import os
from helpFuncs import HelpFuncs
from procSolCards import ProcSolCards
from procInpCards import ProcInpCards
from procLedCards import ProcLedCards
from procVars import ProcVars
from procIndVars import ProcIndVars
from procSound import ProcSound
from procVideo import ProcVideo
from procSimple import ProcSimple
from procTimers import ProcTimers
from procChains import ProcChains

## Parse rules class.
#
#  Parse rules class is the main class which calls other classes to generate
#  individual Python files.
class ParseRules:
    
    ## The constructor.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Used to log information and get configuration
    def __init__(self, parent):
        self.tokens = []
        self.lineNumList = []
        self.consoleObj = parent
        self.currToken = 0
        self.helpFuncs = HelpFuncs()
        self.procSolCards = ProcSolCards()
        self.procInpCards = ProcInpCards()
        self.procLedCards = ProcLedCards()
        self.procVars = ProcVars()
        self.procIndVars = ProcIndVars()
        self.procSound = ProcSound()
        self.procVideo = ProcVideo()
        self.procSimple = ProcSimple()
        self.procTimers = ProcTimers()
        self.procChains = ProcChains()
        
    ## Verify parameters
    #
    #  Verify passed parameters are valid.
    #
    #  @param  self          [in]   Object reference
    #  @return 0 if successful, non-zero if unsuccessful 
    def verifyParameters(self):
        # If rulesFile wasn't passed, return error code
        if not self.consoleObj.rulesFile:
            self.consoleObj.updateConsole("Rules file not configured.  Use -rulesFile= command line argument to set it.")
            return 100
        # If rulesFile doesn't exist, return error code
        if not os.path.isfile(self.consoleObj.rulesFile):
            self.consoleObj.updateConsole("Rules file %s%s%s does not exist." % (os.getcwd(), os.sep, self.consoleObj.rulesFile))
            return 101
        # If outDir is empty, write warning that generated files will be in base directory
        if not self.consoleObj.outDir:
            self.consoleObj.updateConsole("!!! Warning !!! Generated files output in default directory.")
        else:
            # Check if directory exists
            if not os.path.isdir(self.consoleObj.outDir):
                # Create the directory
                self.consoleObj.updateConsole("Creating output directory %s%s%s does not exist." % (os.getcwd(), os.sep, self.consoleObj.outDir))
        # Open the rules files and verify the braces match properly
        hndl = open(self.consoleObj.rulesFile, 'r')
        if not self.verifyMatchingBrackets(hndl.read()):
            self.consoleObj.updateConsole("!!! Error !!! Matching bracket not found.")
        # Rewind the file
        hndl.seek(0)
        self.splitIntoTokens(hndl.read())
        hndl.close()
        self.findNextGroupCmd()
        return 0
    
    ## Verify matching brackets
    #
    #  @param  self          [in]   Object reference
    #  @param  text          [in]   Text to see if all brackets have match
    #  @return True if all brackets have matches 
    def verifyMatchingBrackets(self, text):
        stack = []
        lineStack = []
        posStack = []
        pushChars, popChars = "({[", ")}]"
        lineNum = 1
        for line in text.splitlines():
            # Remove all the comments
            firstComment = line.find('#')
            if firstComment != -1:
                line = line[:firstComment]
            charPos = 0
            for c in line :
                if c in pushChars :
                    stack.append(c)
                    lineStack.append(lineNum)
                    posStack.append(charPos)
                elif c in popChars :
                    if not len(stack) :
                        self.consoleObj.updateConsole("!!! Error !!! Found too many closing braces - %c...Line %d: Pos %d." % (c, lineNum, charPos))
                        return False
                    else :
                        stackTop = stack.pop()
                        openLine = lineStack.pop()
                        openPos = posStack.pop()
                        balancingBracket = pushChars[popChars.index(c)]
                        if stackTop != balancingBracket :
                            self.consoleObj.updateConsole("!!! Error !!! Closing brace doesn't match opening brace - %c...Line %d: Pos %d." % (c, lineNum, charPos))
                            self.consoleObj.updateConsole("Opening brace - %c...Line %d: Pos %d." % (stackTop, openLine, openPos))
                            return False
                charPos += 1
            lineNum += 1
        if len(stack):
            self.consoleObj.updateConsole("!!! Error !!! Not enough closing braces - %d leftover." % (len(stack)))
            while len(stack) != 0:
                stackTop = stack.pop()
                openLine = lineStack.pop()
                openPos = posStack.pop()
                self.consoleObj.updateConsole("No match for opening brace - %c...Line %d: Pos %d." % (stackTop, openLine, openPos))
        return not len(stack)
    
    ## Split into tokens
    #
    #  @param  self          [in]   Object reference
    #  @param  text          [in]   Text to split into tokens
    #  @return None 
    def splitIntoTokens(self, text):
        self.tokens = []
        self.lineNumList = []
        lineNum = 1
        replaceStrings = ["}","{","[","]","(",")",",","++","--"]
        
        for line in text.splitlines():
            # Remove all the comments
            firstComment = line.find('#')
            if firstComment != -1:
                line = line[:firstComment]
            
            # Add spaces before/after parenthesis, curly braces, brackets, commas, ++ and --
            for currRepl in replaceStrings:
                line = line.replace(currRepl, " " + currRepl + " ")
            
            # Split the line into tokens
            tmpTokens = line.split()
            if (len(tmpTokens) != 0):
                self.tokens = self.tokens + tmpTokens
                for _ in xrange(len(tmpTokens)):
                    self.lineNumList.append(lineNum)
            lineNum += 1

    ## Find next group command
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def findNextGroupCmd(self):
        groupCmdDict = dict({'SOLENOID_CARDS': self.procSolCards.procSection,
            'INPUT_CARDS': self.procInpCards.procSection,
            'LED_CARDS': self.procLedCards.procSection,
            'INDEXED_VARIABLES': self.procIndVars.procSection,
            'SOUND_CLIPS': self.procSound.procSection,
            'BGND_CLIPS': self.procSound.procSection,
            'VIDEO_CLIPS': self.procVideo.procSection,
            'VARIABLES': self.procVars.procSection,
            'TICK_TIME': self.procSimple.procSection,
            'FIRST_MODE': self.procSimple.procSection,
            'TIMERS': self.procTimers.procSection})
        
        while (self.currToken != len(self.tokens)):
            func = groupCmdDict.get(self.tokens[self.currToken], None)
            if (func == None):
                self.consoleObj.updateConsole("!!! Error !!! Don't understand %s token at line %d." %
                   (self.tokens[self.currToken], self.lineNumList[self.currToken]))
                return 110
            else:
                func(self)
