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
    STATEPROG_DAVID_COLLECTED = 0x08  # Used to indicate David and Roth collected
    STATEPROG_ROTH_COLLECTED = 0x10
    STATEPROG_JUKEBOX_COLLECTED = 0x20
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
    
    TRGT_DAVID_D1 = 0x10
    TRGT_DAVID_A = 0x08
    TRGT_DAVID_V = 0x04
    TRGT_DAVID_I = 0x02
    TRGT_DAVID_D2 = 0x01
    TRGT_DAVID_ALL_MASK = 0x1f
    davidTrgts = [0, 0, 0, 0]
    
    eddieCnt = [0, 0, 0, 0]
    sammyCnt = [0, 0, 0, 0]
    alexCnt = [0, 0, 0, 0]
    currSong = [0, 0, 0, 0]
    availSongs = [0, 0, 0, 0]
    
    tilted = False

    EVENT_PANAMA = 0x01
    EVENT_EDDIE = 0x02
    EVENT_JUKEBOX_AVAIL = 0x04
    EVENT_RELOAD_ACTIVE = 0x08
    EVENT_ERUPTION_ACTIVE = 0x10
    EVENT_SAUCER_ACTIVE = 0x20
    EVENT_DROP_COMPLETE = 0x40
    EVENT_DROP_1ST = 0x100
    EVENT_DROP_2ND = 0x200
    EVENT_DROP_3RD = 0x400
    EVENT_DROP_4TH = 0x800
    events = 0
    
    CONST_DAVID = [LedBitNames.LED_DAVID_D1_CRD0MSK | LedBitNames.LED_DAVID_V_CRD0MSK | LedBitNames.LED_DAVID_D2_CRD0MSK, LedBitNames.LED_DAVID_A_CRD1MSK | LedBitNames.LED_DAVID_I_CRD1MSK]
    CONST_ROCKER = [LedBitNames.LED_ROCKER_R1_CRD0MSK | LedBitNames.LED_ROCKER_O_CRD0MSK | LedBitNames.LED_ROCKER_K_CRD0MSK | LedBitNames.LED_ROCKER_R2_CRD0MSK, LedBitNames.LED_ROCKER_C_CRD1MSK | LedBitNames.LED_ROCKER_E_CRD1MSK]
    CONST_1984 = [LedBitNames.LED_1984_9_CRD0MSK | LedBitNames.LED_1984_8_CRD0MSK | LedBitNames.LED_1984_4_CRD0MSK, LedBitNames.LED_1984_1_CRD1MSK ]
            
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
        self.events = 0
        self.davidTrgts = [0, 0, 0, 0]
        self.eddieCnt = [0, 0, 0, 0]
        self.sammyCnt = [0, 0, 0, 0]
        self.alexCnt = [0, 0, 0, 0]
        self.currSong = [0, 0, 0, 0]
        self.availSongs = [0, 0, 0, 0]
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
        self.events = 0
        self.davidTrgts = [0, 0, 0, 0]
        self.eddieCnt = [0, 0, 0, 0]
        self.sammyCnt = [0, 0, 0, 0]
        self.alexCnt = [0, 0, 0, 0]
        self.currSong = [0, 0, 0, 0]
        self.availSongs = [0, 0, 0, 0]
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
        
        # Restore state
        self.restore_eddie(plyr)
        self.restore_alex(plyr)
        self.restore_david(plyr)
        self.restore_rocker(plyr)
        self.restore_1984(plyr)
        
        # if this is the first ball, figure out the song and display slide
        if (self.GameData.ballNum == 0):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                # Choose from David Lee Roth songs
                randomNum = random.randint(BgndMusic.BGND_JUMP, BgndMusic.BGND_DROPDEADLEGS)
                self.availSongs[plyr] = 0x3f
            else:
                # Choose from Sammy Hagar songs
                randomNum = random.randint(BgndMusic.BGND_BESTOFBOTHWORLDS, BgndMusic.BGND_CABOWABO)
                self.availSongs[plyr] = 0xfc0
            self.currSong[plyr] = randomNum
        CustomFunc.GameData.StdFuncs.BgndImage(self.currSong[plyr])
        
        # Reset the spinner kickout hole LEDs, 
        self.spinMult = 1
        self.numSpin = 0
        self.events = 0
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SHOOT_AGAIN)
        CustomFunc.GameData.StdFuncs.Enable_Solenoids()
        CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_DROP_BANK)
        CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_OUTHOLE)
        CustomFunc.GameData.StdFuncs.TimerUpdate(Timers.TIMEOUT_RELOAD_TIMER, 20000) 
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RELOAD_TIMER)
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RETRY_TIMER)
        self.events |= self.EVENT_RELOAD_ACTIVE

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
                
        # Calculate bonus
        if not CustomFunc.tilted:
            print "Collect spinner bonus %d x %d" % (self.spinMult, self.numSpin)
            CustomFunc.GameData.score[plyr] += (self.spinMult * self.numSpin)
            
        logging.info('Ball ended:  Player = %s, BallNum = %s, Score = %s', \
            plyr + 1, self.GameData.ballNum + 1, CustomFunc.GameData.score[plyr])

    ## Set lane lights
    #
    #  Set the lane lights
    #
    #  @param  self          [in]   Object reference
    #  @param  change        [in]   Lights that changed
    #  @param  newVal        [in]   New value
    #  @return None
    def set_lane_lights(self, change, newVal):
        turnOn = [0, 0]
        turnOff = [0, 0]
        if (change & CustomFunc.LANE_1984_1):
            if (newVal & CustomFunc.LANE_1984_1):
                turnOn[1] |= LedBitNames.LED_1984_1_CRD1MSK
            else:
                turnOff[1] |= LedBitNames.LED_1984_1_CRD1MSK
        if (change & CustomFunc.LANE_1984_9):
            if (newVal & CustomFunc.LANE_1984_9):
                turnOn[0] |= LedBitNames.LED_1984_9_CRD0MSK
            else:
                turnOff[0] |= LedBitNames.LED_1984_9_CRD0MSK
        if (change & CustomFunc.LANE_1984_8):
            if (newVal & CustomFunc.LANE_1984_8):
                turnOn[0] |= LedBitNames.LED_1984_8_CRD0MSK
            else:
                turnOff[0] |= LedBitNames.LED_1984_8_CRD0MSK
        if (change & CustomFunc.LANE_1984_4):
            if (newVal & CustomFunc.LANE_1984_4):
                turnOn[0] |= LedBitNames.LED_1984_4_CRD0MSK
            else:
                turnOff[0] |= LedBitNames.LED_1984_4_CRD0MSK
        CustomFunc.GameData.StdFuncs.Led_On(turnOn)
        CustomFunc.GameData.StdFuncs.Led_Off(turnOff)
            
    ## Flipper right rotate
    #
    #  Right rotate the LEDs properly depending on the mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def flipper_right_rotate(self, plyr):
        # Rotate 1984, set inserts
        oldVal = self.compLanes[plyr]
        newVal = ((oldVal << 3) & 0x08) | ((oldVal & 0x0e) >> 1)
        self.compLanes[plyr] = newVal
        change = newVal ^ oldVal
        if (change != 0):
            self.set_lane_lights(change, newVal)
        
    ## Flipper left rotate
    #
    #  Left rotate the LEDs properly depending on the mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def flipper_left_rotate(self, plyr):
        # Rotate 1984, set inserts
        oldVal = self.compLanes[plyr]
        newVal = ((oldVal >> 3) & 0x01) | ((oldVal & 0x07) << 1)
        self.compLanes[plyr] = newVal
        change = newVal ^ oldVal
        if (change != 0):
            self.set_lane_lights(change, newVal)

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
            self.compLanes[plyr] &= ~CustomFunc.LANE_ALL_MASK
            CustomFunc.GameData.StdFuncs.Led_Off(CustomFunc.CONST_1984)
            
            # Award 15 second ball save
            self.events |= self.EVENT_RELOAD_ACTIVE
            CustomFunc.GameData.StdFuncs.TimerUpdate(Timers.TIMEOUT_RELOAD_TIMER, 15000) 
            CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RELOAD_TIMER)
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SHOOT_AGAIN)
        CustomFunc.GameData.score[plyr] += ((unlit * 5) + (lit * 2) + (comp * 25))
        
    ## Process drop targets
    #
    #  Process drop targets and see if complete
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_drop_targets(self, plyr):
        if (self.events & CustomFunc.EVENT_DROP_COMPLETE) and CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_DROP_TRGT_TIMER):
            self.events &= ~(CustomFunc.EVENT_DROP_1ST | CustomFunc.EVENT_DROP_2ND | CustomFunc.EVENT_DROP_3RD | CustomFunc.EVENT_DROP_4TH | CustomFunc.EVENT_DROP_COMPLETE)
            CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_DROP_BANK)
        hit = 0
        comp = 1
        if ((self.events & CustomFunc.EVENT_DROP_1ST) == 0) and CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_1ST):
            hit += 1
            self.events |= CustomFunc.EVENT_DROP_1ST
        if ((self.events & CustomFunc.EVENT_DROP_2ND) == 0) and CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_2X):
            hit += 2
            self.events |= CustomFunc.EVENT_DROP_2ND
        if ((self.events & CustomFunc.EVENT_DROP_3RD) == 0) and CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_3X):
            hit += 3
            self.events |= CustomFunc.EVENT_DROP_3RD
        if ((self.events & CustomFunc.EVENT_DROP_4TH) == 0) and CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_DROP_TRGT_5X):
            hit += 5
            self.events |= CustomFunc.EVENT_DROP_4TH
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_SUPER_STAR_TRGT):
            print "Drops Complete!!"
            hit += 10
            comp += 1
            self.pollStatus |= CustomFunc.POLLSTAT_INLINE_COMP
            self.events |= CustomFunc.EVENT_DROP_COMPLETE
            self.events |= CustomFunc.EVENT_JUKEBOX_AVAIL
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_BLW_SAUCER)
            CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_DROP_TRGT_TIMER) 
        CustomFunc.GameData.score[plyr] += (hit * 5)
        
    ## Process spinner
    #
    #  Process spinner
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_spinner(self, plyr):
        if CustomFunc.GameData.StdFuncs.CheckMatrixInpState(InpBitNames.MTRX_INP_SPINNER):
            CustomFunc.GameData.score[plyr] += self.spinMult
            # double jukebox scores if spinner collected
            if ((self.stateProg[plyr] & CustomFunc.STATEPROG_JUKEBOX_COLLECTED) != 0):
                CustomFunc.GameData.score[plyr] += self.spinMult

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
                if (self.eddieCnt[plyr] == 0):
                    # Collected E1
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_E1)
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_D1)
                    CustomFunc.GameData.score[plyr] += 10
                elif (self.eddieCnt[plyr] == 1):
                    # Collected D1
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_D1)
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_D2)
                    CustomFunc.GameData.score[plyr] += 20
                elif (self.eddieCnt[plyr] == 2):
                    # Collected D2
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_D2)
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_I)
                    CustomFunc.GameData.score[plyr] += 30
                elif (self.eddieCnt[plyr] == 3):
                    # Collected I
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_I)
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_E2)
                    CustomFunc.GameData.score[plyr] += 40
                elif (self.eddieCnt[plyr] == 4):
                    # Collected E2
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_E2)
                    CustomFunc.GameData.score[plyr] += 50
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_EDDIE_COLLECTED
                    self.inc_spin_mult()
                    
                    # Stop the currently playing background song
                    CustomFunc.GameData.StdFuncs.StopBgnd()
                    self.events |= CustomFunc.EVENT_ERUPTION_ACTIVE
                    CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_ERUPTION_TIMER) 
                    CustomFunc.GameData.StdFuncs.PlayBgnd(BgndMusic.BGND_ERUPTION)
                    
                    if (self.singer[plyr] & CustomFunc.SNGR_DAVID) == 0:
                        if (self.stateProg[plyr] & (CustomFunc.STATEPROG_SAMMY_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                            CustomFunc.STATEPROG_ALEX_COLLECTED) == (CustomFunc.STATEPROG_SAMMY_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                            CustomFunc.STATEPROG_ALEX_COLLECTED)):
                            self.singer[plyr] |= CustomFunc.SNGR_DAVID
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_DAVID)
                    if (self.singer[plyr] & CustomFunc.SNGR_SAMMY) == 0:
                        if (self.stateProg[plyr] & (CustomFunc.STATEPROG_DAVID_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                            CustomFunc.STATEPROG_ALEX_COLLECTED) == (CustomFunc.STATEPROG_DAVID_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                            CustomFunc.STATEPROG_ALEX_COLLECTED)):
                            self.singer[plyr] |= CustomFunc.SNGR_SAMMY
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_R1)
                self.eddieCnt[plyr] += 1
                
        if (self.events & CustomFunc.EVENT_ERUPTION_ACTIVE):
            if (CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_ERUPTION_TIMER)):
                # Eruption song is complete, so restart the background song
                self.events &= ~CustomFunc.EVENT_ERUPTION_ACTIVE
                CustomFunc.GameData.StdFuncs.PlayBgnd(self.currSong[CustomFunc.GameData.currPlayer])
            
        
    ## Process Alex
    #
    #  Process Alex pops
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_alex(self, plyr):
        oldCnt = self.alexCnt[plyr]/10
        hit = 0
        comp = 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_LFT_POP):
            hit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_TOP_POP):
            hit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_BTM_POP):
            hit += 1
        if (hit != 0):
            # Play rotating drum sound
            CustomFunc.GameData.StdFuncs.Sounds((oldCnt % 3) + Sounds.SOUND_HOT_TEACHER1)
        
            if (self.stateProg[plyr] & CustomFunc.STATEPROG_ALEX_COLLECTED):
                CustomFunc.GameData.score[plyr] += (hit * 10)
            else:
                self.alexCnt[plyr] += hit
                CustomFunc.GameData.score[plyr] += (hit * 5)
                if (oldCnt != (self.alexCnt[plyr]/10)):
                    if (oldCnt == 0):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_A)
                        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_L)
                    elif (oldCnt == 1):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_L)
                        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_E)
                    elif (oldCnt == 2):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_E)
                        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_X)
                    elif (oldCnt == 3):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_X)
                        self.stateProg[plyr] |= CustomFunc.STATEPROG_ALEX_COLLECTED
                        self.inc_spin_mult()
                        if (self.singer[plyr] & CustomFunc.SNGR_DAVID) == 0:
                            if (self.stateProg[plyr] & (CustomFunc.STATEPROG_SAMMY_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                                CustomFunc.STATEPROG_ALEX_COLLECTED) == (CustomFunc.STATEPROG_SAMMY_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                                CustomFunc.STATEPROG_ALEX_COLLECTED)):
                                self.singer[plyr] |= CustomFunc.SNGR_DAVID
                                CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_DAVID)
                        if (self.singer[plyr] & CustomFunc.SNGR_SAMMY) == 0:
                            if (self.stateProg[plyr] & (CustomFunc.STATEPROG_DAVID_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                                CustomFunc.STATEPROG_ALEX_COLLECTED) == (CustomFunc.STATEPROG_DAVID_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                                CustomFunc.STATEPROG_ALEX_COLLECTED)):
                                self.singer[plyr] |= CustomFunc.SNGR_SAMMY
                                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_R1)

    ## Process David
    #
    #  Process David targets
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_david(self, plyr):
        unlit = 0
        lit = 0
        comp = 0
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_D1_TRGT):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                if self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_D1:
                    lit += 1
                else:
                    self.davidTrgts[plyr] |= CustomFunc.TRGT_DAVID_D1
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DAVID_D1)
                    unlit += 1
            else:
                unlit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_A_TRGT):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                if self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_A:
                    lit += 1
                else:
                    self.davidTrgts[plyr] |= CustomFunc.TRGT_DAVID_A
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DAVID_A)
                    unlit += 1
            else:
                unlit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_V_TRGT):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                if self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_V:
                    lit += 1
                else:
                    self.davidTrgts[plyr] |= CustomFunc.TRGT_DAVID_V
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DAVID_V)
                    unlit += 1
            else:
                unlit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_I_TRGT):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                if self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_I:
                    lit += 1
                else:
                    self.davidTrgts[plyr] |= CustomFunc.TRGT_DAVID_I
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DAVID_I)
                    unlit += 1
            else:
                unlit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_D2_TRGT):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                if self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_D2:
                    lit += 1
                else:
                    self.davidTrgts[plyr] |= CustomFunc.TRGT_DAVID_D2
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DAVID_D2)
                    unlit += 1
            else:
                unlit += 1
        if (lit != 0) or (unlit != 0):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                # Add score
                if (self.stateProg[plyr] & CustomFunc.STATEPROG_DAVID_COLLECTED):
                    CustomFunc.GameData.score[plyr] += ((lit + unlit) * 10)
                else:
                    CustomFunc.GameData.score[plyr] += ((lit * 2) + (unlit * 5))
            else:
                # Subtract score for hitting wrong targets
                CustomFunc.GameData.score[plyr] -= ((lit + unlit) * 5)
                if (CustomFunc.GameData.score[plyr] < 0):
                    CustomFunc.GameData.score[plyr] = 0
        if (unlit != 0):
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                # Check if David has been completed
                if (self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_ALL_MASK) == CustomFunc.TRGT_DAVID_ALL_MASK:
                    if (self.stateProg[plyr] & CustomFunc.STATEPROG_ROTH_COLLECTED) == 0:
                        # First time David has been collected so light Roth
                        # Turn off David Led's so they blink again
                        self.stateProg[plyr] |= CustomFunc.STATEPROG_ROTH_COLLECTED
                        self.davidTrgts[plyr] = 0
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROTH)
                        CustomFunc.GameData.StdFuncs.Led_Off(CustomFunc.CONST_DAVID)
                        CustomFunc.GameData.score[plyr] += 25
                    else:
                        # David and Roth collected so mark as complete
                        # If all other band members collected, Sammy can now be collected
                        self.stateProg[plyr] |= CustomFunc.STATEPROG_DAVID_COLLECTED
                        self.inc_spin_mult()
                        if (self.stateProg[plyr] & (CustomFunc.STATEPROG_DAVID_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                            CustomFunc.STATEPROG_ALEX_COLLECTED) == (CustomFunc.STATEPROG_DAVID_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                            CustomFunc.STATEPROG_ALEX_COLLECTED)):                        
                            self.singer[plyr] |= CustomFunc.SNGR_SAMMY
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_R1)
                        CustomFunc.GameData.score[plyr] += 50

    ## Process Sammy
    #
    #  Process Sammy saucer
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_sammy(self, plyr):
        if self.events & CustomFunc.EVENT_SAUCER_ACTIVE:
            if CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_SAUCER_TIMER):
                self.events &= ~CustomFunc.EVENT_SAUCER_ACTIVE
            elif CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_SAUCER_RETRY_TIMER):
                CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_SAUCER_RETRY_TIMER)
                if CustomFunc.GameData.StdFuncs.CheckMatrixInpState(InpBitNames.MTRX_INP_SAUCER):
                    CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_SAUCER)
        else:
            if CustomFunc.GameData.StdFuncs.CheckMatrixInpState(InpBitNames.MTRX_INP_SAUCER):
                if (self.events & CustomFunc.EVENT_JUKEBOX_AVAIL):
                    self.setup_jukebox(plyr)
                else:
                    if (self.singer[plyr] & CustomFunc.SNGR_SAMMY) == 0:
                        CustomFunc.GameData.score[plyr] -= 10
                    else:
                        if (self.sammyCnt[plyr] == 0):
                            # Collected R1
                            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_R1)
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_O)
                            CustomFunc.GameData.score[plyr] += 10
                        elif (self.sammyCnt[plyr] == 1):
                            # Collected O
                            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_O)
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_C)
                            CustomFunc.GameData.score[plyr] += 10
                        elif (self.sammyCnt[plyr] == 2):
                            # Collected C
                            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_C)
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_K)
                            CustomFunc.GameData.score[plyr] += 10
                        elif (self.sammyCnt[plyr] == 3):
                            # Collected K
                            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_K)
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_E)
                            CustomFunc.GameData.score[plyr] += 10
                        elif (self.sammyCnt[plyr] == 4):
                            # Collected E
                            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_E)
                            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_R2)
                            CustomFunc.GameData.score[plyr] += 10
                        elif (self.sammyCnt[plyr] == 5):
                            # Collected R2, after collecting Sammy, David can be collected
                            # if all other band members have been collected
                            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_R2)
                            self.stateProg[plyr] |= CustomFunc.STATEPROG_SAMMY_COLLECTED
                            self.inc_spin_mult()
                            if (self.stateProg[plyr] & (CustomFunc.STATEPROG_SAMMY_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                                CustomFunc.STATEPROG_ALEX_COLLECTED) == (CustomFunc.STATEPROG_SAMMY_COLLECTED | CustomFunc.STATEPROG_EDDIE_COLLECTED | \
                                CustomFunc.STATEPROG_ALEX_COLLECTED)):
                                self.singer[plyr] |= CustomFunc.SNGR_DAVID
                                CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_DAVID)
                            CustomFunc.GameData.score[plyr] += 50
                            
                        self.sammyCnt[plyr] += 1
                    self.saucer_kick()

    ## Process Panama
    #
    #  Process Panama captive ball
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_panama(self, plyr):
        if (self.events & CustomFunc.EVENT_PANAMA):
            if (CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_PANAMA_TIMER)):
                CustomFunc.GameData.StdFuncs.Led_Blink_Off([LedBitNames.LED_RGHT_HDLGHT_CRD0MSK, LedBitNames.LED_LFT_HDLGHT_CRD1MSK])
                self.events &= ~CustomFunc.EVENT_PANAMA
        
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_PANAMA_ROLL):
            CustomFunc.GameData.score[plyr] += 20
            self.events |= CustomFunc.EVENT_PANAMA
            
            CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_PANAMA_TIMER) 
            
            # Play Panama sound clip and blink car lights,
            CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_PANAMA)
            CustomFunc.GameData.StdFuncs.Led_Blink_100([LedBitNames.LED_RGHT_HDLGHT_CRD0MSK, LedBitNames.LED_LFT_HDLGHT_CRD1MSK])

    ## Process drain
    #
    #  Process drain
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_drain(self, plyr):
        if (self.events & self.EVENT_RELOAD_ACTIVE):
            if (CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_RELOAD_TIMER)):
                # Stop blinking the reload LED
                self.events &= ~self.EVENT_RELOAD_ACTIVE
                CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_SHOOT_AGAIN)
        
			# If the retry timer times out, and the ball is in the drain, serve it again,
			# then restart timeout retry
            if (CustomFunc.GameData.StdFuncs.Expired(Timers.TIMEOUT_RETRY_TIMER)):
                CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RETRY_TIMER)
                if (CustomFunc.GameData.StdFuncs.CheckMatrixInpState(InpBitNames.MTRX_INP_OUTHOLE)):
                    CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_OUTHOLE)
                    CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_GIMME_BREAK)
        else:
            if (CustomFunc.GameData.StdFuncs.CheckMatrixInpState(InpBitNames.MTRX_INP_OUTHOLE)):
                # Move to end ball mode
                CustomFunc.GameData.gameMode = State.STATE_END_BALL
            
    ## Process bumper
    #
    #  Process bumper
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_bumper(self, plyr):
        if (CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.MTRX_INP_REBND)):
            CustomFunc.GameData.score[plyr] += 1
    
    ## Normal processing
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def normal_proc(self, plyr):
        score =  CustomFunc.GameData.score[plyr]
        self.proc_inlanes(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "inlane score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_drop_targets(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "drop score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_spinner(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "spinner score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_eddie(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "eddie score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_alex(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "alex score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_david(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "david score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_sammy(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "sammy score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_drain(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "drain score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_bumper(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "bumper score"
            score =  CustomFunc.GameData.score[plyr]
        self.proc_panama(plyr)
        if (score != CustomFunc.GameData.score[plyr]):
            print "panama score"
            score =  CustomFunc.GameData.score[plyr]
                
    ## Change singer to Sammy
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Singer_Sammy(self):
        # Turn off David blink, turn on Sammy (Rocker) blink
        CustomFunc.GameData.StdFuncs.Led_Blink_Off(CustomFunc.CONST_DAVID)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_ROCKER)
        CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_SAMMYHAGAR)
        self.singer[CustomFunc.GameData.currPlayer] = self.SNGR_SAMMY

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
    def restore_eddie(self, plyr):
        if self.eddieCnt[plyr] == 0:
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_E1)
        elif self.eddieCnt[plyr] == 1:
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_EDDIE_E1)
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_D1)
        elif self.eddieCnt[plyr] == 2:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_EDDIE_E1_CRD0MSK, LedBitNames.LED_EDDIE_D1_CRD1MSK])
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_D2)
        elif self.eddieCnt[plyr] == 3:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_EDDIE_E1_CRD0MSK | LedBitNames.LED_EDDIE_D2_CRD0MSK, LedBitNames.LED_EDDIE_D1_CRD1MSK])
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_I)
        elif self.eddieCnt[plyr] == 4:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_EDDIE_E1_CRD0MSK | LedBitNames.LED_EDDIE_D2_CRD0MSK, LedBitNames.LED_EDDIE_D1_CRD1MSK | LedBitNames.LED_EDDIE_I_CRD1MSK])
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_EDDIE_E2)
        else:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_EDDIE_E1_CRD0MSK | LedBitNames.LED_EDDIE_D2_CRD0MSK | LedBitNames.LED_EDDIE_E2_CRD0MSK, LedBitNames.LED_EDDIE_D1_CRD1MSK | LedBitNames.LED_EDDIE_I_CRD1MSK])
        
    ## Restore Alex
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_alex(self, plyr):
        currAlex = self.alexCnt[plyr]/5
        if currAlex == 0:
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_A)
        elif currAlex == 1:
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ALEX_A)
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_L)
        elif currAlex == 2:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ALEX_A_CRD0MSK, LedBitNames.LED_ALEX_L_CRD1MSK])
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_E)
        elif currAlex == 3:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ALEX_A_CRD0MSK | LedBitNames.LED_ALEX_E_CRD0MSK, LedBitNames.LED_ALEX_L_CRD1MSK])
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ALEX_X)
        else:
            CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ALEX_A_CRD0MSK | LedBitNames.LED_ALEX_E_CRD0MSK | LedBitNames.LED_EDDIE_E2_CRD0MSK, LedBitNames.LED_ALEX_L_CRD1MSK | LedBitNames.LED_ALEX_X_CRD1MSK])
        
    ## Restore David
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_david(self, plyr):
        onBits = [0, 0]
        if (self.singer[plyr] & self.SNGR_DAVID):
            CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.CONST_DAVID)
            if (self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_D1) != 0:
                onBits[0] |= LedBitNames.LED_DAVID_D1_CRD0MSK
            if (self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_A) != 0:
                onBits[1] |= LedBitNames.LED_DAVID_A_CRD1MSK
            if (self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_V) != 0:
                onBits[0] |= LedBitNames.LED_DAVID_V_CRD0MSK
            if (self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_I) != 0:
                onBits[1] |= LedBitNames.LED_DAVID_I_CRD1MSK
            if (self.davidTrgts[plyr] & CustomFunc.TRGT_DAVID_D2) != 0:
                onBits[0] |= LedBitNames.LED_DAVID_D2_CRD0MSK
            if (self.stateProg[plyr] & CustomFunc.STATEPROG_ROTH_COLLECTED) != 0:
                onBits[0] |= LedBitNames.LED_ROTH_CRD0MSK
            if (self.stateProg[plyr] & CustomFunc.STATEPROG_DAVID_COLLECTED) != 0:
                onBits[0] |= (LedBitNames.LED_DAVID_D1_CRD0MSK | LedBitNames.LED_DAVID_V_CRD0MSK | LedBitNames.LED_DAVID_D2_CRD0MSK | LedBitNames.LED_ROTH_CRD0MSK)
                onBits[1] |= (LedBitNames.LED_DAVID_A_CRD1MSK | LedBitNames.LED_DAVID_I_CRD1MSK)
            CustomFunc.GameData.StdFuncs.Led_On(onBits)
            
    ## Restore Sammy
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_rocker(self, plyr):
        if (self.singer[plyr] & self.SNGR_SAMMY) and not (self.stateProg[plyr] & CustomFunc.STATEPROG_SAMMY_COLLECTED):
            if self.stateProg[plyr] & CustomFunc.STATEPROG_SAMMY_COLLECTED:
                CustomFunc.GameData.StdFuncs.Led_On(CustomFunc.CONST_ROCKER)
            else:
                if (self.sammyCnt[plyr] == 0):
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_R1)
                elif (self.sammyCnt[plyr] == 1):
                    CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROCKER_R1)
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_O)
                elif (self.sammyCnt[plyr] == 2):
                    CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ROCKER_R1_CRD0MSK | LedBitNames.LED_ROCKER_O_CRD0MSK])
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_C)
                elif (self.sammyCnt[plyr] == 3):
                    CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ROCKER_R1_CRD0MSK | LedBitNames.LED_ROCKER_O_CRD0MSK, LedBitNames.LED_ROCKER_C_CRD1MSK])
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_K)
                elif (self.sammyCnt[plyr] == 4):
                    CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ROCKER_R1_CRD0MSK | LedBitNames.LED_ROCKER_O_CRD0MSK | LedBitNames.LED_ROCKER_K_CRD0MSK, LedBitNames.LED_ROCKER_C_CRD1MSK])
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_E)
                elif (self.sammyCnt[plyr] == 5):
                    CustomFunc.GameData.StdFuncs.Led_On([LedBitNames.LED_ROCKER_R1_CRD0MSK | LedBitNames.LED_ROCKER_O_CRD0MSK | LedBitNames.LED_ROCKER_K_CRD0MSK, LedBitNames.LED_ROCKER_C_CRD1MSK | LedBitNames.LED_ROCKER_E_CRD1MSK])
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_ROCKER_R2)
        
    ## Restore 1984
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def restore_1984(self, plyr):
        newVal = self.compLanes[plyr]
        if (newVal != 0):
            self.set_lane_lights(newVal, newVal)

    ## Increase spin multiplier
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def inc_spin_mult(self):
        self.spinMult += 1
        if (self.spinMult == 2):
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_2X_BONUS)
        elif (self.spinMult == 3):
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_3X_BONUS)
        elif (self.spinMult == 4):
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_4X_BONUS)

    ## Set up jukebox mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def setup_jukebox(self, plyr):
        # Update songs collected if David or Sammy have been collected
        if self.stateProg[plyr] & CustomFunc.STATEPROG_DAVID_COLLECTED:
            self.availSongs[plyr] |= 0x3f
        if self.stateProg[plyr] & CustomFunc.STATEPROG_SAMMY_COLLECTED:
            self.availSongs[plyr] |= 0xfc0
        # If no singers have been collected, only allow current singer songs
        if self.availSongs[plyr] == 0:
            if self.singer[plyr] & CustomFunc.SNGR_DAVID:
                self.availSongs[plyr] |= 0x3f
            else:
                self.availSongs[plyr] |= 0xfc0
    
        self.events &= ~CustomFunc.EVENT_JUKEBOX_AVAIL
        self.stateProg[plyr] |= CustomFunc.STATEPROG_JUKEBOX_COLLECTED
        
        self.inc_spin_mult()
        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_SPINNER)
        CustomFunc.GameData.StdFuncs.StopBgnd()
        CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_CHOOSE_JUKEBOX)
        CustomFunc.GameData.gameMode = State.STATE_JUKEBOX

    ## Saucer kick
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def saucer_kick(self):
        self.events |= CustomFunc.EVENT_SAUCER_ACTIVE
        CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_SAUCER)
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_SAUCER_TIMER) 
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_SAUCER_RETRY_TIMER) 
        
