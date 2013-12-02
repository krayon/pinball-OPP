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
 * @file:   LedClass.java
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
 * LED Card class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class LedClass
{
   private static final int            NUM_LED_PER_CARD        = 8;

   private static final int            LED_NEED_NUM_CARDS      = 0;
   private static final int            LED_NEED_OPEN_CURLY     = 1;
   private static final int            LED_PROC_INP_NAME       = 2;
   private static final int            LED_PROC_INP_CARD       = 3;
   private static final int            LED_PROC_INP_PIN        = 4;
   private static final int            LED_DONE                = 5;
   private static final int            LED_ERROR               = 6;

   private int                         numCards = 0;
   private int                         state = LED_NEED_NUM_CARDS;
   
   private String                      currName;
   private int                         currCard;
   private int                         currPin;

   /*
    * ===============================================================================
    * 
    * Name: LedClass
    * 
    * ===============================================================================
    */
   /**
    * LED card class for LED cards
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
   public LedClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword, second should be num cards  */
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end LedClass */
   
   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create LED pins
    * 
    * Take tokens and add entries to create LED pins.  Each pin is stored in the
    * hashmap.
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
            case LED_NEED_NUM_CARDS:
            {
               try
               {
                  numCards = Integer.parseInt(tokens[currToken]);
                  state = LED_NEED_OPEN_CURLY;
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("LED_CARDS: needs numCards as param.");
                  GlobInfo.parseFail = true;
                  state = LED_ERROR;
               }
               break;
            }
            case LED_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = LED_PROC_INP_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("LED_CARDS: needs curly parenthesis.");
                  GlobInfo.parseFail = true;
                  state = LED_ERROR;
               }
               break;
            }
            case LED_PROC_INP_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = LED_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = LED_PROC_INP_CARD;
               }
               break;
            }
            case LED_PROC_INP_CARD:
            {
               try
               {
                  /* Humans are one based, not zero based. */
                  currCard = Integer.parseInt(tokens[currToken]) - 1;
                  if (currCard < numCards)
                  {
                     state = LED_PROC_INP_PIN;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LED_CARDS: Card Num larger than numCards.");
                     GlobInfo.parseFail = true;
                     state = LED_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("LED_CARDS: Illegal Card Num.");
                  GlobInfo.parseFail = true;
                  state = LED_ERROR;
               }
               break;
            }
            case LED_PROC_INP_PIN:
            {
               Integer                          tstKey;
               
               try
               {
                  currPin = Integer.parseInt(tokens[currToken]) - 1;
                  if (currPin < NUM_LED_PER_CARD)
                  {
                     /* Check if this is a duplicate value */
                     tstKey = ParseRules.hmSymbol.get(currName);
                     if (tstKey == null)
                     {
                        ParseRules.hmSymbol.put(currName,
                           ParseRules.SYMB_LED_PIN | (currCard << 8) | currPin);
                     	GlobInfo.fileConstClass.println("   public static final int             " +
                           	String.format("%-27s= 0x%02x;", currName.toUpperCase(), 1 << currPin));
                        state = LED_PROC_INP_NAME;
                     }
                     else
                     {
                        GlobInfo.hostCtl.printMsg("LED_CARDS: Duplicate input names.");
                        GlobInfo.parseFail = true;
                        state = LED_ERROR;
                     }
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("LED_CARDS: Pin Num > 8.");
                     GlobInfo.parseFail = true;
                     state = LED_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("LED_CARDS: Illegal Pin Num.");
                  GlobInfo.parseFail = true;
                  state = LED_ERROR;
               }
               break;
            }
            case LED_DONE:
            {
               GlobInfo.hostCtl.printMsg("LED_CARDS: Extra info.");
               GlobInfo.parseFail = true;
               state = LED_ERROR;
               break;
            }
            case LED_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if ((state == LED_ERROR) || (state == LED_DONE))
      {
      	GlobInfo.fileConstClass.println("");
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
} /* End LedClass */
