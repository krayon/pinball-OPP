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
 * @file:   ParsePChain.java
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
 * Parse Process Chain Lists
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class ParsePChain
{
   private static final int            MAX_PCHAIN_TOKENS       = 32768;
   
   private static final int            PCHAIN_NEED_OPEN_CURLY  = 1;
   private static final int            PCHAIN_FIND_CLOSE_CURLY = 2;
   private static final int            PCHAIN_FINISH_PROC      = 3;
   private static final int            PCHAIN_ERROR            = 4;
   private static final int            PCHAIN_DONE             = 5;

   private int                         state = PCHAIN_NEED_OPEN_CURLY;
   private String                      currName;
   private String[]                    allTokens;
   private int                         allTokenLen = 0;
   private int                         delimCnt = 0;

   private static final int            MUNGE_OK                = 0;
   private static final int            MUNGE_ERROR             = 1;
   private static final int            MUNGE_DONE              = 2;

   /*
    * ===============================================================================
    * 
    * Name: ParsePChain
    * 
    * ===============================================================================
    */
   /**
    * Parse Processing Chain
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
   public ParsePChain(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword */
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end ParsePChain */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to parse processing chains
    * 
    * Take tokens and add entries to processing chains.  This class uses fields
    * for name for later lookups.
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
      int                              done;
      int                              newLen;
      int                              startInd;
      int                              endInd;
      
      switch (state)
      {
         case PCHAIN_NEED_OPEN_CURLY:
         {
            if (tokens[currToken].equals("{"))
            {
               state = PCHAIN_FIND_CLOSE_CURLY;
               allTokens = new String[MAX_PCHAIN_TOKENS];
               allTokenLen = tokens.length - currToken;
               if (allTokenLen < MAX_PCHAIN_TOKENS)
               {
                  System.arraycopy(tokens, currToken, allTokens, 0, allTokenLen);
                  
                  /* Count start and end curly braces and parenthesis */
                  done = countDelim("{", "}", 0, allTokenLen);
                  if (done != 0)
                  {
                     /* Trim extra tokens if necessary, drop last } since already used it */
                     state = PCHAIN_FINISH_PROC;
                     allTokenLen = done - 1;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("PCHAIN_PROC: too many tokens");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else
            {
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: needs curly brace");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
            }
            break;
         }
         case PCHAIN_FIND_CLOSE_CURLY:
         {
            newLen = tokens.length - currToken;
            startInd = allTokenLen;
            if (startInd + newLen < MAX_PCHAIN_TOKENS)
            {
               System.arraycopy(tokens, currToken, allTokens, startInd, newLen);
               allTokenLen = startInd + newLen;
               
               /* Count start and end curly braces and parenthesis */
               done = countDelim("{", "}", startInd, allTokenLen);
               if (done != 0)
               {
                  /* Trim extra tokens if necessary, drop last } since already used it */
                  state = PCHAIN_FINISH_PROC;
                  allTokenLen = done;
               }
            }
            else
            {
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: too many tokens");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
            }
            break;
         }
         case PCHAIN_FINISH_PROC:
         case PCHAIN_ERROR:
         {
            break;
         }
         case PCHAIN_DONE:
         {
            GlobInfo.hostCtl.printMsg("PCHAIN_PROC: Extra info.");
            GlobInfo.parseFail = true;
            state = PCHAIN_ERROR;
            break;
         }
      }
      if (state == PCHAIN_FINISH_PROC)
      {
         /* Whole PChain list has been tokenized.  Now separate into individual PChain lists */
         startInd = 1;
         while (state == PCHAIN_FINISH_PROC)
         {
            endInd = findNextPchain(startInd);
            startInd = endInd + 1;
            if (startInd == allTokenLen)
            {
               state = PCHAIN_DONE;
            }
            else if (startInd > allTokenLen)
            {
               state = PCHAIN_ERROR;
            }
         }
         if (state == PCHAIN_DONE)
         {
         }
         if (state == PCHAIN_ERROR)
         {
         }
      }
      if ((state == PCHAIN_ERROR) || (state == PCHAIN_DONE))
      {
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
   
   /*
    * ===============================================================================
    * 
    * Name: countDelim
    * 
    * ===============================================================================
    */
   /**
    * Count delimeter
    * 
    * Count delimiters.  The delimiters are passed into the function.
    * 
    * @param   openDelim - character which is the open delimeter 
    * @param   closeDelim - character which is the close delimeter 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  index - location of end delimeter or zero if not found
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public int countDelim(
      String                           openDelim,
      String                           closeDelim,
      int                              startIndex,
      int                              endIndex)
   {
      int                              currIndex;
      
      for (currIndex = startIndex; currIndex < endIndex; currIndex++)
      {
         if (allTokens[currIndex].equals(openDelim))
         {
            delimCnt++;
         }
         else if (allTokens[currIndex].equals(closeDelim))
         {
            delimCnt--;
            if (delimCnt == 0)
            {
               return (currIndex);
            }
         }
      }
      return (0);
   } /* end countDelim */

   /*
    * ===============================================================================
    * 
    * Name: findNextPchain
    * 
    * ===============================================================================
    */
   /**
    * Find the next PChain
    * 
    * Verify the name is the first parameter, then look for opening and closing curly
    * braces.  Make sure it doesn't overflow the buffer.
    * 
    * @param   startIndex - starting index
    * @return  endIndex - end index of the closing curly brace
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private int findNextPchain(
      int                              startIndex)
   {
      int                              endIndex = 0;
      int                              done;
      Integer                          tstKey;
      ProcObj                          procObjStart;
      ProcObj                          retProcObj;
      
      currName = allTokens[startIndex];
      if (allTokens[startIndex + 1].equals("{"))
      {
         done = countDelim("{", "}", startIndex + 1, allTokenLen);
         if (done == 0)
         {
            GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " needs ending curly brace");
            GlobInfo.parseFail = true;
            state = PCHAIN_ERROR;
         }
         else
         {
            /* Check if this is a duplicate value */
            endIndex = done;
            tstKey = ParseRules.hmSymbol.get(currName);
            if (tstKey == null)
            {
               procObjStart = new ProcObj();
               GlobInfo.procObjArr[GlobInfo.numProcObj] = procObjStart;
               procObjStart.num = GlobInfo.numProcObj;
               ParseRules.hmSymbol.put(currName,
                     ParseRules.SYMB_PCHAIN | GlobInfo.numProcObj);
               GlobInfo.numProcObj++;
               procObjStart.oper = ProcObj.OP_START_CHAIN;
               retProcObj = mungePChain(startIndex + 2, endIndex);
               procObjStart.contProcObj = retProcObj.num;
               procObjStart.trueProcObj = ProcObj.END_CHAIN_PROCOBJ;
               procObjStart.falseProcObj = ProcObj.END_CHAIN_PROCOBJ;
            }
            else
            {
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: Duplicate input names.");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
            }
         }
      }
      else
      {
         GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " needs starting curly brace");
         GlobInfo.parseFail = true;
         state = PCHAIN_ERROR;
      }
      return (endIndex);
   } /* end findNextPchain */

   /*
    * ===============================================================================
    * 
    * Name: mungePChain
    * 
    * ===============================================================================
    */
   /**
    * Munge processing chain
    * 
    * Start forming processing objects
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @param   firstProcObj - procObject that starts the chain
    * @return  None
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private ProcObj mungePChain(
      int                              startIndex,
      int                              endIndex)
   {
      int                              currIndex;
      int                              done;
      ProcObj                          currProcObj = null;
      ProcObj                          firstProcObj = null;
      ProcObj                          procObj;
      int                              mungeState = MUNGE_OK;
      
      currIndex = startIndex;
      while (mungeState == MUNGE_OK)
      {
         currProcObj = new ProcObj();
         GlobInfo.procObjArr[GlobInfo.numProcObj] = currProcObj;
         currProcObj.num = GlobInfo.numProcObj;
         currProcObj.trueProcObj = ProcObj.END_CHAIN_PROCOBJ;
         currProcObj.falseProcObj = ProcObj.END_CHAIN_PROCOBJ;
         currProcObj.contProcObj = ProcObj.END_CHAIN_PROCOBJ;
         GlobInfo.numProcObj++;
         if (firstProcObj == null)
         {
            firstProcObj = currProcObj;
         }
         if (allTokens[currIndex].equals("if"))
         {
            if (allTokens[currIndex + 1].equals("("))
            {
               done = countDelim("(", ")", currIndex, endIndex);
               if (done == 0)
               {
                  /* Couldn't find closing paren. */
                  mungeState = MUNGE_DONE;
                  GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in if statement");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
                  break;
               }
               else
               {
                  currProcObj.oper = ProcObj.OP_IF_PROC;
                  procObj = detParamType(currProcObj, currIndex + 2, done, true, true);
                  if (procObj != null)
                  {
                     GlobInfo.procObjArr[GlobInfo.numProcObj] = procObj;
                     currProcObj.trueProcObj = GlobInfo.numProcObj;
                     procObj.num = GlobInfo.numProcObj;
                     GlobInfo.numProcObj++;
                  }
                  currIndex = done + 1;
                  
                  /* Next symbol can be either { if multiple statements, or ( if a single statement */
                  if (allTokens[currIndex].equals("("))
                  {
                     done = countDelim("(", ")", currIndex, endIndex);
                     if (done == 0)
                     {
                        /* Couldn't find closing paren. */
                        mungeState = MUNGE_DONE;
                        GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in if sub-statement");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        break;
                     }
                     else
                     {
                        procObj = new ProcObj();
                        GlobInfo.procObjArr[GlobInfo.numProcObj] = procObj;
                        procObj.num = GlobInfo.numProcObj;
                        procObj.trueProcObj = ProcObj.END_CHAIN_PROCOBJ;
                        procObj.falseProcObj = ProcObj.END_CHAIN_PROCOBJ;
                        procObj.contProcObj = ProcObj.END_CHAIN_PROCOBJ;
                        GlobInfo.numProcObj++;
                        detParamType(procObj, currIndex + 1, done, true, false);
                        currProcObj.trueProcObj = procObj.num;
                        currIndex = done + 1;
                     }
                  }
                  else if (allTokens[currIndex].equals("{"))
                  {
                     done = countDelim("{", "}", currIndex, endIndex);
                     if (done == 0)
                     {
                        mungeState = MUNGE_DONE;
                        GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close curly brace in if sub-statement");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        break;
                     }
                     else
                     {
                        /* Fill out topmost procObj with this returned obj when if is true */
                        procObj = mungePChain(currIndex + 1, done);
                        currProcObj.trueProcObj = procObj.num;
                        currIndex = done + 1;
                     }
                  }
                  else
                  {
                     /* Couldn't find valid symbol in if clause */
                     mungeState = MUNGE_DONE;
                     GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find valid statement in if sub-clause");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                     break;
                  }
                  
                  /* Next token could be the "else" symbol */
                  if ((currIndex != endIndex) && (allTokens[currIndex].equals("else")))
                  {
                     /* Special case for else if */
                     if (allTokens[currIndex + 1].equals("if"))
                     {
                        /* HRS:  Currently stubbed out
                        procObj = mungePChain(currIndex + 1, done); */
                        /* Fill out topmost procObj with this returned obj when if is false */
                        currIndex = done + 1;
                     }
                     /* Next symbol can be either { if multiple statements, or ( if a single statement */
                     else if (allTokens[currIndex + 1].equals("("))
                     {
                        done = countDelim("(", ")", currIndex, endIndex);
                        if (done == 0)
                        {
                           /* Couldn't find closing paren. */
                           mungeState = MUNGE_DONE;
                           GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in else sub-statement");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                           break;
                        }
                        else
                        {
                           procObj = new ProcObj();
                           GlobInfo.procObjArr[GlobInfo.numProcObj] = procObj;
                           procObj.num = GlobInfo.numProcObj;
                           procObj.trueProcObj = ProcObj.END_CHAIN_PROCOBJ;
                           procObj.falseProcObj = ProcObj.END_CHAIN_PROCOBJ;
                           procObj.contProcObj = ProcObj.END_CHAIN_PROCOBJ;
                           GlobInfo.numProcObj++;
                           detParamType(procObj, currIndex + 1, done, true, false);
                           currProcObj.falseProcObj = procObj.num;
                           currIndex = done + 1;
                        }
                     }
                     else if (allTokens[currIndex + 1].equals("{"))
                     {
                        done = countDelim("{", "}", currIndex, endIndex);
                        if (done == 0)
                        {
                           mungeState = MUNGE_DONE;
                           GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close curly brace in else sub-statement");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                           break;
                        }
                        else
                        {
                           procObj = mungePChain(currIndex + 2, done);
                           currProcObj.falseProcObj = procObj.num;
                           currIndex = done + 1;
                        }
                     }
                     else
                     {
                        /* Couldn't find valid symbol in else clause */
                        mungeState = MUNGE_DONE;
                        GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find valid statement in else sub-clause");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        break;
                     }
                  }
                  else
                  {
                     if (currIndex != endIndex)
                     {
                        /* More terms need to be added, use next allocated procObj */
                        currProcObj.contProcObj = GlobInfo.numProcObj;
                     }
                  }
               }
            }
            else
            {
               /* Open paren not found so error */
               mungeState = MUNGE_DONE;
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find open parenthesis in if statement");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
               break;
            }
         }
         else if (allTokens[currIndex].equals("("))
         {
            done = countDelim("(", ")", currIndex, endIndex);
            if (done == 0)
            {
               /* Couldn't find closing paren. */
               mungeState = MUNGE_DONE;
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in statement");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
               break;
            }
            else
            {
               detParamType(currProcObj, currIndex + 1, done, true, false);
               if (currProcObj != firstProcObj)
               {
                  firstProcObj.contProcObj = currProcObj.num;
               }
               currIndex = done + 1;
           }
         }
         else
         {
            /* Only other valid symbol is a process chain name */
            currIndex = endIndex;
         }
         if (currIndex == endIndex)
         {
            mungeState = MUNGE_DONE;
         }
      }
      return (firstProcObj);
   } /* end mungePChain */

   /*
    * ===============================================================================
    * 
    * Name: fillCompOper
    * 
    * ===============================================================================
    */
   /**
    * Fill out comparison operation
    * 
    * Fill out the comparison operation by looking at the String passed in.
    * 
    * @param   procObj - processing object
    * @param   oper - String containing the operation
    * @param   ifStatement - true if filling out a if statement
    * @return  None
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private boolean fillCompOper(
      ProcObj                          procObj,
      String                           oper,
      boolean                          ifStatement)
   {
      boolean                          needsMoreParams = true;
      boolean                          foundOper;
      
      foundOper = true;
      if (ifStatement)
      {
         if (oper.equals("=="))
         {
            procObj.oper += ProcObj.OP_EQUALS;
         }
         else if (oper.equals("!="))
         {
            procObj.oper += ProcObj.OP_NOT_EQUALS;
         }
         else if (oper.equals(">"))
         {
            procObj.oper += ProcObj.OP_GREATER_THAN;
         }
         else if (oper.equals(">="))
         {
            procObj.oper += ProcObj.OP_GREATER_OR_EQUAL;
         }
         else if (oper.equals("<"))
         {
            procObj.oper += ProcObj.OP_LESS_THAN;
         }
         else if (oper.equals("<="))
         {
            procObj.oper =+ ProcObj.OP_LESS_OR_EQUAL;
         }
         else
         {
            foundOper = false;
         }
      }
      else
      {
         if (oper.equals("="))
         {
            procObj.oper += ProcObj.OP_SET_VAL;
         }
         else if (oper.equals("+="))
         {
            procObj.oper += ProcObj.OP_PLUS_EQUALS;
         }
         else if (oper.equals("|="))
         {
            procObj.oper += ProcObj.OP_PLUS_EQUALS;
         }
         else if (oper.equals("&="))
         {
            procObj.oper += ProcObj.OP_AND_EQUALS;
         }
         else if (oper.equals("++"))
         {
            procObj.oper += ProcObj.OP_INCREMENT;
            needsMoreParams = false;
         }
         else if (oper.equals("--"))
         {
            procObj.oper += ProcObj.OP_DECREMENT;
            needsMoreParams = false;
         }
         else
         {
            foundOper = false;
         }
      }
      if (!foundOper)
      {
         if (oper.equals("&"))
         {
            procObj.oper += ProcObj.OP_BITWISE_AND;
            foundOper = true;
         }
         else if (oper.equals("|"))
         {
            procObj.oper += ProcObj.OP_BITWISE_OR;
         }
         else if (oper.equals("&&"))
         {
            procObj.oper += ProcObj.OP_LOGICAL_AND;
         }
         else if (oper.equals("||"))
         {
            procObj.oper += ProcObj.OP_LOGICAL_OR;
         }
      }
      
      return (needsMoreParams);
   }

   /*
    * ===============================================================================
    * 
    * Name: detParamType
    * 
    * ===============================================================================
    */
   /**
    * Determine param type
    * 
    * Determine the param type and fill out the procObj appropriately.  If filling out
    * paramA, flags are returned to indicate 
    * 
    * @param   procObj - processing object
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @param   firstParam - true if filling out first parameter
    * @param   ifStatement - true if filling in an if statement
    * @return  None
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private ProcObj detParamType(
      ProcObj                          prevProcObj,
      int                              startIndex,
      int                              endIndex,
      boolean                          firstParam,
      boolean                          ifStatement)
   {
      boolean                          foundType = true;
      boolean                          moreParam;
      int                              currIndex;
      ProcObj                          procObj = null;
      int                              done;
      Integer                          tstKey;
      int                              type;
      int                              tmpInt;
      
      currIndex = startIndex;
      if (allTokens[currIndex].equals("("))
      {
         done = countDelim("(", ")", currIndex, endIndex);
         if (done == 0)
         {
            /* Couldn't find closing paren. */
            GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis");
            GlobInfo.parseFail = true;
            state = PCHAIN_ERROR;
         }
         else
         {
            procObj = new ProcObj();
            GlobInfo.procObjArr[GlobInfo.numProcObj] = procObj;
            procObj.num = GlobInfo.numProcObj;
            procObj.trueProcObj = ProcObj.END_CHAIN_PROCOBJ;
            procObj.falseProcObj = ProcObj.END_CHAIN_PROCOBJ;
            procObj.contProcObj = ProcObj.END_CHAIN_PROCOBJ;
            GlobInfo.numProcObj++;
            procObj.oper = ProcObj.OP_SUB_QUANT;
            detParamType(procObj, currIndex + 1, done, true, ifStatement);
            currIndex = done + 1;
            if (firstParam)
            {
               prevProcObj.typeA = ProcObj.TYPE_SUB_QUANT;
               prevProcObj.paramA = procObj.num;
               firstParam = false;
            }
            else
            {
               prevProcObj.typeB = ProcObj.TYPE_SUB_QUANT;
               prevProcObj.paramB = procObj.num;
            }
         }
      }
      if (firstParam)
      {
         if (ifStatement)
         {
            if (allTokens[currIndex].equals("EXPIRED"))
            {
               prevProcObj.typeA = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_EXPIRED_TIMERS;
               prevProcObj.oper = ProcObj.OP_BITWISE_AND;
            }
            else if (allTokens[currIndex].equals("MODE"))
            {
               prevProcObj.typeA = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_MODE;
            }
            else
            {
               foundType = false;
            }
         }
         else
         {
            /* Special objects that can only be found as the first parameter */
            if (allTokens[currIndex].equals("DISABLE_SOLENOIDS"))
            {
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_DISABLE_SOLENOIDS;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_DISABLE_SOLENOIDS;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               currIndex++;
               if (currIndex != endIndex)
               {
                  GlobInfo.hostCtl.printMsg("DISABLE_SOLENOIDS: Extra information in statement.");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("LED_ON"))
            {
               /* LED On functions just need a list of LEDs */
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_LED_ON;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_LED_ON;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               if (allTokens[currIndex + 1].equals(","))
               {
                  currIndex = currIndex + 2;
                  tmpInt = 0;
                  while (currIndex < endIndex)
                  {
                     /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                     if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                        (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                     {
                        currIndex++;
                     }
                     else
                     {
                        tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                        if (tstKey == null)
                        {
                           /* I'm flamoozled.  I have no idea what is going on */
                           GlobInfo.hostCtl.printMsg("LED_ON: Parse symbol fail " + allTokens[currIndex] + ".");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        else
                        {
                           type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                           if (type != ParseRules.SYMB_LED_PIN)
                           {
                              GlobInfo.hostCtl.printMsg("LED_ON: Only LED symbols allowed " + allTokens[currIndex] + ".");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Calculate the bit position of the LED */
                              tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                 ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                           }
                        }
                        currIndex++;
                     }
                  }
                  /* tmpInt must be non-zero */
                  if (tmpInt != 0)
                  {
                     /* Last part of the command should be a destination */
                     prevProcObj.paramA = tmpInt;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LED_ON: Mask must be nonzero.");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_ON: " + currName + " has misformed command");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("KICK"))
            {
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_KICK;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_KICK;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               currIndex++;
               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
               if (tstKey == null)
               {
                  /* I'm flamoozled.  I have no idea what is going on */
                  GlobInfo.hostCtl.printMsg("KICK: Parse symbol fail " + allTokens[currIndex] + ".");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
               else
               {
                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                  if (type != ParseRules.SYMB_SOL_PIN)
                  {
                     GlobInfo.hostCtl.printMsg("KICK: Only solenoid symbols allowed " + allTokens[currIndex] + ".");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
                  else
                  {
                     /* Calculate the bit position of the LED */
                     prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                  }
               }
               currIndex++;
               if (currIndex != endIndex)
               {
                  GlobInfo.hostCtl.printMsg("KICK: Extra information in statement.");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("START"))
            {
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_START_TIMER;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_START_TIMER;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               currIndex++;
               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
               if (tstKey == null)
               {
                  /* I'm flamoozled.  I have no idea what is going on */
                  GlobInfo.hostCtl.printMsg("START: Parse symbol fail " + allTokens[currIndex] + ".");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
               else
               {
                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                  if (type != ParseRules.SYMB_TIMER)
                  {
                     GlobInfo.hostCtl.printMsg("START: Only timer symbols allowed " + allTokens[currIndex] + ".");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
                  else
                  {
                     /* Calculate the bit position of the LED */
                     prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                  }
               }
               currIndex++;
               if (currIndex != endIndex)
               {
                  GlobInfo.hostCtl.printMsg("START: Extra information in statement.");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("ENABLE_SOLENOIDS"))
            {
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_ENABLE_SOLENOIDS;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_ENABLE_SOLENOIDS;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               currIndex++;
               if (currIndex != endIndex)
               {
                  GlobInfo.hostCtl.printMsg("PREDEF_ENABLE_SOLENOIDS: Extra information in statement.");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("TEXT"))
            {
               /* HRS */
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_TEXT;
            }
            else if (allTokens[currIndex].equals("SOUND"))
            {
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_SOUND;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_SOUND;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               currIndex++;
               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
               if (tstKey == null)
               {
                  /* I'm flamoozled.  I have no idea what is going on */
                  GlobInfo.hostCtl.printMsg("KICK: Parse symbol fail " + allTokens[currIndex] + ".");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
               else
               {
                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                  if (type != ParseRules.SYMB_SND)
                  {
                     GlobInfo.hostCtl.printMsg("SOUND: Only sound symbols allowed " + allTokens[currIndex] + ".");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
                  else
                  {
                     /* Calculate the bit position of the LED */
                     prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                  }
               }
               currIndex++;
               if (currIndex != endIndex)
               {
                  GlobInfo.hostCtl.printMsg("SOUND: Extra information in statement.");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("WAIT"))
            {
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_WAIT;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_WAIT;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               currIndex++;
               
               /* Check if this is an integer constant */
               try
               {
                  prevProcObj.paramA = Integer.parseInt(allTokens[currIndex]);
                  currIndex++;
                  if (currIndex != endIndex)
                  {
                     GlobInfo.hostCtl.printMsg("WAIT: Extra information in statement.");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("WAIT: Only integers allowed " + allTokens[currIndex] + ".");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("LED_ROT_LEFT"))
            {
               /* Rotate functions needs mask which is a constant, and a variable */
               prevProcObj.oper = ProcObj.OP_STATEMENT_PROC + ProcObj.PREDEF_LED_ROT_LEFT;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_LED_ROT_LEFT;
               if (allTokens[currIndex + 1].equals(","))
               {
                  currIndex = currIndex + 2;
                  tmpInt = 0;
                  while ((!allTokens[currIndex].equals(",")) && (currIndex < endIndex))
                  {
                     /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                     if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                        (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                     {
                        currIndex++;
                     }
                     else
                     {
                        tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                        if (tstKey == null)
                        {
                           /* I'm flamoozled.  I have no idea what is going on */
                           GlobInfo.hostCtl.printMsg("LED_ROT_LEFT: Parse symbol fail " + allTokens[currIndex] + ".");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        else
                        {
                           type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                           if (type != ParseRules.SYMB_LED_PIN)
                           {
                              GlobInfo.hostCtl.printMsg("LED_ROT_LEFT: Only LED symbols allowed " + allTokens[currIndex] + ".");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Calculate the bit position of the LED */
                              tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                 ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                           }
                        }
                        currIndex++;
                     }
                  }
                  if ((currIndex < endIndex) && allTokens[currIndex].equals(","))
                  {
                     /* tmpInt must be non-zero */
                     if (tmpInt != 0)
                     {
                        /* Last part of the command should be a destination */
                        prevProcObj.paramA = tmpInt;
                        currIndex++;
                        detParamType(prevProcObj, currIndex, endIndex, false, false);
                        currIndex = endIndex;
                        if ((((prevProcObj.typeB / 1000) * 1000) != ProcObj.TYPE_VARIABLE) &&
                           (((prevProcObj.typeB / 1000) * 1000) != ProcObj.TYPE_INDX_VAR))
                        {
                           GlobInfo.hostCtl.printMsg("LED_ROT_LEFT: Destination must be a variable.");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                     }
                     else
                     {
                        GlobInfo.hostCtl.printMsg("LED_ROT_LEFT: Mask must be nonzero.");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                     }
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_ROT_LEFT: " + currName + " has misformed command");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("LED_ROT_RIGHT"))
            {
               /* Rotate functions needs mask which is a constant, and a variable */
               prevProcObj.oper = ProcObj.OP_STATEMENT_PROC + ProcObj.PREDEF_LED_ROT_RIGHT;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_LED_ROT_RIGHT;
               if (allTokens[currIndex + 1].equals(","))
               {
                  currIndex = currIndex + 2;
                  tmpInt = 0;
                  while ((!allTokens[currIndex].equals(",")) && (currIndex < endIndex))
                  {
                     /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                     if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                        (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                     {
                        currIndex++;
                     }
                     else
                     {
                        tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                        if (tstKey == null)
                        {
                           /* I'm flamoozled.  I have no idea what is going on */
                           GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Parse symbol fail " + allTokens[currIndex] + ".");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        else
                        {
                           type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                           if (type != ParseRules.SYMB_LED_PIN)
                           {
                              GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Only LED symbols allowed " + allTokens[currIndex] + ".");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Calculate the bit position of the LED */
                              tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                 ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                           }
                        }
                        currIndex++;
                     }
                  }
                  if ((currIndex < endIndex) && allTokens[currIndex].equals(","))
                  {
                     /* tmpInt must be non-zero */
                     if (tmpInt != 0)
                     {
                        /* Last part of the command should be a destination */
                        prevProcObj.paramA = tmpInt;
                        currIndex++;
                        detParamType(prevProcObj, currIndex, endIndex, false, false);
                        currIndex = endIndex;
                        if ((((prevProcObj.typeB / 1000) * 1000) != ProcObj.TYPE_VARIABLE) &&
                           (((prevProcObj.typeB / 1000) * 1000) != ProcObj.TYPE_INDX_VAR))
                        {
                           GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Destination must be a variable.");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                     }
                     else
                     {
                        GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Mask must be nonzero.");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                     }
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: " + currName + " has misformed command");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("LED_OFF"))
            {
               /* LED Off functions just need a list of LEDs */
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_LED_OFF;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_LED_OFF;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               if (allTokens[currIndex + 1].equals(","))
               {
                  currIndex = currIndex + 2;
                  tmpInt = 0;
                  while (currIndex < endIndex)
                  {
                     /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                     if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                        (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                     {
                        currIndex++;
                     }
                     else
                     {
                        tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                        if (tstKey == null)
                        {
                           /* I'm flamoozled.  I have no idea what is going on */
                           GlobInfo.hostCtl.printMsg("LED_OFF: Parse symbol fail " + allTokens[currIndex] + ".");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        else
                        {
                           type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                           if (type != ParseRules.SYMB_LED_PIN)
                           {
                              GlobInfo.hostCtl.printMsg("LED_OFF: Only LED symbols allowed " + allTokens[currIndex] + ".");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Calculate the bit position of the LED */
                              tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                 ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                           }
                        }
                        currIndex++;
                     }
                  }
                  /* tmpInt must be non-zero */
                  if (tmpInt != 0)
                  {
                     /* Last part of the command should be a destination */
                     prevProcObj.paramA = tmpInt;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LED_OFF: Mask must be nonzero.");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_OFF: " + currName + " has misformed command");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("LED_BLINK_100"))
            {
               /* LED Blink functions just need a list of LEDs */
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_LED_BLINK_100;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_LED_BLINK_100;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               if (allTokens[currIndex + 1].equals(","))
               {
                  currIndex = currIndex + 2;
                  tmpInt = 0;
                  while (currIndex < endIndex)
                  {
                     /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                     if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                        (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                     {
                        currIndex++;
                     }
                     else
                     {
                        tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                        if (tstKey == null)
                        {
                           /* I'm flamoozled.  I have no idea what is going on */
                           GlobInfo.hostCtl.printMsg("LED_BLINK_100: Parse symbol fail " + allTokens[currIndex] + ".");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        else
                        {
                           type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                           if (type != ParseRules.SYMB_LED_PIN)
                           {
                              GlobInfo.hostCtl.printMsg("LED_BLINK_100: Only LED symbols allowed " + allTokens[currIndex] + ".");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Calculate the bit position of the LED */
                              tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                 ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                           }
                        }
                        currIndex++;
                     }
                  }
                  /* tmpInt must be non-zero */
                  if (tmpInt != 0)
                  {
                     /* Last part of the command should be a destination */
                     prevProcObj.paramA = tmpInt;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LED_BLINK_100: Mask must be nonzero.");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_BLINK_100: " + currName + " has misformed command");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("LED_BLINK_500"))
            {
               /* LED Blink functions just need a list of LEDs */
               prevProcObj.oper = ProcObj.OP_PREDEF_FUNC + ProcObj.PREDEF_LED_BLINK_500;
               prevProcObj.typeA = ProcObj.TYPE_FUNC + ProcObj.PREDEF_LED_BLINK_500;
               prevProcObj.typeB = ProcObj.TYPE_UNUSED;
               if (allTokens[currIndex + 1].equals(","))
               {
                  currIndex = currIndex + 2;
                  tmpInt = 0;
                  while (currIndex < endIndex)
                  {
                     /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                     if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                        (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                     {
                        currIndex++;
                     }
                     else
                     {
                        tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                        if (tstKey == null)
                        {
                           /* I'm flamoozled.  I have no idea what is going on */
                           GlobInfo.hostCtl.printMsg("LED_BLINK_500: Parse symbol fail " + allTokens[currIndex] + ".");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        else
                        {
                           type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                           if (type != ParseRules.SYMB_LED_PIN)
                           {
                              GlobInfo.hostCtl.printMsg("LED_BLINK_500: Only LED symbols allowed " + allTokens[currIndex] + ".");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Calculate the bit position of the LED */
                              tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                 ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                           }
                        }
                        currIndex++;
                     }
                  }
                  /* tmpInt must be non-zero */
                  if (tmpInt != 0)
                  {
                     /* Last part of the command should be a destination */
                     prevProcObj.paramA = tmpInt;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LED_BLINK_500: Mask must be nonzero.");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_BLINK_500: " + currName + " has misformed command");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else if (allTokens[currIndex].equals("MODE"))
            {
               prevProcObj.typeA = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_MODE;
               if (allTokens[currIndex + 1].equals("="))
               {
                  prevProcObj.oper = ProcObj.OP_SET_VAL;
                  prevProcObj.typeB = ProcObj.TYPE_CONSTANT;
                  prevProcObj.paramB = GlobInfo.modeClass.CreateMode(allTokens[currIndex + 2]);
                  if (endIndex != currIndex + 3)
                  {
                     GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " extra info in set mode command");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                  }
               }
               else
               {
                  /* MODE command has wrong params */
                  GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find = when setting mode");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
            }
            else
            {
               foundType = false;
            }
         }
      }
      else
      {
         /* Check if the operation has already been filled out */
         if ((prevProcObj.oper % 1000) == 0)
         {
            moreParam = fillCompOper(prevProcObj, allTokens[currIndex], ifStatement);
            if (moreParam)
            {
               detParamType(prevProcObj, currIndex + 1, endIndex, false, ifStatement);
               currIndex += 2;
            }
         }
         else
         {
            foundType = false;
         }
      }
      if (currIndex < endIndex)
      {
         if (!foundType)
         {
            /* Check if this is an integer constant */
            try
            {
               tmpInt = Integer.parseInt(allTokens[currIndex]);
               if (firstParam)
               {
                  prevProcObj.paramA = tmpInt;
                  prevProcObj.typeA = ProcObj.TYPE_CONSTANT;
               }
               else
               {
                  prevProcObj.paramB = tmpInt;
                  prevProcObj.typeB = ProcObj.TYPE_CONSTANT;
               }
               currIndex++;
               if (currIndex < endIndex)
               {
                  /* more parameters to process */
                  procObj = detParamType(prevProcObj, currIndex, endIndex, false, ifStatement);
                  currIndex = endIndex + 1;
               }
               else
               {
                  /* No more parameters */
                  if (firstParam && ifStatement)
                  {
                     prevProcObj.oper = ProcObj.OP_NONZERO;
                     prevProcObj.typeB = ProcObj.TYPE_UNUSED;
                  }
               }
            }
            catch (NumberFormatException e)
            {
               /* If it isn't a reserved word, it must be defined symbol */
               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
               if (tstKey == null)
               {
                  /* I'm flamoozled.  I have no idea what is going on */
                  GlobInfo.hostCtl.printMsg("PARSE_PCHAIN: Unknown symbol " + allTokens[currIndex] + ".");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
               else
               {
                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                  switch (type)
                  {
                     case ParseRules.SYMB_SOL_PIN:
                     {
                        if (firstParam)
                        {
                           prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeA = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_SOL_INPUTS;
                        }
                        else
                        {
                           prevProcObj.paramB = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeB = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_SOL_INPUTS;
                        }
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           /* more parameters to process */
                           procObj = detParamType(prevProcObj, currIndex, endIndex, false, ifStatement);
                           currIndex = endIndex + 1;
                        }
                        else
                        {
                           /* No more parameters */
                           if (firstParam && ifStatement)
                           {
                              prevProcObj.oper = ProcObj.OP_NONZERO;
                              prevProcObj.typeB = ProcObj.TYPE_UNUSED;
                           }
                        }
                        break;
                     }
                     case ParseRules.SYMB_INP_PIN:
                     {
                        if (firstParam)
                        {
                           prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeA = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_CARD_INPUTS;
                        }
                        else
                        {
                           prevProcObj.paramB = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeB = ProcObj.TYPE_PREDEF_VAR + ProcObj.PDVAR_CARD_INPUTS;
                        }
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           /* more parameters to process */
                           procObj = detParamType(prevProcObj, currIndex, endIndex, false, ifStatement);
                           currIndex = endIndex + 1;
                        }
                        else
                        {
                           /* No more parameters */
                           if (firstParam && ifStatement)
                           {
                              prevProcObj.oper = ProcObj.OP_NONZERO;
                              prevProcObj.typeB = ProcObj.TYPE_UNUSED;
                           }
                        }
                        break;
                     }
                     case ParseRules.SYMB_LED_PIN:
                     {
                        /* Called when LED pins names are used as constants */
                        tmpInt = 0;
                        while (currIndex < endIndex)
                        {
                           /* Ignore all open, close paren, and '+' and '|' since just creating a mask */
                           if ((allTokens[currIndex].equals("(")) || (allTokens[currIndex].equals(")")) ||
                              (allTokens[currIndex].equals("+")) || (allTokens[currIndex].equals("|")))
                           {
                              currIndex++;
                           }
                           else
                           {
                              tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
                              if (tstKey == null)
                              {
                                 /* I'm flamoozled.  I have no idea what is going on */
                                 GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Parse symbol fail " + allTokens[currIndex] + ".");
                                 GlobInfo.parseFail = true;
                                 state = PCHAIN_ERROR;
                              }
                              else
                              {
                                 type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                                 if (type != ParseRules.SYMB_LED_PIN)
                                 {
                                    GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Only LED symbols allowed " + allTokens[currIndex] + ".");
                                    GlobInfo.parseFail = true;
                                    state = PCHAIN_ERROR;
                                 }
                                 else
                                 {
                                    /* Calculate the bit position of the LED */
                                    tmpInt += (1 << (((((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8) & 0xff) << 3) +
                                       ((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) & 0xff)));
                                 }
                              }
                              currIndex++;
                           }
                        }
                        if (firstParam)
                        {
                           prevProcObj.paramA = tmpInt;
                           prevProcObj.typeA = ProcObj.TYPE_CONSTANT;
                        }
                        else
                        {
                           prevProcObj.paramB = tmpInt;
                           prevProcObj.typeB = ProcObj.TYPE_CONSTANT;
                        }
                        break;
                     }
                     case ParseRules.SYMB_VAR:
                     {
                        if (firstParam)
                        {
                           prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeA = ProcObj.TYPE_VARIABLE;
                        }
                        else
                        {
                           prevProcObj.paramB = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeB = ProcObj.TYPE_VARIABLE;
                        }
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           /* more parameters to process */
                           procObj = detParamType(prevProcObj, currIndex, endIndex, false, ifStatement);
                           currIndex = endIndex + 1;
                        }
                        else
                        {
                           /* No more parameters */
                           if (firstParam && ifStatement)
                           {
                              prevProcObj.oper = ProcObj.OP_NONZERO;
                              prevProcObj.typeB = ProcObj.TYPE_UNUSED;
                           }
                        }
                        break;
                     }
                     case ParseRules.SYMB_INDX_VAR:
                     {
                        /* An indexed variable requires its own ProcObj for extra params */
                        procObj = new ProcObj();
                        GlobInfo.procObjArr[GlobInfo.numProcObj] = procObj;
                        procObj.num = GlobInfo.numProcObj;
                        GlobInfo.numProcObj++;
                        procObj.oper = ProcObj.OP_INDX_VAR;
                        procObj.typeA = ProcObj.TYPE_INDX_VAR;
                        procObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                        if (firstParam)
                        {
                           prevProcObj.paramA = procObj.num;
                           prevProcObj.typeA = ProcObj.TYPE_INDX_VAR;
                        }
                        else
                        {
                           prevProcObj.paramB = procObj.num;
                           prevProcObj.typeB = ProcObj.TYPE_INDX_VAR;
                        }
                        currIndex++;
                        
                        /* Next symbol must be [ */
                        if (allTokens[currIndex].equals("["))
                        {
                           done = countDelim("[", "]", currIndex, endIndex);
                           if (done == 0)
                           {
                              GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " needs ending brace.");
                              GlobInfo.parseFail = true;
                              state = PCHAIN_ERROR;
                           }
                           else
                           {
                              /* Find the variable that is used as the index */
                              detParamType(procObj, currIndex + 1, done, false, false);
                           }
                           currIndex = done + 1;
                        }
                        else
                        {
                           GlobInfo.hostCtl.printMsg("PARSE_PCHAIN: Indexed variable doesn't have open bracket.");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                        }
                        break;
                     }
                     case ParseRules.SYMB_SND:
                     {
                        break;
                     }
                     case ParseRules.SYMB_BIG_VID:
                     {
                        break;
                     }
                     case ParseRules.SYMB_LITTLE_VID:
                     {
                        break;
                     }
                     case ParseRules.SYMB_PCHAIN:
                     {
                        break;
                     }
                     case ParseRules.SYMB_TIMER:
                     {
                        break;
                     }
                     case ParseRules.SYMB_CONST:
                     {
                        if (firstParam)
                        {
                           prevProcObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeA = ProcObj.TYPE_CONSTANT;
                        }
                        else
                        {
                           prevProcObj.paramB = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                           prevProcObj.typeB = ProcObj.TYPE_CONSTANT;
                        }
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           /* more parameters to process */
                           procObj = detParamType(prevProcObj, currIndex, endIndex, false, ifStatement);
                           moreParam = fillCompOper(prevProcObj, allTokens[currIndex], ifStatement);
                           if (moreParam)
                           {
                              /* Check if there are more parameters available */
                              currIndex++;
                              if (currIndex < endIndex)
                              {
                                 if (firstParam)
                                 {
                                    /* Add second param to procObj */
                                    detParamType(prevProcObj, currIndex, endIndex, false, ifStatement);
                                 }
                                 else
                                 {
                                    /* Need to create another procObj to attach to this one */
                                    prevProcObj.typeB = ProcObj.TYPE_PREV_RSLT;
                                    detParamType(prevProcObj, currIndex, endIndex, true, ifStatement);
                                 }
                              }
                              else
                              {
                                 GlobInfo.hostCtl.printMsg("PARSE_PCHAIN: " + currName + " needs more params, but none avail.");
                                 GlobInfo.parseFail = true;
                                 state = PCHAIN_ERROR;
                              }
                           }
                           else
                           {
                              /* Either an increment or decrement command */
                           }
                        }
                        else
                        {
                           /* No more parameters */
                           if (firstParam && ifStatement)
                           {
                              prevProcObj.oper = ProcObj.OP_NONZERO;
                              prevProcObj.typeB = ProcObj.TYPE_UNUSED;
                           }
                        }
                        break;
                     }
                     default:
                     {
                        GlobInfo.hostCtl.printMsg("PARSE_PCHAIN: Unknown symbol type = " + type + ".");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        break;
                     }
                  }
               }
            }
         }
      }
      return (procObj);
   } /* end detParamType */
} /* End ParsePChain */
