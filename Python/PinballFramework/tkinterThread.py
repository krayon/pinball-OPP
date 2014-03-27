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
# @file:   tkinterThread.py
# @author: Hugh Spahr
# @date:   3/26/2014
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
# This is the tkinter thread file that is used for the debug GUI.
#
#===============================================================================

vers = '00.00.01'

import Tkinter as tk
from threading import Thread
import time

class TkinterThread(Thread):
    def __init__(self):
        super(TkinterThread, self).__init__()
        
        #Some queue stuff to send data back and forth

        #private members
        self._runTkinterThread = True

    #Initialize comms to the hardware
    def init(self):
        pass
    
    def start(self):
        super(TkinterThread, self).start()
    
    def tkinterExit(self):
        self._runTkinterThread = False
    
    def run(self):
        count = 0
        root = tk.Tk()
        w, h = 50, 50
        embed = tk.Frame(root, width=w, height=h)
        embed.pack()
        text = tk.Button(root, text = 'Blah.')
        text.pack()
        root.update()
      
        while self._runTkinterThread:
            root.update()
            count += 1
            time.sleep(.1)
            print "tkinter thread: %d" % count
