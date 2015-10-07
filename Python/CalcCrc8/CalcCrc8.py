#!/usr/bin/env python
#
#===============================================================================
## @mainpage
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

#===============================================================================
##
# @file    CalcCrc8.py
# @author  Hugh Spahr
# @date    6/19/2014
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief Calculate the CRC8 of a message.

#===============================================================================

import sys
import os

## Main
#
#  Read passed in arguments.  Create TK window.
#
#  @param  argv          [in]   Passed in arguments
#  @return None 
def main(argv=None):

    end = False

    if argv is None:
        argv = sys.argv
    for arg in argv:
        if arg.startswith('-?'):
            print "python CalcCrc8.py [OPTIONS]"
            print "    -?                 Options Help"
            end = True
    if end:
        return 0

    CRC8Lookup = [0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, \
                  0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d]

    while (not end):
        print "Enter message [ex:  0x11 0x22 0x33]:"
        msg = sys.stdin.readline()
        msgBytes = msg.split()
        if (len(msgBytes) != 0):
            msgInts = []
            for indByte in msgBytes:
                msgInts.append(int(indByte, 16))
            crc8 = 0xff
            for indInt in msgInts:
                crc8 = (((crc8 << 4) & 0xf0) ^ CRC8Lookup[ \
                    (((crc8) ^ (indInt)) >> 4) & 0x0f])
                crc8 = (((crc8 << 4) & 0xf0) ^ CRC8Lookup[ \
                    (((crc8 >> 4) & 0x0f) ^ (indInt)) & 0x0f])
            print "CRC8 = 0x%02x" % crc8
        else:
            end = True
    return (0)

if __name__ == "__main__":
    sys.exit(main())
