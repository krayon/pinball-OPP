#!/usr/bin/env python
#
# Warning - This is an auto-generated file.  All changes to this file will
# be overwritten next time GenPyCode.py is re-run.  Do not change this file
# unless you want to start hand editing the files.
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
# @file    sounds.py
# @author  AutoGenerated
# @date    02/08/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief This is an enumeration of all the sounds.

#===============================================================================

## Sounds enumeration.
#  Contains an entry for each sound
class Sounds():
    def __init__(self):
        pass
    
    SOUND_HOWDYFOLKS     = 0
    SOUND_YALL_COME_BACK = 1
    SOUND_HELL_OF_A_SHOT = 2
    SOUND_NICE_SHOOTIN_TEX = 3
    SOUND_DING_DING      = 4
    SOUND_WAH_WUH        = 5

    ## Sound file list
    # Indexed into using the [Sounds](@ref sounds.Sounds) class
    SND_FILES = ["sounds/howdyFolks.wav", "sounds/yallComeBack.wav", "sounds/hellOfaShotMister.wav", "sounds/niceShootinTex.wav", "sounds/ding_ding.wav", 
        "sounds/wah_wuh.wav"]
