/*
 *===============================================================================
 *
 *                         OOOOOO
 *                       OOOOOOOOOO
 *      PPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP    OOO      OOO    PPP
 *               PPP     OOOOOOOOOO     PPP
 *              PPPPP      OOOOOO      PPPPP
 *
 * @file:   rs232proc.c
 * @author: Hugh Spahr
 * @date:   12/06/2012
 *
 * @note:   Open Pinball Project
 *          Copyright© 2012-2015, Hugh Spahr
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
 * This is the serial port processing for the Gen2 hardware.  It
 * uses the first serial port.
 *
 *===============================================================================
 */
 
#include "stdtypes.h"
#define RS232I_INSTANTIATE
#include "rs232intf.h"
#include "stdlintf.h"
#include "neointf.h"
#include "procdefs.h"         /* for EnableInterrupts macro */
#include "gen2glob.h"

#define STDL_FILE_ID          2

#define TX_BUF_SIZE           0x10
#define RX_BUF_SIZE           0x04
#define MAX_RCV_CMD_LEN       0x34     /* Must include space for CRC8 */

typedef enum
{
   RS232_WAIT_FOR_CARD_ID     = 0x00,
   RS232_WAIT_FOR_CMD         = 0x01,
   RS232_PASSTHRU_CMD         = 0x02,
   RS232_STRIP_CMD            = 0x03,
   RS232_RCV_DATA_CMD         = 0x04,  /* Also strips the data */
   RS232_INVENTORY_CMD        = 0x05,  /* Special case since unknown length */
   RS232_NEO_COLOR_TBL        = 0x06,  /* Special case goes directly into memory */
} RS232_STATE_E;

typedef struct
{
   RS232_STATE_E              state;
   BOOL                       rcvChar;
   BOOL                       myCmd;
   U8                         myAddr;
   U8                         cmdLen;
   RS232I_CMD_E               currCmd;
   U8                         currIndex;
   U8                         crc8;
   U8                         txBuf[TX_BUF_SIZE];
   U8                         rxBuf[MAX_RCV_CMD_LEN];
   STDLI_SER_INFO_T           serInfo;
} RS232_GLOB_T;

RS232_GLOB_T                  rs232_glob;

/* Prototypes */
void digital_set_init_state();
void rs232proc_rx_ser_char(
  void                        *cbParam_p);
void rs232proc_force_boot_mode(void);
void rs232proc_bswap_copy_dest(
   U32                        *data_p,
   U8                         *dst_p);
void rs232proc_copy_dest(
   U8                         *src_p,
   U8                         *dst_p,
   UINT                       length);
void rs232proc_bswap_data_buf(
   U32                        *data_p,
   UINT                       numBytes);
void incand_proc_cmd(
   U8                         cmd,
   U32                        mask);

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
   rs232_glob.serInfo.cbParm_p = 0;
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
 * @note    Verifying the CRC is only necessary for changing configuration
 *    commands.  The CRC will be verified for other commands, but commands are
 *    not ignored if that CRC is bad because the command response is already
 *    being sent.
 * 
 * ===============================================================================
 */
