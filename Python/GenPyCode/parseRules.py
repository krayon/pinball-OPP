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
import procSolCards
import procInpCards
import procLedCards

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
        self._parent = parent
        
    ## Verify parameters
    #
    #  Verify passed parameters are valid.
    #
    #  @param  self          [in]   Object reference
    #  @return 0 if successful, non-zero if unsuccessful 
    def verifyParameters(self):
        # If rulesFile wasn't passed, return error code
        if not self._parent.rulesFile:
            self._parent.updateConsole("Rules file not configured.  Use -rulesFile= command line argument to set it.")
            return 100
        # If rulesFile doesn't exist, return error code
        if not os.path.isfile(self._parent.rulesFile):
            self._parent.updateConsole("Rules file %s%s%s does not exist." % (os.getcwd(), os.sep, self._parent.rulesFile))
            return 101
        # If outDir is empty, write warning that generated files will be in base directory
        if not self._parent.outDir:
            self._parent.updateConsole("!!! Warning !!! Generated files output in default directory.")
        else:
            # Check if directory exists
            if not os.path.isdir(self._parent.outDir):
                # Create the directory
                self._parent.updateConsole("Creating output directory %s%s%s does not exist." % (os.getcwd(), os.sep, self._parent.outDir))
        # Open the rules files and verify the braces match properly
        hndl = open(self._parent.rulesFile, 'r')
        if not self.verifyMatchingBrackets(hndl.read()):
            self._parent.updateConsole("!!! Error !!! Matching bracket not found.")
        # Rewind the file
        hndl.seek(0)
        self.splitIntoTokens(hndl.read())
        hndl.close()
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
                        self._parent.updateConsole("!!! Error !!! Found too many closing braces - %c...Line %d: Pos %d." % (c, lineNum, charPos))
                        return False
                    else :
                        stackTop = stack.pop()
                        openLine = lineStack.pop()
                        openPos = posStack.pop()
                        balancingBracket = pushChars[popChars.index(c)]
                        if stackTop != balancingBracket :
                            self._parent.updateConsole("!!! Error !!! Closing brace doesn't match opening brace - %c...Line %d: Pos %d." % (c, lineNum, charPos))
                            self._parent.updateConsole("Opening brace - %c...Line %d: Pos %d." % (stackTop, openLine, openPos))
                            return False
                charPos += 1
            lineNum += 1
        if len(stack):
            self._parent.updateConsole("!!! Error !!! Not enough closing braces - %d leftover." % (len(stack)))
            while len(stack) != 0:
                stackTop = stack.pop()
                openLine = lineStack.pop()
                openPos = posStack.pop()
                self._parent.updateConsole("No match for opening brace - %c...Line %d: Pos %d." % (stackTop, openLine, openPos))
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
                for index in xrange(len(tmpTokens)):
                    self.lineNumList.append(lineNum)

    ## Find next group command
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def findNextGroupCmd(self, text):
        self.currToken = 0
        groupCmdDict = dict({'SOLENOID_CARDS': procSolCards,
            'INPUT_CARDS': procInpCards,
            'LED_CARDS': procLedCards})
        
        func = groupCmdDict.get(self.tokens[self.currToken], None)
        if (func == None):
            self._parent.updateConsole("!!! Error !!! Don't understand %s token at line %d." %
               (self.tokens[self.currToken], self.lineNumList[self.currToken]))
            return 110
