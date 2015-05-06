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
# @file    gameData.py
# @author  Hugh Spahr
# @date    1/18/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the game data.  It includes data about the current state of the game.

#===============================================================================

from hwobjs.inpBrd import InpBrd
from hwobjs.solBrd import SolBrd
from hwobjs.ledBrd import LedBrd
from comms.commIntf import CommsState
import rs232Intf
from dispConstIntf import DispConst
from stdFuncs import StdFuncs

## Game data class.
#
#  Keeps the current state of the pinball machine.
class GameData():
    credits = 0
    creditsInRow = 0
    partCreditsNum = 0
    extraCredit = 5
    partCreditsDenom = 2
    
    # Used to change displayed values
    creditBallNumDisp = 0
    currPlyrDisp = 0
    score = [0, 0, 0, 0]
    
    prevGameMode = 0xffffffff
    gameMode = 0
    commState = CommsState.COMM_INIT
    ballNum = 0
    currPlayer = 0
    numPlayers = 0
    bgndImage = 0
    scoreLvl = 0
    numSpinners = 0
    kick_retries = 0
    scoring = False
    
    # Current display values
    currDisp = [0, 0, 0, 0, 0, 0]
    blankDisp = [True, True, True, True, True, True]
    updDisp = 0
    
    debug = False
    inpBrd = InpBrd()
    solBrd = SolBrd()
    ledBrd = LedBrd()
    
    #Filled out if debug frame is created
    tkInpBrd = []
    tkSolBrd = []
    tkLedBrd = []
    
    #Comm obj
    commThread = 0
    
    #Used for switch input processing.  Logical OR of debug data (simSwitchBits)
    #  and Comms data (switchInpData, switchSolData)
    currInpStatus = []
    currSolStatus = []
    
    #Timer information
    expiredTimers = []
    runningTimers = []
    timerCnt = []
    reportExpOnce = []

    #LED Chain 
    ledChain = []
    newLedChain = False
    
    #Sound Chain 
    soundChain = []
    newSoundChain = False
    
    #Image Chain 
    imageChain = []
    newImageChain = False
    
    #Bgnd music
    prevBgndSound = 0xffffffff
    bgndSound = 0xffffffff
    
    #Interface objects
    StdFuncs = None
    RulesData = None
    BgndMusic = None
    GameConst = None
    ImageChains = None
    Images = None
    InpBitNames = None
    LedBitNames = None
    LedChains = None
    ProcChain = None
    RulesFunc = None
    SolBitNames = None
    SoundChains = None
    Sounds = None
    States = None
    Timers = None
    
    ## The constructor.
    def __init__(self, rulesDir):
        GameData.rulesDir = rulesDir
        GameData.StdFuncs = StdFuncs(GameData)
        
        # HRS:  Go back and make sure I'm not missing some like video chains
        modules = [rulesDir + ".rulesData", rulesDir + ".bgndSounds", rulesDir + ".gameConst", rulesDir + ".imageChains",
                   rulesDir + ".images", rulesDir + ".inpBitNames", rulesDir + ".ledBitNames", rulesDir + ".ledChains",
                   rulesDir + ".procChains", rulesDir + ".rulesFunc", rulesDir + ".solBitNames", rulesDir + ".soundChains",
                   rulesDir + ".sounds", rulesDir + ".states", rulesDir + ".timers"]
        for currMod in modules:
            failImport = False
            try:
                importedMode = __import__(currMod)
            except ImportError:
                failImport = True
            if (currMod.endswith("rulesData")):
                if (not failImport):
                    GameData.RulesData = importedMode.rulesData.RulesData
            elif (currMod.endswith("bgndSounds")):    
                if (not failImport):
                    GameData.BgndMusic = importedMode.bgndSounds.BgndMusic
            elif (currMod.endswith("gameConst")):    
                if (not failImport):
                    GameData.GameConst = importedMode.gameConst.GameConst
            elif (currMod.endswith("imageChains")):    
                if (not failImport):
                    GameData.ImageChains = importedMode.imageChains.ImageChains
            elif (currMod.endswith("images")):    
                if (not failImport):
                    GameData.Images = importedMode.images.Images
            elif (currMod.endswith("inpBitNames")):    
                if (not failImport):
                    GameData.InpBitNames = importedMode.inpBitNames.InpBitNames
            elif (currMod.endswith("ledBitNames")):    
                if (not failImport):
                    GameData.LedBitNames = importedMode.ledBitNames.LedBitNames
            elif (currMod.endswith("ledChains")):    
                if (not failImport):
                    GameData.LedChains = importedMode.ledChains.LedChains
            elif (currMod.endswith("procChains")):    
                if (not failImport):
                    GameData.ProcChain = importedMode.procChains.ProcChain
            elif (currMod.endswith("rulesFunc")):    
                if (not failImport):
                    GameData.RulesFunc = importedMode.rulesFunc.RulesFunc(GameData)
            elif (currMod.endswith("solBitNames")):    
                if (not failImport):
                    GameData.SolBitNames = importedMode.solBitNames.SolBitNames
            elif (currMod.endswith("soundChains")):    
                if (not failImport):
                    GameData.SoundChains = importedMode.soundChains.SoundChains
            elif (currMod.endswith("sounds")):    
                if (not failImport):
                    GameData.Sounds = importedMode.sounds.Sounds
            elif (currMod.endswith("states")):    
                if (not failImport):
                    GameData.States = importedMode.states.State
            elif (currMod.endswith("timers")):    
                if (not failImport):
                    GameData.Timers = importedMode.timers.Timers
            
        GameData.gameMode = GameData.RulesData.INIT_MODE

    ## Initialize board objects
    #
    #  Initialize the boards based on
    #  [INV_ADDR_LIST](@ref rules.rulesData.RulesData.INV_ADDR_LIST) and
    #  [NUM_LED_BRDS](@ref rules.rulesData.LedBitNames.NUM_LED_BRDS).
    #
    #  @param  self          [in]   Object reference
    #  @return Can return CMD_OK if good, or CANT_OPEN_COM or error codes
    #     from [getInventory](@ref comms.commHelp.getInventory).
    def init_brd_objs(self):
        for i in xrange(len(GameData.RulesData.INV_ADDR_LIST)):
            if ((GameData.RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_INP_CARD)): 
                InpBrd.add_card(self.inpBrd, GameData)
                GameData.currInpStatus.append(0)
            elif ((GameData.RulesData.INV_ADDR_LIST[i] & (ord)(rs232Intf.CARD_ID_TYPE_MASK)) == (ord)(rs232Intf.CARD_ID_SOL_CARD)):
                SolBrd.add_card(self.solBrd, GameData)
                GameData.currSolStatus.append(0)
        for i in xrange(GameData.LedBitNames.NUM_LED_BRDS):
            LedBrd.add_card(self.ledBrd)
