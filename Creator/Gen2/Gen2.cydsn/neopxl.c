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
 * @file:   neopxl.c
 * @author: Hugh Spahr
 * @date:   9/16/2015
 *
 * @note:   Open Pinball Project
 *          Copyright© 2015, Hugh Spahr
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
 * This is the file for driving Neopixels using a SPI bus.  This uses the
 * NeoPixel library to create the NeoPixel protocol.  Since the hardware
 * is prepending a 1 and appending a 0, no special processing needs to be
 * done to the pixel data.  Neopixel data is presented 8 bits of green,
 * then red, then blue with msb first.
 *
 * This file requires a 40ms tick to start the neopixel processing, and an
 * interrupt when the FIFO gets low.
 *
 *===============================================================================
 */
#include <stdlib.h>
#include "stdtypes.h"
#include "gen2glob.h"
#include "neointf.h"
#include "NeoClock.h"
#include "UDBClock.h"
#include "isr_FIFOEmpty.h"
#include "NeoPixel_NeoPixel.h"

#define BYTES_PER_PIXEL          3       /* 24 bits per pixel */
#define MAX_MULT_FACT_SHFT       5       /* 2^5 or 32 */
    
#define CMD_MASK                 0xe0
#define CMD_FADE_CMDS            0x40
#define CMD_COLOR_TBL_MASK       (NEOI_COLOR_TBL_SIZE - 1)
#define CMD_FAST_CMD             0x20
    
#define STAT_START_PROC          0x80    /* Set by isr to start processing */
#define STAT_XMT_DATA            0x40    /* Send neopixel data for update */

typedef struct
{
   U8                stat;                /* Status */
   U8                numPixels;           /* Number of pixels */
   INT               underflow;           /* Underflow count */
   INT               complUpd;            /* Number of completed updates */
   U8                *pxlCmd_p;           /* Ptr to array of pixel commands */
   U8                *buf_p;              /* Holds pixel data bytes */
   U8                *src_p;              /* Ptr to next byte of data to copy to FIFO */
   U8                *end_p;              /* Ptr to end of pixel data buffer */
} NEO_INFO;

NEO_INFO neoInfo;

/*
 * ===============================================================================
 * 
 * Name: FIFOEmpty_isr
 * 
 * ===============================================================================
 */
/**
 * FIFO empty ISR
 * 
 * Grabs data from buffer and adds it to the FIFO.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
CY_ISR(FIFOEmpty_isr)
{
   U8 retCode;
   U32 pixelData;
   
   /* Try writing to the chain, returns non-zero if write failed
    * since FIFO was full.
    */
   retCode = 0;
   while ((neoInfo.stat & STAT_XMT_DATA) && (retCode == 0))
   {
      pixelData = (neoInfo.src_p[0] << 16) | (neoInfo.src_p[1] << 8) | neoInfo.src_p[2];
      retCode = NeoPixel_WriteFifo(pixelData);
      if (retCode == 0)
      {
         neoInfo.src_p += BYTES_PER_PIXEL;
         if (neoInfo.src_p >= neoInfo.end_p)
         {
            /* All LEDs updated, so end updating, mask FIFO empty isr */
            neoInfo.stat &= ~STAT_XMT_DATA;
            isr_FIFOEmpty_Disable();
         }
      }
   }
   isr_FIFOEmpty_ClearPending();
}

/*
 * ===============================================================================
 * 
 * Name: neopxl_init
 * 
 * ===============================================================================
 */
/**
 * Initialize the neopixel driver
 * 
 * Set the neopixel color table pointer.
 * 
 * @param   None
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neopxl_init()
{
   /* Set the location of the configuration data */
   gen2g_info.neoCfg_p = (GEN2G_NEO_CFG_T *)gen2g_info.freeCfg_p;
   gen2g_info.freeCfg_p += sizeof(GEN2G_NEO_CFG_T);
} /* neopxl_init */

/*
 * ===============================================================================
 * 
 * Name: neo_init
 * 
 * ===============================================================================
 */
