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
 * @file:   stdlpwm.c
 * @author: Hugh Spahr
 * @date:   6/25/2008
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
 * This is the pulse width modulation utility file in the Standard
 * Library.  It contains functions to generate PWM signals, and capture pulse
 * lengths.
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "stdlglob.h"

#define TIMER1_ADDR         0x20    /* Address of first timer */
#define STDL_FILE_ID        0xff    /* File ID for logging errors */
#define CAP_INT_EN          0x40
#define CHAN_INT_FLAG       0x80
  
typedef struct
{
  U8                        TPMxSC;
  U16                       TPMxCNT;
  U16                       TPMxMOD;
} STDLPWM_TIMER_REG_T;

typedef struct
{
  U8                        TPMxCnSC;
  U16                       TPMxCnV;
} STDLPWM_CHAN_REG_T;

typedef struct
{
  STDLPWM_TIMER_REG_T       timer;
  STDLPWM_CHAN_REG_T        chan[STDLI_MAX_PWM_CHAN];
} STDLPWM_REG_T;

typedef struct
{
  STDLI_CAP_T               *capInfo_p;
  U8                        cfgdPwmChan;
  U8                        actCapChan;
} STDLPWM_PWM_T;

STDLPWM_PWM_T               stdlpwm_glob;

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_init_pwm_module
 * 
 * ===============================================================================
 */
/**
 * Initialize the PWM module
 * 
 * Clear the capture ptr and configed PWM channel bitmask.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlpwm_init_pwm_module(void)
{
  stdlpwm_glob.capInfo_p = NULL;
  stdlpwm_glob.cfgdPwmChan = 0;
  stdlpwm_glob.actCapChan = 0;
} /* End stdlpwm_init_pwm_module */

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_set_tpm1_period
 * 
 * ===============================================================================
 */
/**
 * Set TPM1 period
 * 
 * Initialize the PWM timer to a period.
 * 
 * @param   maxPeriod   [in]    Maximum period in ticks.  Each tick is 1 us.
 * @return  None
 * 
 * @pre     None 
 * @note    This assumes the bus clock is 8 MHz.  It sets the base clock
 *          frequency to 1 us.
 * 
 * ===============================================================================
 */
void stdlpwm_set_tpm1_period(
  U16                       maxPeriod)    /* Max period in ticks */
{
  TPM1MOD = maxPeriod - 1;      /* Set timing period */
  TPM1SC = 0x0b;                /* No center PWM, use busclk, and clk/8 */
} /* End stdlpwm_set_tpm1_period */

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_cap_tick_func
 * 
 * ===============================================================================
 */
/**
 * Capture tick function
 * 
 * The capture tick function is installed when a capture channel is configed.
 * It checks if a capture measurement is running, and if so, increments the
 * tick counter.  If the tick counter gets to 255 ticks, it stops the capture
 * and calls the callback function indicating the capture failed.
 * 
 * @param   capChan     [in]    TPM number and channel
 * @param   capDone_fp  [in]    Capture done function ptr
 * @param   cbParm      [in]    Callback param
 * @param   maxTicks    [in]    Max sys ticks before capture times out
 * @return  STDLI_CAP_CHAN_PREV_CFG   - capture channel previously configed
 *          STDLI_TIMER_NOT_CFG       - TPM timer is not started
 * 
 * @pre     TPM timer must be started. 
 * @note    The passed structure is added to the capture linked list, so it
 *          must be statically allocated.
 * 
 * ===============================================================================
 */
void stdlpwm_cap_tick_func(
  U16                       cbParam)
{
  STDLI_CAP_T               *curCfg_p;
  STDLPWM_REG_T             *reg_p;
  
  /* Check if any captures are happening */
  cbParam = 0;
  if (stdlpwm_glob.actCapChan)
  {
    for (curCfg_p = stdlpwm_glob.capInfo_p; curCfg_p != NULL;
      curCfg_p = curCfg_p->next_p)
    {
      if (curCfg_p->state != STDLI_CAP_IDLE)
      {
        /* Check if this channel has timed out */
        curCfg_p->tickCnt++;
        if (curCfg_p->tickCnt == curCfg_p->maxTicks)
        {
          /* This channel has timed out */
          reg_p = (STDLPWM_REG_T *)((U8)TIMER1_ADDR +
            (curCfg_p->capChan & STDLI_TPM_MASK));
          reg_p->chan[curCfg_p->capChan & STDLI_PWM_CHAN_MASK].TPMxCnSC &=
            ~(CHAN_INT_FLAG | CAP_INT_EN);
          curCfg_p->state = STDLI_CAP_IDLE;
          stdlpwm_glob.actCapChan--;
    
          /* Call the callback function, indicate timeout */
          curCfg_p->capDone_fp(curCfg_p->cbParm, STDLI_CAP_TIMEOUT);
        }
      }
    }
    
  }
} /* End stdlpwm_cap_tick_func */

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_config_cap_chan
 * 
 * ===============================================================================
 */
