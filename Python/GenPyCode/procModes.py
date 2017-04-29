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
# @file    procModes.py
# @author  Hugh Spahr
# @date    1/16/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Process MODES section.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc Modes class.
#
#  Contains functions for MODES section.
class ProcModes:
    UNKNOWN = 0
    OPEN_PAREN = 1
    CLOSE_PAREN = 2
    COMMA = 3
    
    PROC_INIT_CHAIN = 100
    PROC_PROCESS_CHAIN = 101
    PROC_VIDEO_CHAIN = 102
    PROC_AUDIO_CHAIN = 103
    PROC_LED_CHAIN = 104
    PROC_SCORING = 105
    PROC_END_MODE = 106
    
    FIND_OPEN_PAREN = 200
    FIND_CHAIN = 201
    FIND_COMMA = 202
    FIND_END = 203

    ## Initialize the ProcModes class
    #
    #  Initialize process modes class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcModes.hasModes = False
        ProcModes.nameSet = set()
        ProcModes.name = []
        ProcModes.desc = []
        ProcModes.tokenLookup = {
            '(' : ProcModes.OPEN_PAREN,
            ')' : ProcModes.CLOSE_PAREN,
            ',' : ProcModes.COMMA }
        ProcModes.possLedChainDict = dict() 
        
    ## Add name
    #
    #  @param  self          [in]   Object reference
    #  @param  name          [in]   Name
    #  @param  nameType      [in]   Type of the name
    #  @return None
    def addName(self, name, nameType):
        ProcModes.tokenLookup[name] = nameType
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        parent.consoleObj.updateConsole("Processing MODES section")
        if (parent.tokens[parent.currToken] != "MODES"):
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected MODES, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1500)
        parent.currToken += 1
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1501)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        self.createProcChainsClass(parent)
        while parent.currToken < closeSymb:
            errVal = self.procAllModes(parent)
            if errVal:
                parent.currToken = closeSymb
        parent.currToken += 1
        ProcModes.outHndl.write("    ]\n")
        ProcModes.outHndl.close()
        
        # Create state file writing out state enumeration and strings.
        self.createStateClass(parent)
        
        parent.consoleObj.updateConsole("Done processing MODES.")
        return (0)

    ## Process all modes
    #
    # Mode consists of name, init chain, process chain, video chain, audio chain,
    # LED chain, and scoring.
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def procAllModes(self, parent):
        # Copy name
        name = parent.tokens[parent.currToken]
        if (name in ProcModes.nameSet):
            parent.consoleObj.updateConsole("!!! Error !!! Mode name found twice, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1510)
        ProcModes.nameSet.add(name)
        ProcModes.name.append(name)
        ProcChains.addName(parent.procChains, name, ProcChains.MODE_NAME)
        ProcModes.outHndl.write("        [State.{0}, ".format(name.upper()))
        parent.currToken += 1
        
        # Next symbol should be the description in quotes.
        # HRS:  This should probably support spaces inside the quotes but that will break the current
        #  tokenizer function.
        desc = parent.tokens[parent.currToken]
        if (not desc.startswith('"')) or (not desc.endswith('"')):
            parent.consoleObj.updateConsole("!!! Error !!! Descriptions strings should start and end with quotes, read %s, at line num %d." %
               (desc, parent.lineNumList[parent.currToken]))
            return (1511)
        ProcModes.desc.append(desc)
        parent.currToken += 1

        # Verify opening symbol
        if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
            parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (1512)
        closeSymb = parent.helpFuncs.findMatch(parent)
        parent.currToken += 1
        typeProc = ProcModes.PROC_INIT_CHAIN
        subState = ProcModes.FIND_OPEN_PAREN
        while parent.currToken < closeSymb:
            if parent.tokens[parent.currToken] in ProcModes.tokenLookup:
                tokenType = ProcModes.tokenLookup[parent.tokens[parent.currToken]]
            else:
                tokenType = ProcModes.UNKNOWN
            if (tokenType == ProcModes.OPEN_PAREN):
                # Opening is the beginning of a chain group
                if (subState != ProcModes.FIND_OPEN_PAREN):
                    parent.consoleObj.updateConsole("!!! Error !!! Expected opening paren, read %s, at line num %d." %
                       (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                    return (1513)
                # Find the matching close parenthesis
                if (typeProc == ProcModes.PROC_INIT_CHAIN) or (typeProc == ProcModes.PROC_PROCESS_CHAIN):
                    ProcModes.outHndl.write("[")
                closeChainList = parent.helpFuncs.findMatch(parent)
                _ = closeChainList
                parent.currToken += 1
                subState = ProcModes.FIND_CHAIN
                hasEntries = False
            elif (tokenType == ProcModes.CLOSE_PAREN):
                if not hasEntries:
                    # If this is an audio, LED, scoring, or video chain, need to add starting bracket
                    # to create an empty list
                    if (typeProc == ProcModes.PROC_AUDIO_CHAIN) or (typeProc == ProcModes.PROC_LED_CHAIN) or \
                        (typeProc == ProcModes.PROC_SCORING) or (typeProc == ProcModes.PROC_VIDEO_CHAIN):
                        ProcModes.outHndl.write("[")
                    # If there are no entries, a close parenthesis is valid
                    ProcModes.outHndl.write("]")
                else:
                    if (subState != ProcModes.FIND_COMMA) and (subState != ProcModes.FIND_END): 
                        parent.consoleObj.updateConsole("!!! Error !!! Found close parenthesis at incorrect location at line num %d." %
                           (parent.lineNumList[parent.currToken]))
                        return (1514)
                    else:
                        if (typeProc == ProcModes.PROC_INIT_CHAIN) or (typeProc == ProcModes.PROC_PROCESS_CHAIN):
                            ProcModes.outHndl.write("]")
                subState = ProcModes.FIND_OPEN_PAREN
                if (typeProc == ProcModes.PROC_SCORING):
                    ProcModes.outHndl.write(" ],\n")
                    typeProc = ProcModes.PROC_END_MODE
                else:
                    ProcModes.outHndl.write(", ")
                    typeProc += 1
                parent.currToken += 1
            elif (tokenType == ProcModes.COMMA):
                if subState != ProcModes.FIND_COMMA: 
                    parent.consoleObj.updateConsole("!!! Error !!! Comma in incorrect location at line num %d." %
                       (parent.lineNumList[parent.currToken]))
                    return (1515)
                ProcModes.outHndl.write(", ")
                parent.currToken += 1
                subState = ProcModes.FIND_CHAIN
            else:
                #This must be a name symbol
                if (ProcChains.checkNameExists(parent.procChains, parent.tokens[parent.currToken])):
                    nameType = ProcChains.getNameType(parent.procChains, parent.tokens[parent.currToken])
                    if (typeProc == ProcModes.PROC_INIT_CHAIN):
                        if (nameType != ProcChains.CHAIN_NAME):
                            parent.consoleObj.updateConsole("!!! Error !!! Expected a chain name in init chain, read %s, at line num %d." %
                               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                            return (1516)
                        ProcModes.outHndl.write("RulesFunc." + parent.tokens[parent.currToken])
                        subState = ProcModes.FIND_COMMA
                        hasEntries = True
                        parent.currToken += 1
                    elif (typeProc == ProcModes.PROC_PROCESS_CHAIN):
                        if (nameType != ProcChains.CHAIN_NAME):
                            parent.consoleObj.updateConsole("!!! Error !!! Expected a chain name in process chain, read %s, at line num %d." %
                               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                            return (1517)
                        ProcModes.outHndl.write("RulesFunc." + parent.tokens[parent.currToken])
                        subState = ProcModes.FIND_COMMA 
                        hasEntries = True
                        parent.currToken += 1
                    elif (typeProc == ProcModes.PROC_VIDEO_CHAIN):
                        if (nameType == ProcChains.VIDEO_NAME):
                            ProcModes.outHndl.write("Videos." + parent.tokens[parent.currToken].upper())
                        elif (nameType == ProcChains.VIDEO_CHAIN_NAME):
                            # HRS:  Warning, in the original code, chains were not contained within another list,
                            #   but were simply part of the procChains table.  This will need to be fixed by removing
                            #   the extra list (which would make multiple chains not work), or combining the chains
                            #   into one.
                            ProcModes.outHndl.write("VideoChains." + parent.tokens[parent.currToken])
                        elif (nameType == ProcChains.IMAGE_NAME):
                            ProcModes.outHndl.write("Images." + parent.tokens[parent.currToken].upper())
                        elif (nameType == ProcChains.IMAGE_CHAIN_NAME):
                            # HRS:  Warning, in the original code, chains were not contained within another list,
                            #   but were simply part of the procChains table.  This will need to be fixed by removing
                            #   the extra list (which would make multiple chains not work), or combining the chains
                            #   into one.
                            ProcModes.outHndl.write("ImageChains." + parent.tokens[parent.currToken])
                        else:
                            parent.consoleObj.updateConsole("!!! Error !!! Expected a video/image or video/image chain, read %s, at line num %d." %
                               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                            return (1518)
                        subState = ProcModes.FIND_COMMA 
                        hasEntries = True
                        parent.currToken += 1
                    elif (typeProc == ProcModes.PROC_AUDIO_CHAIN):
                        if (nameType == ProcChains.SOUND_NAME):
                            ProcModes.outHndl.write("Sounds." + parent.tokens[parent.currToken].upper())
                        elif (nameType == ProcChains.SOUND_CHAIN_NAME):
                            ProcModes.outHndl.write("SoundChains." + parent.tokens[parent.currToken])
                        else:
                            parent.consoleObj.updateConsole("!!! Error !!! Expected a sound or sound chain name, read %s, at line num %d." %
                               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                            return (1519)
                        subState = ProcModes.FIND_COMMA 
                        hasEntries = True
                        parent.currToken += 1
                    elif (typeProc == ProcModes.PROC_LED_CHAIN):
                        if (nameType == ProcChains.LED_CHAIN_NAME):
                            ProcModes.outHndl.write("LedChains." + parent.tokens[parent.currToken])
                        else:
                            parent.consoleObj.updateConsole("!!! Error !!! Expected an LED chain name, read %s, at line num %d." %
                               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                            return (1520)
                        subState = ProcModes.FIND_COMMA 
                        hasEntries = True
                        parent.currToken += 1
                    elif (typeProc == ProcModes.PROC_SCORING):
                        print "Not implemented"
                        parent.currToken += 1
                    else:
                        parent.consoleObj.updateConsole("!!! Error !!! Parsing error, invalid typeProc = %d, at line num %d." %
                           (typeProc, parent.lineNumList[parent.currToken]))
                        return (1521)
                else:
                    # Assume this is the name of a chain
                    ProcChains.possChainDict[parent.tokens[parent.currToken]] = parent.lineNumList[parent.currToken]
                    ProcModes.outHndl.write("RulesFunc." + parent.tokens[parent.currToken])
                    subState = ProcModes.FIND_COMMA
                    hasEntries = True
                    parent.currToken += 1
        if (typeProc != ProcModes.PROC_END_MODE):
            parent.consoleObj.updateConsole("!!! Error !!! Mode did not end properly, at line num %d." %
               (parent.lineNumList[parent.currToken]))
            return (1523)
        parent.currToken += 1
        return (0)

    ## Create procChains.py file
    #
    # Create the processing chains function file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createProcChainsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    procChains.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief These are the processing chains.  It includes initial chains and normal",
            "# processing chains that are run each time the rules thread runs.",
            "",
            "#===============================================================================",
            "",
            "from @dir.rulesFunc import RulesFunc",
            "from @dir.states import State",
            "from @dir.ledChains import LedChains",
            "from @dir.soundChains import SoundChains",
            "from @dir.imageChains import ImageChains",
            "from @dir.sounds import Sounds",
            "",
            "## Process chain lists.",
            "#",
            "#  Contains all the chains that are specific this set of pinball rules.",
            "class ProcChain():",
            "    def __init__(self):",
            "        pass",
            "",
            "    INIT_CHAIN_OFFSET = 1",
            "    NORM_CHAIN_OFFSET = 2",
            "    IMAGE_CHAIN_OFFSET = 3",
            "    SOUND_CHAIN_OFFSET = 4",
            "    LED_CHAIN_OFFSET = 5",
            "    VIDEO_CHAIN_OFFSET = 6",
            "",
            "    ## Create process chain lists.",
            "    #    - First entry is State number, only used to ease debugging",
            "    #    - Second entry is initial processing functions, called only when first entering a state",
            "    #    - Third entry are processing functions, called each time the rules thread runs",
            "    #    - Fourth entry is the image chain",
            "    #    - Fifth entry is the sound chain",
            "    #    - Sixth entry is the LED chain",
            "    #    - Seventh entry is the video chain",
            "    PROC_CHAIN = ["]
        # Open the file or create if necessary
        ProcModes.outHndl = open(parent.consoleObj.outDir + os.sep + "procChains.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcModes.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if "@dir." in line:
                line = line.replace("@dir.", parent.consoleObj.outDir + ".")
            if line.startswith("# @date"):
                ProcModes.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcModes.outHndl.write(line + "\n")
        return (0)

    ## Create states.py file
    #
    # Create the states file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def createStateClass(self, parent):
        HDR_COMMENTS = [
            "# @file    states.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief This is an enumeration of all the states.",
            "",
            "#===============================================================================",
            "",
            "## State enumeration.",
            "#  Contains an entry for each state",
            "class State():",
            "    def __init__(self):",
            "        pass",
            ""]
        # Open the file or create if necessary
        ProcModes.outHndl = open(parent.consoleObj.outDir + os.sep + "states.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcModes.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcModes.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcModes.outHndl.write(line + "\n")

        # Write the state name enumeration
        for index in xrange(len(ProcModes.name)):
            ProcModes.outHndl.write("    {0:32} = {1}\n".format(ProcModes.name[index].upper(), index))

        # Write out the state name strings
        ProcModes.outHndl.write("\n\n    ## State name strings.\n")
        ProcModes.outHndl.write("    # Indexed into using [State](@ref states.State) enumeration\n")
        ProcModes.outHndl.write("    STATE_STR = [ ")
        for index in xrange(len(ProcModes.desc)):
            if (index != 0):
                if ((index % 4) == 0):
                    ProcModes.outHndl.write(",\n        ")
                else:
                    ProcModes.outHndl.write(", ")
            ProcModes.outHndl.write(ProcModes.desc[index])
        ProcModes.outHndl.write(" ]\n\n")
        ProcModes.outHndl.close()
        return (0)
