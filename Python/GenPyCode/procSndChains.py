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
# @file    procSndChains.py
# @author  Hugh Spahr
# @date    1/17/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Process SOUND_CHAINS section.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc Sound Chains class.
#
#  Contains functions for SOUND_CHAINS section.
class ProcSndChains:
    UNKNOWN = 0
    WAIT_COMMAND = 1
    REPEAT_COMMAND = 2
    COMMA = 3
    
    PROC_SOUND = 100
    PROC_COMMAND = 101
    PROC_DONE_CHAIN = 102

    ## Initialize the ProcSndChains class
    #
    #  Initialize process sound chains class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcSndChains.nameSet = set()
        ProcSndChains.tokenLookup = {
            ',' : ProcSndChains.COMMA,
            'WAIT' : ProcSndChains.WAIT_COMMAND,
            'REPEAT' : ProcSndChains.REPEAT_COMMAND }
        
    ## Add name
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @param  nameType      [in]   Type of the name
    #  @return None
    def addName(self, name, nameType):
        ProcSndChains.tokenLookup[name] = nameType
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing SOUND_CHAINS section")
        if (parent.tokens[parent.currToken] != "SOUND_CHAINS"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected SOUND_CHAINS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1300)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1301)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createSndChainsClass(parent)
        while parent.currToken < closeSymb:
            errVal = self.procAllChains(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        parent.consoleObj.updateConsole("Done processing SOUND_CHAINS.")
        ProcSndChains.outHndl.close()
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
        if (name in ProcSndChains.nameSet):
            parent.consoleObj.updateConsole("!!! Error !!! Name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1310)
        ProcSndChains.nameSet.add(name)
        ProcChains.addName(parent.procChains, name, ProcChains.SOUND_CHAIN_NAME)
        ProcSndChains.outHndl.write("    ## Sound Chain {0}\n".format(name))
        ProcSndChains.outHndl.write("    #    - Groups have sound name then WAIT command\n")
        ProcSndChains.outHndl.write("    #    - Chain ends with REPEAT if desired\n")
        ProcSndChains.outHndl.write("    {0} = [\n".format(name))

        # Verify opening symbol
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1311)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        typeProc = ProcSndChains.PROC_SOUND
        while parent.currToken < closeSymb:
            if parent.tokens[parent.currToken] in ProcSndChains.tokenLookup:
                tokenType = ProcSndChains.tokenLookup[parent.tokens[parent.currToken]]
            else:
                tokenType = ProcSndChains.UNKNOWN
            if tokenType == ProcSndChains.WAIT_COMMAND:
                if typeProc != ProcSndChains.PROC_COMMAND: 
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT command in sound chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1312)
                # Next token should be wait timeout (ms) 
                if not parent.helpFuncs.isInt(parent.tokens[parent.currToken + 1]):
                    parent.consoleObj.updateConsole("!!! Error !!! WAIT parameter should be integer, read %s, at line num %d." %
                       (parent.tokens[parent.currToken + 1], parent.lineNumList[parent.currToken + 1]))
                    return (1313)
                ProcSndChains.outHndl.write(" WAIT, " + parent.tokens[parent.currToken + 1] + "],\n")
                parent.currToken += 2
                # Next token must be a comma
                if (ProcSndChains.tokenLookup[parent.tokens[parent.currToken]] != ProcSndChains.COMMA):
                    parent.consoleObj.updateConsole("!!! Error !!! Comma missing after wait command, found %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1314)
                parent.currToken += 1
                typeProc = ProcSndChains.PROC_SOUND
            elif tokenType == ProcSndChains.REPEAT_COMMAND:
                if (typeProc == ProcSndChains.PROC_SOUND):
                    ProcSndChains.outHndl.write("        [0, ")
                elif (typeProc == ProcSndChains.PROC_COMMAND):
                    pass
                else:  
                    parent.consoleObj.updateConsole("!!! Error !!! REPEAT command in sound chain in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1315)
                ProcSndChains.outHndl.write("REPEAT, 0] ]\n\n")
                typeProc = ProcSndChains.PROC_DONE_CHAIN
                parent.currToken += 1
            elif tokenType == ProcSndChains.COMMA:
                if (typeProc == ProcSndChains.PROC_SOUND) or (typeProc == ProcSndChains.PROC_COMMAND):
                    # No processing necessary, next sound will start the line
                    parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Unexpected comma at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1316)
            else:
                #This must be a sound name
                if (ProcChains.checkNameExists(parent.procChains, parent.tokens[parent.currToken])):
                    if (ProcChains.getNameType(parent.procChains, parent.tokens[parent.currToken]) != ProcChains.SOUND_NAME):
                        parent.consoleObj.updateConsole("!!! Error !!! Symbol %s should only be a sound name, at line num %d." %
                           (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                        return (1317)
                    else:
                        if typeProc == ProcSndChains.PROC_SOUND:
                            ProcSndChains.outHndl.write("        [Sounds.{0}, ".format(parent.tokens[parent.currToken].upper()))
                            typeProc = ProcSndChains.PROC_COMMAND
                            parent.currToken += 1
                        elif typeProc == ProcSndChains.PROC_COMMAND:
                            # Two or more sounds back to back, put a wait of 0 between them
                            ProcSndChains.outHndl.write("WAIT, 0],\n        [Sounds.{0}, ".format(parent.tokens[parent.currToken].upper()))
                            parent.currToken += 1
                else:
                    parent.consoleObj.updateConsole("!!! Error !!! Can't understand symbol, read %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1318)
        if (typeProc != ProcSndChains.PROC_DONE_CHAIN):
            parent.consoleObj.updateConsole("!!! Error !!! Sound chain did not end properly, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (1319)
        parent.currToken += 1
        return (0)

    ## Create soundChains.py file
    #
    # Create the sound chains function file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createSndChainsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    soundChains.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief These are the sound chains.  It includes chains to automatically play",
            "#    a string of sounds with delays in between.",
            "",
            "#===============================================================================",
            "",
            "from sounds import Sounds",
            "",
            "## Sound chains class.",
            "#",
            "#  Contains all the sound chains that are specific to this set of pinball rules.",
            "#",
            "#  Each sound chain group contains the sound to play, the command, and the",
            "#  parameter to the command.",
            "",
            "class SoundChains():    # Sound chain commands",
            "    def __init__(self):",
            "        pass",
            "",
            "    # Sound chain commands",
            "    WAIT = 0",
            "    REPEAT = 1",
            "    END_CHAIN = 2",
            "",
            "    SOUND_OFFSET = 0",
            "    CH_CMD_OFFSET = 1",
            "    PARAM_OFFSET = 2",
            ""]
    
        # Open the file or create if necessary
        ProcSndChains.outHndl = open(parent.consoleObj.outDir + os.sep + "soundChains.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcSndChains.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcSndChains.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcSndChains.outHndl.write(line + "\n")
        return (0)
