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
 * Hex merge is a DOS application that merges a boot hex file and an application
 * hex file to a single output object file.
 * 
 * @file    hexmerge.c
 * @author  Hugh Spahr
 * @date    10/16/2007
 *
 * @note    Copyright© 2008, Hugh Spahr
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
 */
/*
 *===============================================================================
 */

#include "procdefs.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

U8 hexmrg_version[] = "Version 1.2";

typedef enum
{
   NO_PARAM                = 0,
   FILE_NAME               = 1,
   U32_NUM                 = 2,
} PARAM_TYPE_E;

#define MAX_FILE_NAME_LEN  128
#define CFG_MEM_ADDR       0x300000
#define DATA_CMD           0
#define MAGIC_NUM          0xa5

typedef enum
{
   HEX_MERGE               = 0,
   SREC_MERGE              = 1,
   SREC_CREATE_CRC         = 2,
} MERGE_TYPE_E;

typedef struct
{
   char                    bootName[MAX_FILE_NAME_LEN];
   char                    appName[MAX_FILE_NAME_LEN];
   char                    outName[MAX_FILE_NAME_LEN];
   char                    smSName[MAX_FILE_NAME_LEN];
   U32                     fileSize;
   U32                     optBitfield;
   FILE                    *outputFile_p;
   U32                     currLine;
   U32                     upperAddr;
   MERGE_TYPE_E            mrgType;
   U32                     imageCrc;
   U32                     serNum;
   U32                     sectSz;
   U32                     appAddr;
   U32                     appCrc;
} HEXMRG_GLOB_T;

HEXMRG_GLOB_T hexmrg_glob;

typedef enum
{
   USAGE_STRING            = 0x00000001,
   BOOT_FILE_NAME          = 0x00000002,
   APP_FILE_NAME           = 0x00000004,
   OUT_FILE_NAME           = 0x00000008,
   CRC32_BOOT              = 0x00000010,
   SER_NUM                 = 0x00000020,
   SECT_SIZE               = 0x00000040,
   SM_SREC_FILE_NAME       = 0x00000080,
   APP_ADDR                = 0x00000100,
} HEXMRG_OPT_E;

#define REQUIRED_OPT1      (BOOT_FILE_NAME | APP_FILE_NAME | OUT_FILE_NAME)
#define REQUIRED_OPT2      (BOOT_FILE_NAME | CRC32_BOOT)
#define REQUIRED_OPT3      (APP_FILE_NAME | OUT_FILE_NAME | APP_ADDR)

typedef struct
{
   char                    *optName_p;
   PARAM_TYPE_E            paramType;
   void                    *xtraField_p;
   U32                     optFieldBit;
} HEXMRG_OPT_T;

HEXMRG_OPT_T hexmrg_opt_list[] =
{
   { "-?",                 NO_PARAM,      NULL,                                  USAGE_STRING,     },
   { "-boot",              FILE_NAME,     &hexmrg_glob.bootName[0],              BOOT_FILE_NAME,   },
   { "-app",               FILE_NAME,     &hexmrg_glob.appName[0],               APP_FILE_NAME,    },
   { "-out",               FILE_NAME,     &hexmrg_glob.outName[0],               OUT_FILE_NAME,    },
   { "-crc32",             NO_PARAM,      NULL,                                  CRC32_BOOT,       },
   { "-sn",                U32_NUM,       &hexmrg_glob.serNum,                   SER_NUM,          },
   { "-sectsize",          U32_NUM,       &hexmrg_glob.sectSz,                   SECT_SIZE,        },
   { "-smsrec",            FILE_NAME,     &hexmrg_glob.smSName[0],               SM_SREC_FILE_NAME,},
   { "-appaddr",           U32_NUM,       &hexmrg_glob.appAddr,                  APP_ADDR,         },
   { NULL },
};

U8                         HEXMRG_CRC8_LOOKUP[] = 
   { 0x00, 0x07, 0x0E, 0x09, 0x1C, 0x1B, 0x12, 0x15,
     0x38, 0x3F, 0x36, 0x31, 0x24, 0x23, 0x2A, 0x2D };
U32                        HEXMRG_CRC32_LOOKUP[] =
{
   0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f,
   0xe963a535, 0x9e6495a3, 0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988, 
   0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91, 0x1db71064, 0x6ab020f2, 
   0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
   0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9,
   0xfa0f3d63, 0x8d080df5, 0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172,
   0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b, 0x35b5a8fa, 0x42b2986c,
   0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
   0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423,
   0xcfba9599, 0xb8bda50f, 0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924,
   0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d, 0x76dc4190, 0x01db7106,
   0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
   0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d,
   0x91646c97, 0xe6635c01, 0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e,
   0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457, 0x65b0d9c6, 0x12b7e950,
   0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
   0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7,
   0xa4d1c46d, 0xd3d6f4fb, 0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0,
   0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9, 0x5005713c, 0x270241aa,
   0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
   0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81,
   0xb7bd5c3b, 0xc0ba6cad, 0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a,
   0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683, 0xe3630b12, 0x94643b84,
   0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
   0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb,
   0x196c3671, 0x6e6b06e7, 0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc,
   0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5, 0xd6d6a3e8, 0xa1d1937e,
   0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
   0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55,
   0x316e8eef, 0x4669be79, 0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236,
   0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f, 0xc5ba3bbe, 0xb2bd0b28,
   0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
   0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f,
   0x72076785, 0x05005713, 0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38,
   0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21, 0x86d3d2d4, 0xf1d4e242,
   0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
   0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69,
   0x616bffd3, 0x166ccf45, 0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2,
   0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db, 0xaed16a4a, 0xd9d65adc,
   0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
   0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693,
   0x54de5729, 0x23d967bf, 0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94,
   0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d
};

/* Prototypes */
INT hexmrg_copy_boot_to_output(
   FILE                    *outputFile_p,
   U32                     *bootSize_p);
BOOL hexmrg_verify_hex_line(
   U8                      *currLine_p,
   U8                      *data_p,
   U32                     *addr_p,
   U8                      *len_p,
   BOOL                    *endFile_p,
   U8                      *fileName_p);
BOOL hexmrg_convert_ascii_to_hex(
   U8                      *firstChar_p,
   U8                      numChar,
   U8                      *retVal_p);
INT hexmrg_munge_application(
   FILE                    *appFile_p,
   U32                     *startAddr_p,
   U32                     *length_p,
   U8                      *crc8_p);
U8 hexmrg_calculateCrc8(
   INT                     length,
   U8                      *buffer_p, 
   INT                     offset);
void hexmrg_create_hex_line(
   U8                      length,
   U16                     addr,
   U8                      cmd,
   U8                      *data_p,
   U8                      *outStr_p);
void hexmrg_create_hex_field(
   U32                     data,
   UINT                    length,
   U8                      *outStr_p);
INT hexmrg_copy_app_to_output(
   FILE                    *appFile_p,
   FILE                    *outFile_p,
   U32                     startAddr,
   U32                     length,
   U8                      crc8);
INT hexmrg_srec_copy_boot_to_output(
   FILE                    *outputFile_p);
