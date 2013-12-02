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
 * @file:   ParseModes.java
 * @author: Hugh Spahr
 * @date:   10/22/2013
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
 * Parse Mode Lists
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class ParseModes
{
   private static final int            MAX_MODES_TOKENS           = 1024;
   
   private static final int            MODES_NEED_OPEN_CURLY  		= 1;
   private static final int            MODES_FIND_CLOSE_CURLY 		= 2;
   private static final int            MODES_FINISH_PROC      		= 3;
   private static final int            MODES_ERROR             	= 4;
   private static final int            MODES_DONE              	= 5;

   private int                         state = MODES_NEED_OPEN_CURLY;
   private String                      currName;
   private String[]                    allTokens;
   private int                         allTokenLen = 0;
   private int                         delimCnt = 0;
   private boolean							firstLedChain = true;

   /*
    * ===============================================================================
    * 
    * Name: ParseModes
    * 
    * ===============================================================================
    */
   /**
    * Parse modes
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
   public ParseModes(
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
         case MODES_NEED_OPEN_CURLY:
         {
            if (tokens[currToken].equals("{"))
            {
               state = MODES_FIND_CLOSE_CURLY;
               allTokens = new String[MAX_MODES_TOKENS];
               allTokenLen = tokens.length - currToken;
               if (allTokenLen < MAX_MODES_TOKENS)
               {
                  System.arraycopy(tokens, currToken, allTokens, 0, allTokenLen);
                  
                  /* Count start and end curly braces and parenthesis */
                  done = countDelim("{", "}", 0, allTokenLen);
                  if (done != 0)
                  {
                     /* Trim extra tokens if necessary, drop last } since already used it */
                     state = MODES_FINISH_PROC;
                     allTokenLen = done - 1;
                  }
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("MODES_PROC: too many tokens");
                  GlobInfo.parseFail = true;
                  state = MODES_ERROR;
               }
            }
            else
            {
               GlobInfo.hostCtl.printMsg("MODES_PROC: needs curly brace");
               GlobInfo.parseFail = true;
               state = MODES_ERROR;
            }
            break;
         }
         case MODES_FIND_CLOSE_CURLY:
         {
            newLen = tokens.length - currToken;
            startInd = allTokenLen;
            if (startInd + newLen < MAX_MODES_TOKENS)
            {
               System.arraycopy(tokens, currToken, allTokens, startInd, newLen);
               allTokenLen = startInd + newLen;
               
               /* Count start and end curly braces and parenthesis */
               done = countDelim("{", "}", startInd, allTokenLen);
               if (done != 0)
               {
                  /* Trim extra tokens if necessary, drop last } since already used it */
                  state = MODES_FINISH_PROC;
                  allTokenLen = done;
               }
            }
            else
            {
               GlobInfo.hostCtl.printMsg("MODES_PROC: too many tokens");
               GlobInfo.parseFail = true;
               state = MODES_ERROR;
            }
            break;
         }
         case MODES_FINISH_PROC:
         case MODES_ERROR:
         {
            break;
         }
         case MODES_DONE:
         {
            GlobInfo.hostCtl.printMsg("MODES_PROC: Extra info.");
            GlobInfo.parseFail = true;
            state = MODES_ERROR;
            break;
         }
      }
      if (state == MODES_FINISH_PROC)
      {
         /* Whole PChain list has been tokenized.  Now separate into individual PChain lists */
         startInd = 1;
         while (state == MODES_FINISH_PROC)
         {
            endInd = findNextMode(startInd);
            startInd = endInd + 1;
            if (startInd == allTokenLen)
            {
               state = MODES_DONE;
            	if (firstLedChain == false)
            	{
            		/* End the Gencode_Create_Led_Chains function */
               	GlobInfo.fileRulesClass.println("   }");
            	}
            }
            else if (startInd > allTokenLen)
            {
               state = MODES_ERROR;
            }
         }
      }
      
      /* Clean up memory */
      if ((state == MODES_ERROR) || (state == MODES_DONE))
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
    * Name: findNextMode
    * 
    * ===============================================================================
    */
   /**
    * Find the next mode
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
   private int findNextMode(
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
            GlobInfo.hostCtl.printMsg("MODES_ERROR: " + currName + " needs ending curly brace");
            GlobInfo.parseFail = true;
            state = MODES_ERROR;
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
               	GlobInfo.fileRulesClass.println("   public void Gencode_Create_Modes()");
               	GlobInfo.fileRulesClass.println("   {");
               	firstLedChain = false;
            	}
               ParseRules.hmSymbol.put(currName,
                  ParseRules.SYMB_MODE | GlobInfo.numModes);
            	GlobInfo.fileConstClass.println("   public static final int             " +
                  String.format("%-27s= %2d;", currName.toUpperCase(), GlobInfo.numModes));
               GlobInfo.numModes++;
            	mungeModes(startIndex + 2, endIndex);
            }
            else
            {
               GlobInfo.hostCtl.printMsg("MODES_ERROR: Duplicate input names.");
               GlobInfo.parseFail = true;
               state = MODES_ERROR;
            }
         }
      }
      else
      {
         GlobInfo.hostCtl.printMsg("MODES_ERROR: " + currName + " needs starting curly brace");
         GlobInfo.parseFail = true;
         state = MODES_ERROR;
      }
      return (endIndex);
   } /* end findNextLedchain */

   /*
    * ===============================================================================
    * 
    * Name: mungeModes
    * 
    * ===============================================================================
    */
   /**
    * Munge modes
    * 
    * Call munge modes to process an mode list.
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
   private void mungeModes(
      int                              startIndex,
      int                              endIndex)
   {
      int                              currIndex;
      int										done;
      String									initStr = null;
      String									procStr = null;
      String									videoStr = null;
      String									audioStr = null;
      String									ledStr = null;
      String									scoreStr = null;
      
   	/* First group is the init chain */
      currIndex = startIndex;
		if (allTokens[currIndex].equals("("))
		{
         done = countDelim("(", ")", currIndex, allTokenLen);
         if (done != 0)
         {
         	initStr = modesMungeInit(currIndex + 1, done);
         	if (initStr != null)
         	{
         		currIndex = done + 1;
         	}
         	else
         	{
         		currIndex = endIndex;
         	}
         }
         else
         {
            GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find closing parenthesis in init group");
            GlobInfo.parseFail = true;
            currIndex = endIndex;
            state = MODES_ERROR;
         }
		}
		else
		{
         GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find opening parenthesis in init group");
         GlobInfo.parseFail = true;
         currIndex = endIndex;
         state = MODES_ERROR;
		}

		/* Second group is the proc chain */
		if ((currIndex < endIndex) && (allTokens[currIndex].equals("(")))
		{
         done = countDelim("(", ")", currIndex, allTokenLen);
         if (done != 0)
         {
         	procStr = modesMungeProc(currIndex + 1, done);
         	if (procStr != null)
         	{
         		currIndex = done + 1;
         	}
         	else
         	{
         		currIndex = endIndex;
         	}
         }
         else
         {
            GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find closing parenthesis in proc group");
            GlobInfo.parseFail = true;
            currIndex = endIndex;
            state = MODES_ERROR;
         }
		}
		else
		{
         GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find opening parenthesis in proc group");
         GlobInfo.parseFail = true;
         currIndex = endIndex;
         state = MODES_ERROR;
		}

		/* Third group is the video chain */
		if ((currIndex < endIndex) && (allTokens[currIndex].equals("(")))
		{
         done = countDelim("(", ")", currIndex, allTokenLen);
         if (done != 0)
         {
         	videoStr = modesMungeVideo(currIndex + 1, done);
         	if (videoStr != null)
         	{
         		currIndex = done + 1;
         	}
         	else
         	{
         		currIndex = endIndex;
         	}
         }
         else
         {
            GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find closing parenthesis in video group");
            GlobInfo.parseFail = true;
            currIndex = endIndex;
            state = MODES_ERROR;
         }
		}
		else
		{
         GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find opening parenthesis in video group");
         GlobInfo.parseFail = true;
         currIndex = endIndex;
         state = MODES_ERROR;
		}
		
		/* Fourth group is the audio chain */
		if ((currIndex < endIndex) && (allTokens[currIndex].equals("(")))
		{
         done = countDelim("(", ")", currIndex, allTokenLen);
         if (done != 0)
         {
         	audioStr = modesMungeAudio(currIndex + 1, done);
         	if (audioStr != null)
         	{
         		currIndex = done + 1;
         	}
         	else
         	{
         		currIndex = endIndex;
         	}
         }
         else
         {
            GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find closing parenthesis in audio group");
            GlobInfo.parseFail = true;
            currIndex = endIndex;
            state = MODES_ERROR;
         }
		}
		else
		{
         GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find opening parenthesis in audio group");
         GlobInfo.parseFail = true;
         currIndex = endIndex;
         state = MODES_ERROR;
		}
		
		/* Fifth group is the LED chain */
		if ((currIndex < endIndex) && (allTokens[currIndex].equals("(")))
		{
         done = countDelim("(", ")", currIndex, allTokenLen);
         if (done != 0)
         {
         	ledStr = modesMungeLed(currIndex + 1, done);
         	if (ledStr != null)
         	{
         		currIndex = done + 1;
         	}
         	else
         	{
         		currIndex = endIndex;
         	}
         }
         else
         {
            GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find closing parenthesis in LED group");
            GlobInfo.parseFail = true;
            currIndex = endIndex;
            state = MODES_ERROR;
         }
		}
		else
		{
         GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find opening parenthesis in LED group");
         GlobInfo.parseFail = true;
         currIndex = endIndex;
         state = MODES_ERROR;
		}
		
		/* Sixth group is the scoring */
		if ((currIndex < endIndex) && (allTokens[currIndex].equals("(")))
		{
         done = countDelim("(", ")", currIndex, allTokenLen);
         if (done != 0)
         {
         	scoreStr = modesMungeScoring(currIndex + 1, done);
         	if (scoreStr != null)
         	{
         		currIndex = done + 1;
         	}
         	else
         	{
         		currIndex = endIndex;
         	}
         }
         else
         {
            GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find closing parenthesis in scoring group");
            GlobInfo.parseFail = true;
            currIndex = endIndex;
            state = MODES_ERROR;
         }
		}
		else
		{
         GlobInfo.hostCtl.printMsg("MODES_ERROR: Can't find opening parenthesis in scoring group");
         GlobInfo.parseFail = true;
         currIndex = endIndex;
         state = MODES_ERROR;
		}
		
		/* Write the rules file */
		if (initStr != null)
		{
      	GlobInfo.fileRulesClass.println("      StdFuncs.CreateMode(ConstClass." + currName.toUpperCase() + ",");
      	GlobInfo.currIndent = 3;
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + initStr + "},");
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + procStr + "},");
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + videoStr + "},");
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + audioStr + "},");
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println("new int[] {" + ledStr + "},");
      	GlobInfo.fileRulesClass.printf("%" + (GlobInfo.currIndent * 3) + "s", "");
      	GlobInfo.fileRulesClass.println(scoreStr + ");");
		}
   } /* end mungeModes */

   /*
    * ===============================================================================
    * 
    * Name: modesMungeInit
    * 
    * ===============================================================================
    */
   /**
    * Munge init chains
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  String of constant array
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private String modesMungeInit(
      int                              startIndex,
      int                              endIndex)
   {
		int										currIndex;
      Integer                          tstKey;
      int                              type;
      String									outputStr;

		currIndex = startIndex;
		outputStr = new String("");
		while (currIndex < endIndex)
   	{
      	/* Check to see if this is a processing chain */
         tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
         if (tstKey == null)
         {
            /* Don't know what this symbol is. */
            GlobInfo.hostCtl.printMsg("MODES_PROC:  not expecting " + allTokens[currIndex] + " symbol");
            GlobInfo.parseFail = true;
            state = MODES_ERROR;
            currIndex = endIndex;
         }
         else
         {
            type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
            if (type != ParseRules.SYMB_PCHAIN)
            {
               GlobInfo.hostCtl.printMsg("MODES_PROC: Only pchain symbols allowed " + allTokens[currIndex] + ".");
               GlobInfo.parseFail = true;
               state = MODES_ERROR;
               currIndex = endIndex;
            }
            else
            {
            	/* Write name to output string */
            	if (currIndex + 1 < endIndex)
      			{
            		if (allTokens[currIndex + 1].equals(","))
            		{
            			outputStr = new String(outputStr + "ConstClass." + allTokens[currIndex].toUpperCase() + ", ");
            			currIndex += 2;
            		}
            		else
            		{
                     GlobInfo.hostCtl.printMsg("MODES_PROC: Poorly formed init chain, not expecting " + allTokens[currIndex + 1] + ".");
                     GlobInfo.parseFail = true;
                     state = MODES_ERROR;
                     currIndex = endIndex;
            		}
      			}
            	else
            	{
         			outputStr = new String(outputStr + "ConstClass." + allTokens[currIndex].toUpperCase() + ", ");
         			currIndex++;
            	}
            }
         }
   	}
		
		/* Add terminating 0 */
		outputStr = new String(outputStr + "0");
		return(outputStr);
   } /* end modesMungeInit */

   /*
    * ===============================================================================
    * 
    * Name: modesMungeProc
    * 
    * ===============================================================================
    */
   /**
    * Munge proc chains
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  String of constant array
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private String modesMungeProc(
      int                              startIndex,
      int                              endIndex)
   {
		int										currIndex;
      Integer                          tstKey;
      int                              type;
      String									outputStr;

		currIndex = startIndex;
		outputStr = new String("");
		while (currIndex < endIndex)
   	{
      	/* Check to see if this is a processing chain */
         tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
         if (tstKey == null)
         {
            /* Don't know what this symbol is. */
            GlobInfo.hostCtl.printMsg("MODES_PROC:  not expecting " + allTokens[currIndex] + " symbol");
            GlobInfo.parseFail = true;
            state = MODES_ERROR;
            currIndex = endIndex;
         }
         else
         {
            type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
            if (type != ParseRules.SYMB_PCHAIN)
            {
               GlobInfo.hostCtl.printMsg("MODES_PROC: Only pchain symbols allowed " + allTokens[currIndex] + ".");
               GlobInfo.parseFail = true;
               state = MODES_ERROR;
               currIndex = endIndex;
            }
            else
            {
            	/* Write name to output string */
            	if (currIndex + 1 < endIndex)
      			{
            		if (allTokens[currIndex + 1].equals(","))
            		{
            			outputStr = new String(outputStr + "ConstClass." + allTokens[currIndex].toUpperCase() + ", ");
            			currIndex += 2;
            		}
            		else
            		{
                     GlobInfo.hostCtl.printMsg("MODES_PROC: Poorly formed proc chain, not expecting " + allTokens[currIndex + 1] + ".");
                     GlobInfo.parseFail = true;
                     state = MODES_ERROR;
                     currIndex = endIndex;
            		}
      			}
            	else
            	{
         			outputStr = new String(outputStr + "ConstClass." + allTokens[currIndex].toUpperCase() + ", ");
         			currIndex++;
            	}
            }
         }
   	}
		
		/* Add terminating 0 */
		outputStr = new String(outputStr + "0");
		return(outputStr);
   } /* end modesMungeProc */
   
   /*
    * ===============================================================================
    * 
    * Name: modesMungeVideo
    * 
    * ===============================================================================
    */
   /**
    * Munge video chains
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  String of constant array
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private String modesMungeVideo(
      int                              startIndex,
      int                              endIndex)
   {
		int										currIndex;
      Integer                          tstKey;
      int                              type;
      String									outputStr;

		currIndex = startIndex;
		outputStr = new String("");
		while (currIndex < endIndex)
   	{
			if (allTokens[currIndex].equals("REPEAT"))
			{
				outputStr = new String("StdFuncs.CHAINCMD_REPEAT, ");
				currIndex++;
				if (currIndex < endIndex)
				{
	            /* Should not have any more symbols after the REPEAT. */
	            GlobInfo.hostCtl.printMsg("MODES_PROC:  No symbols after REPEAT cmd");
	            GlobInfo.parseFail = true;
	            state = MODES_ERROR;
	            currIndex = endIndex;
				}
			}
			else if (allTokens[currIndex].equals("WAIT"))
			{
            try
            {
            	type = Integer.parseInt(allTokens[currIndex + 1]);
               if (allTokens[currIndex + 2].equals(","))
         		{
            		outputStr = new String(outputStr + ", StdFuncs.CHAINCMD_WAIT | " + allTokens[currIndex + 1]);
               	currIndex += 3;
         		}
               else
               {
                  GlobInfo.hostCtl.printMsg("MODES_PROC: Extra information in WAIT statement: " + allTokens[currIndex + 2]);
                  GlobInfo.parseFail = true;
                  currIndex = endIndex;
                  state = MODES_ERROR;
               }
            }
            catch (NumberFormatException e)
            {
               GlobInfo.hostCtl.printMsg("MODES_PROC: Only integers allowed " + allTokens[currIndex + 1]);
               GlobInfo.parseFail = true;
               currIndex = endIndex;
               state = MODES_ERROR;
            }
			}
			else
			{
	      	/* Check to see if this is a processing chain */
	         tstKey = ParseRules.hmSymbol.get(allTokens[currIndex]);
	         if (tstKey == null)
	         {
	            /* Don't know what this symbol is. */
	            GlobInfo.hostCtl.printMsg("MODES_PROC:  not expecting " + allTokens[currIndex] + " symbol");
	            GlobInfo.parseFail = true;
	            state = MODES_ERROR;
	            currIndex = endIndex;
	         }
	         else
	         {
	            type = tstKey.intValue() & ParseRules.SYMB_TYPE_MASK;
	            if ((type != ParseRules.SYMB_BIG_VID) && (type != ParseRules.SYMB_LITTLE_VID))
	            {
	               GlobInfo.hostCtl.printMsg("MODES_PROC: Only video symbols allowed " + allTokens[currIndex] + ".");
	               GlobInfo.parseFail = true;
	               state = MODES_ERROR;
	               currIndex = endIndex;
	            }
	            else
	            {
	            	/* Write name to output string */
	            	if (currIndex + 1 < endIndex)
	      			{
	            		if (allTokens[currIndex + 1].equals(","))
	            		{
	            			outputStr = new String(outputStr + "ConstClass." + allTokens[currIndex].toUpperCase() + ", ");
	            			currIndex += 2;
	            		}
	            		else
	            		{
	                     GlobInfo.hostCtl.printMsg("MODES_PROC: Poorly formed proc chain, not expecting " + allTokens[currIndex + 1] + ".");
	                     GlobInfo.parseFail = true;
	                     state = MODES_ERROR;
	                     currIndex = endIndex;
	            		}
	      			}
	            	else
	            	{
	         			outputStr = new String(outputStr + "ConstClass." + allTokens[currIndex].toUpperCase() + ", ");
	            	}
	            }
	         }
	   	}
   	}
		
		/* Add terminating 0 */
		outputStr = new String(outputStr + "StdFuncs.CHAINCMD_END_LIST");
		return(outputStr);
   } /* end modesMungeVideo */

   /*
    * ===============================================================================
    * 
    * Name: modesMungeAudio
    * 
    * ===============================================================================
    */
   /**
    * Munge audio chains
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  String of constant array
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private String modesMungeAudio(
      int                              startIndex,
      int                              endIndex)
   {
   	return("");
   } /* end modesMungeAudio */

   /*
    * ===============================================================================
    * 
    * Name: modesMungeLed
    * 
    * ===============================================================================
    */
   /**
    * Munge LED chains
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  String of constant array
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private String modesMungeLed(
      int                              startIndex,
      int                              endIndex)
   {
   	return("");
   } /* end modesMungeLed */

   /*
    * ===============================================================================
    * 
    * Name: modesMungeScoring
    * 
    * ===============================================================================
    */
   /**
    * Munge Scoring chains
    * 
    * @param   startIndex - starting index
    * @param   endIndex - ending index
    * @return  String of constant array
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private String modesMungeScoring(
      int                              startIndex,
      int                              endIndex)
   {
   	return("");
   } /* end modesMungeScoring */
} /* End ParseModes */
