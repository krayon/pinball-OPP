;/*
; *===============================================================================
; *
; *                          HHHHH            HHHHH
; *                           HHH     SSSS     HHH
; *                           HHH   SSSSSSSS   HHH 
; *                           HHH  SSS    SSS  HHH       Hugh Spahr
; *                           HHH SSS      SSS HHH       Utilities
; *                           HHH  SSS         HHH
; *                           HHH    SSSS      HHH
; *                           HHHHHHHHHHHHHHHHHHHH
; *                           HHHHHHHHHHHHHHHHHHHH
; *                           HHH         SSS  HHH
; *                           HHH SSS      SSS HHH
; *                           HHH  SSS    SSS  HHH
; *                           HHH   SSSSSSSS   HHH
; *                           HHH     SSSS     HHH
; *                          HHHHH            HHHHH
; *
; *===============================================================================
; */
;/**
; * @file:   bootload.app.asm
; * @author: Hugh Spahr
; * @date:   6/12/2008
; *
; * @note:    Copyright© 2008, Hugh Spahr
; *
; *  This program is free software: you can redistribute it and/or modify
; *  it under the terms of the GNU General Public License as published by
; *  the Free Software Foundation, either version 3 of the License, or
; *  (at your option) any later version.
; *
; *  This program is distributed in the hope that it will be useful,
; *  but WITHOUT ANY WARRANTY; without even the implied warranty of
; *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; *  GNU General Public License for more details.
; *
; *  You should have received a copy of the GNU General Public License
; *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
; *
; *===============================================================================
; */
; The 8-bit Freescale bootloader should be less than 0x200 bytes in length because
; that is the size of the flash sector size.  Too bad I can't fit it in that size
; and guarantee integrity of the code.  It currently uses 0x400 bytes.
; The bootloader uses the first byte of RAM to force the program to stay in the
; bootloader on the next reset. This is how the application can force a download.
;
; Bootloader is a simple command/acknowledge protocol.  All the smarts and timeouts
; are on the host to keep the bootloader as simple as possible.  If a command needs
; to be cancelled a string of STX bytes can be sent to clear the current command.
;
; Memory Map
;   -------------------   Application (Start of flash to 0xfc00)
;   |  offset = 0x00  |   Length of application (4 bytes)
;   |  offset = 0x04  |   Remapped vector table (3 bytes per vector for jmp inst)
;   |  offset = 0x61  |   Re-mapped reset vector (start of application address)
;   |  offset = 0x64  |   Remaining application
;   |      ...        |
;   |offset = appLen  |   App CRC (Start of flash + appLength)
;   |offset = appLen+1|   End marker (Start of flash + appLength + 1) 0xa5
;   -------------------   Bootloader (0xfc00)
;   |    0xffc0       |   Boot intrpt vectors, point to remapped vector table
;   |    0xfffe       |   Boot vector (goes to boot start address)
;   -------------------
;
; Definitions:
;
;   STX      -   Start of packet indicator (0x5a)
;   DATA     -   General data up to 8 bytes
;   COMMAND  -   Base command
;   ADDR     -   Address (24 bits for Flash, 16 bits for EEPROM)
;   DATA     -   Data (8 bytes for Flash, 1 byte for EEPROM)
;   CRC8     -   Only valid if write to Flash or EEPROM
;
; Commands:
;
;    WR_FLASH   0x00   Write Program Memory
;    RD_FLASH   0x01   Read Program Memory
;    WR_EE      0x02   Write EEDATA Memory (not implemented in freescale)
;    RD_EE      0x03   Read EEDATA Memory (not implemented in freescale)
;    WR_CFG     0x04   Write config bits (not implemented)
;    Boot_Ver   0x05   Get boot version (Must be last command)
;
; *****************************************************************************
; Include derivative-specific definitions

  IF DEBUG == 1

  ROMStart:             equ $00008000
  RAMEnd:               equ $0000047F

  SCIBDL:               equ $00000039           ;*** SCIBDL - SCI Baud Rate Register Low ***
  SCIC1:                equ $0000003a           ;*** SCIC1 - SCI Control Register 1 ***
  SCIC2:                equ $0000003b           ;*** SCIC2 - SCI Control Register 2 ***
  SCID:                 equ $0000003f           ;*** SCID - SCI Data Register ***
  ICSC1:                equ $00000048           ;*** ICSC1 - ICS Control Register 1; 0x00000048 ***
  ICSC2:                equ $00000049           ;*** ICSC2 - ICS Control Register 2; 0x00000049 ***
  ICSTRM:               equ $0000004a           ;*** ICSTRM - ICS Trim Register; 0x0000004A ***
  ICSSC:                equ $0000004b           ;*** ICSSC - ICS Status and Control Register; 0x0000004B ***
  SOPT1:                equ $00001802           ;*** SOPT1 - System Options Register 1 ***
  FCDIV:                equ $00001820           ;*** FCDIV - FLASH and EEPROM Clock Divider Register; 0x00001820 ***
  NVTRIM:               equ $0000ffaf           ;*** NVTRIM - Trim value for internal osc ***
  NVFTRIM:              equ $0000ffae           ;*** NVFTRIM - Fine trim value for internal osc ***

  ; Application information/addresses
  NON_VOL_REG_ADDR:     equ $0000ffae
  INT_VECT_TBL_ADDR:    equ $0000ffc0
  APP_START_ADDR:       equ ROMStart
  APP_LENGTH_ADDR:      equ APP_START_ADDR
  APP_VECT_TBL_OFF:     equ 16
  APP_VECT_TBL_ADDR:    equ APP_START_ADDR + APP_VECT_TBL_OFF
  BYTES_PER_VECT_ENTRY: equ 3
  BOOTLOAD_ADDR:        equ $0000fc10
  BOOT_SECT_ADDR:       equ $0000fc00

  ORG    BOOTLOAD_ADDR
          
