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
 * @file:   gen2glob.h
 * @author: Hugh Spahr
 * @date:   9/16/2015
 *
 * @note:   Open Pinball Project
 *          Copyright© 2015, Hugh Spahr
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
 * Global file for Gen 2 boards.  It contains function
 *  prototypes and structures
 *
 *===============================================================================
 */
#ifndef GEN2GLOB_H
#define GEN2GLOB_H
 
#include "stdtypes.h"
#include "rs232intf.h"
#include "stdlintf.h"

#define GEN2_DEBUG            1

typedef enum
{
   NO_ERRORS                  = 0x00,
   ERR_MALLOC_FAIL            = 0x01,
   
   /* OR'd with STDLI_ERR_E so error codes don't conflict */
   ERR_STDL_ERR_MASK          = 0x80,
} __attribute__((packed)) GEN2G_ERROR_E;
   
#define GEN2G_CFG_TBL         0x00007e80
#define GEN2G_FLASH_SECT_SZ   0x80
#define GEN2G_NV_PARM_SIZE    0xfc
#define GEN2G_NUM_NVCFG       4
#define GEN2G_SER_NUM_ADDR    0x00007ffc
#define GEN2G_APP_TBL_ADDR    0x00007f80

#define GEN2G_STAT_BLINK_SLOW_ON       0x01
#define GEN2G_STAT_FADE_SLOW_DEC       0x01
#define GEN2G_STAT_BLINK_FAST_ON       0x02
#define GEN2G_STAT_FADE_FAST_DEC       0x02
#define GEN2G_MAX_STATE_NUM            32      /* State num goes from 0 - 31 */

typedef enum
{
   NVCFG_UNUSED               = 0x00,
   NVCFG_SOL                  = 0x01,
   NVCFG_INP                  = 0x02,
   NVCFG_COLOR_TBL            = 0x03,
} __attribute__((packed)) GEN2G_NVCFG_TYPE_E;

typedef struct
{
   U8                         green;
   U8                         red;
   U8                         blue;
} GEN2G_NEO_COLOR_TBL_T;
   
/* Non-volatile configuration stored in flash on Gen2 boards.
 * Requires 256 bytes of flash.
 */
typedef struct
{
   U8                         nvCfgCrc;   /* CRC from wingCfg to end of cfgData */
   U8                         res1[3];
   RS232I_GEN2_WING_TYPE_E    wingCfg[RS232I_NUM_WING];
   U8                         numNeoPxls;
   U8                         res2[7];
   U8                         cfgData[0xf0];
} GEN2G_NV_CFG_T;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
   GEN2G_NV_CFG_T *gen2g_nv_cfg_p
#ifdef GEN2G_INSTANTIATE
   = (GEN2G_NV_CFG_T *)GEN2G_CFG_TBL
#endif
;

/* This will be stored at the beginning of the app when the bootloader
 * rewrite is completed.  Currently it is saved in RAM.
 */
typedef struct
{
  U32                   appLen;           /* Length of application */
  U32                   codeVers;         /* Application version */
} APP_START_T;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
   APP_START_T appStart;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
   APP_START_T *gen2g_appTbl_p
#ifdef GEN2G_INSTANTIATE
   = (APP_START_T *)GEN2G_APP_TBL_ADDR
#endif
;

typedef struct
{
   RS232I_SOL_CFG_T           solCfg[RS232I_NUM_GEN2_SOL];
} GEN2G_SOL_DRV_CFG_T;

typedef struct
{
   RS232I_CFG_INP_TYPE_E      inpCfg[RS232I_NUM_GEN2_INP];
} GEN2G_INP_CFG_T;

typedef struct
{
   GEN2G_NEO_COLOR_TBL_T      colorTbl[RS232I_SZ_COLOR_TBL];
} GEN2G_NEO_CFG_T;

typedef struct
{
   RS232I_CFG_INP_TYPE_E      swMatrixCfg[RS232I_SW_MATRX_INP];
} GEN2G_SW_MATRIX_CFG_T;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
const U8                      CFG_SIZE[MAX_WING_TYPES]
#ifdef GEN2G_INSTANTIATE
 ={   0,                            /* WING_UNUSED */
      sizeof(GEN2G_SOL_DRV_CFG_T),  /* WING_SOL */
      sizeof(GEN2G_INP_CFG_T),      /* WING_INP */
      0,                            /* WING_INCAND */
      0,                            /* WING_SW_MATRIX_OUT */
      sizeof(GEN2G_SW_MATRIX_CFG_T),/* WING_SW_MATRIX_IN */
      sizeof(GEN2G_NEO_CFG_T),      /* WING_NEO */
  }
#endif
;

/* Init prototypes */
void digital_init();
void neopxl_init();
void incand_init();

#ifndef GEN2G_INSTANTIATE
   extern
#endif
 void (*GEN2G_INIT_FP[MAX_WING_TYPES])()
#ifdef GEN2G_INSTANTIATE
 ={   NULL,                         /* WING_UNUSED */
      digital_init,                 /* WING_SOL */
      digital_init,                 /* WING_INP */
      incand_init,                  /* WING_INCAND */
      NULL,                         /* WING_SW_MATRIX_OUT */
      NULL,                         /* WING_SW_MATRIX_IN */
      neopxl_init,                  /* WING_NEO */
  }
#endif
;

typedef struct
{
   BOOL                       validCfg;
   GEN2G_ERROR_E              error;
   U16                        solDrvProcCtl;
   U8                         ledStateNum;   /* 0 - 31 counter used to fade/blink LEDs */
   U8                         ledStatus;      /* If blinking LED is on/fading LED is brighter */
   U32                        typeWingBrds;  /* Bit mask of types of populated wing boards */
   U32                        validSwitch;
   U32                        crcErr;
   GEN2G_NV_CFG_T             nvCfgInfo;
   GEN2G_SOL_DRV_CFG_T        *solDrvCfg_p;
   GEN2G_INP_CFG_T            *inpCfg_p;
   GEN2G_NEO_CFG_T            *neoCfg_p;
   U8                         *freeCfg_p;
} GEN2G_INFO;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
   GEN2G_INFO gen2g_info;

#endif