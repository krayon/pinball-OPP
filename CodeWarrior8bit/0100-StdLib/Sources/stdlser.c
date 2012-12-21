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
 * @file:   stdlser.c
 * @author: Hugh Spahr
 * @date:   6/26/2008
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
 * This is the serial utility file in the Standard Library.  It
 * contains functions read and write to both serial ports.
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "stdlglob.h"

#define SER1_ADDR           0x38    /* Address of first port (port 1) */
#define SCIxS1_RCV_OVERRUN  0x28    /* Rcv bit or overrun */
#define SCIxS1_TDRE         0x80    /* Xmt data register empty */
#define SCIxC2_TX_INT_EN    0x80    /* Xmt interrupt enable */

typedef struct
{
  R8                        SCIxBDH;
  R8                        SCIxBDL;
  R8                        SCIxC1;
  R8                        SCIxC2;
  R8                        SCIxS1;
  R8                        SCIxS2;
  R8                        SCIxC3;
  R8                        SCIxD;
} STDLSER_REG_T;

typedef struct
{
  STDLI_SER_INFO_T          *serInfo_p[STDLI_NUM_SER_PORT];
} STDLSER_GLOB_T;

STDLSER_GLOB_T              stdlser_glob;

/* Prototypes: */
void stdlser_xmt_char(
  STDLI_SER_PORT_E          portNum);

/*
 * ===============================================================================
 * 
 * Name: stdlser_ser_module_init
 * 
 * ===============================================================================
 */
/**
 * Initialize the serial port module
 * 
 * Initialize the global serial port data.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlser_ser_module_init(void)
{
  stdlser_glob.serInfo_p[STDLI_SER_PORT_1] = NULL;
  stdlser_glob.serInfo_p[STDLI_SER_PORT_2] = NULL;
} /* End stdlser_ser_module_init */

/*
 * ===============================================================================
 * 
 * Name: stdlser_init_ser_port
 * 
 * ===============================================================================
 */
/**
 * Initialize a serial port
 * 
 * Initialize head and tail to 0, and make xmt inactive. Configure the port
 * to 19.2 kbps, 8, N, 1, and enable the rcv interrupt.
 * 
 * @param   portNum     [in]    Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2
 *                              OR in STDLI_POLL_SER_PORT if polling
 * @param   serInfo_p   [in]    Info for the serial port state.  Since the passed
 *                              structure is not copied, it must be statically
 *                              allocated.  Serial state contains ptr to txBuf,
 *                              size of txBuf, rxChar callback function addr,
 *                              callback parameter handed to rxChar function.
 * @return  None
 * 
 * @pre     stdlser_init_ser_module must be called first.
 * @note    None
 * 
 * ===============================================================================
 */
void stdlser_init_ser_port(
  STDLI_SER_PORT_E          portNum,      /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
  STDLI_SER_INFO_T          *serInfo_p)   /* Ser state, txBuf addr, txBuf size, rx
                                           *  callback func.
                                           */
{
  U8                        tmpVal;
  STDLSER_REG_T             *ser_p;

#define RCV_INT_EN          0x20;
#define PORT_NUM_MASK       0x01
  
  serInfo_p->curTxHead = 0;
  serInfo_p->curTxTail = 0;
  serInfo_p->txAct = FALSE;
  if (portNum & STDLI_POLL_SER_PORT)
  {
    serInfo_p->pollBit = 0;
  }
  else
  {
    serInfo_p->pollBit = RCV_INT_EN;
  }
  stdlser_glob.serInfo_p[portNum & PORT_NUM_MASK] = serInfo_p;
  
  /* Configure the pins/baud rate */
  ser_p = ((STDLSER_REG_T *)SER1_ADDR) + (portNum & PORT_NUM_MASK);
  if (portNum & STDLI_FAST_OSC)
  {
    ser_p->SCIxBDL = 52;    /* Set baud = 16 MHz/(16 * 19200) = 52 */
  }
  else
  {
    ser_p->SCIxBDL = 26;    /* Set baud = 8 MHz/(16 * 19200) = 26 */
  }
  ser_p->SCIxC1 = 0x00;     /* Normal op, 8, N, 1 */
  tmpVal = ser_p->SCIxD;    /* Clear rcv data reg flag if set */
  ser_p->SCIxC2 = 0x0c | serInfo_p->pollBit; /* Xmt/Rcv enable, rcv int if needed */
  
} /* End stdlser_init_ser_port */

/*
 * ===============================================================================
 * 
 * Name: stdlser_rcv_char
 * 
 * ===============================================================================
 */
