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
 * @file:   timer.c
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
 * This is the timer function.  It is currently expecting a 1ms timer, and
 * simply calls the neopixel stuff on every tick.
 *
 *===============================================================================
 */
#include "stdtypes.h"
#include "procdefs.h"
#include "gen2glob.h"

typedef struct
{
   INT               msCnt;
   INT               neoCnt;
} TMR_INFO;

TMR_INFO tmrInfo;

/* Prototypes */
void neo_40ms_tick();
void incand_40ms_tick();

/*
 * ===============================================================================
 * 
 * Name: timer_init
 * 
 * ===============================================================================
 */
/**
 * Initialize timer
 * 
 * Clear the msCnt.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void timer_init()
{
   tmrInfo.msCnt = 0;
   tmrInfo.neoCnt = 0;
   gen2g_info.ledStateNum = 0;
   gen2g_info.ledStatus = 0;
    
   /* Register the timer isr, start the timer */
}

/*
 * ===============================================================================
 * 
 * Name: timer_overflow_isr
 * 
 * ===============================================================================
 */
/**
 * Timer overflow ISR
 * 
 * On an overflow interrupt, it increments the ms timer.
 * 
 * @param   None 
 * @return  None
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
void timer_overflow_isr()
{
   /* Statement added so interface can be polled instead of interrupt driven */
   if (*(R32 *)TCPWM_CNT0_INTR & TCPWM_INTR_CNT_TC)
   {
      tmrInfo.msCnt++;
       
      /* Clear isr pending bit */
      *(R32 *)TCPWM_CNT0_INTR = TCPWM_INTR_CNT_TC;
        
      /* Call the neopixel timer.  This will eventually be a registered
       *  recurring timer event with a function pointer.
       */
      tmrInfo.neoCnt++;
      if (tmrInfo.neoCnt >= 40)
      {
         /* Move to next LED state */
         gen2g_info.ledStateNum++;
         gen2g_info.ledStateNum &= (GEN2G_MAX_STATE_NUM - 1);
         if ((gen2g_info.ledStateNum & 0x7) == 0)
         {
            gen2g_info.ledStatus ^= GEN2G_STAT_BLINK_FAST_ON;
            if ((gen2g_info.firstCard) && (gen2g_info.ledStateNum == 8))
            {
               stdldigio_write_port(STDLI_DIG_PORT_4, GEN2G_SYNCH_OUT, 0);
            }
         }
         if (gen2g_info.ledStateNum == 0)
         {
            gen2g_info.ledStatus ^= GEN2G_STAT_BLINK_SLOW_ON;
            if (gen2g_info.firstCard && 
               ((gen2g_info.ledStatus & GEN2G_STAT_BLINK_SLOW_ON) == 0))
            {
               stdldigio_write_port(STDLI_DIG_PORT_4, GEN2G_SYNCH_OUT, GEN2G_SYNCH_OUT);
            }
         }
        
         tmrInfo.neoCnt = 0;
         neo_40ms_tick();
         incand_40ms_tick();
      }
   }
}

/*
 * ===============================================================================
 * 
 * Name: timer_get_ms_count
 * 
 * ===============================================================================
 */
/**
 * Get ms count
 * 
 * @param   None 
 * @return  ms count
 * 
 * @pre     None 
 * @note    None
 * 
 * ===============================================================================
 */
INT timer_get_ms_count()
{
   return(tmrInfo.msCnt);
}

/* [] END OF FILE */
