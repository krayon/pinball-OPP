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
 *     PPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP    OOO      OOO    PPP
 *               PPP     OOOOOOOOOO     PPP
 *              PPPPP      OOOOOO      PPPPP
 *
 * @file:   main.c
 * @author: Hugh Spahr
 * @date:   9/21/2017
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
 * Main file showing a simple useage of the NeoPixel library.  By defining the
 * USE_FIFO_INTERRUPTS to 0, the program uses polling to fill the FIFO which
 * writes the data to the NeoPixels.  By defining the USE_FIFO_INTERRUPTS to 1,
 * the program uses interrupts to fill the FIFO.  (Using interrupts is best since
 * the latency to fill the FIFO is kept to a minimum and reduces the chance of a
 * FIFO underflow.
 *
 * A 1 ms system tick is used to set a flag every 500 ms to start processing
 * the NeoPixel chain.  This timer must be at least 50 us longer than the time
 * that it takes to process the NeoPixels to guarantee the end of the cycle dead
 * time.  RGB NeoPixels (3 bytes per NeoPixel) take 30 us per NeoPixel to
 * transmit the data.  (24 * 1.25 us = 30 us).  If programming 90 NeoPixels, the
 * start time must be at least (90 * 30 us) + 50 us = 2.75 ms.  (I'd give it a
 * little wiggle room for interrupt latencies and such).
 *
 * This library could easily be converted to RGBW NeoPixels by changing the
 * width of the FIFO to 32 bits, and the initial value of the UDB D0 register
 * from 0x000018 to 0x00000020.  No other changes should be necessary.
 *
 * Note:  The NeoClock must be 4.8 MHz and fed through a T flipflop so the clock
 * signal can be used as a data signal.  This is used to detect the rising edge
 * of the 2.4 MHz signal to insure timings are correct.
 *
 *===============================================================================
 */
#include <project.h>
#include "SysClock.h"
#include "isr_SysTick.h"
#include "isr_FIFOEmpty.h"

#define USE_FIFO_INTERRUPTS 1

#if USE_FIFO_INTERRUPTS != 0
#include "isr_FIFOEmpty.h"
#endif

#define FALSE 0
#define TRUE  !FALSE

static int data[] = { 0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0x00ffff, 0xff00ff, 0xffffff, 0x000000 };
#define NUM_LEDS ((int)(sizeof(data)/sizeof(int)))

int startChainProc = FALSE;         /* Used to start Neopixel processing every 500 ms */
int updateChain = FALSE;            /* Flag set to false when last Neopixel data written to FIFO */
int currIndex = 0;
int numLedsUpdated = 0;

CY_ISR(SysTick_isr)
{
    static int ms_count = 0;
    
    SysTick_ClearInterrupt(SysTick_INTR_MASK_TC);
    ms_count++;
    
    /* Check if 500 ms elapsed */
    if (ms_count == 500)
    {
        startChainProc = TRUE;
        ms_count = 0;
    }
}

#if USE_FIFO_INTERRUPTS != 0
CY_ISR(FIFOEmpty_isr)
{
   /* Try writing to the chain, returns non-zero if write failed
    * since FIFO was full.
    */
   while (updateChain && (NeoPixel_WriteFifo(data[currIndex]) == 0))
   {
      currIndex++;
      if (currIndex >= NUM_LEDS)
      {
         currIndex = 0;
      }
      numLedsUpdated++;
      if (numLedsUpdated >= NUM_LEDS)
      {
         /* All LEDs updated, so end updating, mask FIFO empty isr */
         updateChain = FALSE;
         isr_FIFOEmpty_Disable();
      }
   }
   isr_FIFOEmpty_ClearPending();
}
#endif

int main()
{
   int startLed = 0;
    
   NeoClock_Start();        /* 4.8 MHz/2 or 2.4 MHz used for NeoPixel bit timings.  Must go through T-flip flop
                             * so it can be used as a data signal
                             */
   UDBClock_Start();        /* 24MHz clock used to move through UDB state machine */

#if USE_FIFO_INTERRUPTS != 0
   isr_FIFOEmpty_StartEx(FIFOEmpty_isr);
   isr_FIFOEmpty_Disable();
#endif

   /* Start the update chain timer, and enable the interrupt */
   SysClock_Start();        /* Clock used for system tick */
   isr_SysTick_StartEx(SysTick_isr);   /* Connect the ISR */
   SysTick_Start();
   CyGlobalIntEnable;       /* Enable global interrupts */

   while (TRUE)
   {
      unsigned long test = *(unsigned long *)0x40010008;
      test++;
    
      /* Timer kicks off start chain processing */
      if (startChainProc)
      {
         startChainProc = FALSE;
         updateChain = TRUE;
         currIndex = startLed;
         startLed++;
         if (startLed >= NUM_LEDS)
         {
            startLed = 0;
         }
         numLedsUpdated = 0;
#if USE_FIFO_INTERRUPTS != 0
         isr_FIFOEmpty_Enable();
#endif
      }
    
      /* Try writing to the chain, returns non-zero if write failed
       * since FIFO was full.
       */
#if USE_FIFO_INTERRUPTS == 0
      if (updateChain && (NeoPixel_WriteFifo(data[currIndex]) == 0))
      {
         currIndex++;
         if (currIndex >= NUM_LEDS)
         {
            currIndex = 0;
         }
         numLedsUpdated++;
         if (numLedsUpdated >= NUM_LEDS)
         {
            updateChain = FALSE;
         }
      }
#endif
   }
}

/* [] END OF FILE */
