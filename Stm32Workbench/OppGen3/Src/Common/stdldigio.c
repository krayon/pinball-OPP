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
	  ((clrBits & 0x00010000) << 14) |
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

/* [] END OF FILE */
