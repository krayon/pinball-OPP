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
# @file    procVidChains.py
# @author  Hugh Spahr
# @date    1/17/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Process VIDEO_CHAINS section.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc Video Chains class.
#
#  Contains functions for VIDEO_CHAINS section.
class ProcVidChains:
    UNKNOWN = 0
    WAIT_COMMAND = 1
    REPEAT_COMMAND = 2
    COMMA = 3
    
    PROC_VIDEO = 100
    PROC_COMMAND = 101
    PROC_DONE_CHAIN = 102

    ## Initialize the ProcVidChains class
    #
    #  Initialize process video chains class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcVidChains.nameSet = set()
        ProcVidChains.tokenLookup = {
            ',' : ProcVidChains.COMMA,
            'WAIT' : ProcVidChains.WAIT_COMMAND,
            'REPEAT' : ProcVidChains.REPEAT_COMMAND }
        
    ## Add name
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @param  nameType      [in]   Type of the name
    #  @return None
    def addName(self, name, nameType):
        ProcVidChains.tokenLookup[name] = nameType
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing VIDEO_CHAINS section")
        if (parent.tokens[parent.currToken] != "VIDEO_CHAINS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected VIDEO_CHAINS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1400)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1401)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createVidChainsClass(parent)
        while parent.currToken < closeSymb:
            errVal = self.procAllChains(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing VIDEO_CHAINS.")
        ProcVidChains.outHndl.close()
        return (0)

    ## Process all chains
    #
    # Chain consists of sound then command repeated until chain ends or REPEAT command is read.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procAllChains(self, parent):
        # Copy name
        name = parent.tokens[parent.currToken]
        if (name in ProcVidChains.nameSet):
            parent.consoleObj.updateConsole("!!! Error !!! Name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1410)
        ProcVidChains.nameSet.add(name)
        ProcChains.addName(parent.procChains, name, ProcChains.VIDEO_CHAIN_NAME)
        ProcVidChains.outHndl.write("    ## Video Chain {0}\n".format(name))
        ProcVidChains.outHndl.write("    #    - Groups have video name then WAIT command\n")
        ProcVidChains.outHndl.write("    #    - Chain ends with REPEAT if desired\n")
        ProcVidChains.outHndl.write("    {0} = [\n".format(name))

        # Verify opening symbol
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1411)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        typeProc = ProcVidChains.PROC_VIDEO
        while parent.currToken < closeSymb:
            if parent.tokens[parent.currToken] in ProcVidChains.tokenLookup:
                tokenType = ProcVidChains.tokenLookup[parent.tokens[parent.currToken]]
            else:
                tokenType = ProcVidChains.UNKNOWN
            if tokenType == ProcVidChains.WAIT_COMMAND:
                if typeProc != ProcVidChains.PROC_COMMAND: 
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT command in video chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1412)
                # Next token should be wait timeout (ms) 
                if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT parameter should be integer, read %s, at line num %d." %
                       (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
                    return (1413)
                ProcVidChains.outHndl.write(" WAIT, " + parent.tokens[parent.currToken + 1] + "],\n")
                parent.currToken += 2
                # Next token must be a comma
                if (ProcVidChains.tokenLookup[parent.tokens[parent.currToken]] != ProcVidChains.COMMA):
                    parent.consoleObj.updateConsole("!!! Error !!! Comma missing after wait command, found %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1414)
                parent.currToken += 1
                typeProc = ProcVidChains.PROC_VIDEO
            elif tokenType == ProcVidChains.REPEAT_COMMAND:
                if (typeProc == ProcVidChains.PROC_VIDEO):
                    ProcVidChains.outHndl.write("        [0, ")
                elif (typeProc == ProcVidChains.PROC_COMMAND):
                    pass
                else:  
                    parent.consoleObj.updateConsole("!!! Error !!! REPEAT command in video chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1415)
                ProcVidChains.outHndl.write("REPEAT, 0] ]\n\n")
                typeProc = ProcVidChains.PROC_DONE_CHAIN
                parent.currToken += 1
            elif tokenType == ProcVidChains.COMMA:
                if (typeProc == ProcVidChains.PROC_VIDEO) or (typeProc == ProcVidChains.PROC_COMMAND):
                    # No processing necessary, next sound will start the line
                    parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Unexpected comma at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1416)
            else:
                #This must be a video name
                if (ProcChains.checkNameExists(parent.procChains, parent.tokens[parent.currToken])):
                    if (ProcChains.getNameType(parent.procChains, parent.tokens[parent.currToken]) != ProcChains.VIDEO_NAME):
                        parent.consoleObj.updateConsole("!!! Error !!! Symbol %s should only be a video name, at line num %d." %
                           (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                        return (1417)
                    else:
                        if typeProc == ProcVidChains.PROC_VIDEO:
                            ProcVidChains.outHndl.write("        [Videos.{0}, ".format(parent.tokens[parent.currToken]))
                            typeProc = ProcVidChains.PROC_COMMAND
                            parent.currToken += 1
                        elif typeProc == ProcVidChains.PROC_COMMAND:
                            # Two or more sounds back to back, put a wait of 0 between them
                            ProcVidChains.outHndl.write("WAIT, 0],\n        [Videos.{0}, ".format(parent.tokens[parent.currToken]))
                            parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1418)
        if (typeProc != ProcVidChains.PROC_DONE_CHAIN):
            parent.consoleObj.updateConsole("!!! Error !!! Video chain did not end properly, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (1419)
        parent.currToken += 1
        return (0)

    ## Create videoChains.py file
    #
    # Create the video chains function file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createVidChainsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    videoChains.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief These are the sound chains.  It includes chains to automatically play",
            "#    a string of videos with delays in between.",
            "",
            "#===============================================================================",
            "",
            "from videos import Videos",
            "",
            "## Video chains class.",
            "#",
            "#  Contains all the video chains that are specific to this set of pinball rules.",
            "#",
            "#  Each video chain group contains the video to play, the command, and the",
            "#  parameter to the command.",
            "",
            "class VideoChains():"
            "    # Video chain commands",
            "    WAIT = 0",
            "    REPEAT = 1",
            "    END_CHAIN = 2",
            "",
            "    VIDEO_OFFSET = 0",
            "    CH_CMD_OFFSET = 1",
            "    PARAM_OFFSET = 2",
            ""]
    
        # Open the file or create if necessary
        ProcVidChains.outHndl = open(parent.consoleObj.outDir + os.sep + "videoChains.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcVidChains.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcVidChains.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcVidChains.outHndl.write(line + "\n")
        return (0)
