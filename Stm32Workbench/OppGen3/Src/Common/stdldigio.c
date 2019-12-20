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
 * @date:   9/17/2015
 *
 * @note:    Copyright© 2015, Hugh Spahr
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
#include "stdlintf.h"

#define GPIO_PRTA_BASE      0x40010800
#define GPIO_PRTB_BASE      0x40010c00
#define GPIO_PRTC_BASE      0x40011000
#define GPIO_PRTA_IDR_BASE  0x40010808
#define GPIO_PRTA_ODR_BASE  0x4001080c
#define GPIO_REG_OFFSET     0x00000400


#define CRL_OFFSET          0
#define CRH_OFFSET          1
#define ODR_OFFSET          3
#define BSRR_OFFSET         4

/*
 * ===============================================================================
 * 
 * Name: stdldigio_read_all_ports
 *
 * ===============================================================================
 */
/**
 * Read all digital ports
 *
 * Use a mask to read and return the digital port data.
 *
 * @param   mask        [in]    mask of bits to read
 * @return  data                data read
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
U32 stdldigio_read_all_ports(
   U32                        mask)         /* mask of data bits to read */
{
   U32                        portAData;
   U32                        portBData;
   U32                        portCData;

   portAData = stdldigio_read_port(STDLI_DIG_PORT_A, 0x0000ffff);
   portBData = stdldigio_read_port(STDLI_DIG_PORT_B, 0x0000ffff);
   portCData = stdldigio_read_port(STDLI_DIG_PORT_C, 0x0000ffff);

   return ((((portAData >> 13) & 0x00000001) |
      ((portBData >> 11) & 0x0000001e) |
	  ((portAData >> 3) & 0x000000e0) |
	  ((portAData >> 7) & 0x00000100) |
	  ((portBData << 6) & 0x0000fe00) |
	  ((portAData << 2) & 0x00010000) |
	  ((portCData << 4) & 0x000e0000) |
	  ((portAData << 20) & 0x0ff00000) |
	  ((portBData << 28) & 0x30000000) |
	  ((portBData << 20) & 0xc0000000)) & mask);
} /* End stdldigio_read_all_ports */

/*
 * ===============================================================================
 *
 * Name: stdldigio_write_all_ports
 *
 * ===============================================================================
 */
