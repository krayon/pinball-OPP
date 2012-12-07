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
 * @file:   interrupt.h
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
 * The interrupt file fills out the application start table that contains the
 *  size of the application, version of the software, and the remapped interrupt
 *  vector table.
 *
 *===============================================================================
 */

#ifndef INTERRUPT_H
#define INTERRUPT_H

#define INTRPT_RESET         0x00000001
#define INTRPT_SWI           0x00000002
#define INTRPT_IRQ           0x00000004
#define INTRPT_LOW_VOLT      0x00000008
#define INTRPT_RESERVED4     0x00000010
#define INTRPT_TPM1_CHAN0    0x00000020
#define INTRPT_TPM1_CHAN1    0x00000040
#define INTRPT_RESERVED7     0x00000080
#define INTRPT_RESERVED8     0x00000100
#define INTRPT_RESERVED9     0x00000200
#define INTRPT_RESERVED10    0x00000400
#define INTRPT_TPM1_OVFL     0x00000800
#define INTRPT_TPM2_CHAN0    0x00001000
#define INTRPT_RESERVED13    0x00002000
#define INTRPT_TPM2_OVFL     0x00004000
#define INTRPT_RESERVED15    0x00008000
#define INTRPT_SCI1_ERROR    0x00010000
#define INTRPT_SCI1_RCV      0x00020000
#define INTRPT_SCI1_XMT      0x00040000
#define INTRPT_RESERVED19    0x00080000
#define INTRPT_PORTA         0x00100000
#define INTRPT_RESERVED21    0x00200000
#define INTRPT_RESERVED22    0x00400000
#define INTRPT_ADC           0x00800000
#define INTRPT_RESERVED24    0x01000000
#define INTRPT_RTC           0x02000000
#define INTRPT_RESERVED26    0x04000000
#define INTRPT_RESERVED27    0x08000000
#define INTRPT_RESERVED28    0x10000000
#define INTRPT_RESERVED29    0x20000000
#define INTRPT_RESERVED30    0x40000000
#define INTRPT_RESERVED31    0x80000000

#include "projintrpts.h"

typedef struct
{
  U8                    jumpInst;
  void                  (*intrptVect)(void);
} JUMP_INST_T;

typedef struct
{
  U32                   appLen;           /* Length of application */
  U8                    codeVersion[4];   /* Application version */
  U32                   prodId;           /* Verifies correct code for upgrades */
  U32                   unused;
  JUMP_INST_T           intJmpTbl[0x20];
} APP_START_T;

#ifndef INTERRUPT_INSTANTIATE
 extern
#endif
interrupt void unused_int(void)
#ifdef INTERRUPT_INSTANTIATE
{
}
#else
;
#endif

void main_entry(void);
interrupt void vector1(void);
interrupt void vector2(void);
interrupt void vector3(void);
interrupt void vector4(void);
interrupt void vector5(void);
interrupt void vector6(void);
interrupt void vector7(void);
interrupt void vector8(void);
interrupt void vector9(void);
interrupt void vector10(void);
interrupt void vector11(void);
interrupt void vector12(void);
interrupt void vector13(void);
interrupt void vector14(void);
interrupt void vector15(void);
interrupt void vector16(void);
interrupt void vector17(void);
interrupt void vector18(void);
interrupt void vector19(void);
interrupt void vector20(void);
interrupt void vector21(void);
interrupt void vector22(void);
interrupt void vector23(void);
interrupt void vector24(void);
interrupt void vector25(void);
interrupt void vector26(void);
interrupt void vector27(void);
interrupt void vector28(void);
interrupt void vector29(void);
interrupt void vector30(void);
interrupt void vector31(void);

#define JUMP_INST       (U8)0xcc

