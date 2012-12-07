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
 * @file:   stdtypes.h
 * @author: Hugh Spahr
 * @date:   4/22/2008
 *
 * @note:    Copyright© 2008, Hugh Spahr
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
#define MAX_U24_DIGITS  7
#define MAX_U32_DIGITS  10

#endif
