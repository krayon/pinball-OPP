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
 * @file:   stdltime.c
 * @author: Hugh Spahr
 * @date:   6/10/2008
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
 * This is the timer utility file in the Standard Library.  It contains
 *  the timing functions.
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "version.h"

#define STDLG_INSTANTIATE
#include "stdlglob.h"

#define STDLTIME_MAX_TICK_FUNC        4

typedef struct
{
  void                      (*timeout_fp)(U16 cbParm);
  U16                       cbParm;
} TICK_FUNC_T;

typedef struct
{
  U16                       currMs;
  U16                       currS;
  U8                        sysTickMs;
  U8                        sysTickCnt;
  U8                        numTickFunc;
  STDLI_TIMER_E             params;
  TICK_FUNC_T               tickFunc[STDLTIME_MAX_TICK_FUNC];
  STDLI_TIMER_EVENT_T       *timeEvt_p;
} STDLTIME_TIMER_T;

STDLTIME_TIMER_T            stdltime_glob;

/*
 * ===============================================================================
 * 
 * Name: stdltime_start_timing_clock
 * 
 * ===============================================================================
 */
/**
 * Start the timing clock.
 * 
 * Start the 1 us timing clock. This allows timestamping and logging functions to
 * store the time of the event.
 * 
 * @param  params       [in]    TIMER_POLL for poll not intrpt
 *                              TIMER_FAST_OSC to use a 16 MHz bus clock
 * @return None
 * 
 * @pre None 
 * @note This does not use the RTC circuitry of the HCS08.  It uses timer 2 to
 *        enable resolutions down to 1 us.  This must be called before
 *        stdltime_start_tick.  This can use either 8, or 16 MHz bus clock.
 * 
 * ===============================================================================
 */
void stdltime_start_timing_clock(
  STDLI_TIMER_E             params)       /* TIMER_POLL or TIMER_FAST_OSC */
{
  U8                        tmp;          /* TIMER_POLL or TIMER_FAST_OSC */
  
#define TPM2SC_DIV8_INIT    0x0b          /* Use busclk and clk/8 */
#define TPM2SC_DIV16_INIT   0x0c          /* Use busclk and clk/16 */
#define TPM2SC_EN_OVFL_INT  0x40          /* Int enable overflow */

  stdlg_info.slowAdc_fp = NULL;
  stdlg_info.fastAdc_fp = NULL;
  stdltime_glob.currMs = 0;
  stdltime_glob.currS = 0;
  stdltime_glob.sysTickMs = 0;
  stdltime_glob.sysTickCnt = 0;
  stdltime_glob.numTickFunc = 0;
  stdltime_glob.timeEvt_p = NULL;
  stdltime_glob.params = params;
  
  TPM2MOD = 999;
  if ((stdltime_glob.params & TIMER_FAST_OSC) == 0)
  {
    tmp = TPM2SC_DIV8_INIT;     /* (8 MHz/8) 1000 ticks = 1 ms */
  }
  else
  {
    tmp = TPM2SC_DIV16_INIT;    /* (16 MHz/8) 1000 ticks = 1 ms */
  }
    
  if (stdltime_glob.params & TIMER_POLL)
  {
    TPM2SC = tmp;
  }
  else
  {
    TPM2SC = tmp | TPM2SC_EN_OVFL_INT;
  }
} /* End stdltime_start_timing_clock */

/*
 * ===============================================================================
 * 
 * Name: stdltime_insert_timer_evt
 * 
 * ===============================================================================
 */
/**
 * Insert a timer event in the timer event chain
 *
 * Walk through the chain until the location for the timed event is found.  The
 * linked list is organized such that the top most event is the next event to
 * occur.  All events that have timeoutTicks set to 0 happen at the same
 * tick. 
 *
 * @param   timeEvt_p   [in]    ptr to time event structure to be inserted
 * @return  None
 *
 * @pre     None
 * @note    Interrupts are disabled so events can be added at non-interrupt
 *          level.  Never called by user.  Call register timer func instead.
 *
 * ===============================================================================
 */
