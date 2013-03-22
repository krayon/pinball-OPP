/*
 *===============================================================================
 *
 *                         OOOO
 *                       OOOOOOOO
 *      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP    OOO    OOO    PPP
 *               PPP     OOOOOOOO     PPP
 *              PPPPP      OOOO      PPPPP
 *
 * @file:   ProcObj.java
 * @author: Hugh Spahr
 * @date:   3/01/2013
 *
 * @note:   Open Pinball Project
 *          Copyright© 2013, Hugh Spahr
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
 * Processing object
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class ProcObj
{
   public static final int             TYPE_VARIABLE              = 0;
   public static final int             TYPE_CONSTANT              = 1000;
   public static final int             TYPE_HW_INPUT              = 2000;
   public static final int             TYPE_PREDEF_VAR            = 3000;
   public static final int             TYPE_FUNC                  = 4000;
   public static final int             TYPE_PROCOBJ_RSLT          = 5000;
   public static final int             TYPE_UNUSED                = 6000;
   
   public static final int             OP_ZERO                    = 0;
   public static final int             OP_NONZERO                 = 1;
   public static final int             OP_PREDEF_FUNC             = 2;
   public static final int             OP_SET_VAL                 = 3;
   public static final int             OP_LOGICAL_AND             = 4;
   public static final int             OP_BITWISE_AND             = 5;
   public static final int             OP_LOGICAL_OR              = 6;
   public static final int             OP_BITWISE_OR              = 7;
   public static final int             OP_BITWISE_INVERT          = 8;
   public static final int             OP_PLUS_EQUALS             = 9;
   public static final int             OP_EQUALS                  = 10;
   public static final int             OP_NOT_EQUALS              = 11;
   public static final int             OP_OR_EQUALS               = 12;
   public static final int             OP_AND_EQUALS              = 13;
   public static final int             OP_GREATER_THAN            = 14;
   public static final int             OP_LESS_THAN               = 15;
   public static final int             OP_GREATER_OR_EQUAL        = 16;
   public static final int             OP_LESS_OR_EQUAL           = 17;
   public static final int             OP_INCREMENT               = 18;
   public static final int             OP_DECREMENT               = 19;
   public static final int             OP_START_CHAIN             = 20;
   public static final int             OP_END_CHAIN               = 21;

   public static final int             PREDEF_DISABLE_SOLENOIDS   = 0;
   public static final int             PREDEF_LED_ON              = 1;
   public static final int             PREDEF_KICK                = 2;
   public static final int             PREDEF_START_TIMER         = 3;
   public static final int             PREDEF_ENABLE_SOLENOIDS    = 4;
   public static final int             PREDEF_EXPIRED_TIMER       = 5;
   public static final int             PREDEF_TEXT                = 6;
   public static final int             PREDEF_SOUND               = 7;
   public static final int             PREDEF_WAIT                = 8;
   public static final int             PREDEF_LED_ROT_LEFT        = 9;
   public static final int             PREDEF_LED_ROT_RIGHT       = 10;
   public static final int             PREDEF_LED_OFF             = 11;
   public static final int             PREDEF_LED_BLINK_100       = 12;
   public static final int             PREDEF_LED_BLINK_500       = 13;

   public static final int             PDVAR_MODE                 = 0;
   public static final int             PDVAR_EXPIRED_TIMERS       = 1;
   public static final int             PDVAR_SOL_INPUTS           = 2;
   public static final int             PDVAR_CARD_INPUTS          = 3;
   
   public int                          oper;
   public int                          paramA;
   public int                          typeA;
   public int                          paramB;
   public int                          typeB;
   public int                          dest;
   public int                          typeDest;
   public int                          trueProcObj;
   public int                          falseProcObj;
} /* End ProcObj */
