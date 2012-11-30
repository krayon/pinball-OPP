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
; *
; * @file:     HCS08MiniBoot.asm
; * @author:   Hugh Spahr
; * @date:     1/23/2009
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
; !!! Note !!! The APP_START_ADDR is passed in to the assembler using -D
; !!! Note !!! The RAM_END is passed in to the assembler using -D

SCI1BDL:            equ    $00000039           ;*** SCI1BDL - SCI1 Baud Rate Register Low ***
SCI1C1:             equ    $0000003a           ;*** SCI1C1 - SCI1 Control Register 1 ***
SCI1C2:             equ    $0000003b           ;*** SCI1C2 - SCI1 Control Register 2 ***
SCI1S1:             equ    $0000003c           ;*** SCI1S1 - SCI1 Status Register 1 ***
SCI1S1_OR:          equ    3                   ; Receiver Overrun Flag
SCI1S1_RDRF:        equ    5                   ; Receive Data Register Full Flag
SCI1S1_TDRE:        equ    7                   ; Transmit Data Register Empty Flag

SCI1D:              equ    $0000003f           ;*** SCI1D - SCI1 Data Register ***
ICSC1:              equ    $00000048           ;*** ICSC1 - ICS Control Register 1 ***
ICSC2:              equ    $00000049           ;*** ICSC2 - ICS Control Register 2 ***
ICSTRM:             equ    $0000004a           ;*** ICSTRM - ICS Trim Register ***
ICSSC:              equ    $0000004b           ;*** ICSSC - ICS Status and Control Register ***

SRS:                equ    $00001800           ;*** SRS - System Reset Status ***
SOPT1:              equ    $00001802           ;*** SOPT1 - System Options Register 1 ***

FCDIV:              equ    $00001820           ;*** FCDIV - FLASH and EEPROM Clock Divider Register ***
FSTAT:              equ    $00001825           ;*** FSTAT - FLASH and EEPROM Status Register ***
mFSTAT_FCCF:        equ    %01000000
mFSTAT_FCBEF:       equ    %10000000
FCMD:               equ    $00001826           ;*** FCMD - FLASH and EEPROM Command Register ***

NVTRIM:             equ    $0000ffaf           ;*** NVTRIM - Trim value for internal osc ***
NVFTRIM:            equ    $0000ffae           ;*** NVFTRIM - Fine trim value for internal osc ***

; Application information/addresses
NON_VOL_REG_ADDR:     equ $0000ffae
INT_VECT_TBL_ADDR:    equ $0000ffc0
APP_LENGTH_ADDR:      equ APP_START_ADDR
APP_VECT_TBL_OFF:     equ 16
APP_VECT_TBL_ADDR:    equ APP_START_ADDR + APP_VECT_TBL_OFF
BYTES_PER_VECT_ENTRY: equ 3
BYTES_INT_VECT:       equ $20
APP_ENTRY_ADDR:       equ APP_VECT_TBL_ADDR + ((BYTES_INT_VECT - 1) * BYTES_PER_VECT_ENTRY)

BOOTLOAD_ADDR         equ $0000fc20

; Message constants
STX                   equ $5a   ; used for start of transmission
MAGIC_NUM             equ $a5   ; magic number written at last location in EEPROM
                                ;    to force the bootloader not to jump to the app

; Message rcv/xmt buffer
MAGIC_NUM_LOC         equ $80   ; Either magic number to stay in boot, or 0
MSG_BUF_STX           equ $81   ; Always contains an STX for transmission
MSG_BUFF              equ $82   ; Rcv or xmt buffer
MSG_BUF_CMD           equ $82   ; Rcv/xmt command
MSG_BUF_HI            equ $83   ; MSB of addr
MSG_BUF_MID           equ $84   ; Middle byte of addr
MSG_BUF_LO            equ $85   ; LSB of addr

MSG_BUF_FL_DATA       equ $86   ; Data location in flash msg
MSG_BUF_FL_CRC8       equ $8e   ; CRC8 location in flash msg

