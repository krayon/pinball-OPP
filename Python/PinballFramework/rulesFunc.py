#===============================================================================
#
#                         OOOO
#                       OOOOOOOO
#      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#     PPPPPPPPPPPPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP    OOO    OOO    PPP
#               PPP     OOOOOOOO     PPP
#              PPPPP      OOOO      PPPPP
#
# @file:   rulesFunc.py
# @author: Hugh Spahr
# @date:   4/19/2014
#
# @note:   Open Pinball Project
#          Copyright 2014, Hugh Spahr
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
#
# This is the rules functions for the simple pinball machine.
#
#===============================================================================

from rules.inpBitNames import InpBitNames
from rules.solBitNames import SolBitNames
from rules.ledBitNames import LedBitNames
from rules.timerBits import Timers
from rules.rulesData import RulesData
from rules.sounds import Sounds
from rules.states import State
from gameData import GameData
from stdFuncs import StdFuncs

class RulesFunc():
    LEFT_FLIPPER = 0x01
    RIGHT_FLIPPER = 0x02
    prev_flipper = 0
    LFT_TRGT_1 = 0x01
    LFT_TRGT_2 = 0x02
    RGHT_TRGT_1 = 0x04
    RGHT_TRGT_2 = 0x08
    TRGT_MSK = 0x0f
    curr_targets = 0
    tilted = False
    kick_retries = 0
    
    #Create rulesFunc instance
    stdFuncs = StdFuncs()
    
    #Initialize rules functions
    def init(self):
        self.prev_flipper = 0
    
    def Proc_Tilt(self):
        if (StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.TILT_SWITCH)):
            StdFuncs.Disable_Solenoids(self.stdFuncs)
            GameData.gameMode = State.TILT

    def Proc_Flipper(self):
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.LFT_FLIP)):
            if ((self.prev_flipper & self.LEFT_FLIPPER) == 0):
                StdFuncs.Led_Rot_Left(self.stdFuncs, LedBitNames.INLANE_MSK)
                GameData.inlaneLights[GameData.currPlayer] = StdFuncs.Var_Rot_Left(self.stdFuncs,  \
                    LedBitNames.INLANE_MSK, GameData.inlaneLights[GameData.currPlayer])
                self.prev_flipper |= self.LEFT_FLIPPER
        else:
            self.prev_flipper &= ~self.LEFT_FLIPPER
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.RGHT_FLIP)):
            if ((self.prev_flipper & self.RIGHT_FLIPPER) == 0):
                StdFuncs.Led_Rot_Right(self.stdFuncs, LedBitNames.INLANE_MSK)
                GameData.inlaneLights[GameData.currPlayer] = StdFuncs.Var_Rot_Right(self.stdFuncs,  \
                    LedBitNames.INLANE_MSK, GameData.inlaneLights[GameData.currPlayer])
                self.prev_flipper |= self.RIGHT_FLIPPER
        else:
            self.prev_flipper &= ~self.RIGHT_FLIPPER

    def Proc_Inlane(self):
        if (StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.INLANE_LFT) and \
                not StdFuncs.CheckLedBit(self.stdFuncs, LedBitNames.INLANE_LFT)):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.INLANE_LFT)
            GameData.inlaneLights[GameData.currPlayer] |= LedBitNames.INLANE_LFT
        if (StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.INLANE_CTR) and \
                not StdFuncs.CheckLedBit(self.stdFuncs, LedBitNames.INLANE_CTR)):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.INLANE_CTR)
            GameData.inlaneLights[GameData.currPlayer] |= LedBitNames.INLANE_CTR
        if (StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.INLANE_RGHT) and \
                not StdFuncs.CheckLedBit(self.stdFuncs, LedBitNames.INLANE_RGHT)):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.INLANE_RGHT)
            GameData.inlaneLights[GameData.currPlayer] |= LedBitNames.INLANE_RGHT
        if (GameData.inlaneLights[GameData.currPlayer] & LedBitNames.INLANE_MSK) == LedBitNames.INLANE_MSK:
            GameData.gameMode = State.INLANE_COMPLETE

    def Proc_Targets(self):
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.LFT_TRGT_1):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.LFT_TRGT_1)
            self.curr_targets |= self.LFT_TRGT_1 
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.LFT_TRGT_2):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.LFT_TRGT_2)
            self.curr_targets |= self.LFT_TRGT_2 
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.RGHT_TRGT_1):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.RGHT_TRGT_1)
            self.curr_targets |= self.RGHT_TRGT_1 
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.RGHT_TRGT_2):
            StdFuncs.Led_On(self.stdFuncs, LedBitNames.RGHT_TRGT_2)
            self.curr_targets |= self.RGHT_TRGT_2 
        if (self.curr_targets & (self.TRGT_MSK)) == self.TRGT_MSK:
            GameData.gameMode = State.TARGETS_COMPLETE

    def Proc_Kickout_Hole(self):
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.KICKOUT_HOLE)):
            StdFuncs.Kick(self.stdFuncs, SolBitNames.KICKOUT_HOLE)

    def Proc_Ball_Drain(self):
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.BALL_IN_PLAY)):
            GameData.gameMode = State.END_OF_BALL
            
    def Proc_Tilt_Init(self):
        self.tilted = True
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.KICKOUT_HOLE)):
            StdFuncs.Kick(self.stdFuncs, SolBitNames.KICKOUT_HOLE)
            self.kick_retries = 0
            StdFuncs.Start(self.stdFuncs, Timers.KICKOUT_TIMER)
        StdFuncs.Start(self.stdFuncs, Timers.BALL_LOCATE)

    def Proc_Tilt_State(self):
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.BALL_IN_PLAY)):
            StdFuncs.Enable_Solenoids(self.stdFuncs)
            GameData.gameMode = State.END_OF_BALL
        if (StdFuncs.Expired(self.stdFuncs, Timers.KICKOUT_TIMER)):
            if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.KICKOUT_HOLE)):
                self.kick_retries += 1
                if (self.kick_retries > 5):
                    GameData.gameMode = State.ERROR
                    print "Can't clear kickout hole"
                StdFuncs.Start(self.stdFuncs, Timers.KICKOUT_TIMER)
                StdFuncs.Kick(self.stdFuncs, SolBitNames.KICKOUT_HOLE)
        if (StdFuncs.Expired(self.stdFuncs, Timers.BALL_LOCATE)):
            GameData.gameMode = State.ERROR
            print "Lost Ball"
            
    def Proc_Init(self):
        StdFuncs.Disable_Solenoids(self.stdFuncs)
        if (GameData.credits == 0):
            GameData.gameMode = State.ATTRACT
        else:
            GameData.gameMode = State.PRESS_START

    def Proc_Add_Coin(self):
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.COIN_DROP):
            GameData.creditsInRow += 1
            GameData.partCreditsNum += 1
            if (GameData.creditsInRow == GameData.extraCredit):
                GameData.credits += 1
                GameData.creditsInRow = 0
                GameData.partCreditsNum = 0
            if (GameData.partCreditsNum == GameData.partCreditsDenom):
                GameData.credits += 1
                GameData.partCreditsNum = 0
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.START_BTN):
            GameData.creditsInRow = 0

    def Proc_Press_Start(self):
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.START_BTN) and (GameData.credits != 0) and \
                (GameData.ballNum == 0):
            if (GameData.numPlayers < RulesData.MAX_NUM_PLYRS):
                GameData.currPlayer = 0
                GameData.credits -= 1
                GameData.score[GameData.numPlayers] = 0
                GameData.numPlayers += 1
        if (GameData.gameMode == State.PRESS_START):
            StdFuncs.BlankScoreDisps(self.stdFuncs)
            StdFuncs.BlankPlyrNumDisp(self.stdFuncs)
            GameData.gameMode = State.START_GAME
                
    def Proc_Start_and_Coin(self):
        self.Proc_Add_Coin()
        self.Proc_Press_Start()
        
    def Proc_Init_Game(self):
        GameData.ballNum = 0
        GameData.specialLvl = 0
        for i in range(RulesData.MAX_NUM_PLYRS):
            GameData.inlaneLights[i] = 0
            
    def Proc_Start_Game(self):
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.BALL_AT_PLUNGER) or \
                StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.KICKOUT_HOLE):
            GameData.gameMode = State.BALL_IN_PLAY
        elif StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.BALL_IN_PLAY):
            GameData.gameMode = State.START_BALL
        else:
            GameData.gameMode = State.ERROR
            print "Can't find ball"
             
    def Proc_Start_Ball_Init(self):
        StdFuncs.Start(self.stdFuncs, Timers.KICKOUT_TIMER)
        StdFuncs.Kick(self.stdFuncs, SolBitNames.BALL_IN_PLAY)
        GameData.kick_retries = 0
        
    def Proc_Start_Ball_Start(self):
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.BALL_AT_PLUNGER):
            GameData.gameMode = State.BALL_IN_PLAY
        if StdFuncs.Expired(self.stdFuncs, Timers.KICKOUT_TIMER):
            GameData.kick_retries += 1
            if (GameData.kick_retries > 5):
                GameData.gameMode = State.ERROR
                print "Ball kick failed!"
            else:
                StdFuncs.Start(self.stdFuncs, Timers.KICKOUT_TIMER)
                StdFuncs.Kick(self.stdFuncs, SolBitNames.BALL_IN_PLAY)

    def Proc_Ball_In_Play_Init(self):
        StdFuncs.Led_Off(self.stdFuncs, LedBitNames.INLANE_MSK | LedBitNames.TRGT_MSK | LedBitNames.SPECIAL)
        StdFuncs.Led_Blink_100(self.stdFuncs, LedBitNames.INLANE_CTR)
        GameData.prev_flipper = 0
        GameData.targets = 0
        GameData.tilted = 0
        GameData.scoreLvl = 1
        GameData.numSpinners = 0

    def Proc_Ball_In_Play_Start(self):
        if (StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.INLANE_LFT) or \
                StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.INLANE_RGHT)):
            GameData.gameMode = State.NORMAL_PLAY
        if StdFuncs.CheckInpBit(self.stdFuncs, InpBitNames.INLANE_CTR):
            StdFuncs.Sounds(self.stdFuncs, Sounds.DING_DING_DING)
            print "Skill Shot"
            GameData.score[GameData.currPlayer] += 10
            GameData.gameMode = State.NORMAL_PLAY
            
    def Proc_Normal_Play_Init(self):
        StdFuncs.Led_Set(self.stdFuncs, LedBitNames.INLANE_MSK, GameData.inlaneLights[GameData.currPlayer])
        
    def Proc_Normal_Play(self):
        self.Proc_Tilt()
        self.Proc_Flipper()
        self.Proc_Inlane()
        self.Proc_Targets()
        self.Proc_Kickout_Hole()
        self.Proc_Start_and_Coin()
        self.Proc_Ball_Drain()

    def Proc_End_Of_Ball(self):
        if not self.tilted:
            print "Bonus %d x %d" % (GameData.scoreLvl, GameData.numSpinners)
            GameData.score[GameData.currPlayer] += (GameData.scoreLvl * GameData.numSpinners)
            StdFuncs.Wait(self.stdFuncs, 3000)
        GameData.currPlayer += 1
        if (GameData.currPlayer > GameData.numPlayers):
            GameData.currPlayer = 0
            GameData.ballNum += 1
            if (GameData.ballNum >= RulesData.BALLS_PER_GAME):
                print "Game over"
                StdFuncs.Wait(self.stdFuncs, 3000)
                if (GameData.credits == 0):
                    GameData.gameMode = State.ATTRACT
                else:
                    GameData.gameMode = State.PRESS_START
            else:
                print "Player %d, Ball %d" % (GameData.currPlayer + 1, GameData.ballNum + 1) 
                GameData.gameMode = State.START_BALL
        else:
            print "Player %d, Ball %d" % (GameData.currPlayer + 1, GameData.ballNum + 1) 
            GameData.gameMode = State.START_BALL

    def Proc_Inlane_Comp(self):
        print "Inlanes Complete!!"
        GameData.scoreLvl += 1
        GameData.score[GameData.currPlayer] += 10
        GameData.inlaneLights[GameData.currPlayer] = 0
        StdFuncs.Led_Off(self.stdFuncs, LedBitNames.INLANE_MSK)
        GameData.gameMode = State.NORMAL_PLAY
   
    def Proc_Targets_Comp_Init(self):
        StdFuncs.Led_Blink_100(self.stdFuncs, LedBitNames.SPECIAL)
        print "Super Mode!"
        GameData.specialLvl[GameData.currPlayer] += 1
        GameData.score[GameData.currPlayer] += (GameData.specialLvl[GameData.currPlayer] * 10)
        StdFuncs.Start(self.stdFuncs, Timers.SPECIAL_TIMER)

    def Proc_Targets_Comp_State(self):
        if (StdFuncs.CheckSolBit(self.stdFuncs, SolBitNames.KICKOUT_HOLE)):
            print "Jackpot"
            GameData.score[GameData.currPlayer] += (GameData.specialLvl[GameData.currPlayer] * 100)
        if (StdFuncs.Expired(self.stdFuncs, Timers.SPECIAL_TIMER)):
            GameData.gameMode = State.NORMAL_PLAY
        self.Proc_Normal_Play()

