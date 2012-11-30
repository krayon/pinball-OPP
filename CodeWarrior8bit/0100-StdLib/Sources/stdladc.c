/*
 *===============================================================================
 *
 *          SSSS
 *        SSSSSSSs                 DDD
 *       SSS    SSS     TTT        DDD            Hugh Spahr
 *      SSS  LLL SSS    TTT        DDD            Standard
 *       SSS LLL      TTTTTTT      DDD            Library
 *         SSSSL      TTTTTTT      DDD  
 *          SSSSS       TTT        DDD
 *           LSSSS      TTT    DDDDDDD
 *           LLLSSS     TTT  DDDDDDDDD
 *      SSS  LLL SSS    TTT DDD    DDD
 *       SSS LLLSSS     TTT DDD    DDD
 *        SSSSSSSS      TTT  DDDDDDDDD
 *          SSSS        TTT    DDDD DD
 *           LLL
 *           LLL   I    BBB
 *           LLL  III   BBB
 *           LLL   I    BBB
 *           LLL        BBB
 *           LLL  III   BBB
 *           LLL  III   BBB
 *           LLL  III   BBBBBBB
 *           LLL  III   BBBBBBBBB
 *           LLL  III   BBB    BBB
 *           LLL        BBB    BBB
 *           LLLLLLLLL  BBBBBBBBB
 *           LLLLLLLLL  BB BBBB
 *
 * @file:   stdladc.c
 * @author: Hugh Spahr
 * @date:   6/12/2008
 *
 * @note:    Copyright© 2008, Hugh Spahr
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
 * This is the analog to digital converter utility file in the Standard
 * Library.  It contains functions to configure ADC sampling.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "stdlglob.h"

#define TAKE_ADC_TIMES      0 

#define MAX_TIME_READINGS   8

typedef struct
{
  STDLI_ADC_CHAN_T          *adcChan_p;
  STDLI_ADC_CHAN_T          *curChan_p;
  U16                       adcSlip;
  BOOL                      slowAdc;
  
#if (TAKE_ADC_TIMES != 0)
  U8                        timeSample;
  STDLI_ELAPSED_TIME_T      timeLen[MAX_TIME_READINGS];
#endif
} STDLADC_ADC_T;

STDLADC_ADC_T               stdladc_glob;

/*
 * ===============================================================================
 * 
 * Name: stdladc_init_adc
 * 
 * ===============================================================================
 */
/**
 * Initialize the ADC
 * 
 * Initialize the ADC including setting up a clock  
 * 
 * @param   adcCfg      [in]   STDLI_ADC_FAST every 1 ms, STDLI_ADC_SLOW once/tick
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdladc_init_adc(
  STDLI_ADC_CFG_E           adcCfg)       /* STDLI_ADC_FAST/SLOW/12BIT/10BIT */
{
  U8                        tmp;
  
  if (adcCfg & STDLI_ADC_10BIT)
  {
    tmp = 0x18;                           /* Long smpl, 10 bits, bus clk */
  }
  else
  {
    tmp = 0x14;                           /* Long smpl, 12 bits, bus clk */
  }
  if (adcCfg & STDLI_ADC_FAST_OSC)
  {
    tmp |= 0x40;                          /* Use busclk/4 */
  }
  ADCCFG = tmp;
  ADCSC2 = 0x00;                          /* SW trigger,  no compare function */
  ADCSC1 = STDLI_ADC_MOD_DISABLE;         /* Disable conversions */
  
  stdladc_glob.adcChan_p = NULL;
  stdladc_glob.curChan_p = NULL;
  stdladc_glob.adcSlip = 0;
  stdladc_glob.slowAdc = ((adcCfg & STDLI_ADC_SLOW) ? TRUE : FALSE);
#if (TAKE_ADC_TIMES != 0)
  stdladc_glob.timeSample = 0;
#endif
} /* End stdladc_init_adc */

/*
 * ===============================================================================
 * 
 * Name: stdladc_reg_adc_chan
 * 
 * ===============================================================================
 */
