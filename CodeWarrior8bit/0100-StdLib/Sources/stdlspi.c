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
 * @file:   stdlspi.c
 * @author: Hugh Spahr
 * @date:   2/24/2010
 *
 * @note:    Copyright© 2010, Hugh Spahr
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
 * This is the SPI utility file in the Standard Library.  It contains
 * functions for reading/writing SPI devices
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "stdlglob.h"

#define STDL_FILE_ID        0xfd    /* File ID for logging errors */

typedef struct
{
  U8                        currByte;
  BOOL                      poll;
  U8                        currInt;
  STDLI_SPI_XFER_T          *head_p;
  STDLI_SPI_XFER_T          *last_p;
} STDLSPI_GLOB_T;

STDLSPI_GLOB_T              stdlspi_glob;

/*
 * ===============================================================================
 * 
 * Name: stdlspi_init_spi
 * 
 * ===============================================================================
 */
/**
 * Initialize the SPI bus
 * 
 * Set the i2c to 200 kbps or 100 kbps for Freescale.
 * 
 * @param   param       [in]    poll mode and clk div
 * @return  None
 * 
 * @pre     None 
 * @note    The chip select signal is not set up during the init.  It is up to
 *          caller of this function to initialize the digital I/O port.
 * 
 * ===============================================================================
 */
void stdlspi_init_spi(
  STDLI_SPI_PARAM_E         param)         /* set poll mode and clk div */
{
#define SPI_RCV_INT         0x80
#define SPI_XMT_INT         0x20
#define MSTR_AND_ENA_BIT    0x50

  SPIBR = (param & SPI_CLK_DIV_MASK) >> 4;
  
  /* Disable the SPI, clear flags, set up enables/intrpt bits */
  SPIC2 = 0x01;
  if (param & SPI_POLL)
  {
    stdlspi_glob.poll = TRUE;
  }
  else
  {
    stdlspi_glob.poll = FALSE;
  }
  SPIC1 = MSTR_AND_ENA_BIT;
  SPIC1 |= (param & STDLI_SPI_CPOL_CPHA_MASK);
  
  stdlspi_glob.currInt = 0;
  stdlspi_glob.head_p = NULL;
  stdlspi_glob.last_p = NULL;
} /* End stdlspi_init_spi */

/*
 * ===============================================================================
 * 
 * Name: stdlspi_start_xfer
 * 
 * ===============================================================================
 */
/**
 * Start a SPI transfer
 * 
 * If the SPI is idle, put it on the linked list, and start the transfer.
 * If the SPI is not idle, add the transfer to the end of the list.
 * 
 * @param   spiXfer_p   [in]    ptr that contains opt, data_p, num bytes, chip
 *                              select, and call back information.
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlspi_start_xfer(void)
{
  STDLI_SPI_XFER_T          *spiXfer_p;
  
#define SPRF_STATUS_BIT     0x80
#define SPTEF_STATUS_BIT    0x20
#define SPI_BIDIROE         0x08
  
  /* Set up the direction bits */
  spiXfer_p = stdlspi_glob.head_p;
  if (spiXfer_p->dir & STDLI_SPI_WRITE)
  {
    /* Current byte is set to 0xff so first interrupt increments to 0 */
    stdlspi_glob.currByte = MAX_U8;
    
    /* Clear the chip select bit */
    stdldigio_write_port(spiXfer_p->csPort, spiXfer_p->csMask, 0);
    
    /* Set up the clock polarity and phase and interrupts.  Enable the SPI */
    if (stdlspi_glob.poll)
    {
      stdlspi_glob.currInt = SPTEF_STATUS_BIT;
    }
    else
    {
      SPIC2 |= SPI_BIDIROE;
      SPIC1 |= SPI_XMT_INT;
    }
  }
  else
  {
    stdlspi_glob.currByte = 0;

    /* Set up the clock polarity and phase and interrupts.  Enable the SPI */
    if (stdlspi_glob.poll)
    {
      stdlspi_glob.currInt = SPRF_STATUS_BIT;
    }
    else
    {
      SPIC2 &= ~SPI_BIDIROE;
      SPIC1 |= SPI_RCV_INT;
    }

    /* Clear the chip select bit */
    stdldigio_write_port(spiXfer_p->csPort, spiXfer_p->csMask, 0);
    
    /* Start the transfer, if reading, doesn't matter what data is written */
    SPID = *spiXfer_p->data_p;    
  }
} /* End stdlspi_start_xfer */

