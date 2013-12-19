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
# @file:   inpDrvTest.py
# @author: Hugh Spahr
# @date:   12/20/2012
#
# @note:   Open Pinball Project
#          Copyright 2012, Hugh Spahr
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
# Input driver board tests.
#
#===============================================================================

testVers = '00.00.02'

import sys
import serial
import array
import time
import re
import msvcrt
import rs232Intf

port = 'COM1'
testNum = 0
data = ""
NUM_MSGS = 1
numSolBrd = 0
solAddrArr = []
currSolData = []
numInpBrd = 0
inpAddrArr = []
currInpData = []

inpCfg = [ [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ] ]

<<<<<<< .mine
solCfg = [ [ '\x00', '\xff', '\x07', '\x00', '\xff', '\x07', \
             '\x00', '\xff', '\x07', '\x00', '\xff', '\x07', \
             '\x00', '\xff', '\x07', '\x00', '\xff', '\x07', \
             '\x00', '\xff', '\x07', '\x00', '\xff', '\x07' ] ]
=======
solCfg = [ [ rs232Intf.CFG_INP_STATE, '\x30', '\x04', rs232Intf.CFG_INP_STATE, '\x30', '\x04', \
             rs232Intf.CFG_INP_STATE, '\x30', '\x04', rs232Intf.CFG_INP_STATE, '\x30', '\x04', \
             rs232Intf.CFG_INP_STATE, '\x30', '\x04', rs232Intf.CFG_INP_STATE, '\x30', '\x04', \
             rs232Intf.CFG_INP_STATE, '\x30', '\x04', rs232Intf.CFG_INP_STATE, '\x30', '\x04' ] ]
>>>>>>> .r55

solCfg1 = [ [ '\x01', '\x30', '\x04', '\x01', '\x30', '\x04', \
              '\x01', '\x30', '\x04', '\x01', '\x30', '\x04', \
              '\x01', '\x30', '\x04', '\x01', '\x30', '\x04', \
              '\x01', '\x30', '\x04', '\x01', '\x30', '\x04' ] ]

#grab data from serial port
def getSerialData():
    global ser
    resp = ser.read(32)
    return (resp)

#send inventory cmd
def sendInvCmd():
    global ser
    cmdArr = []
    cmdArr.append(rs232Intf.INV_CMD)
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)

#rcv inventory resp
def rcvInvResp():
    global numSolBrd
    global solAddrArr
    global numInpBrd
    global inpAddrArr
    global currInpData
    data = getSerialData();
    print repr(data)
    #First byte should be inventory cmd
    index = 1
    if (data[0] != rs232Intf.INV_CMD):
        return (100)
    while (data[index] != rs232Intf.EOM_CMD):
        if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_SOL_CARD)):
            numSolBrd = numSolBrd + 1
            solAddrArr.append(data[index])
            currSolData.append(0)
        elif ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_INP_CARD)):
            numInpBrd = numInpBrd + 1
            inpAddrArr.append(data[index])
            currInpData.append(0)
        index = index + 1
    print "Found %d solenoid brds." % numSolBrd
    print "Addr = "
    print solAddrArr
    print "Found %d input brds." % numInpBrd
    print "Addr = "
    print inpAddrArr
    return (0)

#send input cfg cmd
def sendInpCfgCmd(cardNum, cfg):
    global ser
    global numInpBrd
    global inpAddrArr
    if (cardNum >= numInpBrd):
        return (200)    
    cmdArr = []
    cmdArr.append(inpAddrArr[cardNum])
    cmdArr.append(rs232Intf.CFG_INP_CMD)
    for loop in range(rs232Intf.NUM_INP_PER_BRD):
        if ((cfg == rs232Intf.CFG_INP_STATE) or (cfg != rs232Intf.CFG_INP_FALL_EDGE) or \
            (cfg != rs232Intf.CFG_INP_RISE_EDGE)):
            cmdArr.append(cfg)
        else:
            cmdArr.append(inpCfg[cardNum][loop])
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv end of message resp
def rcvEomResp():
    data = getSerialData();
    if (data[0] != rs232Intf.EOM_CMD):
        return (300)
    return (0)