void stdltime_insert_timer_evt(
  STDLI_TIMER_EVENT_T       *timeEvt_p)   /* ptr to time event struct to insert */
{
  STDLI_TIMER_EVENT_T       *insertTimeEvt_p;
  STDLI_TIMER_EVENT_T       **prevTimeEvt_pp;
  
  prevTimeEvt_pp = &stdltime_glob.timeEvt_p;
  if ((stdltime_glob.params & TIMER_POLL) == 0)
  {
    DisableInterrupts;
  }
  insertTimeEvt_p = stdltime_glob.timeEvt_p;
  while ((insertTimeEvt_p != NULL) &&
    (timeEvt_p->timeoutTicks > insertTimeEvt_p->timeoutTicks))
  {
    timeEvt_p->timeoutTicks -= insertTimeEvt_p->timeoutTicks;
    prevTimeEvt_pp = &insertTimeEvt_p->next_p;
    insertTimeEvt_p = insertTimeEvt_p->next_p;
  }
  if (insertTimeEvt_p != NULL)
  {
    insertTimeEvt_p->timeoutTicks -= timeEvt_p->timeoutTicks;
  }
  timeEvt_p->next_p = insertTimeEvt_p;
  *prevTimeEvt_pp = timeEvt_p;
  if ((stdltime_glob.params & TIMER_POLL) == 0)
  {
    EnableInterrupts;
  }
} /* End stdltime_insert_timer_evt */
 
/*
 * ===============================================================================
 * 
 * Name: stdltime_sys_tick
 * 
 * ===============================================================================
 */
/**
 * System tick funciton
 *
 * Call all registered tick functions.  Look at the timing chain and call
 * all the one-shot or repetitive events.
 *
 * @param   None
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void stdltime_sys_tick(void)
{
  TICK_FUNC_T               *tickFunc_p;
  STDLI_TIMER_EVENT_T       *currTimeEvt_p;
  
  /* Walk through the registered tick functions and call the callback funcs. */
  for (tickFunc_p = &stdltime_glob.tickFunc[0]; 
    tickFunc_p < &stdltime_glob.tickFunc[stdltime_glob.numTickFunc];
    tickFunc_p++)
  {
    tickFunc_p->timeout_fp(tickFunc_p->cbParm);  
  }
 
  /* Check the timing chain */
  currTimeEvt_p = stdltime_glob.timeEvt_p;
  if (currTimeEvt_p)
  {
    /* Decrement the top event to see if it timed out. */
    currTimeEvt_p->timeoutTicks--;
    while (currTimeEvt_p->timeoutTicks == 0)
    {
      /* Move the head of the time event list */
      stdltime_glob.timeEvt_p = currTimeEvt_p->next_p;
      
      /* Check if this is a repetitive event */
      if (currTimeEvt_p->time & STDLI_REPETITIVE_EVT)
      {
        /* Walk through the list, and insert it at appropriate spot */
        currTimeEvt_p->timeoutTicks = currTimeEvt_p->time &
          ~STDLI_REPETITIVE_EVT;
        stdltime_insert_timer_evt(currTimeEvt_p);
      }
      
      /* Timeout occurred, call the callback function */
      currTimeEvt_p->timeout_fp(currTimeEvt_p->cbParm);
      
      currTimeEvt_p = stdltime_glob.timeEvt_p;
    }
  }
} /* End stdltime_sys_tick */

/*
 * ===============================================================================
 * 
 * Name: stdltime_timer2_isr
 * 
 * ===============================================================================
 */
/**
 * Timer 2 overflow interrupt
 * 
 * After getting the timer2 overflow interrupt clear the overflow flag.
 * 
 * @param  None
 * @return None
 * 
 * @pre    None 
 * @note   None
 * 
 * ===============================================================================
 */
