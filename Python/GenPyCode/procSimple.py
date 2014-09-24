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
# @file    procSimple.py
# @author  Hugh Spahr
# @date    9/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process simple sections including FIRST_MODE and TICK_TIME.

#===============================================================================

## Proc Simple class.
#
#  Contains functions for FIST_MODE and TICK_TIME.
class ProcSimple():

    ## Initialize the ProcVideo class
    #
    #  Initialize process video class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def init(self):
        ProcSimple.foundInit = False
        ProcSimple.tickTime = 20
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing %s section" % parent.tokens[parent.currToken])
        if (parent.tokens[parent.currToken] == "FIRST_MODE"):
            #Check if section found before
            if (ProcSimple.foundInit):
                parent.consoleObj.updateConsole("!!! Error !!! Found multiple FIRST_MODE commands, at line num %d." %
                   (parent.lineNumList[parent.currToken]))
                return (900)
            ProcSimple.foundInit = True
            #Verify parent.tokens[parent.currToken + 1] is a valid mode
            parent.consoleObj.updateConsole("FIRST_MODE not implemented")
            return (901)
        elif (parent.tokens[parent.currToken] == "TICK_TIME"):
            if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
                parent.consoleObj.updateConsole("!!! Error !!! Indexed variable numEntries, read %s, at line num %d." %
                   (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
                return (910)
            ProcSimple.tickTime = parent.helpFuncs.out
        else:
            print parent.tokens[parent.currToken]
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected FIRST_MODE or TICK_TIME, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (920)
        parent.currToken += 2
        return (0)
        