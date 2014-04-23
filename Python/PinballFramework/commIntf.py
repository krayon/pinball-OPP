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
# @file:   commIntf.py
# @author: Hugh Spahr
# @date:   1/16/2014
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
# This is the communication interface file that is used to send commands and
# receive responses from the hardware
#
#===============================================================================

vers = '00.00.02'

import rs232Intf
import errIntf

def updateSol(commThread, brd, sol, params):
    if brd > commThread.numSolBrd:
        return errIntf.BAD_SOL_BRD_NUM
    if sol > rs232Intf.NUM_SOL_PER_BRD:
        return errIntf.BAD_SOL_NUM
    if len(params) != rs232Intf.CFG_BYTES_PER_SOL:
        return errIntf.BAD_PARAM_BYTES
    for loop in range(rs232Intf.CFG_BYTES_PER_SOL):
        commThread.solBrdCfg[brd][(rs232Intf.CFG_BYTES_PER_SOL * sol) + loop] = params[loop]
    return errIntf.CMD_OK

def sendSolCfg(commThread, brd):
    if brd > commThread.numSolBrd:
        return errIntf.BAD_SOL_BRD_NUM
    commThread.updateSolBrdCfg |= (1 << brd)
    return errIntf.CMD_OK

def updateInp(commThread, brd, inp, cfg):
    if brd > commThread.numInpBrd:
        return errIntf.BAD_INP_BRD_NUM
    if inp > rs232Intf.NUM_INP_PER_BRD:
        return errIntf.BAD_INP_NUM
    commThread.inpBrdCfg[brd][rs232Intf.CFG_BYTES_PER_INP * inp] = cfg
    return errIntf.CMD_OK

def sendInpCfg(commThread, brd):
    if brd > commThread.numInpBrd:
        return errIntf.BAD_INP_BRD_NUM
    commThread.updateInpBrdCfg |= (1 << brd)
    return errIntf.CMD_OK
