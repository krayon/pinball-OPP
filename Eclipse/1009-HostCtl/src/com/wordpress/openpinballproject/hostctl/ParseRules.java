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
 * @file:   ParseRules.java
 * @author: Hugh Spahr
 * @date:   2/06/2013
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
 * Parse a rules file.
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class ParseRules
{
   public boolean                parseFail               = false;
   
   public static final int       STATE_IDLE              = 0;
   public static final int       STATE_NAME_SOL          = 1;
   public static final int       STATE_NAME_INP          = 2;
   public static final int       STATE_NAME_LED          = 3;
   public static final int       STATE_NAME_VAR          = 4;
   public static final int       STATE_NAME_IND_VAR      = 5;
   public static final int       STATE_NAME_MODE         = 6;
   public static final int       STATE_NAME_PROC_CHAIN   = 7;
   public static final int       STATE_NAME_LED_CHAIN    = 8;
   public static final int       STATE_NAME_SOUND        = 9;
   public static final int       STATE_NAME_VIDEO        = 10;
   private int                   state                   = STATE_IDLE;

   public static final int       SYMB_SOL_PIN            = 0x00000000;
   public static final int       SYMB_INP_PIN            = 0x00010000;
   public static final int       SYMB_LED_PIN            = 0x00020000;
   public static final int       SYMB_VAR                = 0x00030000;
   public static final int       SYMB_INDX_VAR           = 0x00040000;
   public static final int       SYMB_SND                = 0x00050000;
   public static final int       SYMB_BIG_VID            = 0x00060000;
   public static final int       SYMB_LITTLE_VID         = 0x00070000;

   public static int             allocInd = 0;
   public static HashMap<String, Integer>    hmSymbol;
   
   
   private static final Map<String, Integer> RSVD_STATE_MAP = (Map<String, Integer>) createMap();

   private static Map<String, Integer> createMap()
   {
       Map<String, Integer> result = new HashMap<String, Integer>();
       result.put("SOLENOID_CARDS", STATE_NAME_SOL);
       result.put("INPUT_CARDS", STATE_NAME_INP);
       result.put("LED_CARDS", STATE_NAME_LED);
       result.put("VARIABLES", STATE_NAME_VAR);
       result.put("INDEXED_VARIABLES", STATE_NAME_IND_VAR);
       result.put("MODES", STATE_NAME_MODE);
       result.put("PROCESS_CHAINS", STATE_NAME_PROC_CHAIN);
       result.put("LED_CHAINS", STATE_NAME_LED_CHAIN);
       result.put("SOUND_CLIPS", STATE_NAME_SOUND);
       result.put("VIDEO_CLIPS", STATE_NAME_VIDEO);
       return Collections.unmodifiableMap(result);
   }
   
   /*
    * ===============================================================================
    * 
    * Name: ParseRules
    * 
    * ===============================================================================
    */
   /**
    * Parse rules file
    * 
    * Read the the rules file looking for reserved words.  Hand the information to
    * the appropriate sub-classes.
    * 
    * @param   rulesFile - name of the rules file 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   public ParseRules(
      String                           rulesFile)
   {
      int                              offset;
      boolean                          done;
      int                              lineNum = 0;
      String[]                         tokens;
      Integer                          temp;
      
      hmSymbol = new HashMap<String, Integer>();
      
      try
      {
         FileInputStream               fstream = new FileInputStream(rulesFile);
         DataInputStream               in = new DataInputStream(fstream);
         BufferedReader                br = new BufferedReader(new InputStreamReader(in));
         String                        strLine;
         
         try
         {
            while (((strLine = br.readLine()) != null) && !parseFail)
            {
               done = false;
               
               /* Remove everything after a '#' since it is a comment */
               offset = strLine.indexOf("#");
               if (offset != -1)
               {
                  strLine = strLine.substring(0, offset);
               }
               
               /* Guarantee spaces before and after () {} and [] for split */
               strLine = strLine.replaceAll("\\{", " \\{ ").replaceAll("\\}", " \\} ");
               strLine = strLine.replaceAll("\\[", " \\[ ").replaceAll("\\]", " \\] ");
               strLine = strLine.replaceAll("\\(", " \\( ").replaceAll("\\)", " \\) ");
            
               /* Make sure that some tokens exist */
               tokens = strLine.trim().split("\\s+");
               if (tokens[0].equals(""))
               {
                  done = true;
               }
               
               if (!done)
               {
                  if (state == STATE_IDLE)
                  {
                     /* Look for keyword to for section */
                     temp = RSVD_STATE_MAP.get(tokens[0]);
                     if (temp == null)
                     {
                        /* Could not find dictionary entry */
                        done = true;
                     }
                     else
                     {
                        state = temp.intValue();
                        processTokens(tokens);
                     }
                  }
                  else
                  {
                     processTokens(tokens);
                  }
               }
               // Print the content on the console
               lineNum++;
            }
            in.close();
         }
         catch (IOException e)
         {
            GlobInfo.hostCtl.printMsg("I/O exception reading rules file.");
            GlobInfo.parseRules.parseFail = true;
         }
      }
      catch (FileNotFoundException e)
      {
         GlobInfo.hostCtl.printMsg("Rules file not found.");
         GlobInfo.parseRules.parseFail = true;
      }
   } /* end ParseRules */
   
   /*
    * ===============================================================================
    * 
    * Name: processTokens
    * 
    * ===============================================================================
    */
   /**
    * Process tokens (fields) from rules file
    * 
    * Hand tokens to appropriate classes for processing.  This would be an unglorified
    * jump table, but alas, no jump tables in java.  (Grrrr).
    * 
    * @param   state - current processing state
    * @param   tokens - information to be processed 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private void processTokens(
      String[]                         tokens)
   {
      switch (state)
      {
         case STATE_NAME_SOL:
         {
            if (GlobInfo.solClass == null)
            {
               GlobInfo.solClass = new SolenoidClass(tokens);
            }
            else
            {
               if (GlobInfo.solClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing SOLENOID_CARDS.");
                  state = STATE_IDLE;
               }
            }
            break;
         }
         case STATE_NAME_INP:
         {
            if (GlobInfo.inpCardClass == null)
            {
               GlobInfo.inpCardClass = new InpCardClass(tokens);
            }
            else
            {
               if (GlobInfo.inpCardClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing INPUT_CARDS.");
                  state = STATE_IDLE;
               }
            }
            break;
         }
         case STATE_NAME_LED:
         {
            if (GlobInfo.ledClass == null)
            {
               GlobInfo.ledClass = new LedClass(tokens);
            }
            else
            {
               if (GlobInfo.ledClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing LED_CARDS.");
                  state = STATE_IDLE;
               }
            }
            break;
         }
         case STATE_NAME_VAR:
         {
            if (GlobInfo.varClass == null)
            {
               GlobInfo.varClass = new VarClass(tokens);
            }
            else
            {
               if (GlobInfo.varClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing VARIABLES.");
                  state = STATE_IDLE;
               }
            }
            break;
         }
         case STATE_NAME_IND_VAR:
         {
            /* HRS
            if (GlobInfo.indxVarClass == null)
            {
               GlobInfo.indxVarClass = new IndxVarClass(tokens);
            }
            else
            {
               if (GlobInfo.indxVarClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing INDEXED_VARIABLES.");
                  state = STATE_IDLE;
               }
            } */
            state = STATE_IDLE;
            break;
         }
         case STATE_NAME_MODE:
         {
            break;
         }
         case STATE_NAME_PROC_CHAIN:
         {
            break;
         }
         case STATE_NAME_LED_CHAIN:
         {
            break;
         }
         case STATE_NAME_SOUND:
         {
            if (GlobInfo.sndClass == null)
            {
               GlobInfo.sndClass = new SoundClass(tokens);
            }
            else
            {
               if (GlobInfo.sndClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing SOUND_CLIPS.");
                  state = STATE_IDLE;
               }
            }
            break;
         }
         case STATE_NAME_VIDEO:
         {
            if (GlobInfo.vidClass == null)
            {
               GlobInfo.vidClass = new VideoClass(tokens);
            }
            else
            {
               if (GlobInfo.vidClass.addEntries(0, tokens))
               {
                  GlobInfo.hostCtl.printMsg("Finished processing VIDEO_CLIPS.");
                  state = STATE_IDLE;
               }
            }
            break;
         }
      }
   } /* end processTokens */
} /* End ParseRules */
