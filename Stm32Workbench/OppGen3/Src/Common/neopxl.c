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
 *          Copyright© 2015 - 2019, Hugh Spahr
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
 * This is the file for driving Neopixels using a SPI bus.  This uses a
 * DMA to send the data to the SPI.  Neopixel data is presented 8 bits of green,
 * then red, then blue with msb first.
 *
 * This file requires a 10ms tick to start the neopixel processing.
 *
 *===============================================================================
 */
#include <stdlib.h>
#include "stdtypes.h"
#include "procdefs.h"
#include "gen2glob.h"
#include "neointf.h"

#define SPI_BITS_PER_NEO_BIT     4       /* 4 SPI bits are needed for a single NeoPixel bit */
                                         /* SPI clock is 48MHz/16 = 3MHz or 333ns/tick */
#define PWM_BITS_PER_NEO_BIT     8       /* 1 PWM byte is needed to send a single NeoPixel bit */
                                         /* PWM clock is 57/48MHz = 1.19us per NeoPixel bit */
#define MAX_NEOPIXELS            256

#define MAX_MULT_FACT_SHFT       5       /* 2^5 or 32 */
    
#define CMD_MASK                 0xe0
#define CMD_FADE_CMDS            0x40
#define CMD_COLOR_TBL_MASK       (NEOI_COLOR_TBL_SIZE - 1)
#define CMD_FAST_CMD             0x20
    
#define STAT_DMA_DATA            0
#define STAT_UPDATE_FADE         1
#define STAT_WAIT_FOR_TICK       2
#define STAT_DISABLED            0xff

#define PIXEL_HALF_ON            0x80
#define PIXEL_OFF                0x00

#define NUM_FADES                32

typedef struct
{
   INT              totTicks;
   INT              currTick;
   INT              offset;
   INT              numBytes;
} FADE_INFO;

typedef struct
{
   U8                stat;                /* Status */
   BOOL              tickOcc;             /* 10 ms tick occurred */
   INT               numPixels;           /* Number of pixels */
   INT               bytesPerPixel;       /* Number of bytes per pixel */
   INT               underflow;           /* Underflow count */
   INT               complUpd;            /* Number of completed updates */
   FADE_INFO         fadeInfo[NUM_FADES]; /* Number of fade groups supported */
   U8                *currPxlVal_p;       /* Ptr to array of current pixel values */
   U8                *newPxlVal_p;        /* Ptr to array of future pixel values */
   U32               *buf_p;              /* Holds pixel data to be DMA'd */
   FADE_INFO         *fade_p;             /* Current fade group being updated */
} NEO_INFO;

NEO_INFO neoInfo;

