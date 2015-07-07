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
# @date    02/07/2015
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

from SS3.inpBitNames import InpBitNames
from SS3.solBitNames import SolBitNames
from SS3.ledBitNames import LedBitNames
from SS3.timers import Timers
from SS3.rulesData import RulesData
from SS3.sounds import Sounds
from SS3.bgndSounds import BgndMusic
from SS3.states import State
from SS3.images import Images
from dispConstIntf import DispConst
from SS3.customFunc import CustomFunc

## Rules functions class.
#  Contains all the rules that are specific this this set of pinball rules.

class RulesFunc:
    LEFT_FLIPPER = 0x01
    RIGHT_FLIPPER = 0x02
    LFT_TRGT_1 = 0x01
    LFT_TRGT_2 = 0x02
    RGHT_TRGT_1 = 0x04
    RGHT_TRGT_2 = 0x08
    TRGT_MSK = 0x0f
    curr_targets = 0
    kick_retries = 0
    prev_flipper = 0
    
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
#        if (RulesFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.TILT_SWITCH)):
#            RulesFunc.GameData.StdFuncs.Disable_Solenoids()
#            RulesFunc.GameData.gameMode = State.MODE_TILT

    ## Function Proc_Flipper
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Flipper(self):
        if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_LFT_FLIPPER)):
            if ((RulesFunc.prev_flipper & self.LEFT_FLIPPER) == 0):
                RulesFunc.CustomFunc.flipper_left_rotate(RulesFunc.GameData.currPlayer)
                RulesFunc.prev_flipper |= self.LEFT_FLIPPER
        else:
            RulesFunc.prev_flipper &= ~self.LEFT_FLIPPER
        if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_RGHT_FLIPPER)):
            if ((RulesFunc.prev_flipper & self.RIGHT_FLIPPER) == 0):
                RulesFunc.CustomFunc.flipper_right_rotate(RulesFunc.GameData.currPlayer)
                RulesFunc.prev_flipper |= self.RIGHT_FLIPPER
        else:
            RulesFunc.prev_flipper &= ~self.RIGHT_FLIPPER

    ## Function Proc_Kickout_Hole
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Kickout_Hole(self):
        if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_KICKOUT_HOLE)):
            RulesFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_KICKOUT_HOLE)

    ## Function Proc_Ball_Drain
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Ball_Drain(self):
        if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_BALL_IN_PLAY)):
            if (RulesFunc.GameData.StdFuncs.TimerRunning(Timers.TIMEOUT_RELOAD_TIMER)):
                RulesFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_BALL_IN_PLAY)
            else:
                RulesFunc.GameData.gameMode = State.MODE_END_OF_BALL

    ## Function Proc_Timers
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Timers(self):
        if (RulesFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_RELOAD_TIMER)):
            # Stop blinking the reload LED
            RulesFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_SHOOT_AGAIN)
        
        # If the retry timer times out, and the ball is in the drain, serve it again.
        # If the reload timer is running, restart this timer
        if (RulesFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_RETRY_TIMER)):
            if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_BALL_IN_PLAY)):
                RulesFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_BALL_IN_PLAY)
                if (RulesFunc.GameData.StdFuncs.TimerRunning(Timers.TIMEOUT_RELOAD_TIMER)):
                    RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RETRY_TIMER)

    ## Function Proc_Tilt_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Tilt_Init(self):
        RulesFunc.CustomFunc.tilted = True
        if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_KICKOUT_HOLE)):
            RulesFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_KICKOUT_HOLE)
            self.kick_retries = 0
            RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_KICKOUT_TIMER)
        RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_BALL_LOCATE)

    ## Function Proc_Tilt_State
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Tilt_State(self):
        if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_BALL_IN_PLAY)):
            RulesFunc.GameData.StdFuncs.Enable_Solenoids()
            RulesFunc.GameData.gameMode = State.MODE_END_OF_BALL
        if (RulesFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_KICKOUT_TIMER)):
            if (RulesFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_KICKOUT_HOLE)):
                self.kick_retries += 1
                if (self.kick_retries > 5):
                    RulesFunc.GameData.gameMode = State.MODE_ERROR
                    print "Can't clear kickout hole"
                RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_KICKOUT_TIMER)
                RulesFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_KICKOUT_HOLE)
        if (RulesFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_BALL_LOCATE)):
            RulesFunc.GameData.gameMode = State.MODE_ERROR
            print "Lost Ball"

    ## Function Proc_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Init(self):
        RulesFunc.GameData.StdFuncs.Restore_Input_Cfg()
        RulesFunc.GameData.gameMode = State.MODE_ATTRACT

    ## Function Proc_Attract_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Attract_Init(self):
        RulesFunc.GameData.StdFuncs.Disable_Solenoids()
        RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.credits
        RulesFunc.CustomFunc.init_attract_mode()

    ## Function Proc_Add_Coin
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Add_Coin(self):
        if RulesFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_COIN_DROP):
            RulesFunc.GameData.creditsInRow += 1
            RulesFunc.GameData.partCreditsNum += 1
            if (RulesFunc.GameData.creditsInRow == RulesFunc.GameData.extraCredit):
                RulesFunc.GameData.credits += 1
                if RulesFunc.GameData.gameMode == State.MODE_ATTRACT:
                    RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.credits
                RulesFunc.GameData.creditsInRow = 0
                RulesFunc.GameData.partCreditsNum = 0
            if (RulesFunc.GameData.partCreditsNum == RulesFunc.GameData.partCreditsDenom):
                RulesFunc.GameData.credits += 1
                if RulesFunc.GameData.gameMode == State.MODE_ATTRACT:
                    RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.credits
                RulesFunc.GameData.partCreditsNum = 0
        if RulesFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_START):
            RulesFunc.GameData.creditsInRow = 0

    ## Function Proc_Press_Start
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Press_Start(self):
        if RulesFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_START) and (RulesFunc.GameData.ballNum == 0):
            if (RulesFunc.GameData.gameMode == State.MODE_ATTRACT):
                RulesFunc.GameData.StdFuncs.StopBgnd()
                CustomFunc.GameData.gameMode = State.MODE_INIT_GAME
            if (RulesFunc.GameData.numPlayers < RulesFunc.GameData.GameConst.MAX_NUM_PLYRS):
                RulesFunc.GameData.score[RulesFunc.GameData.numPlayers] = 0
                RulesFunc.GameData.blankDisp[DispConst.DISP_PLAYER1 + RulesFunc.GameData.numPlayers] = False
                RulesFunc.GameData.numPlayers += 1
                RulesFunc.GameData.updDisp |= 0x3f

    ## Function Proc_Press_Start_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Press_Start_Init(self):
        pass

    ## Function Proc_Start_and_Coin
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Start_and_Coin(self):
        self.Proc_Press_Start()
        RulesFunc.CustomFunc.proc_attract_mode()

    ## Function Proc_Init_Game
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Init_Game(self):
        RulesFunc.GameData.StdFuncs.Enable_Solenoids()
        RulesFunc.GameData.StdFuncs.BgndImage(Images.IMAGE_SALOON)
        RulesFunc.CustomFunc.init_game()
        RulesFunc.CustomFunc.start_next_ball(0)
        RulesFunc.GameData.gameMode = State.MODE_SKILLSHOT

    ## Function Proc_Start_Game
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Start_Game(self):
        pass

    ## Function Proc_Start_Ball_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Start_Ball_Init(self):
        RulesFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_KICKOUT_TIMER)
        RulesFunc.GameData.kick_retries = 0

    ## Function Proc_Start_Ball_Start
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Start_Ball_Start(self):
        # unused since no switch in the plunger lane
        pass

    ## Function Proc_Skillshot
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Skillshot(self):
        self.Proc_Timers()
        RulesFunc.CustomFunc.proc_skillshot(RulesFunc.GameData.currPlayer)

    ## Function Proc_Normal_Play_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Normal_Play_Init(self):
        pass

    ## Function Proc_Normal_Play
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Normal_Play(self):
        self.Proc_Tilt()
        RulesFunc.CustomFunc.proc_inlanes(RulesFunc.GameData.currPlayer)
        RulesFunc.CustomFunc.proc_drop_targets(RulesFunc.GameData.currPlayer)
        self.Proc_Flipper()
        RulesFunc.CustomFunc.proc_spinner(RulesFunc.GameData.currPlayer)
        self.Proc_Start_and_Coin()
        self.Proc_Ball_Drain()
        self.Proc_Timers()
        RulesFunc.CustomFunc.proc_normal_play(RulesFunc.GameData.currPlayer)


    ## Function Proc_Choose_Mode_Init
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Choose_Mode_Init(self):
        RulesFunc.CustomFunc.init_choose_mode(RulesFunc.GameData.currPlayer)
    
    ## Function Proc_Choose_Mode
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Choose_Mode(self):
        self.Proc_Flipper()
        self.Proc_Timers()
        RulesFunc.CustomFunc.proc_choose_mode(RulesFunc.GameData.currPlayer)

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
        RulesFunc.CustomFunc.proc_inlanes(RulesFunc.GameData.currPlayer)
        RulesFunc.CustomFunc.proc_drop_targets(RulesFunc.GameData.currPlayer)
        RulesFunc.CustomFunc.proc_mode_active(RulesFunc.GameData.currPlayer)
        self.Proc_Timers()
        self.Proc_Ball_Drain()
   
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
        RulesFunc.CustomFunc.proc_jackpot_avail(RulesFunc.GameData.currPlayer)
        self.Proc_Ball_Drain()
       
    ## Function Proc_End_Of_Ball
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_End_Of_Ball(self):
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
                RulesFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_BALL_DRAIN_BANJO)
                RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.credits
                RulesFunc.GameData.StdFuncs.StopBgnd()
                RulesFunc.GameData.StdFuncs.Wait(5000)
                RulesFunc.GameData.ballNum = 0
                RulesFunc.GameData.numPlayers = 0
                RulesFunc.GameData.blankDisp[DispConst.DISP_PLAYER_NUM] = True
                RulesFunc.GameData.blankDisp[DispConst.DISP_CREDIT_BALL_NUM] = True
                if (RulesFunc.GameData.credits == 0):
                    RulesFunc.GameData.gameMode = State.MODE_ATTRACT
                else:
                    RulesFunc.GameData.gameMode = State.MODE_ATTRACT
            else:
                print "Player %d, Ball %d" % (RulesFunc.GameData.currPlayer + 1, RulesFunc.GameData.ballNum + 1) 
                RulesFunc.GameData.creditBallNumDisp = RulesFunc.GameData.ballNum + 1
                RulesFunc.GameData.gameMode = State.MODE_SKILLSHOT
                RulesFunc.CustomFunc.start_next_ball(RulesFunc.GameData.currPlayer)
        else:
            print "Player %d, Ball %d" % (RulesFunc.GameData.currPlayer + 1, RulesFunc.GameData.ballNum + 1) 
            RulesFunc.GameData.gameMode = State.MODE_SKILLSHOT
            RulesFunc.CustomFunc.start_next_ball(RulesFunc.GameData.currPlayer)