; Registers and variables
COUNTER               equ $90   ; General counter
CRC8                  equ $91   ; Result of CRC8 calculation
SCRATCH_PAD           equ $92
CURR_BYTE             equ $93
TMP_VAL1              equ $94
CLEAR_STACK           equ $95

; Location of code size to see if it is valid
CODE_SIZE2            equ $96
CODE_SIZE3            equ $97
RAM_BUF_ADDR          equ $98   ; Location to temporarily copy EEPROM sector/flash data


CRC8_TABLE            equ $a0   ; CRC8 lookup table for speed
CMD_SZ_LKUP           equ $b0   ; Lookup table with length of rcv msgs.

;
; export symbols
;
            XDEF _start_boot
            ABSENTRY _start_boot

            ORG    BOOTLOAD_ADDR
; Boot message sent when connecting, or response to get boot revision
boot_version:
  dc.b "Boot0.0"                ; 8 byte CRC message that has bootloader rev
  dc.b $0d                      ;    Note: host looks for this string to verify connect
  
; Note: The follow constants must be one after another because they
;    are copied into the file registers in a single loop.
; CRC8 lookup table to do CRC a nibble at a time
crc8_lookup_table:
  dc.b $00, $07, $0e, $09, $1c, $1b, $12, $15
  dc.b $38, $3f, $36, $31, $24, $23, $2a, $2d
; Num bytes in rcv msg after cmd byte
rcv_cmd_sz:
  dc.b $0c, $03, $04, $02, $03

;/*
; * ===============================================================================
; * 
; * Name: write_to_flash_or_eeprom
; * 
; * ===============================================================================
; */
;/**
; * Write eight bytes to flash or EEPROM
; * 
; * Index register has the source address.  Accumulator has the destination RAM
; * address.
; * 
; * @param   index      [in]  source address
; * @param   SP         [in]  destination in RAM
; * @return  None
; * 
; * @pre     None
; * @note    This function runs out of RAM.
; * ===============================================================================
; */
write_to_flash_or_eeprom:
      mov      #8, COUNTER       ; Going to store 8 bytes
loop7:
      pshh
      pshx
      clrh
      ldx      SCRATCH_PAD
      lda      , x               ; Grab data byte
      pulx
      pulh
      sta      , x               ; Latch flash address/data
      lda      #$25              ; Burst write cmd
      sta      FCMD
      lda      #mFSTAT_FCBEF     ; Launch the burst write cmd
      sta      FSTAT
loop8:
      bsr      pet_watchdog
      lda      FSTAT
      bpl      loop8             ; Loop if FCBEF is clear
      incx
      inc      SCRATCH_PAD
      dec      COUNTER
      bne      loop7
      bra      flash_cmd_done    ; Use rts from flash cmd done

;/*
; * ===============================================================================
; * 
; * Name: pet_watchdog
; * 
; * ===============================================================================
; */
;/**
; * Give the watchdog a bone
; * 
; * @param   None 
; * @return  None
; * 
; * @pre     None
; * @note    None
; * 
; * ===============================================================================
; */
pet_watchdog:
      psha
      lda     #$55
      sta     SRS
      coma
      sta     SRS
      pula
      rts
      
;/*
; * ===============================================================================
; * 
; * Name: send_prog_cmd
; * 
; * ===============================================================================
; */
;/**
; * Send a program command to the flash or EEPROM and wait for it to complete
; * 
; * @param   cmd       [in] command sent to the FCMD register is in the accumulator
; * @return  None
; * 
; * @pre     None
; * @note    None
; * ===============================================================================
; */
send_prog_cmd:
      sta     FCMD
      lda     #mFSTAT_FCBEF      ; Launch the flash cmd
      sta     FSTAT
      
      ; *** NOTE: *** Falling through to flash cmd done code

