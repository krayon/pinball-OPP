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
    def init(self):
        ProcSound.hasSndClip = False
        ProcSound.hasBgndClip = False
        ProcSound.bgndName = []
        ProcSound.sndName = []
        ProcSound.bgndLoc = []
        ProcSound.sndLoc = []
        
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
            while parent.currToken < closeSymb:
                errVal = self.procLine(parent, False)
                if errVal:
                    parent.currToken = closeSymb
            parent.currToken += 1
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
            while parent.currToken < closeSymb:
                errVal = self.procLine(parent, True)
                if errVal:
                    parent.currToken = closeSymb
            parent.currToken += 1
            parent.consoleObj.updateConsole("Done processing BGND_CLIPS.")
        else:
            parent.consoleObj.updateConsole("!!! SW Error !!! Expected SOUND_CLIPS or BGND_CLIPS, read %s, at line num %d." %
               (parent.tokens[parent.currToken], parent.lineNumList[parent.currToken]))
            return (704)
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
            ProcSound.bgndName.append(name)
        else:
            ProcSound.sndName.append(name)
        
        # Copy location
        loc = parent.tokens[parent.currToken + 1]
        if bgndClip:
            ProcSound.bgndLoc.append(loc)
        else:
            ProcSound.sndLoc.append(loc)
        
        # increment currToken
        parent.currToken += 2
        return (0)
        