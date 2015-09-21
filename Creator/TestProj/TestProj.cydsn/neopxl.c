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
 * This is the file for driving Neopixels using a SPI bus.  The SPI is
 * configured for 2.4 MHz, so each bit of a pixel requires 3 SPI bits.  The
 * first bit is always 1 and the last bit is always 0, while the middle bit
 * determines the value of the data sent to the Neopixel.  Neopixels data
 * is presented 8 bits of green, then red, then blue with msb first.
 *
 * This file requires a 20ms tick to start the neopixel processing, and an
 * interrupt when the SPI FIFO is empty.
 *
 *===============================================================================
 */
#include "stdtypes.h"
#include "neointf.h"

#define SCB1_TX_FIFO_STATUS     0x40070208
#define SCB_USED_MASK           0xf             /* Num FIFO bytes used */
#define NUM_FIFO_BYTES          8               /* Num SCB FIFO bytes */

#define SCB1_TX_FIFO_WR         0x40070240
#define SCB1_INTR_TX            0x40070f80
#define SCB1_INTR_TX_MASK       0x40070f88
#define INTR_TX_SCB_NOT_FULL    0x00000002
#define INTR_TX_SCB_EMPTY       0x00000010

/* This lookup table is used to prepend a 1, and append a 0 to the data.
 * An 8 bit color is broken into two nibbles, then the results of the two lookups
 * are OR'd together.  (Each lookup produces 12 bits of data).  This is repeated
 * for each color of the pixel (green, red, blue).  A complete pixel uses 9 bytes
 * of data.
 */
#define COLOR_LKUP_BITS     12

const U16 colorLkup[] =
    { 0x0924, 0x0926, 0x0934, 0x0936, 0x09a4, 0x09a6, 0x09b4, 0x09b6,
      0x0d24, 0x0d26, 0x0d34, 0x0d36, 0x0da4, 0x0da6, 0x0db4, 0x0db6 };

/* Can be changed by user, order is a byte for green, red, and blue */
U32 colorTbl[32] =
    { 0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffffff, 0x000000,
      0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000,
      0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000,
      0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0xffffff };
    
#define NEO_MAX_PIXELS      64
#define BYTES_PER_PIXEL     9       /* 3 8-bit colors, 3 bits needed/bit color */
#define BUFFER_SIZE         2 * BYTES_PER_PIXEL
#define MAX_STATE_NUM       64      /* State num goes from 0 - 63 */
#define MAX_MULT_FACT_SHFT  6       /* Must be power of 2 */
    
#define CMD_MASK            0xe0
#define CMD_FADE_CMDS       0x40
#define CMD_COLOR_TBL_MASK  (NEOI_COLOR_TBL_SIZE - 1)
#define CMD_FAST_CMD        0x20
    
#define STAT_BLINK_SLOW_ON  0x01
#define STAT_FADE_SLOW_DEC  0x01
#define STAT_BLINK_FAST_ON  0x02
#define STAT_FADE_FAST_DEC  0x02
#define STAT_START_PROC     0x80    /* Set by isr to start processing */
#define STAT_DONE_PIXEL     0x40    /* Set by isr, data for pixel consumed, fill out next buffer */
#define STAT_RUNNING        0x20    /* Neopixel process is running */

typedef struct
{
    U8              pxlCmd[NEO_MAX_PIXELS];
    U8              stateNum;       /* 0 - 63 counter used to fade/blink LEDs */
    U8              pxlIndex;
    U8              stat;           /* If blinking LED is on/fading LED is brighter */
    U8              isrCopyIdx;     /* Next byte to be copied to FIFO */
    U8              buffer[18];     /* Holds next 2 LEDs data bytes */
    U8              numPixels;      /* Number of pixels */
} NEO_INFO;

NEO_INFO neoInfo;

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
 * Turn off all pixels, and reset indices.  Register a 20ms repeating tick function.
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
void neo_init(
    U8              numPixels)
{
    U8              *tmp_p;
    
    /* Initialize the state machine to turn off all the LEDs, set indices to 0 */
    neoInfo.stateNum = 0;
    neoInfo.pxlIndex = 0;
    neoInfo.stat = 0;
    neoInfo.isrCopyIdx = 0;
    neoInfo.numPixels = numPixels;
    for (tmp_p = &neoInfo.pxlCmd[0]; tmp_p < &neoInfo.pxlCmd[numPixels]; tmp_p++)
    {
        *tmp_p = NEOI_CMD_LED_ON;
    }
    
    /* Register a 20ms repeating tick function, register FIFO empty if necessary */
}

/*
 * ===============================================================================
 * 
 * Name: neo_20ms_tick
 * 
 * ===============================================================================
 */