void stdltime_timer2_overflow(void)
{
#define TPM2SC_OVERFLOW     0x80

  DisableInterrupts;
  TPM2SC &= ~TPM2SC_OVERFLOW;    /* Clear the overflow flag */
  stdltime_glob.currMs++;
  if (stdltime_glob.currMs == 1000)
  {
    stdltime_glob.currS++;
    stdltime_glob.currMs = 0;
  }
  EnableInterrupts;
  
  /* Check if the tick timer is initialized */
  if (stdltime_glob.sysTickMs)
  {
    /* Check if the system tick has timed out */
    stdltime_glob.sysTickCnt++;
    if (stdltime_glob.sysTickCnt >= stdltime_glob.sysTickMs)
    {
      stdltime_glob.sysTickCnt = 0;
      
      /* If the slow ADC is configured, start the chain now */
      if (stdlg_info.slowAdc_fp)
      {
        /* The function should only retun an error from user space */
        (void)stdlg_info.slowAdc_fp();
      }
       
      /* Call tick functions */
      stdltime_sys_tick();
    }
  }
  
  /* If the fast ADC is configured, start the chain now */
  if (stdlg_info.fastAdc_fp)
  {
     /* The function should only retun an error from user space */
     (void)stdlg_info.fastAdc_fp();
  }
} /* End stdltime_timer2_overflow */

interrupt void stdltime_timer2_isr(void)
{
  stdltime_timer2_overflow();
} /* End stdltime_timer2_isr */

void stdltime_timer2_poll(void)
{
  if (TPM2SC & TPM2SC_OVERFLOW)
  {
    stdltime_timer2_overflow();
  }
} /* End stdltime_timer2_poll */

/*
 * ===============================================================================
 * 
 * Name: stdltime_get_curr_time
 * 
 * ===============================================================================
 */
/**
 * Get current time
 *
 * Read the current time and pass it back to the calling function
 *
 * @param   time_p      [out]   ptr to structure with current time 
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void stdltime_get_curr_time(
  STDLI_TIMER_T             *time_p)      /* ptr to returned current time struct */
{
  U8                        tpm2Stat;
  
  if ((stdltime_glob.params & TIMER_POLL) == 0)
  {
    DisableInterrupts;
  }
  time_p->usec = TPM2CNT;
  time_p->sec = stdltime_glob.currS;
  time_p->msec = stdltime_glob.currMs;
  tpm2Stat = TPM2SC;
  if ((stdltime_glob.params & TIMER_POLL) == 0)
  {
    EnableInterrupts;
  }
  
  /* There is the possibility that a timer overflow has
   *  happened, but hasn't been recorded yet.  Fix the value.
   */
  if (tpm2Stat & TPM2SC_OVERFLOW)
  {
    if (time_p->msec != 999)
    {
      time_p->msec++;
    }
    else
    {
      time_p->msec = 0;
      time_p->sec++;
    }
  }
} /* End stdltime_get_curr_time */

/*
 * ===============================================================================
 * 
 * Name: stdltime_get_elapsed_time
 * 
 * ===============================================================================
 */
/**
 * Get elapsed time
 *
 * Read the current time.  Subtract the starting time and pass the difference
 * back as elapsed time.
 *
 * @param   elapsed_p   [in/out]ptr to structure with start and elapsed time 
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void stdltime_get_elapsed_time(
  STDLI_ELAPSED_TIME_T      *elapsed_p)   /* ptr to elapsed time struct*/
{
  STDLI_TIMER_T             currTime;
  STDLI_TIMER_T             saveTime;
  STDLI_TIMER_T             *time_p;
  
  /* Get current time */
  time_p = &elapsed_p->startTime; 
  stdltime_get_curr_time(&currTime);
  saveTime.usec = currTime.usec;
  saveTime.msec = currTime.msec;
  saveTime.sec = currTime.sec;
  
  /* Calculate elapsed time */
  if (currTime.usec >= time_p->usec)
  {
    currTime.usec -= time_p->usec;
  }
  else
  {
    if (currTime.msec)
    {
      currTime.msec--;
    }
    else
    {
      currTime.msec = 1000;
      currTime.sec--;
    }
    currTime.usec = (currTime.usec + 1000 - time_p->usec);
  }
  if (currTime.msec >= time_p->msec)
  {
    currTime.msec -= time_p->msec;    
  }
  else
  {
    currTime.sec--;
    currTime.msec = (currTime.msec + 1000 - time_p->msec);
  }
  currTime.sec -= time_p->sec;
  if (currTime.sec == MAX_U16)
  {
    saveTime.usec++;
  }
    
  /* Copy answer to elapsed time */
  time_p = &elapsed_p->elapsedTime;
  time_p->usec = currTime.usec; 
  time_p->msec = currTime.msec; 
  time_p->sec = currTime.sec;
} /* End stdltime_get_elapsed_time */

