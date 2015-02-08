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
# @file    procSound.py
# @author  Hugh Spahr
# @date    7/13/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Process SOUND_CLIPS and BGND_CLIPS sections.

#===============================================================================

import os
import time
from procChains import ProcChains

## Proc Sound class.
#
#  Contains functions for SOUND_CLIPS and BGND_CLIPS sections.
class ProcSound():

    ## Initialize the ProcSound class
    #
    #  Initialize process sound class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        ProcSound.hasSndClip = False
        ProcSound.hasBgndClip = False
        ProcSound.bgndName = []
        ProcSound.sndName = []
        ProcSound.bgndLoc = []
        ProcSound.sndLoc = []
        self.currEnum = 0
        
    ## Process section
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def procSection(self, parent):
        if (parent.tokens[parent.currToken] == "SOUND_CLIPS"):
            if (ProcSound.hasSndClip):
                parent.consoleObj.updateConsole("!!! Error !!! Found multiple SOUND_CLIPS sections, at line num %d." %
                   (parent.lineNumList[parent.currToken]))
                return (700)
            ProcSound.hasSndClip = True
            parent.consoleObj.updateConsole("Processing SOUND_CLIPS section")
            parent.currToken += 1
            if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
                parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (701)
            closeSymb = parent.helpFuncs.findMatch(parent)
            parent.currToken += 1
            self.createSoundsClass(parent)
            self.currEnum = 0
            while parent.currToken < closeSymb:
                errVal = self.procLine(parent, False)
                if errVal:
                    parent.currToken = closeSymb
            parent.currToken += 1
            
            # Write the file locations to the file
            ProcSound.outHndl.write("\n    ## Sound file list\n")
            ProcSound.outHndl.write("    # Indexed into using the [Sounds](@ref sounds.Sounds) class\n")
            ProcSound.outHndl.write("    SND_FILES = [")
            index = 0
            for current in ProcSound.sndLoc:
                if (index != 0):
                    ProcSound.outHndl.write(", ")
                    if ((index % 5) == 0):
                        ProcSound.outHndl.write("\n        ")
                ProcSound.outHndl.write(current)
                index += 1
            ProcSound.outHndl.write("]\n\n")
            parent.consoleObj.updateConsole("Done processing SOUND_CLIPS.")
        elif (parent.tokens[parent.currToken] == "BGND_CLIPS"):
            if (ProcSound.hasBgndClip):
                parent.consoleObj.updateConsole("!!! Error !!! Found multiple BGND_CLIPS sections, at line num %d." %
                   (parent.lineNumList[parent.currToken]))
                return (702)
            ProcSound.hasBgndClip = True
            parent.consoleObj.updateConsole("Processing BGND_CLIPS section")
            parent.currToken += 1
            if not parent.helpFuncs.isOpenSym(parent.tokens[parent.currToken]):
                parent.consoleObj.updateConsole("!!! Error !!! Expected opening symbol, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (703)
            closeSymb = parent.helpFuncs.findMatch(parent)
            parent.currToken += 1
            self.createBgndSoundsClass(parent)
            self.currEnum = 0
            while parent.currToken < closeSymb:
                errVal = self.procLine(parent, True)
                if errVal:
                    parent.currToken = closeSymb
            parent.currToken += 1
            
            # Write the file locations to the file
            ProcSound.outHndl.write("\n    ## Background sound file list\n")
            ProcSound.outHndl.write("    # Indexed into using the [BgndMusic](@ref bgndSounds.BgndMusic) class\n")
            ProcSound.outHndl.write("    BGND_MUSIC_FILES = [")
            index = 0
            for current in ProcSound.bgndLoc:
                if (index != 0):
                    ProcSound.outHndl.write(", ")
                    if ((index % 5) == 0):
                        ProcSound.outHndl.write("\n        ")
                ProcSound.outHndl.write(current)
                index += 1
            ProcSound.outHndl.write("]\n\n")
            parent.consoleObj.updateConsole("Done processing BGND_CLIPS.")
        else:
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected SOUND_CLIPS or BGND_CLIPS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (704)
        ProcSound.outHndl.close()
        return (0)

    ## Process line
    #
    # Line consists of name and location values.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @param  bgndClip      [in]   True if a background clip
    #  @return Error number if an error, or zero if no error
    def procLine(self, parent, bgndClip):

        # Copy name
        name = parent.tokens[parent.currToken]
        if bgndClip:
            if (name in ProcSound.bgndName):
                parent.consoleObj.updateConsole("!!! Error !!! Background sound name found twice, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (710)
            ProcSound.bgndName.append(name)
            ProcChains.addName(parent.procChains, name, ProcChains.BGND_SOUND_NAME)
        else:
            if (name in ProcSound.sndName):
                parent.consoleObj.updateConsole("!!! Error !!! Sound name found twice, read %s, at line num %d." %
                   (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
                return (711)
            ProcSound.sndName.append(name)
            ProcChains.addName(parent.procChains, name, ProcChains.SOUND_NAME)
        ProcSound.outHndl.write("    {0: <20} = {1}\n".format(name.upper(), self.currEnum))
        self.currEnum += 1
        
        # Copy location
        loc = parent.tokens[parent.currToken + 1]
        if bgndClip:
            ProcSound.bgndLoc.append(loc)
        else:
            ProcSound.sndLoc.append(loc)
        
        # increment currToken
        parent.currToken += 2
        return (0)

    ## Create sounds.py file
    #
    # Create the sounds enumeration file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return None
    def createSoundsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    sounds.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief This is an enumeration of all the sounds.",
            "",
            "#===============================================================================",
            "",
            "## Sounds enumeration.",
            "#  Contains an entry for each sound",
            "class Sounds():"]
    
        # Open the file or create if necessary
        ProcSound.outHndl = open(parent.consoleObj.outDir + os.sep + "sounds.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcSound.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcSound.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcSound.outHndl.write(line + "\n")
        return (0)

    ## Create bgndSounds.py file
    #
    # Create the background sounds enumeration file.  
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return None
    def createBgndSoundsClass(self, parent):
        HDR_COMMENTS = [
            "# @file    bgndSounds.py",
            "# @author  AutoGenerated",
            "# @date    ",
            "#",
            "# @note    Open Pinball Project",
            "# @note    Copyright 2015, Hugh Spahr",
            "#",
            "# @brief This is an enumeration of all the background sounds.",
            "",
            "#===============================================================================",
            "",
            "## Background sounds enumeration.",
            "#  Contains an entry for each background sound",
            "class BgndMusic():"]
    
        # Open the file or create if necessary
        ProcSound.outHndl = open(parent.consoleObj.outDir + os.sep + "bgndSounds.py", 'w+')
        stdHdrHndl = open("stdHdr.txt", 'r')
        for line in stdHdrHndl:
            ProcSound.outHndl.write(line)
        stdHdrHndl.close()
        for line in HDR_COMMENTS:
            if line.startswith("# @date"):
                ProcSound.outHndl.write(line + time.strftime("%m/%d/%Y") + "\n")
            else:
                ProcSound.outHndl.write(line + "\n")
        return (0)
        