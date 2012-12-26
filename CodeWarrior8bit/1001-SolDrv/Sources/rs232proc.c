/*
 *===============================================================================
 *
 *                         OOOO
 *                       OOOOOOOO
 *      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *  PPP          PPP   OOO      OOO   PPP          PPP
 *   PPP         PPP   OOO      OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP   OOO      OOO   PPP
 *               PPP    OOO    OOO    PPP
 *               PPP     OOOOOOOO     PPP
 *              PPPPP      OOOO      PPPPP
 *
 * @file:   rs232proc.c
 * @author: Hugh Spahr
 * @date:   12/06/2012
 *
 * @note:   Open Pinball Project
 *          Copyright© 2012, Hugh Spahr
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
 * This is the serial port processing for the solenoid driver board.  It
 * uses the first serial port.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"
#include "stdlintf.h"
#include <hidef.h>          /* for EnableInterrupts macro */
#include "interrupt.h"      /* For prod ID, version num */
#define RS232I_INSTANTIATE
#include "rs232intf.h"
#include "solglob.h"

#define STDL_FILE_ID        2

#define TX_BUF_SIZE         0x10
#define RX_BUF_SIZE         0x04

typedef enum
{
  RS232_WAIT_FOR_CARD_ID    = 0x00,
  RS232_WAIT_FOR_CMD        = 0x01,
  RS232_PASSTHRU_CMD        = 0x02,
  RS232_STRIP_CMD           = 0x03,
  RS232_RCV_DATA_CMD        = 0x04,   /* Also strips the data */
  RS232_INVENTORY_CMD       = 0x05,   /* Special case since unknown length */
} RS232_STATE_E;

typedef struct
{
  RS232_STATE_E             state;
  BOOL                      rcvChar;
  BOOL                      myCmd;
  U8                        rcvData;
  U8                        myAddr;
  U8                        cmdLen;
  RS232I_CMD_E              currCmd;
  U8                        currIndex;
  U8                        txBuf[TX_BUF_SIZE];
  U8                        rxBuf[RX_BUF_SIZE];
  STDLI_SER_INFO_T          serInfo;
} RS232_GLOB_T;

RS232_GLOB_T                rs232_glob;

/* Prototypes */
void rs232proc_rx_ser_char(
  U16                       cbParam,
  U8                        data);
void rs232proc_force_boot_mode(void);

/*
 * ===============================================================================
 * 
 * Name: rs232proc_init
 * 
 * ===============================================================================
 */
/**
 * Initialize RS232 processing
 * 
 * Initialize serial port link.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void rs232proc_init(void) 
{
  /* Initialize the global structure */
  rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
  rs232_glob.rcvChar = FALSE;
  rs232_glob.myCmd = FALSE;
  
  /* Initialize the serial port */
  rs232_glob.serInfo.txBuf_p = &rs232_glob.txBuf[0];
  rs232_glob.serInfo.txBufSize = TX_BUF_SIZE;
  rs232_glob.serInfo.rxSerChar_fp = rs232proc_rx_ser_char;
  rs232_glob.serInfo.cbParm = 0;
  stdlser_init_ser_port(STDLI_SER_PORT_1,
    &rs232_glob.serInfo);
  
} /* End rs232proc_init */

/*
 * ===============================================================================
 * 
 * Name: rs232proc_task
 * 
 * ===============================================================================
 */
