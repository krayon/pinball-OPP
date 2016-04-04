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
# @file:   Gen2Test.py
# @author: Hugh Spahr
# @date:   12/12/2015
#
# @note:   Open Pinball Project
#          Copyright 2015, Hugh Spahr
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
# Tests for Gen2 cards based off input driver tests.
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
currInpData = []
numGen2Brd = 0
gen2AddrArr = []

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

# Config inputs as all state inputs
wingCfg = [ [ rs232Intf.WING_NEO, rs232Intf.WING_SOL, rs232Intf.WING_INP, rs232Intf.WING_INCAND ] ]

# Config inputs as all state inputs
inpCfg = [ [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ] ]

# Config for solenoid wing board in second position, first two config'd as flippers, second two config'd as one-shots
solCfg =  [ [ '\x00', '\x00', '\x00', '\x00', '\x00', '\x00',
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00',
              rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
              rs232Intf.CFG_SOL_USE_SWITCH, '\x10', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x10', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00' ] ]

# Config color table
#              Entry 0                 Entry 1                 Entry 2                 Entry 3 */
colorCfg = [ [ '\xff', '\x00', '\x00', '\x00', '\xff', '\x00', '\x00', '\x00', '\xff', '\xff', '\xff', '\x00', \
               '\xff', '\x00', '\xff', '\x00', '\xff', '\xff', '\xff', '\xff', '\xff', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x10', \
            ] ]

#calculate a crc8
def calcCrc8(msgChars):
    crc8Byte = 0xff
    for indChar in msgChars:
        indInt = ord(indChar)
        crc8Byte = CRC8ByteLookup[crc8Byte ^ indInt];
    return (chr(crc8Byte))


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
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    data = getSerialData();
    #First byte should be inventory cmd
    index = 1
    if (data[0] != rs232Intf.INV_CMD):
        return (100)
    while (data[index] != rs232Intf.EOM_CMD):
        if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_GEN2_CARD)):
            numGen2Brd = numGen2Brd + 1
            gen2AddrArr.append(data[index])
            currInpData.append(0)
        index = index + 1
    print "Found %d Gen2 brds." % numGen2Brd
    print "Addr = "
    print [hex(ord(n)) for n in gen2AddrArr]
    return (0)

#send input cfg cmd
def sendInpCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (200)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.CFG_INP_CMD)
    for loop in range(rs232Intf.NUM_G2_INP_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.inpCfg[cardNum][loop])
        else:
            cmdArr.append(inpCfg[cardNum][loop])
    cmdArr.append(calcCrc8(cmdArr))
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
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (400)
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.READ_GEN2_INP_CMD)
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv read input cmd
def rcvReadInpResp(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    data = getSerialData();
    if (data[0] != inpAddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (500)
    if (data[1] != rs232Intf.READ_GEN2_INP_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_INP_BRD_CMD))
        print repr(data)
        return (501)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (502)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (502)
    currInpData[cardNum] = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    return (0)

#send sol cfg cmd
def sendSolCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (600)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.CFG_SOL_CMD)
    for loop in xrange(rs232Intf.NUM_G2_SOL_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.solCfg[cardNum][loop * 3])
            cmdArr.append(cfgFile.solCfg[cardNum][(loop * 3) + 1])
            cmdArr.append(cfgFile.solCfg[cardNum][(loop * 3) + 2])
        else:
            cmdArr.append(solCfg[cardNum][loop * 3])
            cmdArr.append(solCfg[cardNum][(loop * 3) + 1])
            cmdArr.append(solCfg[cardNum][(loop * 3) + 2])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send read wing cfg board
def sendReadWingCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= gen2AddrArr):
        return (700)
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.GET_GEN2_CFG)
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv read wing cfg resp
def rcvReadWingCfgResp(cardNum):
    global ser
    global gen2AddrArr
    global currSolData
    data = getSerialData();
    if (data[0] != gen2AddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (800)
    if (data[1] != rs232Intf.READ_SOL_INP_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.GET_GEN2_CFG))
        print repr(data)
        return (801)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (802)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (803)
    currWingCfg[cardNum] = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    return (0)

