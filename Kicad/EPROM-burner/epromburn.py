#!/usr/bin/env python
testVers = '00.00.04'

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
baseAddr = 0

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
    #output the data to the flash
    pportData &= ~DATA_SHIFT_OE
    pport.setData(pportData)
    #latch the address into flash
    pportData &= ~FLASH_WE
    pport.setData(pportData)
    #latch the data into flash
    pportData |= FLASH_WE
    pport.setData(pportData)
    #disable output of data to the flash
    pportData |= DATA_SHIFT_OE
    pport.setData(pportData)
        
def eraseFlash():
    print "\nErasing flash."
    sendAddrData(0x5555aa)
    sendAddrData(0x2aaa55)
    sendAddrData(0x555580)
    sendAddrData(0x5555aa)
    sendAddrData(0x2aaa55)
    sendAddrData(0x555510)
    time.sleep(1)
    print "\nErase complete."

def writeByte(data):
    global baseAddr
    if ((baseAddr & 0xff) == 0):
        print "Writing addr: 0x%04x, data: 0x%02x" % (baseAddr, ord(data))
    sendAddrData(0x5555aa)
    sendAddrData(0x2aaa55)
    sendAddrData(0x5555a0)
    sendAddrData((baseAddr << 8) | ord(data))
    baseAddr = baseAddr + 1
    
end = False
erase = 'y'
print ""
for arg in sys.argv:
    if arg.startswith('-file='):
        filename = arg.replace('-file=','',1)
    elif arg.startswith('-erase='):
        erase = arg.replace('-erase=','',1)
    elif arg.startswith('-addr='):
        baseAddr = int(arg.replace('-addr=','',1),0)
    elif arg.startswith('-?'):
        print "\npython epromburn.py [OPTIONS]"
        print "    -?                 Options Help"
        print "    -file=fileName     file name, no default"
        print "    -erase=Y/N         erase, 'Y' for yes, 'N' for no"
        print "    -addr=baseAddr     base address bits, defaults 0x00"
        end = True
if end:
    print "\nPress any key to close window"
    ch = msvcrt.getch()
    sys.exit(0)
print "Initialize parallel port."
pportData = FLASH_WE | FLASH_OE
pport.setData(pportData)
pport.setInitOut(0)
pport.setAutoFeed(0)
pport.setDataStrobe(0)
if (erase == 'y') or (erase == 'Y'):
    #erase the Flash
    eraseFlash()
print "Opening file."
fileHndl = open(filename,'r + b')
while not end:
    data = fileHndl.read(1)
    if data == "":
        end = True
    else:
        writeByte(data)
print "\nFinished flash write."
fileHndl.close()