/**
 * Function for rcving serial port char
 * 
 * Read the rcv data, to clear the ISR.  Check if a rcv function has been
 * registered.  If so, call the rcv function.
 * 
 * @param   portNum     [in]    Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlser_rcv_char(
  STDLI_SER_PORT_E          portNum)
{
  U8                        tmpVal;
  STDLSER_REG_T             *ser_p;
  STDLI_SER_INFO_T          *serInfo_p;

  /* Clear the interrupt bit */  
  ser_p = ((STDLSER_REG_T *)SER1_ADDR) + portNum;
  tmpVal = ser_p->SCIxS1;
  tmpVal = ser_p->SCIxD;    /* Clear rcv data reg flag if set */
  serInfo_p = stdlser_glob.serInfo_p[portNum];
  
  /* If the serial port has been registered, call callback function */
  if (serInfo_p != NULL)
  {
    serInfo_p->rxSerChar_fp(serInfo_p->cbParm, tmpVal);
  }
} /* End stdlser_rcv_char */

/*
 * ===============================================================================
 * 
 * Name: stdlser_rcv_portx_isr
 * 
 * ===============================================================================
 */
/**
 * ISR for rcving serial port chars
 * 
 * Call rcv char func passing in the serial port num.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
interrupt void stdlser_rcv_port1_isr(void)
{
  stdlser_rcv_char(STDLI_SER_PORT_1);
} /* End stdlser_rcv_port1_isr */

void stdlser_port1_poll(void)
{
  STDLSER_REG_T             *ser_p;
  STDLI_SER_INFO_T          *serInfo_p;

  ser_p = ((STDLSER_REG_T *)SER1_ADDR) + STDLI_SER_PORT_1;
  serInfo_p = stdlser_glob.serInfo_p[STDLI_SER_PORT_1];
  if (ser_p->SCIxS1 & SCIxS1_RCV_OVERRUN)
  {
    stdlser_rcv_char(STDLI_SER_PORT_1);
  }
  if (serInfo_p->txAct && (ser_p->SCIxS1 & SCIxS1_TDRE))
  {
    stdlser_xmt_char(STDLI_SER_PORT_1);
  }
} /* End stdlser_rcv_port1_poll */

interrupt void stdlser_rcv_port2_isr(void)
{
  stdlser_rcv_char(STDLI_SER_PORT_2);
} /* End stdlser_rcv_port2_isr */

void stdlser_port2_poll(void)
{
  STDLSER_REG_T             *ser_p;
  STDLI_SER_INFO_T          *serInfo_p;

  ser_p = ((STDLSER_REG_T *)SER1_ADDR) + STDLI_SER_PORT_2;
  serInfo_p = stdlser_glob.serInfo_p[STDLI_SER_PORT_2];
  if (ser_p->SCIxS1 & SCIxS1_RCV_OVERRUN)
  {
    stdlser_rcv_char(STDLI_SER_PORT_2);
  }
  if (serInfo_p->txAct && (ser_p->SCIxS1 & SCIxS1_TDRE))
  {
    stdlser_xmt_char(STDLI_SER_PORT_2);
  }
} /* End stdlser_rcv_port2_poll */

/*
 * ===============================================================================
 * 
 * Name: stdlser_xmt_char
 * 
 * ===============================================================================
 */
/**
 * Function for transmitting a char on a serial port
 * 
 * If the xmt queue isn't empty, set the xmt to active and enable xmt
 * complete ints, send a char to the xmt port, and inc the txHead.  If the
 * xmt queue is empty, clear xmt active, and disable xmt complete ints.
 * 
 * @param   portNum     [in]    Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdlser_xmt_char(
  STDLI_SER_PORT_E          portNum)
{
  STDLI_SER_INFO_T          *serInfo_p;
  STDLSER_REG_T             *ser_p;
  U8                        data;

#define TDRE_FLAG           0x80

  serInfo_p = stdlser_glob.serInfo_p[portNum];
  if (!serInfo_p->txAct)
  {
    serInfo_p->txAct = TRUE;
  }
  
  /* Check if there is a character to be transmitted */
  if (serInfo_p->curTxHead != serInfo_p->curTxTail)
  {        
    /* Send a char serial port */
    ser_p = ((STDLSER_REG_T *)SER1_ADDR) + portNum;
    if (ser_p->SCIxS1 & TDRE_FLAG)
    {
      data = serInfo_p->txBuf_p[serInfo_p->curTxHead]; 
      serInfo_p->curTxHead++;
      if (serInfo_p->curTxHead == serInfo_p->txBufSize)
      {
        serInfo_p->curTxHead = 0;
      }
    }
    
    /* Check if this is the last character */
    if (serInfo_p->curTxHead == serInfo_p->curTxTail)
    {
      /* Clear the transmit done isr bit */
      ser_p->SCIxC2 &= ~SCIxC2_TX_INT_EN;
      serInfo_p->txAct = FALSE;
    }
    ser_p->SCIxD = data; 

  }
} /* End void stdlser_xmt_char */

/*
 * ===============================================================================
 * 
 * Name: stdlser_xmt_data
 * 
 * ===============================================================================
 */