/*
 * ===============================================================================
 * 
 * Name: stdltime_start_tick
 * 
 * ===============================================================================
 */
/**
 * Start system tick
 *
 * Start the system tick timer.
 *
 * @param   numMsec     [in]    number of msec between ticks 
 * @return  None
 *
 * @pre     stdltime_start_tick - must have been called to reset numTickFunc.
 * @note    Uses timer 2, same as timing clock
 *
 * ===============================================================================
 */
void stdltime_start_tick(
  U8                        numMsec)      /* num msec per system tick */
{
  stdltime_glob.sysTickMs = numMsec;
} /* End stdltime_start_tick */

/*
 * ===============================================================================
 * 
 * Name: stdltime_reg_timer_func
 * 
 * ===============================================================================
 */
/**
 * Register a timer function as either one-shot, repetitive, or system tick
 *
 * A system tick timer is indicated by setting the time variable to one.  Since
 * the callback_fp, and passedParam are copied, the passed structure can be
 * allocated on the stack.
 *
 * A one-shot timer is indicated when the time variable > 1 system tick,
 * and the msb of the time variable is clear.  The passed structure is added
 * to the timer linked list so it must be statically allocated.
 *
 * A repetitive timer is indicated when the time variable > 1 system tick,
 * and the msb of the time variable is set using the STDLI_REPETITIVE_EVT
 * define.  The passed structure is added to the timer linked list, so it
 * must be statically allocated.
 *
 * @param   timeEvt_p   [in]    ptr to time event structure to be inserted
 * @param   offset      [in]    offset to the first timer event (only repetetive)
 * @return  None
 *
 * @pre     None
 * @note    Interrupts are disabled so events can be added at non-interrupt
 *          level.
 *
 * ===============================================================================
 */
STDLI_ERR_E stdltime_reg_timer_func(
  STDLI_TIMER_EVENT_T       *timeEvt_p,   /* ptr to time event struct to insert */
  U8                        offset)       /* offset to first timer event, only repetetive */
{
  if (timeEvt_p->timeout_fp == NULL)
  {
    return(STDLI_ILLEGAL_CB_FUNC);
  }

  /* Check if this is a system tick timer */
  if (timeEvt_p->time == 1)
  {
    if (stdltime_glob.numTickFunc == (STDLTIME_MAX_TICK_FUNC - 1))
    {
      return(STDLI_TOO_MANY_TICK_FUNCS);
    }
    stdltime_glob.tickFunc[stdltime_glob.numTickFunc].cbParm =
      timeEvt_p->cbParm;
    stdltime_glob.tickFunc[stdltime_glob.numTickFunc].timeout_fp =
      timeEvt_p->timeout_fp;    
    stdltime_glob.numTickFunc++;    
  }
  else
  {
    /* Fill out timeout ticks, and insert into timer chain */
    if (offset != 0)
    {
      timeEvt_p->timeoutTicks = offset;
    }
    else
    {
      timeEvt_p->timeoutTicks = timeEvt_p->time & ~STDLI_REPETITIVE_EVT;
    }
    if (timeEvt_p->timeoutTicks == 0)
    {
      return(STDLI_BAD_NUM_TICKS);
    }
    stdltime_insert_timer_evt(timeEvt_p);
  }
  return(0);
} /* End stdltime_reg_timer_func */