/* Note:  This is in little endian data format since DMA is little endian */
const U32                   NEO_BYTE_EXPAND[256] =
  { 0x88888888, 0x8c888888, 0xc8888888, 0xcc888888, 0x888c8888, 0x8c8c8888, 0xc88c8888, 0xcc8c8888,	/* 0x00 - 0x07 */
    0x88c88888, 0x8cc88888, 0xc8c88888, 0xccc88888, 0x88cc8888, 0x8ccc8888, 0xc8cc8888, 0xcccc8888,	/* 0x08 - 0x0f */
	0x88888c88, 0x8c888c88, 0xc8888c88, 0xcc888c88, 0x888c8c88, 0x8c8c8c88, 0xc88c8c88, 0xcc8c8c88,	/* 0x10 - 0x17 */
	0x88c88c88, 0x8cc88c88, 0xc8c88c88, 0xccc88c88, 0x88cc8c88, 0x8ccc8c88, 0xc8cc8c88, 0xcccc8c88,	/* 0x18 - 0x1f */
	0x8888c888, 0x8c88c888, 0xc888c888, 0xcc88c888, 0x888cc888, 0x8c8cc888, 0xc88cc888, 0xcc8cc888,	/* 0x20 - 0x07 */
	0x88c8c888, 0x8cc8c888, 0xc8c8c888, 0xccc8c888, 0x88ccc888, 0x8cccc888, 0xc8ccc888, 0xccccc888,	/* 0x28 - 0x2f */
	0x8888cc88, 0x8c88cc88, 0xc888cc88, 0xcc88cc88, 0x888ccc88, 0x8c8ccc88, 0xc88ccc88, 0xcc8ccc88,	/* 0x30 - 0x37 */
	0x88c8cc88, 0x8cc8cc88, 0xc8c8cc88, 0xccc8cc88, 0x88cccc88, 0x8ccccc88, 0xc8cccc88, 0xcccccc88,	/* 0x38 - 0x3f */
	0x8888888c, 0x8c88888c, 0xc888888c, 0xcc88888c, 0x888c888c, 0x8c8c888c, 0xc88c888c, 0xcc8c888c,	/* 0x40 - 0x47 */
    0x88c8888c, 0x8cc8888c, 0xc8c8888c, 0xccc8888c, 0x88cc888c, 0x8ccc888c, 0xc8cc888c, 0xcccc888c,	/* 0x48 - 0x4f */
	0x88888c8c, 0x8c888c8c, 0xc8888c8c, 0xcc888c8c, 0x888c8c8c, 0x8c8c8c8c, 0xc88c8c8c, 0xcc8c8c8c,	/* 0x50 - 0x57 */
	0x88c88c8c, 0x8cc88c8c, 0xc8c88c8c, 0xccc88c8c, 0x88cc8c8c, 0x8ccc8c8c, 0xc8cc8c8c, 0xcccc8c8c,	/* 0x58 - 0x5f */
	0x8888c88c, 0x8c88c88c, 0xc888c88c, 0xcc88c88c, 0x888cc88c, 0x8c8cc88c, 0xc88cc88c, 0xcc8cc88c,	/* 0x60 - 0x67 */
	0x88c8c88c, 0x8cc8c88c, 0xc8c8c88c, 0xccc8c88c, 0x88ccc88c, 0x8cccc88c, 0xc8ccc88c, 0xccccc88c,	/* 0x68 - 0x6f */
	0x8888cc8c, 0x8c88cc8c, 0xc888cc8c, 0xcc88cc8c, 0x888ccc8c, 0x8c8ccc8c, 0xc88ccc8c, 0xcc8ccc8c,	/* 0x70 - 0x77 */
	0x88c8cc8c, 0x8cc8cc8c, 0xc8c8cc8c, 0xccc8cc8c, 0x88cccc8c, 0x8ccccc8c, 0xc8cccc8c, 0xcccccc8c,	/* 0x78 - 0x7f */
	0x888888c8, 0x8c8888c8, 0xc88888c8, 0xcc8888c8, 0x888c88c8, 0x8c8c88c8, 0xc88c88c8, 0xcc8c88c8,	/* 0x80 - 0x87 */
    0x88c888c8, 0x8cc888c8, 0xc8c888c8, 0xccc888c8, 0x88cc88c8, 0x8ccc88c8, 0xc8cc88c8, 0xcccc88c8,	/* 0x88 - 0x8f */
	0x88888cc8, 0x8c888cc8, 0xc8888cc8, 0xcc888cc8, 0x888c8cc8, 0x8c8c8cc8, 0xc88c8cc8, 0xcc8c8cc8,	/* 0x90 - 0x97 */
	0x88c88cc8, 0x8cc88cc8, 0xc8c88cc8, 0xccc88cc8, 0x88cc8cc8, 0x8ccc8cc8, 0xc8cc8cc8, 0xcccc8cc8,	/* 0x98 - 0x9f */
	0x8888c8c8, 0x8c88c8c8, 0xc888c8c8, 0xcc88c8c8, 0x888cc8c8, 0x8c8cc8c8, 0xc88cc8c8, 0xcc8cc8c8,	/* 0xa0 - 0xa7 */
	0x88c8c8c8, 0x8cc8c8c8, 0xc8c8c8c8, 0xccc8c8c8, 0x88ccc8c8, 0x8cccc8c8, 0xc8ccc8c8, 0xccccc8c8,	/* 0xa8 - 0xaf */
	0x8888ccc8, 0x8c88ccc8, 0xc888ccc8, 0xcc88ccc8, 0x888cccc8, 0x8c8cccc8, 0xc88cccc8, 0xcc8cccc8,	/* 0xb0 - 0xb7 */
	0x88c8ccc8, 0x8cc8ccc8, 0xc8c8ccc8, 0xccc8ccc8, 0x88ccccc8, 0x8cccccc8, 0xc8ccccc8, 0xccccccc8,	/* 0xb8 - 0xbf */
	0x888888cc, 0x8c8888cc, 0xc88888cc, 0xcc8888cc, 0x888c88cc, 0x8c8c88cc, 0xc88c88cc, 0xcc8c88cc,	/* 0xc0 - 0xc7 */
    0x88c888cc, 0x8cc888cc, 0xc8c888cc, 0xccc888cc, 0x88cc88cc, 0x8ccc88cc, 0xc8cc88cc, 0xcccc88cc,	/* 0xc8 - 0xcf */
	0x88888ccc, 0x8c888ccc, 0xc8888ccc, 0xcc888ccc, 0x888c8ccc, 0x8c8c8ccc, 0xc88c8ccc, 0xcc8c8ccc,	/* 0xd0 - 0xd7 */
	0x88c88ccc, 0x8cc88ccc, 0xc8c88ccc, 0xccc88ccc, 0x88cc8ccc, 0x8ccc8ccc, 0xc8cc8ccc, 0xcccc8ccc,	/* 0xd8 - 0xdf */
	0x8888c8cc, 0x8c88c8cc, 0xc888c8cc, 0xcc88c8cc, 0x888cc8cc, 0x8c8cc8cc, 0xc88cc8cc, 0xcc8cc8cc,	/* 0xe0 - 0xe7 */
	0x88c8c8cc, 0x8cc8c8cc, 0xc8c8c8cc, 0xccc8c8cc, 0x88ccc8cc, 0x8cccc8cc, 0xc8ccc8cc, 0xccccc8cc,	/* 0xe8 - 0xef */
	0x8888cccc, 0x8c88cccc, 0xc888cccc, 0xcc88cccc, 0x888ccccc, 0x8c8ccccc, 0xc88ccccc, 0xcc8ccccc,	/* 0xf0 - 0xf7 */
	0x88c8cccc, 0x8cc8cccc, 0xc8c8cccc, 0xccc8cccc, 0x88cccccc, 0x8ccccccc, 0xc8cccccc, 0xcccccccc,	/* 0xf8 - 0xff */
  };