;/*
; * ===============================================================================
; * 
; * Name: start_boot
; * 
; * ===============================================================================
; */
;/**
; * Start the bootloader
; * 
; * This code is only used if the DEBUG flag is set to 1.  Initialize the stack
; * ptr, and setup the processor clock for MCGOUT = 16 MHz, busclk = 8 MHz.
; * Initialize the flash clock and setup serial port for 19.2 kbps, 8, N, 1.
; * Enable the serial port, and jump to the application.
; * 
; * @param   None 
; * @return  None
; * 
; * @pre     None 
; * @note    None
; * 
; * ===============================================================================
; */
_start_boot:                ; Setup the serial port to be 19.2, 8, N, 1
      sei                   ; Disable all interrupts
      
      ; Fill out the SOPT1 register (so PTA5 is IRQ, not reset)
      lda     #$46          ; Set up debug pins, COP timer is 32ms
      sta     SOPT1
      
      ldhx    #RAMEnd+1     ; initialize the stack pointer
      txs
      
      ; Load the trim value and store
      lda     NVTRIM
      sta     ICSTRM
      lda     NVFTRIM
      sta     ICSSC
      
      ; Set up clock for processor, ICSOUT = 32.00 MHz, BusClk = 16.00 MHz
      clr     ICSC2         ; Change BDIV[0:1] to 00
      clr     ICSC1         ; 
      lda     #$04          ; initialize FEI
      sta     ICSC1
      
      lda     #$49          ; initialize flash clock register, 200 KHz
      sta     FCDIV

      mov     #52, SCIBDL   ; Set baud = 16.00 MHz/(16 * 19200) = 52
      clr     SCIC1         ; Normal op, 8, N, 1
      mov     #$0c, SCIC2   ; Xmt/Rcv enable
      
      lda     SCID          ; Clear rcv data reg flag if set
      jmp     APP_VECT_TBL_ADDR + ($1f * BYTES_PER_VECT_ENTRY)

  ;**************************************************************
  ;*            Non-volatile Registers                          *
  ;**************************************************************
      org   NON_VOL_REG_ADDR
      dc.b  $ff                   ; FTRIM bit
      dc.b  $ff                   ; TRIM value
      dc.b  $ff, $ff, $ff, $ff, $ff, $ff, $ff, $ff  ; NVBACKKEY
      dc.b  $ff, $ff, $ff, $ff, $ff ; Reserved
      dc.b  $ff                   ; NVPROT, no eeprom/flash protection
      dc.b  $ff                   ; Reserved
      dc.b  $c2                   ; NVOPT, unsecure
            
  ;**************************************************************
  ;*                 Non-volatile info                          *
  ;**************************************************************
  IF SET_NONVOL == 1
  
      org   BOOT_SECT_ADDR
      
      dc.l  $ffffffff   ;Serial number
      dc.l    1000200   ;Product ID
      dc.l  $ffffffff   ;Reserved
      dc.l  $ffffffff   ;Reserved
      
  ENDIF
  
  ;**************************************************************
  ;*                 Interrupt Vectors                          *
  ;**************************************************************
      org   INT_VECT_TBL_ADDR

      dc.w  APP_VECT_TBL_ADDR
      dc.w  APP_VECT_TBL_ADDR + BYTES_PER_VECT_ENTRY
      dc.w  APP_VECT_TBL_ADDR + ($02 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($03 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($04 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($05 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($06 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($07 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($08 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($09 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($0a * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($0b * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($0c * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($0d * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($0e * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($0f * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($10 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($11 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($12 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($13 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($14 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($15 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($16 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($17 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($18 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($19 * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($1a * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($1b * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($1c * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($1d * BYTES_PER_VECT_ENTRY)
      dc.w  APP_VECT_TBL_ADDR + ($1e * BYTES_PER_VECT_ENTRY)
      dc.w  _start_boot
      
  ENDIF