/**
 * Initialize neopixel processing
 * 
 * Turn off all pixels, and reset indices.  Register a 40ms repeating tick function.
 * 
 * @param   numPixels   [in]        Number of pixels
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
GEN2G_ERROR_E neo_init(
   U8                numPixels)
{
   U8                *tmp_p;
   U32               tmpVal;

#define HSIOM_PORT_SEL2_ADDR 0x40010008
#define HSIOM_BIT_MASK       0x0000000f
#define HSIOM_USE_UDB        0x00000003
#define PRT2_DR_ADDR         0x40040200
#define PRT2_ENA_OUTPUT      0x00000001

   /* Only initialize if Neo pixels are configured */
   neoInfo.stat = 0;
   if ((gen2g_info.typeWingBrds & (1 << WING_NEO)) != 0)
   {
      /* Initialize the state machine to turn off all the LEDs, set indices to 0 */
      gen2g_info.haveNeo = TRUE;
      neoInfo.underflow = 0;
      neoInfo.complUpd = 0;
      neoInfo.numPixels = numPixels;
    
      /* Setup hardware including HSIOM and DR for OE */
      tmpVal = *(R32 *)HSIOM_PORT_SEL2_ADDR;
      tmpVal &= ~HSIOM_BIT_MASK;
      tmpVal |= HSIOM_USE_UDB;
      *(R32 *)HSIOM_PORT_SEL2_ADDR = tmpVal;
      *(R32 *)PRT2_DR_ADDR |= PRT2_ENA_OUTPUT;
    
      /* Test for null on commands */
      neoInfo.pxlCmd_p = malloc(numPixels);
      if (neoInfo.pxlCmd_p == NULL)
      {
         gen2g_info.error = ERR_MALLOC_FAIL;
         return(ERR_MALLOC_FAIL);
      }
       
      /* Allocate neopixel buffer memory */
      neoInfo.buf_p = malloc(numPixels * BYTES_PER_PIXEL);
      neoInfo.end_p = neoInfo.buf_p + (numPixels * BYTES_PER_PIXEL);
      if (neoInfo.buf_p == NULL)
      {
         gen2g_info.error = ERR_MALLOC_FAIL;
         return(ERR_MALLOC_FAIL);
      }
    
      /* Set initial values to verify NeoPixels are working */
      for (tmp_p = neoInfo.pxlCmd_p; tmp_p < neoInfo.pxlCmd_p + numPixels; tmp_p++)
      {
         *tmp_p = NEOI_CMD_BLINK_SLOW;
      }
      gen2g_info.neoCfg_p->colorTbl[0].green = 0xff;
      gen2g_info.neoCfg_p->colorTbl[0].blue = 0xff;
      gen2g_info.neoCfg_p->colorTbl[0].red = 0xff;

      NeoClock_Start();        /* 4.8 MHz/2 or 2.4 MHz used for NeoPixel bit timings.  Must go through T-flip flop
                                * so it can be used as a data signal
                                */
      UDBClock_Start();        /* 24MHz clock used to move through UDB state machine */

      isr_FIFOEmpty_StartEx(FIFOEmpty_isr);
      isr_FIFOEmpty_Disable();
   }
    
   /* Register a 40ms repeating tick function, register FIFO empty if necessary */
   return(NO_ERRORS);
}

/*
 * ===============================================================================
 * 
 * Name: neo_40ms_tick
 * 
 * ===============================================================================
 */
/**
 * 40 ms tick function.
 * 
 * Starts the neo pixel processing setting a state bit.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_40ms_tick()
{
   if (gen2g_info.validCfg && gen2g_info.haveNeo)
   {
      if ((neoInfo.stat & (STAT_START_PROC | STAT_XMT_DATA)) == 0)
      {
         neoInfo.stat |= STAT_START_PROC;
      }
   }
}

/*
 * ===============================================================================
 * 
 * Name: neo_mult_pixel_color
 * 
 * ===============================================================================
 */
/**
 * Neopixel multiply pixel color by a factor
 * 
 * Multiply the pixel color by a factor to dim the pixel
 * 
 * @param   pxlColor_p  [in,out]    pixel color, outputs new dimmer color
 * @param   multFact    [in]        factor of 0-63 of brightness of pixel
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_mult_pixel_color(
   INT               *pxlColor_p,
   INT               multFact)
{
   INT               byteIndex;
   INT               outData;
   INT               tmpVal;
    
   /* If factor is max value, there is no change */
   if (multFact != (1 << MAX_MULT_FACT_SHFT))
   {
      outData = 0;
      for (byteIndex = 0; byteIndex < 3; byteIndex++)
      {
         tmpVal = (*pxlColor_p >> (byteIndex * 8)) & 0xff;
         tmpVal = (tmpVal * multFact) >> MAX_MULT_FACT_SHFT;
         outData |= (tmpVal << (byteIndex * 8));
      }
      *pxlColor_p = outData;
   }
}

/*
 * ===============================================================================
 * 
 * Name: neo_fill_buffer
 * 
 * ===============================================================================
 */
