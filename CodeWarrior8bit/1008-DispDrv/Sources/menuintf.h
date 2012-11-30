/*
 *===============================================================================
 *
 *
 *                          8888         999999
 *                        88888888     999999999
 *                       888    888   999    9999
 *                      888      888 999      999
 *                       888    888   999    9999
 *                        88888888     9999999999
 *     NNNNN      NNNNN    888888       999999999     TTT     HHHHH
 *      NNN        NNN    88888888        999 999     TTT      HHH
 *      NNNN       NNN   888    888           999     TTT      HHH
 *      NNNNN      NNN  888      888          999  TTTTTTTTT   HHH
 *      NNNNNN     NNN   888    888           999 TTTTTTTTTTT  HHH
 *      NNNNNNN    NNN    88888888            999     TTT      HHH
 *      NNNNNNNN   NNN      8888              999     TTT      HHH
 *      NNN  NNNN  NNN                                TTT      HHH
 *      NNN   NNNN NNN      OOOOOO     RRR RRRRR      TTT      HHH HHHHH
 *      NNN    NNNNNNN     OOOOOOOO    RRRRRRRRRR     TTT      HHHHHHHHHH
 *      NNN     NNNNNN    OOO    OOO   RRRR    RRR    TTT      HHHH    HHH
 *      NNN      NNNNN   OOO      OOO  RRR            TTT      HHH     HHH
 *      NNN       NNNN    OOO    OOO   RRR            TTT      HHH     HHH
 *      NNN        NNN     OOOOOOOO    RRR            TTT      HHH     HHH
 *     NNNNN      NNNNN      OOOO      RRR           TTTTT    HHHHH   HHHHH
 *
 * @file:   menuintf.h
 * @author: Hugh Spahr
 * @date:   12/10/2010
 *
 * @note:   89 North, Inc.   Copyright© 2010
 *          1 Mill St., Unit 285
 *          Burlington, VT  05401
 *
 *===============================================================================
 */
/**
 * Menu Interface file for hand controller
 *
 *===============================================================================
 */

#ifndef MENUINTF_H
#define MENUINTF_H

typedef enum
{
  MENUI_NO_PROCESSING       = 0x00,
  MENUI_SWITCH_MODES        = 0x01,
  MENUI_PROCESS_BUTTS       = 0x02,
  MAX_NUM_MENU_CMD
} MENUI_CMD_E;

/* Prototypes */
void lcdmenu_processing(
  MENUI_CMD_E               cmd);
  
#endif
