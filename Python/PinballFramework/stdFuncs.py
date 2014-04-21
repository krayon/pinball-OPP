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
# @file:   stdFuncs.py
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
# This is the standard functions for the pinball framework
#
#===============================================================================

vers = '00.00.01'

from gameData import GameData

class StdFuncs():
    def CheckInpBit(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        if ((GameData.currInpStatus[cardNum] & bitPos) != 0):
            return True
        else:
            return False

    def CheckSolBit(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        if ((GameData.currSolStatus[cardNum] & bitPos) != 0):
            return True
        else:
            return False

    def CheckLedBit(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xffff
        if ((GameData.currLeds[cardNum] & bitPos) != 0):
            return True
        else:
            return False

    def Disable_Solenoids(self):
        #HRS:  Finish
        pass
    
    def Enable_Solenoids(self):
        #HRS:  Finish
        pass
    
    def Kick(self, solBit):
        #HRS:  Finish
        pass

    def Start(self, timeout):
        #HRS:  Finish
        pass
    
    def Expired(self, timeout):
        if ((GameData.expiredTimers & timeout) != 0):
            return True
        else:
            return False
    
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
        if (foundFirstBit and foundLastBit):
            tmpLed = GameData.currLeds[cardNum] << 1
            if ((tmpLed & (1 << lastBit)) != 0):
                tmpLed |= (1 << firstBit)
            tmpLed &= ~rotMask
            GameData.currLeds[cardNum] = (GameData.currLeds[cardNum] & ~rotMask) | tmpLed

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
        if (foundFirstBit and foundLastBit):
            tmpData = data << 1
            if ((tmpData & (1 << lastBit)) != 0):
                tmpData |= (1 << firstBit)
            tmpData &= ~rotMask
            return tmpData
        else:
            return 0
                
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
        if (foundFirstBit and foundLastBit):
            tmpLed = GameData.currLeds[cardNum]
            if ((GameData.currLeds[cardNum] & (1 << firstBit)) != 0):
                tmpLed |= (1 << lastBit)
            tmpLed = (tmpLed >> 1) & ~rotMask
            GameData.currLeds[cardNum] = (GameData.currLeds[cardNum] & ~rotMask) | tmpLed

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
        if (foundFirstBit and foundLastBit):
            tmpData = data
            if ((data & (1 << firstBit)) != 0):
                tmpData |= (1 << lastBit)
            tmpData = (tmpData >> 1) & ~rotMask
            return tmpData
        else:
            return 0

    def Led_On(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        GameData.currLeds[cardNum] |= bitPos

    def Led_Off(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        GameData.currLeds[cardNum] &= ~bitPos

    def Led_Set(self, mask, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        GameData.currLeds[cardNum] &= ~mask
        GameData.currLeds[cardNum] |= bitPos

    def Led_Blink_100(self, cardBitPos):
        cardNum = (cardBitPos >> 16) & 0xf
        bitPos = cardBitPos & 0xff
        GameData.currBlinkLeds[cardNum] |= bitPos 
        
    def Sounds(self, soundIdx):
        #HRS:  Finish
        pass

    def Wait(self, delay):
        #HRS:  Finish
        pass
