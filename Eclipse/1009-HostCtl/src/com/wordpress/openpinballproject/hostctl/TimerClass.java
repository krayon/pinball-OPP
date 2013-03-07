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
 * @file:   TimerClass.java
 * @author: Hugh Spahr
 * @date:   3/05/2013
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
 * Timer class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class TimerClass
{
   private static final int            MAX_NUM_TIMERS          = 64;
   
   private static final int            TMR_NEED_OPEN_CURLY     = 1;
   private static final int            TMR_PROC_TMR_NAME       = 2;
   private static final int            TMR_PROC_TIMEOUT_VAL    = 3;
   private static final int            TMR_DONE                = 4;
   private static final int            TMR_ERROR               = 5;

   private int                         state = TMR_NEED_OPEN_CURLY;
   private int                         numTmrs = 0;
   private String                      currName;
   private int[]                       timeoutArr;
   
   /*
    * ===============================================================================
    * 
    * Name: TimerClass
    * 
    * ===============================================================================
    */
   /**
    * Timer class
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
   public TimerClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword, second should be num cards  */
      timeoutArr = new int[MAX_NUM_TIMERS];
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end VarClass */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create timers
    * 
    * Take tokens and add entries to create timers.  This class uses fields
    * to configure the timeout, and name for later lookups.
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
            case TMR_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = TMR_PROC_TMR_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("TIMERS: needs curly parenthesis.");
                  GlobInfo.parseRules.parseFail = true;
                  state = TMR_ERROR;
               }
               break;
            }
            case TMR_PROC_TMR_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = TMR_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = TMR_PROC_TIMEOUT_VAL;
               }
               break;
            }
            case TMR_PROC_TIMEOUT_VAL:
            {
               Integer                          tstKey;
               int                              initVal;
               
               try
               {
                  initVal = Integer.parseInt(tokens[currToken]);
                  
                  /* Check if this is a duplicate value */
                  tstKey = ParseRules.hmSymbol.get(currName);
                  if (tstKey == null)
                  {
                      ParseRules.hmSymbol.put(currName,
                         ParseRules.SYMB_TIMER | numTmrs);
                      if (numTmrs < MAX_NUM_TIMERS)
                      {
                         timeoutArr[numTmrs] = initVal;
                         numTmrs++;
                         state = TMR_PROC_TMR_NAME;
                      }
                      else
                      {
                         GlobInfo.hostCtl.printMsg("TIMERS: Too many timers.");
                         GlobInfo.parseRules.parseFail = true;
                         state = TMR_ERROR;
                      }
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("TIMERS: Duplicate names.");
                     GlobInfo.parseRules.parseFail = true;
                     state = TMR_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("TIMERS: Illegal timeout value.");
                  GlobInfo.parseRules.parseFail = true;
                  state = TMR_ERROR;
               }
               break;
            }
            case TMR_DONE:
            {
               GlobInfo.hostCtl.printMsg("TIMERS: Extra info.");
               GlobInfo.parseRules.parseFail = true;
               state = TMR_ERROR;
               break;
            }
            case TMR_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if (state == TMR_DONE)
      {
         int[]                         tmpArr = new int[numTmrs];
         int                           index;
         
         /* Save some memory by allocating only the space needed for init array */
         for (index = 0; index < numTmrs; index++)
         {
            tmpArr[index] = timeoutArr[index];
         }
         timeoutArr = tmpArr;
      }
      if ((state == TMR_ERROR) || (state == TMR_DONE))
      {
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */

} /* End TimerClass */
