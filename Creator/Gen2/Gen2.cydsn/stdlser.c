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
 * @note:    Copyright© 2008-2015, Hugh Spahr
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
#include "stdlintf.h"
#include "stdlglob.h"

#define TX_FIFO_TRIGGER       4

#define SCB1_ADDR_OFFSET      0x00010000

#define SCB0_TX_FIFO_STATUS   0x40060208
#define TX_FIFO_USED_MASK     0x0000000f

#define SCB0_TX_FIFO_WR       0x40060240

#define SCB0_RX_FIFO_STATUS   0x40060308
#define RX_FIFO_USED_MASK     0x0000000f

#define SCB0_RX_FIFO_RD       0x40060340

#define SCB0_INTR_TX          0x40060f80

#define SCB0_INTR_TX_MASK     0x40060f88
#define INTR_TX_SCB_TRIGGER   0x00000001

#define SCB0_INTR_RX          0x40060fc0
#define INTR_RX_SCB_NOT_EMPTY 0x00000004

#define SCB0_INTR_RX_MASK     0x40060fc8

typedef struct
{
   STDLI_SER_INFO_T           *serInfo_p[STDLI_NUM_SER_PORT];
} STDLSER_GLOB_T;

STDLSER_GLOB_T                stdlser_glob;

/* Prototypes: */
void stdlser_xmt_char(
  STDLI_SER_PORT_E            portNum);

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
  STDLI_SER_PORT_E            portNum,       /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
  STDLI_SER_INFO_T            *serInfo_p)    /* Ser state, txBuf addr, txBuf size, rx
                                              *  callback func.
                                              */
{
#define PORT_NUM_MASK         0x01
   
   R32                        *intrTxMaskReg_p;
   R32                        *intrRxMaskReg_p;
   
   if ((portNum & PORT_NUM_MASK) == STDLI_SER_PORT_1)
   {
      intrTxMaskReg_p = (R32 *)SCB0_INTR_TX_MASK;
      intrRxMaskReg_p = (R32 *)SCB0_INTR_RX_MASK;
   }
   else
   {
      intrTxMaskReg_p = (R32 *)(SCB0_INTR_TX_MASK + SCB1_ADDR_OFFSET);
      intrRxMaskReg_p = (R32 *)(SCB0_INTR_RX_MASK + SCB1_ADDR_OFFSET);
   }
   
   serInfo_p->curTxHead = 0;
   serInfo_p->curTxTail = 0;
   serInfo_p->txAct = FALSE;
   if (portNum & STDLI_POLL_SER_PORT)
   {
      /* Mask interrupts */
      serInfo_p->poll = TRUE;
      *intrRxMaskReg_p &= ~INTR_RX_SCB_NOT_EMPTY;
   }
   else
   {
      /* Enable rx interrupt */
      serInfo_p->poll = FALSE;
      *intrRxMaskReg_p |= INTR_RX_SCB_NOT_EMPTY;
   }
   *intrTxMaskReg_p &= ~INTR_TX_SCB_TRIGGER;
   stdlser_glob.serInfo_p[portNum & PORT_NUM_MASK] = serInfo_p;
  
   /* HRS: Configure the pins/baud rate, currently done by autogen */

} /* End stdlser_init_ser_port */

/*
 * ===============================================================================
 * 
 * Name: stdlser_get_rcv_data
 * 
 * ===============================================================================
 */
/**
 * Function for getting serial port char
 * 
 * Read the rcv data, to clear the ISR.  Check if a rcv function has been
 * registered.  If so, call the rcv function.
 * 
 * @param   portNum     [in]    Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2
 * @return  TRUE if serial character is available
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
BOOL stdlser_get_rcv_data(
   STDLI_SER_PORT_E           portNum,      /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
   U8                         *data_p)      /* Rcv'd character */
{
   STDLI_SER_INFO_T           *serInfo_p;
   R32                        *rxFifoRdReg_p;
   R32                        *rxFifoStatusReg_p;
   R32                        *intrRxMaskReg_p;

   /* Clear the interrupt bit */
   serInfo_p = stdlser_glob.serInfo_p[portNum];
  
   /* If the serial port has been registered, call callback function */
   if (serInfo_p != NULL)
   {
      if (portNum == STDLI_SER_PORT_1)
      {
         rxFifoStatusReg_p = (R32 *)SCB0_RX_FIFO_STATUS;
         rxFifoRdReg_p = (R32 *)SCB0_RX_FIFO_RD;
         intrRxMaskReg_p = (R32 *)SCB0_INTR_RX_MASK;
      }
      else
      {
         rxFifoStatusReg_p = (R32 *)(SCB0_RX_FIFO_STATUS + SCB1_ADDR_OFFSET);
         rxFifoRdReg_p = (R32 *)(SCB0_RX_FIFO_RD + SCB1_ADDR_OFFSET);
         intrRxMaskReg_p = (R32 *)(SCB0_INTR_RX_MASK + SCB1_ADDR_OFFSET);
      }
      if ((*(R32 *)rxFifoStatusReg_p & RX_FIFO_USED_MASK) != 0)
      {
         *data_p = (U8)(*rxFifoRdReg_p & 0xff);
         return (TRUE);
      }
      else
      {
         /* No more data, so re-enable the rx interrupt */
         *intrRxMaskReg_p |= INTR_RX_SCB_NOT_EMPTY;
      }
   }
   return (FALSE);
} /* End stdlser_rcv_char */

