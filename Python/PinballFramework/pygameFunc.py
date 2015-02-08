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
from gameData import GameData
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

    ## The constructor.
    def __init__(self):
        Pygame_Data.inpMode = Pygame_Data.INPMODE_INPUT
        
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
                elif event.key == pygame.K_i:
                    Pygame_Data.inpMode = Pygame_Data.INPMODE_INPUT
                    print "Input mode"
                elif event.key == pygame.K_s:
                    Pygame_Data.inpMode = Pygame_Data.INPMODE_SOUND
                    print "Sound mode"
                elif event.key == pygame.K_l:
                    Pygame_Data.inpMode = Pygame_Data.INPMODE_LIGHTS
                    print "Light mode"
                elif event.key == pygame.K_c:
                    GameData.credits += 1
                    if (GameData.gameMode == GameData.States.ATTRACT):
                        GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = GameData.credits
                        GameData.updDisp |= (1 << DispConst.DISP_CREDIT_BALL_NUM)
                elif event.key == pygame.K_g:
                    #Check if starting a game
                    if (GameData.gameMode == GameData.States.ATTRACT) and (GameData.credits > 0):
                        GameData.credits -= 1
                        GameData.gameMode = GameData.States.NORMAL_PLAY
                        GameData.numPlayers = 1
                        GameData.currBall = 0
                        GameData.currPlayer = 0
                        GameData.score[0] = 0
                      
                        #Set up player 1 score
                        GameData.currDisp[DispConst.DISP_PLAYER1] = GameData.score[0]
                      
                        #Clear player 2, 3, 4 scores
                        GameData.currDisp[DispConst.DISP_PLAYER2] = DispConst.DISP_BLANK
                        GameData.currDisp[DispConst.DISP_PLAYER3] = DispConst.DISP_BLANK
                        GameData.currDisp[DispConst.DISP_PLAYER4] = DispConst.DISP_BLANK
    
                        #Set player number, ball number
                        GameData.currDisp[DispConst.DISP_PLAYER_NUM] = GameData.currPlayer + 1
                        GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = 1
                        GameData.updDisp |= DispConst.UPD_ALL_DISPS
                      
                        #Play background music
                        pygame.mixer.music.load("sounds/bgndtrack.mp3")
                        pygame.mixer.music.play(-1)
                    #Check if another player is being added  
                    elif (GameData.gameMode == GameData.States.NORMAL_PLAY) and (GameData.credits > 0):
                        #Only allow adding players if during first ball
                        if (GameData.ballNum < 1) and (GameData.numPlayers < 4):
                            GameData.credits -= 1
                            GameData.score[GameData.numPlayers] = 0
                            GameData.currDisp[GameData.numPlayers + DispConst.DISP_PLAYER1] = GameData.score[GameData.numPlayers]
                            GameData.updDisp |= (1 << (GameData.numPlayers + DispConst.DISP_PLAYER1))
                            GameData.numPlayers += 1
                elif event.key == pygame.K_d:
                    #Drain the current ball
                    if (GameData.gameMode == GameData.States.NORMAL_PLAY):
                        #If more players, increment currPlayers
                        if (GameData.currPlayer + 1 < GameData.numPlayers):
                            GameData.currPlayer += 1
                            GameData.currDisp[DispConst.DISP_PLAYER_NUM] = GameData.currPlayer + 1
                            GameData.updDisp |= (1 << DispConst.DISP_PLAYER_NUM)
                        elif (GameData.ballNum + 1 < GameData.GameConst.BALLS_PER_GAME):
                            GameData.currPlayer = 0
                            GameData.currDisp[DispConst.DISP_PLAYER_NUM] = GameData.currPlayer + 1
                            GameData.updDisp |= (1 << DispConst.DISP_PLAYER_NUM)
                            GameData.ballNum += 1
                            GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = GameData.currPlayer + 1
                            GameData.updDisp |= (1 << DispConst.DISP_CREDIT_BALL_NUM)
                        else:
                            #Game over, blank player number
                            GameData.currDisp[DispConst.DISP_PLAYER_NUM] = DispConst.DISP_BLANK
                            GameData.updDisp |= (1 << DispConst.DISP_PLAYER_NUM)
                            GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = GameData.credits
                            GameData.updDisp |= (1 << DispConst.DISP_CREDIT_BALL_NUM)
                            pygame.mixer.music.stop()
                            GameData.gameMode = GameData.States.ATTRACT
                elif (event.key >= pygame.K_0) and (event.key <= pygame.K_9):
                    keyPress = event.key - pygame.K_0
        if keyPress != Pygame_Data.NO_KEY_PRESS:
            #keypress processing here
            if Pygame_Data.inpMode == Pygame_Data.INPMODE_SOUND:
                dispIntf.playSound(keyPress)
            elif Pygame_Data.inpMode == Pygame_Data.INPMODE_LIGHTS:
                dispIntf.updateFeatureLight(keyPress, DispConst.LGHT_TOGGLE)
            if GameData.gameMode == GameData.States.NORMAL_PLAY:
                GameData.score[GameData.currPlayer] += GameData.GameConst.SCORE_INC[keyPress]
                GameData.currDisp[GameData.currPlayer + DispConst.DISP_PLAYER1] = GameData.score[GameData.currPlayer]
                GameData.updDisp |= (1 << (GameData.currPlayer + DispConst.DISP_PLAYER1))
            keyPress = Pygame_Data.NO_KEY_PRESS
        return done

    ## Update pygame displays
    #
    #  Call the appropriate update display interface to update displays
    #  that have changed.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Update_Displays(self):
        if (Pygame_Data.prevBgndImage != GameData.bgndImage): 
            dispIntf.updateBgnd(GameData.bgndImage)
            Pygame_Data.prevBgndImage = GameData.bgndImage
            
        if (Pygame_Data.prevPlyrNum != GameData.currPlayer):
            if (GameData.currPlayer != DispConst.DISP_BLANK):
                GameData.currDisp[DispConst.DISP_PLAYER_NUM] = GameData.currPlayer + 1
            else:
                GameData.currDisp[DispConst.DISP_PLAYER_NUM] = DispConst.DISP_BLANK
            GameData.updDisp |= (1 << DispConst.DISP_PLAYER_NUM)
            Pygame_Data.prevPlyrNum = GameData.currPlayer
        if (Pygame_Data.prevCreditBallNum != GameData.creditBallNum):
            if (GameData.creditBallNum != DispConst.DISP_BLANK):
                GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = GameData.creditBallNum
            else:
                GameData.currDisp[DispConst.DISP_CREDIT_BALL_NUM] = DispConst.DISP_BLANK
            GameData.updDisp |= (1 << DispConst.DISP_CREDIT_BALL_NUM)
            Pygame_Data.prevCreditBallNum = GameData.creditBallNum
        for index in xrange(GameData.GameConst.MAX_NUM_PLYRS):
            if (Pygame_Data.prevScore[index] != GameData.score[index]):
                if (GameData.score[index] != DispConst.DISP_BLANK):
                    GameData.currDisp[DispConst.DISP_PLAYER1 + index] = GameData.score[index]
                else:
                    GameData.currDisp[DispConst.DISP_PLAYER1 + index] = DispConst.DISP_BLANK
                GameData.updDisp |= (1 << (DispConst.DISP_PLAYER1 + index))
                Pygame_Data.prevScore[index] = GameData.score[index]

    ## Update background music
    #
    #  See if the background music bitfield has changed.  If so,
    #  turn on/off the channels.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def Update_Bgnd_Music(self):
        if GameData.bgndSound != GameData.prevBgndSound:
            if GameData.bgndSound == 0xffffffff:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.load(GameData.rulesDir + "/" + GameData.BgndMusic.BGND_MUSIC_FILES[GameData.bgndSound])
                pygame.mixer.music.play(-1)
            GameData.prevBgndSound = GameData.bgndSound
            
