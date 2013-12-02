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
 * @file:   IndxVarClass.java
 * @author: Hugh Spahr
 * @date:   2/10/2013
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
 * Indexed Variable class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class IndxVarClass
{
   private static final int            MAX_NUM_INDX_VARS       = 4096;
   private static final int            MAX_INDX_LENGTH         = 16;
   
   private static final int            INDX_NEED_OPEN_CURLY    = 1;
   private static final int            INDX_PROC_INDX_NAME     = 2;
   private static final int            INDX_PROC_ENTRIES       = 3;
   private static final int            INDX_START_INIT_GRP     = 4;
   private static final int            INDX_PROC_INIT_VAL      = 5;
   private static final int            INDX_DONE               = 6;
   private static final int            INDX_ERROR              = 7;

   private int                         state = INDX_NEED_OPEN_CURLY;
   private int                         numIndxVars = 0;
   private String                      currName;
   private int                         numEntries;
   private int                         lastInitVal;
   private int[]                       initIndxArr;
   private int                         initIndex;

   /*
    * ===============================================================================
    * 
    * Name: IndxVarClass
    * 
    * ===============================================================================
    */
   /**
    * Index Variable class
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
   public IndxVarClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword, second should be num cards  */
      initIndxArr = new int[MAX_NUM_INDX_VARS];
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end IndxVarClass */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create indexed variables
    * 
    * Take tokens and add entries to create indexed variables.  This class uses fields
    * to configure the index vars, and name each indexed var for later lookups.
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
            case INDX_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = INDX_PROC_INDX_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: needs curly parenthesis.");
                  GlobInfo.parseFail = true;
                  state = INDX_ERROR;
               }
               break;
            }
            case INDX_PROC_INDX_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = INDX_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = INDX_PROC_ENTRIES;
               }
               break;
            }
            case INDX_PROC_ENTRIES:
            {
               try
               {
                  numEntries = Integer.parseInt(tokens[currToken]);
                  if ((numIndxVars + numEntries < MAX_NUM_INDX_VARS) && (numEntries < MAX_INDX_LENGTH))
                  {
                     state = INDX_START_INIT_GRP;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Too many indexed variables.");
                     GlobInfo.parseFail = true;
                     state = INDX_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Illegal num entries.");
                  GlobInfo.parseFail = true;
                  state = INDX_ERROR;
               }
               break;
            }
            case INDX_START_INIT_GRP:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = INDX_PROC_INIT_VAL;
                  initIndex = 0;
                  lastInitVal = 0;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: needs curly parenthesis for init values.");
                  GlobInfo.parseFail = true;
                  state = INDX_ERROR;
               }
               break;
            }
            case INDX_PROC_INIT_VAL:
            {
               int                              index;
               Integer                          tstKey;
               boolean                          addHash = false;;
               
               if (tokens[currToken].equals("}"))
               {
                  /* Open and close curly brace means all entries are zero.  If only
                   * one entry exists, all entries are initialized to that value.
                   */
                  if ((initIndex == 0) || (initIndex == 1))
                  {
                     /* An open and close curly brace means init entries to zero */
                     for (index = 0; index < numEntries; index++)
                     {
                        initIndxArr[numIndxVars + index] = lastInitVal;
                     }
                     addHash = true;
                  }
                  else if (initIndex == numEntries)
                  {
                     addHash = true;
                  }
                  else
                  {
                     /* Incorrect number of initial values */
                     GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Incorrect num init values.");
                     GlobInfo.parseFail = true;
                     state = INDX_ERROR;
                  }
                  if (addHash)
                  {
                     /* Check if this is a duplicate value */
                     tstKey = ParseRules.hmSymbol.get(currName);
                     if (tstKey == null)
                     {
                         ParseRules.hmSymbol.put(currName,
                            ParseRules.SYMB_INDX_VAR | (numEntries << 12) | ParseRules.allocInd);
                      	 GlobInfo.fileConstClass.println("   public static final int             " +
                               String.format("%-27s= %2d;", currName.toUpperCase(), ParseRules.allocInd));
                         ParseRules.allocInd += numEntries;
                         numIndxVars += numEntries;
                         state = INDX_PROC_INDX_NAME;
                     }
                     else
                     {
                        GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Duplicate names.");
                        GlobInfo.parseFail = true;
                        state = INDX_ERROR;
                     }
                  }
               }
               else
               {
                  /* Grab the init value */
                  try
                  {
                     lastInitVal = Integer.parseInt(tokens[currToken]);
                     if (numIndxVars + initIndex < MAX_NUM_INDX_VARS)
                     {
                        initIndxArr[numIndxVars + initIndex] = lastInitVal;
                        initIndex++;
                     }
                     else
                     {
                        GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Init values, num entries mismatch.");
                        GlobInfo.parseFail = true;
                        state = INDX_ERROR;
                     }
                  }
                  catch (NumberFormatException e)
                  {
                     GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Illegal init value.");
                     GlobInfo.parseFail = true;
                     state = INDX_ERROR;
                  }
               }
               break;
            }
            case INDX_DONE:
            {
               GlobInfo.hostCtl.printMsg("INDEXED_VARIABLES: Extra info.");
               GlobInfo.parseFail = true;
               state = INDX_ERROR;
               break;
            }
            case INDX_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if (state == INDX_DONE)
      {
         int[]                         tmpArr = new int[numIndxVars];
         int                           index;
         
         /* Save some memory by allocating only the space needed for init array */
         for (index = 0; index < numIndxVars; index++)
         {
            tmpArr[index] = initIndxArr[index];
         }
         initIndxArr = tmpArr;
      }
      if ((state == INDX_ERROR) || (state == INDX_DONE))
      {
      	GlobInfo.fileConstClass.println("");
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
} /* End IndxVarClass */
