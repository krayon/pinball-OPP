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
# @file    ledChains.py
# @author  AutoGenerated
# @date    11/20/2016
#
# @note    Open Pinball Project
# @note    Copyright 2015, Hugh Spahr
#
# @brief These are the LED chains.  It includes chains to automatically change
#    LEDs depending on the state.

#===============================================================================

from ledBitNames import LedBitNames

## LED chains class.
#
#  Contains all the LED chains that are specific this this set of pinball rules.
class LedChains():
    def __init__(self):
        pass

    # LED chain commands
    WAIT = 0
    REPEAT = 1
    END_CHAIN = 2

    MASK_OFFSET = 0
    CHAIN_OFFSET = 1

    # Offsets into sublist
    CH_LED_BITS_OFFSET = 0
    CH_CMD_OFFSET = 1
    PARAM_OFFSET = 2

    ## LED Chain LedCh_Attract
    #    - First entry is LED mask
    #    - Next groups have a bitfield of LEDs to change and command
    LedCh_Attract = [
        # LED0W0_ALL_BITS_MSK | LED0W1_ALL_BITS_MSK, LED1W0_ALL_BITS_MSK, LED2W0_ALL_BITS_MSK | LED2W1_ALL_BITS_MSK, LED3W0_ALL_BITS_MSK
        [ 0x0000ffff, 0x000000ff, 0x0000ffff, 0x000000ff ],
        [ # 0, 0, 0, LED_SHOOT_AGAIN
          [ [ 0, 0, 0, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE, LED_SHOOT_AGAIN
          [ [ 0, 0, 0x00000080, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT, LED_SHOOT_AGAIN
          [ [ 0, 0, 0x000010c0, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL, LED_SHOOT_AGAIN
          [ [ 0, 0, 0x000018e0, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT, LED_SHOOT_AGAIN
          [ [ 0, 0, 0x00001cf0, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL, LED_SHOOT_AGAIN
          [ [ 0, 0, 0x00001ef8, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN
          [ [ 0, 0, 0x00001ffc, 0x00000001 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE
          [ [ 0, 0, 0x00001ffc, 0x00000041 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY
          [ [ 0, 0, 0x00001ffc, 0x00000061 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF
          [ [ 0, 0, 0x00001ffc, 0x00000071 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_1, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000040, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_2, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000020, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_3, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000010, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_4, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000008, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_5, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000004, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_6, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000002, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000001, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_6, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000002, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_5, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000004, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_4, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000008, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_3, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000010, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_2, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000020, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_1, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x00000040, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # 0, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 500],
          # 0, 0, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0, 0x00001ffc, 0x00000079 ],  WAIT, 500],
          # 0, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 500],
          # LED_KO_DUEL, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x00000080, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000c0, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000d0, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000f0, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000f4, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000004fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000006fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000007fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT | LED_ROLL_LFT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000087fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT | LED_ROLL_LFT | LED_ROLL_CTR, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x0000c7fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT | LED_ROLL_LFT | LED_ROLL_CTR | LED_ROLL_RGHT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x0000e7fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT | LED_ROLL_LFT | LED_ROLL_CTR | LED_ROLL_RGHT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x0000e7fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 500],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT | LED_ROLL_LFT | LED_ROLL_CTR | LED_ROLL_RGHT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x0000e7fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 500],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x000000fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 100],
          # LED_KO_DUEL | LED_KO_PICK_JOB | LED_2X | LED_3X | LED_4X | LED_5X | LED_INLN_LFT | LED_INLN_CTR | LED_INLN_RGHT | LED_ROLL_LFT | LED_ROLL_CTR | LED_ROLL_RGHT, LED_DT_1 | LED_DT_2 | LED_DT_3 | LED_DT_4 | LED_DT_5 | LED_DT_6 | LED_DT_7, LED_MODE_SHARPE | LED_MODE_SNIPER | LED_MODE_TRKBNDT | LED_MODE_CHKHIDE | LED_MODE_KILLALL | LED_MODE_TRGTPRAC | LED_MODE_BARFGHT | LED_MODE_HUSTLEJIVE | LED_MODE_DUEL | LED_MODE_POSSE | LED_MODE_RIDEHELP, LED_SHOOT_AGAIN | LED_ROOKIE | LED_DEPUTY | LED_SHERIFF | LED_MARSHAL
          [ [ 0x0000e7fc, 0x0000007f, 0x00001ffc, 0x00000079 ],  WAIT, 500],
          # 0, 0, 0, 0
          [ [ 0, 0, 0, 0 ],  WAIT, 500],
          # LED0W0_ALL_BITS_MSK | LED0W1_ALL_BITS_MSK, LED1W0_ALL_BITS_MSK, LED2W0_ALL_BITS_MSK | LED2W1_ALL_BITS_MSK, LED3W0_ALL_BITS_MSK
          [ [ 0x0000ffff, 0x000000ff, 0x0000ffff, 0x000000ff ],  WAIT, 500],
          # 0, 0, 0, 0
          [ [ 0, 0, 0, 0 ],  WAIT, 500],
          # LED0W0_ALL_BITS_MSK | LED0W1_ALL_BITS_MSK, LED1W0_ALL_BITS_MSK, LED2W0_ALL_BITS_MSK | LED2W1_ALL_BITS_MSK, LED3W0_ALL_BITS_MSK
          [ [ 0x0000ffff, 0x000000ff, 0x0000ffff, 0x000000ff ],  WAIT, 500],
          # 0, 0, 0, 0
          [ [ 0, 0, 0, 0 ],  WAIT, 500],
          # LED0W0_ALL_BITS_MSK | LED0W1_ALL_BITS_MSK, LED1W0_ALL_BITS_MSK, LED2W0_ALL_BITS_MSK | LED2W1_ALL_BITS_MSK, LED3W0_ALL_BITS_MSK
          [ [ 0x0000ffff, 0x000000ff, 0x0000ffff, 0x000000ff ],  WAIT, 500],
          # 0, 0, 0, 0
          [ [ 0, 0, 0, 0 ],  WAIT, 500],
          # 0, 0, 0, 0
          [ [ 0, 0, 0, 0 ], REPEAT, 0] ] ]

    ## LED Chain LedCh_Tilt
    #    - First entry is LED mask
    #    - Next groups have a bitfield of LEDs to change and command
    LedCh_Tilt = [
        # 0, 0, 0, LED_SHOOT_AGAIN
        [ 0, 0, 0, 0x00000001 ],
        [ # 0, 0, 0, 0
          [ [ 0, 0, 0, 0 ], END_CHAIN, 0] ] ]

