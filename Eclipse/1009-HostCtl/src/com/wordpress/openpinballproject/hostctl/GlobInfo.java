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
 * @file:   GlobInfo.java
 * @author: Hugh Spahr
 * @date:   1/09/2013
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
 * This class contains the global info shared between objects.
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

import javax.swing.JLabel;

public class GlobInfo
{
   private static final int      MAX_NUM_INP_CARDS          = 8;
   private static final int      MAX_NUM_SOL_CARDS          = 8;
   private static final int      MAX_NUM_LED_CARDS          = 8;
   public static final int       NUM_VIDEO_CLIPS            = 2;
   
   public static int             chngFlag = 0;
   public static boolean         commGood = false;
   public static boolean         debug = false;
   public static int             numInpCards = 0;
   public static int[]           inpCardAddr = new int[MAX_NUM_INP_CARDS];
   public static int[]           inpCardData = new int[MAX_NUM_INP_CARDS];
   public static int[]           inpCardSerNum = new int[MAX_NUM_INP_CARDS];
   public static int[]           inpCardProdId = new int[MAX_NUM_INP_CARDS];
   public static int[]           inpCardVers = new int[MAX_NUM_INP_CARDS];
   public static JLabel[]        inpCardDbgLbl = new JLabel[MAX_NUM_INP_CARDS];
   public static int             numSolCards = 0;
   public static int[]           solCardAddr = new int[MAX_NUM_SOL_CARDS];
   public static int[]           solCardData = new int[MAX_NUM_SOL_CARDS];
   public static int[]           solCardSerNum = new int[MAX_NUM_SOL_CARDS];
   public static int[]           solCardProdId = new int[MAX_NUM_SOL_CARDS];
   public static int[]           solCardVers = new int[MAX_NUM_SOL_CARDS];
   public static JLabel[]        solCardDbgLbl = new JLabel[MAX_NUM_SOL_CARDS];
   public static int             numLedCards = 0;
   public static int[]           ledCardData = new int[MAX_NUM_LED_CARDS];
   public static JLabel[]        ledCardDbgLbl = new JLabel[MAX_NUM_LED_CARDS];
   public static int             tick = 20;
  
   public static HostCtl         hostCtl = null;
   public static SerIntf         serIntf = null;
   public static VideoServ       videoServ = null;
   public static ConsoleFrm      consFrm = null;
   public static ParseRules      parseRules = null;
   public static ParsePChain     parsePChain = null;
   
   public static SolenoidClass   solClass = null;
   public static InpCardClass    inpCardClass = null;
   public static LedClass        ledClass = null;
   public static VarClass        varClass = null;
   public static SoundClass      sndClass = null;
   public static VideoClass      vidClass = null;
   public static IndxVarClass    indxVarClass = null;
   public static TimerClass      tmrClass = null;
} /* End GlobInfo */