/*
 * ===============================================================================
 * 
 * Name: stdlser_isr
 * 
 * ===============================================================================
 */
/**
 * ISR for rcving/xmting serial port chars
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
void stdlser_port1_poll(void)
{
   STDLI_SER_INFO_T           *serInfo_p;

   serInfo_p = stdlser_glob.serInfo_p[STDLI_SER_PORT_1];
   if ((*(R32 *)SCB0_RX_FIFO_STATUS & RX_FIFO_USED_MASK) != 0)
   {
      /* Mask rx interrupts */
      *(R32 *)SCB0_INTR_RX_MASK &= ~INTR_RX_SCB_NOT_EMPTY;
      serInfo_p->rxSerChar_fp(serInfo_p->cbParm_p);
   }
   if (*(R32 *)SCB0_INTR_RX & INTR_RX_SCB_NOT_EMPTY)
   {
      *(R32 *)SCB0_INTR_RX |= INTR_RX_SCB_NOT_EMPTY;
   }
   if ((((*(R32 *)SCB0_TX_FIFO_STATUS) & TX_FIFO_USED_MASK) <= TX_FIFO_TRIGGER) && serInfo_p->txAct)
   {
      stdlser_xmt_char(STDLI_SER_PORT_1);
   }
   if (*(R32 *)SCB0_INTR_TX & INTR_TX_SCB_TRIGGER)
   {
      *(R32 *)SCB0_INTR_TX |= INTR_TX_SCB_TRIGGER;
   }
} /* End stdlser_port1_poll */

void stdlser_port1_isr(void)
{
   stdlser_port1_poll();
} /* End stdlser_port1_isr */

void stdlser_port2_poll(void)
{
   STDLI_SER_INFO_T           *serInfo_p;

   serInfo_p = stdlser_glob.serInfo_p[STDLI_SER_PORT_2];
   if (((*(R32 *)(SCB0_RX_FIFO_STATUS + SCB1_ADDR_OFFSET)) & RX_FIFO_USED_MASK) != 0)
   {
      /* Mask rx interrupts */
      *(R32 *)(SCB0_INTR_RX + SCB1_ADDR_OFFSET) |= INTR_RX_SCB_NOT_EMPTY;
      serInfo_p->rxSerChar_fp(serInfo_p->cbParm_p);
   }
   if (*(R32 *)(SCB0_INTR_RX + SCB1_ADDR_OFFSET) & INTR_RX_SCB_NOT_EMPTY)
   {
      *(R32 *)(SCB0_INTR_RX + SCB1_ADDR_OFFSET) |= INTR_RX_SCB_NOT_EMPTY;
   }
   if ((((*(R32 *)SCB0_TX_FIFO_STATUS + SCB1_ADDR_OFFSET) & TX_FIFO_USED_MASK) <= TX_FIFO_TRIGGER) && serInfo_p->txAct)
   {
      *(R32 *)(SCB0_INTR_TX + SCB1_ADDR_OFFSET) |= INTR_TX_SCB_TRIGGER;
      stdlser_xmt_char(STDLI_SER_PORT_2);
   }
   if (*(R32 *)(SCB0_INTR_TX + SCB1_ADDR_OFFSET) & INTR_TX_SCB_TRIGGER)
   {
      *(R32 *)(SCB0_INTR_TX + SCB1_ADDR_OFFSET) |= INTR_TX_SCB_TRIGGER;
   }
} /* End stdlser_port2_poll */

