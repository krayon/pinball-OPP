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
#define SUB_VERSION 7

const char vers_programVersion[10] = {
   'v', (char)((MAJ_VERSION/10) + 0x30), (char)(MAJ_VERSION - ((MAJ_VERSION/10)*10) + 0x30),
   '.', (char)((MIN_VERSION/10) + 0x30), (char)(MIN_VERSION - ((MIN_VERSION/10)*10) + 0x30),
   '.', (char)((SUB_VERSION/10) + 0x30), (char)(SUB_VERSION - ((SUB_VERSION/10)*10) + 0x30),
   0x00 };
   
#endif
