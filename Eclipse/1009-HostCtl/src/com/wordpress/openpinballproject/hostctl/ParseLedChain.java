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
 * @file:   ParseLedChain.java
 * @author: Hugh Spahr
 * @date:   10/21/2013
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
 * Parse LED Chain Lists
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class ParseLedChain
{
   private static final int            MAX_LEDCHAIN_TOKENS        = 1024;
   
   private static final int            LEDCHAIN_NEED_OPEN_CURLY  	= 1;
   private static final int            LEDCHAIN_FIND_CLOSE_CURLY 	= 2;
   private static final int            LEDCHAIN_FINISH_PROC      	= 3;
   private static final int            LEDCHAIN_ERROR             = 4;
   private static final int            LEDCHAIN_DONE              = 5;

   private int                         state = LEDCHAIN_NEED_OPEN_CURLY;
   private String                      currName;
   private String[]                    allTokens;
   private int                         allTokenLen = 0;
   private int                         delimCnt = 0;
   private boolean							firstLedChain = true;

   /*
    * ===============================================================================
    * 
    * Name: ParseLedChain
    * 
    * ===============================================================================
    */
   /**
    * Parse Led Chain
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
   public ParseLedChain(
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
         case LEDCHAIN_NEED_OPEN_CURLY:
         {
            if (tokens[currToken].equals("{"))
            {
               state = LEDCHAIN_FIND_CLOSE_CURLY;
               allTokens = new String[MAX_LEDCHAIN_TOKENS];
               allTokenLen = tokens.length - currToken;
               if (allTokenLen < MAX_LEDCHAIN_TOKENS)
               {
                  System.arraycopy(tokens, currToken, allTokens, 0, allTokenLen);
                  
                  /* Count start and end curly braces and parenthesis */
                  done = countDelim("{", "}", 0, allTokenLen);
                  if (done != 0)
                  {
                     /* Trim extra tokens if necessary, drop last } since already used it */
                     state = LEDCHAIN_FINISH_PROC;
                     allTokenLen = done - 1;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LEDCHAIN_PROC: too many tokens");
                  GlobInfo.parseFail = true;
                  state = LEDCHAIN_ERROR;
               }
            }
            else
            {
               GlobInfo.hostCtl.printMsg("LEDCHAIN_PROC: needs curly brace");
               GlobInfo.parseFail = true;
               state = LEDCHAIN_ERROR;
            }
            break;
         }
         case LEDCHAIN_FIND_CLOSE_CURLY:
         {
            newLen = tokens.length - currToken;
            startInd = allTokenLen;
            if (startInd + newLen < MAX_LEDCHAIN_TOKENS)
            {
               System.arraycopy(tokens, currToken, allTokens, startInd, newLen);
               allTokenLen = startInd + newLen;
               
               /* Count start and end curly braces and parenthesis */
               done = countDelim("{", "}", startInd, allTokenLen);
               if (done != 0)
               {
                  /* Trim extra tokens if necessary, drop last } since already used it */
                  state = LEDCHAIN_FINISH_PROC;
                  allTokenLen = done;
               }
            }
            else
            {
               GlobInfo.hostCtl.printMsg("LEDCHAIN_PROC: too many tokens");
               GlobInfo.parseFail = true;
               state = LEDCHAIN_ERROR;
            }
            break;
         }
         case LEDCHAIN_FINISH_PROC:
         case LEDCHAIN_ERROR:
         {
            break;
         }
         case LEDCHAIN_DONE:
         {
            GlobInfo.hostCtl.printMsg("LEDCHAIN_PROC: Extra info.");
            GlobInfo.parseFail = true;
            state = LEDCHAIN_ERROR;
            break;
         }
      }
      if (state == LEDCHAIN_FINISH_PROC)
      {
         /* Whole PChain list has been tokenized.  Now separate into individual PChain lists */
         startInd = 1;
         while (state == LEDCHAIN_FINISH_PROC)
         {
            endInd = findNextLedchain(startInd);
            startInd = endInd + 1;
            if (startInd == allTokenLen)
            {
               state = LEDCHAIN_DONE;
            	if (firstLedChain == false)
            	{
            		/* End the Gencode_Create_Led_Chains function */
               	GlobInfo.fileRulesClass.println("   }");
            	}
            }
            else if (startInd > allTokenLen)
            {
               state = LEDCHAIN_ERROR;
            }
         }
      }
      
      /* Clean up memory */
      if ((state == LEDCHAIN_ERROR) || (state == LEDCHAIN_DONE))
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
    * Name: findNextLedchain
    * 
    * ===============================================================================
    */
   /**
    * Find the next Led chain
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
   private int findNextLedchain(
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
            GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: " + currName + " needs ending curly brace");
            GlobInfo.parseFail = true;
            state = LEDCHAIN_ERROR;
         }
         else
         {
            /* Check if this is a duplicate value */
            endIndex = done;
            tstKey = ParseRules.hmSymbol.get(currName);
            if (tstKey == null)
            {
            	/* If this is the first LED chain, create the function */
            	if (firstLedChain)
            	{
               	GlobInfo.fileRulesClass.println("   public void Gencode_Create_Led_Chains()");
               	GlobInfo.fileRulesClass.println("   {");
               	firstLedChain = false;
            	}
               ParseRules.hmSymbol.put(currName,
                  ParseRules.SYMB_LED_CHAIN | GlobInfo.numLedChain);
            	GlobInfo.fileConstClass.println("   public static final int             " +
                  String.format("%-27s= %2d;", currName.toUpperCase(), GlobInfo.numLedChain));
               GlobInfo.numLedChain++;

            	GlobInfo.fileRulesClass.println("      StdFuncs.CreateLedChain(ConstClass." + currName.toUpperCase() + ",");
            	GlobInfo.currIndent = 3;
               mungeLedChain(startIndex + 2, endIndex);
            }
            else
            {
               GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Duplicate input names.");
               GlobInfo.parseFail = true;
               state = LEDCHAIN_ERROR;
            }
         }
      }
      else
      {
         GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: " + currName + " needs starting curly brace");
         GlobInfo.parseFail = true;
         state = LEDCHAIN_ERROR;
      }
      return (endIndex);
   } /* end findNextLedchain */

   /*
    * ===============================================================================
    * 
    * Name: mungeLedChain
    * 
    * ===============================================================================
    */
   /**
    * Munge Led chain
    * 
    * Call munge Led chain to process an LED chain list.
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
   private void mungeLedChain(
      int                              startIndex,
      int                              endIndex)
   {
      int                              currIndex;
      Integer                          tstKey;
      int                              type = 0;
      String									cmdStr = new String("");
      String									ledStr = new String("");
      boolean									mask = true;
      
      currIndex = startIndex;
      while (currIndex < endIndex)
      {
      	/* Grab the mask, or the list of LEDs to change */
      	if (ledStr.length() != 0)
      	{
      		ledStr = new String(ledStr + ", ");
      	}
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	while ((currIndex < endIndex) && !allTokens[currIndex].equals(","))
      	{
      		/* Ignore open and close parenthesis since forming mask */
      		if (allTokens[currIndex].equals("(") || allTokens[currIndex].equals(")"))
				{
				}
      		else if (allTokens[currIndex].equals("+"))
      		{
      			if (mask)
      			{
      				GlobInfo.fileRulesClass.print(" + ");
      			}
      			else
      			{
            		ledStr = new String(ledStr + " + ");
      			}
      		}
      		else if (allTokens[currIndex].equals("|"))
      		{
      			if (mask)
      			{
         			GlobInfo.fileRulesClass.print(" | ");
      			}
      			else
      			{
            		ledStr = new String(ledStr + " | ");
      			}
      		}
      		else if (allTokens[currIndex].equals(","))
      		{
      		}
      		else if (allTokens[currIndex].equals("0"))
      		{
      			if (mask)
      			{
         			GlobInfo.fileRulesClass.print("0");
      			}
      			else
      			{
            		ledStr = new String(ledStr + "0");
      			}
      		}
      		else
      		{
      			/* Only other possibility is a LED bit */
               tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
               if (tstKey == null)
               {
                  /* I'm flamoozled.  I have no idea what is going on */
                  GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Unknown symbol " + allTokens[currIndex] + ".");
                  GlobInfo.parseFail = true;
                  currIndex = endIndex;
                  state = LEDCHAIN_ERROR;
               }
               else
               {
                  type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
               	if (type != ParseRules.SYMB_LED_PIN)
               	{
                     GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Mask should only contain LEDs. " + allTokens[currIndex]);
                     GlobInfo.parseFail = true;
                     currIndex = endIndex;
                     state = LEDCHAIN_ERROR;
               	}
               	else
               	{
            			if (mask)
            			{
                       	GlobInfo.fileRulesClass.print("ConstClass." + allTokens[currIndex].toUpperCase());
            			}
            			else
            			{
                  		ledStr = new String(ledStr + "ConstClass." + allTokens[currIndex].toUpperCase());
            			}
               	}
               }
      		}
   			currIndex++;
      	}
      	/* Next token, after the ',' is going to be a command */
         if ((currIndex < endIndex) && allTokens[currIndex].equals(",") && !mask)
         {
      		GlobInfo.fileRulesClass.println(",");
      		currIndex++;
      		if (allTokens[currIndex].equals("WAIT"))
      		{
      			/* Next token must be the number of milliseconds to wait */
               try
               {
               	type = Integer.parseInt(allTokens[currIndex + 1]);
	               if (allTokens[currIndex + 2].equals(","))
            		{
	               	if (cmdStr.length() == 0)
	               	{
	               		cmdStr = new String("StdFuncs.CHAINCMD_WAIT | " + allTokens[currIndex + 1]);
	               	}
	               	else
	               	{
	               		cmdStr = new String(cmdStr + ", StdFuncs.CHAINCMD_WAIT | " + allTokens[currIndex + 1]);
	               	}
	               	currIndex += 3;
            		}
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Extra information in WAIT statement in " + currName);
                     GlobInfo.parseFail = true;
                     currIndex = endIndex;
                     state = LEDCHAIN_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Only integers allowed " + currName);
                  GlobInfo.parseFail = true;
                  currIndex = endIndex;
                  state = LEDCHAIN_ERROR;
               }
      		}
      		else if ((allTokens[currIndex].equals("REPEAT")) || (allTokens[currIndex].equals("END_CHAIN")))
      		{
      			/* This should be the end of the chain */
      			currIndex++;
      			if (currIndex == endIndex)
      			{
               	if (cmdStr == null)
               	{
                     GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: No commands in LED chain " + currName);
	                  GlobInfo.parseFail = true;
                     currIndex = endIndex;
	                  state = LEDCHAIN_ERROR;
               	}
               	else
               	{
               		cmdStr = new String(cmdStr + ", StdFuncs.CHAINCMD_" + allTokens[currIndex - 1]);
               		ledStr = new String(ledStr + ", 0");
               	}
      			}
      			else
      			{
                  GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Extra information in LED chain " + currName);
                  GlobInfo.parseFail = true;
                  currIndex = endIndex;
                  state = LEDCHAIN_ERROR;
      			}
      		}
      		else
      		{
               GlobInfo.hostCtl.printMsg("LEDCHAIN_ERROR: Unknown command " + allTokens[currIndex]);
               GlobInfo.parseFail = true;
               currIndex = endIndex;
               state = LEDCHAIN_ERROR;
      		}
         }
         if (mask)
         {
         	mask = false;
         	currIndex++;
         }
      }
      if (state != LEDCHAIN_ERROR)
      {
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + ledStr + "},   /* LED set array */");
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + cmdStr + "});   /* Command array */");
      }
   } /* end mungeLedChain */
} /* End ParseLedChain */
