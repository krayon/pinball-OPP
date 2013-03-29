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
 * @file:   ModeClass.java
 * @author: Hugh Spahr
 * @date:   3/29/2013
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
 * Mode class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class ModeClass
{
   private int                         numModes = 0;

   /*
    * ===============================================================================
    * 
    * Name: ModeClass
    * 
    * ===============================================================================
    */
   /**
    * Mode class
    * 
    * Currently no processing
    * 
    * @param   None 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public ModeClass()
   {
   } /* end ModeClass */

   /*
    * ===============================================================================
    * 
    * Name: Create Mode
    * 
    * ===============================================================================
    */
   /**
    * Create a Mode
    * 
    * Check if the mode currently exists.  If so, do nothing.  If not, allocate it
    * into the symbol array.
    * 
    * @param   name     - name of the mode to be created 
    * @return  modeNum  - mode number
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public int CreateMode(
      String                           name)
   {
      int                              num = 0;
      Integer                          tstKey;
      int                              type;
      
      tstKey = ParseRules.hmSymbol.get(name);
      if (tstKey == null)
      {
         /* The mode symbol does not exist */ 
         ParseRules.hmSymbol.put(name, ParseRules.SYMB_MODE | numModes);
         num = numModes;
         numModes++;
      }
      else
      {
         /* Verify that the symbol isn't already used. */
         type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
         if (type != ParseRules.SYMB_MODE)
         {
            GlobInfo.hostCtl.printMsg("MODE: Symbol " + name + " used as mode and something else.");
            GlobInfo.parseFail = true;
         }
         else
         {
            num = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
         }
      }
      return (num);
   } /* end CreateMode */
} /* End ModeClass */
