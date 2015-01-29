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
# @file    gameConst.py
# @author  User Changed
# @date    01/28/2015
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief This is the game constants file.  It includes sound files, general illumination
# locations, and feature light locations, and string names for the debug window.

#===============================================================================

## Game constant class.
#  Contains the configuration of the pinball rules such as balls/game, num players,
#  feature light/GI light locations if the display is used to backlight a translight.
#  It also gives score display positions.
class GameConst:

    ## Number of balls per game
    BALLS_PER_GAME = 3
    
    ## Maximum number of players per game
    MAX_NUM_PLYRS = 4
    
    ## Display resolution
    DISPLAY_RESOLUTION = [1280, 1024]
    
    ## Radius of feature and GI lights
    LGHT_RADIUS = 20
    
    ## Location of feature lights
    # Located using actual screen x,y coordinates.  Auto scaled in simulation.
    # Only used if backglass is in front of monitor
    FEATURE_LGHT_POS = []       #Ex:  [[200, 300], [300,300], [400,300]]
    
    ## Location of general illumination lights
    # Located using actual screen x,y coordinates.  Auto scaled in simulation.
    # Only used if backglass is in front of monitor
    GI_LGHT_POS = []            #Ex: [[200,100], [300,200], [400,100]]
    
    ## Location of score displays/player num/ball num displays
    # Located using actual screen x,y coordinates for center of display.
    # Auto scaled in simulation.  First entry is playerNum, second entry
    # is BallNum/Credits, third entry is player 1 score, fourth entry is
    # player 2 score, etc. 
    SCORE_DISP_POS = [[683,653], [683,730],
        [304,653], [1064,653], [304,730], [1064,730]]   #Player score positions
    
    ## Height of score displays
    SCORE_HEIGHT = 77
    
