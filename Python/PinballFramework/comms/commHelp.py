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
# @file    commHelp.py
# @author  Hugh Spahr
# @date    1/16/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the communication helper file.  It should only be called by commThread.

#===============================================================================

import rs232Intf
import errIntf
from gameData import GameData
from hwobjs.solBrd import SolBrd
from hwobjs.inpBrd import InpBrd

CRC8ByteLookup = \
    [ 0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, \
      0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, \
      0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, \
      0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, \
      0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, \
      0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, \
      0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, \
      0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, \
      0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, \
      0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, \
      0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, \
      0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, \
      0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, \
      0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, \
      0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, \
      0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3 ]

## Calculate a CRC8
#
#  @param  msgChars      [in]   List of chars that make up the message
#  @return CRC8
def calcCrc8(msgChars):
    crc8Byte = 0xff
    for indChar in msgChars:
        indInt = ord(indChar)
        crc8Byte = CRC8ByteLookup[crc8Byte ^ indInt];
    return (chr(crc8Byte))

## Get Data from serial port
#
#  @param  commThread    [in]   Comm thread object
#  @param  numBytes      [in]   Number of bytes to read
#  @return List of bytes that were read
def getSerialData(commThread, numBytes):
    resp = commThread.ser.read(numBytes)
    return (resp)

## Rcv EOM response
#
#  @param  commThread    [in]   Comm thread object
#  @return True if error
def rcvEomResp(commThread):
    data = getSerialData(commThread, 1)
    if (data[0] != rs232Intf.EOM_CMD):
        return (True)
    return (False)

## Get inventory
#
#  Grab the inventory and make sure a valid response was received.  Verify
#  the received inventory matches [INV_ADDR_LIST](@ref rules.rulesData.RulesData.INV_ADDR_LIST).
#
#  @param  commThread    [in]   Comm thread object
#  @return Can return CMD_OK if good, or INVENTORY_NO_RESP, BAD_INV_RESP,
#     EXTRA_INFO_RCVD, BAD_NUM_CARDS, INV_MATCH_FAIL if an error
#  @note   Don't know size of the response since it depends on the
#     number of installed cards.
def getInventory(commThread):
    cmdArr = []
    cmdArr.append(rs232Intf.INV_CMD)
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    commThread.ser.write(sendCmd)
    
    #add two extra bytes for command and EOM
    data = getSerialData(commThread, rs232Intf.MAX_NUM_INP_BRD + rs232Intf.MAX_NUM_SOL_BRD + 2)

    #Response must have at least inv command and eom or return INVENTORY_NO_RESP
    if (len(data) < 2):
        print "Inventory response fail"
        return (errIntf.INVENTORY_NO_RESP)
    #Response must have inv command at start or return BAD_INV_RESP
    if (data[0] != rs232Intf.INV_CMD):
        print "Inventory response fail.  Expected = 0x%02x, Rcvd = 0x%02x" % \
            (ord(rs232Intf.INV_CMD), data[0])
        return (errIntf.BAD_INV_RESP)
    index = 1

    #Reset variables so function can be run more than once.
    #  Note:  Config of boards is not reset
    commThread.numSolBrd = 0
    commThread.solAddrArr = []
    commThread.currSolData = []
    commThread.solKickVal = []
    commThread.numInpBrd = 0
    commThread.inpAddrArr = []
    commThread.currInpData = []
    
    added = False
    while (data[index] != rs232Intf.EOM_CMD):
        if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_SOL_CARD)):
            commThread.numSolBrd += 1
            commThread.solAddrArr.append(data[index])
            commThread.currSolData.append(0)
            commThread.solKickVal.append(0)

            #add to the config/read cmd if necessary
            if (len(commThread.solBrdCfg) < commThread.numSolBrd):
                commThread.solBrdCfg.append(['\x00' for _ in xrange(24)])
                for cfgIndx in xrange(24):
                    commThread.solBrdCfg[commThread.numSolBrd - 1][cfgIndx] = GameData.SolBitNames.SOL_BRD_CFG[commThread.numSolBrd - 1][cfgIndx]
                commThread.updateSolBrdCfg |= (1 << (commThread.numSolBrd - 1))
                commThread.readInpCmd.append(data[index])
                commThread.readInpCmd.append(rs232Intf.READ_SOL_INP_CMD)
                commThread.readInpCmd.append('\x00')
                added = True
        elif ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_INP_CARD)):
            commThread.numInpBrd += 1
            commThread.inpAddrArr.append(data[index])
            commThread.currInpData.append(0)

            #add to the config/read cmd if necessary
            if (len(commThread.inpBrdCfg) < commThread.numInpBrd):
                commThread.inpBrdCfg.append(['\x00' for _ in xrange(16)])
                for cfgIndx in xrange(16):
                    commThread.inpBrdCfg[commThread.numInpBrd - 1][cfgIndx] = GameData.InpBitNames.INP_BRD_CFG[commThread.numInpBrd - 1][cfgIndx]
                commThread.updateInpBrdCfg |= (1 << (commThread.numInpBrd - 1))
                commThread.readInpCmd.append(data[index])
                commThread.readInpCmd.append(rs232Intf.READ_INP_BRD_CMD)
                commThread.readInpCmd.append('\x00')
                commThread.readInpCmd.append('\x00')
                added = True
        index += 1
    if added:
        commThread.readInpCmd.append(rs232Intf.EOM_CMD)
        commThread.readInpStr = ''.join(commThread.readInpCmd)
    if (index + 1 != len(data)):
        return (errIntf.EXTRA_INFO_RCVD)
    
    #Store off the response removing command and EOM
    commThread.invResp = list(data[1:-1])
    
    #Verify the number of cards is correct
    if len(commThread.invResp) != len(GameData.RulesData.INV_ADDR_LIST):
        print "Bad Num Cards.  Expected = %d, Found = %d" % \
            (len(GameData.RulesData.INV_ADDR_LIST), len(commThread.invResp))
        return (errIntf.BAD_NUM_CARDS)
    for i in xrange(len(commThread.invResp)):
        if (ord(commThread.invResp[i]) != GameData.RulesData.INV_ADDR_LIST[i]):
            print "Inv match fail.  Expected = 0x%02x, Rcvd = 0x%02x, index = %d" % \
                (GameData.RulesData.INV_ADDR_LIST[i], ord(commThread.invResp[i]), i)
            return (errIntf.INV_MATCH_FAIL)
        
    return (errIntf.CMD_OK)

