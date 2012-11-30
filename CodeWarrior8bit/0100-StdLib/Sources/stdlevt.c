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
 * @file:   stdlevt.c
 * @author: Hugh Spahr
 * @date:   6/24/2008
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
 * This is the event utility file in the Standard Library.  It contains
 *  logging and k_fatal functions.
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "stdlglob.h"

typedef struct
{
  BOOL                      eeprom;
  STDLI_EVENT_LOG_T         *nxtEvt_p;
  U8                        *endLog_p;
} STDLEVT_EVENT_T;

STDLEVT_EVENT_T             stdlevt_glob;

/* Prototypes */
void stdlevt_write_nvmemory( 
  U8                        *data_p,
  U8                        numBytes);
  
/*
 * ===============================================================================
 * 
 * Name: stdlevt_init_log_event
 * 
 * ===============================================================================
 */
/**
 * Initialize the event log.
 * 
 * Initialize the event log.  It must be handed in the address of the first event
 * log entry, the address of the end of the log, and the starting EEPROM address.
 * The EEPROM address allows the library to support multiple processors.  If the
 * event log is to be stored in Flash instead of EEPROM, eeprom_p must be 0.
 * 
 * @param   firstEvt_p  [in]    ptr to first event log entry
 * @param   endLog_p    [in]    ptr to the end of the log
 * @param   eeprom_p    [in]    ptr to first address of EEPROM, or 0 for Flash
 * @return  STDLI_NO_EVENTS_AVAIL   - Event log is completely filled
 * 
 * @pre None 
 * @note First and end addresses must be within the EEPROM memory.
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdlevt_init_log_event( 
  STDLI_EVENT_LOG_T         *firstEvt_p,  /* ptr to first event log entry */
  U8                        *endLog_p,    /* ptr to the end of the log */
  U8                        *eeprom_p)    /* EEPROM start or 0 for log in Flash */
{
#define START_OF_EEPROM     0x1400
#define END_OF_EEPROM       0x1c00

  /* Initialize the structure */
  stdlevt_glob.nxtEvt_p = firstEvt_p;
  stdlevt_glob.endLog_p = endLog_p;
  if (eeprom_p)
  {
    /* Event log is in EEPROM */
    stdleeprom_init_eeprom_addr(eeprom_p);
    stdlevt_glob.eeprom = TRUE;
  }
  else
  {
    /* Event log is in Flash */
    stdlevt_glob.eeprom = FALSE;
  }
  
  /* Find the first empty location */
  while (stdlevt_glob.nxtEvt_p->event != STDLI_UNUSED_EVENT)
  {
    stdlevt_glob.nxtEvt_p++;
    if ((U8 *)(stdlevt_glob.nxtEvt_p + 1) > (U8 *)endLog_p)
    {
      return(STDLI_NO_EVENTS_AVAIL);
    }
  }
  return(0);
} /* End stdlevt_init_log_event */

/*
 * ===============================================================================
 * 
 * Name: stdlevt_log_event
 * 
 * ===============================================================================
 */
/**
 * Log an event
 * 
 * This function is usually called through a macro.  The macro fills out the
 * fileId and lineNum.  The current time is grabbed, and the next unused event
 * is located.  The log record is stored in the EEPROM.  If this is a k_fatal
 * event, the processor is reset.
 * 
 * @param   eventId     [in]    (event << 20) | (fileId << 12) | lineNum
 * @param   data1       [in]    16 bits of extra info which is event specific
 * @param   data2       [in]    16 bits of extra info which is event specific
 * @param   k_fatal     [in]    TRUE if this is a k_fatal event.
 * @return  None
 * 
 * @pre  stdltime_start_timing_clock 
 * @note None
 * 
 * ===============================================================================
 */
void stdlevt_log_event( 
  U32                       eventId,      /* event id, includes event/file/line */
  U16                       data1,        /* event spec data */
  U16                       data2,        /* event spec data */
  BOOL                      kFatal)       /* TRUE if this is a k_fatal */
{
  STDLI_TIMER_T             time;
  U32                       data[STDLI_EVENT_LOG_LEN/sizeof(U32)];

  /* Get the current time */
  stdltime_get_curr_time(&time);
  
  /* Fill out the event record */
  data[0] = eventId;
  data[1] = ((U32)time.sec << 20) | ((U32)time.msec << 10) | time.usec;
  data[2] = ((U32)data1 << 16) | data2;

  /* Store off the data in the event log */
  if ((U8 *)(stdlevt_glob.nxtEvt_p + 1) <= (U8 *)stdlevt_glob.endLog_p)
  {
    /* Space exists, store it in the log */
    stdlevt_write_nvmemory((U8 *)&data[0], sizeof(STDLI_EVENT_LOG_T));
    stdlevt_glob.nxtEvt_p++;
  }
  
  /* If this is k_fatal event, reset the processor */
  if (kFatal)
  {
    #if DEBUG != 0
    /* Endless loop */
    while (kFatal)
    {
      __RESET_WATCHDOG();
    }
    #else
    /* Reset the processor */
    asm DCB 0x8D ;    /* Use illegal instruction to cause reset */
    #endif
  }
} /* End stdlevt_log_event */

/*
 * ===============================================================================
 * 
 * Name: stdlevt_write_nvmemory
 * 
 * ===============================================================================
 */
/**
 * Write to non-volatile memory (Either EEPROM or FLASH)
 * 
 * This function writes bytes to the Flash or EEPROM.  It assumes that the memory
 * is erased (all 1's).
 * 
 * @param   data_p      [in]    Data to be stored in NV memory
 * @param   numBytes    [in]    Number of bytes to be stored
 * @return  None
 * 
 * @pre  None
 * @note None
 * 
 * ===============================================================================
 */
void stdlevt_write_nvmemory( 
  U8                        *data_p,
  U8                        numBytes)
{
  U8                        *dest_p;
  U8                        tmpCnt;
  BOOL                      cmdDone;
  
  for (tmpCnt = 0, dest_p = (U8 *)stdlevt_glob.nxtEvt_p; tmpCnt < numBytes;
    data_p++, dest_p++, tmpCnt++)
  {
    if (stdlevt_glob.eeprom)
    {
      stdleeprom_start_write(dest_p, *data_p);
    }
    else
    {
      stdleeprom_start_flash_write(dest_p, *data_p);
    }
    do
    {
      /* Clear the watchdog timer, needed for FSTAT to change */
      SRS = 0x55;
      SRS = 0xaa;
      cmdDone = stdleeprom_check_cmd_done();
    } while (!cmdDone);
  }
} /* End stdlevt_write_nvmemory */