/**
 * Neopixel fill a buffer
 * 
 * Grab info about next pixel.  Determine the pixel command and fill out the
 * pixel color.  Convert pixel color to a buffer, and copy the buffer to empty
 * buffer slot.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
U8 *neo_fill_buffer(
   U8                pxlCmd,
   U8                *dest_p)
{
   INT               pxlColor;
   INT               multFact;
   INT               index;
   
   pxlColor = (((INT)gen2g_info.neoCfg_p->colorTbl[pxlCmd & CMD_COLOR_TBL_MASK].green) << 16) |
      (((INT)gen2g_info.neoCfg_p->colorTbl[pxlCmd & CMD_COLOR_TBL_MASK].red) << 8) | 
      (INT)gen2g_info.neoCfg_p->colorTbl[pxlCmd & CMD_COLOR_TBL_MASK].blue; 
    
   /* Verify pixel is not "on".  An "on" pixel overrides the state */
   if ((pxlCmd & NEOI_CMD_LED_ON) == 0)
   {
      if (pxlCmd & CMD_FADE_CMDS)
      {
         /* Determine if fast or slow fade */
         if (pxlCmd & CMD_FAST_CMD)
         {
            /* Fast fade command, check if getting brighter or darker */
            if (gen2g_info.ledStatus & GEN2G_STAT_FADE_FAST_DEC)
            {
               multFact = GEN2G_MAX_STATE_NUM - ((gen2g_info.ledStateNum & 0xf) * 4);
            }
            else
            {
               multFact = ((gen2g_info.ledStateNum & 0xf) + 1) * 4;
            }
         }
         else
         {
            /* Slow fade command, check if getting brighter or darker */
            if (gen2g_info.ledStatus & GEN2G_STAT_FADE_SLOW_DEC)
            {
               multFact = GEN2G_MAX_STATE_NUM - gen2g_info.ledStateNum;
            }
            else
            {
               multFact = gen2g_info.ledStateNum + 1;
            }
         }
         neo_mult_pixel_color(&pxlColor, multFact);
      }
      else
      {
         /* Determine if fast or blink */
         if (pxlCmd & CMD_FAST_CMD)
         {
            /* Fast blink command, check if pixel should be off */
            if ((gen2g_info.ledStatus & GEN2G_STAT_BLINK_FAST_ON) == 0)
            {
               pxlColor = 0;
            }
         }
         else
         {
            /* Slow blink command, check if pixel should be off */
            if ((gen2g_info.ledStatus & GEN2G_STAT_BLINK_SLOW_ON) == 0)
            {
               pxlColor = 0;
            }
            else
            {
                pxlCmd++;
            }
         }
      }
   }
   for (index = 0; index < BYTES_PER_PIXEL; index++)
   {
      *dest_p++ = (U8)(pxlColor >> ((2 - index) << 3));
   }
   return (dest_p);
}

/*
 * ===============================================================================
 * 
 * Name: neo_task
 * 
 * ===============================================================================
 */
/**
 * Neopixel task
 * 
 * Check if a new neopixel cycle needs to start.  If so, clear indices, create
 * data for two neopixels, and fill the SPI buffer.  Otherwise check if the
 * buffer needs more data.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_task()
{
   U8                *cmd_p;
   U8                *buf_p;
    
   /* Check if new cycle needs to be started */
   if (gen2g_info.validCfg && (neoInfo.stat & STAT_START_PROC))
   {
      neoInfo.stat &= ~STAT_START_PROC;
      neoInfo.stat |= STAT_XMT_DATA;

      /* Update the pixel data buffer,  */
      buf_p = neoInfo.buf_p;
      for (cmd_p = neoInfo.pxlCmd_p; cmd_p < neoInfo.pxlCmd_p + neoInfo.numPixels; cmd_p++)
      {
         buf_p = neo_fill_buffer(*cmd_p, buf_p);
      }
      neoInfo.src_p = neoInfo.buf_p;
    
      isr_FIFOEmpty_Enable();
   }
}

/*
 * ===============================================================================
 * 
 * Name: neo_update_pixel_color
 * 
 * ===============================================================================
 */
/**
 * Neopixel update pixel color
 * 
 * Update the pixel's colorTbl index
 * 
 * @param   pixel       [in]        Pixel to change
 * @param   colorTblIdx [in]        New color table index
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_update_pixel_color(
   INT               pixel,
   INT               colorTblIdx)
{
   INT               pxlCmd;
   
   pxlCmd = neoInfo.pxlCmd_p[pixel];
   pxlCmd &= ~CMD_COLOR_TBL_MASK;
   pxlCmd |= colorTblIdx;
   neoInfo.pxlCmd_p[pixel] = pxlCmd;
}

/*
 * ===============================================================================
 * 
 * Name: neo_update_pixel_cmd
 * 
 * ===============================================================================
 */
/**
 * Neopixel update pixel command
 * 
 * Update the pixel's command
 * 
 * @param   pixel       [in]        Pixel to change
 * @param   cmd         [in]        New pixel command
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_update_pixel_cmd(
   INT               pixel,
   INT               cmd)
{
   INT               pxlCmd;
   
   pxlCmd = neoInfo.pxlCmd_p[pixel];
   pxlCmd &= ~CMD_MASK;
   pxlCmd |= cmd;
   neoInfo.pxlCmd_p[pixel] = pxlCmd;
}

/*
 * ===============================================================================
 * 
 * Name: neo_update_color_tbl
 * 
 * ===============================================================================
 */
/**
 * Neopixel update color table entry
 * 
 * Update the pixel's command
 * 
 * @param   index       [in]        Index in color table to change
 * @param   color       [in]        New color table color
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_update_color_tbl(
   INT               index,
   U32               color)
{
   gen2g_info.neoCfg_p->colorTbl[index].green = (color >> 16) & 0xff;
   gen2g_info.neoCfg_p->colorTbl[index].red = (color >> 8) & 0xff;
   gen2g_info.neoCfg_p->colorTbl[index].blue = color & 0xff;
}

/* [] END OF FILE */
