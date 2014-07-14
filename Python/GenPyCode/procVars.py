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
# @file    procVars.py
# @author  Hugh Spahr
# @date    7/13/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process VARIABLES section.

#===============================================================================

## Proc Input Cards class.
#
#  Contains functions for INPUT_CARDS section.
class ProcVars():

    ## Initialize the ProcVars class
    #
    #  Initialize input cards to zero
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def init(self):
        ProcVars.hasData = False
        ProcVars.name = []
        ProcVars.initVal = []
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        if (ProcVars.hasData):
            parent.consoleObj.updateConsole("!!! Error !!! Found multiple VARIABLES sections, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (500)
        ProcVars.hasData = True
        parent.consoleObj.updateConsole("Processing VARIABLES section")
        if (parent.tokens[parent.currToken] != "VARIABLES"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected VARIABLES, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (501)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (502)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing VARIABLES.")
        return (0)

    ## Process line
    #
    # Line consists of name and init value.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):

        name = parent.tokens[parent.currToken]
        ProcVars.name.append(name)
        
        # Verify initVal
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
            parent.consoleObj.updateConsole("!!! Error !!! Variable initVal, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (510)
        initVal = parent.helpFuncs.out
        ProcVars.initVal.append(initVal)
        
        # increment currToken
        parent.currToken += 2
        return (0)
