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
# @file    customFunc.py
# @author  Hugh Spahr
# @date    3/10/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief This file provides custom functions for a pinball ruleset.  It should
# live in the rules directory for the individual machine.

#===============================================================================
from VH.inpBitNames import InpBitNames
from VH.solBitNames import SolBitNames
from VH.sounds import Sounds
from VH.ledBitNames import LedBitNames
from VH.timers import Timers
from VH.bgndSounds import BgndMusic
import random
import rs232Intf
from VH.states import State
from dispConstIntf import DispConst
import time
import logging

## Custom functions class.
#  Contains all the custom rules and functions that are specific this this set
#  of pinball rules.  These are not created or generated from GenPyCode.
class CustomFunc:
    SNGR_SAMMY = 0x01
    SNGR_DAVID = 0x02
    singer = [0, 0, 0, 0]
    
    STATEPROG_NONE = 0x00
    STATEPROG_EDDIE_COLLECTED = 0x01
    STATEPROG_ALEX_COLLECTED = 0x02
    STATEPROG_SAMMY_COLLECTED = 0x04
    STATEPROG_DAVID_COLLECTED = 0x08
    STATEPROG_JUKEBOX_COLLECTED = 0x10
    stateProg = [0, 0, 0, 0]

    # Used to note big events that happen during a poll cycle (bitfield)
    POLLSTAT_INLINE_COMP = 0x01
    POLLSTAT_DAVID_COMP = 0x02
    POLLSTAT_SAMMY_COMP = 0x04
    POLLSTAT_ALEX_COMP = 0x08
    POLLSTAT_EDDIE_COMP = 0x10
    POLLSTAT_1984_COMP = 0x20
    pollStatus = [0, 0, 0, 0]
    
    LANE_1984_1 = 0x08
    LANE_1984_9 = 0x04
    LANE_1984_8 = 0x02
    LANE_1984_4 = 0x01
    LANE_ALL_MASK = 0x0f
    compLanes = [0, 0, 0, 0]
    
    eddieCnt = [0, 0, 0, 0]
    alexCnt = [0, 0, 0, 0]
    
    tilted = False
    
    CONST_DAVID = LedBitNames.LED_DAVID_D1 | LedBitNames.LED_DAVID_A | LedBitNames.LED_DAVID_V | LedBitNames.LED_DAVID_I | LedBitNames.LED_DAVID_D2
    CONST_ROCKER = LedBitNames.LED_ROCKER_R1 | LedBitNames.LED_ROCKER_O | LedBitNames.LED_ROCKER_C | LedBitNames.LED_ROCKER_K | LedBitNames.LED_ROCKER_E | LedBitNames.LED_ROCKER_R2
    CONST_1984 = LedBitNames.LED_1984_1 | LedBitNames.LED_1984_9 | LedBitNames.LED_1984_8 | LedBitNames.LED_1984_4
            
    ## Initialize CustomFunc class
    #
    #  Initialize custom functions class
    #
    #  @param  self          [in]   Object reference
    #  @param  gameData      [in]   Object reference
    #  @return None
    def __init__(self, gameData):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='VH.log', level=logging.INFO)
        logging.info('Machine initialized')
        CustomFunc.GameData = gameData
        CustomFunc.tilted = False
        self.stateProg = [CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE]
        self.compLanes = [0, 0, 0, 0]
        self.eddieCnt = [0, 0, 0, 0]
        self.alexCnt = [0, 0, 0, 0]
        self.dropTrgtGoal = [0, 0, 0, 0]
        self.selectMode = 0
        self.spinMult = 1
        self.numSpin = 0
        self.tiltActive = False
        self.disableRotate = False
        self.saveModeState = [0, 0, 0, 0]
        self.saveModeData = [0, 0, 0, 0]
        self.saveModeValue = 0
        self.pollStatus = 0
        self._compInlaneScore = [50, 75, 100, 150]
        self._compModeScore = [500, 750, 1000, 1500]
        self.dropHit = 0
        self.totDrops = 0
        self.tmpValue = 0
        self.normInpScore = [ [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0 ],
                              [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0,
                                1, 0, 1, 5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
                              [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                              [ 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                                2, 5, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                              ]
        self.attractStart = 0
        
    ## Initialize game
    #
    #  Initialize the game variables
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def init_game(self):
        self.stateProg = [CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE]
        self.selectMode = 0
        self.compLanes = [0, 0, 0, 0]
        self.eddieCnt = [0, 0, 0, 0]
        self.alexCnt = [0, 0, 0, 0]
        self.spinMult = 1
        self.numSpin = 0
        self.tiltActive = False
        self.disableRotate = False
        self.GameData.currPlayer = 0
        self.GameData.currPlyrDisp = 1
        self.GameData.creditBallNumDisp = 1
        self.GameData.ballNum = 0
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER1] = False
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER_NUM] = False
        CustomFunc.GameData.blankDisp[DispConst.DISP_CREDIT_BALL_NUM] = False
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER2] = True
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER3] = True
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER4] = True

        # Turn off all the LEDs from attract mode
        CustomFunc.GameData.StdFuncs.Led_Off([LedBitNames.LED_CRD0_LIST_BITS_MSK, LedBitNames.LED_CRD1_LIST_BITS_MSK])
                
    ## Init attract mode
    #
    #  Initialize attract mode
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def init_attract(self):
        logging.info('Machine state:  Attract_mode')
        self.attractStart = time.time()

    ## attract mode
    #
    #  Process attract mode
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def mode_attract(self):
        elapsed = time.time() - self.attractStart
        # Play song every 20 minutes
        if ((elapsed/60) >= 20):
            self.attractStart = time.time()
            randomNum = random.randint(BgndMusic.BGND_JUMP, BgndMusic.BGND_ICECREAMMAN)
            CustomFunc.GameData.StdFuncs.PlayBgnd(randomNum | \
                CustomFunc.GameData.StdFuncs.BGND_PLAY_ONCE)

    ## Start next ball
    #
    #  Start the next ball, and reset LEDs
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def start_next_ball(self, plyr):
        logging.info('Ball started:  Player = %s, BallNum = %s', plyr + 1, self.GameData.ballNum + 1)
        
        # Restore Eddie inserts
        self.restore_eddie(plyr)
        
        # Restore Alex inserts
        self.restore_alex(plyr)
        
        # Restore David inserts
        self.restore_david(plyr)
        
        # Restore Rocker inserts
        self.restore_rocker(plyr)
        
        # Restore 1984 inserts
        self.restore_1984(plyr)
        
        # Reset the spinner kickout hole LEDs, 
        self.spinMult = 1
        self.numSpin = 0
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SHOOT_AGAIN)
        CustomFunc.GameData.StdFuncs.Enable_Solenoids()
        CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_OUTHOLE)
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RELOAD_TIMER)
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RETRY_TIMER)

        # Tilt is not active during skill shot to allow nudging
        self.tilted = False
        self.tiltActive = False
                
    ## End ball
    #
    #  End the ball, and reset LEDs
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def end_ball(self, plyr):
        # End background music
        CustomFunc.GameData.StdFuncs.StopBgnd()

        # Turn off the blinking on all the LEDs (cleanup from previous mode)
        CustomFunc.GameData.StdFuncs.Led_Blink_Off([LedBitNames.LED_CRD0_LIST_BITS_MSK, LedBitNames.LED_CRD1_LIST_BITS_MSK])
        CustomFunc.GameData.StdFuncs.Led_Off([LedBitNames.LED_CRD0_LIST_BITS_MSK, LedBitNames.LED_CRD1_LIST_BITS_MSK])
                
        # Calculate bonus, HRS must add complete mode bonus
        if not CustomFunc.tilted:
            print "Collect spinner bonus %d x %d" % (self.spinMult, self.numSpin)
            CustomFunc.GameData.score[plyr] += (self.spinMult * self.numSpin)
            
        logging.info('Ball ended:  Player = %s, BallNum = %s, Score = %s', \
            plyr + 1, self.GameData.ballNum + 1, CustomFunc.GameData.score[plyr])
    
    ## Flipper right rotate
    #
    #  Right rotate the LEDs properly depending on the mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def flipper_right_rotate(self, plyr):
        mask = [0, CustomFunc.CONST_1984]
        
        # Rotate 1984, set inserts
        self.compLanes[plyr] = ((self.compLanes[plyr] << 3) & 0x08) | ((self.compInlanes[plyr] & 0x0e) >> 1)
        
    ## Flipper left rotate
    #
    #  Left rotate the LEDs properly depending on the mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def flipper_left_rotate(self, plyr):
        mask = [0, CustomFunc.CONST_1984]
        
        # Rotate 1984, set inserts
        self.compLanes[plyr] = ((self.compLanes[plyr] >> 3) & 0x01) | ((self.compInlanes[plyr] & 0x07) << 1)

    ## Process inlanes
    #
    #  Process inlanes and see if complete
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_inlanes(self, plyr):
        unlit = 0
        lit = 0
        comp = 0
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_LFT_OUTLN):
            if (self.compLanes[plyr] & CustomFunc.LANE_1984_1) == 0:
                # Unlit 1984 lane hit
                unlit += 1
                self.compLanes[plyr] |= CustomFunc.LANE_1984_1
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_1984_1)
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_LFT_INLN):
            if (self.compLanes[plyr] & CustomFunc.LANE_1984_9) == 0:
                # Unlit 1984 lane hit
                unlit += 1
                self.compLanes[plyr] |= CustomFunc.LANE_1984_9
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_1984_9)
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_RGHT_INLN):
            if (self.compLanes[plyr] & CustomFunc.LANE_1984_8) == 0:
                # Unlit 1984 lane hit
                unlit += 1
                self.compLanes[plyr] |= CustomFunc.LANE_1984_8
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_1984_8)
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_RGHT_OUTLN):
            if (self.compLanes[plyr] & CustomFunc.LANE_1984_4) == 0:
                # Unlit 1984 lane hit
                unlit += 1
                self.compLanes[plyr] |= CustomFunc.LANE_1984_4
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_1984_4)
            else:
                lit += 1
        if (self.compLanes[plyr] & CustomFunc.LANE_ALL_MASK) == CustomFunc.LANE_ALL_MASK:
            comp = 1
            self.pollStatus |= CustomFunc.POLLSTAT_1984_COMP
        CustomFunc.GameData.score[plyr] += ((unlit * 5) + (lit * 2) + (comp * 25))
        
    ## Process drop targets
    #
    #  Process drop targets and see if complete
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_drop_targets(self, plyr):
        hit = 0
        comp = 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_1ST):
            hit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_2X):
            hit += 2
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_3X):
            hit += 3
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_5X):
            hit += 5
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_SUPER_STAR_TRGT):
            print "Drops Complete!!"
            hit += 10
            comp += 1
            self.pollStatus |= CustomFunc.POLLSTAT_INLINE_COMP
        CustomFunc.GameData.score[plyr] += (hit * 5)
        
    ## Process spinner
    #
    #  Process spinner
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_spinner(self, plyr):
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_SPINNER):
            CustomFunc.GameData.score[plyr] += self.spinMult
            self.numSpin += 1

    ## Process Eddie
    #
    #  Process Eddie target
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_eddie(self, plyr):
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_LFT_TRGT):
            if (self.stateProg[plyr] & CustomFunc.STATEPROG_EDDIE_COLLECTED):
                CustomFunc.GameData.score[plyr] += 50
            else:
                if (CustomFunc.GameData.eddieCnt[plyr] == 0):
                    # Collected E1
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_E1)
                    CustomFunc.GameData.score[plyr] += 10
                elif (CustomFunc.GameData.eddieCnt[plyr] == 1):
                    # Collected D1
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_D1)
                    CustomFunc.GameData.score[plyr] += 20
                elif (CustomFunc.GameData.eddieCnt[plyr] == 2):
                    # Collected D2
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_D2)
                    CustomFunc.GameData.score[plyr] += 30
                elif (CustomFunc.GameData.eddieCnt[plyr] == 3):
                    # Collected I
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_I)
                    CustomFunc.GameData.score[plyr] += 40
                elif (CustomFunc.GameData.eddieCnt[plyr] == 4):
                    # Collected E2
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_E2)
                    CustomFunc.GameData.score[plyr] += 50
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_EDDIE_COLLECTED
                CustomFunc.GameData.eddieCnt[plyr] += 1
            
    ## Process Alex
    #
    #  Process Alex pops
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_alex(self, plyr):
        oldCnt = CustomFunc.GameData.alexCnt[plyr]/5
        hit = 0
        comp = 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_LFT_POP):
            hit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_TOP_POP):
            hit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_BTM_POP):
            hit += 1
        if (hit != 0):
            if (self.stateProg[plyr] & CustomFunc.STATEPROG_ALEX_COLLECTED):
                CustomFunc.GameData.score[plyr] += (hit * 10)
            else:
                CustomFunc.GameData.alexCnt[plyr] += hit
                CustomFunc.GameData.score[plyr] += (hit * 5)
                if (oldCnt != (CustomFunc.GameData.alexCnt[plyr]/5)):
                    if (oldCnt == 0):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_A)
                    elif (oldCnt == 1):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_L)
                    elif (oldCnt == 2):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_E)
                    elif (oldCnt == 3):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_X)
                        self.stateProg[plyr] |= CustomFunc.STATEPROG_ALEX_COLLECTED
                    
    ## Collect bonus
    #
    #  Collect the bonus
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  sound         [in]   True to play sound
    #  @return None
    #
    #  @note Five orbits, then sink kickout hole.  Future:  Gives two ball multiball.
    def proc_collect_bonus(self, plyr, sound):
        
        #Hitting kickout hole, collects the bonus
        if not (CustomFunc.GameData.StdFuncs.TimerRunning(Timers.TIMEOUT_KICKOUT)):
            logging.info('Collect bonus:  Player = %s, BallNum = %s', plyr + 1, self.GameData.ballNum + 1)
            CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_KICKOUT)
            print "Collect bonus"
            CustomFunc.GameData.score[plyr] += (self.spinMult * self.numSpin)
            if (sound):
                randomNum = random.randint(0, 1)
                CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_HORSE_NEIGH + randomNum)
                CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_KICKOUT_HOLE)

    ## Change singer to Sammy
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Singer_Sammy(self):
        # Turn off David blink, turn on Sammy (Rocker) blink
        CustomFunc.GameData.StdFuncs.Led_Blink_Off(CustomFunc.CONST_DAVID)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_ROCKER)
        CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_SAMMYHAGAR)
        CustomFunc.singer[CustomFunc.GameData.currPlayer] = self.SNGR_SAMMY

    ## Change singer to David Lee Roth
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Singer_David(self):
        # Turn off Rocker blink, turn on David blink
        CustomFunc.GameData.StdFuncs.Led_Blink_Off(CustomFunc.CONST_ROCKER)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_DAVID)
        CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_DAVIDLEEROTH)
        CustomFunc.singer[CustomFunc.GameData.currPlayer] = self.SNGR_DAVID

    ## Restore Eddie
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_eddie(self):
        pass
        
    ## Restore Alex
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_alex(self):
        pass
        
    ## Restore David
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_david(self):
        pass
        
    ## Restore Sammy
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_rocker(self):
        pass
        
    ## Restore 1984
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_1984(self):
        pass
        