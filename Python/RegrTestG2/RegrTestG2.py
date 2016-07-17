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
import subprocess
import os

port = 'COM1'
vers = ""
testNum = 255
data = ""
NUM_MSGS = 1
currInpData = []
numGen2Brd = 0
gen2AddrArr = []
currWingCfg = []

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
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00' ],
            [ '\x00', '\x00', '\x00', '\x00', '\x00', '\x00',
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00',
              rs232Intf.CFG_SOL_USE_SWITCH, '\x01', '\x01', rs232Intf.CFG_SOL_USE_SWITCH, '\xff', '\x0f', \
              rs232Intf.CFG_SOL_USE_SWITCH, '\x01', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\xff', '\x00', \
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
    global currWingCfg
    data = getSerialData();
    #First byte should be inventory cmd
    index = 1
    numGen2Brd = 0
    gen2AddrArr = []
    currInpData = []
    currWingCfg = []
    if (data[0] != rs232Intf.INV_CMD):
        return (100)
    while (data[index] != rs232Intf.EOM_CMD):
        if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_GEN2_CARD)):
            numGen2Brd = numGen2Brd + 1
            gen2AddrArr.append(data[index])
            currInpData.append(0)
            currWingCfg.append(0)
        index = index + 1
    print "Found %d Gen2 brds." % numGen2Brd
    print "Addr = %s" % [hex(ord(n)) for n in gen2AddrArr]
    return (0)

#send standard 4 byte command
def sendStd4ByteCmd(cmd):
    global ser
    cmdArr = []
    
    # First address for Gen2 cards is always 0x20
    cmdArr.append('\x20')
    cmdArr.append(cmd)
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)

#send get version cmd
def sendGetVersCmd():
    sendStd4ByteCmd(rs232Intf.GET_GET_VERS_CMD)

#rcv get version resp
def rcvGetVersResp(version):
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    global currWingCfg
    data = getSerialData();
    if (data[0] != gen2AddrArr[0]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[0]))
        print repr(data)
        return (200)
    if (data[1] != rs232Intf.GET_GET_VERS_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_INP_BRD_CMD))
        print repr(data)
        return (201)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (202)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (203)
    versResp = "%d.%d.%d.%d" % (ord(data[2]), ord(data[3]), ord(data[4]), ord(data[5]))
    print "Found version " + versResp
    if version:
        # Verify the version number if it was passed in on the command line
        if version != versResp:
            print "\n!!! Fail !!! Version does not match expected version.\n"
            print "Data = %s, expected = %s" % (versResp, version)
            return (204)
    return (0)

#send get serial number cmd
def sendSetSerNumCmd(serialNum):
    global ser
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.SET_SER_NUM_CMD)
    cmdArr.append(chr((serialNum >> 24) & 0xff))
    cmdArr.append(chr((serialNum >> 16) & 0xff))
    cmdArr.append(chr((serialNum >> 8) & 0xff))
    cmdArr.append(chr(serialNum & 0xff))
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)

#send get serial number cmd
def sendGetSerNumCmd():
    sendStd4ByteCmd(rs232Intf.GET_SER_NUM_CMD)

#rcv get serial number resp
def rcvGetSerNumResp():
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    global currWingCfg
    expectedSerialNum = 123456789
    data = getSerialData();
    if (data[0] != gen2AddrArr[0]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[0]))
        print repr(data)
        return (300)
    if (data[1] != rs232Intf.GET_SER_NUM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_INP_BRD_CMD))
        print repr(data)
        return (301)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (302)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (303)
    serialNum = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    print "Found serial num: %d" % serialNum
    if (serialNum == 0):
        sendSetSerNumCmd(expectedSerialNum)
        retCode = rcvEomResp()
        if (retCode != 0):
            print "\n!!! Fail !!! Could not program serial number into card.\n"
            return (304)
    elif (serialNum != expectedSerialNum):
        print "\n!!! Fail !!! Serial number not the expected value.\n"
        return (305)
    return (0)

