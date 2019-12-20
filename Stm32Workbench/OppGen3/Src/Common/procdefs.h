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
 * @file:   procdefs.h
 * @author: Hugh Spahr
 * @date:   9/22/2015
 *
 * @note:   Copyright© 2015, Hugh Spahr
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
 * Processor definitions.  It contains generic defines for processor registers,
 * and macros for enable/disable interrupts.
 *
 *===============================================================================
 */

#ifndef PROCDEFS_H
#define PROCDEFS_H

   typedef struct TIMx
   {
      R32 CR1;
      R32 CR2;
      R32 SMCR;
      R32 DIER;
      R32 SR;
      R32 EGR;
      R32 CCMR1;
      R32 CCMR2;
      R32 CCER;
      R32 CNT;
      R32 PSC;
      R32 ARR;
      R32 Unused1;
      R32 CCR1;
      R32 CCR2;
      R32 CCR3;
      R32 CCR4;
      R32 Unused2;
      R32 DCR;
      R32 DMAR;
   } TIMxRegs;

#ifndef INSTANTIATE_PROC
extern
#endif
   TIMxRegs * volatile tim2Base_p
#ifdef INSTANTIATE_PROC
   = (TIMxRegs * volatile)0x40000000
#endif
;

#define TIMx_SR_UIF   0x00000001

typedef struct GPIOxRegs
{
   R32 CRL;
   R32 CRH;
   R32 IDR;
   R32 ODR;
   R32 BSRR;
   R32 BRR;
   R32 LCKR;
} GPIOxRegs;

#ifndef INSTANTIATE_PROC
extern
#endif
   GPIOxRegs * volatile gpioABase_p
#ifdef INSTANTIATE_PROC
= (GPIOxRegs * volatile)0x40010800
#endif
;

#ifndef INSTANTIATE_PROC
extern
#endif
   GPIOxRegs * volatile gpioBBase_p
#ifdef INSTANTIATE_PROC
= (GPIOxRegs * volatile)0x40010c00
#endif
;

#ifndef INSTANTIATE_PROC
extern
#endif
   GPIOxRegs * volatile gpioCBase_p
#ifdef INSTANTIATE_PROC
= (GPIOxRegs * volatile)0x40011000
#endif
;


   typedef struct RCCRegs
   {
      R32 CR;
      R32 CFGR;
      R32 CIR;
      R32 APB2RSTR;
      R32 APB1RSTR;
      R32 AHBENR;
      R32 APB2ENR;
      R32 APB1ENR;
      R32 BDCR;
      R32 CSR;
      R32 AHBSTR;
      R32 CFGR2;
   } RCCRegs;

#ifndef INSTANTIATE_PROC
extern
#endif
	RCCRegs * volatile rccBase_p
#ifdef INSTANTIATE_PROC
   = (RCCRegs * volatile)0x40021000
#endif
;

   typedef struct FlashRegs
   {
      R32 ACR;
      R32 KEYR;
      R32 OPTKEYR;
      R32 SR;
      R32 CR;
      R32 AR;
      R32 Unused;
      R32 OBR;
      R32 WRPR;
   } FlashRegs;

#ifndef INSTANTIATE_PROC
extern
#endif
	FlashRegs * volatile flashBase_p
#ifdef INSTANTIATE_PROC
   = (FlashRegs * volatile)0x40022000
#endif
;

#define FLSH_SR_BSY       0x00000001
#define FLSH_SR_PGERR     0x00000004
#define FLSH_SR_WRPRTERR  0x00000010
#define FLSH_CR_PG        0x00000001
#define FLSH_CR_PER       0x00000002
#define FLSH_CR_STRT      0x00000040

#define EnableInterrupts         do                      \
                                 {                       \
                                    __asm("CPSIE   i");  \
                                 } while ( 0 )

#define DisableInterrupts        do                      \
                                 {                       \
                                    __asm("CPSID   i");  \
                                 } while ( 0 )

/* HRS:  Fill this out */
#define ResetProc                do                      \
                                 {                       \
                                 } while ( 0 )

void Bootloadable_Load();
   
#endif

/* [] END OF FILE */
