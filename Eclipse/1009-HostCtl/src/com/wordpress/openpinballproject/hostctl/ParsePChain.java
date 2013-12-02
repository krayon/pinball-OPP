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
      }

      /* Clean up memory */
      if ((state == PCHAIN_ERROR) || (state == PCHAIN_DONE))
      {
         allTokens = null;
      	GlobInfo.fileConstClass.println("");
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
            	GlobInfo.fileRulesClass.println("   public void " + currName + "()");
            	GlobInfo.fileRulesClass.println("   {");
            	GlobInfo.currIndent = 2;
               ParseRules.hmSymbol.put(currName,
                  ParseRules.SYMB_PCHAIN | GlobInfo.numPChain);
            	GlobInfo.fileConstClass.println("   public static final int             " +
                  String.format("%-27s= %2d;", currName.toUpperCase(), GlobInfo.numPChain));
               GlobInfo.numPChain++;
               mungePChain(startIndex + 2, endIndex);
            	GlobInfo.fileRulesClass.println("   }");
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
    * Call munge pchain when walking through a list of tokens that can contain
    * if statements.  If in a testing clause, call detParamType.
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  None
    * 
    * @pre None 
    * @note Can change state to PCHAIN_ERROR if an error occurs.
    * 
    * ===============================================================================
    */
   private void mungePChain(
      int                              startIndex,
      int                              endIndex)
   {
      int                              currIndex;
      int                              done;
      Integer                          tstKey;
      int                              type;
      
      currIndex = startIndex;
      while (currIndex < endIndex)
      {
         if (allTokens[currIndex].equals("if"))
         {
            if (allTokens[currIndex + 1].equals("("))
            {
               done = countDelim("(", ")", currIndex, endIndex);
               if (done == 0)
               {
                  /* Couldn't find closing paren. */
                  GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in if statement");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
                  currIndex = endIndex;
                  break;
               }
               else
               {
               	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
               	GlobInfo.fileRulesClass.print("if (");
                  detParamType(currIndex + 2, done, true, true);
                  currIndex = done + 1;
               	GlobInfo.fileRulesClass.println(")");
               	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
               	GlobInfo.fileRulesClass.println("{");
               	GlobInfo.currIndent++;

                  /* Next symbol can be either { if multiple statements, or ( if a single statement */
                  if (allTokens[currIndex].equals("("))
                  {
                     done = countDelim("(", ")", currIndex, endIndex);
                     if (done == 0)
                     {
                        /* Couldn't find closing paren. */
                        GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in if sub-statement");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        currIndex = endIndex;
                        break;
                     }
                     else
                     {
                     	/* This is a single command, so call detParamType */
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                        detParamType(currIndex + 1, done, true, false);
                     	GlobInfo.fileRulesClass.println(";");
                        currIndex = done + 1;
                     	GlobInfo.currIndent--;
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.println("}");
                     }
                  }
                  else if (allTokens[currIndex].equals("{"))
                  {
                     done = countDelim("{", "}", currIndex, endIndex);
                     if (done == 0)
                     {
                        GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close curly brace in if sub-statement");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        currIndex = endIndex;
                        break;
                     }
                     else
                     {
                     	/* This has multiple commands, so call mungePChain */
                        mungePChain(currIndex + 1, done);
                        currIndex = done + 1;
                     	GlobInfo.currIndent--;
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.println("}");
                     }
                  }
                  else
                  {
                     /* Couldn't find valid symbol in if clause */
                     GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find valid statement in if sub-clause");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                     currIndex = endIndex;
                     break;
                  }
                  
                  /* Next token could be the "else" symbol */
                  if ((currIndex < endIndex) && (allTokens[currIndex].equals("else")))
                  {
                     /* Special case for else if */
                     if (allTokens[currIndex + 1].equals("if"))
                     {
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.print("else");
                        mungePChain(currIndex + 1, endIndex);
                        currIndex = endIndex + 1;
                     }
                     /* Next symbol can be either { if multiple statements, or ( if a single statement */
                     else if (allTokens[currIndex + 1].equals("("))
                     {
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.println("else");
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.println("{");
                     	GlobInfo.currIndent++;
                        done = countDelim("(", ")", currIndex, endIndex);
                        if (done == 0)
                        {
                           /* Couldn't find closing paren. */
                           GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in else sub-statement");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                           currIndex = endIndex;
                           break;
                        }
                        else
                        {
                        	/* This is a single command, so call detParamType */
	                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
	                        detParamType(currIndex + 2, done, true, false);
	                     	GlobInfo.fileRulesClass.println(";");
	                     	GlobInfo.currIndent--;
	                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
	                     	GlobInfo.fileRulesClass.println("}");
                           currIndex = done + 1;
                        }
                     }
                     else if (allTokens[currIndex + 1].equals("{"))
                     {
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.println("else");
                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     	GlobInfo.fileRulesClass.println("{");
                     	GlobInfo.currIndent++;
                        done = countDelim("{", "}", currIndex, endIndex);
                        if (done == 0)
                        {
                           GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close curly brace in else sub-statement");
                           GlobInfo.parseFail = true;
                           state = PCHAIN_ERROR;
                           currIndex = endIndex;
                           break;
                        }
                        else
                        {
                        	/* This has multiple commands, so call mungePChain */
	                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
	                        mungePChain(currIndex + 2, done);
	                        currIndex = done + 1;
	                     	GlobInfo.currIndent--;
	                     	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
	                     	GlobInfo.fileRulesClass.println("}");
                        }
                     }
                     else
                     {
                        /* Couldn't find valid symbol in else clause */
                        GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find valid statement in else sub-clause");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
                        currIndex = endIndex;
                        break;
                     }
                  }
               }
            }
            else
            {
               /* Open paren not found so error */
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find open parenthesis in if statement");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
               currIndex = endIndex;
               break;
            }
         }
         else if (allTokens[currIndex].equals("("))
         {
            done = countDelim("(", ")", currIndex, endIndex);
            if (done == 0)
            {
               /* Couldn't find closing paren. */
               GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " couldn't find close parenthesis in statement");
               GlobInfo.parseFail = true;
               state = PCHAIN_ERROR;
               currIndex = endIndex;
               break;
            }
            else
            {
            	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
               detParamType(currIndex + 1, done, true, false);
            	GlobInfo.fileRulesClass.println(";");
               currIndex = done + 1;
           }
         }
         else
         {
         	while (currIndex < endIndex)
         	{
            	/* Check to see if this is a processing chain */
               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
               if (tstKey == null)
               {
                  /* Don't know what this symbol is. */
                  GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " not expecting " + allTokens[currIndex] + " symbol");
                  GlobInfo.parseFail = true;
                  state = PCHAIN_ERROR;
                  currIndex = endIndex;
               }
               else
               {
                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
                  if (type != ParseRules.SYMB_PCHAIN)
                  {
                     GlobInfo.hostCtl.printMsg("PCHAIN_PROC: Only pchain symbols allowed " + allTokens[currIndex] + ".");
                     GlobInfo.parseFail = true;
                     state = PCHAIN_ERROR;
                     currIndex++;
                  }
                  else
                  {
                     /* Calculate the bit position of the LED */
                  	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
   	            	GlobInfo.fileRulesClass.printf("StdFuncs.CallPChain(ConstClass.%s)",
                       	allTokens[currIndex].toUpperCase());
                     currIndex++;
                     
                     /* Check if the next token is "," so another it could be another pchain */
                     if (allTokens[currIndex].equals(","))
                     {
                        currIndex++;
                     	GlobInfo.fileRulesClass.printf(";");
                     }
   	            }
               }
         	}
         }
      }
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
      String                           oper,
      boolean                          ifStatement)
   {
      boolean                          foundOper;
      
      foundOper = true;
      if (ifStatement)
      {
         if (oper.equals("=="))
         {
         	GlobInfo.fileRulesClass.print(" == ");
         }
         else if (oper.equals("!="))
         {
         	GlobInfo.fileRulesClass.print(" != ");
         }
         else if (oper.equals(">"))
         {
         	GlobInfo.fileRulesClass.print(" > ");
         }
         else if (oper.equals(">="))
         {
         	GlobInfo.fileRulesClass.print(" >= ");
         }
         else if (oper.equals("<"))
         {
         	GlobInfo.fileRulesClass.print(" < ");
         }
         else if (oper.equals("<="))
         {
         	GlobInfo.fileRulesClass.print(" <= ");
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
         	GlobInfo.fileRulesClass.print(" = ");
         }
         else if (oper.equals("+="))
         {
         	GlobInfo.fileRulesClass.print(" += ");
         }
         else if (oper.equals("|="))
         {
         	GlobInfo.fileRulesClass.print(" |= ");
         }
         else if (oper.equals("&="))
         {
         	GlobInfo.fileRulesClass.print(" &= ");
         }
         else if (oper.equals("++"))
         {
         	GlobInfo.fileRulesClass.print("++");
         }
         else if (oper.equals("--"))
         {
         	GlobInfo.fileRulesClass.print("--");
         }
         else
         {
            foundOper = false;
         }
      }
      if (!foundOper)
      {
         foundOper = true;
         if (oper.equals("&"))
         {
         	GlobInfo.fileRulesClass.print(" & ");
         }
         else if (oper.equals("|"))
         {
         	GlobInfo.fileRulesClass.print(" | ");
         }
         else if (oper.equals("&&"))
         {
         	GlobInfo.fileRulesClass.println(" &&");
         	GlobInfo.fileRulesClass.printf("%" + ((GlobInfo.currIndent + 1) * 3) + "s", "");
         }
         else if (oper.equals("||"))
         {
         	GlobInfo.fileRulesClass.println(" ||");
         	GlobInfo.fileRulesClass.printf("%" + ((GlobInfo.currIndent + 1) * 3) + "s", "");
         }
         else if (oper.equals("+"))
         {
         	GlobInfo.fileRulesClass.print(" + ");
         }
         else if (oper.equals("-"))
         {
         	GlobInfo.fileRulesClass.print(" - ");
         }
         else if (oper.equals("*"))
         {
         	GlobInfo.fileRulesClass.print(" * ");
         }
         else if (oper.equals("/"))
         {
         	GlobInfo.fileRulesClass.print(" / ");
         }
         else
         {
            foundOper = false;
         }
      }
      return(foundOper);
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
   private void detParamType(
      int                              startIndex,
      int                              endIndex,
      boolean                          firstParam,
      boolean                          ifStatement)
   {
      boolean									foundSomething;
      int                              currIndex;
      int                              done;
      Integer                          tstKey;
      int                              type;
      int                              tmpInt;
      
      currIndex = startIndex;
      while (currIndex < endIndex)
      {
      	foundSomething = false;
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
	         	GlobInfo.fileRulesClass.print("(");
	            detParamType(currIndex + 1, done, true, ifStatement);
	            currIndex = done + 1;
	         	GlobInfo.fileRulesClass.print(")");
	         	firstParam = false;
	         	foundSomething = true;
	         }
	      }
	      if (firstParam && !foundSomething)
	      {
	         if (ifStatement)
	         {
	         	/* Special if statement checks */
	         	foundSomething = true;
	            if (allTokens[currIndex].equals("EXPIRED"))
	            {
	               currIndex++;
	               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
	               if (tstKey == null)
	               {
	                  /* I'm flamoozled.  I have no idea what is going on */
	                  GlobInfo.hostCtl.printMsg("EXPIRED: Parse symbol fail " + allTokens[currIndex] + ".");
	                  GlobInfo.parseFail = true;
	                  state = PCHAIN_ERROR;
	               }
	               else
	               {
	                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
	                  if (type != ParseRules.SYMB_TIMER)
	                  {
	                     GlobInfo.hostCtl.printMsg("EXPIRED: Only timer symbols allowed " + allTokens[currIndex] + ".");
	                     GlobInfo.parseFail = true;
	                     state = PCHAIN_ERROR;
	                  }
	                  else
	                  {
	                     /* Calculate the bit position of the LED */
	   	            	GlobInfo.fileRulesClass.printf("GlobInfo.tmrClass.expTmr & ConstClass.%s",
	                       	allTokens[currIndex].toUpperCase());
	   	            	GlobInfo.fileRulesClass.println("");
	   	            }
	               }
	               currIndex++;
	               if (currIndex != endIndex)
	               {
	                  GlobInfo.hostCtl.printMsg("EXPIRED: Extra information in statement.");
	                  GlobInfo.parseFail = true;
	                  state = PCHAIN_ERROR;
	               }
	            }
	            else if (allTokens[currIndex].equals("MODE"))
	            {
	            	/* Next symbol should be == */
	            	if (allTokens[currIndex + 1].equals("=="))
	            	{
		            	GlobInfo.fileRulesClass.printf("mode == ConstClass.%s", allTokens[currIndex].toUpperCase());
		               currIndex += 3;
	            	}
	            	else
	            	{
	                  GlobInfo.hostCtl.printMsg("MODE: only support == match for mode");
	                  GlobInfo.parseFail = true;
	                  state = PCHAIN_ERROR;
		            }
	            }
	            else
	            {
		         	foundSomething = false;
	            }
	         }
	         else
	         {
	            /* Special objects that can only be found as the first parameter */
	         	foundSomething = true;
	            if (allTokens[currIndex].equals("DISABLE_SOLENOIDS"))
	            {
	            	GlobInfo.fileRulesClass.print("StdFuncs.DisableSolenoids()");
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
	               if (allTokens[currIndex + 1].equals(","))
	               {
   	            	GlobInfo.fileRulesClass.print("StdFuncs.LedOn(");
	                  currIndex = currIndex + 2;
                     detParamType(currIndex, endIndex, false, false);
                     currIndex = endIndex;
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
	   	            	GlobInfo.fileRulesClass.printf("StdFuncs.Kick(%d, ConstClass.%s);",
	                       	((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8),
	                       	allTokens[currIndex].toUpperCase());
	   	            	GlobInfo.fileRulesClass.println("");
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
	   	            	GlobInfo.fileRulesClass.println("StdFuncs.StartTimer(ConstClass." +
	   	            		allTokens[currIndex].toUpperCase() + ");");
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
	               currIndex++;
	               if (currIndex != endIndex)
	               {
	                  GlobInfo.hostCtl.printMsg("PREDEF_ENABLE_SOLENOIDS: Extra information in statement.");
	                  GlobInfo.parseFail = true;
	                  state = PCHAIN_ERROR;
	               }
	               else
	               {
   	            	GlobInfo.fileRulesClass.println("StdFuncs.EnableSolenoids();");
	               }
	            }
	            else if (allTokens[currIndex].equals("TEXT"))
	            {
	               /* HRS */
	            	currIndex = endIndex;
	            }
	            else if (allTokens[currIndex].equals("SOUND"))
	            {
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
	   	            	GlobInfo.fileRulesClass.println("StdFuncs.PlaySound(ConstClass." +
	   	            		allTokens[currIndex].toUpperCase() + ");");
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
	               currIndex++;
	               
	               /* Check if this is an integer constant */
	               try
	               {
		               tmpInt = Integer.parseInt(allTokens[currIndex]);
	                  currIndex++;
	                  if (currIndex != endIndex)
	                  {
	                     GlobInfo.hostCtl.printMsg("WAIT: Extra information in statement.");
	                     GlobInfo.parseFail = true;
	                     state = PCHAIN_ERROR;
	                  }
	                  else
	                  {
	   	            	GlobInfo.fileRulesClass.printf("StdFuncs.Wait(%d);", tmpInt);
		   	            GlobInfo.fileRulesClass.println("");
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
	            	GlobInfo.fileRulesClass.print("StdFuncs.LedRotLeft(");
	               if (allTokens[currIndex + 1].equals(","))
	               {
	                  currIndex = currIndex + 2;
	                  tmpInt = currIndex;
	                  while ((!allTokens[tmpInt].equals(",")) && (tmpInt < endIndex))
	                  {
	                  	tmpInt++;
	                  }
	                  if (tmpInt == endIndex)
	                  {
                        GlobInfo.hostCtl.printMsg("LED_ROT_LEFT: Can't find variable to rotate");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
	                  }
	                  else
	                  {
	                     detParamType(currIndex, tmpInt, false, false);
	                     currIndex = tmpInt + 1;
	                     
                        /* Last part of the command should be a destination */
                     	GlobInfo.fileRulesClass.println(",");
                     	GlobInfo.fileRulesClass.printf("%" + ((GlobInfo.currIndent + 1) * 3) + "s", "");
                        detParamType(currIndex, endIndex, false, false);
                        currIndex = endIndex;
                     	GlobInfo.fileRulesClass.print(")");
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
	            	GlobInfo.fileRulesClass.print("StdFuncs.LedRotRight(");
	               if (allTokens[currIndex + 1].equals(","))
	               {
	                  currIndex = currIndex + 2;
	                  tmpInt = currIndex;
	                  while ((!allTokens[tmpInt].equals(",")) && (tmpInt < endIndex))
	                  {
	                  	tmpInt++;
	                  }
	                  if (tmpInt == endIndex)
	                  {
                        GlobInfo.hostCtl.printMsg("LED_ROT_RIGHT: Can't find variable to rotate");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
	                  }
	                  else
	                  {
	                     detParamType(currIndex, tmpInt, false, false);
	                     currIndex = tmpInt + 1;
	                     
                        /* Last part of the command should be a destination */
                     	GlobInfo.fileRulesClass.println(",");
                     	GlobInfo.fileRulesClass.printf("%" + ((GlobInfo.currIndent + 1) * 3) + "s", "");
                        detParamType(currIndex, endIndex, false, false);
                        currIndex = endIndex;
                     	GlobInfo.fileRulesClass.print(")");
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
	               if (allTokens[currIndex + 1].equals(","))
	               {
	                  currIndex = currIndex + 2;
                     detParamType(currIndex, endIndex, false, false);
                     currIndex = endIndex;
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
	               if (allTokens[currIndex + 1].equals(","))
	               {
	                  currIndex = currIndex + 2;
                     detParamType(currIndex, endIndex, false, false);
                     currIndex = endIndex;
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
	               if (allTokens[currIndex + 1].equals(","))
	               {
	                  currIndex = currIndex + 2;
                     detParamType(currIndex, endIndex, false, false);
                     currIndex = endIndex;
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
	               if (allTokens[currIndex + 1].equals("="))
	               {
	                  if (endIndex != currIndex + 3)
	                  {
	                     GlobInfo.hostCtl.printMsg("PCHAIN_PROC: " + currName + " extra info in set mode command");
	                     GlobInfo.parseFail = true;
	                     state = PCHAIN_ERROR;
	                  }
	                  else
	                  {
	                  	GlobInfo.fileRulesClass.printf("mode = ConstClass.%s", allTokens[currIndex + 2]);
	                  	currIndex += 3;
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
	            else if (allTokens[currIndex].equals("LED_SET"))
	            {
	               /* Rotate functions needs mask which is a constant, and a variable */
	            	GlobInfo.fileRulesClass.print("StdFuncs.LedSet(");
	               if (allTokens[currIndex + 1].equals(","))
	               {
	                  currIndex = currIndex + 2;
	                  tmpInt = currIndex;
	                  while ((!allTokens[tmpInt].equals(",")) && (tmpInt < endIndex))
	                  {
	                  	tmpInt++;
	                  }
	                  if (tmpInt == endIndex)
	                  {
                        GlobInfo.hostCtl.printMsg("LED_SET: Can't find to use for set");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
	                  }
	                  else
	                  {
	                     detParamType(currIndex, tmpInt, false, false);
	                     currIndex = tmpInt + 1;
	                     
                        /* Last part of the command should be a destination */
                     	GlobInfo.fileRulesClass.println(",");
                     	GlobInfo.fileRulesClass.printf("%" + ((GlobInfo.currIndent + 1) * 3) + "s", "");
                        detParamType(currIndex, endIndex, false, false);
                        currIndex = endIndex;
                     	GlobInfo.fileRulesClass.print(")");
	                  }
	               }
	               else
	               {
	                  GlobInfo.hostCtl.printMsg("LED_SET: " + currName + " has misformed command");
	                  GlobInfo.parseFail = true;
	                  state = PCHAIN_ERROR;
	               }
	            }
	            else if (allTokens[currIndex].equals("VIDEO"))
	            {
	               /* HRS */
	            	currIndex = endIndex;
	            }
	            else
	            {
		         	foundSomething = false;
	            }
	         }
	      }
	      else if (!firstParam && !foundSomething)
	      {
	         /* Check if the operation has already been filled out */
	         foundSomething = fillCompOper(allTokens[currIndex], ifStatement);
	         if (foundSomething)
	         {
	         	currIndex++;
	         }
	      }
	      if (!foundSomething)
	      {
            /* Check if this is an integer constant */
            try
            {
            	if (currIndex == 1139)
            	{
            		currIndex++;
            		currIndex--;
            	}
               tmpInt = Integer.parseInt(allTokens[currIndex]);
            	GlobInfo.fileRulesClass.print(allTokens[currIndex]);
               currIndex++;
               foundSomething = true;
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
   	         	foundSomething = true;
                  switch (type)
                  {
                     case ParseRules.SYMB_SOL_PIN:
                     {
                     	if (ifStatement)
                     	{
	                     	GlobInfo.fileRulesClass.printf("((GlobInfo.solClass.currInputs[%d] & ConstClass.%s) != 0)",
		                       	((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8),
		                       	allTokens[currIndex].toUpperCase());
                     	}
                     	else
                     	{
	                     	GlobInfo.fileRulesClass.printf("(GlobInfo.solClass.currInputs[%d] & ConstClass.%s)",
		                       	((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8),
		                       	allTokens[currIndex].toUpperCase());
                     	}
                        currIndex++;
                        break;
                     }
                     case ParseRules.SYMB_INP_PIN:
                     {
                     	GlobInfo.fileRulesClass.printf("((GlobInfo.inpCardClass.currInputs[%d] & ConstClass.%s) != 0)",
                     		((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 8),
                     		allTokens[currIndex].toUpperCase());
                        currIndex++;
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
	        	                     	GlobInfo.fileRulesClass.print("ConstClass." + allTokens[currIndex].toUpperCase());
                                       
                                 }
                              }
                              currIndex++;
                           }
                        }
                        break;
                     }
                     case ParseRules.SYMB_VAR:
                     {
                     	GlobInfo.fileRulesClass.printf("Variable[ConstClass.%s]",
                        	allTokens[currIndex].toUpperCase());
                        currIndex++;
                        if (currIndex < endIndex)
                        {
                           /* more parameters to process */
                           detParamType(currIndex, endIndex, false, ifStatement);
                           currIndex = endIndex + 1;
            	         	firstParam = false;
                        }
                        else
                        {
                           /* No more parameters */
                        }
                        break;
                     }
                     case ParseRules.SYMB_INDX_VAR:
                     {
                        /* Next symbol is either [ or =, if [ setting individual */
                        if (allTokens[currIndex + 1].equals("["))
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
                           	if (firstParam)
                           	{
                           		GlobInfo.fileRulesClass.printf("Variable[");
                           	}
                           	
                              /* An indexed variable requires its own ProcObj for extra params */
                           	GlobInfo.fileRulesClass.printf("ConstClass.%s + ",
                                 	allTokens[currIndex].toUpperCase());
                              
                              /* Find the variable that is used as the index */
                              detParamType(currIndex + 2, done, false, false);
                           	if (firstParam)
                           	{
                           		GlobInfo.fileRulesClass.printf("]");
                  	         	firstParam = false;
                           	}
                           }
                           currIndex = done + 1;
                        }
                        else if (allTokens[currIndex + 1].equals("="))
                        {
                     		GlobInfo.fileRulesClass.printf("for (int autoGenIndex = 0; autoGenIndex < %d; autoGenIndex++)",
                     			((tstKey.intValue() & ParseRules.SYMB_PARAM_MASK) >> 12));
                        	GlobInfo.fileRulesClass.println("");
                        	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     		GlobInfo.fileRulesClass.println("{");
                        	GlobInfo.fileRulesClass.printf("%" + ((GlobInfo.currIndent + 1) * 3) + "s", "");
                     		GlobInfo.fileRulesClass.printf("Variable[ConstClass.%s + autoGenIndex] = %s;",
                     			allTokens[currIndex].toUpperCase(), allTokens[currIndex + 2]);
                     		GlobInfo.fileRulesClass.println(";");
                        	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
                     		GlobInfo.fileRulesClass.println("}");
                        	currIndex += 3;
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
      	            	GlobInfo.fileRulesClass.printf("StdFuncs.CallPChain(ConstClass.%s)",
                          	allTokens[currIndex].toUpperCase());
                        currIndex++;
                        break;
                     }
                     case ParseRules.SYMB_TIMER:
                     {
                        break;
                     }
                     case ParseRules.SYMB_CONST:
                     {
                     	GlobInfo.fileRulesClass.printf("ConstClass.%s",
                           	allTokens[currIndex].toUpperCase());
                        currIndex++;
                        break;
                     }
                     default:
                     {
                        GlobInfo.hostCtl.printMsg("PARSE_PCHAIN: Unknown symbol type = " + type + ".");
                        GlobInfo.parseFail = true;
                        state = PCHAIN_ERROR;
         	         	foundSomething = false;
                        break;
                     }
                  }
               }
            }
         }
	      if (foundSomething)
	      {
	      	firstParam = false;
	      }
      }
   } /* end detParamType */
} /* End ParsePChain */