#if ((POPULATED_INTS & 0x00000001) != 0)
#define MAIN_VECT       { JUMP_INST, main_vector }
#else
#define MAIN_VECT       { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000002) != 0)
#define VECTOR1         { JUMP_INST, vector1 }
#else
#define VECTOR1         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000004) != 0)
#define VECTOR2         { JUMP_INST, vector2 }
#else
#define VECTOR2         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000008) != 0)
#define VECTOR3         { JUMP_INST, vector3 }
#else
#define VECTOR3         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000010) != 0)
#define VECTOR4         { JUMP_INST, vector4 }
#else
#define VECTOR4         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000020) != 0)
#define VECTOR5         { JUMP_INST, vector5 }
#else
#define VECTOR5         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000040) != 0)
#define VECTOR6         { JUMP_INST, vector6 }
#else
#define VECTOR6         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000080) != 0)
#define VECTOR7         { JUMP_INST, vector7 }
#else
#define VECTOR7         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000100) != 0)
#define VECTOR8         { JUMP_INST, vector8 }
#else
#define VECTOR8         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000200) != 0)
#define VECTOR9         { JUMP_INST, vector9 }
#else
#define VECTOR9         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000400) != 0)
#define VECTOR10         { JUMP_INST, vector10 }
#else
#define VECTOR10         { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00000800) != 0)
#define VECTOR11        { JUMP_INST, vector11 }
#else
#define VECTOR11        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00001000) != 0)
#define VECTOR12        { JUMP_INST, vector12 }
#else
#define VECTOR12        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00002000) != 0)
#define VECTOR13        { JUMP_INST, vector13 }
#else
#define VECTOR13        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00004000) != 0)
#define VECTOR14        { JUMP_INST, vector14 }
#else
#define VECTOR14        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00008000) != 0)
#define VECTOR15        { JUMP_INST, vector15 }
#else
#define VECTOR15        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00010000) != 0)
#define VECTOR16        { JUMP_INST, vector16 }
#else
#define VECTOR16        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00020000) != 0)
#define VECTOR17        { JUMP_INST, vector17 }
#else
#define VECTOR17        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00040000) != 0)
#define VECTOR18        { JUMP_INST, vector18 }
#else
#define VECTOR18        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00080000) != 0)
#define VECTOR19        { JUMP_INST, vector19 }
#else
#define VECTOR19        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00100000) != 0)
#define VECTOR20        { JUMP_INST, vector20 }
#else
#define VECTOR20        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00200000) != 0)
#define VECTOR21        { JUMP_INST, vector21 }
#else
#define VECTOR21        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00400000) != 0)
#define VECTOR22        { JUMP_INST, vector22 }
#else
#define VECTOR22        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x00800000) != 0)
#define VECTOR23        { JUMP_INST, vector23 }
#else
#define VECTOR23        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x01000000) != 0)
#define VECTOR24        { JUMP_INST, vector24 }
#else
#define VECTOR24        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x02000000) != 0)
#define VECTOR25        { JUMP_INST, vector25 }
#else
#define VECTOR25        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x04000000) != 0)
#define VECTOR26        { JUMP_INST, vector26 }
#else
#define VECTOR26        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x08000000) != 0)
#define VECTOR27        { JUMP_INST, vector27 }
#else
#define VECTOR27        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x10000000) != 0)
#define VECTOR28        { JUMP_INST, vector28 }
#else
#define VECTOR28        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x20000000) != 0)
#define VECTOR29        { JUMP_INST, vector29 }
#else
#define VECTOR29        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x40000000) != 0)
#define VECTOR30        { JUMP_INST, vector30 }
#else
#define VECTOR30        { JUMP_INST, unused_int }
#endif

#if ((POPULATED_INTS & 0x80000000) != 0)
#define VECTOR31        { JUMP_INST, vector31 }
#else
#define VECTOR31        { JUMP_INST, unused_int }
#endif

#ifndef INTERRUPT_INSTANTIATE
 extern
#endif
const APP_START_T       appStart
#ifdef INTERRUPT_INSTANTIATE
 @APP_START_ADDR = 
{
  (U32)0xffffffff,                           /* App Length */
  {
    MAJ_VERSION, MIN_VERSION, SUB_VERSION, 0x00,
  },
  (U32)PROD_ID,
  (U32)0xffffffff,                           /* Unused */
  { VECTOR31, VECTOR30, VECTOR29, VECTOR28,
    VECTOR27, VECTOR26, VECTOR25, VECTOR24,
    VECTOR23, VECTOR22, VECTOR21, VECTOR20,
    VECTOR19, VECTOR18, VECTOR17, VECTOR16,
    VECTOR15, VECTOR14, VECTOR13, VECTOR12,
    VECTOR11, VECTOR10, VECTOR9,  VECTOR8,
    VECTOR7,  VECTOR6,  VECTOR5,  VECTOR4,
    VECTOR3,  VECTOR2,  VECTOR1,  MAIN_VECT,
  }
}
#endif
;


#endif