/**
 * Register the ADC channel to be sampled
 * 
 * Register the ADC channel by adding it to the ADC linked list.  If the
 * ADC channel is previously configured, an error is returned.  Set up the
 * pin control and the digital port. 
 * 
 * @param   chanInfo    [in]    ptr to ADC chan, and callback info
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdladc_reg_adc_chan(
  STDLI_ADC_CHAN_T          *adcChan_p)   /* ptr to ADC chan, callback info */
{
  STDLI_ADC_CHAN_T          **prevAdcChan_pp;
  STDLI_ADC_CHAN_T          *curAdcChan_p;
  U8                        chan;
  U8                        port;
  U8                        mask;
  U8                        smallModel;
  U8                        poll;

#define APCTL1_REG_ADDR     0x0017
#define APCTL_REG_MASK      0x18
#define APCTL_REG_SHIFT     3
#define APCTL_BIT_MASK      0x07
#define INT_ENABLE          0x40
  
  /* Add the ADC channel to the ADC chain */
  prevAdcChan_pp = &stdladc_glob.adcChan_p;
  curAdcChan_p = *prevAdcChan_pp;
  smallModel = adcChan_p->chan & STDLI_ADC_DIG_SMALL_MODEL;
  poll = adcChan_p->chan & STDLI_ADC_POLL_MODE;
  adcChan_p->chan &= ~(STDLI_ADC_DIG_SMALL_MODEL | STDLI_ADC_POLL_MODE);
  chan = adcChan_p->chan;
  if (!poll)
  {
    adcChan_p->chan |= INT_ENABLE;
  }
  while ((curAdcChan_p != NULL) && (curAdcChan_p->chan < adcChan_p->chan))
  {
    prevAdcChan_pp = &curAdcChan_p->next_p;
    curAdcChan_p = *prevAdcChan_pp;
  }
  
  /* Check if user is registering the channel twice */
  if ((curAdcChan_p != NULL) && (curAdcChan_p->chan == adcChan_p->chan))
  {
    return (STDLI_ADC_CHAN_REG_TWICE);
  }
  adcChan_p->next_p = curAdcChan_p;
  *prevAdcChan_pp = adcChan_p;
  
  /* Set up the pin control if needed */
  if (chan <= STDLI_ADC_PORT23)
  {
    port = ((chan & APCTL_REG_MASK) >> APCTL_REG_SHIFT);
    mask = (1 << (chan & APCTL_BIT_MASK));
    *(U8 *)(APCTL1_REG_ADDR + port) = mask;
  } 
  return(0);
} /* End stdladc_reg_adc_chan */

/*
 * ===============================================================================
 * 
 * Name: stdladc_start_adc_sampling
 * 
 * ===============================================================================
 */
/**
 * Start the ADC sampling
 * 
 * At the next 1 ms clock tick, the ADC will start sampling, and move from the
 * lowest channel to the highest channel.  
 * 
 * @param   None
 * @return  STDLI_ADC_NO_CHAN_REG   - No ADC channels registered  
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdladc_start_adc_sampling(void)
{
  if (stdladc_glob.adcChan_p == NULL)
  {
    return(STDLI_ADC_NO_CHAN_REG);
  }
  if (stdladc_glob.slowAdc && (stdlg_info.slowAdc_fp == NULL))
  {
    stdlg_info.slowAdc_fp = stdladc_start_adc_sampling;
  }
  if (!stdladc_glob.slowAdc && (stdlg_info.fastAdc_fp == NULL))
  {
    stdlg_info.fastAdc_fp = stdladc_start_adc_sampling;
  }
  if (stdladc_glob.curChan_p != NULL)
  {
    /* Oh, no */
    stdladc_glob.adcSlip++;
  }
  else
  {
#if (TAKE_ADC_TIMES != 0)
    stdltime_get_curr_time(&stdladc_glob.timeLen[stdladc_glob.timeSample].startTime);
#endif    
  
    /* Start the conversion.  The interrupt enable bit is already set in chan */
    stdladc_glob.curChan_p = stdladc_glob.adcChan_p;
    ADCSC1 = stdladc_glob.curChan_p->chan;
  }
  return(0);
} /* End stdladc_start_adc_sampling */

/*
 * ===============================================================================
 * 
 * Name: stdladc_adc_complete_isr
 * 
 * ===============================================================================
 */
/**
 * ADC conversion complete isr
 * 
 * Call the ADC callback function to hand back the data.  If another channel
 * is registered, start the next conversion. 
 * 
 * @param None 
 * @return None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void stdladc_adc_complete(void)
{
  STDLI_ADC_CHAN_T          *curAdc_p;
  
  /* Call the callback function */
  curAdc_p = stdladc_glob.curChan_p;
  curAdc_p->adcSample_fp(curAdc_p->cbParm, ADCR);
    
  /* Check if another conversion needs to be done */
  curAdc_p = curAdc_p->next_p;
  stdladc_glob.curChan_p = curAdc_p;
  if (curAdc_p)
  {
    ADCSC1 = curAdc_p->chan;
  }
#if (TAKE_ADC_TIMES != 0)
  else
  {
    stdltime_get_elapsed_time(&stdladc_glob.timeLen[stdladc_glob.timeSample]);
    stdladc_glob.timeSample++;
    stdladc_glob.timeSample &= (MAX_TIME_READINGS - 1);
  }
#endif
} /* End stdladc_adc_complete */

interrupt void stdladc_adc_complete_isr(void)
{
  stdladc_adc_complete();
} /* End stdladc_adc_complete_isr */

void stdladc_adc_complete_poll(void)
{
#define ADCSC1_CONV_COMP    0x80

  if (ADCSC1 & ADCSC1_CONV_COMP)
  {
    stdladc_adc_complete();
  }
} /* End stdladc_adc_complete_poll */

