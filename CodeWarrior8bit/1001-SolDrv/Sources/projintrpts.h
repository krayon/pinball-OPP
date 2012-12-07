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
 * @file:   projintrpts.h
 * @author: Hugh Spahr
 * @date:   11/30/2012
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
 * Project interrupts contains all of the interrupts that are used on the
 *  Freescale processor for a project.  POPULATED_INTS contains a bitfield
 *  with a bit set for each interrupt used.  For each interrupt, a function
 *  prototype, and a macro must be defined setting the function to the correct
 *  vector.  APP_START_ADDR contains the starting address of the flash memory
 *  for the Freescale processor.
 *
 *===============================================================================
 */
 
#ifndef PROJINTRPTS_H
#define PROJINTRPTS_H

#define APP_START_ADDR    0x8000
#define POPULATED_INTS    (INTRPT_RESET | INTRPT_TPM2_OVFL |      \
                             INTRPT_SCI1_RCV | INTRPT_SCI1_XMT)

void _Startup(void); 
#define main_vector _Startup
interrupt void stdltime_timer2_isr(void);
#define vector14 stdltime_timer2_isr
interrupt void stdlser_rcv_port1_isr(void);
#define vector17 stdlser_rcv_port1_isr
interrupt void stdlser_xmt_port1_isr(void);
#define vector18 stdlser_xmt_port1_isr

#endif
