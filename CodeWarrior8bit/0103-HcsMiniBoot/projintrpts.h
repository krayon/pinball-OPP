/*
 *===============================================================================
 *
 *                          HHHHH            HHHHH
 *                           HHH     SSSS     HHH
 *                           HHH   SSSSSSSS   HHH 
 *                           HHH  SSS    SSS  HHH       Hugh Spahr
 *                           HHH SSS      SSS HHH       Utilities
 *                           HHH  SSS         HHH
 *                           HHH    SSSS      HHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHHHHHHHHHHHHHHHHHHH
 *                           HHH         SSS  HHH
 *                           HHH SSS      SSS HHH
 *                           HHH  SSS    SSS  HHH
 *                           HHH   SSSSSSSS   HHH
 *                           HHH     SSSS     HHH
 *                          HHHHH            HHHHH
 *
 * @file:   projintrpts.h
 * @author: Hugh Spahr
 * @date:   4/22/2008
 *
 * @note:    Copyright© 2008, Hugh Spahr
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

#define APP_START_ADDR    0x1900
#define POPULATED_INTS    (INTRPT_RESET | INTRPT_TPM1_OVFL)

void _Startup(void); 
#define main_vector _Startup
interrupt void timer1_isr(void);
#define vector11 timer1_isr

#endif
