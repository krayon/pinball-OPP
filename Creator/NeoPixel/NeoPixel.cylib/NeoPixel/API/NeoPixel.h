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
 * Interface file for running RGB Neopixels on PSoC 4200
 *
 *===============================================================================
 */

#if !defined (`$INSTANCE_NAME`_NEOPIXEL_H) 

  #define `$INSTANCE_NAME`_NEOPIXEL_H 
  #include "cytypes.h"
    
#define `$INSTANCE_NAME`_STATUS_FIFONOTFULL 0x01   /* FIFO NOT FULL  */

  uint8 `$INSTANCE_NAME`_WriteFifo(uint32 data); 
  uint8 `$INSTANCE_NAME`_FifoFull(); 

#define `$INSTANCE_NAME`_STAT_FIFO_FULL 0x01
#define `$INSTANCE_NAME`_ERR_FIFO_FULL 0x02 

#endif 

/* [] END OF FILE */