;/*
; * ===============================================================================
; * 
; * Name: flash_cmd_done
; * 
; * ===============================================================================
; */
;/**
; * Wait for flash command done
; * 
; * Wait for flash command to be completed.  This is partially done to wait for
; * the four clock cycles before checking the FCCF bit
; * 
; * @param   None 
; * @return  None
; * 
; * @pre     None
; * @note    None
; * 
; * ===============================================================================
; */
flash_cmd_done:
      bsr     pet_watchdog
      lda     FSTAT
      lsla                      ; Move FCCF into msb
      bpl     flash_cmd_done    ; Loop if FCCF is clear
      rts
end_ram_code:
      
ram_write_to_flash_or_eeprom  equ   (write_to_flash_or_eeprom - crc8_lookup_table + CRC8_TABLE)
ram_send_prog_cmd             equ   (send_prog_cmd - crc8_lookup_table + CRC8_TABLE)
COPY_SIZE                     equ   (end_ram_code - crc8_lookup_table)

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
; * Disable interrupts, setup SOPT1, set the clocking registers.  Look for
; * a magic number at the beginning of RAM to force us to not jump to the
; * application.  (Clear the magic number so this condition is reset next boot).
; * Call calculate_code_crc8 to see if app CRC is correct.  If not print boot
; * message, otherwise jump to application.
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
      
      ldhx    #RAM_END+1    ; initialize the stack pointer
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

      mov     #52, SCI1BDL  ; Set baud = 16.00 MHz/(16 * 19200) = 52
      clr     SCI1C1        ; Normal op, 8, N, 1
      mov     #$0c, SCI1C2  ; Xmt/Rcv enable
      
      lda     SCI1D         ; Clear rcv data reg flag if set
      bclr    0, CLEAR_STACK; Mark stack as not needing cleared
      lda     #STX          ; Store STX in STX msg position
      sta     MSG_BUF_STX
            
      ; Fill out the CRC8 lookup table
      ldhx    #crc8_lookup_table
      mov     #COPY_SIZE, COUNTER          ; Going to store
      mov     #CRC8_TABLE, SCRATCH_PAD     ; Address to move data
      jsr     copy_to_ram

      lda     MAGIC_NUM_LOC
      eor     #MAGIC_NUM
      beq     clear_magic_num
      
      jsr     calculate_code_crc8  ; Accumulator contains 0 if CRC8 is correct
      bne     print_boot_hdr
      jmp     APP_VECT_TBL_ADDR + ($1f * BYTES_PER_VECT_ENTRY)

;/*
; * ===============================================================================
; * 
; * Name: print_boot_hdr
; * 
; * ===============================================================================
; */
;/**
; * Print boot header message
; * 
; * Print boot header message which contains the boot revision.  FSR0 contains
; *   buffer to be sent, and W reg contains length of msg.
; * 
; * @param   None 
; * @return  None
; * 
; * @pre     None
; * @note    None
; * 
; * ===============================================================================
; */
print_boot_hdr:
      lda     #8                   ; Boot msg is 8 chars long
      ldhx    #boot_version        ; Setup pointer to buffer area
      jmp     write_spec_packet

;/*
; * ===============================================================================
; * 
; * Name: clear_magic_num
; * 
; * ===============================================================================
; */
;/**
; * Clear magic number in RAM
; * 
; * Clear the magic number at end of RAM so next reset checks the application CRC.
; * Jump to look_for_stx to look for the next cmd.
; * 
; * @param   None 
; * @return  None
; * 
; * @pre     Index register must be set to the end of EEPROM
; * @note    Waits for write to be completed before continuing.
; * 
; * ===============================================================================
; */
clear_magic_num:
      clr     MAGIC_NUM_LOC
      bra     look_for_stx
      
