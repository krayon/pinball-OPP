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
 * @file:   SolenoidClass.java
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
 * Solenoid class
 *
 *===============================================================================
 */
package com.wordpress.openpinballproject.hostctl;

public class SolenoidClass
{
   private static final int            NUM_SOL_PER_CARD        = 8;
   private static final int            CFG_BYTES_PER_INP       = 3;
   private static final int            MAX_INIT_KICK           = 255;
   private static final int            INIT_KICK_OFFSET        = 1;
   private static final int            MAX_DUTY_CYCLE          = 15;
   private static final int            MAX_MIN_OFF_NUM         = 7;
   private static final int            MIN_OFF_SHIFT           = 4;
   private static final int            DUTY_MIN_OFF_OFFSET     = 2;
   
   private static final int            SOL_NEED_NUM_CARDS      = 0;
   private static final int            SOL_NEED_OPEN_CURLY     = 1;
   private static final int            SOL_PROC_SOL_NAME       = 2;
   private static final int            SOL_PROC_SOL_CARD       = 3;
   private static final int            SOL_PROC_SOL_PIN        = 4;
   private static final int            SOL_PROC_SOL_FLAGS      = 5;
   private static final int            SOL_PROC_NEED_FLAG      = 6;
   private static final int            SOL_PROC_NEED_SEP       = 7;
   private static final int            SOL_PROC_SOL_INIT_KICK  = 8;
   private static final int            SOL_PROC_SOL_DUTY_CYCLE = 9;
   private static final int            SOL_PROC_SOL_MIN_OFF    = 10;
   private static final int            SOL_DONE                = 11;
   private static final int            SOL_ERROR               = 12;

   private int                         numCards = 0;
   private int                         state = SOL_NEED_NUM_CARDS;
   private int[]                       cardCfgArr;
   public int[]                        currInputs;
   
   private String                      currName;
   private int                         currCard;
   private int                         currPin;
   
   /*
    * ===============================================================================
    * 
    * Name: SolenoidClass
    * 
    * ===============================================================================
    */
   /**
    * Solenoid class for solenoid cards
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
   public SolenoidClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword, second should be num cards  */
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end SolenoidClass */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create solenoid outputs
    * 
    * Take tokens and add entries to create solenoid outputs.  This class uses fields
    * to configure the outputs, and name each output for later lookups.
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
      int                              tmpVal;
      
