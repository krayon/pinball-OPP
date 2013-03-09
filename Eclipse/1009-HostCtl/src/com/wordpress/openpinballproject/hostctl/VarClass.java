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
 * @file:   VarClass.java
 * @author: Hugh Spahr
 * @date:   2/09/2013
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
 * Variable class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class VarClass
{
   private static final int            MAX_NUM_VARS            = 4096;
   
   private static final int            VAR_NEED_OPEN_CURLY     = 1;
   private static final int            VAR_PROC_VAR_NAME       = 2;
   private static final int            VAR_PROC_INIT_VAL       = 3;
   private static final int            VAR_DONE                = 4;
   private static final int            VAR_ERROR               = 5;

   private int                         state = VAR_NEED_OPEN_CURLY;
   private int                         numVars = 0;
   private String                      currName;
   private int[]                       initVarArr;
   
   /*
    * ===============================================================================
    * 
    * Name: VarClass
    * 
    * ===============================================================================
    */
   /**
    * Variable class
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
   public VarClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword, second should be num cards  */
      initVarArr = new int[MAX_NUM_VARS];
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
    * Add entries to create variables
    * 
    * Take tokens and add entries to create variables  This class uses fields
    * to configure the variables, and name each for later lookups.
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
            case VAR_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = VAR_PROC_VAR_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("VARIABLES: needs curly parenthesis.");
                  GlobInfo.parseFail = true;
                  state = VAR_ERROR;
               }
               break;
            }
            case VAR_PROC_VAR_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = VAR_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = VAR_PROC_INIT_VAL;
               }
               break;
            }
            case VAR_PROC_INIT_VAL:
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
                         ParseRules.SYMB_VAR | ParseRules.allocInd);
                      if (numVars < MAX_NUM_VARS)
                      {
                         initVarArr[numVars] = initVal;
                         ParseRules.allocInd++;
                         numVars++;
                         state = VAR_PROC_VAR_NAME;
                      }
                      else
                      {
                         GlobInfo.hostCtl.printMsg("VARIABLES: Too many variable names.");
                         GlobInfo.parseFail = true;
                         state = VAR_ERROR;
                      }
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("VARIABLES: Duplicate input names.");
                     GlobInfo.parseFail = true;
                     state = VAR_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("VARIABLES: Illegal init value.");
                  GlobInfo.parseFail = true;
                  state = VAR_ERROR;
               }
               break;
            }
            case VAR_DONE:
            {
               GlobInfo.hostCtl.printMsg("VARIABLES: Extra info.");
               GlobInfo.parseFail = true;
               state = VAR_ERROR;
               break;
            }
            case VAR_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if (state == VAR_DONE)
      {
         int[]                         tmpArr = new int[numVars];
         int                           index;
         
         /* Save some memory by allocating only the space needed for init array */
         for (index = 0; index < numVars; index++)
         {
            tmpArr[index] = initVarArr[index];
         }
         initVarArr = tmpArr;
      }
      if ((state == VAR_ERROR) || (state == VAR_DONE))
      {
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
} /* End VarClass */
