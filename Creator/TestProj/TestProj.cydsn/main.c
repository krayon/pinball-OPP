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
 * @file:   main.c
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
 * This is main file.  It initializes the tasks, and runs them.
 *
 *===============================================================================
 */
#include <project.h>
#include "stdtypes.h"
#include "neointf.h"

/* HRS:  This should be a configuration param from serial port */
#define NUM_PIXELS          16

/* Prototype declarations */
void neo_fifo_empty_isr();

void timer_init();
void timer_overflow_isr();

void button_init(
    INT             numPxl);
void button_task();

int main()
{
    /* CyGlobalIntEnable; Enable global interrupts. */

    Clock_Start();
    Clock_1_Start();
    PWM_Start();
    PWM_1_Start();
    SPI_1_Start();
	
    /* Initialize tasks */
    neo_init(NUM_PIXELS);
    timer_init();
    button_init(NUM_PIXELS);

    for(;;)
    {
        timer_overflow_isr();
        neo_fifo_empty_isr();
        neo_task();
        button_task();
    }
}

/* [] END OF FILE */
