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
 * @file:   stdli2c.c
 * @author: Hugh Spahr
 * @date:   7/15/2008
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
 * This is the i2c utility file in the Standard Library.  It contains
 * functions for reading/writing i2c devices
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"
#include "stdlglob.h"

#define STDL_FILE_ID        0xfe    /* File ID for logging errors */

#define ENABLE_I2C_GEN_STOP 0x80
#define I2C_INTRPT_FLAG     0x02

typedef enum
{
  I2C_IDLE                  = 0x00,
  I2C_SEND_ADDR             = 0x01,
  I2C_TX_DATA               = 0x02,
  I2C_RX_DATA               = 0x03,
  I2C_SLAVE_RCV_ADDR        = 0x04,
  I2C_SLAVE_XMT             = 0x05,
  I2C_SLAVE_RCV             = 0x06,
} I2C_STATE_T;

typedef struct
{
  I2C_STATE_T               state;
  U8                        currByte;
  STDLI_I2C_XFER_T          *i2cXfer_p;
  STDLI_I2C_SLAVE_T         *slaveI2c_p;
  U8                        intEn;
} STDLI2C_GLOB_T;

STDLI2C_GLOB_T              stdli2c_glob;

/*
 * ===============================================================================
 * 
 * Name: stdli2c_init_i2c
 * 
 * ===============================================================================
 */
/**
 * Initialize the i2c bus
 * 
 * Set the i2c to 200 kbps or 100 kbps for Freescale.
 * 
 * @param   params      [in]    I2C_POLL,I2C_FREESCALE or I2C_SLAVE
 * @param   addr        [in]    i2c slave addr, only valid if I2C_SLAVE is set
 * @param   slave_p     [in]    i2c slave parameters (must not be on stack)
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdli2c_init_i2c(
  STDLI_I2C_E               params,       /* I2C_POLL,I2C_FREESCALE or I2C_SLAVE */
  U8                        addr,         /* Slave i2c addr */
  STDLI_I2C_SLAVE_T         *slave_p)     /* Slave i2c params */
{
#define IICC1_INT_EN        0x40

  IICC2 = 0;                              /* No gen call, 7 bit addr */
  if (params & I2C_FREESCALE)
  {
    IICF = 0x1d;                          /* MUL = 1, ICR = 0x1d, SCLdiv = 160 */
  }
  else
  {
    IICF = 0x00;                          /* MUL = 1, ICR = 0, SCLdiv = 20 */
  }
  if (params & I2C_POLL)
  {
    stdli2c_glob.intEn = 0;
  }
  else
  {
    stdli2c_glob.intEn = IICC1_INT_EN;
  }
  if (params & I2C_SLAVE)
  {
    IICA = addr;
    stdli2c_glob.state = I2C_SLAVE_RCV_ADDR;
    stdli2c_glob.currByte = 0;
    stdli2c_glob.slaveI2c_p = slave_p;
  }
  else
  {
    stdli2c_glob.state = I2C_IDLE;
    stdli2c_glob.slaveI2c_p = NULL;
  }
  IICC1 = (ENABLE_I2C_GEN_STOP | stdli2c_glob.intEn);
  IICS = I2C_INTRPT_FLAG;  /* Clear arbitration loss bit */
  
  stdli2c_glob.i2cXfer_p = NULL;
} /* End stdli2c_init_i2c */

/*
 * ===============================================================================
 * 
 * Name: stdli2c_send_i2c_msg
 * 
 * ===============================================================================
 */
/**
 * Send an i2c message to read/write data
 * 
 * Verify the i2c state machine is idle.  Set i2c controller to start
 * transmitting.  Write the address of the slave to access.
 * 
 * @param   i2cXfer_p   [in]    ptr that contains address, data_p, num bytes, and
 *                              call back information.
 * @return  STDLI_I2C_NOT_IDLE if bus not idle
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
STDLI_ERR_E stdli2c_send_i2c_msg(
  STDLI_I2C_XFER_T          *i2cXfer_p)   /* ptr to i2c xfer structure */
{
#define START_MSTR_XMT      0xb0

  /* If bus is not idle, return an error */
  if (stdli2c_glob.state != I2C_IDLE)
  {
    return(STDLI_I2C_NOT_IDLE);
  }
  
  stdli2c_glob.state = I2C_SEND_ADDR;
  stdli2c_glob.currByte = 0;
  stdli2c_glob.i2cXfer_p = i2cXfer_p;
  IICC1 = (START_MSTR_XMT | stdli2c_glob.intEn);
  IICD = i2cXfer_p->addr;
  return(0);
} /* End stdli2c_send_i2c_msg */

/*
 * ===============================================================================
 * 
 * Name: stdli2c_i2c_isr
 * 
 * ===============================================================================
 */
/**
 * I2C interrupt service routine
 * 
 * Clear the interrupt flag.  If sending the address, verify it has been
 * acknowledged, and move to tx data, or rx data state.  If in tx data state,
 * verify the byte has been acknowledged, and send another byte if necessary.
 * If in rx data state, and 2nd to last byte, send tx ack, if last byte,
 * end the cycle.  Grab the data that has been received and store it in the
 * structure.   
 * 
 * @param None 
 * @return None
 * 
 * @pre None 
 * @note None
 * 
 * ===============================================================================
 */
