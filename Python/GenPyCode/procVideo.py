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
# @file    procVideo.py
# @author  Hugh Spahr
# @date    7/13/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process VIDEO_CLIPS section.

#===============================================================================

## Proc Video class.
#
#  Contains functions for VIDEO_CLIPS section.
class ProcVideo():

    ## Initialize the ProcVideo class
    #
    #  Initialize process video class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcVideo.hasVideo = False
        ProcVideo.name = []
        ProcVideo.flagStr = []
        ProcVideo.loc = []
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing VIDEO_CLIPS section")
        if (parent.tokens[parent.currToken] != "VIDEO_CLIPS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected VIDEO_CLIPS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (800)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (801)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing VIDEO_CLIPS.")
        return (0)

    ## Process line
    #
    # Line consists of name and location values.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):
        VALID_FLAGS = ["MAIN_SCR", "SUB_SCR"]

        # Copy name
        name = parent.tokens[parent.currToken]
        ProcVideo.name.append(name)
        
        # Copy location
        loc = parent.tokens[parent.currToken + 1]
        ProcVideo.loc.append(loc)
        
        # Verify flagStr
        if not parent.helpFuncs.isValidString(parent.tokens[parent.currToken + 2], VALID_FLAGS):
            parent.consoleObj.updateConsole("!!! Error !!! Video illegal flags, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (810)
        ProcVideo.flagStr.append(parent.tokens[parent.currToken + 2])
        
        # increment currToken
        parent.currToken += 3
        return (0)
        