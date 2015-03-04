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
# @file    pygameFunc.py
# @author  Hugh Spahr
# @date    4/22/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Pygame functions.

#===============================================================================

import pygame
from dispConstIntf import DispConst
import dispIntf

## Pygame data class.
#
#  Handles communication with pygame thread.  It contains functions for
#  acting on keypress events and updating the pygame displays
class Pygame_Data():
    #input mode
    INPMODE_INPUT = 0
    INPMODE_SOUND = 1
    INPMODE_LIGHTS = 2
    
    NO_KEY_PRESS = '\xff'
    
    ## Previous score to see if there has been a change
    prevScore = [0, 0, 0, 0]
    
    ## Previous player num display
    prevPlyrNum = 0
    
    ## Previous credit/ball num display
    prevCreditBallNum = 0

    ## Previous background image
    prevBgndImage = 0
    
    ## Game data object pointer
    GameData = None

    ## The constructor.
    def __init__(self, gameData):
        Pygame_Data.inpMode = Pygame_Data.INPMODE_INPUT
        Pygame_Data.GameData = gameData
        
    ## Process pygame events function
    #
    #  Grab the event list.  Parse each event and change the mode,
    #  increment the score, exit the game, play the sound, etc.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Proc_Pygame_Events(self):
        keyPress = Pygame_Data.NO_KEY_PRESS
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        return done

    ## Update pygame displays
    #
    #  Call the appropriate update display interface to update displays
    #  that have changed.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Update_Displays(self):
        if (Pygame_Data.prevBgndImage != Pygame_Data.GameData.bgndImage): 
            dispIntf.updateBgnd(Pygame_Data.GameData.bgndImage)
            Pygame_Data.prevBgndImage = Pygame_Data.GameData.bgndImage
            
        if (Pygame_Data.prevPlyrNum != Pygame_Data.GameData.currPlyrDisp):
            Pygame_Data.GameData.currDisp[DispConst.DISP_PLAYER_NUM] = Pygame_Data.GameData.currPlyrDisp
            Pygame_Data.GameData.updDisp |= (1 << DispConst.DISP_PLAYER_NUM)
            Pygame_Data.prevPlyrNum = Pygame_Data.GameData.currPlyrDisp
        if (Pygame_Data.prevCreditBallNum != Pygame_Data.GameData.creditBallNumDisp):
            Pygame_Data.GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = Pygame_Data.GameData.creditBallNumDisp
            Pygame_Data.GameData.updDisp |= (1 << DispConst.DISP_CREDIT_BALL_NUM)
            Pygame_Data.prevCreditBallNum = Pygame_Data.GameData.creditBallNumDisp
        for index in xrange(Pygame_Data.GameData.GameConst.MAX_NUM_PLYRS):
            if (Pygame_Data.prevScore[index] != Pygame_Data.GameData.score[index]):
                Pygame_Data.GameData.currDisp[DispConst.DISP_PLAYER1 + index] = Pygame_Data.GameData.score[index]
                Pygame_Data.GameData.updDisp |= (1 << (DispConst.DISP_PLAYER1 + index))
                Pygame_Data.prevScore[index] = Pygame_Data.GameData.score[index]

    ## Update background music
    #
    #  See if the background music bitfield has changed.  If so,
    #  turn on/off the channels.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Update_Bgnd_Music(self):
        if Pygame_Data.GameData.bgndSound != Pygame_Data.GameData.prevBgndSound:
            if Pygame_Data.GameData.bgndSound == 0xffffffff:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.load(Pygame_Data.GameData.rulesDir + "/" + Pygame_Data.GameData.BgndMusic.BGND_MUSIC_FILES[Pygame_Data.GameData.bgndSound])
                pygame.mixer.music.play(-1)
            Pygame_Data.GameData.prevBgndSound = Pygame_Data.GameData.bgndSound
            
