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
# @file    stdFuncs.py
# @author  Hugh Spahr
# @date    4/19/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief These are the standard functions for the pinball framework.

#===============================================================================

from hwobjs.ledBrd import LedBrd
from hwobjs.solBrd import SolBrd
from dispConstIntf import DispConst
import dispIntf
import time
import comms.commIntf
import rs232Intf

## Standard functions class.
#
#  Class that holds all the standard functions.
class StdFuncs():
    ## Initialize StdFuncs class
    #
    #  Initialize standard functions class
    #
    #  @param  self          [in]   Object reference
    #  @param  gameData      [in]   Object reference
    #  @return None
    def __init__(self, gameData):
        StdFuncs.GameData = gameData
    
    ## Check input bit
    #
    #  Check if a bit from an input card is currently set.
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   input card index and bit position
    #  @return True if set 
    def CheckInpBit(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        if ((StdFuncs.GameData.currInpStatus[cardNum] & bitPos) != 0):
            return True
        else:
            return False

    ## Check solenoid bit
    #
    #  Check if a bit from a solenoid card is currently set.
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   solenoid card index and bit position
    #  @return True if set 
    def CheckSolBit(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        if ((StdFuncs.GameData.currSolStatus[cardNum] & bitPos) != 0):
            return True
        else:
            return False

    ## Check LED bit
    #
    #  Check if an LED bit is set.
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   LED card index and bit position
    #  @return True if set 
    def CheckLedBit(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        if ((LedBrd.currLedData[cardNum] & bitPos) != 0):
            return True
        else:
            return False

    ## Disable solenoids
    #
    #  Send a command to disable the solenoids
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def Disable_Solenoids(self):
        cfg = [rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00']
        for cardNum in xrange(SolBrd.numSolBrd):
            for solIndex in xrange(rs232Intf.NUM_SOL_PER_BRD):
                comms.commIntf.updateSol(StdFuncs.GameData.commThread, cardNum, solIndex, cfg)
            comms.commIntf.sendSolCfg(StdFuncs.GameData.commThread, cardNum)
    
    ## Enable solenoids
    #
    #  Send a command to enable the solenoids.  Copies the standard solenoid
    #  configuration to the solenoids.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def Enable_Solenoids(self):
        for cardNum in xrange(SolBrd.numSolBrd):
            for solIndex in xrange(rs232Intf.NUM_SOL_PER_BRD):
                cfgOffs = rs232Intf.CFG_BYTES_PER_SOL * solIndex
                cfg = [StdFuncs.GameData.SolBitNames.SOL_BRD_CFG[cardNum][cfgOffs],
                    StdFuncs.GameData.SolBitNames.SOL_BRD_CFG[cardNum][cfgOffs + 1],
                    StdFuncs.GameData.SolBitNames.SOL_BRD_CFG[cardNum][cfgOffs + 2]]
                comms.commIntf.updateSol(StdFuncs.GameData.commThread, cardNum, solIndex, cfg)
            comms.commIntf.sendSolCfg(StdFuncs.GameData.commThread, cardNum)
    
    ## Change solenoid config
    #
    #  Send a command to change the solenoid config
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   solenoid card index and bit position
    #  @return None 
    def Change_Solenoid_Cfg(self, cardBitPos, cfg):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        comms.commIntf.updateSol(StdFuncs.GameData.commThread, cardNum, bitPos, cfg)
        comms.commIntf.sendSolCfg(StdFuncs.GameData.commThread, cardNum)
    
    ## Kick solenoid
    #
    #  Send a command to kick a solenoid
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   solenoid card index and bit position
    #  @return None 
    def Kick(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        comms.commIntf.sendSolKick(StdFuncs.GameData.commThread, cardNum, bitPos)

    ## Start a timer
    #
    #  Start a timer
    #
    #  @param  self          [in]   Object reference
    #  @param  timeout       [in]   bit position of the timer
    #  @return None 
    def Start(self, timeout):
        index = timeout >> 6
        bitPos = timeout & 0x1f
        StdFuncs.GameData.expiredTimers[index] &= ~(1 << bitPos)
        StdFuncs.GameData.timerCnt[timeout] = 0
        StdFuncs.GameData.runningTimers[index] |= (1 << bitPos)
    
    ## Check for expired timeout
    #
    #  Look if expired timeout bit is set
    #
    #  @param  self          [in]   Object reference
    #  @param  timeout       [in]   bit position of the timer
    #  @return True if expired 
    def Expired(self, timeout):
        index = timeout >> 6
        bitPos = timeout & 0x1f
        if ((StdFuncs.GameData.expiredTimers[index] & (1 << bitPos)) != 0):
            return True
        else:
            return False
    
    ## Rotate LED left
    #
    #  Rotate a group of LEDs to the left.
    #
    #  @param  self          [in]   Object reference
    #  @param  rotMask       [in]   Card number and mask of LEDs to rotate
    #  @return True if set
    #  @note The LEDs must be contiguous and not span cards
    def Led_Rot_Left(self, rotMask):
        #Currently rotated bits must be next to each other and on same card
        cardNum = (rotMask >> 16) & 0xf
        index = 0
        firstBit = 0
        lastBit = 0
        foundFirstBit = False
        foundLastBit = False
        while ((index < 8) and (foundLastBit == False)):
            if (((1 << index) & rotMask) != 0):
                if not foundFirstBit:
                    firstBit = index
                    foundFirstBit = True
            else:
                if foundFirstBit:
                    lastBit = index
                    foundLastBit = True
            index += 1
        if (foundFirstBit and not foundLastBit):
            foundLastBit = True
            lastBit = 7
        if (foundFirstBit and foundLastBit):
            rotBitSet = LedBrd.currLedData[cardNum] & (1 << lastBit)
            tmpLed = (LedBrd.currLedData[cardNum] << 1) & rotMask 
            if (rotBitSet != 0):
                tmpLed |= (1 << firstBit)
            LedBrd.currLedData[cardNum] = (LedBrd.currLedData[cardNum] & ~rotMask) | tmpLed

    ## Rotate variable left
    #
    #  Rotate a variable to the left.
    #
    #  @param  self          [in]   Object reference
    #  @param  rotMask       [in]   Mask to rotate
    #  @param  data          [in]   Data to be rotated
    #  @return Rotated value
    #  @note The rotMask bits must be contiguous
    def Var_Rot_Left(self, rotMask, data):
        index = 0
        firstBit = 0
        lastBit = 0
        foundFirstBit = False
        foundLastBit = False
        while ((index < 8) and (foundLastBit == False)):
            if (((1 << index) & rotMask) != 0):
                if not foundFirstBit:
                    firstBit = index
                    foundFirstBit = True
            else:
                if foundFirstBit:
                    lastBit = index
                    foundLastBit = True
            index += 1
        if (foundFirstBit and foundLastBit):
            tmpData = data << 1
            if ((tmpData & (1 << lastBit)) != 0):
                tmpData |= (1 << firstBit)
            tmpData &= rotMask
            return tmpData
        else:
            return 0
                
    ## Rotate LED right
    #
    #  Rotate a group of LEDs to the right.
    #
    #  @param  self          [in]   Object reference
    #  @param  rotMask       [in]   Card number and mask of LEDs to rotate
    #  @return True if set
    #  @note The LEDs must be contiguous and not span cards
    def Led_Rot_Right(self, rotMask):
        #Currently rotated bits must be next to each other and on same card
        cardNum = (rotMask >> 16) & 0xf
        index = 0
        firstBit = 0
        lastBit = 0
        foundFirstBit = False
        foundLastBit = False
        while ((index < 8) and (foundLastBit == False)):
            if (((1 << index) & rotMask) != 0):
                if not foundFirstBit:
                    firstBit = index
                    foundFirstBit = True
            else:
                if foundFirstBit:
                    lastBit = index
                    foundLastBit = True
            index += 1
        if (foundFirstBit and not foundLastBit):
            foundLastBit = True
            lastBit = 7
        if (foundFirstBit and foundLastBit):
            rotBitSet = LedBrd.currLedData[cardNum] & (1 << lastBit)
            tmpLed = LedBrd.currLedData[cardNum] << 1
            if (rotBitSet != 0):
                tmpLed |= (1 << firstBit)
            tmpLed &= ~rotMask
        if (foundFirstBit and foundLastBit):
            rotBitSet = LedBrd.currLedData[cardNum] & (1 << firstBit)
            tmpLed = (LedBrd.currLedData[cardNum] >> 1) & rotMask 
            if (rotBitSet != 0):
                tmpLed |= (1 << lastBit)
            LedBrd.currLedData[cardNum] = (LedBrd.currLedData[cardNum] & ~rotMask) | tmpLed

    ## Rotate variable right
    #
    #  Rotate a variable to the right.
    #
    #  @param  self          [in]   Object reference
    #  @param  rotMask       [in]   Mask to rotate
    #  @param  data          [in]   Data to be rotated
    #  @return Rotated value
    #  @note The rotMask bits must be contiguous
    def Var_Rot_Right(self, rotMask, data):
        index = 0
        firstBit = 0
        lastBit = 0
        foundFirstBit = False
        foundLastBit = False
        while ((index < 8) and (foundLastBit == False)):
            if (((1 << index) & rotMask) != 0):
                if not foundFirstBit:
                    firstBit = index
                    foundFirstBit = True
            else:
                if foundFirstBit:
                    lastBit = index
                    foundLastBit = True
            index += 1
        if (foundFirstBit and foundLastBit):
            tmpData = data & rotMask
            if ((data & (1 << firstBit)) != 0):
                tmpData |= (1 << lastBit)
            tmpData = (tmpData >> 1) & rotMask
            return tmpData
        else:
            return 0

    ## Turn LEDs on
    #
    #  Turn on a group of LEDs
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   Card number and mask of LEDs to turn on
    #  @return None
    def Led_On(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        LedBrd.currLedData[cardNum] |= bitPos

    ## Turn LEDs off
    #
    #  Turn off a group of LEDs
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   Card number and mask of LEDs to turn off
    #  @return None
    def Led_Off(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        LedBrd.currLedData[cardNum] &= ~bitPos

    ## Set a group of LEDs to a certain state
    #
    #  Set a group of LEDs to an absolute state
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   Card number and mask of LEDs to change
    #  @param  data          [in]   Data with new state of LEDs
    #  @return None
    def Led_Set(self, cardBitPos, data):
        # LED set can now accept a mask for a single card, or a list of cards
        if (isinstance( cardBitPos, int )):
            cardNum = (cardBitPos >> 16) & 0xf
            mask = cardBitPos & 0xff
            LedBrd.currLedData[cardNum] &= ~mask
            LedBrd.currLedData[cardNum] |= data
        else:
            for curr in xrange(len(cardBitPos)):
                if cardBitPos[curr] != 0:
                    cardNum = (cardBitPos[curr] >> 16) & 0xf
                    mask = cardBitPos[curr] & 0xff
                    LedBrd.currLedData[cardNum] &= ~mask
                    LedBrd.currLedData[cardNum] |= data[curr]

    ## Set a group of LEDs to blink
    #
    #  Set a group of LEDs to blink rapidly
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   Card number and mask of LEDs to change
    #  @return None
    def Led_Blink_100(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        LedBrd.currBlinkLeds[cardNum] |= bitPos 
        
    ## Turn off blink on a group of LEDs
    #
    #  Set a group of LEDs to blink rapidly
    #
    #  @param  self          [in]   Object reference
    #  @param  cardBitPos    [in]   Card number and mask of LEDs to change
    #  @return None
    def Led_Blink_Off(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        LedBrd.currBlinkLeds[cardNum] &= ~bitPos 
        
    ## Play a sound
    #
    #  Play a sound
    #
    #  @param  self          [in]   Object reference
    #  @param  soundIdx      [in]   Sound index
    #  @return None
    def Sounds(self, soundIdx):
        dispIntf.playSound(soundIdx)

    ## Show a background image
    #
    #  Show an image
    #
    #  @param  self          [in]   Object reference
    #  @param  imageIdx      [in]   Image index
    #  @return None
    def BgndImage(self, imageIdx):
        StdFuncs.GameData.bgndImage = imageIdx

    ## Play background music
    #
    #  Play the background music, index of bgnd track 
    #
    #  @param  self          [in]   Object reference
    #  @param  soundIdx      [in]   Sound index
    #  @return None
    def PlayBgnd(self, soundIdx):
        StdFuncs.GameData.bgndSound = soundIdx

    ## Stop background music
    #
    #  Stop the background music 
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def StopBgnd(self):
        StdFuncs.GameData.bgndSound = 0xffffffff

    ## Wait
    #
    #  Wait a certain number of milliseconds
    #
    #  @param  self          [in]   Object reference
    #  @param  delay         [in]   Delay in ms
    #  @return None
    def Wait(self, delay):
        time.sleep(float(delay)/1000.0)
    
    ## Blank score displays
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def BlankScoreDisps(self):
        for index in xrange(StdFuncs.GameData.GameConst.MAX_NUM_PLYRS):
            StdFuncs.GameData.blankDisp[index + DispConst.DISP_PLAYER1] = True

    ## Blank player num display
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def BlankPlyrNumDisp(self):
        StdFuncs.GameData.blankDisp[DispConst.DISP_PLAYER_NUM] = True