#send reset cmd
def sendResetCmd():
    global ser
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.RESET_CMD)
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)

#Update code, tests go bootloader command
def TestGoBoot():
    global ser
    global gen2AddrArr
    
    print "\nForcing board into the boot loader.  Sent Go Boot command."
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.GO_BOOT_CMD)
    cmdArr.append(calcCrc8(cmdArr))
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    time.sleep(1)
    ser.close()

    command = "cd ..\cyflash &" \
       "c:\Python27\python.exe -m cyflash.__main__" + \
       " --serial " + port + " --serial_baudrate 115200" + \
       " ..\..\Creator\Gen2\Gen2.cydsn\CortexM0\ARM_GCC_493\Debug\Gen2.cyacd"
    print "Updating code to latest version."
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    if not "Device checksum verifies OK." in proc_stdout:
        print "!!! Fail !!! Update code failed.\n"
        return 400
    # Send inventory command so card "relearns" its address.
    try:
        ser=serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
    except serial.SerialException:
        print "\nCould not open " + port + " after upgrading firmware."
        return 401
    sendInvCmd()
    rcvInvResp()
    print "GoBoot tested successfully."
    return 0

def TestGetVersion(version):
    print "\nTesting Get Version command."
    sendGetVersCmd()
    retCode = rcvGetVersResp(version)
    return retCode

def TestGetSerialNum():
    print "\nTesting Get Serial Number command."
    sendGetSerNumCmd()
    retCode = rcvGetSerNumResp()
    return retCode

def ResetBoard():
    global ser
    sendResetCmd()
    ser.close()
    time.sleep(1)
    # Re-open the serial port.
    try:
        ser=serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
    except serial.SerialException:
        print "\nCould not open " + port + " when resetting card."
        return 550
    sendInvCmd()
    rcvInvResp()
    return 0

#Update board with standard configuration
def TestStoreStdCfg():
    global ser
    
    print "\nStoring standard configuration on the card."
    ser.close()

    command = "cd ..\Gen2Test & " \
       "c:\Python27\python.exe Gen2Test.py -port=" + port + " -eraseCfg & " \
       "c:\Python27\python.exe Gen2Test.py -port=" + port + " -saveCfg -loadCfg=regrCfg"
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    # Re-open the serial port.
    try:
        ser=serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
    except serial.SerialException:
        print "\nCould not open " + port + " updating configuration."
        return 500
    retCode = ResetBoard()
    if retCode: return retCode
    print "Store standard configuration successful."
    return 0

#Verify standard configuration, tests read input cmd, verifies
#solenoid configuration working for one-shots and PWMs
def VerifyStdCfg():
    print "\nVerify standard configuration."
    print "\nTest input switches for solenoids."
    print "Verify 0 and 1 act like flippers."
    print "Verify 2 and 3 act like one-shots."
    print "Press (y) if working, (n) if not working."
    ch = msvcrt.getch()
    if (ch != 'y') and (ch != 'Y'):
        print "\nStandard configuration for solenoids failed."
        return 601
    print "\nTest read input cmd for input switches."
    print "All inputs are configured in state mode."
    print "Press (y) if working, (n) if not working."
    exitReq = False
    while (not exitReq):
        sendReadInpBrdCmd()
        retCode = rcvReadInpResp()
        if retCode != 0:
            print "\nRead input response failed." % count
            return (retCode)
        outArr = []
        outArr.append('\r')
        for loop in range(rs232Intf.NUM_G2_INP_PER_BRD):
            if (currInpData[0] & (1 << (rs232Intf.NUM_G2_INP_PER_BRD - loop - 1))):
                outArr.append('1')
            else:
                outArr.append('0')
        sys.stdout.write(''.join(outArr))
        
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if (char != 'y') and (char != 'Y'):
                print "\nStandard configuration for inputs failed."
                retCode = 602
            else:
                retCode = 0
            exitReq = True
    return retCode

