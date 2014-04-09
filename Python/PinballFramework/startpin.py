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
# @file:   startPin.py
# @author: Hugh Spahr
# @date:   1/15/2014
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
# Start the pin
#
#===============================================================================
vers = '00.00.02'

import pygame
from sys import exit
import sys
import dispConstIntf
import dispIntf
import time
import gameData
from commThread import CommThread
from rulesData import RulesData
from tkinterThread import TkinterThread

def main(argv=None):
    #input mode
    INPMODE_INPUT = 0
    INPMODE_SOUND = 1
    INPMODE_LIGHTS = 2

    end = False
    simWidth = 1920
    comPort = ""
    inpMode = INPMODE_INPUT
    debug = False

    actWidth = 0
    fullScreen = False
    if argv is None:
        argv = sys.argv
    for arg in argv:
        if arg.startswith('-simWidth='):
            simWidth = int(arg[10:])
        elif arg.startswith('-actualWidth='):
            actWidth = int(arg[13:])
        elif arg.startswith('-fullscr'):
            fullScreen = True
        elif arg.startswith('-port='):
            comPort = arg[6:]
        elif arg.startswith('-debug'):
            debug = True
        elif arg.startswith('-?'):
            print "python startPin.py [OPTIONS]"
            print "    -?                 Options Help"
            print "    -simWidth=         Width of simulation screen in pixels (assumes HD format)"
            print "    -actualWidth=      Width of final screen in pixels (assumes HD format)"
            print "                       Used for scaling.  If not set, assume simWidth is final"
            print "    -fullscr           Full screen mode"
            print "    -port=             COM port number (ex. COM1)"
            end = True
    if end:
        return 0
    
    #Set actual width if not entered
    if (actWidth < simWidth):
        actWidth = simWidth
    error = dispIntf.initDisp(simWidth, actWidth, fullScreen)
    if error: exit()
    dispIntf.startDisp()
    
    #Initialize the COMMs to the hardware
    commThread = CommThread()
    commThread.init(comPort)
    commThread.start()
    
    #HRS:  Debug
    if debug:
        tkinterThread = TkinterThread()
        tkinterThread.init()
        tkinterThread.start()
    
    NO_KEY_PRESS = '\xff'
    keyPress = NO_KEY_PRESS
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_i:
                    inpMode = INPMODE_INPUT
                    print "Input mode"
                elif event.key == pygame.K_s:
                    inpMode = INPMODE_SOUND
                    print "Sound mode"
                elif event.key == pygame.K_l:
                    inpMode = INPMODE_LIGHTS
                    print "Light mode"
                elif event.key == pygame.K_c:
                    gameData.numCredits += 1
                    if (gameData.gameMode == gameData.GAME_ATTRACT):
                        dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, gameData.numCredits, False)
                elif event.key == pygame.K_g:
                    #Check if starting a game
                    if (gameData.gameMode == gameData.GAME_ATTRACT) and (gameData.numCredits > 0):
                        gameData.numCredits -= 1
                        gameData.gameMode = gameData.GAME_PLAYING
                        gameData.numPlayers = 1
                        gameData.currBall = 0
                        gameData.currPlayer = 0
                        gameData.score[0] = 0
                      
                        #Set up player 1 score
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER1, gameData.score[0], False)
                      
                        #Clear player 2, 3, 4 scores
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER2, 0, True)
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER3, 0, True)
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER4, 0, True)
    
                        #Set player number, ball number
                        dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, gameData.currPlayer + 1, False)
                        dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, 1, False)
                      
                        #Play background music
                        pygame.mixer.music.load("sounds/bgndtrack.mp3")
                        pygame.mixer.music.play(-1)
                    #Check if another player is being added  
                    elif (gameData.gameMode == gameData.GAME_PLAYING) and (gameData.numCredits > 0):
                        #Only allow adding players if during first ball
                        if (gameData.currBall < 1) and (gameData.numPlayers < 4):
                            gameData.numCredits -= 1
                            gameData.score[gameData.numPlayers] = 0
                            dispIntf.updateDisp(gameData.numPlayers, gameData.score[gameData.numPlayers], False)
                            gameData.numPlayers += 1
                elif event.key == pygame.K_d:
                    #Drain the current ball
                    if (gameData.gameMode == gameData.GAME_PLAYING):
                        #If more players, increment currPlayers
                        if (gameData.currPlayer + 1 < gameData.numPlayers):
                            gameData.currPlayer += 1
                            dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, gameData.currPlayer + 1, False)
                        elif (gameData.currBall + 1 < RulesData.BALLS_PER_GAME):
                            currPlayer = 0
                            dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, currPlayer + 1, False)
                            gameData.currBall += 1
                            dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, gameData.currBall + 1, False)
                        else:
                            #Game over, blank player number
                            dispIntf.updateDisp(dispConstIntf.DISP_PLAYER_NUM, 0, True)
                            dispIntf.updateDisp(dispConstIntf.DISP_CREDIT_BALL_NUM, gameData.numCredits, False)
                            pygame.mixer.music.stop()
                            gameData.gameMode = gameData.GAME_ATTRACT
                elif (event.key >= pygame.K_0) and (event.key <= pygame.K_9):
                    keyPress = event.key - pygame.K_0
        if keyPress != NO_KEY_PRESS:
            #keypress processing here
            if inpMode == INPMODE_SOUND:
                dispIntf.playSound(keyPress)
            elif inpMode == INPMODE_LIGHTS:
                dispIntf.updateFeatureLight(keyPress, dispConstIntf.LGHT_TOGGLE)
            if gameData.gameMode == gameData.GAME_PLAYING:
                gameData.score[currPlayer] += RulesData.SCORE_INC[keyPress]
                dispIntf.updateDisp(currPlayer, gameData.score[currPlayer], False)
            keyPress = NO_KEY_PRESS
        time.sleep(.01)    
    commThread.commExit()
    if debug:
        tkinterThread.tkinterExit()

if __name__ == "__main__":
    sys.exit(main())