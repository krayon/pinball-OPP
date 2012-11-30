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
 *===============================================================================
 */
/**
 * Procdefs is an include file that defines standard types so code can easily
 * be ported to different processors.
 * 
 * @file    procdefs.h
 * @author  Hugh Spahr
 * @date    10/16/2007
 *
 * @note    Copyright© 2008, Hugh Spahr
 */
/*
 *===============================================================================
 */
#ifndef PROCDEFS_H_
#define PROCDEFS_H_

typedef unsigned char        U8;
typedef char                 S8;
typedef unsigned short       U16;
typedef short                S16;
typedef unsigned int         U32;
typedef int                  S32;
typedef int                  INT;
typedef unsigned int         UINT;

typedef enum
{
   FALSE                   = 0,
   TRUE                    = !FALSE,
} BOOL;

#endif /*PROCDEFS_H_*/