;/*
; * ===============================================================================
; * 
; * Name: look_for_stx
; * 
; * ===============================================================================
; */
;/**
; * Look for STX command
; * 
; * Call read_rs232 to wait for next byte to be STX.  After a single STX is
; * received, discard the next received STX bytes until a valid command is found.
; * If the msb of the command is set, reset the PIC to see if app is valid.
; * If the command is the last command (Boot_Ver), jump to print_boot_hdr.
; * Otherwise verify the cmd is valid and lookup the number of bytes that should
; * be received for this command.  Loop waiting for these bytes.  Use a jump table
; * to jump to the correct processing.
; * 
; * @param   None 
; * @return  None
; * 
; * @pre     None
; * @note    None
; * 
; * ===============================================================================
; */
look_for_stx:
      ldhx    #MSG_BUFF
      jsr     read_rs232         ; Get <STX>
      eor     #STX
      bne     look_for_stx       ; Otherwise go back for another character

look_for_cmd:
      ldhx    #MSG_BUFF          ; Now we rcvd STX, eat them up until rcv a cmd
      jsr     read_rs232         ; Get cmd or stx
      eor     #STX
      beq     look_for_cmd       ; if STX keep looking for a cmd
                                 ; MSG_BUF_CMD contains the command

      brclr   7, MSG_BUF_CMD, label1  ; if 0x80 set, done programming
         dc.b $8d                ; Reset the processor
label1:
      lda     MSG_BUF_CMD
      sub     #5                 ; Cmds 0-5 are valid
      beq     print_boot_hdr     ; If 5, print version (always last command)
      bgt     look_for_stx       ; Cmd > 5, so bad cmd, look for new cmd

      clrh
      ldx     MSG_BUF_CMD
      lda     CMD_SZ_LKUP, x     ; Compute number of bytes we should rcv
      sta     COUNTER            ; Counter now has number of bytes to rcv
      ldhx    #MSG_BUF_HI
      
rcv_cmd_loop:
      jsr     read_rs232
      dec     COUNTER
         bne  rcv_cmd_loop       ; Not finished then repeat

      clrh
      ldx     MSG_BUF_CMD        ; Calculate offset into jump table
      lslx
      jmp     jump_table, x      ; Jump

jump_table:
      bra     write_prog_mem
      bra     read_prog_mem
      bra     look_for_stx       ; write_ee not implemented for freescale mini boot
      bra     look_for_stx       ; read_ee not implemented for freescale mini boot
      bra     look_for_stx       ; write_cfg_mem not implemented for freescale

      
;/*
; * ===============================================================================
; * 
; * Name: write_prog_mem
; * 
; * ===============================================================================
; */
;/**
; * Write program memory
; * 
; * Verify that address is above the bootloader.  Verify the CRC8 is correct.
; * Jump to look_for_stx if either of these errors occur.  If this write is
; * on a 0x200 byte boundary, erase the flash memory first.  Write the data
; * to the flash memory.  Jump to write_packet to send the response.
; * 
; * @param   flashAddr [in] first three bytes after cmd in msg 
; * @param   flashData [in] next eight bytes
; * @param   CRC8      [in] last byte in msg
; * @return  None
; * 
; * @pre     None
; * @note    In:    <STX><0x00><ADDRU><ADDRH><ADDRL><DATA[0..7]><CRC8>
; *          Out:   <STX><0x00><ADDRU><ADDRH><ADDRL>
; *    All writes to flash must be 8 byte aligned.  This is guaranteed by the
; *    host and not checked here.  Top address byte (ADDRU) is not used.
; * ===============================================================================
; */
write_prog_mem:
      lda      MSG_BUF_MID       ; Insure not overwriting boot loader
      sub      #$fc              ; Addr 0xfc00 - 0xffff are boot locations
      bge      look_for_stx      ; Bad address so look for new cmd
      lda      #$0c              ; Number of bytes in the CRC8
      jsr      start_crc8
      lda      MSG_BUF_FL_CRC8   ; Grab rcvd CRC8
      eor      CRC8              ; W is 0 if CRC is correct
      bne      look_for_stx
      lda      MSG_BUF_LO        ; Check if this is on a sector boundary (0x300)
         bne   start_write_code  ; No erase needs to be done
      lda      MSG_BUF_MID       ; Check if 0x200 boundary
      and      #$01
      bne      start_write_code
      
      ldhx     MSG_BUF_MID
      sta      , x               ; Latch sector address
      lda      #$40              ; Sector erase
      jsr      ram_send_prog_cmd ; Send the command and wait for it to be done
      
