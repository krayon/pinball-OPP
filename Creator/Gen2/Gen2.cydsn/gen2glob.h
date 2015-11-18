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

#define GEN2G_CFG_TBL         0x00007e80
#define GEN2G_NV_PARM_SIZE    0xfc
#define GEN2G_NUM_NVCFG       4

typedef enum
{
  NVCFG_UNUSED              = 0x00,
  NVCFG_SOL                 = 0x01,
  NVCFG_INP                 = 0x02,
  NVCFG_COLOR_TBL           = 0x03,
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
   U8                         nvCfgCrc;   /* CRC from wingCfg to end of res3 */
   U8                         res1[3];
   RS232I_GEN2_WING_TYPE_E    wingCfg[RS232I_NUM_WING];
   GEN2G_NVCFG_TYPE_E         nvCfg[GEN2G_NUM_NVCFG];
   U8                         res2[4];
   U8                         cfgData[0xf0];
   /* HRS:  Config can have different orders
   RS232I_SOL_CFG_T           solCfg[RS232I_NUM_GEN2_SOL];
   RS232I_CFG_INP_TYPE_E      inpCfg[RS232I_NUM_GEN2_INP];
   GEN2G_NEO_COLOR_TBL_T      colorTbl[RS232I_SZ_COLOR_TBL];
   U8                         reserved2[0x40]; */
} GEN2G_NV_CFG_T;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
   GEN2G_NV_CFG_T *gen2g_nv_cfg_p
#ifdef GEN2G_INSTANTIATE
   = (GEN2G_NV_CFG_T *)GEN2G_CFG_TBL
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
void soldrv_init();
void inpdrv_init();

#ifndef GEN2G_INSTANTIATE
   extern
#endif
 void (*GEN2G_INIT_FP[MAX_WING_TYPES])()
#ifdef GEN2G_INSTANTIATE
 ={   NULL,                         /* WING_UNUSED */
      soldrv_init,                  /* WING_SOL */
      inpdrv_init,                  /* WING_INP */
      NULL,                         /* WING_INCAND */
      NULL,                         /* WING_SW_MATRIX_OUT */
      NULL,                         /* WING_SW_MATRIX_IN */
      NULL,                         /* WING_NEO */
  }
#endif
;

typedef struct
{
   U16                        procCtl;
   U16                        validSwitch;
   U16                        stateMask;
   STDLI_ELAPSED_TIME_T       elapsedTime;
} GEN2G_SOL_DRV_T;

typedef struct
{
   U16                        inpSwitch;
   U16                        stateMask;
} GEN2G_INP_DRV_T;

typedef struct
{
   BOOL                       validCfg;
   U32                        typeWingBrds;  /* Bit mask of types of populated wing boards */
   U16                        solDrvProcCtl;
   U16                        solDrvValidSwitch;
   GEN2G_SOL_DRV_T            solDrv;
   GEN2G_INP_DRV_T            inpDrv;
   GEN2G_NV_CFG_T             nvCfgInfo;
   U8                         *freeCfg_p;
} GEN2G_INFO;

#ifndef GEN2G_INSTANTIATE
   extern
#endif
   GEN2G_INFO gen2g_info;

#endif