const U32                   NEO_NIBBLE_EXPAND[16] =
  { 0x13131313, 0x26131313, 0x13261313, 0x26261313,	/* 0x00 - 0x03 */
    0x13132613, 0x26132613, 0x13262613, 0x26262613, /* 0x04 - 0x07 */
    0x13131326, 0x26131326, 0x13261326, 0x26261326,	/* 0x08 - 0x0b */
    0x13132626, 0x26132626, 0x13262626, 0x26262626, /* 0x0c - 0x0f */
  };

/* Prototypes */
void neo_process_fade_record();

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
 * Turn pixels to default output, allocate memory, and reset state machine.
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
   INT               index;
   INT               offset;
   U8                *tmp1_p;
   U8                *tmp2_p;

#define SPI2_NEO 1

   /* HRS: Debug, should be configurable */
   neoInfo.bytesPerPixel = 3;

   /* Only initialize if Neo pixels are configured */
   neoInfo.stat = STAT_DISABLED;
   if ((gen2g_info.typeWingBrds & (1 << WING_NEO)) != 0)
   {
      /* Initialize the state machine to turn off all the LEDs, set indices to 0 */
      gen2g_info.haveNeo = TRUE;
      neoInfo.tickOcc = FALSE;
      neoInfo.underflow = 0;
      neoInfo.complUpd = 0;
      neoInfo.numPixels = numPixels;
      if (numPixels == 0)
      {
         neoInfo.numPixels = MAX_NEOPIXELS;
      }
      for (index = 0; index < NUM_FADES; index++)
      {
         neoInfo.fadeInfo[index].numBytes = 0;
      }
    
      /* Test for null on commands */
      neoInfo.currPxlVal_p = malloc(neoInfo.numPixels * neoInfo.bytesPerPixel);
      if (neoInfo.currPxlVal_p == NULL)
      {
         gen2g_info.error = ERR_MALLOC_FAIL;
         return(ERR_MALLOC_FAIL);
      }

      neoInfo.newPxlVal_p = malloc(neoInfo.numPixels * neoInfo.bytesPerPixel);
      if (neoInfo.newPxlVal_p == NULL)
      {
         gen2g_info.error = ERR_MALLOC_FAIL;
         return(ERR_MALLOC_FAIL);
      }

      /* Allocate neopixel DMA buffer memory */
#if PWM1_NEO
      neoInfo.buf_p = malloc((neoInfo.numPixels * neoInfo.bytesPerPixel * PWM_BITS_PER_NEO_BIT) + 1);
#endif
#if SPI2_NEO
      neoInfo.buf_p = malloc((neoInfo.numPixels * neoInfo.bytesPerPixel * SPI_BITS_PER_NEO_BIT) + 1);
#endif
      if (neoInfo.buf_p == NULL)
      {
         gen2g_info.error = ERR_MALLOC_FAIL;
         return(ERR_MALLOC_FAIL);
      }
#if PWM1_NEO
      // Count of zero turns off PWM at end of string
      *((U8 *)neoInfo.buf_p + (neoInfo.numPixels * neoInfo.bytesPerPixel * PWM_BITS_PER_NEO_BIT)) = 0;
#endif
#if SPI2_NEO
      *((U8 *)neoInfo.buf_p + (neoInfo.numPixels * neoInfo.bytesPerPixel * SPI_BITS_PER_NEO_BIT)) = 0;
#endif
    
      for (tmp1_p = neoInfo.currPxlVal_p, tmp2_p = neoInfo.newPxlVal_p;
         tmp1_p < neoInfo.currPxlVal_p + (neoInfo.numPixels * neoInfo.bytesPerPixel); tmp1_p++, tmp2_p++)
      {
         *tmp1_p = PIXEL_OFF;
         *tmp2_p = PIXEL_OFF;
      }

      /* Set initial values to verify NeoPixels are working */
      for (index = 0; index < neoInfo.numPixels; index++)
      {
    	  offset = index % neoInfo.bytesPerPixel;
    	  *(neoInfo.currPxlVal_p + ((index * neoInfo.bytesPerPixel) + offset)) = PIXEL_HALF_ON;
    	  *(neoInfo.newPxlVal_p + ((index * neoInfo.bytesPerPixel) + offset)) = PIXEL_HALF_ON;
      }

      neo_fill_out_dma_data(0, neoInfo.currPxlVal_p, neoInfo.numPixels * neoInfo.bytesPerPixel);

#if SPI2_NEO
      /* HRS:  For SPI2 */
      /* Setup GPIO port */
      gpioBBase_p->CRH &= ~0xf0000000;
      gpioBBase_p->CRH |= 0xb0000000;  // Alternate function push/pull output 50MHz
      gpioBBase_p->BSRR = 0x80000000;

      /* Enable clocks to SPI2 and DMA1 */
      rccBase_p->AHBENR |= 0x00000001;  // DMA1
      rccBase_p->APB1ENR |= 0x00004000;  // SPI2

      /* Set up SPI2 */
      spi2Base_p->CR1 = SPIx_CR1_SPE | SPIx_CR1_BR_8 | SPIx_CR1_MSTR;
      spi2Base_p->CR2 = SPIx_CR2_TXDMAEN;

      /* Set up DMA */
      dma1Base_p->CPAR5 = (R32)&spi2Base_p->DR;
      dma1Base_p->CMAR5 = (R32)neoInfo.buf_p;
      dma1Base_p->CNDTR5 = (neoInfo.numPixels * neoInfo.bytesPerPixel * SPI_BITS_PER_NEO_BIT) + 1;
      dma1Base_p->CCR5 = DMAx_CCR_MINC | DMAx_CCR_DIR | DMAx_CCR_EN;
#endif

#if PWM1_NEO
      /* HRS: For PWM1 */
      /* Setup GPIO port */
      gpioBBase_p->CRH &= ~0xf0000000;
      gpioBBase_p->CRH |= 0xb0000000;  // Alternate function push/pull output 50MHz
      gpioBBase_p->BSRR = 0x80000000;

      /* Enable clocks to TIM1 and DMA1 */
      rccBase_p->AHBENR |= 0x00000001;  // DMA1
      rccBase_p->APB2ENR |= 0x00000800;  // TIM1

      tim1Base_p->PSC = 0;
      tim1Base_p->ARR = 56;
      // tim1Base_p->CCR3 = 0x13;  // HRS:  No DMA set duty cycle
      tim1Base_p->CCMR1 = 0x0000;
      tim1Base_p->CCMR2 = 0x0068;
      tim1Base_p->EGR = 0x0001;
      tim1Base_p->SMCR = 0x0000;
      // DMA bits
      tim1Base_p->DIER = 0x0800; // CC3DE = 1
      tim1Base_p->BDTR = 0x8000; // MOE = 1, OSSR = 0, OSSI = x
      tim1Base_p->CCER = 0x0400; // CC3NP = 0, CC3NE = 1, CC3P = x, CC3E = 0
      tim1Base_p->CR2 = 0x0000;
      tim1Base_p->CR1 = 0x0001;

      /* Set up DMA1 Chan 6 */
      dma1Base_p->CPAR6 = (R32)&tim1Base_p->CCR3;
      dma1Base_p->CMAR6 = (R32)neoInfo.buf_p;
      dma1Base_p->CNDTR6 = (neoInfo.numPixels * neoInfo.bytesPerPixel * PWM_BITS_PER_NEO_BIT) + 1;
      dma1Base_p->CCR6 = DMAx_CCR_PSIZE16 | DMAx_CCR_MINC | DMAx_CCR_DIR | DMAx_CCR_EN;
#endif

      neoInfo.stat = STAT_DMA_DATA;
   }
    
   /* Register a 40ms repeating tick function, register FIFO empty if necessary */
   return(NO_ERRORS);
}