void hexmrg_create_srecord_line(
   U8                      length,
   U32                     addr,
   U8                      cmd,
   U8                      *data_p,
   U8                      *outStr_p);
BOOL hexmrg_update_srecord_length_line(
   U32                     length,
   U8                      *data_p);
void hexmrg_calculate_crc32(
   U8                      *data_p,
   UINT                    length,
   U32                     *crc_p);

/*
*===============================================================================
*
* Name: main
*
*===============================================================================
*/
/**
* Main C entrance function to the application.
*
*  Combine two hex files (boot and application) into a single hex output.
*
* @param  argc [in] number of input params
* @param  argv [in] input param strings
* @return 0 if call successful, nonzero otherwise
*
* @pre   None
* @note  None
*
*===============================================================================
*/
int main(
   int                     argc,
   char                    *argv[])
{
   U32                     currOpt;
   HEXMRG_OPT_T            *currOpt_p;
   INT                     retVal;
   BOOL                    foundOpt;
   FILE                    *outputFile_p;
   FILE                    *appFile_p;
   U32                     bootSize;
   U32                     startAddr;
   U32                     bootNameLen;
   U32                     appNameLen;
   U32                     length;
   U8                      crc8;
   U8                      inputBuf[4];
   U8                      dataBuf[255];
   INT                     index;

#define FREESCALE_TOP_MEM               0x10000
#define SERNUM_ADDR                     0xfc00
   
   currOpt = 1;
   hexmrg_glob.optBitfield = 0;
   hexmrg_glob.imageCrc = 0xffffffff;
   outputFile_p = NULL;
   hexmrg_glob.sectSz = 0x300;
   hexmrg_glob.bootName[0] = 0;
   hexmrg_glob.appName[0] = 0;

   while (currOpt < argc)
   {
      for (currOpt_p = &hexmrg_opt_list[0], foundOpt = FALSE;
         (currOpt_p->optName_p != NULL) && !foundOpt;
         currOpt_p++)
      {
         retVal = strcmp(currOpt_p->optName_p ,argv[currOpt]);
         if (retVal == 0)
         {
            foundOpt = TRUE;
            hexmrg_glob.optBitfield |= currOpt_p->optFieldBit;
            switch (currOpt_p->paramType)
            {
               case NO_PARAM:
               {
                  currOpt++;
                  break;
               }
               case FILE_NAME:
               {
                  retVal = strlen(argv[currOpt + 1]);
                  if (retVal >= MAX_FILE_NAME_LEN)
                  {
                     printf("File name \"%s\" too long.\n", argv[currOpt + 1]);
                     return(1);
                  }
                  strcpy(currOpt_p->xtraField_p, argv[currOpt + 1]);
                  currOpt += 2;
                  break;
               }
               case U32_NUM:
               {
                  *(U32 *)currOpt_p->xtraField_p = (U32)strtol(argv[currOpt + 1], 0, 0);
                  currOpt += 2;
                  break;
               }
               default:
               {
                  printf("Software error!  paramType = %d!\n", currOpt_p->paramType);
                  return(2);
               }
            }
         } /* end if passed parameter option found */
      } /* find the passed parameter option */
      
      if (!foundOpt)
      {
         printf("Illegal parameter \"%s\".\n", argv[currOpt]);
         return(3);
      }
   } /* end walking through passed parameters */
   
   if ((argc == 1) || (hexmrg_glob.optBitfield & USAGE_STRING) || 
      (((hexmrg_glob.optBitfield & REQUIRED_OPT1) != REQUIRED_OPT1) &&
      ((hexmrg_glob.optBitfield & REQUIRED_OPT2) != REQUIRED_OPT2) &&
      ((hexmrg_glob.optBitfield & REQUIRED_OPT3) != REQUIRED_OPT3)))
   {
      printf("hexmerge -boot bootFileName -app appFileName -out outFileName\n");
      printf("hexmerge -boot bootFileName -crc32\n");
      printf("           -?                        Options Help\n");
      printf("           -boot bootFileName        Input boot hex filename\n");
      printf("           -app  appFileName         Input application hex filename\n");
      printf("           -out  outFileName         Output merged hex filename\n");
      printf("           -crc32                    Display CRC32 of bootloader\n");
      printf("           -sn serialNumber          Input serial number for the unit\n");
      printf("           -sectsize sectorsize      Sector size for the processor\n");
      printf("           -smsrec fileName          Output s-records with 8 bytes data\n");
      printf("           -appaddr appaddr          Address of the start of the application\n");
      printf("%s", &hexmrg_version[0]);
      return(0);
   }
   
   /* Open the output file. Create it if necessary */
   if (hexmrg_glob.optBitfield & OUT_FILE_NAME)
   {
      outputFile_p = fopen(&hexmrg_glob.outName[0], "w+b");
      if (outputFile_p == NULL)
      {
         printf("Output file \"%s\" couldn't be created.", &hexmrg_glob.outName[0]);
         return(4);
      }
   }
   
   /* Check to see if this is a hex merge or an s-record merge */
   bootNameLen = strlen(&hexmrg_glob.bootName[0]);
   appNameLen = strlen(&hexmrg_glob.appName[0]);
   if ((bootNameLen > 2) && ((strcmp(&hexmrg_glob.bootName[bootNameLen - 2], "sx") == 0) ||
	   (strcmp(&hexmrg_glob.bootName[bootNameLen - 2], "SX") == 0)))
   {
      hexmrg_glob.mrgType = SREC_MERGE;
   }
   else if ((appNameLen > 3) && ((strcmp(&hexmrg_glob.appName[appNameLen - 3], "s19") == 0) ||
         (strcmp(&hexmrg_glob.appName[appNameLen - 3], "S19") == 0)))
   {
      hexmrg_glob.mrgType = SREC_CREATE_CRC;
   }
   else
   {
      hexmrg_glob.mrgType = HEX_MERGE;
   }
   
   /* Copy the boot to the output file if a hex file.  If Srecord, just verify
    * the file.  Find boot size.
    */
   if ((hexmrg_glob.mrgType == SREC_MERGE) ||
         (hexmrg_glob.mrgType == HEX_MERGE))
   {
      retVal = hexmrg_copy_boot_to_output(outputFile_p, &bootSize);
      if (retVal || (outputFile_p == NULL))
      {
         /* Either an error occurred, or only want to calculate CRC32 of boot */
         if (outputFile_p)
         {
            fclose(outputFile_p);
         }
         if (retVal == 0)
         {
            printf("HexMerge worked!\n");
         }
         return(retVal);
      }
   }
      
   /* Open the application file. */
   appFile_p = fopen(&hexmrg_glob.appName[0], "r+b");
   if (appFile_p == NULL)
   {
      printf("Application file \"%s\" couldn't be found.", &hexmrg_glob.appName[0]);
      fclose(outputFile_p);
      return(5);
   }
   
   /* Munge application file */
   retVal = hexmrg_munge_application(appFile_p, &startAddr, &length, &crc8);
   if (retVal)
   {
      fclose(appFile_p);
      fclose(outputFile_p);
      return(retVal);
   }
   
   /* Make sure that the boot code isn't being overwritten */
   if (((hexmrg_glob.mrgType == HEX_MERGE) && bootSize >= startAddr) ||
      ((hexmrg_glob.mrgType == SREC_MERGE) && (FREESCALE_TOP_MEM -
            ((bootSize + (hexmrg_glob.sectSz - 1))/hexmrg_glob.sectSz) *
            hexmrg_glob.sectSz < startAddr + length)))
   {
      printf("Application file \"%s\" overwrites boot file.", &hexmrg_glob.appName[0]);
      fclose(appFile_p);
      fclose(outputFile_p);
      return(6);
   }

   /* Copy application file to output file */
   rewind(appFile_p);
   retVal = hexmrg_copy_app_to_output(appFile_p, outputFile_p, startAddr, length, crc8);
   if (retVal)
   {
      fclose(appFile_p);
      fclose(outputFile_p);
      return(retVal);
   }
   
   /* If S-Record file, now copy the bootloader to the output file */
   if (hexmrg_glob.mrgType == SREC_MERGE)
   {
      /* Insert the Serial Number into the unit if needed */
      if (hexmrg_glob.optBitfield & SER_NUM)
      {
         /* Write app length to the file */
         for (index = 0; index < sizeof(hexmrg_glob.serNum); index++)
         {
            inputBuf[index] = (hexmrg_glob.serNum >> ((3 - index) * 8)) & 0xff;
         }
         hexmrg_create_srecord_line(sizeof(hexmrg_glob.serNum), SERNUM_ADDR, 1,
            &inputBuf[0], &dataBuf[0]);
         fprintf(outputFile_p, "%s", &dataBuf[0]);
      }
      
      retVal = hexmrg_srec_copy_boot_to_output(outputFile_p);
      if (retVal)
      {
         fclose(outputFile_p);
         return(retVal);
      }
   }   
   
   /* Calculate the CRC32 for the image file */
   hexmrg_glob.imageCrc ^= 0xffffffff;
   printf("Image CRC = 0x%08x\n", hexmrg_glob.imageCrc);
   
   fclose(appFile_p);
   fclose(outputFile_p);
   printf("HexMerge worked!\n");
   return(0);
}