#send read input board
def sendReadInpBrdCmd(cardNum):
    global ser
    global numInpBrd
    global inpAddrArr
    if (cardNum >= numInpBrd):
        return (400)
    cmdArr = []
    cmdArr.append(inpAddrArr[cardNum])
    cmdArr.append(rs232Intf.READ_INP_BRD_CMD)
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv read input cmd
def rcvReadInpResp(cardNum):
    global ser
    global numInpBrd
    global inpAddrArr
    global currInpData
    data = getSerialData();
    if (data[0] != inpAddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(inpAddrArr[cardNum]))
        print repr(data)
        return (500)
    if (data[1] != rs232Intf.READ_INP_BRD_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_INP_BRD_CMD))
        print repr(data)
        return (501)
    if (data[4] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[4]),ord(rs232Intf.EOM_CMD))
        return (502)
    currInpData[cardNum] = (ord(data[2]) << 8) | ord(data[3])
    return (0)

#send sol cfg cmd
def sendSolCfgCmd(cardNum, cfgNum):
    global ser
    global numSolBrd
    global solAddrArr
    if (cardNum >= numSolBrd):
        return (600)    
    cmdArr = []
    cmdArr.append(solAddrArr[cardNum])
    cmdArr.append(rs232Intf.CFG_SOL_CMD)
    for loop in xrange(rs232Intf.NUM_SOL_PER_BRD):
        if cfgNum == 0:
            cmdArr.append(solCfg[cardNum][loop * 3])
            cmdArr.append(solCfg[cardNum][(loop * 3) + 1])
            cmdArr.append(solCfg[cardNum][(loop * 3) + 2])
        else:
            cmdArr.append(solCfg1[cardNum][loop * 3])
            cmdArr.append(solCfg1[cardNum][(loop * 3) + 1])
            cmdArr.append(solCfg1[cardNum][(loop * 3) + 2])
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send read input board
def sendReadSolBrdCmd(cardNum):
    global ser
    global numSolBrd
    global solAddrArr
    if (cardNum >= numSolBrd):
        return (700)
    cmdArr = []
    cmdArr.append(solAddrArr[cardNum])
    cmdArr.append(rs232Intf.READ_SOL_INP_CMD)
    cmdArr.append('\x00')
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv read input cmd
def rcvReadSolResp(cardNum):
    global ser
    global numSolBrd
    global solAddrArr
    global currSolData
    data = getSerialData();
    if (data[0] != solAddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(solAddrArr[cardNum]))
        print repr(data)
        return (800)
    if (data[1] != rs232Intf.READ_SOL_INP_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_SOL_INP_CMD))
        print repr(data)
        return (801)
    if (data[3] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[3]),ord(rs232Intf.EOM_CMD))
        return (802)
    currSolData[cardNum] = ord(data[2])
    return (0)

def endTest(error):
    global ser
    global errMsg
    print "\nError code =", error
    ser.close()
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(error)

#Main code
end = False
boot = False
for arg in sys.argv:
  if arg.startswith('-port='):
    port = arg.replace('-port=','',1)
  elif arg.startswith('-test='):
    testNum = int(arg.replace('-test=','',1))
  elif arg.startswith('-?'):
    print "python inpDrvTest.py [OPTIONS]"
    print "    -?                 Options Help"
    print "    -port=portName     COM port number, defaults to COM1"
    print "    -test=testNum      test number, defaults to 0\n"
    print "    -boot              force a single board into bootloader\n"
    print "-test=0: Send inventory and verify response 10000 times."
    print "-test=1: Read first input board continuously.  ('x' exits)"
    print "-test=2: Read first solenoid board continuously.  ('x' exits)"
    end = True
  elif arg.startswith('-boot'):
    boot = True
