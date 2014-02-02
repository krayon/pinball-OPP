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
# @file:   commThread.py
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
# This is the communication thread file that is used to communicate with
# the hardware.  commIntf.py should be the only file importing this file.
#
#===============================================================================

vers = '00.00.01'

import array
import thread
import rs232Intf
import errIntf
import commHelp

#Data that is shared with the interface file
numSolBrd = 0
updateSolBrdCfg = 0
solBrdCfg = [][]
solAddrArr = []
currSolData = []
numInpBrd = 0
updateInpBrdCfg = 0
inpBrdCfg = [][]
inpAddrArr = []
currInpData = []

#Comm thread states
COMM_INIT           = 0
COMM_INV_DONE       = 1
COMM_CFG_DONE       = 2
COMM_SENT_CFG_CMD   = 3
COMM_SENT_GET_INP   = 4
COMM_EXIT           = 5
COMM_ERROR_OCC      = 6
state = COMM_INIT

#Data not shared to the outside world
defaultSolCfg = [ rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                  rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00' ]

defaultInpCfg = [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
                  rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
                  rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
                  rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ]
runCommThread = True
threadlock = thread.allocate_lock()

#Initialize comms to the hardware
def init(portId):
    global ser
    
    try:
        ser=serial.Serial(port, baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
    except serial.SerialException:
        state = COMM_ERROR_OCC
        return(errIntf.CANT_OPEN_COM)
    retCode = commHelp.getInventory()
    if retCode:
        state = COMM_ERROR_OCC
        return (retCode)
    state = COMM_INV_DONE
    return(errIntf.CMD_OK)

def start():
    thread.start_new_thread(commThread, ("Comm Thread",))

def commExit():
    runCommThread = False

def commThread():
    global ser
  
    while runCommThread:
        #Comm thread processing
        runTask = False