      while (currToken < tokens.length)
      {
         switch (state)
         {
            case SOL_NEED_NUM_CARDS:
            {
               try
               {
                  numCards = Integer.parseInt(tokens[currToken]);
                  cardCfgArr = new int[numCards * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD];
                  currInputs = new int[numCards * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD];
                  state = SOL_NEED_OPEN_CURLY;
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: needs numCards as param.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = SOL_PROC_SOL_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: needs curly parenthesis.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_PROC_SOL_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = SOL_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = SOL_PROC_SOL_CARD;
               }
               break;
            }
            case SOL_PROC_SOL_CARD:
            {
               try
               {
                  /* Humans are one based, not zero based. */
                  currCard = Integer.parseInt(tokens[currToken]) - 1;
                  if (currCard < numCards)
                  {
                     state = SOL_PROC_SOL_PIN;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Card Num larger than numCards.");
                     GlobInfo.parseFail = true;
                     state = SOL_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Illegal Card Num.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_PROC_SOL_PIN:
            {
               try
               {
                  currPin = Integer.parseInt(tokens[currToken]) - 1;
                  if (currPin < NUM_SOL_PER_CARD)
                  {
                     state = SOL_PROC_SOL_FLAGS;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Pin Num > 8.");
                     GlobInfo.parseFail = true;
                     state = SOL_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Illegal Pin Num.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_PROC_SOL_FLAGS:
            {
               if (tokens[currToken].equals("0"))
               {
                  state = SOL_PROC_SOL_INIT_KICK;
               }
               else if (tokens[currToken].equals("("))
               {
                  state = SOL_PROC_NEED_FLAG;
               }
               else
               {
                  cardCfgArr[(currCard * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD) +
                     (currPin * CFG_BYTES_PER_INP)] |= convertFlagToHex(tokens[currToken]);
                  if (state == SOL_PROC_NEED_SEP)
                  {
                     state = SOL_PROC_SOL_INIT_KICK;
                  }
               }
               break;
            }
            case SOL_PROC_NEED_FLAG:
            {
               cardCfgArr[(currCard * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD) +
                  (currPin * CFG_BYTES_PER_INP)] |= convertFlagToHex(tokens[currToken]);
               break;
            }
            case SOL_PROC_NEED_SEP:
            {
               if (tokens[currToken].equals("|"))
               {
                  state = SOL_PROC_NEED_FLAG;
               }
               else if (tokens[currToken].equals(")"))
               {
                  state = SOL_PROC_SOL_INIT_KICK;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Unknown separator.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_PROC_SOL_INIT_KICK:
            {
               try
               {
                  tmpVal = Integer.parseInt(tokens[currToken]);
                  if ((tmpVal > 0) && (tmpVal <= MAX_INIT_KICK))
                  {
                     cardCfgArr[(currCard * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD) +
                        (currPin * CFG_BYTES_PER_INP) + INIT_KICK_OFFSET] = tmpVal;
                     state = SOL_PROC_SOL_DUTY_CYCLE;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Init kick must be 0 < initKick < 256.");
                     GlobInfo.parseFail = true;
                     state = SOL_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Illegal initial kick value.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_PROC_SOL_DUTY_CYCLE:
            {
               try
               {
                  tmpVal = Integer.parseInt(tokens[currToken]);
                  if ((tmpVal >= 0) && (tmpVal <= MAX_DUTY_CYCLE))
                  {
                     cardCfgArr[(currCard * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD) +
                        (currPin * CFG_BYTES_PER_INP) + DUTY_MIN_OFF_OFFSET] = tmpVal;
                     state = SOL_PROC_SOL_MIN_OFF;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Duty cycle must be 0 <= dutyCycle < 16.");
                     GlobInfo.parseFail = true;
                     state = SOL_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Illegal duty cycle value.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_PROC_SOL_MIN_OFF:
            {
               Integer                          tstKey;
               
               try
               {
                  tmpVal = Integer.parseInt(tokens[currToken]);
                  if ((tmpVal >= 0) && (tmpVal <= MAX_MIN_OFF_NUM))
                  {
                     cardCfgArr[(currCard * CFG_BYTES_PER_INP * NUM_SOL_PER_CARD) +
                        (currPin * CFG_BYTES_PER_INP) + DUTY_MIN_OFF_OFFSET] |= (tmpVal << MIN_OFF_SHIFT);
                     
                     /* Check if this is a duplicate value */
                     tstKey = ParseRules.hmSymbol.get(currName);
                     if (tstKey == null)
                     {
                        ParseRules.hmSymbol.put(currName,
                           ParseRules.SYMB_SOL_PIN | (currCard << 8) | currPin);
                        ParseRules.hmSymbol.put(currName.toUpperCase(),
                           ParseRules.SYMB_CONST | (currCard << 8) | currPin);
                     	GlobInfo.fileConstClass.println("   public static final int             " +
                        	String.format("%-27s= 0x%02x;", currName.toUpperCase(), 1 << currPin));
                        state = SOL_PROC_SOL_NAME;
                     }
                     else
                     {
                        GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Duplicate solenoid names.");
                        GlobInfo.parseFail = true;
                        state = SOL_ERROR;
                     }
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Min off must be 0 <= dutyCycle < 8.");
                     GlobInfo.parseFail = true;
                     state = SOL_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Illegal min off value.");
                  GlobInfo.parseFail = true;
                  state = SOL_ERROR;
               }
               break;
            }
            case SOL_DONE:
            {
               GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Extra info.");
               GlobInfo.parseFail = true;
               state = SOL_ERROR;
               break;
            }
            case SOL_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if ((state == SOL_ERROR) || (state == SOL_DONE))
      {
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
    * Name: convertFlagToHex
    * 
    * ===============================================================================
    */
   /**
    * Convert flags to serial interface hex values
    * 
    * Convert flag reserved words to hex values use during hardware configuration.
    * 
    * @param   inpStr - string containing flag 
    * @return  None
    * 
    * @pre None 
    * @note None
    * 
    * ===============================================================================
    */
   private int convertFlagToHex(
      String                           inpStr)
   {
      if (inpStr.equals("USE_SWITCH"))
      {
         state = SOL_PROC_NEED_SEP;
         return (SerIntf.SOLCFG_FLG_USE_SWITCH);
      }
      else if (inpStr.equals("AUTO_CLR"))
      {
         state = SOL_PROC_NEED_SEP;
         return (SerIntf.SOLCFG_FLG_AUTO_CLR);
      }
      else if (inpStr.equals("0"))
      {
         state = SOL_PROC_NEED_SEP;
         return (0);
      }
      else
      {
         GlobInfo.hostCtl.printMsg("SOLENOID_CARDS: Unknown flag.");
         GlobInfo.parseFail = true;
         state = SOL_DONE;
         return (0);
      }
   } /* end convertFlagToHex */
} /* End SolenoidClass */