void stdli2c_i2c_complete(void)
{
  U8                        status;
  BOOL                      genStop;
  STDLI_I2C_RESP_E          resp;
  R8                        tmpReg;
  
#define NO_ACK_RCVD         0x01
#define LOST_ARBITRATION    0x10
#define ADDR_AS_SLAVE       0x40
#define SLAVE_READ_WR       0x04
#define START_MSTR_RCV      0xa0
#define TX_ACK_ENABLE       0xa8
#define SLAVE_TX            0x90
#define SLAVE_RX            0x80
#define MSTA_BIT            0x20
  
  /* Clear interrupt flag */
  status = IICS;
  status |= I2C_INTRPT_FLAG;
  IICS = status;
  
  /* If an ack was received */
  genStop = FALSE;
  switch (stdli2c_glob.state)
  {
    case I2C_SEND_ADDR:
    {
      /* Verify ack was rcvd, and didn't lose arbitration */
      if (((status & NO_ACK_RCVD) == 0) &&
        ((status & LOST_ARBITRATION) == 0))
      {
        /* Check if this is a read/write msg */
        if (stdli2c_glob.i2cXfer_p->addr &
          STDLI_I2C_READ_ADDR)
        {
          /* Switch to rx mode, perform dummy read */
          if (stdli2c_glob.i2cXfer_p->numDataBytes == 1)
          {
            IICC1 = (START_MSTR_RCV | TX_ACK_ENABLE | stdli2c_glob.intEn);
          }
          else
          {
            IICC1 = (START_MSTR_RCV | stdli2c_glob.intEn);
          }
          status = IICD;
          stdli2c_glob.state = I2C_RX_DATA;
        }
        else
        {
          /* Write msg */
          IICD = stdli2c_glob.i2cXfer_p->data_p[0];
          stdli2c_glob.state = I2C_TX_DATA;
          stdli2c_glob.currByte++;
        }
      }
      else
      {
        IICS = (status & ~LOST_ARBITRATION);
        resp = STDLI_I2C_NO_RESP;
        IICC1 = (ENABLE_I2C_GEN_STOP | stdli2c_glob.intEn);
        genStop = TRUE;
      }
      break;
    }
    case I2C_TX_DATA:
    {
      /* Check if done */
      if (stdli2c_glob.currByte < stdli2c_glob.i2cXfer_p->numDataBytes)
      {
        /* Verify ack was rcvd */
        if ((status & NO_ACK_RCVD) == 0)
        {
          IICD = stdli2c_glob.i2cXfer_p->data_p[stdli2c_glob.currByte];
          stdli2c_glob.currByte++;
        }
        else
        {
          resp = STDLI_I2C_NO_RESP;
          genStop = TRUE;
        }
      }
      else
      {
        /* all done */
        resp = STDLI_I2C_XFER_OK;
        genStop = TRUE;
      }
      if (genStop)
      {
        IICC1 = (ENABLE_I2C_GEN_STOP | stdli2c_glob.intEn);
      }
      break;
    }
    case I2C_RX_DATA:
    {
      /* Check if this is the 2nd to last byte */
      if (stdli2c_glob.currByte == (stdli2c_glob.i2cXfer_p->numDataBytes - 2))
      {
        /* Set the txAck bit */
        IICC1 = (TX_ACK_ENABLE | stdli2c_glob.intEn);
      }
      if (stdli2c_glob.currByte == stdli2c_glob.i2cXfer_p->numDataBytes - 1)
      {
        resp = STDLI_I2C_XFER_OK;
        genStop = TRUE;
        IICC1 = (ENABLE_I2C_GEN_STOP | stdli2c_glob.intEn);
      }
      stdli2c_glob.i2cXfer_p->data_p[stdli2c_glob.currByte] = IICD;
      stdli2c_glob.currByte++;
      break;
    }
    case I2C_SLAVE_RCV_ADDR:
    {  
      /* Slave rcv, first byte is addr match.  Verify arb isn't lost and  */
      if ((status & (LOST_ARBITRATION | ADDR_AS_SLAVE)) == ADDR_AS_SLAVE)
      {
        /* Look at slave read/write bit */
        if (status & SLAVE_READ_WR)
        {
          /* Slave read */
          if (stdli2c_glob.i2cXfer_p) 
          {
            IICC1 = (SLAVE_TX | stdli2c_glob.intEn);
            IICD = *stdli2c_glob.i2cXfer_p->data_p;
            stdli2c_glob.i2cXfer_p->data_p++;
            stdli2c_glob.i2cXfer_p->numDataBytes--;
            
            /* Check if slave only needs to rcv a single byte. */
            if (stdli2c_glob.i2cXfer_p->numDataBytes == 0)
            {
              stdli2c_glob.i2cXfer_p->i2cDone_fp(stdli2c_glob.i2cXfer_p->cbParm,
                STDLI_I2C_XFER_OK);
            }
            stdli2c_glob.state = I2C_SLAVE_XMT;
          }
          else
          {
            /* Driver was not prepared to send data.  The master
             * needs to send a command for what data is needed before
             * requesting the data.
             */
            STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
              STDLI_SW_ERROR), I2C_SLAVE_RCV_ADDR, status);
          }
        }
        else
        {
          /* Slave write, perform dummy read */
          IICC1 = (SLAVE_RX | stdli2c_glob.intEn);
          tmpReg = IICD;
          stdli2c_glob.state = I2C_SLAVE_RCV;
          
          /* currByte is used as a flag cmd callback */
          stdli2c_glob.currByte = 0;
        }
      }
      else
      {
        if (status)
        {
          status++;
        }
        STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
          STDLI_SW_ERROR), I2C_SLAVE_RCV_ADDR, status);
      }
      break;
    }
    case I2C_SLAVE_XMT:
    {  
      /* Slave rcv, first byte is addr match.  Verify arb isn't lost and  */
      if ((status & LOST_ARBITRATION) == 0)
      {
        /* Look at rx ack bit */
        if ((status & NO_ACK_RCVD) == 0)
        {
          IICD = *stdli2c_glob.i2cXfer_p->data_p;
          stdli2c_glob.i2cXfer_p->data_p++;
          stdli2c_glob.i2cXfer_p->numDataBytes--;
          if (stdli2c_glob.i2cXfer_p->numDataBytes == 0)
          {
            stdli2c_glob.i2cXfer_p->i2cDone_fp(stdli2c_glob.i2cXfer_p->cbParm,
              STDLI_I2C_XFER_OK);
          }
        }
        else
        {
          /* No ack received, switch to rx mode, and perform dummy read.
           *  This should be the end of the cycle.
           */
          IICC1 = (SLAVE_RX | stdli2c_glob.intEn);
          status = IICD;
          stdli2c_glob.state = I2C_SLAVE_RCV_ADDR;
        }
      }
      else
      {
        STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
          STDLI_SW_ERROR), I2C_SLAVE_XMT, status);
      }
      break;
    }
    case I2C_SLAVE_RCV:
    {  
      /* Slave rcv, first byte is addr match.  Verify arb isn't lost and  */
      if ((status & LOST_ARBITRATION) == 0)
      {
        if (stdli2c_glob.currByte == 0) 
        {
          /* Mark the cmd as being received */
          stdli2c_glob.currByte = 1;
          status = IICD;
          stdli2c_glob.slaveI2c_p->cmd = status;
          stdli2c_glob.slaveI2c_p->slaveCmd_fp(status,
            &stdli2c_glob.slaveI2c_p->cmdLen,
            &stdli2c_glob.slaveI2c_p->cmdDest_p);
          if (stdli2c_glob.slaveI2c_p->cmdLen == 0)
          {
            stdli2c_glob.state = I2C_SLAVE_RCV_ADDR;
          }
        }
        else if (stdli2c_glob.slaveI2c_p->cmdLen)
        {
          *stdli2c_glob.slaveI2c_p->cmdDest_p = IICD;
          stdli2c_glob.slaveI2c_p->cmdDest_p++;
          stdli2c_glob.slaveI2c_p->cmdLen--;
        }
        else
        {
          /* Driver ask for too much data.  The master-slave
           * protocol wasn't followed.
           */
          STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
            STDLI_SW_ERROR), I2C_SLAVE_XMT, status);
        }
        if (stdli2c_glob.slaveI2c_p->cmdLen == 0)
        {
          /* Cmd is done, use callback to fill out next rcv
           * packet parameters.  If the next packet isn't
           * a slave xmt packet, NULL should be returned.
           */
          stdli2c_glob.slaveI2c_p->slaveRcvDone_fp(
            stdli2c_glob.slaveI2c_p->cmd,
            &stdli2c_glob.i2cXfer_p);
          stdli2c_glob.state = I2C_SLAVE_RCV_ADDR;
        }
      }
      else
      {
        STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
          STDLI_SW_ERROR), I2C_SLAVE_RCV, status);
      }
      break;
    }
    case I2C_IDLE:
    default:
    {
      STDLI_K_FATAL_M((U16)(STDLI_CRITICAL_FAIL |
        STDLI_SW_ERROR), stdli2c_glob.state, 0);
      break;
    }
  }
  if (genStop)
  {
    /* Change state to idle, call callback func with response. */
    stdli2c_glob.state = I2C_IDLE;
    stdli2c_glob.i2cXfer_p->i2cDone_fp(stdli2c_glob.i2cXfer_p->cbParm,
      resp);
  }
} /* End stdli2c_i2c_complete */

interrupt void stdli2c_i2c_complete_isr(void)
{
  stdli2c_i2c_complete();
} /* End stdli2c_i2c_complete_isr */

void stdli2c_i2c_complete_poll(void)
{
  if (IICS & I2C_INTRPT_FLAG)
  {
    stdli2c_i2c_complete();
  }
} /* End stdli2c_i2c_complete_poll */