/*
*===============================================================================
*
* Name: hexmrg_copy_boot_to_output
*
*===============================================================================
*/
/**
* Copy boot hex image to an output file
*
* @param  outputFile_p [in]  output file 
* @param  bootSize_p   [out] size of the boot image 
* @return 0 if call successful, nonzero otherwise
*
* @pre   None
* @note  None
*
*===============================================================================
*/
INT hexmrg_copy_boot_to_output(
   FILE                    *outputFile_p,
   U32                     *bootSize_p)
{
   FILE                    *inputFile_p;
   U8                      inputBuf[272];
   U8                      dataBuf[255];
   U32                     bootSize;
   BOOL                    endFile;
   U8                      *ret_p;
   BOOL                    retVal;
   U32                     addr;
   U8                      len;
   U32                     bootCrc;

   bootSize = 0;
   endFile = FALSE;
   bootCrc = 0xffffffff;
   
   /* Open the input file and verify it exists */
   inputFile_p = fopen(&hexmrg_glob.bootName[0], "rb");
   if (inputFile_p == NULL)
   {
      printf("Input file \"%s\" doesn't exist.\n", &hexmrg_glob.bootName[0]);
      return(100);
   }
   
   hexmrg_glob.currLine = 0;
   hexmrg_glob.upperAddr = 0;
   while (!endFile)
   {
      ret_p = fgets(&inputBuf[0], 272, inputFile_p);
      if (ret_p == NULL)
      {
         printf("Boot file \"%s\":%d ended prematurely.\n",
            &hexmrg_glob.bootName[0], hexmrg_glob.currLine);
         fclose(inputFile_p);
         return(101);
      }
      retVal = hexmrg_verify_hex_line(&inputBuf[0], &dataBuf[0], &addr,
         &len, &endFile, &hexmrg_glob.bootName[0]);
      if (retVal)
      {
         /* Error messages already output */
         fclose(inputFile_p);
         return(102);
      }
      if (addr + len >= CFG_MEM_ADDR)
      {
         /* Warn about boot containing config bits */
         printf("\n!! Warning !! Boot image contains config bits.\n");
         printf("!! Warning !! This should only occur in debug mode.\n\n");
      }
      if ((addr + len > bootSize) && (addr < CFG_MEM_ADDR))
      {
         bootSize = addr + len;
      }
      
      /* Copy the data to the output if a hex file since the bootloader is in
       *    lower memory.
       */
      if (!endFile && (hexmrg_glob.mrgType == HEX_MERGE) && outputFile_p)
      {
         /* Copy the data into the output file */
         fprintf(outputFile_p, "%s", &inputBuf[0]);
      }

      /* Calculate the CRC32 for the boot file.  If this is an S-Record
       *    file, ignore the S0 record.
       */
      if (!endFile && ((hexmrg_glob.mrgType == HEX_MERGE) ||
         ((hexmrg_glob.mrgType == SREC_MERGE) && (inputBuf[1] != '0'))))
      {
         hexmrg_calculate_crc32(&inputBuf[0], strlen(&inputBuf[0]),
            &bootCrc);
      }
      hexmrg_glob.currLine++;
   }
   *bootSize_p = bootSize;
   fclose(inputFile_p);
   bootCrc ^= 0xffffffff;
   printf("Boot CRC = 0x%08x\n", bootCrc);
   
   /* If this is a hex file, the boot CRC is the start of the image CRC */
   hexmrg_glob.imageCrc = bootCrc;
   return(0);
} /* End hexmrg_copy_boot_to_output */

/*
*===============================================================================
*
* Name: hexmrg_srec_copy_boot_to_output
*
*===============================================================================
*/
/**
* Copy boot hex image to an output file (only called for S-Record files)
*
* @param  outputFile_p [in]  output file 
* @return 0 if call successful, nonzero otherwise
*
* @pre   None
* @note  None
*
*===============================================================================
*/
INT hexmrg_srec_copy_boot_to_output(
   FILE                    *outputFile_p)
{
   FILE                    *inputFile_p;
   U8                      inputBuf[272];
   BOOL                    endFile;
   U8                      *ret_p;

   endFile = FALSE;
   
   /* Open the input file and verify it exists */
   inputFile_p = fopen(&hexmrg_glob.bootName[0], "rb");
   if (inputFile_p == NULL)
   {
      printf("Input file \"%s\" doesn't exist.\n", &hexmrg_glob.bootName[0]);
      return(400);
   }
   
   while (!endFile)
   {
      ret_p = fgets(&inputBuf[0], 272, inputFile_p);
      if (ret_p == NULL)
      {
         printf("Boot file \"%s\":%d ended prematurely.\n",
            &hexmrg_glob.bootName[0], hexmrg_glob.currLine);
         fclose(inputFile_p);
         return(401);
      }
      
      /* The S0 header record is ignored */
      if (inputBuf[1] != '0')
      {
         /* Copy the data into the output file */
         fprintf(outputFile_p, "%s", &inputBuf[0]);
         hexmrg_calculate_crc32(&inputBuf[0], strlen(&inputBuf[0]),
            &hexmrg_glob.imageCrc);
      }
      /* The S9 record is the last record in the file */
      if (inputBuf[1] == '9')
      {
         endFile = TRUE;
      }
      hexmrg_glob.currLine++;
   }
   return(0);
} /* End hexmrg_srec_copy_boot_to_output */