/**
 * Configure a PWM capture channel
 * 
 * Verify the channel has not been previously configured.  Insure the clock
 * is configured.  Initialize the state and add to the capture linked list.
 * 
 * @param   capChan     [in]    TPM number and channel
 * @param   capDone_fp  [in]    Capture done function ptr
 * @param   cbParm      [in]    Callback param
 * @return  STDLI_CAP_CHAN_PREV_CFG   - capture channel previously configed
 *          STDLI_TIMER_NOT_CFG       - TPM timer is not started
 * 
 * @pre     TPM timer must be started. 
 * @note    The passed structure is added to the capture linked list, so it
 *          must be statically allocated.
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdlpwm_config_cap_chan(
  STDLI_CAP_T               *capCfg_p)    /* Capture cfg with TPM num, chan num,
                                           *    done func ptr, and callback param.
                                           */
{
  STDLI_CAP_T               *curCfg_p;
  STDLPWM_REG_T             *reg_p;
  U8                        pin;
  STDLI_ERR_E               error;
  STDLI_TIMER_EVENT_T       timeEvt;

#define CLOCK_CFG_MASK      0x18
#define INPUT_CAP_RISE_EDGE 0x04
  
  /* Verify channel is not previously configured */
  for (curCfg_p = stdlpwm_glob.capInfo_p;
    (curCfg_p != NULL) && (curCfg_p->capChan != capCfg_p->capChan);
    curCfg_p = curCfg_p->next_p)
  {
    /* Note: No statements */
  }
  if (curCfg_p)
  {
    return(STDLI_CAP_CHAN_PREV_CFG);
  }

  /* Verify the clock has been configured */
  reg_p = (STDLPWM_REG_T *)((U8)TIMER1_ADDR +
    (capCfg_p->capChan & STDLI_TPM_MASK));
  if ((reg_p->timer.TPMxSC & CLOCK_CFG_MASK) == 0)
  {
    return(STDLI_TIMER_NOT_CFG);
  }
  
  /* If this is the first cap chan, set up the tick func */
  if (stdlpwm_glob.capInfo_p == NULL)
  {
    timeEvt.time = 1;
    timeEvt.timeout_fp = stdlpwm_cap_tick_func;
    timeEvt.cbParm = 0;
    error = stdltime_reg_timer_func(&timeEvt, 0);
    if (error)
    {
      STDLI_K_FATAL_M((U16)STDLI_CRITICAL_FAIL | error, 0, 0);
    }
  }
  
  /* Initialize the state and add to list */
  capCfg_p->state = STDLI_CAP_IDLE;
  DisableInterrupts;
  capCfg_p->next_p = stdlpwm_glob.capInfo_p;
  stdlpwm_glob.capInfo_p = capCfg_p;
  EnableInterrupts;
  
  /* Set up the hardware bits, and rising edge input capture */
  reg_p->chan[capCfg_p->capChan & STDLI_PWM_CHAN_MASK].TPMxCnSC =
    INPUT_CAP_RISE_EDGE;
  if ((capCfg_p->capChan & STDLI_TPM_MASK) == 0)
  {
    /* Timer 1, bits 0, and 1 are for timer 2 */
    pin = capCfg_p->capChan + 2;
  }
  else
  {
    /* Mask of timer 2 bit */
    pin = capCfg_p->capChan & STDLI_PWM_CHAN_MASK;
  }
  stdldigio_config_dig_port((capCfg_p->capChan & STDLI_TPM_DIG_SMALL_MODEL) |
    STDLI_DIG_PORT_D | STDLI_DIG_PULLUP, 1 << pin, 0);
    
  return(0);
} /* End stdlpwm_config_cap_chan */

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_start_cap_chan
 * 
 * ===============================================================================
 */
