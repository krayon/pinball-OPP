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
 * @file:   VideoClass.java
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
 * Video class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

import java.util.ArrayList;

public class VideoClass
{
   private static final int            VID_NEED_OPEN_CURLY     = 1;
   private static final int            VID_PROC_VID_NAME       = 2;
   private static final int            VID_PROC_LOC            = 3;
   private static final int            VID_PROC_SCREEN         = 4;
   private static final int            VID_DONE                = 5;
   private static final int            VID_ERROR               = 6;

   private ArrayList<String>           bigVidArrLst = new ArrayList<String>(); 
   private ArrayList<String>           smallVidArrLst = new ArrayList<String>(); 
   private int                         state = VID_NEED_OPEN_CURLY;
   private String                      currName;
   private String                      locPath;
   private int                         bigVidIndex = 0;
   private int                         littleVidIndex = 0;
   
   /*
    * ===============================================================================
    * 
    * Name: VideoClass
    * 
    * ===============================================================================
    */
   /**
    * Video class
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
   public VideoClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword */
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end VideoClass */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create videos
    * 
    * Take tokens and add entries to create videos.  This class uses fields
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
            case VID_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = VID_PROC_VID_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("VIDEO_CLIPS: needs curly parenthesis.");
                  GlobInfo.parseFail = true;
                  state = VID_ERROR;
               }
               break;
            }
            case VID_PROC_VID_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = VID_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = VID_PROC_LOC;
               }
               break;
            }
            case VID_PROC_LOC:
            {
               locPath = tokens[currToken];
               state = VID_PROC_SCREEN;
               break;
            }
            case VID_PROC_SCREEN:
            {
               Integer                          tstKey;
               boolean                          addEntry = true;
               boolean                          mainScr = true;

               if (tokens[currToken].equals("MAIN_SCR"))
               {
                  mainScr = true;
               }
               else if (tokens[currToken].equals("SUB_SCR"))
               {
                  mainScr = false;
               }
               else
               {
                  addEntry = false;
                  GlobInfo.hostCtl.printMsg("VIDEO_CLIPS: Illegal screen name.");
                  GlobInfo.parseFail = true;
                  state = VID_ERROR;
               }
               if (addEntry)
               {
                  /* Check if this is a duplicate value */
                  tstKey = ParseRules.hmSymbol.get(currName);
                  if (tstKey == null)
                  {
                     /* Add the location to the array list */
                     if (mainScr)
                     {
                        bigVidArrLst.add(bigVidIndex, locPath);
                        ParseRules.hmSymbol.put(currName,
                           ParseRules.SYMB_BIG_VID | bigVidIndex);
                     	GlobInfo.fileConstClass.println("   public static final int             " +
                           String.format("%-27s= %2d;", currName.toUpperCase(), bigVidIndex));
                        bigVidIndex++;
                     }
                     else
                     {
                        smallVidArrLst.add(littleVidIndex, locPath);
                        ParseRules.hmSymbol.put(currName,
                           ParseRules.SYMB_LITTLE_VID | littleVidIndex);
                     	GlobInfo.fileConstClass.println("   public static final int             " +
                           String.format("%-27s= %2d;", currName.toUpperCase(), littleVidIndex));
                        littleVidIndex++;
                     }
                     state = VID_PROC_VID_NAME;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("VIDEO_CLIPS: Duplicate input names.");
                     GlobInfo.parseFail = true;
                     state = VID_ERROR;
                  }
               }
               break;
            }
            case VID_DONE:
            {
               GlobInfo.hostCtl.printMsg("VIDEO_CLIPS: Extra info.");
               GlobInfo.parseFail = true;
               state = VID_ERROR;
               break;
            }
            case VID_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if ((state == VID_ERROR) || (state == VID_DONE))
      {
      	GlobInfo.fileConstClass.println("");
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
} /* End VideoClass */