start_write_code:
      ldhx     MSG_BUF_MID       ; Set up to write to flash
      mov      #MSG_BUF_FL_DATA, SCRATCH_PAD
      jsr      ram_write_to_flash_or_eeprom
      lda      #5                ; Response is 5 bytes long
      jmp      write_packet

;/*
; * ===============================================================================
; * 
; * Name: read_prog_mem
; * 
; * ===============================================================================
; */
;/**
; * Read program memory
; * 
; * Move address into index register.  Read the data from flash, calculate the
; * CRC8 and put in response msg. Jump to write_packet to send the response.
; * 
; * @param   flashAddr [in]  first three bytes after cmd in msg 
; * @param   flashData [out] next eight bytes
; * @param   CRC8      [out] last byte in msg
; * @return  None
; * 
; * @pre     None
; * @note    In:    <STX><0x01><ADDRU><ADDRH><ADDRL>
; *          Out:   <STX><0x01><ADDRU><ADDRH><ADDRL><DATA[0..7]><CRC8>
; * ===============================================================================
; */
read_prog_mem:
      ldhx     MSG_BUF_MID
      mov      #8, COUNTER       ; Going to store 8 bytes
      mov      #MSG_BUF_FL_DATA, SCRATCH_PAD  ; Address to move data
      jsr      copy_to_ram
      
      lda      #$0c              ; Number of bytes in the CRC8
      jsr      start_crc8
      mov      CRC8, MSG_BUF_FL_CRC8
      lda      #$0e              ; Response is 14 bytes long
      jmp      write_packet

;/*
; * ===============================================================================
; * 
; * Name: copy_to_ram
; * 
; * ===============================================================================
; */
;/**
; * Copy bytes to ram
; * 
; * Index register has the source address.  SCRATCH_PAD has the destination RAM
; * address.  COUNTER contains the number of bytes to copy.
; * 
; * @param   index      [in]  source address
; * @param   SCRATCH_PAD[in]  destination in RAM
; * @param   COUNTER    [in]  number of bytes to copy
; * @return  None
; * 
; * @pre     None
; * @note    None
; * ===============================================================================
; */
copy_to_ram:
      lda      , x               ; Grab data
      pshh
      pshx
      clrh
      ldx      SCRATCH_PAD
      sta      , x               ; Write data to msg
      pulx
      pulh
      aix      #1
      inc      SCRATCH_PAD
      dec      COUNTER
      bne      copy_to_ram
      rts

;/*
; * ===============================================================================
; * 
; * Name: write_packet, write_spec_packet
; * 
; * ===============================================================================
; */
;/**
; * Write standard packet or special packet response
; * 
; * Write standard packet which is located in MSG_BUF_STX in RAM.  Write
; * special packet is for sending the boot version message.  Call write_rs232
; * to send the bytes out the serial port.  Jump to look_for_stx to wait for
; * next cmd.
; * 
; * @param   numBytes [in] number of bytes in the message (in accumulator)
; * @param   msgLoc   [in] addr of msg buffer (only for special pkt, in index reg)
; * @return  None
; * 
; * \pre     None
; * \note    None
; * ===============================================================================
; */
write_packet:
      ldhx     #MSG_BUF_STX      ; Setup pointer to buffer area
write_spec_packet:
      sta      COUNTER
loop9:
      lda      , x               ; Send Data
      bsr      write_rs232
      incx
      dec      COUNTER
        bne    loop9
      jmp      look_for_stx

;/*
; * ===============================================================================
; * 
; * Name: write_rs232
; * 
; * ===============================================================================
; */
;/**
; * Write a byte to the RS232 port
; * 
; * Clear the watch dog timer.  Wait until transmit is available.  Send byte.
; * 
; * @param   txByte [in] Byte to transmit (in accumulator)
; * @return  None
; * 
; * @pre     None
; * @note    None
; * ===============================================================================
; */
write_rs232:
      jsr      pet_watchdog
        brclr  SCI1S1_TDRE, SCI1S1, write_rs232   ; Check if SCI1D is available
      sta      SCI1D
      rts

