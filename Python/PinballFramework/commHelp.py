#!/usr/bin/env python
#
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
# @file:   commHelp.py
# @author: Hugh Spahr
# @date:   1/16/2014
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
# This is the communication helper file.  It should only be call by commThread.
#
#===============================================================================

vers = '00.00.02'

import rs232Intf
import errIntf
import commIntf
from rulesData import RulesData

#grab data from serial port
def getSerialData(commThread, numBytes):
    resp = commThread.ser.read(numBytes)
    return (resp)

#get inventory.  Note:  don't know the size of the
#response since it depends on the number of installed cards.
def getInventory(commThread):
    cmdArr = []
    cmdArr.append(rs232Intf.INV_CMD)
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    commThread.ser.write(sendCmd)
    
    #add two extra bytes for command and EOM
    data = getSerialData(commThread, rs232Intf.MAX_NUM_INP_BRD + rs232Intf.MAX_NUM_SOL_BRD + 2)

    #Should at least inv command and eom
    if (len(data) < 2):
        return (errIntf.INVENTORY_NO_RESP)
    if (data[0] != rs232Intf.INV_CMD):
        return (errIntf.BAD_INV_RESP)
    index = 1

    #Reset variables so function can be run more than once.
    #  Note:  Config of boards is not reset
    commThread.numSolBrd = 0
    commThread.solAddrArr = []
    commThread.currSolData = []
    commThread.numInpBrd = 0
    commThread.inpAddrArr = []
    commThread.currInpData = []
    
    while (data[index] != rs232Intf.EOM_CMD):
        if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_SOL_CARD)):
            commThread.numSolBrd += 1
            commThread.solAddrArr.append(data[index])
            commThread.currSolData.append(0)

            #add to the config structure if necessary
            if (len(commThread.solBrdCfg[0]) < commThread.numSolBrd):
                commThread.solBrdCfg.append(commThread.DFLT_SOL_CFG)
        elif ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_INP_CARD)):
            commThread.numInpBrd += 1
            commThread.inpAddrArr.append(data[index])
            commThread.currInpData.append(0)

            #add to the config structure if necessary
            if (len(commThread.inpBrdCfg[0]) < commThread.numInpBrd):
                commThread.inpBrdCfg.append(commThread.DFLT_INP_CFG)
        index += 1
    if (index != len(data)):
        return (errIntf.EXTRA_INFO_RCVD)
    
    #Store off the response removing command and EOM
    commThread.invResp = list(data[1:-1])
    
    #Verify the number of cards is correct
    if len(commThread.invResp) != len(RulesData.INV_ADDR_LIST):
        return (errIntf.BAD_NUM_CARDS)
    for i in range(len(commThread.invResp)):
        if (commThread.invResp[i] != RulesData.INV_ADDR_LIST[i]):
            return (errIntf.INV_MATCH_FAIL)
        
    return (errIntf.CMD_OK)

