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

/* Clock select register can choose IMO or EXT clock */
#define SRSS_CLK_SELECT          0x400b0100

#define PCLK_CLK_DIVIDER_A00     0x40020000u
#define PCLK_CLK_DIVIDER_A01     0x40020004u
#define PCLK_CLK_DIVIDER_A02     0x40020008u
#define PCLK_CLK_DIVIDER_B00     0x40020040u
#define PCLK_CLK_DIVIDER_B01     0x40020044u
#define PCLK_CLK_DIVIDER_B02     0x40020048u
#define PCLK_CLK_DIVIDER_C00     0x40020080u
#define PCLK_CLK_DIVIDER_C01     0x40020084u
#define PCLK_CLK_DIVIDER_C02     0x40020088u

#define PCLK_CLK_SELECT01        0x40020204      /* SARPUMP */
#define PCLK_CLK_SELECT02        0x40020208      /* SCB0 */
#define PCLK_CLK_SELECT03        0x4002020c      /* SCB1 */
#define PCLK_CLK_SELECT04        0x40020210      /* LCD */
#define PCLK_CLK_SELECT05        0x40020214      /* CSD (1) */
#define PCLK_CLK_SELECT06        0x40020218      /* CSD (2) */
#define PCLK_CLK_SELECT07        0x4002021c      /* SAR */
#define PCLK_CLK_SELECT08        0x40020220      /* TCPWM0 */
#define PCLK_CLK_SELECT09        0x40020224      /* TCPWM1 */
#define PCLK_CLK_SELECT10        0x40020228      /* TCPWM2 */
#define PCLK_CLK_SELECT11        0x4002022c      /* TCPWM3 */
#define PCLK_CLK_SELECT12        0x40020230      /* UDB0 */
#define PCLK_CLK_SELECT13        0x40020234      /* UDB1 */
#define PCLK_CLK_SELECT14        0x40020238      /* UDB2 */
#define PCLK_CLK_SELECT15        0x4002023c      /* UDB3 */

#define TCPWM_CTRL               0x40050000
#define TCPWM_CMD                0x40050008

#define TCPWM_CNT0_CTRL          0x40050100
#define TCPWM_CNT0_STATUS        0x40050104
#define TCPWM_CNT0_COUNTER       0x40050108
#define TCPWM_CNT0_CC            0x4005010c
#define TCPWM_CNT0_CC_BUFF       0x40050110
#define TCPWM_CNT0_PERIOD        0x40050114
#define TCPWM_CNT0_PERIOD_BUFF   0x40050118
#define TCPWM_CNT0_TR_CTRL0      0x40050120
#define TCPWM_CNT0_TR_CTRL1      0x40050124
#define TCPWM_CNT0_TR_CTRL2      0x40050128
#define TCPWM_CNT0_INTR          0x40050130
#define TCPWM_CNT0_INTR_SET      0x40050134
#define TCPWM_CNT0_INTR_MASK     0x40050138
#define TCPWM_CNT0_INTR_MASKED   0x4005013c
    
#define TCPWM_INTR_CNT_TC        0x00000001
   
#define EnableInterrupts         do                      \
                                 {                       \
                                    __asm("CPSIE   i"); \
                                 } while ( 0 )

#define DisableInterrupts        do                      \
                                 {                       \
                                    __asm("CPSID   i"); \
                                 } while ( 0 )
    
#endif

/* [] END OF FILE */
