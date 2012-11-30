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
 * @file:   stdldigio.c
 * @author: Hugh Spahr
 * @date:   6/12/2008
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
 * This is the digital i/o utility file in the Standard Library.
 *  It contains a function to configure, read and write the digital i/o ports.
 *
 *===============================================================================
 */
#include "stdtypes.h"   /* include peripheral declarations */
#include <hidef.h>      /* for EnableInterrupts macro */
#include "derivative.h" /* include peripheral declarations */
#include "stdlintf.h"

#define PTAD_ADDR           0x00    /* Address of first port (port A) */
#define LOW_REG_OFFSET      0x02    /* Offset btwn low mem reg btwn ports */
#define PTXDD_OFFSET        0x01    /* Offset btwn low reg ptr and data dir */
#define PTAPE_ADDR          0x1840  /* Address of first port (port A) */
#define SMALL_HI_REG_OFFSET 0x04    /* Offset btwn hi mem reg btwn ports */
#define BIG_HI_REG_OFFSET   0x08    /* Offset btwn hi mem reg btwn ports */
#define PTXDS_OFFSET        0x02    /* Offset btwn hi reg ptr and drive str */

/*
 * ===============================================================================
 * 
 * Name: stdldigio_config_dig_port
 * 
 * ===============================================================================
 */
/**
 * Configure digital port
 * 
 * Configure the digital port by setting up direction, pullups if it is an input,
 * or drive strength if it is an output.
 * 
 * @param   portInfo    [in]    port, input/output, drive, and pullup 
 * @param   mask        [in]    mask of bits to change 
 * @param   data        [in]    data for output bits 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdldigio_config_dig_port(
  STDLI_DIG_PORT_INFO_E     portInfo,     /* port, input/output, drive, and pullup */
  U8                        mask,         /* mask of data bits to change */
  U8                        data)         /* data if output bits, unused if input */
{
  U8                        port;
  U8                        *lowReg_p;
  U8                        *hiReg_p;
  
  port = portInfo & STDLI_DIG_PORT_MASK;
  lowReg_p = (U8 *)(PTAD_ADDR + (port * LOW_REG_OFFSET));
  if (portInfo & STDLI_DIG_SMALL_MODEL)
  {
    hiReg_p = (U8 *)(PTAPE_ADDR + (port * SMALL_HI_REG_OFFSET));
  }
  else
  {
    hiReg_p = (U8 *)(PTAPE_ADDR + (port * BIG_HI_REG_OFFSET));
  }
  
  /* check the direction of the digital bits */
  if (portInfo & STDLI_DIG_OUT)
  {
    /* This is an output, write the data, drive strength, and direction */
    *lowReg_p = (*lowReg_p & ~mask) | (data & mask);
    if (portInfo & STDLI_DIG_HI_DRIVE)
    {
      *(hiReg_p + PTXDS_OFFSET) |= mask;
    }
    else
    {
      *(hiReg_p + PTXDS_OFFSET) &= ~mask;
    }
    *(lowReg_p + PTXDD_OFFSET) |= mask;
  }
  else
  {
    /* This is an input, write pullup, and direction */
    if (portInfo & STDLI_DIG_PULLUP)
    {
      *hiReg_p |= mask;
    }
    else
    {
      *hiReg_p &= ~mask;
    }
    *(lowReg_p + PTXDD_OFFSET) &= ~mask;
  }
} /* End stdldigio_config_dig_port */

/*
 * ===============================================================================
 * 
 * Name: stdldigio_read_port
 * 
 * ===============================================================================
 */
/**
 * Read digital port
 * 
 * Use a mask to read and return the digital port data.
 * 
 * @param   port        [in]    port such as STDLI_DIG_PORT_A  
 * @param   mask        [in]    mask of bits to change 
 * @return  data                data read
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
U8 stdldigio_read_port(
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        mask)         /* mask of data bits to read */
{
  return((*(U8 *)(PTAD_ADDR + ((port) * LOW_REG_OFFSET))) & mask);
} /* End stdldigio_read_port */

/*
 * ===============================================================================
 * 
 * Name: stdldigio_write_port
 * 
 * ===============================================================================
 */
/**
 * Write digital port
 * 
 * Write to a digital port using a bit mask.
 * 
 * @param   port        [in]    port such as STDLI_DIG_PORT_A  
 * @param   mask        [in]    mask of bits to change 
 * @param   data        [in]    data to be written 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void stdldigio_write_port(
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        mask,         /* mask of data bits to write */
  U8                        data)         /* data to write */
{
  U8                        *lowReg_p;
  
  lowReg_p = (U8 *)(PTAD_ADDR + (port * LOW_REG_OFFSET));
  
  *lowReg_p = (*lowReg_p & ~mask) | (data  & mask);
} /* End stdldigio_write_port */