/**
 * Function for transmitting data on a serial port
 * 
 * Copy xmt data to the xmt data queue if space is available.  If no space is
 * avail, either block waiting for space (while petting the watchdog), or return
 * the number of chars that were sent.
 * 
 * @param   portNum     [in]    Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2
 * @param   blocking    [in]    TRUE if wait forever put the tx data on the queue
 * @param   data_p      [in]    Ptr to data to xmt
 * @param   numChar     [in]    Num chars to xmt
 * @return  Num chars sent, always numChar if blocking = TRUE
 * 
 * @pre     stdlser_init_ser_port must be called first.
 * @note    None
 * 
 * ===============================================================================
 */
U16 stdlser_xmt_data(
  STDLI_SER_PORT_E          portNum,      /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
  BOOL                      blocking,     /* TRUE to block waiting to put xmt data on queue */
  U8                        *data_p,      /* Ptr to data to xmt */
  U16                       numChar)      /* Num chars to xmt */
{
  U8                        tmpCnt;
  STDLI_SER_INFO_T          *serInfo_p;
  U8                        nxtIndex;
  BOOL                      spaceAvail;
  STDLSER_REG_T             *ser_p;
  
  serInfo_p = stdlser_glob.serInfo_p[portNum];
  if (serInfo_p == NULL)
  {
    return(0);
  }
  
  for (tmpCnt = 0, spaceAvail = TRUE; 
    (tmpCnt < numChar) && spaceAvail; )
  {
    /* Check if at the end of the tx buffer */
    nxtIndex = serInfo_p->curTxTail + 1;
    if (nxtIndex == serInfo_p->txBufSize)
    {
      nxtIndex = 0;
    }
    if (serInfo_p->curTxHead == nxtIndex)
    {
      if (blocking)
      {
         /* Pet the watchdog timer and try again */
         __RESET_WATCHDOG();
      }
      else
      {
        spaceAvail = FALSE;
      }
    }
    else
    {
      serInfo_p->txBuf_p[serInfo_p->curTxTail] = data_p[tmpCnt];
      serInfo_p->curTxTail = nxtIndex;
      tmpCnt++;
    }
  }
  if (!serInfo_p->txAct)
  {
    /* Since tx is not active, enable the isr bit if not polled */
    serInfo_p->txAct = TRUE;
    if (serInfo_p->pollBit)
    {
      /* Set tx int bit if not polling */
      ser_p = ((STDLSER_REG_T *)SER1_ADDR) + portNum;
      ser_p->SCIxC2 |= SCIxC2_TX_INT_EN;
    }
  }
  return(tmpCnt);
} /* End void stdlser_xmt_data */

/*
 * ===============================================================================
 * 
 * Name: stdlser_xmt_portx_isr
 * 
 * ===============================================================================
 */
/**
 * ISR for tx complete serial port chars
 * 
 * Call send char func passing in the serial port.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
interrupt void stdlser_xmt_port1_isr(void)
{
  stdlser_xmt_char(STDLI_SER_PORT_1);
} /* End stdlser_xmt_port1_isr */

interrupt void stdlser_xmt_port2_isr(void)
{
  stdlser_xmt_char(STDLI_SER_PORT_2);
} /* End stdlser_xmt_port2_isr */

/*
 * ===============================================================================
 * 
 * Name: stdlser_calc_crc8
 * 
 * ===============================================================================
 */
/**
 * Function for calculating the CRC8 of a data stream
 * 
 * Set the initial value of the CRC8 to 0xff, and run the CRC8 calculation using
 * a 16 entry lookup table.
 * 
 * @param   crc8_p      [in]    Ptr to the CRC8.  Data should be 0xff initially
 * @param   length      [in]    Num chars in data stream
 * @param   data_p      [in]    Ptr to data stream
 * @return  None
 * 
 * @pre     None
 * @note    Generator polynomial is x^8+x^2+x+1.  Initial value is 0xff to
 * conform to the ATM HEC CRC8
 * 
 * ===============================================================================
 */
const U8                    CRC8_LOOKUP[16] = 
  { 0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d };
                            
void stdlser_calc_crc8(
  U8                        *crc8_p,      /* Ptr to crc8 */
  U16                       length,       /* Num chars in data stream */
  U8                        *data_p)      /* Ptr to data stream */
{
  U8                        currCrc;
  U16                       count;  

  for (count = 0, currCrc = *crc8_p; count < length; count++)
  {
    currCrc = ((currCrc << 4) & 0xf0) ^ CRC8_LOOKUP[((currCrc ^ data_p[count]) >> 4) & 0x0f];
    currCrc = ((currCrc << 4) & 0xf0) ^ CRC8_LOOKUP[(((currCrc >> 4) & 0x0f) ^ (data_p[count])) & 0x0f];
  }
  *crc8_p = currCrc;
} /* End stdlser_calc_crc8 */
