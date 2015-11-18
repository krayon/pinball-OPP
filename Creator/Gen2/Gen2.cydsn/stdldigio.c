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

#define GPIO_PRT0_BASE      0x40040000
#define GPIO_PRT0_PS_BASE   0x40040004
#define GPIO_REG_OFFSET     0x00000100
#define HSIO_PORT_SEL_BASE  0x40010000
#define HSIO_REG_OFFSET     0x00000004

#define DR_OFFSET           0
#define PC_OFFSET           2
#define INT_CFG_OFFSET      3
#define PC2_OFFSET          5

#define GPIO_PRT0_DR        0x40040000
#define GPIO_PRT0_PS        0x40040004
#define GPIO_PRT0_PC        0x40040008
#define GPIO_PRT0_INTR_CFG  0x4004000c
#define GPIO_PRT0_INTR      0x40040010
#define GPIO_PRT0_PC2       0x40040014
#define HSIOM_PORT_SEL0     0x40010000

#define GPIO_PRT1_DR        0x40040100

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
   U8                         mask,         /* mask of data bits to change */
   U8                         data)         /* data if output bits, unused if input */
{
#define HIGH_IMP              0x01
#define RES_PUP               0x02
#define RES_PDN               0x03
#define OPEN_DRAIN_DRV_LOW    0x04
#define STRONG_DRV            0x06
    
   U8                         port;
   R32                        *gpioReg_p;
   R32                        *hsioReg_p;
   INT                        pinCfg;
   INT                        index;
   U32                        portCfg;
   U32                        portCfgMsk;
   U32                        hsioMsk;
   U32                        intCfgMsk;

   port = portInfo & STDLI_DIG_PORT_MASK;
   gpioReg_p = (R32 *)(GPIO_PRT0_BASE + (port * GPIO_REG_OFFSET));
   hsioReg_p = (R32 *)(HSIO_PORT_SEL_BASE + (port * HSIO_REG_OFFSET));
    
   /* check the direction of the digital bits */
   if (portInfo & STDLI_DIG_OUT)
   {
      /* This is an output, write the data, figure out cfg */
      gpioReg_p[DR_OFFSET] = (gpioReg_p[DR_OFFSET] & ~mask) | (data & mask);
        
      if (portInfo & STDLI_DIG_OC_PULLDWN)
      {
         pinCfg = OPEN_DRAIN_DRV_LOW;
      }
      else
      {
         pinCfg = STRONG_DRV;
      }
   }
   else
   {
      if (portInfo & STDLI_DIG_PULLUP)
      {
         /* Set DR to turn on pullup */
         pinCfg = RES_PUP;
         gpioReg_p[DR_OFFSET] |= mask;
      }
      else if (portInfo & STDLI_DIG_PULLDWN)
      {
         /* Set DR to turn on pulldown */
         pinCfg = RES_PDN;
         gpioReg_p[DR_OFFSET] &= ~mask;
      }
      else
      {
         pinCfg = HIGH_IMP;
      }
   }
    
   /* Calculate the complete config for the port and GPIO routing */
   portCfg = 0;
   portCfgMsk = 0;
   hsioMsk = 0;
   intCfgMsk = 0;
   for (index = 0; index < 8; index++)
   {
      if (mask & (1 << index))
      {
         portCfg |= (pinCfg << (index * 3));
         portCfgMsk |= (0x07 << (index * 3));
         hsioMsk |= (0x0f << (index * 4));
         intCfgMsk |= (0x03 << (index * 2));
      }
   }
    
   /* Set the pin configuration, turn off pin interrupts, and disable
    * analog pin drivers.
    */
   gpioReg_p[PC_OFFSET] &= ~portCfgMsk;
   gpioReg_p[PC_OFFSET] |= portCfg;
   gpioReg_p[INT_CFG_OFFSET] &= ~intCfgMsk;
   gpioReg_p[PC2_OFFSET] &= ~mask;

   /* Send the GPIO bit to the hardware pin */
   *hsioReg_p &= ~hsioMsk;
    
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
 * @param   port        [in]    port such as STDLI_DIG_PORT_0  
 * @param   mask        [in]    mask of bits to read
 * @return  data                data read
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
U8 stdldigio_read_port(
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_0 */
   U8                         mask)         /* mask of data bits to read */
{
   return((U8)(*(R32 *)(GPIO_PRT0_PS_BASE + ((port) * GPIO_REG_OFFSET))) & mask);
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
 * @param   port        [in]    port such as STDLI_DIG_PORT_1 
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
   STDLI_DIG_PORT_INFO_E      port,         /* data port, ex. STDLI_DIG_PORT_1 */
   U8                         mask,         /* mask of data bits to write */
   U8                         data)         /* data to write */
{
   R32                        *reg_p;
  
   reg_p = (R32 *)(GPIO_PRT0_BASE + (port * GPIO_REG_OFFSET));
  
   *reg_p = (*reg_p & ~mask) | (data  & mask);
} /* End stdldigio_write_port */

/* [] END OF FILE */
