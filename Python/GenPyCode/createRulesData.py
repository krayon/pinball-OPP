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
from procChains import ProcChains

## Proc Modes class.
#
#  Contains functions for MODES section.
class CreateRulesData:
    PROC_BALLS_PER_GAME = 103
    PROC_MAX_NUM_PLYRS = 104
    PROC_LGHT_RADIUS = 105
    PROC_FEATURE_LGHT_POS = 106
    PROC_GI_LGHT_POS = 107
    PROC_SCORE_DISP_POS = 108
    PROC_SCORE_HEIGHT = 109
    PROC_SCORE_INC = 110
    PROC_NUM_LED_BRDS = 111
    PROC_INV_ADDR_LIST = 112
    PROC_INP_BRD_BIT_NAMES = 113
    PROC_INP_SCORE = 114
    PROC_INP_BRD_CFG = 115
    PROC_SOL_BRD_BIT_NAMES = 116
    PROC_SOL_SCORE = 117
    PROC_SOL_BRD_CFG = 118
    PROC_LED_BRD_BIT_NAMES = 119
    PROC_STATE_STR = 120
    PROC_INIT_BGND_IMAGE = 121
    PROC_INIT_MODE = 122
    PROC_END = 123

    ## Initialize the ProcModes class
    #
    #  Initialize process modes class
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def __init__(self):
        CreateRulesData.groupCmdDict = dict({
            CreateRulesData.PROC_BALLS_PER_GAME: self.ballsPerGame,
            CreateRulesData.PROC_MAX_NUM_PLYRS: self.maxNumPlyrs,
            CreateRulesData.PROC_LGHT_RADIUS: self.lghtRadius,
            CreateRulesData.PROC_FEATURE_LGHT_POS: self.featureLghtPos,
            CreateRulesData.PROC_GI_LGHT_POS: self.giLghtPos,
            CreateRulesData.PROC_SCORE_DISP_POS: self.scoreDispPos,
            CreateRulesData.PROC_SCORE_HEIGHT: self.scoreHeight,
            CreateRulesData.PROC_SCORE_INC: self.scoreInc,
            CreateRulesData.PROC_NUM_LED_BRDS: self.numLedBrds,
            CreateRulesData.PROC_INV_ADDR_LIST: self.invAddrList,
            CreateRulesData.PROC_INP_BRD_BIT_NAMES: self.inpBrdBitNames,
            CreateRulesData.PROC_INP_SCORE: self.inpScore,
            CreateRulesData.PROC_INP_BRD_CFG: self.inpBrdCfg,
            CreateRulesData.PROC_SOL_BRD_BIT_NAMES: self.solBrdBitNames,
            CreateRulesData.PROC_SOL_SCORE: self.solScore,
            CreateRulesData.PROC_SOL_BRD_CFG: self.solBrdCfg,
            CreateRulesData.PROC_LED_BRD_BIT_NAMES: self.ledBrdBitNames,
            CreateRulesData.PROC_STATE_STR: self.stateStr,
            CreateRulesData.PROC_INIT_BGND_IMAGE: self.bgndImage,
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
        CreateRulesData.state = CreateRulesData.PROC_BALLS_PER_GAME
        
        while CreateRulesData.state != CreateRulesData.PROC_END:
            func = CreateRulesData.groupCmdDict.get(CreateRulesData.state, None)
            if (func == None):
                parent.consoleObj.updateConsole("!!! Error !!! Create rules software failure, state = %d." %
                   (CreateRulesData.state))
                return 1800
            else:
                errVal = func()
                if errVal:
                    return(errVal)
            CreateRulesData.state += 1
        CreateRulesData.outHndl.close()
    
    ## Create balls per game
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def ballsPerGame(self):
        pass
    
    ## Create max num players
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def maxNumPlyrs(self):
        pass
    
    ## Create light radius
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def lghtRadius(self):
        pass
    
    ## Create feature light position section
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def featureLghtPos(self):
        pass
    
    ## Create GI light position section
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def giLghtPos(self):
        pass
    
    ## Create score display position section
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def scoreDispPos(self):
        pass
    
    ## Create score height
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def scoreHeight(self):
        pass
    
    ## Create score increment
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def scoreInc(self):
        pass
    
    ## Create num LED boards
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def numLedBrds(self):
        pass
    
    ## Create inventory address list
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def invAddrList(self):
        pass
    
    ## Create input board bit names
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def inpBrdBitNames(self):
        pass
    
    ## Create input scores
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def inpScore(self):
        pass
    
    ## Create input board configuration
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def inpBrdCfg(self):
        pass
    
    ## Create solenoid board bit names
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def solBrdBitNames(self):
        pass
    
    ## Create solenoid score
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def solScore(self):
        pass
    
    ## Create solenoid board configuration
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def solBrdCfg(self):
        pass
    
    ## Create LED board bit names
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def ledBrdBitNames(self):
        pass
    
    ## Create state string
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def stateStr(self):
        pass
    
    ## Create background image section
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def bgndImage(self):
        pass
    
    ## Create init mode
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Parent object for logging and tokens
    #  @return Error number if an error, or zero if no error
    def initMode(self):
        pass

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
            "import rs232Intf",
            "from rules.states import State",
            "from rules.images import Images",
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
