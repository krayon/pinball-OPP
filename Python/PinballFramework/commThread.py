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

vers = '00.00.02'

import rs232Intf
import errIntf
import serial
import thread
from threading import Thread
import time
import commHelp

class CommThread(Thread):
    #Comm thread states
    COMM_INIT           = 0
    COMM_INV_DONE       = 1
    COMM_CFG_DONE       = 2
    COMM_SENT_CFG_CMD   = 3
    COMM_SENT_GET_INP   = 4
    COMM_EXIT           = 5
    COMM_ERROR_OCC      = 6
    COMM_NO_COMM_PORT   = 7

    #Data not shared to the outside world
    DFLT_SOL_CFG = [ rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00',
                      rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00', rs232Intf.CFG_SOL_DISABLE, '\x00', '\x00' ]
    
    DFLT_INP_CFG = [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
                      rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
                      rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE,
                      rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ]
    
    def __init__(self):
        super(CommThread, self).__init__()
        
        #Data that is shared with the interface file
        self.numSolBrd = 0
        self.updateSolBrdCfg = 0
        self.solBrdCfg = [[]]
        self.solAddrArr = []
        self.numInpBrd = 0
        self.updateInpBrdCfg = 0
        self.inpBrdCfg = [[]]
        self.inpAddrArr = []
        self.switchInpData = []
        self.switchSolData = []
        self.state = CommThread.COMM_INIT
        self.ser = None
        self.invResp = []

        #private members
        self._runCommThread = True
        self._threadlock = thread.allocate_lock()

    #Initialize comms to the hardware
    def init(self, portId):
        if (portId != ""):
            try:
                self.ser=serial.Serial(portId, baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
            except serial.SerialException:
                self.state = CommThread.COMM_ERROR_OCC
                return(errIntf.CANT_OPEN_COM)
            retCode = commHelp.getInventory(self)
            if retCode:
                self.state = CommThread.COMM_ERROR_OCC
                return (retCode)
            self.state = CommThread.COMM_INV_DONE
        else:
            self.state = CommThread.COMM_NO_COMM_PORT
        return(errIntf.CMD_OK)
    
    def start(self):
        super(CommThread, self).start()
    
    def commExit(self):
        self._runCommThread = False
    
    def run(self):
        count = 0
      
        while self._runCommThread:
            count += 1
            time.sleep(1)
            #Comm thread processing
