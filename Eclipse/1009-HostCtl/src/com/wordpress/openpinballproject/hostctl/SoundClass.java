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
 * @file:   SoundClass.java
 * @author: Hugh Spahr
 * @date:   2/11/2013
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
 * Sound class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

import java.util.ArrayList;

public class SoundClass
{
   private static final int            SND_NEED_OPEN_CURLY     = 1;
   private static final int            SND_PROC_SND_NAME       = 2;
   private static final int            SND_PROC_LOC            = 3;
   private static final int            SND_DONE                = 4;
   private static final int            SND_ERROR               = 5;

   private ArrayList<String>           sndArrLst = new ArrayList<String>(); 
   private int                         state = SND_NEED_OPEN_CURLY;
   private String                      currName;
   private int                         currIndex = 0;
   
   /*
    * ===============================================================================
    * 
    * Name: SoundClass
    * 
    * ===============================================================================
    */
   /**
    * Sound class
    * 
    * If more information is available call add entries to process it.
    * 
    * @param   tokens - fields to be processed 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public SoundClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword */
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end SoundClass */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create sounds
    * 
    * Take tokens and add entries to create variables  This class uses fields
    * for locations, and name each for later lookups.
    * 
    * @param   currToken - index of first token to be processed 
    * @param   tokens - fields to be processed 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public boolean addEntries(
      int                              currToken,
      String[]                         tokens)
   {
      while (currToken < tokens.length)
      {
         switch (state)
         {
            case SND_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = SND_PROC_SND_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("SOUND_CLIPS: needs curly parenthesis.");
                  GlobInfo.parseFail = true;
                  state = SND_ERROR;
               }
               break;
            }
            case SND_PROC_SND_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = SND_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = SND_PROC_LOC;
               }
               break;
            }
            case SND_PROC_LOC:
            {
               String                           locPath;
               Integer                          tstKey;

               locPath = tokens[currToken];
               
               /* Check if this is a duplicate value */
               tstKey = ParseRules.hmSymbol.get(currName);
               if (tstKey == null)
               {
                  /* Add the location to the array list */
                  sndArrLst.add(currIndex, locPath);
                  ParseRules.hmSymbol.put(currName,
                      ParseRules.SYMB_SND | currIndex);
                  currIndex++;
                  state = SND_PROC_SND_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("SOUND_CLIPS: Duplicate input names.");
                  GlobInfo.parseFail = true;
                  state = SND_ERROR;
               }
               break;
            }
            case SND_DONE:
            {
               GlobInfo.hostCtl.printMsg("SOUND_CLIPS: Extra info.");
               GlobInfo.parseFail = true;
               state = SND_ERROR;
               break;
            }
            case SND_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if ((state == SND_ERROR) || (state == SND_DONE))
      {
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
} /* End SoundClass */
