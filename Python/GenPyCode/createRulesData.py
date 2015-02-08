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
# @file    createRulesData.py
# @author  Hugh Spahr
# @date    1/19/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Create rulesData.py file which contains system level configurations.

#===============================================================================

import os
import time
from procSimple import ProcSimple

## Proc Modes class.
#
#  Contains functions for MODES section.
class CreateRulesData:
    PROC_SCORE_INC = 100
    PROC_INV_ADDR_LIST = 101
    PROC_INP_SCORE = 102
    PROC_SOL_SCORE = 103
    PROC_INIT_MODE = 104
    PROC_END = 105

    ## Initialize the ProcModes class
    #
    #  Initialize process modes class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        CreateRulesData.groupCmdDict = dict({
            CreateRulesData.PROC_SCORE_INC: self.scoreInc,
            CreateRulesData.PROC_INV_ADDR_LIST: self.invAddrList,
            CreateRulesData.PROC_INP_SCORE: self.inpScore,
            CreateRulesData.PROC_SOL_SCORE: self.solScore,
            CreateRulesData.PROC_INIT_MODE: self.initMode})
        
    ## Process rules data file
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return None
    def procRulesData(self, parent):
        parent.consoleObj.updateConsole("Creating rules data")
        errVal = self.createRulesDataClass(parent)
        if errVal:
            return(errVal)
        CreateRulesData.state = CreateRulesData.PROC_SCORE_INC
        
        while CreateRulesData.state != CreateRulesData.PROC_END:
            func = CreateRulesData.groupCmdDict.get(CreateRulesData.state, None)
            if (func == None):
                parent.consoleObj.updateConsole("!!! Error !!! Create rules software failure, state = %d." %
                   (CreateRulesData.state))
                return 1800
            else:
                errVal = func(parent)
                if errVal:
                    return(errVal)
            CreateRulesData.state += 1
        CreateRulesData.outHndl.close()
    
    ## Create score increment
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def scoreInc(self, parent):
        pass
    
    ## Create inventory address list
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def invAddrList(self, parent):
        if (len(ProcSimple.cardInv) == 0):
            parent.consoleObj.updateConsole("!!! Warning !!! No CARD_ORDER found in rules file.  This is probably an error"
               " or the most boring pinball machine ever.  Tough to tell.")
        else:
            # Write the initial state
            CreateRulesData.outHndl.write("    ## Board inventory list\n")
            CreateRulesData.outHndl.write("    # Used to determine number of solenoid and input boards and order in chain.\n")
            CreateRulesData.outHndl.write("    INV_ADDR_LIST = [")
            firstEntry = True
            for addr in ProcSimple.cardInv:
                if not firstEntry:
                    CreateRulesData.outHndl.write(", ")
                firstEntry = False
                CreateRulesData.outHndl.write("0x{0:02x}".format(addr))
            CreateRulesData.outHndl.write("]\n\n")
    
    ## Create input scores
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def inpScore(self, parent):
        pass
    
    ## Create solenoid score
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def solScore(self, parent):
        pass
    
    ## Create init mode
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def initMode(self, parent):
        if ProcSimple.foundInit == False:
            parent.consoleObj.updateConsole("!!! Error !!! No FIRST_MODE found in rules file, state = %d." %
               (CreateRulesData.state))
            return 1850
        # Write the initial state
        CreateRulesData.outHndl.write("    ## Initial State\n")
        CreateRulesData.outHndl.write("    INIT_MODE = State.")
        CreateRulesData.outHndl.write(ProcSimple.initMode.upper())
        CreateRulesData.outHndl.write("\n\n")

    ## Create procChains.py file
    #
    # Create the rules data class file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createRulesDataClass(self, parent):
        HDR_COMMENTS = [
            "# @file    rulesData.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief This is the rules data.  It includes sound files, general illumination",
            "# locations, and feature light locations, and string names for the debug window.",
            "",
            "#===============================================================================",
            "",
            "from states import State",
            "",
            "## Rule data class.",
            "#",
            "#  Contains most of the information for the configuration of the pinball machine",
            "class RulesData():",
            ""]
        # Open the file or create if necessary
        CreateRulesData.outHndl = open(parent.consoleObj.outDir + os.sep + "rulesData.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            CreateRulesData.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                CreateRulesData.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                CreateRulesData.outHndl.write(line + "\n")
        return (0)
