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
               ParseRules.hmSymbol.put(currName,
                     ParseRules.SYMB_PCHAIN | GlobInfo.numProcObj);
               GlobInfo.numProcObj++;
               mungePChain(startIndex + 2, endIndex, procObjStart);
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
   private void mungePChain(
      int                              startIndex,
      int                              endIndex,
      ProcObj                          firstProcObj)
   {
      int                              currIndex;
      int                              done;
      ProcObj                          currProcObj = null;
      ProcObj                          procObj;
      int                              mungeState = MUNGE_OK;
      
      currIndex = startIndex;
      while (mungeState == MUNGE_OK)
      {
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
                  currProcObj = detParamType(null, currIndex + 2, done - 1, true, true);
                  GlobInfo.procObjArr[GlobInfo.numProcObj] = currProcObj;
                  firstProcObj.oper = ProcObj.OP_GO_TO_PROCOBJ;
                  firstProcObj.trueProcObj = GlobInfo.numProcObj;
                  GlobInfo.numProcObj++;
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
                        /* HRS:  Currently stubbed out
                        procObj = procStatement(currIndex + 1, done); */
                        /* Fill out topmost procObj with this returned obj when if is true */
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
                        procObj = new ProcObj();
                        GlobInfo.procObjArr[GlobInfo.numProcObj] = procObj;
                        currProcObj.trueProcObj = GlobInfo.numProcObj;
                        GlobInfo.numProcObj++;
                        
                        mungePChain(currIndex + 1, done, procObj);
                        /* Fill out topmost procObj with this returned obj when if is true */
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
                           /* HRS:  Currently stubbed out
                           procObj = procStatement(currIndex + 1, done); */
                           /* Fill out topmost procObj with this returned obj when if is false */
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
                           /* HRS:  Currently stubbed out
                           procObj = mungePChain(currIndex + 1, done); */
                           /* Fill out topmost procObj with this returned obj when if is false */
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
               currProcObj = detParamType(currProcObj, currIndex + 1, done - 1, true, false); /* HRS */
               /* HRS: Currently stubbed out
               procObj = procStatement(currIndex + 1, done); */
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
   } /* end mungePChain */

   /*
    * ===============================================================================
    * 
    * Name: procIfState
    * 
    * ===============================================================================
    */
   /**
    * Process if statement
    * 
    * Forming processing objects to determine whether if statement is true or false.
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  startProcObj - index of the starting processing object
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private ProcObj procIfState(
      int                              startIndex,
      int                              endIndex)
   {
      int                              currIndex;
      int                              done;
      ProcObj                          procObj;
      
      procObj = new ProcObj();
      currIndex = startIndex;
      
      /* Walk down looking for multiple open parenthesis.  It could be many
       * levels depending on the "if" statement.
       */
      while (allTokens[currIndex].equals("("))
      {
         done = countDelim("(", ")", currIndex, endIndex);
         if (done == 0)
         {
            /* Couldn't find closing paren. */
            GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in if statement");
            GlobInfo.parseFail = true;
            state = PCHAIN_ERROR;
         }
         else
         {
            /* This is a multi-level if */
            procObj = procIfState(currIndex + 1, done);
         }
      }
      /* 
      fillCompOper(procObj, allTokens[currIndex + 1]);
      
      detParamType(procObj, allTokens[currIndex + 2], false);
      currIndex += 2; */
         /* Must be a variable name/switch input/etc */
      return (procObj);
   } /* end procIfState */

   /*
    * ===============================================================================
    * 
    * Name: procStatement
    * 
    * ===============================================================================
    */
   /**
    * Process a statement
    * 
    * Forming processing objects to implement a statement.
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  startProcObj - index of the starting processing object
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private ProcObj procStatement(
      int                              startIndex,
      int                              endIndex)
   {
      ProcObj                          procObj;
      
      procObj = new ProcObj();
      return (procObj);
   } /* end procStatement */
   
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
            procObj.oper = ProcObj.OP_EQUALS;
         }
         else if (oper.equals("!="))
         {
            procObj.oper = ProcObj.OP_NOT_EQUALS;
         }
         else if (oper.equals(">"))
         {
            procObj.oper = ProcObj.OP_GREATER_THAN;
         }
         else if (oper.equals(">="))
         {
            procObj.oper = ProcObj.OP_GREATER_OR_EQUAL;
         }
         else if (oper.equals("<"))
         {
            procObj.oper = ProcObj.OP_LESS_THAN;
         }
         else if (oper.equals("<="))
         {
            procObj.oper = ProcObj.OP_LESS_OR_EQUAL;
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
            procObj.oper = ProcObj.OP_SET_VAL;
         }
         else if (oper.equals("+="))
         {
            procObj.oper = ProcObj.OP_PLUS_EQUALS;
         }
         else if (oper.equals("|="))
         {
            procObj.oper = ProcObj.OP_PLUS_EQUALS;
         }
         else if (oper.equals("&="))
         {
            procObj.oper = ProcObj.OP_AND_EQUALS;
         }
         else if (oper.equals("++"))
         {
            procObj.oper = ProcObj.OP_INCREMENT;
            needsMoreParams = false;
         }
         else if (oper.equals("--"))
         {
            procObj.oper = ProcObj.OP_DECREMENT;
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
            procObj.oper = ProcObj.OP_BITWISE_AND;
            foundOper = true;
         }
         else if (oper.equals("|"))
         {
            procObj.oper = ProcObj.OP_BITWISE_OR;
         }
         else if (oper.equals("&&"))
         {
            procObj.oper = ProcObj.OP_LOGICAL_AND;
         }
         else if (oper.equals("||"))
         {
            procObj.oper = ProcObj.OP_LOGICAL_OR;
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
      
      currIndex = startIndex;
      if (firstParam)
      {
         procObj = new ProcObj();
         if (ifStatement)
         {
            if (allTokens[currIndex].equals("("))
            {
               done = countDelim("(", ")", currIndex, endIndex);
               if (done == 0)
               {
                  /* Couldn't find closing paren. */
                  GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in if boolean equation");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
               }
               else
               {
                  detParamType(procObj, currIndex + 1, done - 1, true, true);
               }
            }
            else if (allTokens[currIndex].equals("EXPIRED"))
            {
               procObj.paramA = ProcObj.PDVAR_EXPIRED_TIMERS;
               procObj.typeA = ProcObj.TYPE_PREDEF_VAR;
            }
            else if (allTokens[currIndex].equals("MODE"))
            {
               procObj.paramA = ProcObj.PDVAR_MODE;
               procObj.typeA = ProcObj.TYPE_PREDEF_VAR;
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
               procObj.paramA = ProcObj.PREDEF_DISABLE_SOLENOIDS;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("LED_ON"))
            {
               procObj.paramA = ProcObj.PREDEF_LED_ON;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("KICK"))
            {
               procObj.paramA = ProcObj.PREDEF_KICK;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("START"))
            {
               procObj.paramA = ProcObj.PREDEF_START_TIMER;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("ENABLE_SOLENOIDS"))
            {
               procObj.paramA = ProcObj.PREDEF_DISABLE_SOLENOIDS;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("TEXT"))
            {
               procObj.paramA = ProcObj.PREDEF_TEXT;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("SOUND"))
            {
               procObj.paramA = ProcObj.PREDEF_SOUND;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("WAIT"))
            {
               procObj.paramA = ProcObj.PREDEF_WAIT;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("LED_ROT_LEFT"))
            {
               procObj.paramA = ProcObj.PREDEF_LED_ROT_LEFT;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("LED_ROT_RIGHT"))
            {
               procObj.paramA = ProcObj.PREDEF_LED_ROT_RIGHT;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("LED_OFF"))
            {
               procObj.paramA = ProcObj.PREDEF_LED_OFF;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("LED_BLINK_100"))
            {
               procObj.paramA = ProcObj.PREDEF_LED_BLINK_100;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("LED_BLINK_500"))
            {
               procObj.paramA = ProcObj.PREDEF_LED_BLINK_500;
               procObj.typeA = ProcObj.TYPE_FUNC;
            }
            else if (allTokens[currIndex].equals("MODE"))
            {
               procObj.paramA = ProcObj.PDVAR_MODE;
               procObj.typeA = ProcObj.TYPE_PREDEF_VAR;
            }
            else
            {
               foundType = false;
            }
         }
      }
      if (!foundType)
      {
         Integer                          tstKey;
         int                              type;
         
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
                     procObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                     procObj.typeA = ProcObj.TYPE_PREDEF_VAR | ProcObj.PDVAR_SOL_INPUTS;
                  }
                  else
                  {
                     procObj.paramB = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                     procObj.typeB = ProcObj.TYPE_PREDEF_VAR | ProcObj.PDVAR_SOL_INPUTS;
                  }
                  currIndex++;
                  if (currIndex < endIndex)
                  {
                     /* more parameters to process */
                     moreParam = fillCompOper(procObj, allTokens[currIndex], ifStatement);
                     if (moreParam)
                     {
                        /* Check if there are more parameters available */
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           if (firstParam)
                           {
                              /* Add second param to procObj */
                              detParamType(procObj, currIndex, endIndex, false, ifStatement);
                           }
                           else
                           {
                              /* Need to create another procObj to attach to this one */
                              procObj.typeB = ProcObj.TYPE_PROCOBJ_RSLT;
                              detParamType(procObj, currIndex, endIndex, true, ifStatement);
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
                        procObj.oper = ProcObj.OP_NONZERO;
                        procObj.typeB = ProcObj.TYPE_UNUSED;
                     }
                  }
                  break;
               }
               case ParseRules.SYMB_INP_PIN:
               {
                  if (firstParam)
                  {
                     procObj.paramA = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                     procObj.typeA = ProcObj.TYPE_PREDEF_VAR | ProcObj.PDVAR_CARD_INPUTS;
                  }
                  else
                  {
                     procObj.paramB = tstKey.intValue() & ParseRules.SYMB_PARAM_MASK;
                     procObj.typeB = ProcObj.TYPE_PREDEF_VAR | ProcObj.PDVAR_CARD_INPUTS;
                  }
                  currIndex++;
                  if (currIndex < endIndex)
                  {
                     /* more parameters to process */
                     moreParam = fillCompOper(procObj, allTokens[currIndex], ifStatement);
                     if (moreParam)
                     {
                        /* Check if there are more parameters available */
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           if (firstParam)
                           {
                              /* Add second param to procObj */
                              detParamType(procObj, currIndex, endIndex, false, ifStatement);
                           }
                           else
                           {
                              /* Need to create another procObj to attach to this one */
                              procObj.typeB = ProcObj.TYPE_PROCOBJ_RSLT;
                              detParamType(procObj, currIndex, endIndex, true, ifStatement);
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
                        procObj.oper = ProcObj.OP_NONZERO;
                        procObj.typeB = ProcObj.TYPE_UNUSED;
                     }
                  }
                  break;
               }
               case ParseRules.SYMB_LED_PIN:
               {
                  break;
               }
               case ParseRules.SYMB_VAR:
               {
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
      return (procObj);
   } /* end detParamType */
} /* End ParsePChain */
