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
# @file    helpFuncs.py
# @author  Hugh Spahr
# @date    7/11/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Helper functions for things such as seeing if a string is an int, etc.

#===============================================================================

## Helper functions class.
#
#  Helper class does simple parsing.
class HelpFuncs:
    
    ## Is integer
    #
    # Checks to see if a string is an integer
    #
    #  @param  self          [in]   Object reference
    #  @param  text          [in]   Text to see if it is an int
    #  @return True if an integer 
    def isInt(self, text):
        try: 
            self.out = int(text)
            return True
        except ValueError:
            return False

    ## Is opening symbol
    #
    # Check to see if char is opening symbol like (, {, or [
    #
    #  @param  self          [in]   Object reference
    #  @param  char          [in]   Opening character to test
    #  @return True if an opening bracket 
    def isOpenSym(self, char):
        openChars = "({["
        if char in openChars :
            return True
        else:
            return False

    ## Find match
    #
    # Find matching symbol.  Note:  This function does not
    # do any checking.  It assumes that a matching symbol
    # is in the list
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object that contains tokens/currToken
    #  @return Index of the matching bracket 
    def findMatch(self, parent):
        stack = []
        pushChars, popChars = "({[", ")}]"
        found = False
        currToken = parent.currToken
        stack.append(parent.tokens[currToken])
        while not found:
            currToken += 1
            c = parent.tokens[currToken]
            if c in pushChars :
                stack.append(c)
            elif c in popChars :
                stackTop = stack.pop()
                if len(stack) == 0:
                    found = True
        return (currToken)            

    ## Is valid string
    #
    # Find if the string is in a list of valid strings.  Returns
    # True if a match is found and the index of the match
    #
    #  @param  self          [in]   Object reference
    #  @param  inpStr        [in]   Input string to be tested
    #  @param  validStrList  [in]   Valid string list
    #  @return True if all brackets have matches 
    def isValidString(self, inpStr, validStrList):
        index = 0
        found = False
        for currStr in validStrList:
            if not found:
                if inpStr == currStr:
                    self.out = index
                    found = True
                else:
                    index += 1
        return (found)
