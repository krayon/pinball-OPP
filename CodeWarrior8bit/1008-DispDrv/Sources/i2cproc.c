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
 * @file:   i2cproc.c
 * @author: Hugh Spahr
 * @date:   11/30/2012
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
 * This is the I2c processing file.  It interfaces 16 bit register chips
 *
 *===============================================================================
 */
 
#include "stdtypes.h"
#include "stdlintf.h"
#include "dispglob.h"
#include "derivative.h" /* include for petting the watchdog */

#define STDL_FILE_ID        2

#define MAX_SEND_SIZE       3

typedef enum
{
  I2C_STATE_IDLE            = 0x00,
  I2C_STATE_SEND            = 0x01,
} I2C_STATE_E;

typedef struct
{
  volatile I2C_STATE_E      state;
  U8                        currPlyr;
  U8                        valPlyr;
  U8                        txBuf[MAX_SEND_SIZE];
  STDLI_I2C_RESP_E          msgStatus;
  STDLI_I2C_XFER_T          i2cMsg;
  STDLI_TIMER_EVENT_T       timeEvt;
} I2C_GLOB_T;

I2C_GLOB_T                  i2c_glob;

U8                          charLkup[MAX_CHAR_ID] = {
  0x3f /* 0 */, 0x06 /* 1 */, 0x6b /* 2 */, 0x4f /* 3 */, 0x66 /* 4 */,
  0x1b /* 5 */, 0x7d /* 6 */, 0x07 /* 7 */, 0x7f /* 8 */, 0x67 /* 9 */,
  0x00 /*   */, 0x00 /*   */, 0x00 /*   */, 0x00 /*   */, 0x00 /*   */, 
  0x73 /* P */, 0x79 /* E */, 0x37 /* N */, 0x38 /* L */, 0x77 /* A */,
  0x1e /* J */, 0x39 /* C */ };

U8                          i2cAddrLkup[DISPG_NUM_DISP][CHARS_PER_DISP/2] = {
  { 0x20, 0x22, 0x24 }, /* Note:  First addr dig2,3, 2nd 5,6, 3rd 1,4 */
  { 0x28, 0x2a, 0x2c }, /* Note:  First addr dig2,3, 2nd 5,6, 3rd 1,4 */
  { 0xa0, 0xa2, 0xa4 }, /* Note:  First addr dig2,3, 2nd 5,6, 3rd 1,4 */
  { 0xa8, 0xaa, 0xac }, /* Note:  First addr dig2,3, 2nd 5,6, 3rd 1,4 */
  { 0x40, 0x42, 0x00 }  /* Note:  First addr dig2,3, 2nd 5,6, last digit invalid */
};

U8                          bitToPlayer[NUM_UPDATE_BITS] = {
  DISPG_PLAYER1, DISPG_PLAYER1, DISPG_PLAYER1,
  DISPG_PLAYER2, DISPG_PLAYER2, DISPG_PLAYER2,
  DISPG_PLAYER3, DISPG_PLAYER3, DISPG_PLAYER3,
  DISPG_PLAYER4, DISPG_PLAYER4, DISPG_PLAYER4,
  DISPG_CREDIT_MATCH, DISPG_CREDIT_MATCH
};

U8                          bitToOffset[NUM_UPDATE_BITS] = {
  0x01, 0x04, 0x00,
  0x01, 0x04, 0x00,
  0x01, 0x04, 0x00,
  0x01, 0x04, 0x00,
  0x01, 0x04
};

U8                          bitToIndex[NUM_UPDATE_BITS] = {
  0x00, 0x01, 0x02,
  0x00, 0x01, 0x02,
  0x00, 0x01, 0x02,
  0x00, 0x01, 0x02,
  0x00, 0x01
};

/* Prototypes */
void i2cproc_i2c_xfer_done(
  U16                       cbParam,
  STDLI_I2C_RESP_E          status);
void i2cproc_set_digit(
  U8                        ledNum,
  U16                       color);

/*
 * ===============================================================================
 * 
 * Name: i2cproc_init_i2c
 * 
 * ===============================================================================
 */
/**
 * Initialize i2c driver
 * 
 * Initialize i2c driver for master mode.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    Mux is initialized in the digital module
 * 
 * ===============================================================================
 */
void i2cproc_init_i2c(void) 
{
#define INIT_VALID_PLYR     0x1f

  i2c_glob.i2cMsg.i2cDone_fp = i2cproc_i2c_xfer_done;
  i2c_glob.i2cMsg.cbParm = 0;
  i2c_glob.state = I2C_STATE_IDLE;
  i2c_glob.valPlyr = 0x1f;
  i2c_glob.currPlyr = 0;

  /* Initialize the i2c bus */
  stdli2c_init_i2c(I2C_FREESCALE, 0, NULL);
  
} /* End i2cproc_init_i2c */