/*
 * ===============================================================================
 * 
 * Name: neo_10ms_tick
 *
 * ===============================================================================
 */
/**
 * Neopixel 10 ms tick
 *
 * Set the flag to start another Neopixel DMA.
 *
 * @param   None
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void neo_10ms_tick()
{
   neoInfo.tickOcc = TRUE;
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
#define STAT_DMA_DATA            0
#define STAT_UPDATE_FADE         1
#define STAT_WAIT_FOR_TICK       2
#define STAT_DISABLED            0xff
   if (gen2g_info.validCfg && gen2g_info.haveNeo)
   {
      if ((neoInfo.stat == STAT_DMA_DATA) && (dma1Base_p->CNDTR5 == 0))
      {
         /* Look for a fade update group */
         neoInfo.fade_p = &neoInfo.fadeInfo[0];
      }
      if (neoInfo.stat == STAT_UPDATE_FADE)
      {
         if (neoInfo.fade_p->numBytes != 0)
         {
            /* Process this fade info record */
        	neo_process_fade_record();
            neoInfo.fade_p++;
         }

         /* Find next fade record that needs to be updated */
         while ((neoInfo.fade_p < &neoInfo.fadeInfo[NUM_FADES]) && (neoInfo.fade_p->numBytes == 0))
         {
            neoInfo.fade_p++;
         }
         if (neoInfo.fade_p >= &neoInfo.fadeInfo[NUM_FADES])
         {
            neoInfo.stat = STAT_WAIT_FOR_TICK;
         }
      }
      if ((neoInfo.stat == STAT_WAIT_FOR_TICK) && neoInfo.tickOcc)
      {
         neoInfo.stat = STAT_DMA_DATA;
#if SPI2_NEO
         dma1Base_p->CNDTR5 = (neoInfo.numPixels * neoInfo.bytesPerPixel * SPI_BITS_PER_NEO_BIT) + 1;
         dma1Base_p->CCR5 = DMAx_CCR_MINC | DMAx_CCR_DIR | DMAx_CCR_EN;
#endif
       }
   }
}