#Test processor can kick solenoids (with no auto clear)
#Verify on both one-shots and flipper configurations
def TestProcNoAutoClr():
    print "\nVerify main processor driving solenoids (no auto clear)."
    print "\nTurning on flipper 1 'on' for 1 second/'off' for 1 second."
    print "Press (y) if working, (n) if not working."
    exitReq = False
    while (not exitReq):
        sendKickSolCmd(0x0020, 0x0020)
        retCode = rcvEomResp()
        if retCode: return (retCode)
        time.sleep(1)
        sendKickSolCmd(0x0000, 0x0020)
        retCode = rcvEomResp()
        if retCode: return (retCode)
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if (char != 'y') and (char != 'Y'):
                print "\nSolenoid kick command failed for flippers."
                retCode = 1401
            else:
                retCode = 0
            exitReq = True
        if not exitReq:
            time.sleep(1)
    print "\nOne shot solenoid 3 firing continuously for 1 second/off for 1 second."
    print "Press (y) if working, (n) if not working."
    exitReq = False
    while (not exitReq):
        sendKickSolCmd(0x0080, 0x0080)
        retCode = rcvEomResp()
        if retCode: return (retCode)
        time.sleep(1)
        sendKickSolCmd(0x0000, 0x0080)
        retCode = rcvEomResp()
        if retCode: return (retCode)
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if (char != 'y') and (char != 'Y'):
                print "\nSolenoid kick command failed for one shots."
                retCode = 1402
            else:
                retCode = 0
            exitReq = True
        if not exitReq:
            time.sleep(1)
    return retCode

#Test processor can kick solenoids (with auto clear)
#Verify on both one-shots and flipper configurations
def TestProcAutoClr():
    # Reconfigure solenoid with auto clear bit set
    sendCfgIndSolCmd(0x04, 0x03, 0x30, 0x04)
    retCode = rcvEomResp()
    if retCode: return (retCode)
    
    print "\nVerify main processor driving solenoids (with auto clear)."
    print "\nTurning on flipper 0 'on', wait 1 second then repeat."
    print "Press (y) if working, (n) if not working."
    exitReq = False
    while (not exitReq):
        sendKickSolCmd(0x0010, 0x0010)
        retCode = rcvEomResp()
        if retCode: return (retCode)
        time.sleep(1)
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if (char != 'y') and (char != 'Y'):
                print "\nSolenoid kick command failed for flippers."
                retCode = 1501
            else:
                retCode = 0
            exitReq = True
        if not exitReq:
            time.sleep(1)
            
    # Reconfigure solenoid with auto clear bit set
    sendCfgIndSolCmd(0x06, 0x03, 0x10, 0x00)
    retCode = rcvEomResp()
    if retCode: return (retCode)
    print "\nOne shot solenoid 2 firing once, wait 1 second then repeat."
    print "Press (y) if working, (n) if not working."
    
    exitReq = False
    while (not exitReq):
        sendKickSolCmd(0x0040, 0x0040)
        retCode = rcvEomResp()
        if retCode: return (retCode)
        time.sleep(1)
        #Check if exit is requested
        while msvcrt.kbhit():
            char = msvcrt.getch()
            if (char != 'y') and (char != 'Y'):
                print "\nSolenoid kick command failed for one shots."
                retCode = 1502
            else:
                retCode = 0
            exitReq = True
        if not exitReq:
            time.sleep(1)
    return retCode