/*
 * ===============================================================================
 * 
 * Name: stdlspi_send_spi_msg
 * 
 * ===============================================================================
 */
/**
 * Send a SPI message to read/write data
 * 
 * If the SPI is idle, put it on the linked list, and start the transfer.
 * If the SPI is not idle, add the transfer to the end of the list.
 * 
 * @param   spiXfer_p   [in]    ptr that contains opt, data_p, num bytes, chip
 *                              select, and call back information.
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlspi_send_spi_msg(
  STDLI_SPI_XFER_T          *spiXfer_p)   /* ptr to SPI xfer structure */
{
  spiXfer_p->next_p = NULL;
  DisableInterrupts;
  if (stdlspi_glob.head_p == NULL)
  {
    /* SPI was idle, so start transfer */
    stdlspi_glob.head_p = spiXfer_p;
    stdlspi_glob.last_p = spiXfer_p;
    EnableInterrupts;
    stdlspi_start_xfer();
  }
  else
  {
    stdlspi_glob.last_p->next_p = spiXfer_p;
    stdlspi_glob.last_p = spiXfer_p;
    EnableInterrupts;
  }
} /* End stdlspi_send_spi_msg */

/*
 * ===============================================================================
 * 
 * Name: stdlspi_spi_isr
 * 
 * ===============================================================================
 */
/**
 * SPI interrupt service routine
 * 
 * If writing, check if done transmitting.  If not, clear status and send next
 * byte.  If reading, check if done.  If not, write the next dummy data value
 * to be sent.  If the transfer is complete, clear the CS, and call the callback
 * function.  Check to see if another SPI xfer is pending and start it if it
 * exists.
 * 
 * @param None 
 * @return None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void stdlspi_spi_complete(void)
{
  STDLI_SPI_XFER_T          *spiXfer_p;
  BOOL                      startNext;
  R8                        tmp;
  
  /* Check if reading or writing */
  startNext = FALSE;
  spiXfer_p = stdlspi_glob.head_p;
  if (spiXfer_p->dir & STDLI_SPI_WRITE)
  {
    /* Check if done transmitting */
    stdlspi_glob.currByte++;
    if (stdlspi_glob.currByte < spiXfer_p->numDataBytes)
    {
      /* Read status and send next byte, also clears flag */
      tmp = SPIS;
      SPID = spiXfer_p->data_p[stdlspi_glob.currByte];
    }
    else
    {
      /* Done transfer */
      startNext = TRUE;
    }
  }
  else
  {
    /* Read status and the data byte, this also clears flag */
    tmp = SPIS;
    spiXfer_p->data_p[stdlspi_glob.currByte] = SPID;
    stdlspi_glob.currByte++;
    if (stdlspi_glob.currByte < spiXfer_p->numDataBytes)
    {
      /* Send garbage byte to read next byte of data */
      SPID = 0;
    }
    else
    {
      /* Done transfer */
      startNext = TRUE;
    }
  }
  if (startNext)
  {
    /* Disable chip select and disable SPI */
    SPIC1 &= ~(SPI_RCV_INT | SPI_XMT_INT);
    stdlspi_glob.currInt = 0;
    stdldigio_write_port(spiXfer_p->csPort, spiXfer_p->csMask,
      spiXfer_p->csMask);
    
    /* Call callback function */
    spiXfer_p->spiDone_fp(spiXfer_p->cbParm);
    
    /* Move to the next xfer */
    DisableInterrupts;
    stdlspi_glob.head_p = spiXfer_p->next_p;
    EnableInterrupts;
    spiXfer_p = stdlspi_glob.head_p;
    
    /* If next xfer exists, start it */
    if (spiXfer_p)
    {
      stdlspi_start_xfer();
    }
  }
} /* End stdlspi_spi_complete */

interrupt void stdlspi_spi_complete_isr(void)
{
  stdlspi_spi_complete();
} /* End stdlspi_spi_complete_isr */

void stdlspi_spi_complete_poll(void)
{
  if (SPIS & stdlspi_glob.currInt)
  {
    stdlspi_spi_complete();
  }
} /* End stdlspi_spi_complete_poll */