/**
 * Write all digital ports
 *
 * Use a mask to write digital port data.
 *
 * @param   data        [in]    data bits to write
 * @param   mask        [in]    mask of bits to write
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void stdldigio_write_all_ports(
   U32                        data,         /* data bits to write */
   U32                        mask)         /* mask of bits to write */
{
   U32                        setBits;
   U32                        clrBits;
   U32                        portABsrr;
   U32                        portBBsrr;
   U32                        portCBsrr;

   setBits = data & mask;
   clrBits = data ^ mask;

   portABsrr = ((setBits & 0x00000001) << 13) |
      ((setBits & 0x000000e0) << 3) |
	  ((setBits & 0x00000100) << 7) |
	  ((setBits & 0x00010000) >> 2) |
	  ((setBits & 0x0ff00000) >> 20) |
	  ((clrBits & 0x00000001) << 29) |
      ((clrBits & 0x000000e0) << 19) |
	  ((clrBits & 0x00000100) << 23) |
	  ((clrBits & 0x00010000) >> 14) |
	  ((clrBits & 0x0ff00000) >> 4);
   portBBsrr = ((setBits & 0x0000001e) << 11) |
      ((setBits & 0x0000fe00) >> 6) |
	  ((setBits & 0x30000000) >> 28) |
	  ((setBits & 0xc0000000) >> 20) |
	  ((clrBits & 0x0000001e) << 27) |
      ((clrBits & 0x0000fe00) << 10) |
	  ((clrBits & 0x30000000) >> 12) |
	  ((clrBits & 0xc0000000) >> 4);
   portCBsrr = ((setBits & 0x000e0000) >> 4) |
      ((clrBits & 0x000e0000) << 12);

   ((R32 *)GPIO_PRTA_BASE)[BSRR_OFFSET] = portABsrr;
   ((R32 *)GPIO_PRTB_BASE)[BSRR_OFFSET] = portBBsrr;
   ((R32 *)GPIO_PRTC_BASE)[BSRR_OFFSET] = portCBsrr;
} /* End stdldigio_write_all_ports */

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
 * @param   portInfo    [in]    port, input/output, pullup/pulldown, etc
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
   STDLI_DIG_PORT_INFO_E      portInfo,     /* port, input/output, drive, and pullup */
   U32                        mask,         /* mask of data bits to change */
   U32                        data)         /* data if output bits, unused if input */
{
#define HIGH_IMP              0x00
#define INPUT_PIN             0x08
#define RES_PUP               0x01
#define RES_PDN               0x03
#define OPEN_DRAIN_DRV_LOW    0x06
#define OUTPUT_PIN            0x02

   INT                        port;
   R32                        *gpioReg_p;
   INT                        index;
   U32                        pinCfg = 0;
   U32                        cfgLo = 0;
   U32                        cfgLoMsk = 0;
   U32                        cfgHi = 0;
   U32                        cfgHiMsk = 0;
   U32                        odrCfg = 0;
   U32                        odrCfgMsk = 0;

   port = portInfo & STDLI_DIG_PORT_MASK;
   gpioReg_p = (R32 *)(GPIO_PRTA_BASE + (port * GPIO_REG_OFFSET));

   /* check the direction of the digital bits */
   if (portInfo & STDLI_DIG_OUT)
   {
      if (portInfo & STDLI_DIG_OC_PULLDWN)
      {
         pinCfg = OPEN_DRAIN_DRV_LOW;
      }
      else
      {
         pinCfg = OUTPUT_PIN;
      }
   }
   else
   {
      if (portInfo & STDLI_DIG_PULLUP)
      {
         /* Set DR to turn on pullup */
         pinCfg = INPUT_PIN;
         odrCfg = RES_PUP;
      }
      else if (portInfo & STDLI_DIG_PULLDWN)
      {
         /* Set DR to turn on pulldown */
         pinCfg = INPUT_PIN;
         odrCfg = RES_PDN;
      }
      else
      {
         pinCfg = HIGH_IMP;
      }
   }

   /* Calculate the complete config for the port routing */

   // Create cfg bits and mask
   for (index = 0; index < 8; index++)
   {
      if (mask & (1 << index))
      {
         cfgLo |= (pinCfg << (index * 4));
         cfgLoMsk |= (0x0f << (index * 4));
         odrCfgMsk |= (1 << index);
         odrCfg |= (odrCfg << index);
      }
      if (mask & (1 << (index + 8)))
      {
          cfgHi |= (pinCfg << (index * 4));
          cfgHiMsk |= (0x0f << (index * 4));
          odrCfgMsk |= (1 << (index + 8));
          odrCfg |= (odrCfg << (index + 8));
      }
   }

   /* Set the pin configuration */
   gpioReg_p[CRL_OFFSET] &= ~cfgLoMsk;
   gpioReg_p[CRL_OFFSET] |= cfgLo;
   gpioReg_p[CRH_OFFSET] &= ~cfgHiMsk;
   gpioReg_p[CRH_OFFSET] |= cfgHi;
   gpioReg_p[ODR_OFFSET] &= ~odrCfgMsk;
   gpioReg_p[ODR_OFFSET] |= odrCfg;

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
 * @param   mask        [in]    mask of bits to read
 * @return  data                data read
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
U32 stdldigio_read_port(
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_A */
   U32                        mask)         /* mask of data bits to read */
{
   return ((*(R32 *)(GPIO_PRTA_IDR_BASE + ((port) * GPIO_REG_OFFSET))) & mask);
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
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_A */
   U32                        mask,         /* mask of data bits to write */
   U32                        data)         /* data to write */
{
   R32                        *reg_p;
  
   reg_p = (R32 *)(GPIO_PRTA_ODR_BASE + (port * GPIO_REG_OFFSET));
  
   *reg_p = (*reg_p & ~mask) | (data  & mask);
} /* End stdldigio_write_port */

/* [] END OF FILE */
