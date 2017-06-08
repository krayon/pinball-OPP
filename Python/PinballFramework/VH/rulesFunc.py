#!/usr/bin/env python
#
# Warning - This is an auto-generated file.  All changes to this file will
# be overwritten next time GenPyCode.py is re-run.  Do not change this file
# unless you want to start hand editing the files.
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
# @file    rulesFunc.py
# @author  AutoGenerated
# @date    04/27/2017
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief These are the rules function names.  The rules functions can call
#    other rules functions, or be called in chains.  The generator saves
#    the file as rulesFunc.py.gen.  The pinball framework uses rulesFunc.py.
#    This insures a newly generated file won't accidentally overwrite a
#    user modified rules file.

#===============================================================================

from VH.inpBitNames import InpBitNames
from VH.solBitNames import SolBitNames
from VH.ledBitNames import LedBitNames
from VH.timers import Timers
from VH.rulesData import RulesData
from VH.sounds import Sounds
from VH.bgndSounds import BgndMusic
from VH.states import State
from VH.images import Images
from dispConstIntf import DispConst
from VH.customFunc import CustomFunc

## Rules functions class.
#  Contains all the rules that are specific this this set of pinball rules.

class RulesFunc:
    LEFT_FLIPPER = 0x01
    RIGHT_FLIPPER = 0x02
    prev_flipper = 0

    WAIT_FOR_BALL_SERVE = 0
    WAIT_FOR_RUNNIN_CLIP_FINISH = 1
    init_state = WAIT_FOR_BALL_SERVE
    
    ## Initialize rulesFuncs class
    #
    #  Initialize rules functions class
    #
    #  @param  self          [in]   Object reference
    #  @param  gameData      [in]   Object reference
    #  @return None
    def __init__(self, gameData):
        RulesFunc.GameData = gameData
        RulesFunc.CustomFunc = CustomFunc(gameData)

    ## Function Proc_Tilt
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Tilt(self):
        pass

    ## Function Choose_Random_Singer
    #
    #  Choose a random singer if one hasn't been selected
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Choose_Random_Singer(self):
        if (RulesFunc.CustomFunc.singer == 0):
            if (random.randint(0, 1) == 0):
                RulesFunc.CustomFunc.Singer_David()
            else:
                RulesFunc.CustomFunc.Singer_Sammy()
    
    ## Function Proc_Select_Singer
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Select_Singer(self):
        lftFlip = RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_LFT_FLIPPER)
        rghtFlip = RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_RGHT_FLIPPER)
        
        if (rghtFlip):
            RulesFunc.prev_flipper |= self.RIGHT_FLIPPER
        if (lftFlip):
            RulesFunc.prev_flipper |= self.LEFT_FLIPPER
        # Selection is made on release of flipper button
        if ((not rghtFlip) and (not lftFlip) and (RulesFunc.prev_flipper != 0)):
            if (RulesFunc.prev_flipper & (self.RIGHT_FLIPPER | self.LEFT_FLIPPER) == \
                (self.RIGHT_FLIPPER | self.LEFT_FLIPPER)):
                
                # If singer hasn't been chosen, pick randomly
                self.Choose_Random_Singer()
                
                # Move to start ball
                RulesFunc.GameData.gameMode = State.STATE_STARTBALL
            else:
                if (RulesFunc.prev_flipper & self.RIGHT_FLIPPER):
                    # Singer is Sammy Hagar
                    RulesFunc.CustomFunc.Singer_Sammy()
                if (RulesFunc.prev_flipper & self.LEFT_FLIPPER):
                    # Singer is David Lee Roth
                    RulesFunc.CustomFunc.Singer_David()
            RulesFunc.prev_flipper = 0
            
        # If general timer times out, automatically select a singer    
        if (RulesFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_GENERAL_TIMER)):
            # If singer hasn't been chosen, pick randomly
            self.Choose_Random_Singer()
            
            # Move to start ball
            RulesFunc.GameData.gameMode = State.STATE_STARTBALL

    ## Function Proc_Inlane
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Inlane(self):
        pass

    ## Function Proc_Targets
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Targets(self):
        pass

    ## Function Proc_Kickout_Hole
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Kickout_Hole(self):
        pass

    ## Function Proc_Ball_Drain
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Ball_Drain(self):
        pass

    ## Function Proc_Tilt_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Tilt_Init(self):
        pass

    ## Function Proc_Tilt_State
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Tilt_State(self):
        pass

    ## Function Proc_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Init(self):
        RulesFunc.GameData.StdFuncs.Restore_Input_Cfg()
        RulesFunc.GameData.gameMode = State.STATE_ATTRACT

    ## Function Init_Attract
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Attract(self):
        RulesFunc.GameData.StdFuncs.Disable_Solenoids()
        RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.credits
        RulesFunc.CustomFunc.init_attract()

    ## Function Mode_Attract
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Attract(self):
        self.Proc_Press_Start()
        RulesFunc.CustomFunc.mode_attract()
        
    ## Function Proc_Add_Coin
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Add_Coin(self):
        pass

    ## Function Proc_Press_Start
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Press_Start(self):
        if RulesFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_CRDT_RST) and (RulesFunc.GameData.ballNum == 0):
            if (RulesFunc.GameData.gameMode == State.STATE_ATTRACT):
                RulesFunc.GameData.StdFuncs.StopBgnd()
                RulesFunc.CustomFunc.init_game()
                RulesFunc.GameData.gameMode = State.STATE_INIT_GAME
                RulesFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_CHOOSESINGER)
            if (RulesFunc.GameData.numPlayers < RulesFunc.GameData.GameConst.MAX_NUM_PLYRS):
                RulesFunc.GameData.score[RulesFunc.GameData.numPlayers] = 0
                RulesFunc.GameData.blankDisp[DispConst.DISP_PLAYER1 + RulesFunc.GameData.numPlayers] = False
                RulesFunc.GameData.numPlayers += 1
                RulesFunc.GameData.updDisp |= 0x3f

    ## Function Proc_Start_and_Coin
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Start_and_Coin(self):
        self.Proc_Add_Player()
        RulesFunc.CustomFunc.proc_attract_mode()

    ## Function Init_Init_Game
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Init_Game(self):
        RulesFunc.GameData.StdFuncs.Enable_Solenoids()
        
        # 30 second timer is used in case no selection is made
        RulesFunc.GameData.StdFuncs.TimerUpdate(Timers.TIMEOUT_GENERAL_TIMER, 30000)
        RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_GENERAL_TIMER)

    ## Function Mode_Init_Game
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Init_Game(self):
        self.Proc_Press_Start()
        self.Proc_Select_Singer()

    ## Function Init_Start_Ball
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Start_Ball(self):
        RulesFunc.CustomFunc.start_next_ball(RulesFunc.GameData.currPlayer)
        self.init_state = RulesFunc.WAIT_FOR_BALL_SERVE

    ## Function Mode_Start_Ball
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Start_Ball(self):
        # General timer expires and playing running with the devil stereo fade
        # Reset timer, and when it expires again, play the selected song
        if (RulesFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_GENERAL_TIMER)):
            if (self.init_state == RulesFunc.WAIT_FOR_BALL_SERVE):
                self.init_state = RulesFunc.WAIT_FOR_RUNNIN_CLIP_FINISH
            
                RulesFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_RUNNIN_DEVIL)
                RulesFunc.GameData.StdFuncs.TimerUpdate(Timers.TIMEOUT_GENERAL_TIMER, 8000)
                RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_GENERAL_TIMER)
            elif (self.init_state == RulesFunc.WAIT_FOR_RUNNIN_CLIP_FINISH):
                # Move to normal play mode, start playing the background song
                RulesFunc.GameData.StdFuncs.PlayBgnd(RulesFunc.CustomFunc.currSong[RulesFunc.GameData.currPlayer])
                RulesFunc.GameData.gameMode = State.STATE_NORMAL_PLAY
                
        RulesFunc.CustomFunc.normal_proc(RulesFunc.GameData.currPlayer)

    ## Function Init_Normal_Play
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Normal_Play(self):
        pass

    ## Function Proc_Normal_Play
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Normal_Play(self):
        RulesFunc.CustomFunc.normal_proc(RulesFunc.GameData.currPlayer)

    ## Function Proc_Choose_Mode_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Choose_Mode_Init(self):
        pass

    ## Function Proc_Choose_Mode
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Choose_Mode(self):
        pass

    ## Function Proc_Mode_Active_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Mode_Active_Init(self):
        pass

    ## Function Proc_Mode_Active
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Mode_Active(self):
        pass

    ## Function Proc_Jpot_Avail_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Jpot_Avail_Init(self):
        pass

    ## Function Proc_Jpot_Avail
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Jpot_Avail(self):
        pass

    ## Function Proc_End_Of_Ball
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_End_Of_Ball(self):
        pass

    ## Function Init_Jukebox
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Jukebox(self):
        pass

    ## Function Mode_Jukebox
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Jukebox(self):
        pass

    ## Function Init_End_Ball
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_End_Ball(self):
        RulesFunc.CustomFunc.end_ball(RulesFunc.GameData.currPlayer)
        if not RulesFunc.CustomFunc.tilted:
            RulesFunc.GameData.StdFuncs.Wait(1000)
        RulesFunc.GameData.scoreLvl = 0
        RulesFunc.GameData.scoring = False
        RulesFunc.GameData.currPlayer += 1
        RulesFunc.GameData.currPlyrDisp += 1
        if (RulesFunc.GameData.currPlayer >= RulesFunc.GameData.numPlayers):
            RulesFunc.GameData.currPlayer = 0
            RulesFunc.GameData.currPlyrDisp = 1
            RulesFunc.GameData.ballNum += 1
            if (RulesFunc.GameData.ballNum >= RulesFunc.GameData.GameConst.BALLS_PER_GAME):
                print "Game over"
                RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.credits
                RulesFunc.GameData.StdFuncs.StopBgnd()
                RulesFunc.GameData.StdFuncs.Wait(5000)
                RulesFunc.GameData.ballNum = 0
                RulesFunc.GameData.numPlayers = 0
                RulesFunc.GameData.blankDisp[DispConst.DISP_PLAYER_NUM] = True
                RulesFunc.GameData.blankDisp[DispConst.DISP_CREDIT_BALL_NUM] = True
                RulesFunc.GameData.gameMode = State.STATE_ATTRACT
            else:
                print "Player %d, Ball %d" % (RulesFunc.GameData.currPlayer + 1, RulesFunc.GameData.ballNum + 1) 
                RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.ballNum + 1
                RulesFunc.GameData.gameMode = State.STATE_STARTBALL
        else:
            print "Player %d, Ball %d" % (RulesFunc.GameData.currPlayer + 1, RulesFunc.GameData.ballNum + 1) 
            RulesFunc.GameData.gameMode = State.STATE_STARTBALL
    
    ## Function Mode_End_Ball
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_End_Ball(self):
        pass

    ## Function Init_Error
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Error(self):
        pass
    
    ## Function Mode_Error
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Error(self):
        pass

    ## Function Init_Tilt
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Init_Tilt(self):
        pass
    
    ## Function Mode_Tilt
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Mode_Tilt(self):
        pass
                        