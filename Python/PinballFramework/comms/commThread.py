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
# @file    commThread.py
# @author  Hugh Spahr
# @date    1/16/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the communication thread file that is used to communicate with
# the hardware.  commIntf.py should be the only file importing this file.

#===============================================================================

import rs232Intf
import errIntf
import serial
from gameData import GameData
from tk.tkCmdFrm import TkCmdFrm
from threading import Thread
import time
import commHelp

## Communication thread class.
#
#  Communicates at periodic intervals to the hardware.  Inherits from Thread class.
#  Multiple Comms threads could be supported if the hardware had multiple serial ports.
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
    
    #private members
    _runCommThread = True
    _threadlock = 0
    
    ## The constructor.
    def __init__(self):
        super(CommThread, self).__init__()
        
        #Data that is shared with the interface file
        ## Number of solenoid boards
        self.numSolBrd = 0
        
        ## Bitmask to request update cfg for solenoid brd
        self.updateSolBrdCfg = 0
        
        ## Solenoid board configurations
        self.solBrdCfg = [[]]
        
        ## Solenoid board addresses
        self.solAddrArr = []
        
        ## Number of input boards
        self.numInpBrd = 0
        
        ## Bitmask to request update cfg for input brd
        self.updateInpBrdCfg = 0
        
        ## Input board configurations
        self.inpBrdCfg = [[]]
        
        ## Input board addresses
        self.inpAddrArr = []
        
        ## Rcvd switch data from input boards
        self.switchInpData = []
        
        ## Rcvd switch data from solenoid boards
        self.switchSolData = []
        
        ## Current comms thread state
        self.state = CommThread.COMM_INIT
        
        ## Serial port object
        self.ser = None
        
        ## Response from inventory command
        self.invResp = []

    ## Initialize comms to the hardware
    #
    #  Hands back error if comm port can't be opened.  If comm port is blank,
    #  disables communications to hardware.
    #
    #  @param  self          [in]   Object reference
    #  @param  portId        [in]   String for port name.  Ex. COM1
    #  @return Can return CMD_OK if good, or CANT_OPEN_COM or error codes
    #     from [getInventory](@ref comms.commHelp.getInventory).
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
    
    ## Start the comms thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def start(self):
        super(CommThread, self).start()
    
    ## Exit the comms thread
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def commExit(self):
        CommThread._runCommThread = False
        
    ## Process the comms thread
    #
    #  Periodically send get status commands to get switch status.
    #  Check bitfields to see if configurations need to be updated.
    #  Send solenoid kick commands if necessary.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def proc_comms(self):
        pass
    
    ## The Comms thread
    #
    #  If debug is not set, just run the comms thread processing.  If debug is set,
    #  run debug processing if set to run the comms thread, or if a single step
    #  command has been received.
    #
    #  @param  self          [in]   Object reference
    #  @return None 
    def run(self):
        count = 0
      
        while CommThread._runCommThread:
            #Process comms if not running in debug mode
            if not GameData.debug: 
                self.proc_comms()
            #Process comms if run button is active
            elif GameData.debug and TkCmdFrm.threadRun[TkCmdFrm.COMMS_THREAD_IDX] and \
                    TkCmdFrm.toggleState[TkCmdFrm.COMMS_THREAD_IDX]:
                self.proc_comms()
            #Process comms if send step was pressed
            elif GameData.debug and (not TkCmdFrm.threadRun[TkCmdFrm.COMMS_THREAD_IDX]) and \
                    TkCmdFrm.threadSendStep[TkCmdFrm.COMMS_THREAD_IDX]:
                TkCmdFrm.threadSendStep[TkCmdFrm.COMMS_THREAD_IDX] = False
                self.proc_comms()
            
            #Sleep until next rules processing time
            time.sleep(1)
            count += 1
