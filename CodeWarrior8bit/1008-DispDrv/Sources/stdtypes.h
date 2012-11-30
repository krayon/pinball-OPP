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
 * @file:   stdtypes.h
 * @author: Hugh Spahr
 * @date:   4/22/2008
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
 * These are the standard types that are used by the sample application.
 *
 *===============================================================================
 */
#ifndef STDTYPES_H
#define STDTYPES_H

typedef enum 
{
  FALSE = 0,
  TRUE = !FALSE,
} BOOL;

typedef unsigned char            U8;
typedef char                     S8;
typedef volatile unsigned char   R8;
typedef unsigned int             U16;
typedef int                      S16;
typedef volatile unsigned int    R16;
typedef unsigned long            U32;
typedef long                     S32;
typedef volatile unsigned long   R32;
typedef int                      INT;
typedef unsigned int             UINT;

#define MAX_U8          0xff
#define MAX_U16         0xffff
#define MAX_U32         0xffffffff

#define MAX_U8_DIGITS   3
#define MAX_U32_DIGITS  10

#ifndef NULL
#define NULL            ((void *)0)
#endif

#endif