#Test solenoid configs, verifies configure all solenoids command works.
#Two solenoids are configured as flippers, one with minimum init kick/PWM,
#one with maximum init kick/PWM.  Two solenoids are configured as one shots
#with one having minimum init kick, and one having maximum init kick.
def TestSolenoidConfig():
    # Reconfigure all solenoids with single command
    sendSolCfgCmd(1)
    retCode = rcvEomResp()
    if retCode: return (retCode)
    
    print "\nVerify solenoid 0 is flipper with minimum (1 ms init kick/min PWM)"
    print "Verify solenoid 1 is flipper with maximum (255 ms init kick/max PWM)"
    print "Verify solenoid 2 is one shot with minimum (1 ms) init kick"
    print "Verify solenoid 3 is one shot with maximum (255 ms) init kick"
    print "Press (y) if working, (n) if not working."
    ch = msvcrt.getch()
    if (ch != 'y') and (ch != 'Y'):
        print "\nStandard configuration for solenoids failed."
        return 1601
    return 0

#send input cfg cmd
def sendInpCfgCmd():
    global ser
    global numGen2Brd
    global gen2AddrArr
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.CFG_INP_CMD)
    for loop in range(rs232Intf.NUM_G2_INP_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.inpCfg[0][loop])
        else:
            cmdArr.append(inpCfg[0][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv end of message resp
def rcvEomResp():
    data = getSerialData();
    if (data[0] != rs232Intf.EOM_CMD):
        return (800)
    return (0)

#send read input board
def sendReadInpBrdCmd():
    global ser
    global numGen2Brd
    global gen2AddrArr
    sendStd4ByteCmd(rs232Intf.READ_GEN2_INP_CMD)
    return (0)

#rcv read input cmd
def rcvReadInpResp():
    global ser
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    data = getSerialData();
    if (data[0] != gen2AddrArr[0]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[0]))
        print repr(data)
        return (1000)
    if (data[1] != rs232Intf.READ_GEN2_INP_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_INP_BRD_CMD))
        print repr(data)
        return (1001)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (1002)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (1003)
    currInpData[0] = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    return (0)

#send sol cfg cmd
def sendSolCfgCmd(cfgNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.CFG_SOL_CMD)
    for loop in xrange(rs232Intf.NUM_G2_SOL_PER_BRD):
        cmdArr.append(solCfg[cfgNum][loop * 3])
        cmdArr.append(solCfg[cfgNum][(loop * 3) + 1])
        cmdArr.append(solCfg[cfgNum][(loop * 3) + 2])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send read wing cfg board
def sendReadWingCfgCmd():
    sendStd4ByteCmd(rs232Intf.GET_GEN2_CFG)
    return (0)

#rcv read wing cfg resp
def rcvReadWingCfgResp():
    global ser
    global gen2AddrArr
    global currSolData
    global currWingCfg
    data = getSerialData();
    if (data[0] != gen2AddrArr[0]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[0]))
        print repr(data)
        return (1300)
    if (data[1] != rs232Intf.GET_GEN2_CFG):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.GET_GEN2_CFG))
        print repr(data)
        return (1301)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (1302)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (1303)
    currWingCfg[0] = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    print hex(ord(gen2AddrArr[0])),"WingCfg = 0x{:08x}".format(currWingCfg[0])
    print hex(ord(gen2AddrArr[0])),
    for index in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
        if data[index + 2] == rs232Intf.WING_SOL:
            print "SOL_WING ",
        elif data[index + 2] == rs232Intf.WING_INP:
            print "INP_WING ",
        elif data[index + 2] == rs232Intf.WING_INCAND:
            print "INCAND_WING ",
        elif data[index + 2] == rs232Intf.WING_SW_MATRIX_OUT:
            print "SW_MATRIX_OUT_WING ",
        elif data[index + 2] == rs232Intf.WING_SW_MATRIX_IN:
            print "SW_MATRIX_IN_WING ",
        elif data[index + 2] == rs232Intf.WING_NEO:
            print "NEO_WING ",
    print ""
    return (0)

