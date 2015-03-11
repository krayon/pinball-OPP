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
    data = getSerialData(commThread, 1);
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
                commThread.solBrdCfg.append(GameData.SolBitNames.SOL_BRD_CFG[commThread.numSolBrd - 1])
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
                commThread.inpBrdCfg.append(GameData.InpBitNames.INP_BRD_CFG[commThread.numInpBrd - 1])
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
    if len(commThread.invResp) != len(GameData.GameConst.INV_ADDR_LIST):
        print "Bad Num Cards.  Expected = %d, Found = %d" % \
            (len(GameData.GameConst.INV_ADDR_LIST), len(commThread.invResp))
        return (errIntf.BAD_NUM_CARDS)
    for i in xrange(len(commThread.invResp)):
        if (ord(commThread.invResp[i]) != GameData.GameConst.INV_ADDR_LIST[i]):
            print "Inv match fail.  Expected = 0x%02x, Rcvd = 0x%02x, index = %d" % \
                (GameData.GameConst.INV_ADDR_LIST[i], ord(commThread.invResp[i]), i)
            return (errIntf.INV_MATCH_FAIL)
        
    return (errIntf.CMD_OK)

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
    print repr(data)
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
                    InpBrd.update_status(GameData.inpBrd, boardIndex, (ord(data[index + 2]) << 8) | ord(data[index + 3]))
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
    addr = commThread.solAddrArr[solBrd]
    cmdArr.append(addr)
    cmdArr.append(rs232Intf.KICK_SOL_CMD)
    value = commThread.solKickVal[solBrd]
    commThread.solKickVal[solBrd] = 0
    # Value
    cmdArr.append(value)
    # Mask
    cmdArr.append(value)
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    commThread.ser.write(sendCmd)
    
    # Kick command, just return EOM.
    error = rcvEomResp(commThread)
    if error:
        print "Kick error, Addr = 0x%02x" % addr
        return (errIntf.KICK_BAD_RESP)

    # Now clear the set bit
    cmdArr = []
    cmdArr.append(addr)
    cmdArr.append(rs232Intf.KICK_SOL_CMD)
    # Value
    cmdArr.append(0)
    # Mask
    cmdArr.append(value)
    sendCmd = ''.join(cmdArr)
    commThread.ser.write(sendCmd)
    
    # Kick command, just return EOM.
    error = rcvEomResp(commThread)
    if error:
        print "Kick error, Addr = 0x%02x" % addr
        return (errIntf.KICK_BAD_RESP)
    return (errIntf.CMD_OK)