if end:
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(0)
try:
    ser=serial.Serial(port, baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
except serial.SerialException:
    print "\nCould not open " + port
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(1)
print "Sending inventory cmd"
bad = False
sendInvCmd()
rcvInvResp()
if (boot):
    if ((numSolBrd == 0) and (numInpBrd == 1)) or ((numSolBrd == 1) and (numInpBrd == 1)):
        cmdArr = []
        if (numInpBrd == 1):
            cmdArr.append(inpAddrArr[0])
        else:
            cmdArr.append(solAddrArr[0])
        cmdArr.append(rs232Intf.GO_BOOT_CMD)
        sendCmd = ''.join(cmdArr)
        ser.write(sendCmd)
        print "Sent Go Boot command."
        time.sleep(1)
    else:
        print "Only one board should be attached"
        bad = True
if (testNum == 0):
    for superLoop in range(10000):
        sendInvCmd()
        data = getSerialData();
        if (data[0] != rs232Intf.INV_CMD):
            print "Bad resp, index = %d, data = %d" % (0, ord(data[0]))
            bad = True
        if (data[1] != '\x10'):
            print repr(data)
            print "Bad resp, index = %d, data = %d" % (1, ord(data[1]))
            bad = True
        if (data[2] != rs232Intf.EOM_CMD):
            print repr(data)
            print "Bad resp, index = %d, data = %d" % (2, ord(data[2]))
            bad = True
        if (bad):
            break;
        print "\nSuccessful loop."
elif (testNum == 1):
    sendInpCfgCmd(0, rs232Intf.CFG_INP_STATE)
    error = rcvEomResp()
    if error: endTest(error)
    exitReq = False
    count = 0
    while (not exitReq):
        sendReadInpBrdCmd(0)
        error = rcvReadInpResp(0)
        if error:
            print "\nCount = %d" % count
            endTest(error)
        outArr = []
        outArr.append('\r')
        for loop in range(rs232Intf.NUM_INP_PER_BRD):
            if (currInpData[0] & (1 << (rs232Intf.NUM_INP_PER_BRD - loop - 1))):
                outArr.append('1')
            else:
                outArr.append('0')
        sys.stdout.write(''.join(outArr))
        count = count + 1
        
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if ((char == 'x') or (char == 'X')):
                print "\nCount = %d" % count
                exitReq = True
elif (testNum == 2):
    sendSolCfgCmd(0,0)
    error = rcvEomResp()
    if error: endTest(error)
    exitReq = False
    count = 0
    while (not exitReq):
        sendReadSolBrdCmd(0)
        error = rcvReadSolResp(0)
        if error:
            print "\nCount = %d" % count
            endTest(error)
        outArr = []
        outArr.append('\r')
        for loop in range(rs232Intf.NUM_SOL_PER_BRD):
            if (currSolData[0] & (1 << (rs232Intf.NUM_SOL_PER_BRD - loop - 1))):
                outArr.append('1')
            else:
                outArr.append('0')
        sys.stdout.write(''.join(outArr))
        count = count + 1
        
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if ((char == 'x') or (char == 'X')):
                print "\nCount = %d" % count
                exitReq = True
elif (testNum == 3):
    sendSolCfgCmd(0,1)
    error = rcvEomResp()
    if error: endTest(error)
    exitReq = False
    count = 0
    while (not exitReq):
        sendReadSolBrdCmd(0)
        error = rcvReadSolResp(0)
        if error:
            print "\nCount = %d" % count
            endTest(error)
        outArr = []
        outArr.append('\r')
        for loop in range(rs232Intf.NUM_SOL_PER_BRD):
            if (currSolData[0] & (1 << (rs232Intf.NUM_SOL_PER_BRD - loop - 1))):
                outArr.append('1')
            else:
                outArr.append('0')
        sys.stdout.write(''.join(outArr))
        count = count + 1
        
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if ((char == 'x') or (char == 'X')):
                print "\nCount = %d" % count
                exitReq = True
elif (testNum == 4):
    sendSolCfgCmd(0,1)
    error = rcvEomResp()
    if error: endTest(error)
    exitReq = False
    count = 0
    while (not exitReq):
        sendReadSolBrdCmd(0)
        error = rcvReadSolResp(0)
        if error:
            print "\nCount = %d" % count
            endTest(error)
        outArr = []
        outArr.append('\r')
        for loop in range(rs232Intf.NUM_SOL_PER_BRD):
            if (currSolData[0] & (1 << (rs232Intf.NUM_SOL_PER_BRD - loop - 1))):
                outArr.append('1')
            else:
                outArr.append('0')
        sys.stdout.write(''.join(outArr))
        count = count + 1
        
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if ((char == 'x') or (char == 'X')):
                print "\nCount = %d" % count
                exitReq = True
ser.close()
print "\nSuccessful completion."
print "\nPress any key to close window"
ch = msvcrt.getch()
sys.exit(0)