/*
 * ===============================================================================
 * 
 * Name: neo_process_fade_record
 * 
 * ===============================================================================
 */
/**
 * Neopixel process fade record
 * 
 * Process a fade record
 * 
 * @param   None
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void neo_process_fade_record()
{
   INT               index;
   U8                *src_p;
   U8                *dst_p;
   U32               *dma_p;
   U8                newData;
   U8                currData;
   U8                diff;

   /* Check if fade is finished, if so copy newPxlVal into currPxlVal
    *   and update DMA data.
    */
   src_p = neoInfo.newPxlVal_p + neoInfo.fade_p->offset;
   dst_p = neoInfo.currPxlVal_p + neoInfo.fade_p->offset;
   dma_p = neoInfo.buf_p +  neoInfo.fade_p->offset;
   if (neoInfo.fade_p->totTicks >= neoInfo.fade_p->currTick)
   {
      for (index = 0; index < neoInfo.fade_p->numBytes; index++)
      {
         newData = *src_p++;
         *dst_p++ = newData;
         *dma_p++ = NEO_BYTE_EXPAND[newData];
      }

      /* Mark fade record as not used */
      neoInfo.fade_p->numBytes = 0;
   }
   else
   {
      for (index = 0; index < neoInfo.fade_p->numBytes; index++)
      {
         newData = *src_p++;
         currData = *dst_p++;
         if (newData > currData)
         {
            diff = newData - currData;
         }
         else
         {
            diff = currData - newData;
         }
         diff = (diff * neoInfo.fade_p->currTick)/neoInfo.fade_p->totTicks;
         if (newData > currData)
         {
            currData += diff;
         }
         else
         {
             currData -= diff;
         }
         *dma_p++ = NEO_BYTE_EXPAND[currData];
         neoInfo.fade_p->currTick++;
      }
   }
}

/*
 * ===============================================================================
 *
 * Name: neo_fill_out_dma_data
 *
 * ===============================================================================
 */
/**
 * Neopixel fill out DMA data
 *
 * Update the pixel's command
 *
 * @param   offset      [in]        Byte offset to start conversion
 * @param   srcData_p   [in]        Pointer to source of data
 * @param   numBytes    [in]        Number of bytes to convert
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void neo_fill_out_dma_data(
   INT                  offset,
   U8                   *srcData_p,
   INT                  numBytes)
{
   U32                  *dst_p;
   U8                   *end_p;
   U8                   data;

   dst_p = neoInfo.buf_p + (offset << 1);
   for (end_p = srcData_p + numBytes; srcData_p < end_p; srcData_p++)
   {
      data = *srcData_p;
#if PWM1_NEO
      *dst_p++ = NEO_NIBBLE_EXPAND[data >> 4];
      *dst_p++ = NEO_NIBBLE_EXPAND[data & 0x0f];
#endif
#if SPI2_NEO
      *dst_p++ = NEO_BYTE_EXPAND[data];
#endif
   }
}

/* [] END OF FILE */