/**
 * Start a PWM capture channel
 * 
 * Start a prev configed capture channel.  Find capture channel on linked
 * list, verify it isn't currently running, and start a new capture calculation.
 * 
 * @param   capChan     [in]    TPM number and channel
 * @return  STDLI_CAP_CHAN_NOT_CFG    - capture channel not configed
 *          STDLI_CAP_CUR_RUNNING     - capture is currently running
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdlpwm_start_cap_chan(
  STDLI_TPM_CHAN_E          capChan)      /* TPM number and channel */
{
  STDLI_CAP_T               *curCfg_p;
  STDLPWM_REG_T             *reg_p;
  U8                        chan;
  U8                        tmpVal;

  /* Find previously configured capture channel */
  for (curCfg_p = stdlpwm_glob.capInfo_p;
    (curCfg_p != NULL) && (curCfg_p->capChan != capChan);
    curCfg_p = curCfg_p->next_p)
  {
    /* Note: No statements */
  }
  if (curCfg_p == NULL)
  {
    return(STDLI_CAP_CHAN_NOT_CFG);
  }

  /* Verify capture calc isn't currently running */
  if (curCfg_p->state != STDLI_CAP_IDLE)
  {
    return(STDLI_CAP_CUR_RUNNING);
  }
  
  /* Start the capture calculation, change state, enable int */
  reg_p = (STDLPWM_REG_T *)((U8)TIMER1_ADDR +
    (capChan & STDLI_TPM_MASK));
  chan = capChan & STDLI_PWM_CHAN_MASK;
  curCfg_p->tickCnt = 0;
  curCfg_p->state = STDLI_CAP_START;
  tmpVal = reg_p->chan[chan].TPMxCnSC;
  tmpVal |= CAP_INT_EN;
  tmpVal &= ~CHAN_INT_FLAG;
  reg_p->chan[chan].TPMxCnSC = tmpVal;
  DisableInterrupts;
  stdlpwm_glob.actCapChan++;
  EnableInterrupts;
  return(0);
} /* End stdlpwm_start_cap_chan */

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_read_capture_value
 * 
 * ===============================================================================
 */
/**
 * Read capture value
 * 
 * Find the capture channel.  If this is the first capture, grab the count value,
 * clear the interrupt and update the state.  If this is the second capture, grab
 * the count value, disable the interrupt, calculate the count diff, and call the
 * callback function.
 * 
 * @param   capChan     [in]    TPM number and channel
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlpwm_read_capture_value(
  STDLI_TPM_CHAN_E          capChan)      /* TPM number and channel */
{
  STDLI_CAP_T               *curCfg_p;
  STDLPWM_REG_T             *reg_p;
  U8                        chan;
  U16                       endCnt;
  
  /* Find previously configured capture channel */
  for (curCfg_p = stdlpwm_glob.capInfo_p;
    (curCfg_p != NULL) && (curCfg_p->capChan != capChan);
    curCfg_p = curCfg_p->next_p)
  {
    /* Note: No statements */
  }
  if (curCfg_p == NULL)
  {
    /* This should never happen */
    STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
      STDLI_CAP_CHAN_NOT_CFG) , 0, 0);
  }
  
  /* Start the capture calculation, change state, enable int */
  reg_p = (STDLPWM_REG_T *)((U8)TIMER1_ADDR +
    (capChan & STDLI_TPM_MASK));
  chan = capChan & STDLI_PWM_CHAN_MASK;
  switch (curCfg_p->state)
  {
    case STDLI_CAP_START:
    {
      /* Read the first count number */
      curCfg_p->startCnt = reg_p->chan[chan].TPMxCnV;
      curCfg_p->state = STDLI_CAP_FIRST_SMPLE;
      
      /* Clear the interrupt */
      reg_p->chan[chan].TPMxCnSC &= ~CHAN_INT_FLAG;
      break;
    }
    case STDLI_CAP_FIRST_SMPLE:
    {
      /* Disable and clear the interrupt */
      reg_p->chan[chan].TPMxCnSC &= ~(CHAN_INT_FLAG | CAP_INT_EN);
      curCfg_p->state = STDLI_CAP_IDLE;
      stdlpwm_glob.actCapChan--;
    
      /* Read the end count number, and calculate the difference */
      endCnt = reg_p->chan[chan].TPMxCnV;
      if (endCnt > curCfg_p->startCnt)
      {
        endCnt -= curCfg_p->startCnt;
      }
      else
      {
        endCnt = reg_p->timer.TPMxMOD + 1 -
          (curCfg_p->startCnt - endCnt);
      }
      
      /* Call the callback function */
      curCfg_p->capDone_fp(curCfg_p->cbParm, endCnt);
      break;
    }
    case STDLI_CAP_IDLE:
    default:
    {
      STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
        STDLI_SW_ERROR), curCfg_p->state, 0);
      break;
    }
  }
} /* End stdlpwm_read_capture_value */
 
/*
 * ===============================================================================
 * 
 * Name: stdlpwm_capture_tpmx_chn_isr
 * 
 * ===============================================================================
 */
/**
 * ISRs for reading capture values
 * 
 * Call capture channel func passing in the channel num.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
interrupt void stdlser_rcv_tpm1_chan0_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_1 | STDLI_PWM_CHAN_0);
} /* End stdlser_rcv_tpm1_chan0_isr */