#send wing cfg cmd
def sendWingCfgCmd():
    global ser
    global numGen2Brd
    global gen2AddrArr
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.SET_GEN2_CFG)
    for loop in range(rs232Intf.NUM_G2_WING_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.wingCfg[0][loop])
        else:
            cmdArr.append(wingCfg[0][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send color table cfg cmd
def sendColorCfgCmd():
    global ser
    global numGen2Brd
    global gen2AddrArr
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.SET_NEO_COLOR_TBL)
    for loop in range((rs232Intf.NUM_COLOR_TBL * 3) + 1):
        if loadCfg:
            cmdArr.append(cfgFile.colorCfg[0][loop])
        else:
            cmdArr.append(colorCfg[0][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send kick solenoid cmd
def sendKickSolCmd(solenoids, mask):
    global ser
    global gen2AddrArr
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.KICK_SOL_CMD)
    cmdArr.append(chr((solenoids >> 8) & 0xff))
    cmdArr.append(chr(solenoids & 0xff))
    cmdArr.append(chr((mask >> 8) & 0xff))
    cmdArr.append(chr(mask & 0xff))
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send cfg individual solenoid cmd
def sendCfgIndSolCmd(solIndex, cmd, initKick, offHold):
    global ser
    global gen2AddrArr
    cmdArr = []
    cmdArr.append(gen2AddrArr[0])
    cmdArr.append(rs232Intf.CFG_IND_SOL_CMD)
    cmdArr.append(chr(solIndex))
    cmdArr.append(chr(cmd))
    cmdArr.append(chr(initKick))
    cmdArr.append(chr(offHold))
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
skipProg = False
skipSaveStdCfg = False
for arg in sys.argv:
  if arg.startswith('-port='):
    port = arg.replace('-port=','',1)
  elif arg.startswith('-vers='):
    vers = arg.replace('-vers=','',1)
  elif arg.startswith('-skipProg'):
    skipProg = True
  elif arg.startswith('-skipSaveStdCfg'):
    skipSaveStdCfg = True
  elif arg.startswith('-?'):
    print "python RegrTestG2.py [OPTIONS]"
    print "    -?                 Options Help"
    print "    -port=portName     COM port number, defaults to COM1"
    print "    -vers=version num  Ex. 0.1.1.0"
    print "    -skipProg          Skip programming (used for debugging tests)"
    print "    -skipSaveStdCfg    Skip saving standard config (used for debugging tests)"
    end = True

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
sendInvCmd()
rcvInvResp()

# Verify only a single board is attached
if (numGen2Brd != 1):
    print "Only one board should be attached.  Exiting regression tests."
    sys.exit(2)
    
#Get the current configuration
sendReadWingCfgCmd()
rcvReadWingCfgResp()
    
# Verify the board is configured as Neopixel, solenoid, input and incandescent
if (currWingCfg[0] != 0x06010203):
    print "Regression testing board must have wing board configuration of:"
    print "Neopixel, solenoid, input, incandescent.  Exiting regression tests."
    sys.exit(3)

# Update code to newest version, also verifies go to bootloader command works
if not skipProg:
    retCode = TestGoBoot()
    if retCode != 0: sys.exit(retCode)

# Verify Get Version command
retCode = TestGetVersion(vers)
if retCode != 0: sys.exit(retCode)

# Verify Get Serial Number command
retCode = TestGetSerialNum()
if retCode != 0: sys.exit(retCode)

# Program the standard configuration
# Erases the configuration and stores the standard configuration
# to the card, and resets the card.  (Verification will happen when
# a second configuration is stored and saved.)
if not skipSaveStdCfg:
    retCode = TestStoreStdCfg()
    if retCode != 0: sys.exit(retCode)
else:
    #Reset the board to get back to the stored configuration so
    #rerunning regression tests will work
    ResetBoard()

retCode = VerifyStdCfg()
if retCode != 0: sys.exit(retCode)

retCode = TestProcNoAutoClr()
if retCode != 0: sys.exit(retCode)

retCode = TestProcAutoClr()
if retCode != 0: sys.exit(retCode)

retCode = TestSolenoidConfig()
if retCode != 0: sys.exit(retCode)

print "\nSuccessful completion."
print "\nPress any key to close window"
ch = msvcrt.getch()
sys.exit(0)