/**
 * Task for rs232 commands
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void rs232proc_task(void)
{
  U8                        data;
  U8                        txBuf[6];
  U8                        *src_p;
  U8                        *dest_p;
  U8                        index;

#define MAGIC_NUM           0xa5
#define RAM_FIRST_ADDR      0x80
  
  /* Check if received a char */
  if (rs232_glob.rcvChar)
  {
    rs232_glob.rcvChar = FALSE;
    data = rs232_glob.rcvData;
    if (rs232_glob.state == RS232_WAIT_FOR_CARD_ID)
    {
      rs232_glob.myCmd = FALSE;
      if (data == RS232I_INVENTORY)
      {
        rs232_glob.state = RS232_INVENTORY_CMD;
        rs232_glob.myAddr = MAX_U8;
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      }
      else if (data == RS232I_EOM)
      {
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      }
      else if (data == rs232_glob.myAddr)
      {
        /* It is my command, it may or may not need stripped */
        rs232_glob.state = RS232_WAIT_FOR_CMD;
        rs232_glob.myCmd = TRUE;
      }
      else
      {
        /* It is not my cmd but inspect for length */
        rs232_glob.state = RS232_WAIT_FOR_CMD;
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      }
    }
    else if (rs232_glob.state == RS232_WAIT_FOR_CMD)
    {
      rs232_glob.currIndex = 0;
      if (data < RS232I_NUM_CMDS)
      {
        rs232_glob.currCmd = data;
        rs232_glob.cmdLen = CMD_LEN[data];
        if (rs232_glob.myCmd)
        {
          txBuf[0] = rs232_glob.myAddr;
          txBuf[1] = data;
          if (data == RS232I_GET_SER_NUM)
          {
            for (index = 0, src_p = (U8 *)SERNUM_ADDR, dest_p = &txBuf[2];
              index < sizeof(U32); index++)
            {
              *dest_p++ = *src_p++;
            }
            rs232_glob.state = RS232_STRIP_CMD;
            (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 6);
          }
          else if (data == RS232I_GET_PROD_ID)
          {
            for (index = 0, src_p = (U8 *)&appStart.prodId, dest_p = &txBuf[2];
              index < sizeof(U32); index++)
            {
              *dest_p++ = *src_p++;
            }
            rs232_glob.state = RS232_STRIP_CMD;
            (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 6);
          }
          else if (data == RS232I_GET_VERS)
          {
            for (index = 0, src_p = (U8 *)&appStart.codeVersion[0], dest_p = &txBuf[2];
              index < sizeof(U32); index++)
            {
              *dest_p++ = *src_p++;
            }
            rs232_glob.state = RS232_STRIP_CMD;
            (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 6);
          }
          else if (data == RS232I_SET_SER_NUM)
          {
            /* Check if serial number is blank, strip cmd */
            if (*(U32 *)SERNUM_ADDR == MAX_U32)
            {
              rs232_glob.state = RS232_RCV_DATA_CMD;
            }
            else
            {
              /* Already set, so allow cmd to pass through */
              rs232_glob.state = RS232_PASSTHRU_CMD;
              (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 2);
            }
          }
          else if (data == RS232I_RESET)
          {
            /* Reset the processor */
            asm DCB 0x8D ;    /* Use illegal instruction to cause reset */
          }
          else if (data == RS232I_GO_BOOT)
          {
            /* Write the magic number */
            *(U8 *)RAM_FIRST_ADDR = MAGIC_NUM;

            /* Reset the processor */
            asm DCB 0x8D ;    /* Use illegal instruction to cause reset */
          }
          else if (data == RS232I_CONFIG_SOL)
          {
            rs232_glob.state = RS232_RCV_DATA_CMD;
          }
          else if (data == RS232I_KICK_SOL)
          {
            rs232_glob.state = RS232_RCV_DATA_CMD;
          }
          else if (data == RS232I_READ_SOL_INP)
          {
            rs232_glob.state = RS232_STRIP_CMD;
            DisableInterrupts;
            txBuf[2] = solg_glob.validSwitch;
            solg_glob.validSwitch = 0;
            EnableInterrupts;
            (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 3);
          }
          else
          {
            /* Bad command received, send EOM */
            data = RS232I_EOM;
            (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
            rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
          }
        }
        else
        {
          /* Not my command, so send it through */
          rs232_glob.state = RS232_PASSTHRU_CMD;
          (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
        }
      }
      else
      {
        /* Bad command received, send EOM */
        data = RS232I_EOM;
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
        rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
      }
    }
    else if (rs232_glob.state == RS232_PASSTHRU_CMD)
    {
      (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      rs232_glob.currIndex++;
      if (rs232_glob.currIndex >= rs232_glob.cmdLen)
      {
        /* Whole command has been passed on, now wait for next cmd */
        rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
      }
    }
    else if (rs232_glob.state == RS232_STRIP_CMD)
    {
      rs232_glob.currIndex++;
      if (rs232_glob.currIndex >= rs232_glob.cmdLen)
      {
        /* Whole command has been passed on, now wait for next cmd */
        rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
      }
    }
    else if (rs232_glob.state == RS232_RCV_DATA_CMD)
    {
      if (rs232_glob.currCmd == RS232I_SET_SER_NUM)
      {
        rs232_glob.rxBuf[rs232_glob.currIndex++] = data;
        if (rs232_glob.currIndex >= rs232_glob.cmdLen)
        {
          /* Save the data in the flash */
          dest_p = (U8 *)SERNUM_ADDR;
          for (index = 0; index < sizeof(U32); index++)
          {
            stdleeprom_start_flash_write(dest_p + index,
              rs232_glob.rxBuf[index]);
          }
          rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
        }
      }
      else if (rs232_glob.currCmd == RS232I_CONFIG_SOL)
      {
        /* Store data directly in structure */
        ((U8 *)&solg_glob.solCfg[0])[rs232_glob.currIndex++] = data;
        if (rs232_glob.currIndex >= rs232_glob.cmdLen)
        {
          solg_glob.state = SOL_STATE_NORM;
          solg_glob.stateMask = 0;
          for (index = 0; index < RS232I_NUM_SOL; index++)
          {
            if ((solg_glob.solCfg[index].type & USE_SWITCH) == 0)
            {
              solg_glob.stateMask |= (1 << index);
            }
          }
          rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
        }
      }
      else if (rs232_glob.currCmd == RS232I_KICK_SOL)
      {
        rs232_glob.rxBuf[rs232_glob.currIndex++] = data;
        if (rs232_glob.currIndex >= rs232_glob.cmdLen)
        {
          DisableInterrupts;
          solg_glob.procCtl = (solg_glob.procCtl & ~rs232_glob.rxBuf[1]) |
            rs232_glob.rxBuf[0];
          EnableInterrupts;
          rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
        }
      }
      else
      {
        /* Invalid cmd for RS232_RCV_DATA_CMD, send EOM */
        data = RS232I_EOM;
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
        rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
      }
    }
    else if (rs232_glob.state == RS232_INVENTORY_CMD)
    {
      if (data == RS232I_EOM)
      {
        /* Rcv'd EOM, so my addr is next addr */
        if (rs232_glob.myAddr == MAX_U8)
        {
          rs232_glob.myAddr = CARD_ID_SOL_CARD;
        }
        else
        {
          rs232_glob.myAddr++;
        }
        txBuf[0] = rs232_glob.myAddr;
        txBuf[1] = RS232I_EOM;
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 2);
        rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
      }
      else if ((data & CARD_ID_TYPE_MASK) == CARD_ID_SOL_CARD)
      {
        rs232_glob.myAddr = data;
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      }
      else
      {
        /* Not my card type and make no assumptions, pass thru */
        (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      }
    }
    else
    {
      /* Invalid state, send EOM */
      data = RS232I_EOM;
      (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
      rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
    }
  }
} /* End rs232proc_task */

/*
 * ===============================================================================
 * 
 * Name: rs232proc_rx_ser_char
 * 
 * ===============================================================================
 */
/**
 * Receive serial character
 * 
 * Grab the serial character.  Save the character and mark the flag.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void rs232proc_rx_ser_char(
  U16                       cbParam,
  U8                        data)
{
  cbParam = 0;
  
  rs232_glob.rcvChar = TRUE;
  rs232_glob.rcvData = data;
} /* End rs232proc_rx_ser_char */
