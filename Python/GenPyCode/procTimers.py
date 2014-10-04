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
# @file    procTimers.py
# @author  Hugh Spahr
# @date    9/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process TIMERS section.

#===============================================================================

import os
import time

## Proc Timers class.
#
#  Contains functions for TIMERS section.
class ProcTimers():

    ## Initialize the ProcTimers class
    #
    #  Initialize timers
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcTimers.hasData = False
        ProcTimers.name = []
        ProcTimers.timeoutTicks = []
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        if (ProcTimers.hasData):
            parent.consoleObj.updateConsole("!!! Error !!! Found multiple TIMERS sections, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (1000)
        ProcTimers.hasData = True
        parent.consoleObj.updateConsole("Processing TIMERS section")
        if (parent.tokens[parent.currToken] != "TIMERS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected TIMERS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1001)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1002)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        self.createTimers(parent)
        parent.currToken += 1
        return (0)

    ## Process line
    #
    # Line consists of name, and timeoutTicks.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent):
        name = parent.tokens[parent.currToken]
        ProcTimers.name.append(name)
        
        # Read timeoutTicks
        if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
            parent.consoleObj.updateConsole("!!! Error !!! Timeout ticks, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
            return (1010)
        timeoutTicks = parent.helpFuncs.out
        ProcTimers.timeoutTicks.append(timeoutTicks)
        
        # increment currToken
        parent.currToken += 2
        return (0)

    ## Create timers.py file
    #
    # Create the timer names file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createTimers(self, parent):
        HDR_COMMENTS = [
            "# @file    timers.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2014, Hugh Spahr",
            "#",
            "# @brief These are the timer names.  The timer names are converted into a",
            "#    bitmask",
            "",
            "#===============================================================================",
            "",
            "## Timer bit name enumeration.",
            "#  Contains an enumeration for each timer.",
            "",
            "class Timers:",
            "    #Used to index into timeouts and grab timeout in ms",
            "    TIMEOUT_OFFSET = 1",
            "    TIMERS_PER_GROUP = 32",
            "",
            "    ## Enumeration of timers",
            "    # @Note Must be contiguous starting from 0 since used as index"]

        # Open the file or create if necessary
        outHndl = open(parent.consoleObj.outDir + os.sep + "timers.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                outHndl.write(line + "\n")
        for tmrIndex in xrange(len(ProcTimers.name)):
            outHndl.write("    {0:32} = {1:2d}\n".format(ProcTimers.name[tmrIndex].upper(),
                tmrIndex))
        outHndl.write("\n    timeouts = [\n")
        for tmrIndex in xrange(len(ProcTimers.name)):
            outHndl.write("        [{0}, {1:d}]".format(ProcTimers.name[tmrIndex].upper(),
                ProcTimers.timeoutTicks[tmrIndex]))
            if (tmrIndex < (len(ProcTimers.name) - 1)):
                outHndl.write(",\n")
            else:
                outHndl.write(" ]\n")
        outHndl.write("\n")
        outHndl.close()
        parent.consoleObj.updateConsole("Completed: timers.py file.")
        return (0)