/**
 * 20 ms tick function.
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
void neo_20ms_tick()
{
    neoInfo.stat |= STAT_START_PROC;
}

/*
 * ===============================================================================
 * 
 * Name: neo_fill_fifo
 * 
 * ===============================================================================
 */
/**
 * Neopixel fill the FIFO
 * 
 * Grabs data from buffer and adds it to the FIFO.  If it finishes a pixel, it sets
 * the done pixel flag so the data for the next pixel is calculated.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_fill_fifo()
{
    INT bytesWritten = 0;
    U32 regData;
    
    /* While the Tx FIFO is not full */
    /* HRS:  Was while (*(R32 *)SCB1_INTR_TX & INTR_TX_SCB_NOT_FULL) */
    while (((*(R32 *)SCB1_TX_FIFO_STATUS) & SCB_USED_MASK) < NUM_FIFO_BYTES)
    {
        regData = *(R32 *)SCB1_INTR_TX;
        bytesWritten++;
        *(R32 *)SCB1_TX_FIFO_WR = neoInfo.buffer[neoInfo.isrCopyIdx];
        *(R32 *)SCB1_INTR_TX = INTR_TX_SCB_NOT_FULL;
        neoInfo.isrCopyIdx++;
        if (neoInfo.isrCopyIdx == BYTES_PER_PIXEL)
        {
            /* Only create new pixel info if <= num pixels.
             * Note: must create blank pixel to cmds to pixels and
             *   force low signal level.
             */
            if (neoInfo.pxlIndex <= neoInfo.numPixels)
            {
                /* Mark that a new pixel needs to be calculated */
                neoInfo.stat |= STAT_DONE_PIXEL;
            }
            else
            {
                /* Disable FIFO empty isr, mask it */
                *(R32 *)SCB1_INTR_TX_MASK |= INTR_TX_SCB_EMPTY;
                neoInfo.stat &= ~STAT_RUNNING;
            }
        }
        else if (neoInfo.isrCopyIdx == 2 * BYTES_PER_PIXEL)
        {
            /* Only create new pixel info if <= num pixels.
             * Note: must create blank pixel to cmds to pixels and
             *   force low signal level.
             */
            if (neoInfo.pxlIndex <= neoInfo.numPixels)
            {
                /* Mark that a new pixel needs to be calculated, and wrap index */
                neoInfo.stat |= STAT_DONE_PIXEL;
                neoInfo.isrCopyIdx = 0;
            }
            else
            {
                /* Disable FIFO empty interrupt */
                *(R32 *)SCB1_INTR_TX_MASK |= INTR_TX_SCB_EMPTY;
            }
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
    INT             *pxlColor_p,
    INT             multFact)
{
    INT             byteIndex;
    INT             outData;
    INT             tmpVal;
    
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
 * Name: neo_convert_color_to_buffer
 * 
 * ===============================================================================
 */
/**
 * Neopixel convert color to buffer
 * 
 * Convert the 24 bit color to a 9 bytes of buffer data
 * 
 * @param   pxlColor    [in]        pixel color (24 bits)
 * @param   buf_p       [out]       Pointer to buffer to be filled out
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_convert_color_to_buffer(
    INT             pxlColor,
    U8              *buf_p)
{
#define NUM_DATA_NIBS       6
#define BITS_IN_NIB_SHIFT   2
    
    INT             nibbleIndex;
    INT             nibble;
    INT             data = 0;
    INT             dataIndex;
    
    for (nibbleIndex = 0; nibbleIndex < NUM_DATA_NIBS; nibbleIndex++)
    {
        nibble = (pxlColor >> ((NUM_DATA_NIBS - nibbleIndex - 1) << BITS_IN_NIB_SHIFT)) & 0xf;
        if ((nibbleIndex & 0x01) == 0)
        {
            data = colorLkup[nibble] << COLOR_LKUP_BITS;
        }
        else
        {
            data |= colorLkup[nibble];

            /* Data for color formed, copy 3 bytes to output buffer */
            for (dataIndex = 2; dataIndex >= 0; dataIndex--)
            {
                *buf_p = data >> (dataIndex * 8);
                buf_p++;
            }
        }
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
void neo_fill_buffer()
{
    INT             pxlCmd;
    INT             pxlColor;
    INT             multFact;
    U8              buffer[BYTES_PER_PIXEL];
    U8              *src_p;
    U8              *dest_p;
    
    /* If more than the number of pixels, fill with all 0s */
    if (neoInfo.pxlIndex >= neoInfo.numPixels)
    {
        for (dest_p = &buffer[0]; dest_p < &buffer[BYTES_PER_PIXEL]; dest_p++)
        {
            *dest_p = 0;
        }
    }
    else
    {
        pxlCmd = neoInfo.pxlCmd[neoInfo.pxlIndex];
        pxlColor = colorTbl[pxlCmd & CMD_COLOR_TBL_MASK];
        
        /* Verify pixel is not "on".  An "on" pixel overrides the state */
        if ((pxlCmd & NEOI_CMD_LED_ON) == 0)
        {
            if (pxlCmd & CMD_FADE_CMDS)
            {
                /* Determine if fast or slow fade */
                if (pxlCmd & CMD_FAST_CMD)
                {
                    /* Fast fade command, check if getting brighter or darker */
                    if (neoInfo.stat & STAT_FADE_FAST_DEC)
                    {
                        multFact = MAX_STATE_NUM - ((neoInfo.stateNum & 0xf) * 4);
                    }
                    else
                    {
                        multFact = ((neoInfo.stateNum & 0xf) + 1) * 4;
                    }
                }
                else
                {
                    /* Slow fade command, check if getting brighter or darker */
                    if (neoInfo.stat & STAT_FADE_SLOW_DEC)
                    {
                        multFact = MAX_STATE_NUM - neoInfo.stateNum;
                    }
                    else
                    {
                        multFact = neoInfo.stateNum + 1;
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
                    if ((neoInfo.stat & STAT_BLINK_FAST_ON) == 0)
                    {
                        pxlColor = 0;
                    }
                }
                else
                {
                    /* Slow blink command, check if pixel should be off */
                    if ((neoInfo.stat & STAT_BLINK_SLOW_ON) == 0)
                    {
                        pxlColor = 0;
                    }
                }
            }
        }
        neo_convert_color_to_buffer(pxlColor, &buffer[0]);
    }
    
    if (neoInfo.pxlIndex & 0x01)
    {
        /* Fill out the 2nd buffer */
        dest_p = &neoInfo.buffer[BYTES_PER_PIXEL];
    }
    else
    {
        /* Fill out the 1st buffer */
        dest_p = &neoInfo.buffer[0];
    }
    for (src_p = &buffer[0]; src_p < &buffer[BYTES_PER_PIXEL]; src_p++, dest_p++)
    {
        *dest_p = *src_p;
    }
    
    neoInfo.pxlIndex++;
}

/*
 * ===============================================================================
 * 
 * Name: neo_fifo_empty_isr
 * 
 * ===============================================================================
 */
/**
 * FIFO empty ISR
 * 
 * Grabs data from buffer and adds it to the FIFO.  If it finishes a pixel, it sets
 * the done pixel flag so the data for the next pixel is calculated.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_fifo_empty_isr()
{
    /* Statement added so interface can be polled instead of interrupt driven */
    if (*(R32 *)SCB1_INTR_TX & INTR_TX_SCB_EMPTY)
    {
        if (neoInfo.stat & STAT_RUNNING)
        {
            neo_fill_fifo();
        }
        
        /* Clear isr pending bit */
        *(R32 *)SCB1_INTR_TX = INTR_TX_SCB_EMPTY;
    }
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
    /* Check if new cycle needs to be started */
    if (neoInfo.stat & STAT_START_PROC)
    {
        neoInfo.stat &= ~STAT_START_PROC;
        neoInfo.stat |= STAT_RUNNING;
        neoInfo.pxlIndex = 0;
        neoInfo.isrCopyIdx = 0;

        /* Move to next pixel state */
        neoInfo.stateNum++;
        neoInfo.stateNum &= (MAX_STATE_NUM - 1);
        if ((neoInfo.stateNum & 0xf) == 0)
        {
            neoInfo.stat ^= STAT_BLINK_FAST_ON;
        }
        if (neoInfo.stateNum == 0)
        {
            neoInfo.stat ^= STAT_BLINK_SLOW_ON;
        }
        
        /* Fill out two buffers */
        neo_fill_buffer();
        neo_fill_buffer();
        
        /* Fill SPI FIFO to start transfer */
        neo_fill_fifo();
        
        /* Enable FIFO empty isr, clear bit and unmask it */
        *(R32 *)SCB1_INTR_TX = INTR_TX_SCB_EMPTY;
        *(R32 *)SCB1_INTR_TX_MASK &= ~INTR_TX_SCB_EMPTY;
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
    INT             pixel,
    INT             colorTblIdx)
{
    INT             pxlCmd;
   
    pxlCmd = neoInfo.pxlCmd[pixel];
    pxlCmd &= ~CMD_COLOR_TBL_MASK;
    pxlCmd |= colorTblIdx;
    neoInfo.pxlCmd[pixel] = pxlCmd;
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
    INT             pixel,
    INT             cmd)
{
    INT             pxlCmd;
   
    pxlCmd = neoInfo.pxlCmd[pixel];
    pxlCmd &= ~CMD_MASK;
    pxlCmd |= cmd;
    neoInfo.pxlCmd[pixel] = pxlCmd;
}

/* [] END OF FILE */
