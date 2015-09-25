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
 * @file:   stdlintf.c
 * @author: Hugh Spahr
 * @date:   9/17/2015
 *
 * @note:   Copyright© 2015, Hugh Spahr
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
 * Interface file to the Standard Library.  It contains function
 *  prototypes and structures
 *
 *===============================================================================
 */
#ifndef STDLINTF_H
#define STDLINTF_H
 
#include "stdtypes.h"

/*
 * Generic structures/enumerations used for Standard Library.
 */
typedef enum
{
   STDLI_TOO_MANY_TICK_FUNCS  = 0x01,
   STDLI_ILLEGAL_CB_FUNC      = 0x02,
   STDLI_BAD_NUM_TICKS        = 0x03,  
   STDLI_TIMER_NOT_CFG        = 0x08,
   STDLI_SW_ERROR             = 0x0c,
} STDLI_ERR_E;

/* 
 * API for timing functions
 */
/* Timing interface structures/enumerations */
typedef enum
{
   TIMER_POLL                 = 0x01,
} STDLI_TIMER_E;

typedef struct
{
   U16                        usec;
   U16                        msec;
   U32                        sec;
} STDLI_TIMER_T;

typedef struct
{
   STDLI_TIMER_T              startTime;
   STDLI_TIMER_T              elapsedTime;  
} STDLI_ELAPSED_TIME_T;

#define STDLI_REPETITIVE_EVT        0x8000

typedef struct stdli_timer_s
{
   U16                        time;
   void                       (*timeout_fp)(U16 cbParm);
   U16                        cbParm;
   U16                        timeoutTicks; /* Filled by utility */
   struct stdli_timer_s       *next_p;      /* Filled by utility */
} STDLI_TIMER_EVENT_T;

/* To install timing functions, add INTRPT_TPM2_OVFL to POPULATED_INTS in
 *  projintrpts.h file.  Add the following lines to install the isr:
 *      interrupt void stdltime_timer2_isr(void);
 *      #define vector14 stdltime_timer2_isr
 * To install timing polled functions, call stdltime_start_timing_clock
 * with poll set to TRUE, and call stdltime_timer2_poll to poll interrupt.
 */
/* Timing function prototypes */
void stdltime_start_timing_clock(
   STDLI_TIMER_E              params);      /* TIMER_POLL or TIMER_FAST_OSC */
void stdltime_get_curr_time(
   STDLI_TIMER_T              *time_p);     /* ptr to returned current time struct */
void stdltime_get_elapsed_time(
   STDLI_ELAPSED_TIME_T       *elapsed_p);  /* ptr to elapsed time struct*/
void stdltime_start_tick(
   U8                         numMsec);     /* num msec per system tick */
STDLI_ERR_E stdltime_reg_timer_func(
   STDLI_TIMER_EVENT_T        *timeEvt_p,   /* ptr to time event struct to insert */
   U8                         offset);      /* offset to first timer event, only repetitive */
void stdltime_timer2_poll(void);

/* 
 * API for digital I/O functions
 */
/* Digital I/O interface structures/enumerations */
typedef enum
{
   STDLI_DIG_PORT_0           = 0x00,
   STDLI_DIG_PORT_1           = 0x01,
   STDLI_DIG_PORT_2           = 0x02,
   STDLI_DIG_PORT_3           = 0x03,
   STDLI_DIG_PORT_4           = 0x04,
   STDLI_DIG_PORT_MASK        = 0x07,
   STDLI_DIG_OUT              = 0x10,
   STDLI_DIG_OC_PULLDWN       = 0x20,
   STDLI_DIG_PULLUP           = 0x40,
   STDLI_DIG_PULLDWN          = 0x80,
} STDLI_DIG_PORT_INFO_E;

/* Digital I/O function prototypes */
void stdldigio_config_dig_port(
   STDLI_DIG_PORT_INFO_E      portInfo,     /* port, input/output, drive, and pullup */
   U8                         mask,         /* mask of data bits to change */
   U8                         data);        /* data if output bits, unused if input */
U8 stdldigio_read_port(
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_1 */
   U8                         mask);        /* mask of data bits to read */
void stdldigio_write_port(
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_1 */
   U8                         mask,         /* mask of data bits to write */
   U8                         data);        /* data to write */
#endif

/* [] END OF FILE */