void stdlser_port2_isr(void)
{
   stdlser_port2_poll();
} /* End stdlser_port2_isr */

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
   STDLI_SER_PORT_E           portNum)
{
   STDLI_SER_INFO_T           *serInfo_p;
   R32                        *txFifoWrReg_p;
   R32                        *intrTxMaskReg_p;
   R32                        *txFifoStatusReg_p;

   if (portNum == STDLI_SER_PORT_1)
   {
      txFifoWrReg_p = (R32 *)SCB0_TX_FIFO_WR;
      intrTxMaskReg_p = (R32 *)SCB0_INTR_TX_MASK;
      txFifoStatusReg_p = (R32 *)SCB0_TX_FIFO_STATUS;
   }
   else
   {
      txFifoWrReg_p = (R32 *)(SCB0_TX_FIFO_WR + SCB1_ADDR_OFFSET);
      intrTxMaskReg_p = (R32 *)(SCB0_INTR_TX_MASK + SCB1_ADDR_OFFSET);
      txFifoStatusReg_p = (R32 *)(SCB0_TX_FIFO_STATUS + SCB1_ADDR_OFFSET);
   }
   serInfo_p = stdlser_glob.serInfo_p[portNum];
  
   /* Check if there is a character to be transmitted */
   if (serInfo_p->curTxHead != serInfo_p->curTxTail)
   {
      /* While the Tx FIFO is not full */
      while (((*txFifoStatusReg_p & TX_FIFO_USED_MASK) != 8) &&
        (serInfo_p->curTxHead != serInfo_p->curTxTail))
      {
         /* Send the byte */
         *txFifoWrReg_p = serInfo_p->txBuf_p[serInfo_p->curTxHead];
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
         serInfo_p->txAct = FALSE;
         *intrTxMaskReg_p &= ~INTR_TX_SCB_TRIGGER;
      }
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
INT stdlser_xmt_data(
   STDLI_SER_PORT_E           portNum,      /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
   BOOL                       blocking,     /* TRUE to block waiting to put xmt data on queue */
   U8                         *data_p,      /* Ptr to data to xmt */
   U16                        numChar)      /* Num chars to xmt */
{
   INT                        tmpCnt;
   STDLI_SER_INFO_T           *serInfo_p;
   U8                         nxtIndex;
   BOOL                       spaceAvail;
   R32                        *intrTxMaskReg_p;
  
   serInfo_p = stdlser_glob.serInfo_p[portNum];
   if (serInfo_p == NULL)
   {
      return(0);
   }
   if (portNum == STDLI_SER_PORT_1)
   {
      intrTxMaskReg_p = (R32 *)SCB0_INTR_TX_MASK;
   }
   else
   {
      intrTxMaskReg_p = (R32 *)(SCB0_INTR_TX_MASK + SCB1_ADDR_OFFSET);
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
      if (!serInfo_p->poll)
      {
         /* Set tx int bit if not polling */
         *intrTxMaskReg_p |= INTR_TX_SCB_TRIGGER;
      }
   }
   return(tmpCnt);
} /* End void stdlser_xmt_data */

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
const U8                    CRC8_NIBBLE_LOOKUP[16] = 
  { 0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d };

const U8                    CRC8_BYTE_LOOKUP[256] =
{
   0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, \
   0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, \
   0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, \
   0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, \
   0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, \
   0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, \
   0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, \
   0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, \
   0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, \
   0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, \
   0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, \
   0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, \
   0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, \
   0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, \
   0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, \
   0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
};

void stdlser_calc_crc8(
   U8                        *crc8_p,      /* Ptr to crc8 */
   INT                       length,       /* Num chars in data stream */
   U8                        *data_p)      /* Ptr to data stream */
{
   U8                        currCrc;
   U16                       count;
   U8                        crc8Byte;

   for (count = 0, currCrc = *crc8_p, crc8Byte = *crc8_p; count < length; count++)
   {
      currCrc = ((currCrc << 4) & 0xf0) ^ CRC8_NIBBLE_LOOKUP[((currCrc ^ data_p[count]) >> 4) & 0x0f];
      currCrc = ((currCrc << 4) & 0xf0) ^ CRC8_NIBBLE_LOOKUP[(((currCrc >> 4) & 0x0f) ^ (data_p[count])) & 0x0f];
      crc8Byte = CRC8_BYTE_LOOKUP[crc8Byte ^ data_p[count]];
   }
   *crc8_p = currCrc;
} /* End stdlser_calc_crc8 */