/*
* ===============================================================================
* 
* Name: hexmrg_verify_hex_line
* 
* ===============================================================================
*/
/**
* Verify a line from a hex file to positions in the byte array.
* 
* Extract the length and address from the line.  Verify that the line checksum
* is correct.  Return the end hex address of this line.
* 
* @param   currLine_p   [in]  current line 
* @param   data_p       [out] data from the ascii line 
* @param   addr_p       [out] starting data address 
* @param   len_p        [out] length of data 
* @param   endFile_p    [out] TRUE if reached end of file 
* @param   fileName_p   [in]  File name, only used for error reporting 
* @return  0 if call successful, nonzero otherwise
* 
* @pre     None
* @note    We assume all hex files are in upper case. 
* 
* ===============================================================================
*/
BOOL hexmrg_verify_hex_line(
   U8                      *currLine_p,
   U8                      *data_p,
   U32                     *addr_p,
   U8                      *len_p,
   BOOL                    *endFile_p,
   U8                      *fileName_p)
{
   U8                      length;
   BOOL                    retVal;
   U8                      checksum;
   INT                     index;

   /* Check if this looks like a valid line */
   if (((hexmrg_glob.mrgType == HEX_MERGE) && (currLine_p[0] != ':')) ||
		(((hexmrg_glob.mrgType == SREC_MERGE) || (hexmrg_glob.mrgType == SREC_CREATE_CRC)) &&
		(currLine_p[0] != 'S')) ||
		(currLine_p[1] == 0) || (currLine_p[2] == 0))
   {
      printf("File \"%s\":%d line invalid.\n", fileName_p,
         hexmrg_glob.currLine);
      printf("Error line = \"%s\"\n", currLine_p);
      return (TRUE);
   }
   if (hexmrg_glob.mrgType == HEX_MERGE)
   {
      /* This is a hex file so do appropriate processing */
      retVal = hexmrg_convert_ascii_to_hex(&currLine_p[1], 1, &length);
      if (retVal)
      {
         printf("File \"%s\":%d line length field invalid.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      if ((strlen(currLine_p) < (length * 2) + 11) || (length > 16))
      {
         /* Line not long enough to be valid */
         printf("File \"%s\":%d line length mismatch.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      
      /* Convert the ascii chars to hex */
      retVal = hexmrg_convert_ascii_to_hex(&currLine_p[1], length + 5, data_p);
      if (retVal)
      {
         /* Convert ascii to hex failed */
         printf("File \"%s\":%d convert ascii to hex failed.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      
      /* Verify the checksum */
      for (index = 0, checksum = 0; index < length + 4; index++)
      {
         checksum += data_p[index];
      }
      checksum = -checksum;
      if (checksum != data_p[index])
      {
         /* Convert ascii to hex failed */
         printf("File \"%s\":%d line checksum failure.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      
      /* Store info in the array */
      switch (data_p[3])
      {
         case 0:
         {
            /* Data record */
            *addr_p = hexmrg_glob.upperAddr + (data_p[1] << 8) + data_p[2];
            *len_p = length;
            *endFile_p = FALSE;
            break;
         }
         case 1:
         {
            /* End record */
            *addr_p = 0;
            *len_p = 0;
            *endFile_p = TRUE;
            break;
         }
         case 4:
         {
            /* addr record, update upper 16 bits of address */
            hexmrg_glob.upperAddr = ((data_p[4] << 24) | (data_p[5] << 16));
            *addr_p = hexmrg_glob.upperAddr;
            *len_p = 0;
            *endFile_p = FALSE;
            break;
         }
         default:
         {
            printf("File \"%s\":%d unknown command.\n",
               fileName_p, hexmrg_glob.currLine);
            printf("Error line = \"%s\"\n", currLine_p);
            return(TRUE);
            break;
         }
      }
   }
   else
   {
      /* This is a S-Record file so do appropriate processing */
      retVal = hexmrg_convert_ascii_to_hex(&currLine_p[2], 1, &length);
      if (retVal)
      {
         printf("File \"%s\":%d line length field invalid.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      if (strlen(currLine_p) != (length * 2) + 6)
      {
         /* Line length not valid */
         printf("File \"%s\":%d line length mismatch.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      
      /* Convert the ascii chars to hex */
      retVal = hexmrg_convert_ascii_to_hex(&currLine_p[4], length, data_p);
      if (retVal)
      {
         /* Convert ascii to hex failed */
         printf("File \"%s\":%d convert ascii to hex failed.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      
      /* Verify the checksum */
      for (index = 0, checksum = length; index < length - 1; index++)
      {
         checksum += data_p[index];
      }
      checksum = -checksum;
      checksum--;
      if (checksum != data_p[index])
      {
         /* Convert ascii to hex failed */
         printf("File \"%s\":%d line checksum failure.\n", fileName_p,
            hexmrg_glob.currLine);
         printf("Error line = \"%s\"\n", currLine_p);
         return (TRUE);
      }
      
      /* Store info in the array */
      switch (currLine_p[1])
      {
         case '0':
         {
            /* Header record */
            *addr_p = 0;
            *len_p = 0;
            *endFile_p = FALSE;
            break;
         }
         case '1':
         {
            /* Data record */
            *addr_p = hexmrg_glob.upperAddr + (data_p[0] << 8) + data_p[1];
            *len_p = length - 3;
            *endFile_p = FALSE;
            break;
         }
         case '3':
         {
            /* Data record */
            *addr_p = (data_p[0] << 24) + (data_p[1] << 16) + (data_p[2] << 8) + data_p[3];
            *len_p = length - 5;
            *endFile_p = FALSE;
            break;
         }
         case '7':
         case '9':
         {
            /* End record */
            *addr_p = 0;
            *len_p = 0;
            *endFile_p = TRUE;
            break;
         }
         default:
         {
            printf("File \"%s\":%d unknown command.\n",
               fileName_p, hexmrg_glob.currLine);
            printf("Error line = \"%s\"\n", currLine_p);
            return(TRUE);
            break;
         }
      }
   }
   return (FALSE);
} /* End hexmrg_verify_hex_line */

/*
* ===============================================================================
* 
* Name: hexmrg_convert_ascii_to_hex
* 
* ===============================================================================
*/
/**
* Convert ascii characters to hex data
* 
* @param   firstChar_p  [in]  first char to convert 
* @param   numChar      [in]  number of characters to convert 
* @param   retVal_p     [out] the converted value returned 
* @return  FALSE if call successful, TRUE otherwise
* 
* @pre     None
* @note    None 
* 
* ===============================================================================
*/
BOOL hexmrg_convert_ascii_to_hex(
   U8                      *firstChar_p,
   U8                      numChar,
   U8                      *retVal_p)
{
   UINT                    retVal;
   UINT                    cnt;
   U8                      currChar;
   
   retVal = 0;
   for (cnt = 0; cnt < numChar * 2; cnt++, firstChar_p++)
   {
      currChar = *firstChar_p;
      if ((currChar >= '0') && (currChar <= '9'))
      {
         currChar -= '0';
      }  
      else if ((currChar >= 'A') && (currChar <= 'F'))
      {
         currChar = currChar - 'A' + 10;
      }
      else
      {
         /* Unsupported character */
         return (TRUE);
      }
      retVal <<= 4;
      retVal |= currChar;
      
      /* If this is the second character, update array */
      if (cnt & 0x1)
      {
         *retVal_p = retVal;
         retVal_p++;
         retVal = 0;
      }
   }
   return (FALSE);
} /* End hexmrg_convert_ascii_to_hex */

/*
* ===============================================================================
* 
* Name: hexmrg_munge_application
* 
* ===============================================================================
*/
/**
* Munge application file
* 
* Extract data from the application file.  Compute the starting address, length
* and CRC8 of the application.
* 
* @param   appFile_p    [in]  file structure for app file 
* @param   startAddr_p  [out] startAddr for app file 
* @param   length_p     [out] length of application 
* @param   crc8_p       [out] crc8 for the application 
* @return  0 if call successful, nonzero otherwise
* 
* @pre     None
* @note    None 
* 
* ===============================================================================
*/
INT hexmrg_munge_application(
   FILE                    *appFile_p,
   U32                     *startAddr_p,
   U32                     *length_p,
   U8                      *crc8_p)
{
   U8                      inputBuf[255];
   U8                      dataBuf[255];
   U32                     addr;
   U8                      len;
   BOOL                    endFile;
   U32                     startAddr;
   U32                     endAddr;
   U8                      *image_p;
   U8                      *ret_p;
   BOOL                    foundCfg;
   INT                     index;
   INT                     retVal;
   U32                     appCrc;
   U8                      crc8;
   FILE                    *smallSrecFile_p;
   U32                     length;
   U32                     smSrecCrc;
   U32                     imageLen;
   U32                     bootCrc;

#define BYTES_IN_SREC	   8
#define MAX_IMAGE_SZ       0x80000
#define CF_IMAGE_LEN_OFF   sizeof(void *) + sizeof(UINT)    /* Offset from start of app */
   
   image_p = malloc(MAX_IMAGE_SZ);
   if (image_p == NULL)
   {
      printf("Could not allocate memory for image.\n");
      return(200);
   }
   for (index = 0, ret_p = image_p; index < MAX_IMAGE_SZ; index++, ret_p++)
   {
      *ret_p = 0xff;
   }
   
   startAddr = 0xffffffff;
   appCrc = 0xffffffff;
   endAddr = 0;
   hexmrg_glob.currLine = 0;
   hexmrg_glob.upperAddr = 0;
   foundCfg = FALSE;
   endFile = FALSE;
   while (!endFile)
   {
      ret_p = fgets(&inputBuf[0], 255, appFile_p);
      if (ret_p == NULL)
      {
         printf("App file \"%s\":%d ended prematurely.\n",
            &hexmrg_glob.appName[0], hexmrg_glob.currLine);
         free(image_p);
         return(201);
      }
      retVal = hexmrg_verify_hex_line(&inputBuf[0], &dataBuf[0], &addr,
         &len, &endFile, &hexmrg_glob.appName[0]);
      if (retVal)
      {
         /* Error messages already output */
         free(image_p);
         return(202);
      }
      
      /* Calculate the CRC32 for the app file.  If this is an S-Record
       *    file, ignore the S0 record.
       */
      if (!endFile && ((hexmrg_glob.mrgType == HEX_MERGE) ||
         ((hexmrg_glob.mrgType == SREC_MERGE) && (inputBuf[1] != '0'))))
      {
         hexmrg_calculate_crc32(&inputBuf[0], strlen(&inputBuf[0]),
            &appCrc);
      }
      
      if (addr + len >= CFG_MEM_ADDR)
      {
         foundCfg = TRUE;
      }
      if (addr < CFG_MEM_ADDR)
      {
         if (addr + len > endAddr)
         {
            endAddr = addr + len;
         }
         if ((addr < startAddr) && (len != 0))
         {
            startAddr = addr;
         }
         for (index = 0; index < len; index++)
         {
            /* Copy the data into the image file */
            if ((hexmrg_glob.mrgType == HEX_MERGE) ||
               (hexmrg_glob.mrgType == SREC_CREATE_CRC))
            {
               image_p[addr + index] = dataBuf[index + 4];               
            }
            else
            {
               image_p[addr + index] = dataBuf[index + 2];               
            }
         }
      }
      hexmrg_glob.currLine++;
   }

   /* If just creating the CRC, i.e. coldfire, app starts at hexmrg_glob.appAddr */
   if (hexmrg_glob.mrgType == SREC_CREATE_CRC)
   {
      startAddr = hexmrg_glob.appAddr;
   }

   /* Check if the config bits were found, only for hex files */
   if (!foundCfg && (hexmrg_glob.mrgType == HEX_MERGE))
   {
      printf("\n!! Warning !! App image does not contain config bits.\n");
      printf("!! Warning !! This should not occur.\n\n");
   }

   /* If this is a hex file, the app length isn't stuffed into the image.
    *   For S-record files, it is which seems to make more sense to me.
    */
   if (hexmrg_glob.mrgType == HEX_MERGE)
   {
      addr = 0x04;
   }
   else
   {
      addr = 0x00;
   }
   if ((startAddr & 0xff) != addr)
   {
      printf("App file \"%s\" has incorrect start addr 0x%08x.\n",
         &hexmrg_glob.appName[0], startAddr);
      free(image_p);
      return(203);
   }
   startAddr &= ~0xff;
   length = endAddr - startAddr;
   
   /* The s19 file already has the image size installed by the linker */
   if ((hexmrg_glob.mrgType == HEX_MERGE) || (hexmrg_glob.mrgType == SREC_MERGE))
   {
      /* Toss the size into the image */
      *length_p = length;
      for (index = 0; index < sizeof(U32); index++)
      {
         image_p[startAddr + index] =  (length >> ((3 - index) * 8)) & 0xff;
      }

      /* Calculate the CRC8 */
      crc8 =  hexmrg_calculateCrc8(length, image_p, startAddr);

      /* See if need to create small S record file */
      if (hexmrg_glob.optBitfield & SM_SREC_FILE_NAME)
      {
         smallSrecFile_p = fopen(&hexmrg_glob.smSName[0], "w+b");
         if (smallSrecFile_p == NULL)
         {
            printf("Small S record file \"%s\"can't be created.\n",
               &hexmrg_glob.smSName[0]);
            free(image_p);
            return(204);
         }
         smSrecCrc = 0xffffffff;

         /* Store CRC8 and end marker in image */
         image_p[startAddr + length] = crc8;
         image_p[startAddr + 1 + length] = MAGIC_NUM;

         /* Add length for CRC and magic num, and make divisible by 8 */
         length += 2;
         length = (length + (BYTES_IN_SREC - 1)) & ~(BYTES_IN_SREC - 1);

         /* Write the small S record file */
         for (index = startAddr; index < startAddr + length; index += 8)
         {
            hexmrg_create_srecord_line(BYTES_IN_SREC, index, 1,
               &image_p[index], &dataBuf[0]);
            fprintf(smallSrecFile_p, "%s", &dataBuf[0]);
            hexmrg_calculate_crc32(&dataBuf[0], strlen(&dataBuf[0]),
               &smSrecCrc);
         }
         fclose(smallSrecFile_p);
         smSrecCrc ^= 0xffffffff;
         printf("Small Srec CRC = 0x%08x\n", smSrecCrc);
      }
      *crc8_p = crc8;
      appCrc ^= 0xffffffff;
   }
   else
   {
      /* SREC_CREATE_CRC, Verify the length is correct */
      imageLen = (image_p[hexmrg_glob.appAddr + CF_IMAGE_LEN_OFF] << 24) +
            (image_p[hexmrg_glob.appAddr + CF_IMAGE_LEN_OFF + 1] << 16) +
            (image_p[hexmrg_glob.appAddr + CF_IMAGE_LEN_OFF + 2] << 8) +
            image_p[hexmrg_glob.appAddr + CF_IMAGE_LEN_OFF + 3];
      if (imageLen != length)
      {
         printf("Application image length mismatch.  Image Len = 0x%08x, App Len = 0x%08x.\n",
               imageLen, length);
         free(image_p);
         return(205);
      }
      *length_p = length;

      /* Calculate the CRC for the bootloader */
      bootCrc = 0xffffffff;
      hexmrg_calculate_crc32(&image_p[0], hexmrg_glob.appAddr,
         &bootCrc);
      bootCrc ^= 0xffffffff;
      printf("Boot CRC = 0x%08x\n", bootCrc);

      /* Calculate the CRC32 for the application */
      appCrc = 0xffffffff;
      hexmrg_calculate_crc32(&image_p[hexmrg_glob.appAddr], imageLen,
         &appCrc);
      appCrc ^= 0xffffffff;
      hexmrg_glob.appCrc = appCrc;

      /* Write the app CRC to the image */
      image_p[hexmrg_glob.appAddr + imageLen] = (appCrc >> 24) & 0xff;
      image_p[hexmrg_glob.appAddr + imageLen + 1] = (appCrc >> 16) & 0xff;
      image_p[hexmrg_glob.appAddr + imageLen + 2] = (appCrc >> 8) & 0xff;
      image_p[hexmrg_glob.appAddr + imageLen + 3] = appCrc & 0xff;

      /* Calculate the CRC32 for the image */
      hexmrg_calculate_crc32(&image_p[0], hexmrg_glob.appAddr + imageLen + sizeof(U32),
         &hexmrg_glob.imageCrc);

   }

   *startAddr_p = startAddr;
   free(image_p);

   printf("App CRC = 0x%08x\n", appCrc);
   return(0);
} /* End hexmrg_munge_application */

/*
* ===============================================================================
* 
* Name: hexmrg_calculateCrc8
* 
* ===============================================================================
*/
/**
* \brief   Calculate CRC8
* 
* Calculate the CRC8 for a byte stream.  This uses a lookup table to process
* 4 bits at a time for speed.  Generator polynomial is x^8+x^2+x+1 with an
* initial value of 0xff.  This conforms to the CCITT-CRC8.
* 
* @param   length   [in] number of bytes in array 
* @param   buffer_p [in] array of bytes to calculate CRC8 
* @param   offset   [in] offset into array to start calculation 
* @return  None
* 
* @pre     None 
* @note    None
* 
* ===============================================================================
*/
U8 hexmrg_calculateCrc8(
   INT                     length,
   U8                      *buffer_p, 
   INT                     offset)
{
   U8                      currCrc;
   INT                     count;

   currCrc = 0xff;
   for (count = 0; count < length; count++)
   {
      currCrc = (((currCrc << 4) & 0xf0) ^ HEXMRG_CRC8_LOOKUP[
         (((currCrc) ^ (buffer_p[count + offset])) >> 4) & 0x0f]);
      currCrc = (((currCrc << 4) & 0xf0) ^ HEXMRG_CRC8_LOOKUP[
         (((currCrc >> 4) & 0x0f) ^ (buffer_p[count + offset])) & 0x0f]);
   }
   return (currCrc);
}

/*
*===============================================================================
*
* Name: hexmrg_copy_app_to_output
*
*===============================================================================
*/
/**
* Copy app hex image to an output file
*
* @param  appFile_p  [in]  application file 
* @param  outFile_p  [in]  output file 
* @param  startAddr  [in]  size of the boot image 
* @param  length     [in]  size of the boot image 
* @param  crc8       [in]  size of the boot image 
* @return 0 if call successful, nonzero otherwise
*
* @pre   None
* @note  None
*
*===============================================================================
*/
INT hexmrg_copy_app_to_output(
   FILE                    *appFile_p,
   FILE                    *outFile_p,
   U32                     startAddr,
   U32                     length,
   U8                      crc8)
{
   U8                      inputBuf[4];
   U8                      dataBuf[255];
   U8                      outBuf[255];
   BOOL                    endFile;
   U8                      *ret_p;
   BOOL                    retVal;
   U32                     addr;
   U8                      len;
   INT                     index;
   U8                      headerStr[]= "Hugh Spahr Utils";

#define EXT_ADDR_CMD       4
#define EXT_ADDR_LEN       2

   hexmrg_glob.currLine = 0;
   hexmrg_glob.upperAddr = 0;
   if (hexmrg_glob.mrgType == HEX_MERGE)
   {
      /* Jamma-wamma the length into the application */
      /* Start by forcing the upper address to 0 */
      inputBuf[0] = 0;
      inputBuf[1] = 0;
      hexmrg_create_hex_line(EXT_ADDR_LEN, DATA_CMD, EXT_ADDR_CMD,
         &inputBuf[0], &dataBuf[0]);
      fprintf(outFile_p, "%s", &dataBuf[0]);
      hexmrg_calculate_crc32(&dataBuf[0], strlen(&dataBuf[0]),
         &hexmrg_glob.imageCrc);
      
      /* Write app length to the file */
      for (index = 0; index < sizeof(length); index++)
      {
         inputBuf[index] = (length >> ((3 - index) * 8)) & 0xff;
      }
      hexmrg_create_hex_line(sizeof(length), startAddr, DATA_CMD,
         &inputBuf[0], &dataBuf[0]);
      fprintf(outFile_p, "%s", &dataBuf[0]);
      hexmrg_calculate_crc32(&dataBuf[0], strlen(&dataBuf[0]),
         &hexmrg_glob.imageCrc);
   }
   else
   {
      /* Fill out the S0 Record, "Hugh Spahr Utils"  The S0 record
       *    does not get CRC'd.
       */
      hexmrg_create_srecord_line(strlen(&headerStr[0]), 0, 0,
            &headerStr[0], &dataBuf[0]);
      fprintf(outFile_p, "%s", &dataBuf[0]);
      
      /* Read the S0 record and discard it. */
      ret_p = fgets(&dataBuf[0], 255, appFile_p);
      if (ret_p == NULL)
      {
         printf("App file \"%s\":%d S0 record couldn't be found.\n",
            &hexmrg_glob.appName[0], hexmrg_glob.currLine);
         return(301);
      }
      
      if (hexmrg_glob.mrgType == SREC_MERGE)
      {
         /* Read the line with app length, update length and checksum */
         ret_p = fgets(&dataBuf[0], 255, appFile_p);
         if ((ret_p == NULL) || (dataBuf[0] != 'S') || (dataBuf[1] != '1') ||
            (dataBuf[8] != 'F') || (dataBuf[9] != 'F') || (dataBuf[10] != 'F') ||
            (dataBuf[11] != 'F') || (dataBuf[12] != 'F') || (dataBuf[13] != 'F') ||
            (dataBuf[14] != 'F') || (dataBuf[15] != 'F'))
         {
            printf("App file \"%s\":%d app length record couldn't be found or not empty.\n",
               &hexmrg_glob.appName[0], hexmrg_glob.currLine);
            return(302);
         }

         /* Update the app length record */
         retVal = hexmrg_update_srecord_length_line(length, &dataBuf[0]);
         if (retVal)
         {
            printf("App file \"%s\":%d couldn't update app length record.\n",
               &hexmrg_glob.appName[0], hexmrg_glob.currLine);
            return(303);
         }
         fprintf(outFile_p, "%s", &dataBuf[0]);
         hexmrg_calculate_crc32(&dataBuf[0], strlen(&dataBuf[0]),
               &hexmrg_glob.imageCrc);
      }
   }
   
   /* Copy the rest of the app file into the out file */
   endFile = FALSE;
   while (!endFile)
   {
      ret_p = fgets(&dataBuf[0], 255, appFile_p);
      if (ret_p == NULL)
      {
         printf("App file \"%s\":%d ended prematurely.\n",
            &hexmrg_glob.appName[0], hexmrg_glob.currLine);
         return(304);
      }
      retVal = hexmrg_verify_hex_line(&dataBuf[0], &outBuf[0], &addr,
         &len, &endFile, &hexmrg_glob.appName[0]);
      if (retVal)
      {
         /* Error messages already output */
         return(305);
      }
      /* Check if this is an extended address to config bits cmd */
      if ((addr == CFG_MEM_ADDR) && (len == 0))
      {
         /* Found the first config msg, update upper addr bits. */
         inputBuf[0] = ((startAddr + length) >> 24) & 0xff;
         inputBuf[1] = ((startAddr + length) >> 16) & 0xff;
         hexmrg_create_hex_line(EXT_ADDR_LEN, DATA_CMD, EXT_ADDR_CMD,
            &inputBuf[0], &outBuf[0]);
         fprintf(outFile_p, "%s", &outBuf[0]);
         hexmrg_calculate_crc32(&outBuf[0], strlen(&outBuf[0]),
            &hexmrg_glob.imageCrc);
         
         /* Stuff in crc here. */
         inputBuf[0] = crc8;
         inputBuf[1] = MAGIC_NUM;
         hexmrg_create_hex_line(2, (startAddr + length) & 0xffff, DATA_CMD,
            &inputBuf[0], &outBuf[0]);
         fprintf(outFile_p, "%s", &outBuf[0]);
         hexmrg_calculate_crc32(&outBuf[0], strlen(&outBuf[0]),
            &hexmrg_glob.imageCrc);
      }
      
      /* Check for the S9 record that marks the end of the S-Record file */
      if ((hexmrg_glob.mrgType == SREC_MERGE) && endFile)
      {
         /* Stuff in crc here. */
         inputBuf[0] = crc8;
         inputBuf[1] = MAGIC_NUM;
         hexmrg_create_srecord_line(2, startAddr + length, 1,
            &inputBuf[0], &dataBuf[0]);
      }
      else if ((hexmrg_glob.mrgType == SREC_CREATE_CRC) && endFile)
      {
         /* Stuff in crc here. */
         inputBuf[0] = (hexmrg_glob.appCrc >> 24) & 0xff;
         inputBuf[1] = (hexmrg_glob.appCrc >> 16) & 0xff;
         inputBuf[2] = (hexmrg_glob.appCrc >> 8) & 0xff;
         inputBuf[3] = hexmrg_glob.appCrc & 0xff;
         hexmrg_create_srecord_line(4, startAddr + length, 3,
            &inputBuf[0], &outBuf[0]);
         fprintf(outFile_p, "%s", &outBuf[0]);
         hexmrg_glob.currLine++;

         /* Allow program to output original ending record */
      }
      
      /* Copy the data into the output file */
      fprintf(outFile_p, "%s", &dataBuf[0]);
      if ((hexmrg_glob.mrgType == HEX_MERGE) || (hexmrg_glob.mrgType == SREC_MERGE))
      {
         hexmrg_calculate_crc32(&dataBuf[0], strlen(&dataBuf[0]),
            &hexmrg_glob.imageCrc);
      }
      hexmrg_glob.currLine++;
   }
   return(0);
} /* End hexmrg_copy_app_to_output */

/*
* ===============================================================================
* 
* Name: hexmrg_create_hex_line
* 
* ===============================================================================
*/
/**
* Create hex data line
* 
* @param   length    [in]  number of characters to convert 
* @param   addr      [in]  address of data 
* @param   cmd       [in]  command to be converted
* @param   data_p    [in]  data
* @param   outStr_p  [out] output string
* @return  None
* 
* @pre     None
* @note    None 
* 
* ===============================================================================
*/
void hexmrg_create_hex_line(
   U8                      length,
   U16                     addr,
   U8                      cmd,
   U8                      *data_p,
   U8                      *outStr_p)
{
   INT                     index;
   U8                      checkSum;
   
   /* Write initial char */
   outStr_p[0] = ':';
   checkSum = 0;
   
   /* Write length of cmd */
   checkSum += length;
   hexmrg_create_hex_field(length, 1, &outStr_p[1]);
    
   /* Write addr */
   checkSum += (addr >> 8) + (addr & 0xff);
   hexmrg_create_hex_field(addr, 2, &outStr_p[3]);

   /* Write cmd */
   checkSum += cmd;
   hexmrg_create_hex_field(cmd, 1, &outStr_p[7]);
   
   /* Write the data to the output line */
   for (index = 0; index < length; index++)
   {
      checkSum += data_p[index];
      hexmrg_create_hex_field(data_p[index], 1, &outStr_p[(index * 2) + 9]);
   }
   
   /* Calculate the checksum and stuff in the output string */
   checkSum = -checkSum;
   hexmrg_create_hex_field(checkSum, 1, &outStr_p[(length * 2) + 9]);

   /* Place \n and null termination on string */
   outStr_p[(length * 2) + 11] = '\r';
   outStr_p[(length * 2) + 12] = '\n';
   outStr_p[(length * 2) + 13] = 0;
} /* End hexmrg_create_hex_line */

/*
* ===============================================================================
* 
* Name: hexmrg_update_srecord_length_line
* 
* ===============================================================================
*/
/**
* Update S-Record length line
* 
* @param   length    [in]      length of the application 
* @param   data_p    [in/out]  initial string
* @return  None
* 
* @pre     None
* @note    None 
* 
* ===============================================================================
*/
BOOL hexmrg_update_srecord_length_line(
   U32                     length,
   U8                      *data_p)
{
   INT                     index;
   U8                      lineLen;
   U8                      checkSum;
   U8                      tmpVal[255];
   BOOL                    retVal;
   U8                      test1;
   U8                      testData[255];
   
   /* Update the length within the string */
   hexmrg_create_hex_field(length, 4, &data_p[8]);
   
   /* Read the length of the line */
   retVal = hexmrg_convert_ascii_to_hex(&data_p[2], 1, &lineLen);
   if (retVal)
   {
      printf("File \"%s\":%d line length field invalid.\n", &hexmrg_glob.appName[0],
         hexmrg_glob.currLine);
      printf("Error line = \"%s\"\n", data_p);
      return (TRUE);
   }

   /* Convert the ascii chars to hex */
   retVal = hexmrg_convert_ascii_to_hex(&data_p[4], lineLen - 1, &tmpVal[0]);
   if (retVal)
   {
      /* Convert ascii to hex failed */
      printf("File \"%s\":%d convert ascii to hex failed.\n", &hexmrg_glob.appName[0],
         hexmrg_glob.currLine);
      printf("Error line = \"%s\"\n", data_p);
      return (TRUE);
   }
   
   /* Calculate the checksum and stuff in the output string */
   for (index = 0, checkSum = lineLen; index < lineLen - 1; index++)
   {
      checkSum += tmpVal[index];
   }
   checkSum = -checkSum;
   checkSum--;
   hexmrg_create_hex_field(checkSum, 1, &data_p[(lineLen * 2) + 2]);
   
   /* Verify the checksum */
   for (index = 0, checkSum = test1; index < test1 - 1; index++)
   {
      checkSum += testData[index];
   }
   checkSum = -checkSum;
   checkSum--;
   
   return (FALSE);
} /* End hexmrg_update_srecord_length_line */

/*
* ===============================================================================
* 
* Name: hexmrg_create_srecord_line
* 
* ===============================================================================
*/
/**
* Create S-record data line
* 
* @param   length    [in]  length of data to be converted 
* @param   addr      [in]  address 
* @param   cmd       [in]  command (0 = header, 1 = data, 3 = 4 byte addr data)
* @param   data_p    [in]  data
* @param   outStr_p  [out] output string
* @return  None
* 
* @pre     None
* @note    None 
* 
* ===============================================================================
*/
void hexmrg_create_srecord_line(
   U8                      length,
   U32                     addr,
   U8                      cmd,
   U8                      *data_p,
   U8                      *outStr_p)
{
   INT                     index;
   U8                      checkSum;
   
   /* Write initial char */
   outStr_p[0] = 'S';
   outStr_p[1] = cmd + '0';
   
   /* Write length of cmd */
   if (cmd != 3)
   {
      checkSum = length + 3;
      hexmrg_create_hex_field(length + 3, 1, &outStr_p[2]);

      /* Write addr */
      checkSum += ((addr >> 8) & 0xff) + (addr & 0xff);
      hexmrg_create_hex_field(addr, 2, &outStr_p[4]);
   }
   else
   {
      checkSum = length + 5;
      hexmrg_create_hex_field(length + 5, 1, &outStr_p[2]);

      /* Write addr */
      checkSum += ((addr >> 24) & 0xff) + ((addr >> 16) & 0xff) +
            ((addr >> 8) & 0xff) + (addr & 0xff);
      hexmrg_create_hex_field(addr, 4, &outStr_p[4]);
   }

   /* Write the data to the output line */
   for (index = 0; index < length; index++)
   {
      checkSum += data_p[index];
      if (cmd != 3)
      {
         hexmrg_create_hex_field(data_p[index], 1, &outStr_p[(index * 2) + 8]);
      }
      else
      {
         hexmrg_create_hex_field(data_p[index], 1, &outStr_p[(index * 2) + 12]);
      }
   }
   
   /* Calculate the checksum and stuff in the output string */
   checkSum = -checkSum;
   checkSum--;
   if (cmd != 3)
   {
      index = (length * 2) + 8;
      hexmrg_create_hex_field(checkSum, 1, &outStr_p[index]);
   }
   else
   {
      index = (length * 2) + 12;
      hexmrg_create_hex_field(checkSum, 1, &outStr_p[index]);
   }
   index += 2;

   /* Place \n and null termination on string */
   outStr_p[index++] = '\r';
   outStr_p[index++] = '\n';
   outStr_p[index++] = 0;
   
} /* End hexmrg_create_srecord_line */

/*
* ===============================================================================
* 
* Name: hexmrg_create_hex_field
* 
* ===============================================================================
*/
/**
* Create hex field
* 
* @param   data      [in]  data to be converted 
* @param   length    [in]  length of data (in bytes) to be converted 
* @param   outStr_p  [out] output string_p
* @return  None
* 
* @pre     None
* @note    None 
* 
* ===============================================================================
*/
void hexmrg_create_hex_field(
   U32                     data,
   UINT                    length,
   U8                      *outStr_p)
{
   UINT                    index;
   U8                      currNibble;                    
      
   for (index = 0; index < (length * 2); index++)
   {
      currNibble = (data >> (((length * 2) - 1 - index) * 4) & 0xf);
      if (currNibble >= 10)
      {
         outStr_p[index] = (currNibble - 10) + 'A';
      }
      else
      {
         outStr_p[index] = currNibble + '0';
      }
   }
} /* End hexmrg_create_hex_field */

/*
* ===============================================================================
* 
* Name: hexmrg_calculate_crc32
* 
* ===============================================================================
*/
/**
* Create hex field
* 
* @param   data_p    [in]  ptr to data to be CRC'd 
* @param   length    [in]  length of data (in bytes) to be CRC'd 
* @param   crc_p     [in/out] ptr to interim CRC value
* @return  None
* 
* @pre     None
* @note    None
*
* ===============================================================================
*/
void hexmrg_calculate_crc32(
   U8                      *data_p,
   UINT                    length,
   U32                     *crc_p)
{
   UINT                    index;
   U32                     currCrc;

   currCrc = *crc_p;
   for (index = 0; index < length; index++, data_p++)
   {
      currCrc = (currCrc >> 8) ^ HEXMRG_CRC32_LOOKUP[(currCrc & 0xff) ^ (*data_p)];
   }
   *crc_p = currCrc;
} /* End hexmrg_calculate_crc32 */