#send wing cfg cmd
def sendWingCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (900)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.SET_GEN2_CFG)
    for loop in range(rs232Intf.NUM_G2_WING_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.wingCfg[cardNum][loop])
        else:
            cmdArr.append(wingCfg[cardNum][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send color table cfg cmd
def sendColorCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (900)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.SET_NEO_COLOR_TBL)
    for loop in range((rs232Intf.NUM_COLOR_TBL * 3) + 1):
        if loadCfg:
            cmdArr.append(cfgFile.colorCfg[cardNum][loop])
        else:
            cmdArr.append(colorCfg[cardNum][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
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
saveCfg = False
eraseCfg = False
loadCfg = False
for arg in sys.argv:
  if arg.startswith('-port='):
    port = arg.replace('-port=','',1)
  elif arg.startswith('-test='):
    testNum = int(arg.replace('-test=','',1))
  elif arg.startswith('-?'):
    print "python Gen2Test.py [OPTIONS]"
    print "    -?                 Options Help"
    print "    -port=portName     COM port number, defaults to COM1"
    print "    -test=testNum      test number, defaults to 0"
    print "    -boot              force a single board into bootloader"
    print "    -saveCfg           save a cfg on a single board."
    print "        Only 1 board can be attached.  Load configuration option must also be set."
    print "    -eraseCfg          erase a cfg on a single board."
    print "        Only 1 board can be attached.\n"
    print "    -loadCfg           configuration is read from cfgFile.py"
    print "        Only 1 board can be attached.  Uses wingCfg, solCfg, inpCfg and colorCfg\n"
    print "-test=0: Send inventory and verify response 10000 times."
    print "-test=1: Read first Gen2 inputs continuously.  ('x' exits)"
    end = True
  elif arg.startswith('-boot'):
    boot = True
  elif arg.startswith('-saveCfg'):
    saveCfg = True
  elif arg.startswith('-eraseCfg'):
    eraseCfg = True
  elif arg.startswith('-loadCfg'):
    loadCfg = True
if end:
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(0)
try:
    ser=serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
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
    #Make test num invalid
    testNum = 255
    if (numGen2Brd == 1):
        cmdArr = []
        cmdArr.append(gen2AddrArr[0])
        cmdArr.append(rs232Intf.GO_BOOT_CMD)
        cmdArr.append(calcCrc8(cmdArr))
        sendCmd = ''.join(cmdArr)
        ser.write(sendCmd)
        print "Sent Go Boot command."
        time.sleep(1)
    else:
        print "Only one board should be attached"
        bad = True
elif (saveCfg):
    #Make test num invalid
    testNum = 255
    if loadCfg:
        import cfgFile
    if (numGen2Brd == 1):
        #Save config for Gen2 board
        print "Sending wing cfg."
        sendWingCfgCmd(0)
        error = rcvEomResp()
        if error: endTest(error)
        print "Sending input cfg."
        sendInpCfgCmd(0)
        error = rcvEomResp()
        if error: endTest(error)
        print "Sending solenoid cfg."
        sendSolCfgCmd(0)
        error = rcvEomResp()
        if error: endTest(error)
        if loadCfg:
            colorTblExists = 'cfgFile.colorCfg' in locals() or 'cfgFile.colorCfg' in globals()
            if colorTblExists:
                print "Sending color table cfg."
                sendColorCfgCmd(0)
                error = rcvEomResp()
                if error: endTest(error)
            else:
                print "Skipping sending color table."
        else:
            print "Sending color table cfg."
            sendColorCfgCmd(0)
            error = rcvEomResp()
            if error: endTest(error)
        print "Sending save cfg command."
        cmdArr = []
        cmdArr.append(gen2AddrArr[0])
        cmdArr.append(rs232Intf.SAVE_CFG_CMD)
        cmdArr.append(calcCrc8(cmdArr))
        sendCmd = ''.join(cmdArr)
        ser.write(sendCmd)
        print "Done save cfg command."
        time.sleep(1)
    else:
        print "Only one board should be attached"
        bad = True        
elif (eraseCfg):
    #Make test num invalid
    testNum = 255
    cmdArr = []
    if (numGen2Brd == 1):
        #Erase config for Gen2 board
        cmdArr.append(gen2AddrArr[0])
        cmdArr.append(rs232Intf.ERASE_CFG_CMD)
        cmdArr.append(calcCrc8(cmdArr))
        sendCmd = ''.join(cmdArr)
        ser.write(sendCmd)
        print "Sent erase cfg command."
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
        if (data[1] != '\x20'):
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
        for loop in range(rs232Intf.NUM_G2_INP_PER_BRD):
            if (currInpData[0] & (1 << (rs232Intf.NUM_G2_INP_PER_BRD - loop - 1))):
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
