
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
 * @file:   InpCardClass.java
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
 * Input Card class
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.hostctl;

public class InpCardClass
{
   private static final int            NUM_INP_PER_CARD        = 16;

   private static final int            INP_NEED_NUM_CARDS      = 0;
   private static final int            INP_NEED_OPEN_CURLY     = 1;
   private static final int            INP_PROC_INP_NAME       = 2;
   private static final int            INP_PROC_INP_CARD       = 3;
   private static final int            INP_PROC_INP_PIN        = 4;
   private static final int            INP_PROC_INP_TYPE       = 5;
   private static final int            INP_DONE                = 6;
   private static final int            INP_ERROR               = 7;

   private int                         numCards = 0;
   private int                         state = INP_NEED_NUM_CARDS;
   private int[]                       cardCfgArr;
   
   private String                      currName;
   private int                         currCard;
   private int                         currPin;
   
   /*
    * ===============================================================================
    * 
    * Name: InpCardClass
    * 
    * ===============================================================================
    */
   /**
    * Input card class for input cards
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
   public InpCardClass(
      String[]                         tokens)
   {
      /* Initialize the class, first token is keyword, second should be num cards  */
      if (tokens.length > 1)
      {
         /* If more tokens, keep processing */
         addEntries(1, tokens);         
      }
   } /* end InpCardClass */

   /*
    * ===============================================================================
    * 
    * Name: addEntries
    * 
    * ===============================================================================
    */
   /**
    * Add entries to create input pins
    * 
    * Take tokens and add entries to create input pins.  This class uses fields
    * to configure the inputs, and name each output for later lookups.
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
            case INP_NEED_NUM_CARDS:
            {
               try
               {
                  numCards = Integer.parseInt(tokens[currToken]);
                  cardCfgArr = new int[numCards * NUM_INP_PER_CARD];
                  state = INP_NEED_OPEN_CURLY;
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("INPUT_CARDS: needs numCards as param.");
                  GlobInfo.parseRules.parseFail = true;
                  state = INP_ERROR;
               }
               break;
            }
            case INP_NEED_OPEN_CURLY:
            {
               if (tokens[currToken].equals("{"))
               {
                  state = INP_PROC_INP_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("INPUT_CARDS: needs curly parenthesis.");
                  GlobInfo.parseRules.parseFail = true;
                  state = INP_ERROR;
               }
               break;
            }
            case INP_PROC_INP_NAME:
            {
               if (tokens[currToken].equals("}"))
               {
                  state = INP_DONE;
               }
               else
               {
                  currName = new String(tokens[currToken]);
                  state = INP_PROC_INP_CARD;
               }
               break;
            }
            case INP_PROC_INP_CARD:
            {
               try
               {
                  /* Humans are one based, not zero based. */
                  currCard = Integer.parseInt(tokens[currToken]) - 1;
                  if (currCard < numCards)
                  {
                     state = INP_PROC_INP_PIN;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("INPUT_CARDS: Card Num larger than numCards.");
                     GlobInfo.parseRules.parseFail = true;
                     state = INP_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("INPUT_CARDS: Illegal Card Num.");
                  GlobInfo.parseRules.parseFail = true;
                  state = INP_ERROR;
               }
               break;
            }
            case INP_PROC_INP_PIN:
            {
               try
               {
                  currPin = Integer.parseInt(tokens[currToken]) - 1;
                  if (currPin < NUM_INP_PER_CARD)
                  {
                     state = INP_PROC_INP_TYPE;
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("INPUT_CARDS: Pin Num > 16.");
                     GlobInfo.parseRules.parseFail = true;
                     state = INP_ERROR;
                  }
               }
               catch (NumberFormatException e)
               {
                  GlobInfo.hostCtl.printMsg("INPUT_CARDS: Illegal Pin Num.");
                  GlobInfo.parseRules.parseFail = true;
                  state = INP_ERROR;
               }
               break;
            }
            case INP_PROC_INP_TYPE:
            {
               Integer                          tstKey;
               
               if (tokens[currToken].equals("STATE_INPUT"))
               {
                  cardCfgArr[(currCard * NUM_INP_PER_CARD) + currPin] =
                     SerIntf.INPCFG_STATE_INPUT;
                  state = INP_PROC_INP_NAME;
               }
               else if (tokens[currToken].equals("FALL_EDGE"))
               {
                  cardCfgArr[(currCard * NUM_INP_PER_CARD) + currPin] =
                     SerIntf.INPCFG_FALL_EDGE;
                  state = INP_PROC_INP_NAME;
               }
               else if (tokens[currToken].equals("RISE_EDGE"))
               {
                  cardCfgArr[(currCard * NUM_INP_PER_CARD) + currPin] =
                     SerIntf.INPCFG_RISE_EDGE;
                  state = INP_PROC_INP_NAME;
               }
               else
               {
                  GlobInfo.hostCtl.printMsg("INPUT_CARDS: Illegal type.");
                  GlobInfo.parseRules.parseFail = true;
                  state = INP_ERROR;
               }
               
               /* Add to the hash map */
               if (state == INP_PROC_INP_NAME)
               {
                  /* Check if this is a duplicate value */
                  tstKey = ParseRules.hmSymbol.get(currName);
                  if (tstKey == null)
                  {
                      ParseRules.hmSymbol.put(currName,
                         ParseRules.SYMB_INP_PIN | (currCard << 8) | currPin);
                  }
                  else
                  {
                     GlobInfo.hostCtl.printMsg("INPUT_CARDS: Duplicate input names.");
                     GlobInfo.parseRules.parseFail = true;
                     state = INP_ERROR;
                  }
               }
               break;
            }
            case INP_DONE:
            {
               GlobInfo.hostCtl.printMsg("INPUT_CARDS: Extra info.");
               GlobInfo.parseRules.parseFail = true;
               state = INP_ERROR;
               break;
            }
            case INP_ERROR:
            {
               break;
            }
         }
         currToken++;
      }
      if ((state == INP_ERROR) || (state == INP_DONE))
      {
         return (true);
      }
      else
      {
         return (false);
      }
   } /* end addEntries */
   
} /* End InpCardClass */
