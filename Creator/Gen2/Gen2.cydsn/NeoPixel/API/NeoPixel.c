/*
 *===============================================================================
 *
 *                         OOOOOO
 *                       OOOOOOOOOO
 *      PPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP    OOO      OOO    PPP
 *               PPP     OOOOOOOOOO     PPP
 *              PPPPP      OOOOOO      PPPPP
 *
 * @file:   NeoPixel.h
 * @author: Hugh Spahr
 * @date:   9/12/2017
 *
 * @note:   Open Pinball Project
 *          Copyright© 2017, Hugh Spahr
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
 * Interface functions for running RGB Neopixels on PSoC 4200
 *
 *===============================================================================
 */

#include "cytypes.h"
#include "`$INSTANCE_NAME`_NeoPixel.h"
#include "`$INSTANCE_NAME`_defs.h"

uint8 `$INSTANCE_NAME`_WriteFifo(uint32 data)
{
   uint8 status;
   
   status = NeoPixel_StatusReg_Read();

   /* Check if FIFO is full */
   if (status & `$INSTANCE_NAME`_STATUS_FIFONOTFULL)
   {
      CySetReg24(NeoPixel_Datapath_F0_PTR, data);
      return 0;
   }
   else
   {
      return `$INSTANCE_NAME`_ERR_FIFO_FULL;
   }
}

uint8 `$INSTANCE_NAME`_FifoFull()
{ 
   uint8 status;
   
   status = NeoPixel_StatusReg_Read();
   if (status & `$INSTANCE_NAME`_STATUS_FIFONOTFULL)
   {
      return 0;
   }
   else
   {
      return `$INSTANCE_NAME`_STAT_FIFO_FULL;
   }
}

/* [] END OF FILE */
