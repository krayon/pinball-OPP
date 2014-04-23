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
# @file:   pygameFunc.py
# @author: Hugh Spahr
# @date:   4/22/2014
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
# Pygame functions
#
#===============================================================================
vers = '00.00.01'

import pygame
from gameData import GameData
import dispConstIntf
import dispIntf
from rulesData import RulesData
from rulesData import State

class Pygame_Data():
    #input mode
    INPMODE_INPUT = 0
    INPMODE_SOUND = 1
    INPMODE_LIGHTS = 2
    
    NO_KEY_PRESS = '\xff'

    inpMode = INPMODE_INPUT
    
    def __init__(self):
        self.inpMode = self.INPMODE_INPUT
        
    def Proc_Pygame_Events(self):
        keyPress = self.NO_KEY_PRESS
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_i:
                    self.inpMode = self.INPMODE_INPUT
                    print "Input mode"
                elif event.key == pygame.K_s:
                    self.inpMode = self.INPMODE_SOUND
                    print "Sound mode"
                elif event.key == pygame.K_l:
                    self.inpMode = self.INPMODE_LIGHTS
                    print "Light mode"
                elif event.key == pygame.K_c:
                    GameData.credits += 1
                    if (GameData.gameMode == State.ATTRACT):
                        dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, GameData.credits, False)
                elif event.key == pygame.K_g:
                    #Check if starting a game
                    if (GameData.gameMode == State.ATTRACT) and (GameData.credits > 0):
                        GameData.credits -= 1
                        GameData.gameMode = State.NORMAL_PLAY
                        GameData.numPlayers = 1
                        GameData.currBall = 0
                        GameData.currPlayer = 0
                        GameData.score[0] = 0
                      
                        #Set up player 1 score
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER1, GameData.score[0], False)
                      
                        #Clear player 2, 3, 4 scores
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER2, 0, True)
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER3, 0, True)
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER4, 0, True)
    
                        #Set player number, ball number
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, GameData.currPlayer + 1, False)
                        dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, 1, False)
                      
                        #Play background music
                        pygame.mixer.music.load("sounds/bgndtrack.mp3")
                        pygame.mixer.music.play(-1)
                    #Check if another player is being added  
                    elif (GameData.gameMode == State.NORMAL_PLAY) and (GameData.credits > 0):
                        #Only allow adding players if during first ball
                        if (GameData.ballNum < 1) and (GameData.numPlayers < 4):
                            GameData.credits -= 1
                            GameData.score[GameData.numPlayers] = 0
                            dispIntf.updateDisp(GameData.numPlayers, GameData.score[GameData.numPlayers], False)
                            GameData.numPlayers += 1
                elif event.key == pygame.K_d:
                    #Drain the current ball
                    if (GameData.gameMode == State.NORMAL_PLAY):
                        #If more players, increment currPlayers
                        if (GameData.currPlayer + 1 < GameData.numPlayers):
                            GameData.currPlayer += 1
                            dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, GameData.currPlayer + 1, False)
                        elif (GameData.ballNum + 1 < RulesData.BALLS_PER_GAME):
                            GameData.currPlayer = 0
                            dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, GameData.currPlayer + 1, False)
                            GameData.ballNum += 1
                            dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, GameData.ballNum + 1, False)
                        else:
                            #Game over, blank player number
                            dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, 0, True)
                            dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, GameData.credits, False)
                            pygame.mixer.music.stop()
                            GameData.gameMode = State.ATTRACT
                elif (event.key >= pygame.K_0) and (event.key <= pygame.K_9):
                    keyPress = event.key - pygame.K_0
        if keyPress != self.NO_KEY_PRESS:
            #keypress processing here
            if self.inpMode == self.INPMODE_SOUND:
                dispIntf.playSound(keyPress)
            elif self.inpMode == self.INPMODE_LIGHTS:
                dispIntf.updateFeatureLight(keyPress, dispConstIntf.LGHT_TOGGLE)
            if GameData.gameMode == State.NORMAL_PLAY:
                GameData.score[GameData.currPlayer] += RulesData.SCORE_INC[keyPress]
                dispIntf.updateDisp(GameData.currPlayer, GameData.score[GameData.currPlayer], False)
            keyPress = self.NO_KEY_PRESS
        return done


