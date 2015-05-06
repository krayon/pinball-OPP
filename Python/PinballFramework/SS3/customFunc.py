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
from SS3.inpBitNames import InpBitNames
from SS3.solBitNames import SolBitNames
from SS3.sounds import Sounds
from SS3.ledBitNames import LedBitNames
from SS3.timers import Timers
import random
import rs232Intf
from SS3.states import State
from dispConstIntf import DispConst

## Custom functions class.
#  Contains all the custom rules and functions that are specific this this set
#  of pinball rules.  These are not created or generated from GenPyCode.
class CustomFunc:
    STATE_SKILL_SHOT = 0
    STATE_NONE = 1
    STATE_CHOOSE_MODE = 2
    STATE_MODE_ACTIVE = 3
    STATE_MODE_JKPOT_AVAIL = 4
    
    STATEPROG_NONE = 0x00
    STATEPROG_INLANES_COLLECTED = 0x01
    STATEPROG_SHOOTER_COLLECTED = 0x02
    STATEPROG_KICKOUTHOLE_COLLECTED = 0x04

    MODE_CALL_POSSE = 0
    MODE_HUSTLE_JIVE = 1
    MODE_TARGET_PRACTICE = 2
    MODE_CHECK_HIDEOUTS = 3
    MODE_SNIPER = 4
    MODE_SHARPE_ATTACK = 5
    MODE_TRACK_BANDITS = 6
    MODE_KILL_EM_ALL = 7
    MODE_BAR_FIGHT = 8
    MODE_DUEL = 9
    MODE_RIDE_FOR_HELP = 10
    MODE_NUM_MODES = 11
    
    LEVEL_EASY = 0
    LEVEL_MED = 1
    LEVEL_HARD = 2
    LEVEL_WIZARD = 3
    
    _reverseLookup = [ 0x0, 0x8, 0x4, 0xc, 0x2, 0xa, 0x6, 0xe, 0x1, 0x9, 0x5, 0xd, 0x3, 0xb, 0x7, 0xf]
   
    INLNSAVE_INLANE_MASK = 0xe7
    INLNSAVE_HORSESHOE = 0x10
    
    MODETRGT_POP_BUMPER = 0
    MODETRGT_DROP_TRGT = 1
    MODETRGT_INLANE = 2
    MODETRGT_SPINNER = 3 
    MODETRGT_KICKOUT_HOLE = 4 
    
    MODETRKBNDT_INLANES = 0
    MODETRKBNDT_TARGETS = 0
    
    # Used to note big events that happen during a poll cycle (bitfield)
    POLLSTAT_INLANE_COMP = 0x01
    POLLSTAT_COMP_DROPS = 0x02
    POLLSTAT_HIT_SKILLSHOT = 0x04
    POLLSTAT_HIT_DROP = 0x08
    
    tilted = False
    
    ## Initialize CustomFunc class
    #
    #  Initialize custom functions class
    #
    #  @param  self          [in]   Object reference
    #  @param  gameData      [in]   Object reference
    #  @return None
    def __init__(self, gameData):
        CustomFunc.GameData = gameData
        CustomFunc.tilted = False
        self.state = [CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT]
        self.stateProg = [CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE]
        self.level = [CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY]
        CustomFunc.modeLedLkup = [LedBitNames.LED_MODE_POSSE, LedBitNames.LED_MODE_HUSTLEJIVE, LedBitNames.LED_MODE_TRGTPRAC, LedBitNames.LED_MODE_CHKHIDE, \
            LedBitNames.LED_MODE_SNIPER, LedBitNames.LED_MODE_SHARPE, LedBitNames.LED_MODE_TRKBNDT, LedBitNames.LED_MODE_KILLALL, \
            LedBitNames.LED_MODE_BARFGHT, LedBitNames.LED_MODE_DUEL, LedBitNames.LED_MODE_RIDEHELP ]
        self.compModes = [0, 0, 0, 0]
        self.compInlanes = [0, 0, 0, 0]
        self.dropTrgtGoal = [0, 0, 0, 0]
        self.numSkillShots = [0, 0, 0, 0]
        self.selectMode = 0
        self.mode = [CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE]
        self.spinMult = 1
        self.numSpin = 0
        self.tiltActive = False
        self.disableRotate = False
        self.saveModeState = [0, 0, 0, 0]
        self.saveModeData = [0, 0, 0, 0]
        self.saveModeValue = 0
        self.pollStatus = 0
        self._initFuncTbl = [self.init_call_posse, self.init_hustle_jive, self.init_target_practice, self.init_check_hideouts,
            self.init_sniper, self.init_sharpe_attack, self.init_track_bandits, self.init_kill_em_all,
            self.init_bar_fight, self.init_duel, self.init_ride_for_help]
        self._procFuncTbl = [self.proc_call_posse, self.proc_hustle_jive, self.proc_target_practice, self.proc_check_hideouts,
            self.proc_sniper, self.proc_sharpe_attack, self.proc_track_bandits, self.proc_kill_em_all,
            self.proc_bar_fight, self.proc_duel, self.proc_ride_for_help]
        self._compInlaneScore = [50, 75, 100, 150]
        self._compModeScore = [500, 750, 1000, 1500]
        self.dropHit = 0
        self.totDrops = 0
        
    ## Initialize game
    #
    #  Initialize the game variables
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def init_game(self):
        self.state = [CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT]
        self.stateProg = [CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE]
        self.level = [CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY]
        self.compModes = [0, 0, 0, 0]
        self.compInlanes = [0, 0, 0, 0]
        self.numSkillShots = [0, 0, 0, 0]
        self.selectMode = 0
        self.mode = [CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE]
        self.spinMult = 1
        self.numSpin = 0
        self.tiltActive = False
        self.disableRotate = False
        self.saveModeState = [0, 0, 0, 0]
        self.GameData.currPlayer = 0
        self.GameData.currPlyrDisp = 1
        self.GameData.creditBallNumDisp = 1
        self.GameData.ballNum = 0
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER_NUM] = False
        CustomFunc.GameData.blankDisp[DispConst.DISP_CREDIT_BALL_NUM] = False
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER2] = True
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER3] = True
        CustomFunc.GameData.blankDisp[DispConst.DISP_PLAYER4] = True

    ## Start next ball
    #
    #  Start the next ball, and reset LEDs
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def start_next_ball(self, plyr):
        # First fill in level
        leds = 0
        mask = [0, 0, 0, LedBitNames.LED_ROOKIE | LedBitNames.LED_DEPUTY | LedBitNames.LED_SHERIFF | LedBitNames.LED_MARSHAL | LedBitNames.LED_SHOOT_AGAIN]
        if (self.level[plyr] == CustomFunc.LEVEL_EASY):
            leds = LedBitNames.LED_ROOKIE
        elif (self.level[plyr] == CustomFunc.LEVEL_MED):
            leds = LedBitNames.LED_ROOKIE | LedBitNames.LED_DEPUTY
        elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
            leds = LedBitNames.LED_ROOKIE | LedBitNames.LED_DEPUTY | LedBitNames.LED_SHERIFF
        elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
            leds = LedBitNames.LED_ROOKIE | LedBitNames.LED_DEPUTY | LedBitNames.LED_SHERIFF | LedBitNames.LED_MARSHAL
        CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, 0, 0, leds])
        
        # Set the completed modes
        mask = [0, 0, LedBitNames.LED_MODE_RIDEHELP | LedBitNames.LED_MODE_DUEL | LedBitNames.LED_MODE_BARFGHT | LedBitNames.LED_MODE_KILLALL | LedBitNames.LED_MODE_TRKBNDT,
            0, LedBitNames.LED_MODE_POSSE | LedBitNames.LED_MODE_HUSTLEJIVE | LedBitNames.LED_MODE_TRGTPRAC | LedBitNames.LED_MODE_CHKHIDE | LedBitNames.LED_MODE_SNIPER | LedBitNames.LED_MODE_SHARPE]
        # Bits are oriented so reversed bits are in proper position
        leds = self.reverseByte((self.compModes[plyr] & 0x7c0) >> 6)
        ledList = [0, 0, 0x20000 | leds, 0, 0x40000 | ((self.compModes[plyr] & 0x3f) << 2)] 
        CustomFunc.GameData.StdFuncs.Led_Set(mask, ledList)
    
        # Set the inlanes if easy or medium
        if (self.level[plyr] == CustomFunc.LEVEL_EASY) or (self.level[plyr] == CustomFunc.LEVEL_MED):
            if ((self.compInlanes[plyr] & LedBitNames.LED_INLN_CTR) == LedBitNames.LED_INLN_CTR):
                # The center inlane is already complete.  Move that bit to another position if possible
                if ((self.compInlanes[plyr] & LedBitNames.LED_INLN_RGHT) == 0):
                    self.compInlanes[plyr] &= ~LedBitNames.LED_INLN_CTR
                    self.compInlanes[plyr] |= LedBitNames.LED_INLN_RGHT
                elif ((self.compInlanes[plyr] & LedBitNames.LED_INLN_LFT) == 0):
                    self.compInlanes[plyr] &= ~LedBitNames.LED_INLN_CTR
                    self.compInlanes[plyr] |= LedBitNames.LED_INLN_LFT
                elif (self.level[plyr] == CustomFunc.LEVEL_EASY):
                    # On easy, can rotate between both levels so find clear one on the lower rollovers.
                    if ((self.compInlanes[plyr] & LedBitNames.LED_ROLL_RGHT) == 0):
                        self.compInlanes[plyr] &= ~LedBitNames.LED_INLN_CTR
                        self.compInlanes[plyr] |= LedBitNames.LED_ROLL_RGHT
                    elif ((self.compInlanes[plyr] & LedBitNames.LED_ROLL_CTR) == 0):
                        self.compInlanes[plyr] &= ~LedBitNames.LED_INLN_CTR
                        self.compInlanes[plyr] |= LedBitNames.LED_ROLL_CTR
                    elif ((self.compInlanes[plyr] & LedBitNames.LED_ROLL_LFT) == 0):
                        self.compInlanes[plyr] &= ~LedBitNames.LED_INLN_CTR
                        self.compInlanes[plyr] |= LedBitNames.LED_ROLL_LFT
                     
            mask = [0, LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT]
            CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, self.compInlanes[plyr]])
        else:
            self.compInlanes[plyr] = 0
            CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT)

        # Turn off all the drop target LEDs
        CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED6_ALL_BITS_MSK)

        # Blink the skill shot
        # HRS:  This should blink regardless of if the center target has been hit or not            
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_CTR)
        
        # Reset the spinner kickout hole LEDs, 
        self.spinMult = 1
        self.numSpin = 0
        CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED1_ALL_BITS_MSK)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SHOOT_AGAIN)
        CustomFunc.GameData.StdFuncs.Kick(SolBitNames.SOL_BALL_IN_PLAY)
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RELOAD_TIMER)
        CustomFunc.GameData.StdFuncs.Start(Timers.TIMEOUT_RETRY_TIMER)
        CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_LFT_OUTLN | LedBitNames.LED_LFT_INLN)
        self.state[plyr] = CustomFunc.STATE_SKILL_SHOT

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
        # In easy mode inlanes are retained for next ball, mode completes on ball end.
        # self.compInlanes[plyr] are kept up to date during play, so don't need to store here
        if (self.level[plyr] == CustomFunc.LEVEL_EASY):
            if (self.state[plyr] == CustomFunc.STATE_MODE_ACTIVE):
                self.compModes[plyr] |= (1 << self.mode[plyr])
                self.stateProg[plyr] = 0
        # In medium mode, inlanes are retained, and mode is continued if currently in a mode
        # Kickout hole must be sunk again to restart mode 
        elif (self.level[plyr] == CustomFunc.LEVEL_MED):
            pass
        # In hard mode, progress and inlanes are reset
        elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
            self.stateProg[plyr] = CustomFunc.STATEPROG_NONE
            self.compInlanes[plyr] = 0
        # In wizard mode, absolutely everything is reset including modes
        elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
            self.stateProg[plyr] = CustomFunc.STATEPROG_NONE
            self.compInlanes[plyr] = 0
            self.compModes[plyr] = 0
        
        # Calculate bonus, HRS must add complete mode bonus
        if not CustomFunc.tilted:
            print "Collect spinner bonus %d x %d" % (self.spinMult, self.numSpin)
            CustomFunc.GameData.score[plyr] += (self.spinMult * self.numSpin)
    
    ## Reverse byte
    #
    #  Reverse bits in a byte
    #
    #  @param  self          [in]   Object reference
    #  @param  data          [in]   Data to reverse
    #  @return None
    def reverseByte(self, data):
        return((CustomFunc._reverseLookup[data & 0xf] << 4) | CustomFunc._reverseLookup[data >> 4])
        
    ## Flipper right rotate
    #
    #  Right rotate the LEDs properly depending on the mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def flipper_right_rotate(self, plyr):
        # Normal states where rotation of inlanes can happen
        if (self.state[plyr] == CustomFunc.STATE_SKILL_SHOT) or (self.state[plyr] == CustomFunc.STATE_NONE) or (self.state[plyr] == CustomFunc.STATE_MODE_JKPOT_AVAIL):
            mask = [0, LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT]
            
            # If easy, rotate allows rotate between both levels
            if (self.level[plyr] == CustomFunc.LEVEL_EASY):
                leds = ((self.compInlanes[plyr] >> 1) & 0x63) | ((self.compInlanes[plyr] & 0x20) >> 3) | ((self.compInlanes[plyr] & 0x01) << 7)
                CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, leds])
                self.compInlanes[plyr] = leds
                
            # Can only rotate within the row
            elif (self.level[plyr] == CustomFunc.LEVEL_MED):
                leds = ((self.compInlanes[plyr] >> 1) & 0x63) | ((self.compInlanes[plyr] & 0x20) << 2) | ((self.compInlanes[plyr] & 0x01) << 2)
                CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, leds])
                self.compInlanes[plyr] = leds
                
            # No rotation allowed
            elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
                pass
            
            # HRS:  No idea what to do in wizard mode
            elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
                pass
            
        elif (self.state[plyr] == CustomFunc.STATE_CHOOSE_MODE):
            # Rotate blinking LED to indicate mode to choose
            oldMode = self.selectMode
            foundNew = False
            
            # Look for a new mode.  First look for higher numbered modes
            for index in xrange(oldMode + 1, CustomFunc.MODE_NUM_MODES):
                if ((self.compModes[plyr] & (1 << index)) == 0):
                    self.selectMode = index
                    foundNew = True
                    break
            
            # If didn't find a higher number mode, look for lower numbered ones
            if not foundNew:
                for index in xrange(CustomFunc.MODE_NUM_MODES):
                    if ((self.compModes[plyr] & (1 << index)) == 0):
                        self.selectMode = index
                        break
            
            # If new mode doesn't equal old mode (i.e. only one mode left)
            if (oldMode != self.selectMode):
                CustomFunc.GameData.StdFuncs.Led_Blink_Off(CustomFunc.modeLedLkup[oldMode])
                CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.modeLedLkup[self.selectMode])
                    
        # Rotate may or may not happen depending on mode
        elif (self.state[plyr] == CustomFunc.STATE_MODE_ACTIVE):
            pass

        
    ## Flipper left rotate
    #
    #  Left rotate the LEDs properly depending on the mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def flipper_left_rotate(self, plyr):
        # Normal states where rotation of inlanes can happen
        if (self.state[plyr] == CustomFunc.STATE_SKILL_SHOT) or (self.state[plyr] == CustomFunc.STATE_NONE) or (self.state[plyr] == CustomFunc.STATE_MODE_JKPOT_AVAIL):
            mask = [0, LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT]
            
            # If easy, rotate allows rotate between both levels
            if (self.level[plyr] == CustomFunc.LEVEL_EASY):
                leds = ((self.compInlanes[plyr] << 1) & 0xc6) | ((self.compInlanes[plyr] & 0x80) >> 7) | ((self.compInlanes[plyr] & 0x04) << 3)
                CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, leds])
                self.compInlanes[plyr] = leds
                
            # Can only rotate within the row
            elif (self.level[plyr] == CustomFunc.LEVEL_MED):
                leds = ((self.compInlanes[plyr] << 1) & 0xc6) | ((self.compInlanes[plyr] & 0x80) >> 2) | ((self.compInlanes[plyr] & 0x04) >> 2)
                CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, leds])
                self.compInlanes[plyr] = leds
                
            # No rotation allowed in hard level
            elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
                pass
            
            # No rotation allowed in wizard level
            elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
                pass
            
        elif (self.state[plyr] == CustomFunc.STATE_CHOOSE_MODE):
            # Left flipper chooses the mode, LED is already blinking, so no changes needed
            self.mode[plyr] = self.selectMode
            self.state[plyr] = CustomFunc.STATE_MODE_ACTIVE
            
            # Initialize the mode function
            self._initFuncTbl[self.mode[plyr]](plyr, False)
            CustomFunc.GameData.gameMode = State.MODE_MODE_ACTIVE
                    
        # Rotate may or may not happen depending on mode
        elif (self.state[plyr] == CustomFunc.STATE_MODE_ACTIVE):
            pass

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
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_LFT_ROLLOVER):
            if (self.compInlanes[plyr] & LedBitNames.LED_INLN_LFT & 0xffff) == 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_INLN_LFT)
                self.compInlanes[plyr] |= (LedBitNames.LED_INLN_LFT & 0xffff)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_CTR_ROLLOVER):
            if (self.compInlanes[plyr] & LedBitNames.LED_INLN_CTR & 0xffff) == 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_INLN_CTR)
                self.compInlanes[plyr] |= (LedBitNames.LED_INLN_CTR & 0xffff)
                unlit += 1
                self.pollStatus |= CustomFunc.POLLSTAT_HIT_SKILLSHOT
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_RGHT_ROLLOVER):
            if (self.compInlanes[plyr] & LedBitNames.LED_INLN_RGHT & 0xffff) == 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_INLN_RGHT)
                self.compInlanes[plyr] |= (LedBitNames.LED_INLN_RGHT & 0xffff)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_CTR_LFT_ROLLOVER):
            if (self.compInlanes[plyr] & LedBitNames.LED_ROLL_LFT & 0xffff) == 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROLL_LFT)
                self.compInlanes[plyr] |= (LedBitNames.LED_ROLL_LFT & 0xffff)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_CTR_CTR_ROLLOVER):
            if (self.compInlanes[plyr] & LedBitNames.LED_ROLL_CTR & 0xffff) == 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROLL_CTR)
                self.compInlanes[plyr] |= (LedBitNames.LED_ROLL_CTR & 0xffff)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_CTR_RGHT_ROLLOVER):
            if (self.compInlanes[plyr] & LedBitNames.LED_ROLL_RGHT & 0xffff) == 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_ROLL_RGHT)
                self.compInlanes[plyr] |= (LedBitNames.LED_ROLL_RGHT & 0xffff)
                unlit += 1
            else:
                lit += 1
        if (self.compInlanes[plyr] & (LedBitNames.LED_INLN_LFT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_RGHT | LedBitNames.LED_ROLL_LFT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_RGHT)) == \
                (LedBitNames.LED_INLN_LFT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_RGHT | LedBitNames.LED_ROLL_LFT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_RGHT) & 0xffff:
            print "Inlanes Complete!!"
            comp += 1
            self.compInlanes[plyr] = 0
            CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_INLN_LFT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_RGHT | LedBitNames.LED_ROLL_LFT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_RGHT)
            self.pollStatus |= CustomFunc.POLLSTAT_INLANE_COMP
        CustomFunc.GameData.score[plyr] += ((unlit * 5) + (lit * 2) + (comp * self._compInlaneScore[self.level[plyr]]))
        
    ## Process drop targets
    #
    #  Process drop targets and see if complete
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def proc_drop_targets(self, plyr):
        unlit = 0
        lit = 0
        self.dropHit = 0
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_1S):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_1)
            self.dropHit |= LedBitNames.LED_DT_1
            self.totDrops |= LedBitNames.LED_DT_1
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_1) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_1)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_2H):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_2)
            self.dropHit |= LedBitNames.LED_DT_2
            self.totDrops |= LedBitNames.LED_DT_2
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_2) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_2)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_3O):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_3)
            self.dropHit |= LedBitNames.LED_DT_3
            self.totDrops |= LedBitNames.LED_DT_3
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_3) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_3)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_4O):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_4)
            self.dropHit |= LedBitNames.LED_DT_4
            self.totDrops |= LedBitNames.LED_DT_4
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_4) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_4)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_5T):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_5)
            self.dropHit |= LedBitNames.LED_DT_5
            self.totDrops |= LedBitNames.LED_DT_5
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_5) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_5)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_6E):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_6)
            self.dropHit |= LedBitNames.LED_DT_6
            self.totDrops |= LedBitNames.LED_DT_6
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_6) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_6)
                unlit += 1
            else:
                lit += 1
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_DROP_TRGT_7R):
            self.pollStatus |= CustomFunc.POLLSTAT_HIT_DROP
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_7)
            self.dropHit |= LedBitNames.LED_DT_7
            self.totDrops |= LedBitNames.LED_DT_7
            if (self.dropTrgtGoal[plyr] & LedBitNames.LED_DT_7) != 0:
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_DT_7)
                unlit += 1
            else:
                lit += 1
        if (self.totDrops == (LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | LedBitNames.LED_DT_4 | 
                LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7)):
            print "Drops Complete!!"
            self.pollStatus |= CustomFunc.POLLSTAT_COMP_DROPS
            self.totDrops = 0
            CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_INLN_LFT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_RGHT | LedBitNames.LED_ROLL_LFT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_RGHT)
        CustomFunc.GameData.score[plyr] += ((unlit * 5) + (lit * 2))
        
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
            
    ## Init call posse
    #
    #  Initialize call posse mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Spinner lane 10 spins, then kickout hole.  Future: gives two ball multiball
    #
    #  State contains number of spins already counted
    def init_call_posse(self, plyr, restoreState):
        # Blink spinner lane
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SPINNER)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_POSSE)
        
        # If restoring, 
        if restoreState:
            if (self.saveModeState[plyr] >= 10):
                self.saveModeState[plyr] = 9
        else:
            self.saveModeState[plyr] = 0
    
    ## Init hustle and jive
    #
    #  Initialize hustle and jive mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Turn off tilt bob.  Disable rotate of inlanes using flippers.  Mode is
    #  successfully completed when all the lanes have been entered
    #
    #  State contains inlanes that have already been completed
    def init_hustle_jive(self, plyr, restoreState):
        # Blink non-lit inlanes
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
            LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_HUSTLEJIVE)
        self.disableRotate = True
        if restoreState:
            self.compInlanes[plyr] = self.saveModeState[plyr]
        else:
            self.compInlanes[plyr] = 0
            self.saveModeState[plyr] = 0
    
    ## Init target practice
    #
    #  Initialize target practice mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Blink random pop, random shooter target, random inlane,
    #  spinner orbit, then finish with kickout hole.
    #
    #  State contains next thing to hit.
    def init_target_practice(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_TRGTPRAC)
        if restoreState:
            # If only had to hit the kickout hole, move back to hit spinner
            if (self.saveModeState[plyr] == CustomFunc.MODETRGT_KICKOUT_HOLE):
                self.saveModeState[plyr] = CustomFunc.MODETRGT_SPINNER
        else:
            self.saveModeState[plyr] = CustomFunc.MODETRGT_POP_BUMPER
        if self.saveModeState[plyr] == CustomFunc.MODETRGT_POP_BUMPER:
            # Pick the pop bumper that must be hit
            randomNum = random.randint(0, 3)
            # Blink the pop bumper
            lowBit = randomNum & 0x01
            if ((self.saveModeValue & 0x02) != 0):
                # Randomly pick an upper pop bumper
                self.saveModeValue = SolBitNames.SOL_UPPER_LFT_POP + lowBit
                CustomFunc.GameData.StdFuncs.Led_Blink_100(0x10000 | (0x08 << lowBit))
            else:
                # Randomly pick an lower pop bumper
                self.saveModeValue = SolBitNames.SOL_BTM_LOW_POP + lowBit
                CustomFunc.GameData.StdFuncs.Led_Blink_100(0x20000 | (0x01 << lowBit))
        elif self.saveModeState[plyr] == CustomFunc.MODETRGT_DROP_TRGT:
            # Pick the drop that must be hit.  Blink the drop target
            self.saveModeValue = random.randint(0, 6)
            CustomFunc.GameData.StdFuncs.Led_Blink_100(0x50000 | (0x80 >> self.saveModeValue))
        elif self.saveModeState[plyr] == CustomFunc.MODETRGT_INLANE:
            # Pick the inlane that must be hit.
            self.disableRotate = True
            self.saveModeValue = random.randint(0, 5)
            if (self.saveModeValue < 3):
                CustomFunc.GameData.StdFuncs.Led_Blink_100(0x10000 | (0x01 << self.saveModeValue))
            else:
                CustomFunc.GameData.StdFuncs.Led_Blink_100(0x10000 | (0x04 << self.saveModeValue))
        elif self.saveModeState[plyr] == CustomFunc.MODETRGT_SPINNER:
            # Blink the spinner
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SPINNER)
    
    ## Init check hideouts
    #
    #  Initialize check hideouts mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Must get two standup targets 5 times each within 60s.  Top target is a cave, while
    #  the lower target is an abandoned house.  Blink top left pop bumper to indicate where shots
    #  should be aimed.  (Verbal callouts will happen to indicate which target is needs to be hit
    #  the most.)
    #
    #  State contains number of times standups have been hit.  Upper 16 bits contains number of
    #  times cave has been hit, lower 16 bits contains number of times abandoned house has been
    #  hit.
    def init_check_hideouts(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_CHKHIDE)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_POP_UPLFT)
        if restoreState:
            if (self.saveModeState[plyr] >> 16) >= (self.saveModeState[plyr] & 0xffff):
                # Play sound "Look in the abandoned house"
                pass
            else:
                # Play sound "Go check out the abandoned mine"
                pass
        else:
            self.saveModeState[plyr] = 0
            # Play sound "Look in the bandit hideouts"
        # HRS:  Start timeout to play sound every 10s to indicate what target needs hit most
    
    ## Init sniper
    #
    #  Initialize sniper mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Disable pop bumpers.  Can only hit blinking shooter target,
    #  then next one, etc.  Hit 5 individual targets completes the mode.  In
    #  easy and medium mode, the target next to the blinking target can be
    #  hit without failing the mode.
    #
    #  State contains number of standups that have successfully been hit
    def init_sniper(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_SNIPER)
        
        # Pick the drop that must be hit.  Blink the drop target
        if not restoreState:
            self.saveModeState[plyr] = 0
        self.saveModeValue = random.randint(0, 6)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(0x50000 | (0x80 >> self.saveModeValue))
    
    ## Init Sharpe attack
    #
    #  Initialize Sharpe attack mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Disable pop bumpers.  Can only hit blinking shooter target,
    #  then next one, etc.  Hit 5 individual targets completes the mode.  In
    #  easy and medium mode, the target next to the blinking target can be
    #  hit without failing the mode.  No cradling is allowed.
    #
    #  State contains number of standups that have successfully been hit
    def init_sharpe_attack(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_SHARPE)
        # HRS:  Disable cradling
        # Reset drop targets
        
        # Pick the drop that must be hit.  Blink the drop target
        if not restoreState:
            self.saveModeState[plyr] = 0
        self.saveModeValue = random.randint(0, 6)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(0x50000 | (0x80 >> self.saveModeValue))

    ## Init track bandits
    #
    #  Initialize track bandits mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Collect all lanes (may use flippers to rotate depending on level).
    #  Jackpot lane must also be collected, then knock down all the shooter targets.
    #
    #  State contains if shooting for inlanes or drop targets.  Data contains
    #  inlanes that have already been completed.
    def init_track_bandits(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_TRKBNDT)
    
        if restoreState:
            self.compInlanes[plyr] = self.saveModeData[plyr] & CustomFunc.INLNSAVE_INLANE_MASK
        else:
            self.saveModeState[plyr] = CustomFunc.MODETRKBNDT_INLANES
            self.saveModeData[plyr] = 0
            
        if self.saveModeState[plyr] == CustomFunc.MODETRKBNDT_INLANES:
            # Blink inlanes
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT)
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_HORSESHOE)
            if ((self.saveModeData[plyr] & CustomFunc.INLNSAVE_HORSESHOE) != 0):
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_HORSESHOE)
        else:
            # Blink drop targets
            self.dropTrgtGoal[plyr] = LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | \
                LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | 
                LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7)
            
    ## Init kill em all
    #
    #  Initialize kill em all mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Drop all shooter targets 3 times.  60 sec to drop bank.
    #  Resets timer when bank is finished.
    #
    #  State contains number of drop targets banks that have successfully been completed
    def init_kill_em_all(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_KILLALL)
        
        # Blink drop targets
        self.dropTrgtGoal[plyr] = LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | \
            LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | 
            LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7)
    
        if not restoreState:
            self.saveModeData[plyr] = 0
    
    ## Init bar fight
    #
    #  Initialize bar fight mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Hit each pop bumper 10 times.  Each time bumper is hit,
    #  light in bumper is lit 10% more time.  10 hits are full on.
    #
    #  State contains number of pop bumper hits.  Each pop bumper is in a
    #  single byte.
    def init_bar_fight(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_BARFGHT)
        
        # Blink pop bumpers
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_POP_UPCTR | LedBitNames.LED_POP_UPLFT)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_POP_BTMUP | LedBitNames.LED_POP_BTMLOW)

        if restoreState:
            # Disable pop bumpers if completed
            if ((self.saveModeData[plyr] & 0xff) > 9):
                CustomFunc.GameData.StdFuncs.Change_Solenoid_Cfg(SolBitNames.SOL_BTM_LOW_POP, [rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00'])
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_POP_BTMLOW)
            if (((self.saveModeData[plyr] >> 8) & 0xff) > 9):
                CustomFunc.GameData.StdFuncs.Change_Solenoid_Cfg(SolBitNames.SOL_BTM_UP_POP, [rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00'])
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_POP_BTMUP)
            if (((self.saveModeData[plyr] >> 16) & 0xff) > 9):
                CustomFunc.GameData.StdFuncs.Change_Solenoid_Cfg(SolBitNames.SOL_UPPER_CTR_POP, [rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00'])
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_POP_UPCTR)
            if (((self.saveModeData[plyr] >> 24) & 0xff) > 9):
                CustomFunc.GameData.StdFuncs.Change_Solenoid_Cfg(SolBitNames.SOL_UPPER_LFT_POP, [rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00'])
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_POP_UPLFT)
        else:
            self.saveModeData[plyr] = 0
    
    ## Init duel
    #
    #  Initialize duel mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Hit flashing shooter target within certain amount of time.
    def init_duel(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_DUEL)

        # Pick the drop that must be hit.  Blink the drop target
        self.saveModeValue = random.randint(0, 6)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(0x50000 | (0x80 >> self.saveModeValue))
        
        # HRS:  Start duel timer
    
    ## Init ride for help
    #
    #  Initialize ride for help mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Five orbits, then sink kickout hole.  Future:  Gives two ball multiball.
    def init_ride_for_help(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_RIDEHELP)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_HORSESHOE)
        
        if not restoreState:
            self.saveModeData[plyr] = 0

    ## Process skillshot
    #
    #  Process skillshot
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Skillshot gives next advance towards mode in easy and medium.  In hard
    #  and wizard, it only gives points
    def proc_skillshot(self, plyr):
        self.proc_inlanes(plyr)
        moveNextMode = False
        
        # Check if skillshot made
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_CTR_ROLLOVER):
            self.numSkillShots[plyr] += 1
            if (self.numSkillShots[plyr] & 1 != 0):
                CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_NICE_SHOOTIN_TEX)
            else:
                CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_HELL_OF_A_SHOT)
                
            # If easy mode, inlanes and shooter can be collected in any order
            if (self.level[plyr] == CustomFunc.LEVEL_EASY):
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                    # Skill shot completes collecting inlanes in easy
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_INLANES_COLLECTED
                    self.compInlanes[plyr] = 0
                elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_SHOOTER_COLLECTED
            # If medium mode, inlanes must be collected, then shooter is collected
            elif (self.level[plyr] == CustomFunc.LEVEL_MED):
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                    # Skill shot completes collecting inlanes in medium
                    self.compInlanes[plyr] = 0
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_INLANES_COLLECTED
                elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_SHOOTER_COLLECTED
            
            # Move to normal mode
            moveNextMode = True
            
        # If any other switches get hit, move to normal mode
        if ((CustomFunc.GameData.currInpStatus[0] & (InpBitNames.INP_SPINNER | InpBitNames.INP_HORSHOE_ROLLOVER | InpBitNames.INP_UPPER_LFT_ROLLOVER | InpBitNames.INP_UPPER_RGHT_ROLLOVER |
                InpBitNames.INP_BELOW_KICKOUT_RUBBER | InpBitNames.INP_UPPER_LFT_TOP_TRGT | InpBitNames.INP_UPPER_LFT_BTM_TRGT )) != 0) or \
           ((CustomFunc.GameData.currInpStatus[1] & (InpBitNames.INP_BTM_LFT_INLN_ROLLOVER | InpBitNames.INP_BTM_LFT_OUTLN_ROLLOVER |
            InpBitNames.INP_CTR_LOW_ROLLOVER | InpBitNames.INP_DROP_BANK_MISS | InpBitNames.INP_BTM_RGHT_RUBBER | InpBitNames.INP_BTM_RGHT_LOW_RUBBER  |
            InpBitNames.INP_DROP_TRGT_1S | InpBitNames.INP_DROP_TRGT_2H | InpBitNames.INP_DROP_TRGT_3O | InpBitNames.INP_DROP_TRGT_4O  |
            InpBitNames.INP_DROP_TRGT_5T | InpBitNames.INP_DROP_TRGT_6E | InpBitNames.INP_DROP_TRGT_7R)) != 0):
            moveNextMode = True
        
        # Depending on the level depends on the mode we move into
        if moveNextMode:
            # Stop blinking the ctr inlane
            CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_INLN_CTR)
            self.move_to_normal_mode(plyr)

    ## Move to normal mode
    #
    #  Move to normal mode from skillshot or finishing a mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note None
    def move_to_normal_mode(self, plyr):
        if (self.level[plyr] == CustomFunc.LEVEL_EASY):
            # Even if in a mode at end of last ball, mode was marked as completed.  Move to normal state.
            if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                # Blink inlanes that aren't lit
                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                    LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT) 
            if ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                # Blink shooter targets
                self.dropTrgtGoal[plyr] = LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | \
                    LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7
                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | 
                    LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7) 
            self.state[plyr] = CustomFunc.STATE_NONE
                
        elif (self.level[plyr] == CustomFunc.LEVEL_MED):
            # Check if at end of last ball, a mode was active
            if ((self.stateProg[plyr] & CustomFunc.STATEPROG_KICKOUTHOLE_COLLECTED) != 0):
                # Re-enter the mode, saving the state
                self._initFuncTbl[self.mode[plyr]](self, plyr, True)
                self.state[plyr] = CustomFunc.STATE_MODE_ACTIVE
            elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) != 0):
                # Blink kickout hole to indicate mode is ready
                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_KO_PICK_JOB)
                self.state[plyr] = CustomFunc.STATE_NONE
            elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) != 0):
                # Blink shooter targets
                self.dropTrgtGoal[plyr] = LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | \
                    LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7
                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | 
                    LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7) 
                self.state[plyr] = CustomFunc.STATE_NONE
            else:
                # Blink non-lit inlanes
                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                    LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT) 
                self.state[plyr] = CustomFunc.STATE_NONE
        
        elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
            # Blink non-lit inlanes
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT) 
            self.state[plyr] = CustomFunc.STATE_NONE
            
        elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
            # Blink non-lit inlanes
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT) 
            self.state[plyr] = CustomFunc.STATE_NONE
            
        # Tilt becomes active again
        self.tiltActive = True
        CustomFunc.GameData.gameMode = State.MODE_NORMAL_PLAY
                        
    ## Process normal play
    #
    #  Process normal play
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note None
    def proc_normal_play(self, plyr):
        if (self.level[plyr] == CustomFunc.LEVEL_EASY):
            if ((self.pollStatus & CustomFunc.POLLSTAT_INLANE_COMP) != 0):
                # Check if just collected inlane towards starting mode
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                    # Turn off blinking inlanes, mark state bit, 
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_INLANES_COLLECTED
                    CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                        LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT)
                    # Check if drops have been collected.  If so, start blinking kickout hole
                    if ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) != 0):
                        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_KO_PICK_JOB)
                # Inlanes collected again, increase spinner multiplier
                else:
                    if (self.spinMult < 5):
                        self.spinMult += 1
                    if (self.spinMult == 2):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_2X)
                    elif (self.spinMult == 3):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_3X)
                    elif (self.spinMult == 4):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_4X)
                    elif (self.spinMult == 5):
                        CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_5X)
            if ((self.pollStatus & CustomFunc.POLLSTAT_COMP_DROPS) != 0):
                # Check if just collected drops towards starting mode
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                    # Turn off blinking drops, mark state bit, 
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_SHOOTER_COLLECTED
                    CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | 
                        LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7) 
                    # Check if inlanes have been collected.  If so, start blinking kickout hole
                    if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) != 0):
                        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_KO_PICK_JOB)
            # Check if kickout hole collected
            if CustomFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_KICKOUT_HOLE):
                if ((self.stateProg[plyr] & (CustomFunc.STATEPROG_INLANES_COLLECTED | CustomFunc.STATEPROG_SHOOTER_COLLECTED)) == \
                    (CustomFunc.STATEPROG_INLANES_COLLECTED | CustomFunc.STATEPROG_SHOOTER_COLLECTED)):
                    CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_KO_PICK_JOB)
                    print "Choose mode started"
                    self.state[plyr] = CustomFunc.STATE_CHOOSE_MODE
                    CustomFunc.GameData.gameMode = State.MODE_CHOOSE_MODE
                else:
                    #Hitting kickout hole, collects the bonus
                    print "Collect bonus"
                    CustomFunc.GameData.score[plyr] += (self.spinMult * self.numSpin)
        self.pollStatus = 0            
    
    ## Initialize choose mode
    #
    #  Initialize choose mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note None
    def init_choose_mode(self, plyr):
        # Stop blinking inlanes and drop targets
        CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
            LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT) 
        CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_DT_1 | LedBitNames.LED_DT_2 | LedBitNames.LED_DT_3 | 
            LedBitNames.LED_DT_4 | LedBitNames.LED_DT_5 | LedBitNames.LED_DT_6 | LedBitNames.LED_DT_7)
        
        # Find the first available incomplete mode
        for index in xrange(CustomFunc.MODE_NUM_MODES):
            if ((self.compModes[plyr] & (1 << index)) == 0):
                self.selectMode = index
                break
        # Blink the mode LED
        CustomFunc.GameData.StdFuncs.Led_Blink_100(CustomFunc.modeLedLkup[self.selectMode])
        
    ## Process call posse
    #
    #  Process call posse mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Spinner lane 10 spins, then kickout hole.  Future: gives two ball multiball
    def proc_call_posse(self, plyr):
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_SPINNER):
            self.saveModeState[plyr] += 1
            if (self.saveModeState[plyr] > 10):
                # Stop blinking the spinner target, and blink kickout hole (duel)
                CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_SPINNER)
                CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_SPINNER)
                CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_KO_DUEL)
        if (self.saveModeState[plyr] > 10) and CustomFunc.GameData.StdFuncs.CheckSolBit(SolBitNames.SOL_KICKOUT_HOLE):
            # Mode successfully completed
            CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_KO_DUEL)
            CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_SPINNER)
            CustomFunc.GameData.StdFuncs.Led_Blink_Off(LedBitNames.LED_MODE_POSSE)
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_MODE_POSSE)
            self.compModes[plyr] |= CustomFunc.MODE_CALL_POSSE
            
            # Reset state progress
            self.stateProg[plyr] = 0
            CustomFunc.GameData.score[plyr] += self._compModeScore[self.level[plyr]]
            
            # Call move to next mode
            # HRS:  This should move to jackpot mode, not normal mode
            self.move_to_normal_mode(plyr)
            
    
    ## Process hustle and jive
    #
    #  Process hustle and jive mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Turn off tilt bob.  Disable rotate of inlanes using flippers.  Mode is
    #  successfully completed when all the lanes have been entered
    def proc_hustle_jive(self, plyr):
        pass
    
    ## Process target practice
    #
    #  Process target practice mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Blink random pop, random shooter target, random inlane,
    #  spinner orbit, then finish with kickout hole. 
    def proc_target_practice(self, plyr):
        pass
    
    ## Process check hideouts
    #
    #  Process check hideouts mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Must get two standup targets within 60s
    def proc_check_hideouts(self, plyr):
        pass
    
    ## Process sniper
    #
    #  Process sniper mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Disable pop bumpers.  Can only hit blinking shooter target,
    #  then next one, etc.  Hit 5 individual targets completes the mode
    def proc_sniper(self, plyr):
        pass
    
    ## Process Sharpe attack
    #
    #  Process Sharpe attack mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Five shooter individual targets, no cradling allowed.
    def proc_sharpe_attack(self, plyr):
        pass

    ## Process track bandits
    #
    #  Process track bandits mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Collect all lanes (can use flippers to rotate).  Jackpot lane must
    #  also be collected, then knock down all the shooter targets.
    def proc_track_bandits(self, plyr):
        pass
    
    ## Process kill em all
    #
    #  Process kill em all mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Drop all shooter targets 3 times.  60 sec to drop bank.
    #  Resets timer when bank is finished.
    def proc_kill_em_all(self, plyr):
        pass
    
    ## Process bar fight
    #
    #  Process bar fight mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Hit each pop bumper 10 times.  Each time bumper is hit,
    #  light in bumper is lit 10% ore time.  10 hits are full on.
    def proc_bar_fight(self, plyr):
        pass
    
    ## Process duel
    #
    #  Process duel mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Hit flashing shooter target within certain amount of time.
    def proc_duel(self, plyr):
        pass
    
    ## Process ride for help
    #
    #  Process ride for help mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Five orbits, then sink kickout hole.  Future:  Gives two ball multiball.
    def proc_ride_for_help(self, plyr):
        pass