;/*
; * ===============================================================================
; * 
; * Name: read_rs232
; * 
; * ===============================================================================
; */
;/**
; * Read a byte from the RS232 port
; * 
; * Clear the watch dog timer.  Wait until a byte is received.  Copy byte into
; * index address and increment.
; * 
; * @param   None
; * @return  rxData [out] stored at index reg address
; * 
; * @pre     Index reg must be initialized to location to rcv byte.
; * @note    None
; * ===============================================================================
; */
read_rs232:
      jsr      pet_watchdog
      brclr    SCI1S1_OR, SCI1S1, label2        ; if overrun, reset the processor
         dc.b  $8d                              ; Reset the processor
label2:
      brclr    SCI1S1_RDRF, SCI1S1, read_rs232  ; wait for data from RS232
      mov      SCI1D, x+                        ; Grab the data and store in msg
      lda      SCI1D
      rts

;/*
; * ===============================================================================
; * 
; * Name: calculate_code_crc8
; * 
; * ===============================================================================
; */
;/**
; * Calculate code CRC8
; * 
; * Grab the code size out of flash.  If MSb is not clear, the app is not written
; * so return non-zero value.  First read the code chunk that is not a multiple of
; * 8 bytes.  Move the number of bytes into counter, and call move_to_crc_buff.
; *   If count is zero, compare the calculated CRC with the next location in program
; * memory.  If they match, return zero.  If count is nonzero, jump to
; * more_code_to_go.  Decrement code size count and call move_to_crc_buff.
; * 
; * @param   None
; * @return  Non-Zero if CRC8 not correct.
; *          Zero if CRC8 is correct.
; * 
; * @pre     None
; * @note    None
; * ===============================================================================
; */
calculate_code_crc8:
      ldhx     APP_START_ADDR + 2 ; Grab application code size (Start of Flash)
      sthx     CODE_SIZE2
      lda      APP_START_ADDR     ; Load the highest byte of the code size           

      beq      label3             ; If MSB of code size is 0, code size is filled out
        lda    #$55               ; Otherwise return non-zero value
        rts
      
label3:
      ldhx     #APP_START_ADDR    ; Start at beginning of the code
      mov      #$ff, CRC8         ; Put initial CRC8 in variable
      lda      CODE_SIZE3
      and      #$f8
      cbeq     CODE_SIZE3, code_size_mult_8   ; CODE_SIZE3 is on 8 byte boundary,
                                              ;    jump to multiple of 8 bytes
      psha                        ; Store CODE_SIZE3 with 3 lsbs cleared on stack
      eor      CODE_SIZE3         ; Gives us 3 ls bits
      sta      COUNTER            ; Move number of bytes into COUNTER
      bsr      move_to_crc_buff   ; Move memory to the CRC buffer
      pula                        ; Grab CODE_SIZE3 with 3 lsbs cleared from stack
      sta      CODE_SIZE3         ; save back to CODE_SIZE3
code_size_mult_8:                 ; Check if any more stuff to read
      jsr      pet_watchdog
      lda      CODE_SIZE2
      ora      CODE_SIZE3
      bne      more_code_to_go

      lda      , x                ; Check if CRC is correct
      eor      CRC8               ; Accumulator is 0 if CRC is correct
      rts

more_code_to_go:
      lda      CODE_SIZE3
      sub      #8
      bcc      label4             ; Jump over decrement if carry bit is clear
      dec        CODE_SIZE2
label4:
      sta      CODE_SIZE3
      mov      #8, COUNTER
      bsr      move_to_crc_buff   ; Move memory to the CRC buffer
      bra      code_size_mult_8

