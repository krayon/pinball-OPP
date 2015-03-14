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
from ledBitNames import LedBitNames
from inpBitNames import InpBitNames
from solBitNames import SolBitNames
from sounds import Sounds
from SS3.ledBitNames import LedBitNames
import random

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
    
    LEVEL_EASY = 0
    LEVEL_MED = 1
    LEVEL_HARD = 2
    LEVEL_WIZARD = 3
    
    _reverseLookup = [ 0x0, 0x8, 0x4, 0xc, 0x2, 0xa, 0x6, 0xe, 0x1, 0x9, 0x5, 0xd, 0x3, 0xb, 0x7, 0xf]
   
    MODETRGT_POP_BUMPER = 0
    MODETRGT_DROP_TRGT = 1
    MODETRGT_INLANE = 2
    MODETRGT_SPINNER = 3 
    MODETRGT_KICKOUT_HOLE = 4 
    
    ## Initialize CustomFunc class
    #
    #  Initialize custom functions class
    #
    #  @param  self          [in]   Object reference
    #  @param  gameData      [in]   Object reference
    #  @return None
    def __init__(self, gameData):
        CustomFunc.GameData = gameData
        self.state = [CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT, CustomFunc.STATE_SKILL_SHOT]
        self.stateProg = [CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE, CustomFunc.STATEPROG_NONE]
        self.level = [CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY, CustomFunc.LEVEL_EASY]
        self.compModes = [0, 0, 0, 0]
        self.compInlanes = [0, 0, 0, 0]
        self.numSkillShots = [0, 0, 0, 0]
        self.selectMode = 0
        self.mode = [CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE, CustomFunc.MODE_CALL_POSSE]
        self.spinMult = 0
        self.tiltActive = False
        self.disableRotate = False
        self.saveModeState = [0, 0, 0, 0]
        self.saveModeValue = 0
        self._initFuncTbl = [self.init_call_posse, self.init_hustle_jive, self.init_target_practice, self.init_check_hideouts,
            self.init_sniper, self.init_sharpe_attack, self.init_track_bandits, self.init_kill_em_all,
            self.init_bar_fight, self.init_duel, self.init_ride_for_help]
        self._procFuncTbl = [self.proc_call_posse, self.proc_hustle_jive, self.proc_target_practice, self.proc_check_hideouts,
            self.proc_sniper, self.proc_sharpe_attack, self.proc_track_bandits, self.proc_kill_em_all,
            self.proc_bar_fight, self.proc_duel, self.proc_ride_for_help]
        
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
        self.spinMult = 0
        self.tiltActive = False
        self.disableRotate = False
        self.saveModeState = [0, 0, 0, 0]

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
        mask = [0, 0, 0, LedBitNames.LED_MULT_2 | LedBitNames.LED_MULT_3 | LedBitNames.LED_MULT_4 | LedBitNames.LED_MULT_5]
        if (self.level[plyr] == CustomFunc.LEVEL_EASY):
            leds = LedBitNames.LED_MULT_2
        elif (self.level[plyr] == CustomFunc.LEVEL_MED):
            leds = LedBitNames.LED_MULT_2 | LedBitNames.LED_MULT_3
        elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
            leds = LedBitNames.LED_MULT_2 | LedBitNames.LED_MULT_3 | LedBitNames.LED_MULT_4
        elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
            leds = LedBitNames.LED_MULT_2 | LedBitNames.LED_MULT_3 | LedBitNames.LED_MULT_4 | LedBitNames.LED_MULT_5
        CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, 0, 0, leds])
        
        # Set the completed modes
        mask = [0, 0, LedBitNames.LED_MODE_11 | LedBitNames.LED_MODE_10 | LedBitNames.LED_MODE_9 | LedBitNames.LED_MODE_8 | LedBitNames.LED_MODE_7,
            0, LedBitNames.LED_MODE_1 | LedBitNames.LED_MODE_2 | LedBitNames.LED_MODE_3 | LedBitNames.LED_MODE_4 | LedBitNames.LED_MODE_5 | LedBitNames.LED_MODE_6]
        # Bits are oriented so reversed bits are in proper position
        leds = self.reverseByte((self.compModes[plyr] & 0x7c0) >> 6)
        ledList = [0, 0, 0x20000 | leds, 0, 0x40000 | ((self.compModes[plyr] & 0x3f) << 2)] 
        CustomFunc.GameData.StdFuncs.Led_Set(mask, ledList)
    
        # Set the inlanes if easy or medum
        if (self.level[plyr] == CustomFunc.LEVEL_EASY) or (self.level[plyr] == CustomFunc.LEVEL_MED):
            mask = [0, LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT]
            CustomFunc.GameData.StdFuncs.Led_Set(mask, [0, self.compInlanes[plyr]])
        else:
            self.compInlanes[plyr] = 0
            CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT)
        
        # Reset the spinner kickout hole LEDs, 
        self.spinMult = 0
        CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED1_ALL_BITS_MSK)
        CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_SHOOT_AGAIN)
        CustomFunc.GameData.StdFuncs.Led_Off(LedBitNames.LED_LFT_OUTLN | LedBitNames.LED_LFT_INLN)
        self.state[plyr] = CustomFunc.STATE_SKILL_SHOT

        # Tilt is not active during skill shot to allow nudging
        self.tiltActive = False

    ## End ball
    #
    #  End the ball, and reset LEDs
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    def end_ball(self, plyr):
        # In easy mode inlanes are retained for next ball, mode completes on ball end
        if (self.level[plyr] == CustomFunc.LEVEL_EASY):
            if (self.state[plyr] == CustomFunc.STATE_MODE_ACTIVE):
                self.compModes[plyr] |= (1 << self.mode[plyr])
                self.stateProg[plyr] = CustomFunc.STATEPROG_NONE
        # In medium mode, inlanes are retained, and mode is continued if currently in a mode 
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
        
        # Calculate bonus
    
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
            newMode = self.selectMode
            foundNew = False
            while not foundNew:
                # increment the mode
                if (newMode == CustomFunc.MODE_RIDE_FOR_HELP):
                    newMode = CustomFunc.MODE_CALL_POSSE
                else:
                    newMode += 1
                # see if the new mode has not been completed
                if (self.compModes[plyr] & (1 << newMode) == 0):
                    foundNew = True
            # Verify mode has changed
            if (newMode != self.selectMode):
                # Disable the blinking on the old mode
                bit = (1 << self.selectMode)
                if ((bit & 0x3f) != 0):
                    modeBit = 0x40000 | (bit << 2)
                else:
                    modeBit = 0x20000 | self.reverseByte(bit >> 6)
                CustomFunc.GameData.StdFuncs.Led_Off(modeBit)
                
                # Enable the blinking on the new mode
                bit = (1 << newMode)
                if ((bit & 0x3f) != 0):
                    modeBit = 0x40000 | (bit << 2)
                else:
                    modeBit = 0x20000 | self.reverseByte(bit >> 6)
                CustomFunc.GameData.StdFuncs.Led_Blink_100(modeBit)
                self.selectMode = newMode
                    
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
                
            # No rotation allowed
            elif (self.level[plyr] == CustomFunc.LEVEL_HARD):
                pass
            
            # HRS:  No idea what to do in wizard mode
            elif (self.level[plyr] == CustomFunc.LEVEL_WIZARD):
                pass
            
        elif (self.state[plyr] == CustomFunc.STATE_CHOOSE_MODE):
            # Left flipper chooses the mode, LED is already blinking, so no changes needed
            self.mode[plyr] = self.selectMode
            self.state[plyr] = CustomFunc.STATE_MODE_ACTIVE
            
            # Initialize the mode function
            self._initFuncTbl[self.mode](self, plyr, False)
                    
        # Rotate may or may not happen depending on mode
        elif (self.state[plyr] == CustomFunc.STATE_MODE_ACTIVE):
            pass

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
    #  State contains number of spins already counted
    def init_call_posse(self, plyr, restoreState):
        # Blink spinner lane
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_SPINNER)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_1)
        
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
    def init_hustle_jive(self, plyr, restoreState):
        # Blink non-lit inlanes
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
            LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT)
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_2)
        self.disableRotate = True
        if not restoreState:
            self.compInlanes[plyr] = 0
    
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
    #  State contains next thing to hit.
    def init_target_practice(self, plyr, restoreState):
        CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_MODE_3)
        if restoreState:
            # If only had to hit the kickout hole, move back to hit spinner
            if (self.saveModeState[plyr] == CustomFunc.MODETRGT_KICKOUT_HOLE):
                self.saveModeState[plyr] = CustomFunc.MODETRGT_SPINNER
        else:
            self.saveModeState[plyr] = CustomFunc.MODETRGT_POP_BUMPER
        if self.saveModeState[plyr] == CustomFunc.MODETRGT_POP_BUMPER:
            # Pick the pop bumper that must be hit
            self.saveModeValue = random.randint(0, 3)
            # HRS:  I don't have these in the LED bit names yet.  Blink the pop bumper
            CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT)
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
    #  @note Must get two standup targets within 60s
    def init_check_hideouts(self, plyr, restoreState):
        pass
    
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
    #  then next one, etc.  Hit 5 individual targets completes the mode
    def init_sniper(self, plyr, restoreState):
        pass
    
    ## Init Sharpe attack
    #
    #  Initialize Sharpe attack mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Five shooter individual targets, no cradling allowed.
    def init_sharpe_attack(self, plyr, restoreState):
        pass

    ## Init track bandits
    #
    #  Initialize track bandits mode
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @param  restoreState  [in]   Restore the state of the mode
    #  @return None
    #
    #  @note Collect all lanes (can use flippers to rotate).  Jackpot lane must
    #  also be collected, then knock down all the shooter targets.
    def init_track_bandits(self, plyr, restoreState):
        pass
    
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
    def init_kill_em_all(self, plyr, restoreState):
        pass
    
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
    #  light in bumper is lit 10% ore time.  10 hits are full on.
    def init_bar_fight(self, plyr, restoreState):
        pass
    
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
        pass
    
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
        pass

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
        moveNextMode = False
        
        # Check if skillshot made
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_CTR_ROLLOVER):
            self.numSkillShots[plyr] += 1
            if (self.numSkillShots[plyr] & 1 != 0):
                CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_NICE_SHOOTIN_TEX)
            else:
                CustomFunc.GameData.StdFuncs.Sounds(Sounds.SOUND_HELL_OF_A_SHOT)
                
            # Mark the inlane as completed
            self.compInlanes[plyr] |= 0x02
            
            # If easy mode, inlanes and shooter can be collected in any order
            if (self.level[plyr] == CustomFunc.LEVEL_EASY):
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_INLANES_COLLECTED
                elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_SHOOTER_COLLECTED
            # If medium mode, inlanes must be collected, then shooter is collected
            elif (self.level[plyr] == CustomFunc.LEVEL_MED):
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_INLANES_COLLECTED
                elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                    self.stateProg[plyr] |= CustomFunc.STATEPROG_SHOOTER_COLLECTED
            
            # Move to normal mode
            moveNextMode = True
            
        # Check if another upper switch has happened
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_LFT_ROLLOVER):
            if ((self.compInlanes[plyr] & 0x04) == 0):
                CustomFunc.GameData.score[plyr] += 5
            else:
                CustomFunc.GameData.score[plyr] += 1
            self.compInlanes[plyr] |= 0x04
            moveNextMode = True
            
        if CustomFunc.GameData.StdFuncs.CheckInpBit(InpBitNames.INP_UPPER_RGHT_ROLLOVER):
            if ((self.compInlanes[plyr] & 0x01) == 0):
                CustomFunc.GameData.score[plyr] += 5
            else:
                CustomFunc.GameData.score[plyr] += 1
            self.compInlanes[plyr] |= 0x01
            moveNextMode = True
        
        # If any other switches get hit, it probably means the inlane switch didn't register, move to normal mode
        if ((CustomFunc.GameData.currInpStatus[0] & (InpBitNames.INP_SPINNER | InpBitNames.INP_HORSHOE_ROLLOVER |
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
            CustomFunc.GameData.StdFuncs.Led_On(LedBitNames.LED_INLN_CTR)
            if (self.level[plyr] == CustomFunc.LEVEL_EASY):
                # Even if in a mode at end of last ball, mode was marked as completed.  Move to normal state.
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) == 0):
                    # Blink inlanes that aren't lit
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_INLN_RGHT | LedBitNames.LED_INLN_CTR | LedBitNames.LED_INLN_LFT | 
                        LedBitNames.LED_ROLL_RGHT | LedBitNames.LED_ROLL_CTR | LedBitNames.LED_ROLL_LFT) 
                if ((self.stateProg[plyr] & CustomFunc.STATEPROG_SHOOTER_COLLECTED) == 0):
                    # Blink shooter targets
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
                    CustomFunc.GameData.StdFuncs.Led_Blink_100(LedBitNames.LED_KO_CTR_CTR) 
                    self.state[plyr] = CustomFunc.STATE_NONE
                elif ((self.stateProg[plyr] & CustomFunc.STATEPROG_INLANES_COLLECTED) != 0):
                    # Blink shooter targets
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
                        
    ## Process normal play
    #
    #  Process normal play
    #
    #  @param  self          [in]   Object reference
    #  @param  plyr          [in]   Current player
    #  @return None
    #
    #  @note Spinner lane 10 spins, then kickout hole.  Future: gives two ball multiball
    def proc_normal_play(self, plyr):
        pass
    
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
        pass
    
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