void rs232proc_task(void)
{
   U8                         data;
   U8                         txBuf[7];
   U8                         *src_p;
   U8                         *dest_p;
   UINT                       index;
   U32                        mask;
   U32                        tmpU32;
   U32                        currBit;

#define MAGIC_NUM             0xa5a5a5a5
#define RAM_FIRST_ADDR        0x00000000
#define NEO_CMD_OFFSET        0
#define NEO_COLOR_OFFSET      0
#define NEO_INDEX_OFFSET      1
#define NEO_START_MASK_OFFSET 2
#define NEO_GREEN_OFFSET      1
#define NEO_RED_OFFSET        2
#define NEO_BLUE_OFFSET       3
#define INCAND_CMD_OFFSET     0
#define INCAND_MASK_OFFSET    1
#define CONFIG_NUM_OFFSET     0
#define CONFIG_DATA_OFFSET    1
  
   /* Check if received a char */
   if (rs232_glob.rcvChar)
   {
      rs232_glob.rcvChar = FALSE;
      while (stdlser_get_rcv_data(STDLI_SER_PORT_1, &data))
      {
         switch (rs232_glob.state)
         {
            case RS232_WAIT_FOR_CARD_ID:
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
                  rs232_glob.crc8 = 0xff;
                  stdlser_calc_crc8(&rs232_glob.crc8, 1, &data);
                  rs232_glob.state = RS232_WAIT_FOR_CMD;
                  rs232_glob.myCmd = TRUE;
               }
               else if ((data & CARD_ID_TYPE_MASK) == CARD_ID_GEN2_CARD)
               {
                  /* It is not my cmd but use command to figure out length */
                  rs232_glob.state = RS232_WAIT_FOR_CMD;
                  (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
               }
               else
               {
                  /* Lost synchronization.  Keep looking for a valid card ID */
               }
               break;
            }
            case RS232_WAIT_FOR_CMD:
            {
               rs232_glob.currIndex = 0;
               if (data < RS232I_NUM_CMDS)
               {
                  /* Save the current command and the length */
                  rs232_glob.currCmd = data;
                  rs232_glob.cmdLen = CMD_LEN[data] + 1;
                  if (rs232_glob.myCmd)
                  {
                     stdlser_calc_crc8(&rs232_glob.crc8, 1, &data);
                     txBuf[0] = rs232_glob.myAddr;
                     txBuf[1] = data;
                     
                     switch (data)
                     {
                        case RS232I_GET_SER_NUM:
                        {
                           rs232proc_bswap_copy_dest((U32 *)GEN2G_SER_NUM_ADDR, &txBuf[2]);
                           rs232_glob.state = RS232_STRIP_CMD;
                           txBuf[6] = 0xff;
                           stdlser_calc_crc8(&txBuf[6], 6, &txBuf[0]);
                           (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 7);
                           break;
                        }
                        case RS232I_GET_PROD_ID:
                        case RS232I_GET_GEN2_CFG:
                        {
                           /* Product ID is uniquely identified by wing board cfg */
                           rs232proc_copy_dest(&gen2g_info.nvCfgInfo.wingCfg[0], &txBuf[2], RS232I_NUM_WING);
                           rs232_glob.state = RS232_STRIP_CMD;
                           txBuf[6] = 0xff;
                           stdlser_calc_crc8(&txBuf[6], 6, &txBuf[0]);
                           (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 7);
                           break;
                        }
                        case RS232I_GET_VERS:
                        {
                           /* HRS: Debug 
                           rs232proc_bswap_copy_dest((U32 *)&gen2g_appTbl_p->codeVers, &txBuf[2]); */
                           rs232proc_bswap_copy_dest((U32 *)&appStart.codeVers, &txBuf[2]);
                           rs232_glob.state = RS232_STRIP_CMD;
                           txBuf[6] = 0xff;
                           stdlser_calc_crc8(&txBuf[6], 6, &txBuf[0]);
                           (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 7);
                           break;
                        }
                        case RS232I_SET_SER_NUM:
                        {
                           /* Check if serial number is blank, strip cmd */
                           if (*(U32 *)GEN2G_SER_NUM_ADDR == 0)
                           {
                              rs232_glob.state = RS232_RCV_DATA_CMD;
                           }
                           else
                           {
                              /* Already set, so respond with serial number */
                              rs232_glob.state = RS232_STRIP_CMD;
                              rs232proc_bswap_copy_dest((U32 *)GEN2G_SER_NUM_ADDR, &txBuf[2]);
                              rs232_glob.state = RS232_STRIP_CMD;
                              stdlser_calc_crc8(&txBuf[6], 6, &txBuf[0]);
                              (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 7);
                           }
                           break;
                        }
                        case RS232I_RESET:
                        case RS232I_GO_BOOT:
                        case RS232I_CONFIG_SOL:
                        case RS232I_KICK_SOL:
                        case RS232I_CONFIG_INP:
                        case RS232I_SAVE_CFG:
                        case RS232I_ERASE_CFG:
                        case RS232I_SET_GEN2_CFG:
                        case RS232I_CHNG_NEO_CMD:
                        case RS232I_CHNG_NEO_COLOR:
                        case RS232I_CHNG_NEO_COLOR_TBL:
                        case RS232I_INCAND_CMD:
                        case RS232I_CONFIG_IND_SOL:
                        case RS232I_CONFIG_IND_INP:
                        case RS232I_SET_IND_NEO:
                        {
                           /* Verify CRC to be sure */
                           rs232_glob.state = RS232_RCV_DATA_CMD;
                           break;
                        }
                        case RS232I_READ_GEN2_INP:
                        {
                           DisableInterrupts;
                           tmpU32 = gen2g_info.validSwitch;
                           gen2g_info.validSwitch = 0;
                           EnableInterrupts;
                           rs232proc_bswap_copy_dest(&tmpU32, &txBuf[2]);
                           rs232_glob.state = RS232_STRIP_CMD;
                           txBuf[6] = 0xff;
                           stdlser_calc_crc8(&txBuf[6], 6, &txBuf[0]);
                           (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &txBuf[0], 7);
                           break;
                        }
                        case RS232I_SET_NEO_COLOR_TBL:
                        {
                           rs232_glob.state = RS232_NEO_COLOR_TBL;
                           break;
                        }
                        case RS232I_GEN2_UNUSED:
                        default:
                        {
                           /* Bad command received, send EOM */
                           data = RS232I_EOM;
                           (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
                           rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
                           break;
                        }
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
               break;
            }
            case RS232_PASSTHRU_CMD:
            {
               /* Not my command, or RS232I_SET_SER_NUM and serial number has
                * already been set.
                */
               (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
               rs232_glob.currIndex++;
               if (rs232_glob.currIndex >= rs232_glob.cmdLen)
               {
                  /* Whole command has been passed on, now wait for next cmd */
                  rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
               }
               break;
            }
            case RS232_STRIP_CMD:
            {
               /* The following commands are stripped:  RS232I_GET_SER_NUM,
                * RS232I_GET_PROD_ID, RS232I_GET_GEN2_CFG, RS232I_GET_VERS, and
                * RS232I_READ_GEN2_INP.  Responses are sent when first rcv'd.
                */
               rs232_glob.currIndex++;
               if (rs232_glob.currIndex < rs232_glob.cmdLen)
               {
                  stdlser_calc_crc8(&rs232_glob.crc8, 1, &data);
               }
               else
               {
                  if (data != rs232_glob.crc8)
                  {
                     gen2g_info.crcErr++;
                  }
                  
                  /* Whole command has been passed on, now wait for next cmd */
                  rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
               }
               break;
            }
            case RS232_RCV_DATA_CMD:
            {
               /* Copy the data into the rcv buffer, and calculate CRC */
               rs232_glob.rxBuf[rs232_glob.currIndex++] = data;
               if (rs232_glob.currIndex < rs232_glob.cmdLen)
               {
                  stdlser_calc_crc8(&rs232_glob.crc8, 1, &data);
               }
               else
               {
                  /* Whole command has been received */
                  if (data == rs232_glob.crc8)
                  {
                     /* Do command special processing */
                     switch(rs232_glob.currCmd)
                     {
                        case RS232I_SET_SER_NUM:
                        {
                           rs232proc_bswap_data_buf((U32 *)&rs232_glob.rxBuf[0], sizeof(U32));
                           stdlflash_write(&rs232_glob.rxBuf[0], (U8 *)GEN2G_SER_NUM_ADDR, sizeof(U32));
                           break;
                        }
                        case RS232I_RESET:
                        {
                           ResetProc;
                           break;
                        }
                        case RS232I_GO_BOOT:
                        {
                           /* This command resets the processor */
                           Bootloadable_Load();
                           break;
                        }
                        case RS232I_CONFIG_SOL:
                        {
                           for (index = 0, src_p = &rs232_glob.rxBuf[0],
                              dest_p = (U8 *)gen2g_info.solDrvCfg_p;
                              index < sizeof(GEN2G_SOL_DRV_CFG_T);
                              index++)
                           {
                              *dest_p++ = *src_p++;
                           }
                           digital_set_init_state();
                           break;
                        }
                        case RS232I_KICK_SOL:
                        {
                           DisableInterrupts;
                           gen2g_info.solDrvProcCtl = (gen2g_info.solDrvProcCtl & 
                              ~(((U16)rs232_glob.rxBuf[2] << 8) | (U16)rs232_glob.rxBuf[3])) |
                              (((U16)rs232_glob.rxBuf[0] << 8) | (U16)rs232_glob.rxBuf[1]);
                           EnableInterrupts;
                           break;
                        }
                        case RS232I_CONFIG_INP:
                        {
                           for (index = 0, src_p = &rs232_glob.rxBuf[0],
                              dest_p = (U8 *)gen2g_info.inpCfg_p;
                              index < sizeof(GEN2G_INP_CFG_T);
                              index++)
                           {
                              *dest_p++ = *src_p++;
                           }
                           digital_set_init_state();
                           break;
                        }
                        case RS232I_SAVE_CFG:
                        {
                           /* Calculate the CRC */
                           gen2g_info.nvCfgInfo.nvCfgCrc = 0xff;
                           stdlser_calc_crc8(&gen2g_info.nvCfgInfo.nvCfgCrc, 0xfc,
                              &gen2g_info.nvCfgInfo.wingCfg[0]);
                           
                           stdlflash_write((U8 *)&gen2g_info.nvCfgInfo,
                              (U8 *)GEN2G_CFG_TBL, GEN2G_FLASH_SECT_SZ);
                           stdlflash_write(((U8 *)&gen2g_info.nvCfgInfo) + GEN2G_FLASH_SECT_SZ,
                              ((U8 *)GEN2G_CFG_TBL) + GEN2G_FLASH_SECT_SZ, GEN2G_FLASH_SECT_SZ);
                           gen2g_info.validCfg = TRUE;
                           break;
                        }
                        case RS232I_ERASE_CFG:
                        {
                           gen2g_info.validCfg = FALSE;
                           gen2g_info.freeCfg_p = &gen2g_info.nvCfgInfo.cfgData[0];
                           gen2g_info.typeWingBrds = 0;
                           gen2g_info.inpCfg_p = NULL;
                           gen2g_info.neoCfg_p = NULL;
                           for (index = 0, dest_p = &gen2g_info.nvCfgInfo.cfgData[0];
                              index < sizeof(gen2g_info.nvCfgInfo.cfgData);
                              index++)
                           {
                              *dest_p++ = 0;
                           }
                           stdlflash_sector_erase((U8 *)GEN2G_CFG_TBL);
                           stdlflash_sector_erase((U8 *)(GEN2G_CFG_TBL + GEN2G_FLASH_SECT_SZ));
                           break;
                        }
                        case RS232I_SET_GEN2_CFG:
                        {
                           for (index = 0; index < RS232I_NUM_WING; index++)
                           {
                              gen2g_info.nvCfgInfo.wingCfg[index] = rs232_glob.rxBuf[index];
                              if (gen2g_info.nvCfgInfo.wingCfg[index] != WING_UNUSED)
                              {
                                 gen2g_info.typeWingBrds |= (1 << gen2g_info.nvCfgInfo.wingCfg[index]);
                              }
                           }
                           
                           /* Walk through types and call init functions using jump table, sets up config ptrs */
                           for (index = WING_UNUSED + 1; index < MAX_WING_TYPES; index++)
                           {
                              if (((gen2g_info.typeWingBrds & (1 << index)) != 0) &&
                                 (GEN2G_INIT_FP[index] != NULL))
                              {
                                 GEN2G_INIT_FP[index]();
                              }
                           }
                           break;
                        }
                        case RS232I_CHNG_NEO_CMD:
                        {
                           /* tmpU32 starting index of pixels to change */
                           tmpU32 = (U32)rs232_glob.rxBuf[NEO_INDEX_OFFSET];
                           mask = (U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET + 3] |
                              ((U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET + 2] << 8) |
                              ((U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET + 1] << 16) |
                              ((U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET] << 24);
                           for (index = 0, currBit = 1; index < 32; index++, currBit <<= 1)
                           {
                              if ((currBit & mask) != 0)
                              {
                                 neo_update_pixel_cmd(index + tmpU32, (INT)rs232_glob.rxBuf[NEO_CMD_OFFSET]);
                              }
                           }
                           break;
                        }
                        case RS232I_CHNG_NEO_COLOR:
                        {
                           /* tmpU32 starting index of pixels to change */
                           tmpU32 = (U32)rs232_glob.rxBuf[NEO_INDEX_OFFSET];
                           mask = (U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET + 3] |
                              ((U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET + 2] << 8) |
                              ((U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET + 1] << 16) |
                              ((U32)rs232_glob.rxBuf[NEO_START_MASK_OFFSET] << 24);
                           for (index = 0, currBit = 1; index < 32; index++, currBit <<= 1)
                           {
                              if ((currBit & mask) != 0)
                              {
                                 neo_update_pixel_color(index + tmpU32, (INT)rs232_glob.rxBuf[NEO_COLOR_OFFSET]);
                              }
                           }
                           break;
                        }
                        case RS232I_CHNG_NEO_COLOR_TBL:
                        {
                           /* tmpU32 is the new color table color */
                           tmpU32 = ((U32)rs232_glob.rxBuf[NEO_GREEN_OFFSET] << 16) |
                              ((U32)rs232_glob.rxBuf[NEO_RED_OFFSET] << 8) |
                              (U32)rs232_glob.rxBuf[NEO_BLUE_OFFSET];
                           neo_update_color_tbl((INT)rs232_glob.rxBuf[NEO_CMD_OFFSET], tmpU32);
                           break;
                        }
                        case RS232I_INCAND_CMD:
                        {
                           mask = ((U32)rs232_glob.rxBuf[INCAND_MASK_OFFSET] << 24) |
                              ((U32)rs232_glob.rxBuf[INCAND_MASK_OFFSET + 1] << 16) |
                              ((U32)rs232_glob.rxBuf[INCAND_MASK_OFFSET + 2] << 8) |
                              (U32)rs232_glob.rxBuf[INCAND_MASK_OFFSET + 3];
                           incand_proc_cmd(rs232_glob.rxBuf[INCAND_CMD_OFFSET], mask);
                           break;
                        }
                        case RS232I_CONFIG_IND_SOL:
                        {
                           /* First byte contains solenoid number [0-15] */
                           for (index = 0, src_p = &rs232_glob.rxBuf[CONFIG_DATA_OFFSET],
                              dest_p = ((U8 *)gen2g_info.solDrvCfg_p) +
                                 (rs232_glob.rxBuf[CONFIG_NUM_OFFSET] * sizeof(RS232I_SOL_CFG_T));
                              index < sizeof(RS232I_SOL_CFG_T);
                              index++)
                           {
                              *dest_p++ = *src_p++;
                           }
                           digital_set_init_state();
                           break;
                        }
                        case RS232I_CONFIG_IND_INP:
                        {
                           gen2g_info.inpCfg_p->inpCfg[rs232_glob.rxBuf[CONFIG_NUM_OFFSET]] =
                              rs232_glob.rxBuf[CONFIG_DATA_OFFSET];
                           digital_set_init_state();
                           break;
                        }
                        case RS232I_SET_IND_NEO:
                        {
                           neo_update_pixel_cmd(rs232_glob.rxBuf[CONFIG_NUM_OFFSET],
                              (INT)rs232_glob.rxBuf[CONFIG_DATA_OFFSET]);
                           neo_update_pixel_color(rs232_glob.rxBuf[CONFIG_NUM_OFFSET],
                              (INT)rs232_glob.rxBuf[CONFIG_DATA_OFFSET]);
                           break;
                        }
                        default:
                        {
                           /* Invalid cmd for RS232_RCV_DATA_CMD, send EOM */
                           data = RS232I_EOM;
                           (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
                           rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
                           break;
                        }
                     }
                  }
                  else
                  {
                     gen2g_info.crcErr++;
                  }
                  
                  /* Whole command has been received */
                  rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
               }
               break;
            }
            case RS232_INVENTORY_CMD:
            {
               if (data == RS232I_EOM)
               {
                  /* Rcv'd EOM, so my addr is next addr */
                  if (rs232_glob.myAddr == MAX_U8)
                  {
                     rs232_glob.myAddr = CARD_ID_GEN2_CARD;
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
               else if ((data & CARD_ID_TYPE_MASK) == CARD_ID_GEN2_CARD)
               {
                  rs232_glob.myAddr = data;
                  (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
               }
               else
               {
                  /* Not my card type and make no assumptions, pass thru */
                  (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
               }
               break;
            }
            case RS232_NEO_COLOR_TBL:
            {
               /* Copy the data into the rcv buffer, and calculate CRC */
               index = rs232_glob.currIndex % 3;
               rs232_glob.rxBuf[index] = data;
               if (index == 2)
               {
                  /* New color table entry completed */
                  tmpU32 = ((U32)rs232_glob.rxBuf[0] << 16) |
                     ((U32)rs232_glob.rxBuf[1] << 8) |
                     (U32)rs232_glob.rxBuf[2];
                  index = rs232_glob.currIndex / 3;
                  neo_update_color_tbl(index, tmpU32);
               }
               rs232_glob.currIndex++;
               if (rs232_glob.currIndex < rs232_glob.cmdLen)
               {
                  stdlser_calc_crc8(&rs232_glob.crc8, 1, &data);
               }
               else
               {
                  /* rcvBuf[0] contains the number of Neopixels */
                  gen2g_info.nvCfgInfo.numNeoPxls = rs232_glob.rxBuf[0];
                  
                  /* Whole command has been received */
                  if (data != rs232_glob.crc8)
                  {
                     gen2g_info.crcErr++;
                  }
                  
                  /* Whole command has been passed on, now wait for next cmd */
                  rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
               }
               break;
            }
            default:
            {
               /* Invalid state, send EOM */
               data = RS232I_EOM;
               (void)stdlser_xmt_data(STDLI_SER_PORT_1, FALSE, &data, 1);
               rs232_glob.state = RS232_WAIT_FOR_CARD_ID;
               break;
            }
         }
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
   void                        *cbParam_p)
{
   cbParam_p = 0;
  
   rs232_glob.rcvChar = TRUE;
} /* End rs232proc_rx_ser_char */

/*
 * ===============================================================================
 * 
 * Name: rs232proc_bswap_copy_dest
 * 
 * ===============================================================================
 */
/**
 * Byte swap 32 bit data and copy to destination
 * 
 * This converts from little endian to big endian for destination byte stream.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void rs232proc_bswap_copy_dest(
   U32                        *data_p,
   U8                         *dst_p)
{
   U32                        data;
   U8                         *src_p;
   UINT                       index;
   
   data = *data_p;
   data = ((data >> 24) & 0xff) | ((data << 8) & 0xff0000) |
      ((data >> 8) & 0xff00) | ((data << 24) & 0xff000000);
   for (src_p = (U8 *)&data, index = 0; index < sizeof(U32); index++)
   {
      *dst_p++ = *src_p++;
   }
} /* End rs232proc_bswap_copy_dest */

/*
 * ===============================================================================
 * 
 * Name: rs232proc_copy_dest
 * 
 * ===============================================================================
 */
/**
 * Byte copy to destination
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void rs232proc_copy_dest(
   U8                         *src_p,
   U8                         *dst_p,
   UINT                       length)
{
   UINT                       index;
   
   for (index = 0; index < length; index++)
   {
      *dst_p++ = *src_p++;
   }
} /* End rs232proc_copy_dest */


/*
 * ===============================================================================
 * 
 * Name: rs232proc_bswap_data_buf
 * 
 * ===============================================================================
 */
/**
 * Byte swap received data buffer to move from little endian to big endian
 * 
 * This converts from received bytes stream from little endian to big endian.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void rs232proc_bswap_data_buf(
   U32                        *data_p,
   UINT                       numBytes)
{
   U32                        data;
   UINT                       index;
   
   for (index = 0; index < numBytes; index += sizeof(U32))
   {
      data = *data_p;
      *data_p++ = ((data >> 24) & 0xff) | ((data << 8) & 0xff0000) |
         ((data >> 8) & 0xff00) | ((data << 24) & 0xff000000);
   }
} /* End rs232proc_bswap_data_buf */

/* [] END OF FILE */