;/*
; * ===============================================================================
; * 
; * Name: start_crc8
; * 
; * ===============================================================================
; */
;/**
; * Start a CRC8
; * 
; * Load initial 0xff into the CRC8 register, and store the number of bytes for
; * the CRC8 in COUNTER rester.  Jump to the crc8_math_loop (it will perform the
; * rts.
; * 
; * @param   counter [in] number of byte to include in the CRC passed in accumulator
; * @return  CRC8 stored in register
; * 
; * @pre     None
; * @note    None
; * ===============================================================================
; */
start_crc8:
      sta      COUNTER               ; Store the counter
      ldhx     #MSG_BUFF             ; Grab the address of the data
      mov      #$ff, CRC8            ; Initial CRC8 value
      bra      crc8_math_loop        ; Branch to CRC8 routine

;/*
; * ===============================================================================
; * 
; * Name: move_to_crc_buff
; * 
; * ===============================================================================
; */
;/**
; * Move code to CRC buffer
; * 
; * Copy the code from flash memory to the CRC buffer.  Run the CRC calculation
; * on the CRC buffer.  CRC interim value is stored in the CRC variable.
; * 
; * @param   counter [in] number of byte to include in the CRC.
; * @param   addr    [in] address of flash
; * @return  Non-Zero if CRC8 not correct.
; *          Zero if CRC8 is correct.
; * 
; * @pre     Counter contains number of bytes in CRC.  Index registers contain the
; *          address of flash to read.
; * @note    None
; * ===============================================================================
; */
move_to_crc_buff:
      mov      COUNTER, TMP_VAL1     ; Save off the count for later
      mov      #RAM_BUF_ADDR, SCRATCH_PAD ; Address to move data
      jsr      copy_to_ram           ; Copy EEPROM bytes to RAM
      mov      TMP_VAL1, COUNTER     ; Copy the counter back from the scratch pad
      pshh                           ; Push the address onto the stack
      pshx
      bset     0, CLEAR_STACK        ; Mark stack as needing to be cleaned
      ldhx     #RAM_BUF_ADDR         ; Since data is in the buffer, start CRC
crc8_math_loop:                      ; Calculate the actual CRC8
      mov      , x+, CURR_BYTE       ; Store current byte in tmp area
      lda      CRC8
      nsa                            ; Essentially a shift left 4
      and      #$f0
      sta      TMP_VAL1
      lda      CRC8
      eor      CURR_BYTE
      nsa                            ; Essentially a shift right 4
      and      #$0f                  ; Accumulator contains lookup table index
      add      #CRC8_TABLE
      pshx                           ; Save buffer address on stack
      tax
      lda      , x
      eor      TMP_VAL1
      sta      CRC8
      nsa                            ; Essentially a shift left 4
      and      #$f0
      sta      TMP_VAL1
      lda      CRC8
      nsa                            ; Essentially a shift right 4
      and      #$0f
      eor      CURR_BYTE
      and      #$0f                  ; Accumulator contains lookup table index
      add      #CRC8_TABLE
      tax
      lda      , x
      pulx                           ; Restore buffer address on stack
      eor      TMP_VAL1
      sta      CRC8
      dec      COUNTER
         bne   crc8_math_loop        ; Not finished then repeat
      brclr    0, CLEAR_STACK, label6
         pulx                        ; Restore the stack if needed
         pulh
         bclr  0, CLEAR_STACK
label6:
      rts

  org   APP_START_ADDR + $10
app_start:

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
  dc.b  $62                   ; NVOPT, unsecure
            
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
  dc.w  _start_boot          ; Reset

  ;**************************************************************
  ;*                 Non-volatile info                          *
  ;**************************************************************
;  IF SET_NONVOL == 1
  
;BOOT_SECT_ADDR:       equ $0000fc00
;      org   BOOT_SECT_ADDR
      
;      dc.l       4747   ;Serial number
;      dc.l    1000200   ;Product ID
;      dc.l  $ffffffff   ;Reserved
;      dc.l  $ffffffff   ;Reserved
      
;  ENDIF
