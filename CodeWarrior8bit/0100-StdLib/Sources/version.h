/*
 *===============================================================================
 *
 *                          HHHHH            HHHHH
 *                           HHH     SSSS     HHH
 *                           HHH   SSSSSSSS   HHH 
 *                           HHH  SSS    SSS  HHH       Hugh Spahr
 *                           HHH SSS      SSS HHH       Utilities
 *                           HHH  SSS         HHH
 *                           HHH    SSSS      HHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHH         SSS  HHH
 *                           HHH SSS      SSS HHH
 *                           HHH  SSS    SSS  HHH
 *                           HHH   SSSSSSSS   HHH
 *                           HHH     SSSS     HHH
 *                          HHHHH            HHHHH
 *
 * @file:   version.h
 * @author: Hugh Spahr
 * @date:   4/22/2008
 *
 * @note:    Copyright© 2008, Hugh Spahr
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *===============================================================================
 */
/**
 * The version file keeps the current version of the software.  These defines
 *  are used to fill out the APP_START_T found at the end of interrupt.h.
 *
 *===============================================================================
 */
#ifndef VERSION_H
#define VERSION_H

#define MAJ_VERSION 0
#define MIN_VERSION 0
#define SUB_VERSION 5

const char vers_stdlVersion[10] = {
   'v', (char)((MAJ_VERSION/10) + 0x30), (char)(MAJ_VERSION - ((MAJ_VERSION/10)*10) + 0x30),
   '.', (char)((MIN_VERSION/10) + 0x30), (char)(MIN_VERSION - ((MIN_VERSION/10)*10) + 0x30),
   '.', (char)((SUB_VERSION/10) + 0x30), (char)(SUB_VERSION - ((SUB_VERSION/10)*10) + 0x30),
   0x00 };
   
#endif