## Create Cfg Arrays
#
#  Create configuration arrays for the cards.  Used in simulation mode so cfg updates do not
#  fail.
#
#  @param  commThread    [in]   Comm thread object
#  @return None
def createCfgArr(commThread):
    for index in xrange(len(GameData.SolBitNames.SOL_BRD_CFG)):
        commThread.solBrdCfg.append(GameData.SolBitNames.SOL_BRD_CFG[index])
        commThread.solKickVal.append(0)
    for index in xrange(len(GameData.InpBitNames.INP_BRD_CFG)):
        commThread.inpBrdCfg.append(GameData.InpBitNames.INP_BRD_CFG[index])

## Send configuration
#
#  Send the current configuration to the card.
#
#  @param  commThread    [in]   Comm thread object
#  @param  solBrd        [in]   True if solenoid board
#  @param  index         [in]   Index of board to configure
#  @return Can return CMD_OK if good, or CFG_BAD_RESP if an error
def sendConfig(commThread, solBrd, index):
    cmdArr = []
    if solBrd:
        addr = commThread.solAddrArr[index]
        cmdArr.append(addr)
        cmdArr.append(rs232Intf.CFG_SOL_CMD)
        for loop in xrange(rs232Intf.NUM_SOL_PER_BRD):
            cmdArr.append(commThread.solBrdCfg[index][loop * 3])
            cmdArr.append(commThread.solBrdCfg[index][(loop * 3) + 1])
            cmdArr.append(commThread.solBrdCfg[index][(loop * 3) + 2])
    else:
        addr = commThread.inpAddrArr[index]
        cmdArr.append(addr)
        cmdArr.append(rs232Intf.CFG_INP_CMD)
        for loop in xrange(rs232Intf.NUM_INP_PER_BRD):
            cmdArr.append(commThread.inpBrdCfg[index][loop])
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    commThread.ser.write(sendCmd)
    
    #Config command just return EOM.
    error = rcvEomResp(commThread)
    if error:
        print "Cfg error, Addr = 0x%02x" % addr
        return (errIntf.CFG_BAD_RESP)
    return (errIntf.CMD_OK)

## Read inputs
#
#  Send the read inputs commands and get response.  Update the status
#  fields in the board objects.
#
#  @param  commThread    [in]   Comm thread object
#  @return None, but can print an error if response format is wrong
def readInputs(commThread):
    commThread.ser.write(commThread.readInpStr)
    data = getSerialData(commThread, len(commThread.readInpStr))
    if (len(data) == len(commThread.readInpStr)):
        index = 0
        while index < len(data):
            boardIndex = ord(data[index]) & 0x0f
            if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_SOL_CARD)):
                if data[index + 1] == rs232Intf.READ_SOL_INP_CMD:
                    SolBrd.update_status(GameData.solBrd, boardIndex, ord(data[index + 2]))
                    index += 3
            elif ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_INP_CARD)):
                if data[index + 1] == rs232Intf.READ_INP_BRD_CMD:
                    status = (ord(data[index + 2]) << 8) | ord(data[index + 3])
                    InpBrd.update_status(GameData.inpBrd, boardIndex, status)
                    index += 4
            else:
                index +=1
    else:
        print "Bad read input response."
    
## Send kick
#
#  Send a kick to a solenoid card
#
#  @param  commThread    [in]   Comm thread object
#  @param  solBrd        [in]   Solenoid board number base 0
#  @return Can return CMD_OK if good, or KICK_BAD_RESP if an error
def sendKick(commThread, solBrd):
    cmdArr = []
    clearArr = []
    addr = commThread.solAddrArr[solBrd]
    cmdArr.append(addr)
    clearArr.append(addr)
    cmdArr.append(rs232Intf.KICK_SOL_CMD)
    clearArr.append(rs232Intf.KICK_SOL_CMD)
    value = commThread.solKickVal[solBrd]
    commThread.solKickVal[solBrd] = 0
    # Value
    cmdArr.append(chr(value))
    clearArr.append(chr(0))
    # Mask
    cmdArr.append(chr(value))
    clearArr.append(chr(value))
    cmdArr.append(rs232Intf.EOM_CMD)
    clearArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    clearCmd = ''.join(clearArr)
    commThread.ser.write(sendCmd)
    
    # Kick command, just return EOM.
    error = rcvEomResp(commThread)
    if error:
        print "Kick error, Addr = 0x%02x" % addr
        return (errIntf.KICK_BAD_RESP)

    # Now clear the set bit
    commThread.ser.write(clearCmd)
    
    # Kick command, just return EOM.
    error = rcvEomResp(commThread)
    if error:
        print "Kick error, Addr = 0x%02x" % addr
        return (errIntf.KICK_BAD_RESP)
    return (errIntf.CMD_OK)
