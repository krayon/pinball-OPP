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
# @file    procImageChains.py
# @author  Hugh Spahr
# @date    1/18/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Process IMAGE_CHAINS section.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc Image Chains class.
#
#  Contains functions for SOUND_CHAINS section.
class ProcImageChains:
    UNKNOWN = 0
    WAIT_COMMAND = 1
    REPEAT_COMMAND = 2
    COMMA = 3
    
    PROC_IMAGE = 100
    PROC_COMMAND = 101
    PROC_DONE_CHAIN = 102

    ## Initialize the ProcImageChains class
    #
    #  Initialize process image chains class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcImageChains.nameSet = set()
        ProcImageChains.tokenLookup = {
            ',' : ProcImageChains.COMMA,
            'WAIT' : ProcImageChains.WAIT_COMMAND,
            'REPEAT' : ProcImageChains.REPEAT_COMMAND }
        
    ## Add name
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @param  nameType      [in]   Type of the name
    #  @return None
    def addName(self, name, nameType):
        ProcImageChains.tokenLookup[name] = nameType
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing IMAGE_CHAINS section")
        if (parent.tokens[parent.currToken] != "IMAGE_CHAINS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected IMAGE_CHAINS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1700)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1701)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createImageChainsClass(parent)
        while parent.currToken < closeSymb:
            errVal = self.procAllChains(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing IMAGE_CHAINS.")
        ProcImageChains.outHndl.close()
        return (0)

    ## Process all chains
    #
    # Chain consists of image then command repeated until chain ends or REPEAT command is read.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procAllChains(self, parent):
        # Copy name
        name = parent.tokens[parent.currToken]
        if (name in ProcImageChains.nameSet):
            parent.consoleObj.updateConsole("!!! Error !!! Name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1710)
        ProcImageChains.nameSet.add(name)
        ProcChains.addName(parent.procChains, name, ProcChains.IMAGE_CHAIN_NAME)
        ProcImageChains.outHndl.write("    ## Image Chain {0}\n".format(name))
        ProcImageChains.outHndl.write("    #    - Groups have image name then WAIT command\n")
        ProcImageChains.outHndl.write("    #    - Chain ends with REPEAT if desired\n")
        ProcImageChains.outHndl.write("    {0} = [\n".format(name))

        # Verify opening symbol
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1711)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        typeProc = ProcImageChains.PROC_IMAGE
        while parent.currToken < closeSymb:
            if parent.tokens[parent.currToken] in ProcImageChains.tokenLookup:
                tokenType = ProcImageChains.tokenLookup[parent.tokens[parent.currToken]]
            else:
                tokenType = ProcImageChains.UNKNOWN
            if tokenType == ProcImageChains.WAIT_COMMAND:
                if typeProc != ProcImageChains.PROC_COMMAND: 
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT command in image chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1712)
                # Next token should be wait timeout (ms) 
                if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT parameter should be integer, read %s, at line num %d." %
                       (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
                    return (1713)
                ProcImageChains.outHndl.write(" WAIT, " + parent.tokens[parent.currToken + 1] + "],\n")
                parent.currToken += 2
                # Next token must be a comma
                if (ProcImageChains.tokenLookup[parent.tokens[parent.currToken]] != ProcImageChains.COMMA):
                    parent.consoleObj.updateConsole("!!! Error !!! Comma missing after wait command, found %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1714)
                parent.currToken += 1
                typeProc = ProcImageChains.PROC_IMAGE
            elif tokenType == ProcImageChains.REPEAT_COMMAND:
                if (typeProc == ProcImageChains.PROC_IMAGE):
                    ProcImageChains.outHndl.write("        [0, ")
                elif (typeProc == ProcImageChains.PROC_COMMAND):
                    pass
                else:  
                    parent.consoleObj.updateConsole("!!! Error !!! REPEAT command in image chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1715)
                ProcImageChains.outHndl.write("REPEAT, 0] ]\n\n")
                typeProc = ProcImageChains.PROC_DONE_CHAIN
                parent.currToken += 1
            elif tokenType == ProcImageChains.COMMA:
                if (typeProc == ProcImageChains.PROC_IMAGE) or (typeProc == ProcImageChains.PROC_COMMAND):
                    # No processing necessary, next sound will start the line
                    parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Unexpected comma at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1716)
            else:
                #This must be a sound name
                if (ProcChains.checkNameExists(parent.procChains, parent.tokens[parent.currToken])):
                    if (ProcChains.getNameType(parent.procChains, parent.tokens[parent.currToken]) != ProcChains.IMAGE_NAME):
                        parent.consoleObj.updateConsole("!!! Error !!! Symbol %s should only be a sound name, at line num %d." %
                           (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                        return (1717)
                    else:
                        if typeProc == ProcImageChains.PROC_IMAGE:
                            ProcImageChains.outHndl.write("        [Images.{0}, ".format(parent.tokens[parent.currToken].upper()))
                            typeProc = ProcImageChains.PROC_COMMAND
                            parent.currToken += 1
                        elif typeProc == ProcImageChains.PROC_COMMAND:
                            # Two or more sounds back to back, put a wait of 0 between them
                            ProcImageChains.outHndl.write("WAIT, 0],\n        [Images.{0}, ".format(parent.tokens[parent.currToken].upper()))
                            parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1718)
        if (typeProc != ProcImageChains.PROC_DONE_CHAIN):
            parent.consoleObj.updateConsole("!!! Error !!! Image chain did not end properly, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (1719)
        parent.currToken += 1
        return (0)

    ## Create imageChains.py file
    #
    # Create the image chains function file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createImageChainsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    imageChains.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief These are the image chains.  It includes chains to automatically play",
            "#    a set of images with delays in between.",
            "",
            "#===============================================================================",
            "",
            "from images import Images",
            "",
            "## Image chains class.",
            "#",
            "#  Contains all the image chains that are specific to this set of pinball rules.",
            "#",
            "#  Each image chain group contains the image to play, the command, and the",
            "#  parameter to the command.",
            "",
            "class ImageChains():"
            "    # Image chain commands",
            "    WAIT = 0",
            "    REPEAT = 1",
            "    END_CHAIN = 2",
            "",
            "    IMAGE_OFFSET = 0",
            "    CH_CMD_OFFSET = 1",
            "    PARAM_OFFSET = 2",
            ""]
    
        # Open the file or create if necessary
        ProcImageChains.outHndl = open(parent.consoleObj.outDir + os.sep + "imageChains.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcImageChains.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcImageChains.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcImageChains.outHndl.write(line + "\n")
        return (0)
