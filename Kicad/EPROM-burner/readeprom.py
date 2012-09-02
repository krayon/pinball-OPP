#!/usr/bin/env python
testVers = '00.00.03'

import parallel
import sys
import time
import msvcrt

ADDR16                      = 0x80
FLASH_WE                    = 0x40
FLASH_OE                    = 0x20
FLASH_CE                    = 0x10
SHIFT_REG_DATA              = 0x08
DATA_SHIFT_OE               = 0x04
LATCH_DATA_SHIFT            = 0x02
DATA_SHIFT_CLK              = 0x01

pport = parallel.Parallel()
pportData = 0
addr = 0

def sendAddrData(addrData):
    global pport
    global pportData

    #set addr16/addr17.  Note:  addr shifted 8
    if (addrData & 0x1000000):
        pportData |= ADDR16
    else:
        pportData &= ~ADDR16
    pport.setData(pportData)
    if (addrData & 0x2000000):
        pport.setAutoFeed(1)
    else:
        pport.setAutoFeed(0)
    for loop in range(8,24):
        if (addrData & (1 << loop)):
            pportData |= SHIFT_REG_DATA
        else:
            pportData &= ~SHIFT_REG_DATA
        #set the data bit
        pport.setData(pportData)
        #clock addr/data shift regs
        pportData |= DATA_SHIFT_CLK
        pport.setDataStrobe(1)
        pport.setData(pportData)
        #clear the data clock
        pportData &= ~DATA_SHIFT_CLK
        pport.setDataStrobe(0)
        pport.setData(pportData)
    for loop in range(8):
        if (addrData & (1 << loop)):
            pportData |= SHIFT_REG_DATA
        else:
            pportData &= ~SHIFT_REG_DATA
        #set the data bit
        pport.setData(pportData)
        #clock addr/data shift regs
        pportData |= DATA_SHIFT_CLK
        pport.setDataStrobe(1)
        pport.setData(pportData)
        #clear the data clock
        pportData &= ~DATA_SHIFT_CLK
        pport.setDataStrobe(0)
        pport.setData(pportData)
    #latch addr/data shift regs
    pportData |= LATCH_DATA_SHIFT
    pport.setData(pportData)
    pport.setInitOut(1)
    #latch addr/data shift regs
    pportData &= ~LATCH_DATA_SHIFT
    pport.setData(pportData)
    pport.setInitOut(0)
        
def readByte():
    global addr
    print "Reading addr: 0x%04x" % (addr)
    sendAddrData(addr << 8)
    addr = addr + 1
    
end = False
erase = 'y'
print ""
for arg in sys.argv:
    if arg.startswith('-addr='):
        addr = int(arg.replace('-addr=','',1),0)
    elif arg.startswith('-?'):
        print "\npython readeprom.py [OPTIONS]"
        print "    -?                 Options Help"
        print "    -addr=addr         address to read, defaults to 0"
        end = True
if end:
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(0)
print "Initialize parallel port."
pportData = FLASH_WE | DATA_SHIFT_OE
pport.setData(pportData)
pport.setInitOut(0)
pport.setAutoFeed(0)
pport.setDataStrobe(0)
while not end:
    readByte()
    print "Press enter for next byte, 'y' or 'Y' to end"
    ch = msvcrt.getch()
    if (ch == 'y') or (ch == 'Y'):
        end = True
print "\nPress any key to close window"
ch = msvcrt.getch()
sys.exit(0)
