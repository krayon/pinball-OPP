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
#include "dispglob.h"
#include "stdlintf.h"
#include "derivative.h" /* include for petting the watchdog */

#define STDL_FILE_ID        2

#define MAX_SEND_SIZE       2
#define MAX_RCV_SIZE        2

typedef enum
{
  I2CPROC_I2C_IDLE          = 0x00,
  I2CPROC_I2C_BUSY          = 0x01,
} I2CPROC_I2C_E;

typedef enum
{
  I2C_STATE_IDLE            = 0x00,
  I2C_STATE_SEND            = 0x01,
} I2C_STATE_E;
/* Warning: State machine.  It uses increment to move to next state */

typedef struct
{
  I2C_STATE_E               state;
  U8                        txBuf[MAX_SEND_SIZE];
  U8                        rxBuf[MAX_RCV_SIZE];
  volatile I2CPROC_I2C_E    i2cState;
  STDLI_I2C_RESP_E          msgStatus;
  STDLI_I2C_XFER_T          i2cMsg;
  STDLI_TIMER_EVENT_T       timeEvt;
} I2C_GLOB_T;

I2C_GLOB_T                  i2c_glob;

U8                          charLkup[MAX_CHAR_ID] = {
  0x3f /* 0 */, 0x06 /* 1 */, 0x6b /* 2 */, 0x4f /* 3 */, 0x66 /* 4 */,
  0x1b /* 5 */, 0x7d /* 6 */, 0x07 /* 7 */, 0x7f /* 8 */, 0x67 /* 9 */,
  0x73 /* P */, 0x79 /* E */, 0x37 /* N */, 0x38 /* L */, 0x77 /* A */,
  0x1e /* J */, 0x39 /* C */, 0x00 /* blank */ };

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
  STDLI_ERR_E               error;
  
  i2c_glob.i2cState = I2CPROC_I2C_IDLE;
  i2c_glob.i2cMsg.i2cDone_fp = i2cproc_i2c_xfer_done;
  i2c_glob.i2cMsg.cbParm = 0;
  i2c_glob.state = I2C_STATE_IDLE;

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
} /* End i2cproc_i2c_xfer_done */