/*
 * ===============================================================================
 * 
 * Name: i2cproc_task
 * 
 * ===============================================================================
 */
/**
 * Task for i2c processing
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void i2cproc_task(void)
{
  U16                       tmpU16;
  U8                        updIndex;
  U8                        player;
  U8                        offset;
  U8                        index;
  STDLI_ERR_E               error;
  
#define WRITE_PORT          0x02
#define CFG_PORT            0x06
  
  /* Check if i2c bus is idle */
  if (i2c_glob.state == I2C_STATE_IDLE)
  {
    /* Check if any of the update display bits are set */
    if (dispg_glob.updDispBits)
    {
      /* Find the display bit that is set */
      tmpU16 = dispg_glob.updDispBits;
      for (updIndex = 0; updIndex < NUM_UPDATE_BITS; updIndex++)
      {
        if (tmpU16 & (1 << updIndex))
        {
          break;
        }
      }
      if (updIndex < NUM_UPDATE_BITS)
      {
        /* Clear the update bit */
        DisableInterrupts;
        dispg_glob.updDispBits &= ~(1 << updIndex);
        EnableInterrupts;
        
        /* Look up the digits that are changing */
        player = bitToPlayer[updIndex];
        
        /* Check if the player is valid */
        if (i2c_glob.valPlyr & (1 << player))
        {
          offset = bitToOffset[updIndex];
          index = bitToIndex[updIndex];
          i2c_glob.i2cMsg.cbParm = player;
          i2c_glob.i2cMsg.addr = i2cAddrLkup[player][index];
          i2c_glob.i2cMsg.data_p = &i2c_glob.txBuf[0];
          i2c_glob.i2cMsg.numDataBytes = 3;
          if (dispg_glob.state != DISP_STATE_CFG)
          {
            i2c_glob.txBuf[0] = WRITE_PORT;
            
            /* Fill out the txBuf */
            if (offset != 0x00)
            {
              i2c_glob.txBuf[1] = charLkup[dispg_glob.curDisp[player][offset]];
              i2c_glob.txBuf[2] = charLkup[dispg_glob.curDisp[player][offset + 1]];
            }
            else
            {
              /* Updating chars 1 and 4 */
              i2c_glob.txBuf[1] = charLkup[dispg_glob.curDisp[player][0]];
              i2c_glob.txBuf[2] = charLkup[dispg_glob.curDisp[player][3]];
            }
          }
          else
          {
            /* Configure the port as all outputs */
            i2c_glob.txBuf[0] = CFG_PORT;
            i2c_glob.txBuf[1] = 0x00;
            i2c_glob.txBuf[2] = 0x00;
            if (dispg_glob.updDispBits == 0)
            {
              dispg_glob.state = DISP_STATE_INIT;
              dispg_glob.updDispBits = UPD_ALL_MASK;
            }
          }
          
          /* Call the stdlib to send the msg */
          error = stdli2c_send_i2c_msg(&i2c_glob.i2cMsg);
          if (error)
          {
            /* HRS:  Should deal with errors */
            error++;
          }
        }
      }
    }
  }
} /* End i2cproc_task */

/*
 * ===============================================================================
 * 
 * Name: i2cproc_i2c_xfer_done
 * 
 * ===============================================================================
 */
/**
 * I2c transfer done callback function
 * 
 * Called when an i2c transfer is complete.  If an error occurs, STDLI_I2C_NO_RESP
 * is returned as the status parameter.
 * 
 * @param   cbParam     [in]    callback parameter
 * @param   status      [in]    status of xfer, either OK, or no response
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void i2cproc_i2c_xfer_done(
  U16                       cbParam,
  STDLI_I2C_RESP_E          status)
{
  if (status != STDLI_I2C_XFER_OK)
  {
    /* Failed i2c transfer, stop sending updates to player score */
    i2c_glob.valPlyr &= ~((1 << (U8)cbParam));
    
    /* Mark failed boards in the match/display */
    if (cbParam == 0)
    {
      dispg_glob.curDisp[DISPG_CREDIT_MATCH][1] = CHAR_0;
    }
    else if (cbParam == 1)
    {
      dispg_glob.curDisp[DISPG_CREDIT_MATCH][2] = CHAR_0;
    }
    else if (cbParam == 2)
    {
      dispg_glob.curDisp[DISPG_CREDIT_MATCH][4] = CHAR_0;
    }
    else if (cbParam == 3)
    {
      dispg_glob.curDisp[DISPG_CREDIT_MATCH][5] = CHAR_0;
    }
  }
  i2c_glob.msgStatus = status;
  i2c_glob.state = I2C_STATE_IDLE;
} /* End i2cproc_i2c_xfer_done */

