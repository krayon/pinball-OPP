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
# @file    procImage.py
# @author  Hugh Spahr
# @date    1/18/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Process IMAGES section.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc Image class.
#
#  Contains functions for IMAGES section.
class ProcImage():
    loc = []

    ## Initialize the ProcImage class
    #
    #  Initialize process image class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcImage.hasImage = False
        ProcImage.name = []
        ProcImage.flagStr = []
        ProcImage.loc = []
        self.currEnum = 0
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing IMAGES section")
        if (parent.tokens[parent.currToken] != "IMAGES"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected IMAGES, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1600)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1601)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createImagesClass(parent)
        self.currEnum = 0
        while parent.currToken < closeSymb:
            errVal = self.procLine(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        
        # Write image locations
        ProcImage.outHndl.write("\n    ## Background images\n")
        ProcImage.outHndl.write("    # Indexed into using the [Images](@ref images.Images) class\n")
        ProcImage.outHndl.write("    BGND_GRAPHIC_FILES = [")
        index = 0
        for current in ProcImage.loc:
            if (index != 0):
                ProcImage.outHndl.write(", ")
                if ((index % 5) == 0):
                    ProcImage.outHndl.write("\n        ")
            ProcImage.outHndl.write(current)
            index += 1
        ProcImage.outHndl.write("]\n\n")
        parent.consoleObj.updateConsole("Done processing IMAGES.")
        ProcImage.outHndl.close()
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
        if (name in ProcImage.name):
            parent.consoleObj.updateConsole("!!! Error !!! Image name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1610)
        ProcImage.name.append(name)
        ProcChains.addName(parent.procChains, name, ProcChains.IMAGE_NAME)
        ProcImage.outHndl.write("    {0: <20} = {1}\n".format(name.upper(), self.currEnum))
        self.currEnum += 1
        
        # Copy location
        loc = parent.tokens[parent.currToken + 1]
        ProcImage.loc.append(loc)
        
        # Verify flagStr
        if not parent.helpFuncs.isValidString(parent.tokens[parent.currToken + 2], VALID_FLAGS):
            parent.consoleObj.updateConsole("!!! Error !!! Image illegal flags, read %s, at line num %d." %
               (parent.tokens[parent.currToken + 2], parent.lineNumList[parent.currToken + 2]))
            return (1611)
        ProcImage.flagStr.append(parent.tokens[parent.currToken + 2])
        
        # increment currToken
        parent.currToken += 3
        return (0)

    ## Create images.py file
    #
    # Create the images enumeration file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return None
    def createImagesClass(self, parent):
        HDR_COMMENTS = [
            "# @file    images.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief This is an enumeration of all the images.",
            "",
            "#===============================================================================",
            "",
            "## Images enumeration.",
            "#  Contains an entry for each image",
            "",
            "class Images():",
            "    def __init__(self):",
            "        pass",
            ""]

        # Open the file or create if necessary
        ProcImage.outHndl = open(parent.consoleObj.outDir + os.sep + "images.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcImage.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcImage.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcImage.outHndl.write(line + "\n")
        return (0)
        