interrupt void stdlser_rcv_tpm1_chan1_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_1 | STDLI_PWM_CHAN_1);
} /* End stdlser_rcv_tpm1_chan1_isr */

interrupt void stdlser_rcv_tpm1_chan2_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_1 | STDLI_PWM_CHAN_2);
} /* End stdlser_rcv_tpm1_chan2_isr */

interrupt void stdlser_rcv_tpm1_chan3_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_1 | STDLI_PWM_CHAN_3);
} /* End stdlser_rcv_tpm1_chan3_isr */

interrupt void stdlser_rcv_tpm1_chan4_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_1 | STDLI_PWM_CHAN_4);
} /* End stdlser_rcv_tpm1_chan4_isr */

interrupt void stdlser_rcv_tpm1_chan5_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_1 | STDLI_PWM_CHAN_5);
} /* End stdlser_rcv_tpm1_chan5_isr */

interrupt void stdlser_rcv_tpm2_chan0_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_2 | STDLI_PWM_CHAN_0);
} /* End stdlser_rcv_tpm2_chan0_isr */

interrupt void stdlser_rcv_tpm2_chan1_isr(void)
{
  stdlpwm_read_capture_value(STDLI_TPM_2 | STDLI_PWM_CHAN_1);
} /* End stdlser_rcv_tpm2_chan1_isr */

/*
 * ===============================================================================
 * 
 * Name: stdlpwm_start_pwm_chan
 * 
 * ===============================================================================
 */
/**
 * Start a PWM channel
 * 
 * If the PWM channel was not previously configed, verify the timer
 * is started, set up the digital port, and config the PWM.  Verify the
 * on count is less than the period and program.
 * 
 * @param   capChan     [in]    TPM number and channel
 * @param   onCount     [in]    count when PWM is active high
 * @param   port        [in]    STDLI_DIG_PORT_A to STDLI_DIG_PORT_G
 * @param   digPinMask  [in]    Mask of PWM bit within the port
 * @return  STDLI_TIMER_NOT_CFG       - timer not configed
 *          STDLI_PWM_BAD_ON_COUNT    - on count larger than period count
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdlpwm_start_pwm_chan(
  STDLI_TPM_CHAN_E          capChan,      /* TPM number and channel */
  U16                       onCount,      /* PWM active high count */
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        digPinMask)   /* mask of data bits */
{
  STDLPWM_REG_T             *reg_p;
  U8                        chan;
  U8                        pin;
  U16                       currMod;
  U8                        smallModel;

#define OUTPUT_PWM          0x28
#define OUTPUT_CONST        0x00

  /* Figure out the bit mask for the channel */
  smallModel = capChan & STDLI_TPM_DIG_SMALL_MODEL;
  capChan &= ~STDLI_TPM_DIG_SMALL_MODEL;
  chan = capChan & STDLI_PWM_CHAN_MASK;
  if ((capChan & STDLI_TPM_MASK) == 0)
  {
    /* Timer 1, bits 0, and 1 are for timer 2 */
    pin = 1 << (capChan + 2);
  }
  else
  {
    /* Mask of timer 2 bit */
    pin = 1 << (capChan & STDLI_PWM_CHAN_MASK);
  }
  
  /* If not previously configured */
  reg_p = (STDLPWM_REG_T *)((U8)TIMER1_ADDR +
    (capChan & STDLI_TPM_MASK));
  if ((stdlpwm_glob.cfgdPwmChan & pin) == 0)
  {
    /* Verify the timer is configured */
    if ((reg_p->timer.TPMxSC & CLOCK_CFG_MASK) == 0)
    {
      return(STDLI_TIMER_NOT_CFG);
    }
    
    /* Set up the digital port */
    stdldigio_config_dig_port(smallModel | port |
      STDLI_DIG_OUT, digPinMask, 0);
    reg_p->chan[chan].TPMxCnSC = OUTPUT_PWM;
    stdlpwm_glob.cfgdPwmChan |= pin;
  }
  
  /* If the onCount is more than the period it is a misconfig */
  currMod = reg_p->timer.TPMxMOD + 1;
  if (onCount > currMod)
  {
    return(STDLI_PWM_BAD_ON_COUNT);
  }
  if ((onCount == 0) || (onCount == currMod))
  {
    reg_p->chan[chan].TPMxCnSC = OUTPUT_CONST;
    if (onCount)
    {
      stdldigio_write_port(port, digPinMask, digPinMask);
    }
    else
    {
      stdldigio_write_port(port, digPinMask, 0);
    }
  }
  else
  {
    reg_p->chan[chan].TPMxCnSC = OUTPUT_PWM;
    reg_p->chan[chan].TPMxCnV = onCount - 1;
  }
  return(0);
} /* End stdlpwm_start_pwm_chan */
