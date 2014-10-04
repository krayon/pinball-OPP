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
# @file    procIndVars.py
# @author  Hugh Spahr
# @date    7/13/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process INDEXED_VARIABLES section.

#===============================================================================

## Proc Indexed Variables class.
#
#  Contains functions for INDEXED_VARIABLES section.
class ProcIndVars():

    ## Initialize the ProcIndVars class
    #
    #  Initialize process indexed variables class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcIndVars.hasData = False
        ProcIndVars.name = []
        ProcIndVars.numEntries = []
        ProcIndVars.initVals = []
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        if (ProcIndVars.hasData):
            parent.consoleObj.updateConsole("!!! Error !!! Found multiple INDEXED_VARIABLES sections, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (600)
        ProcIndVars.hasData = True
        parent.consoleObj.updateConsole("Processing INDEXED_VARIABLES section")
        if (parent.tokens[parent.currToken] != "INDEXED_VARIABLES"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected INDEXED_VARIABLES, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (601)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (602)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing INDEXED_VARIABLES.")
        return (0)

    ## Process line
    #
    # Line consists of name, numEntries and init values.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):

        name = parent.tokens[parent.currToken]
        ProcIndVars.name.append(name)
        
        # Verify numEntries
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
            parent.consoleObj.updateConsole("!!! Error !!! Indexed variable numEntries, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (610)
        numEntries = parent.helpFuncs.out
        if (numEntries <= 0):
            parent.consoleObj.updateConsole("!!! Error !!! Illegal indexed variable numEntries, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (611)
        ProcIndVars.numEntries.append(numEntries)
        parent.currToken += 2
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected indexed variable init opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (612)
        closeSymb = parent.helpFuncs.findMatch(parent)
        if (closeSymb != (parent.currToken + numEntries + 1)):
            parent.consoleObj.updateConsole("!!! Error !!! Index variable, wrong num init values, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (613)
        initVals = []
        parent.currToken += 1
        for _ in xrange(numEntries):
            # Verify initValues
            if not parent.helpFuncs.isInt(parent.tokens[parent.currToken]):
                parent.consoleObj.updateConsole("!!! Error !!! Indexed variable initVal, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (614)
            initVals.append(parent.helpFuncs.out)
            parent.currToken += 1
        ProcIndVars.initVals.append(initVals)
        
        # increment currToken
        parent.currToken += 1
        return (0)
        