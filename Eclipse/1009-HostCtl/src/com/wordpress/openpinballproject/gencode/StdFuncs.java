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
 * @file:   StdFuncs.java
 * @author: Hugh Spahr
 * @date:   10/16/2013
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
 * This is the standard functions class file.
 *
 *===============================================================================
 */

package com.wordpress.openpinballproject.gencode;

import com.wordpress.openpinballproject.gencode.RulesClass;

public class StdFuncs
{
   public static final int          CHAINCMD_END_LIST             =  0x00000000;
   public static final int          CHAINCMD_WAIT                 =  0x01000000;
   public static final int          CHAINCMD_REPEAT               =  0x02000000;

   public static void DisableSolenoids()
   {
   	/* HRS: Add code */
   }
   public static void LedRotLeft(
   	int									mask,
   	int									varIndex)
   {
   	int									firstBit;
   	boolean								currBit = false;
   	boolean								foundBit;
   	int									index;

   	/* Find first bit in mask */
   	for (firstBit = 0, foundBit = false; (firstBit < 32) && !foundBit; firstBit++)
   	{
   		if ((mask & (1 << firstBit)) != 0)
   		{
   			foundBit = true;
   			if ((RulesClass.Variable[varIndex] & (1 << firstBit)) == 0)
   			{
   				currBit = false;
   			}
   			else
   			{
   				currBit = true;
   			}
   		}
   	}
   	if (foundBit)
   	{
      	for (index = firstBit + 1; index < 32; index++)
      	{
      		if ((mask & (1 << index)) != 0)
      		{
      			if ((RulesClass.Variable[varIndex] & (1 << index)) == 0)
      			{
      				foundBit = false;
      			}
      			else
      			{
      				foundBit = true;
      			}
      			if (currBit)
      			{
         			RulesClass.Variable[varIndex] |= (1 << index);
      			}
      			else
      			{
         			RulesClass.Variable[varIndex] &= ~(1 << index);
      			}
      			currBit = foundBit;
      		}
      	}
      	
      	/* Rotate and finish first bit */
			if (currBit)
			{
   			RulesClass.Variable[varIndex] |= (1 << firstBit);
			}
			else
			{
   			RulesClass.Variable[varIndex] &= ~(1 << firstBit);
			}
   	}
   }
   public static void LedRotRight(
   	int									mask,
   	int									varIndex)
   {
   	int									firstBit;
   	boolean								currBit = false;
   	boolean								foundBit;
   	int									index;

   	/* Find first bit in mask */
   	for (firstBit = 31, foundBit = false; (firstBit > 0) && !foundBit; firstBit--)
   	{
   		if ((mask & (1 << firstBit)) != 0)
   		{
   			foundBit = true;
   			if ((RulesClass.Variable[varIndex] & (1 << firstBit)) == 0)
   			{
   				currBit = false;
   			}
   			else
   			{
   				currBit = true;
   			}
   		}
   	}
   	if (foundBit)
   	{
      	for (index = firstBit - 1; index > 0; index--)
      	{
      		if ((mask & (1 << index)) != 0)
      		{
      			if ((RulesClass.Variable[varIndex] & (1 << index)) == 0)
      			{
      				foundBit = false;
      			}
      			else
      			{
      				foundBit = true;
      			}
      			if (currBit)
      			{
         			RulesClass.Variable[varIndex] |= (1 << index);
      			}
      			else
      			{
         			RulesClass.Variable[varIndex] &= ~(1 << index);
      			}
      			currBit = foundBit;
      		}
      	}
      	
      	/* Rotate and finish first bit */
			if (currBit)
			{
   			RulesClass.Variable[varIndex] |= (1 << firstBit);
			}
			else
			{
   			RulesClass.Variable[varIndex] &= ~(1 << firstBit);
			}
   	}
   }
   public static void CreateLedChain(
   		int									index,
      	int									mask,
      	int[]									ledSet,
      	int[]									ledCmd)
   {
   	
   }
   public static void CreateMode(
   		int									index,
      	int[]									initChains,
      	int[]									procChains,
      	int[]									video,
			int[]									audio,
			int[]									ledChain,
			int									initScoring)
   {
   	
   }
}
