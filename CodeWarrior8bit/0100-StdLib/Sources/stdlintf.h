/*
 *===============================================================================
 *
 *          SSSS
 *        SSSSSSSs                 DDD
 *       SSS    SSS     TTT        DDD            Hugh Spahr
 *      SSS  LLL SSS    TTT        DDD            Standard
 *       SSS LLL      TTTTTTT      DDD            Library
 *         SSSSL      TTTTTTT      DDD  
 *          SSSSS       TTT        DDD
 *           LSSSS      TTT    DDDDDDD
 *           LLLSSS     TTT  DDDDDDDDD
 *      SSS  LLL SSS    TTT DDD    DDD
 *       SSS LLLSSS     TTT DDD    DDD
 *        SSSSSSSS      TTT  DDDDDDDDD
 *          SSSS        TTT    DDDD DD
 *           LLL
 *           LLL   I    BBB
 *           LLL  III   BBB
 *           LLL   I    BBB
 *           LLL        BBB
 *           LLL  III   BBB
 *           LLL  III   BBB
 *           LLL  III   BBBBBBB
 *           LLL  III   BBBBBBBBB
 *           LLL  III   BBB    BBB
 *           LLL        BBB    BBB
 *           LLLLLLLLL  BBBBBBBBB
 *           LLLLLLLLL  BB BBBB
 *
 * @file:   stdlintf.c
 * @author: Hugh Spahr
 * @date:   6/10/2008
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
 * Interface file to the Standard Library.  It contains function
 *  prototypes and structures
 *
 *===============================================================================
 */
#ifndef STDLINTF_H
#define STDLINTF_H
 
#include "stdtypes.h"   /* include peripheral declarations */

/*
 * Generic structures/enumerations used for Standard Library.
 */
typedef enum
{
  STDLI_TOO_MANY_TICK_FUNCS = 0x01,
  STDLI_ILLEGAL_CB_FUNC     = 0x02,
  STDLI_BAD_NUM_TICKS       = 0x03,  
  STDLI_ADC_CHAN_REG_TWICE  = 0x04,
  STDLI_ADC_NO_CHAN_REG     = 0x05,
  STDLI_NO_EVENTS_AVAIL     = 0x06,
  STDLI_CAP_CHAN_PREV_CFG   = 0x07,
  STDLI_TIMER_NOT_CFG       = 0x08,
  STDLI_CAP_CHAN_NOT_CFG    = 0x09,
  STDLI_CAP_CUR_RUNNING     = 0x0a,
  STDLI_PWM_BAD_ON_COUNT    = 0x0b,
  STDLI_SW_ERROR            = 0x0c,
  STDLI_I2C_NOT_IDLE        = 0x0d,
} STDLI_ERR_E;

#define STDLI_CRITICAL_FAIL 0xf00

/* 
 * API for timing functions
 */
/* Timing interface structures/enumerations */
typedef enum
{
  TIMER_POLL                = 0x01,
  TIMER_FAST_OSC            = 0x02,
} STDLI_TIMER_E;

typedef struct
{
  U16                       usec;
  U16                       msec;
  U16                       sec;
} STDLI_TIMER_T;

typedef struct
{
  STDLI_TIMER_T             startTime;
  STDLI_TIMER_T             elapsedTime;  
} STDLI_ELAPSED_TIME_T;

#define STDLI_REPETITIVE_EVT          0x8000

typedef struct stdli_timer_s
{
  U16                       time;
  void                      (*timeout_fp)(U16 cbParm);
  U16                       cbParm;
  U16                       timeoutTicks; /* Filled by utility */
  struct stdli_timer_s      *next_p;      /* Filled by utility */
} STDLI_TIMER_EVENT_T;

/* To install timing functions, add INTRPT_TPM2_OVFL to POPULATED_INTS in
 *  projintrpts.h file.  Add the following lines to install the isr:
 *      interrupt void stdltime_timer2_isr(void);
 *      #define vector14 stdltime_timer2_isr
 * To install timing polled functions, call stdltime_start_timing_clock
 * with poll set to TRUE, and call stdltime_timer2_poll to poll interrupt.
 */
/* Timing function prototypes */
void stdltime_start_timing_clock(
  STDLI_TIMER_E             params);      /* TIMER_POLL or TIMER_FAST_OSC */
void stdltime_get_curr_time(
  STDLI_TIMER_T             *time_p);     /* ptr to returned current time struct */
void stdltime_get_elapsed_time(
  STDLI_ELAPSED_TIME_T      *elapsed_p);  /* ptr to elapsed time struct*/
void stdltime_start_tick(
  U8                        numMsec);     /* num msec per system tick */
STDLI_ERR_E stdltime_reg_timer_func(
  STDLI_TIMER_EVENT_T       *timeEvt_p,   /* ptr to time event struct to insert */
  U8                        offset);      /* offset to first timer event, only repetetive */
void stdltime_timer2_poll(void);

/* 
 * API for digital I/O functions
 */
/* Digital I/O interface structures/enumerations */
typedef enum
{
  STDLI_DIG_PORT_A          = 0x00,
  STDLI_DIG_PORT_B          = 0x01,
  STDLI_DIG_PORT_C          = 0x02,
  STDLI_DIG_PORT_D          = 0x03,
  STDLI_DIG_PORT_E          = 0x04,
  STDLI_DIG_PORT_F          = 0x05,
  STDLI_DIG_PORT_G          = 0x06,
  STDLI_DIG_PORT_MASK       = 0x07,
  STDLI_DIG_OUT             = 0x10,
  STDLI_DIG_HI_DRIVE        = 0x20,
  STDLI_DIG_PULLUP          = 0x40,
  STDLI_DIG_SMALL_MODEL     = 0x80,       /* set if PTAPE = 0x1840, PTBPE = 0x1844 */
} STDLI_DIG_PORT_INFO_E;

/* Digital I/O function prototypes */
void stdldigio_config_dig_port(
  STDLI_DIG_PORT_INFO_E     portInfo,     /* port, input/output, drive, and pullup */
  U8                        mask,         /* mask of data bits to change */
  U8                        data);        /* data if output bits, unused if input */
U8 stdldigio_read_port(
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        mask);        /* mask of data bits to read */
void stdldigio_write_port(
  STDLI_DIG_PORT_INFO_E     port,         /* data port, ex. STDLI_DIG_PORT_A */
  U8                        mask,         /* mask of data bits to write */
  U8                        data);        /* data to write */

/* 
 * API for ADC functions
 */
/* ADC interface structures/enumerations */
typedef enum
{
  STDLI_ADC_PORT0           = 0x00,
  STDLI_ADC_PORT1           = 0x01,
  STDLI_ADC_PORT2           = 0x02,
  STDLI_ADC_PORT3           = 0x03,
  STDLI_ADC_PORT4           = 0x04,
  STDLI_ADC_PORT5           = 0x05,
  STDLI_ADC_PORT6           = 0x06,
  STDLI_ADC_PORT7           = 0x07,
  STDLI_ADC_PORT8           = 0x08,
  STDLI_ADC_PORT9           = 0x09,
  STDLI_ADC_PORT10          = 0x0a,
  STDLI_ADC_PORT11          = 0x0b,
  STDLI_ADC_PORT12          = 0x0c,
  STDLI_ADC_PORT13          = 0x0d,
  STDLI_ADC_PORT14          = 0x0e,
  STDLI_ADC_PORT15          = 0x0f,
  STDLI_ADC_PORT16          = 0x10,
  STDLI_ADC_PORT17          = 0x11,
  STDLI_ADC_PORT18          = 0x12,
  STDLI_ADC_PORT19          = 0x13,
  STDLI_ADC_PORT20          = 0x14,
  STDLI_ADC_PORT21          = 0x15,
  STDLI_ADC_PORT22          = 0x16,
  STDLI_ADC_PORT23          = 0x17,
  STDLI_ADC_TEMP_SENSOR     = 0x1a,
  STDLI_ADC_BANDGAP         = 0x1b,
  STDLI_ADC_REFHI           = 0x1d,
  STDLI_ADC_REFLO           = 0x1e,
  STDLI_ADC_MOD_DISABLE     = 0x1f,
  STDLI_ADC_PORT_MASK       = 0x1f,
  STDLI_ADC_POLL_MODE       = 0x40,       /* set if ADC channel is polled */
  STDLI_ADC_DIG_SMALL_MODEL = 0x80,       /* set if PTAPE = 0x1840, PTBPE = 0x1844 */
} STDLI_ADC_PORT_E;

typedef struct stdli_adc_chan_s
{
  STDLI_ADC_PORT_E          chan;
  void                      (*adcSample_fp)(U16 cbParam, U16 sample);
  U16                       cbParm;
  struct stdli_adc_chan_s   *next_p;      /* Filled by utility */
} STDLI_ADC_CHAN_T;

typedef enum
{
  STDLI_ADC_FAST            = 0x00,
  STDLI_ADC_SLOW            = 0x01,
  STDLI_ADC_12BIT           = 0x00,
  STDLI_ADC_10BIT           = 0x02,
  STDLI_ADC_FAST_OSC        = 0x04,
} STDLI_ADC_CFG_E;

/* To install ADC functions, add INTRPT_ADC to POPULATED_INTS in
 * projintrpts.h file.  Add the following lines to install the isr:
 *      interrupt void stdladc_adc_complete_isr(void);
 *      #define vector23 stdladc_adc_complete_isr
 * If ADC samples need to be taken every ms, timing functions need
 * to be installed.  See above for installing timing functions.
 *
 * To install ADC polled functions, call stdladc_adc_complete_poll
 * and OR STDLI_ADC_POLL_MODE into chan field when registering.
 */
/* ADC function prototypes */
void stdladc_init_adc(
  STDLI_ADC_CFG_E           adcCfg);      /* STDLI_ADC_FAST/SLOW/12BIT/10BIT */
STDLI_ERR_E stdladc_reg_adc_chan(
  STDLI_ADC_CHAN_T          *adcChan_p);  /* ptr to ADC chan, callback info */
STDLI_ERR_E stdladc_start_adc_sampling(void);
void stdladc_adc_complete_poll(void);

/* 
 * API for eeprom functions
 */
/* EEPROM interface structures/enumerations */
#define STDLI_SECTOR_SIZE   8
#define STDLI_SECTOR_MASK   (STDLI_SECTOR_SIZE - 1)

/* EEPROM/Flash function prototypes */
void stdleeprom_init_eeprom_addr( 
  U8                        *addr_p);     /* ptr to first addr of eeprom */
void stdleeprom_start_sector_erase( 
  U8                        *addr_p);     /* ptr to sector addr in eeprom */
BOOL stdleeprom_check_cmd_done(void);
void stdleeprom_start_write( 
  U8                        *addr_p,      /* ptr to addr in eeprom to write */
  U8                        data);        /* data to write */
void stdleeprom_start_flash_sector_erase( 
  U8                        *addr_p);     /* ptr to sector addr in flash */
void stdleeprom_start_flash_write( 
  U8                        *addr_p,      /* ptr to addr in flash to write */
  U8                        data);        /* data to write */

/* 
 * API for event functions
 */
/* Event interface structures/enumerations */
typedef struct
{
  U32                       event;
  U32                       timeStamp;
  U16                       data[2];
} STDLI_EVENT_LOG_T;

#define STDLI_EVENT_LOG_LEN sizeof(STDLI_EVENT_LOG_T)
#define STDLI_UNUSED_EVENT  0xffffffff

/* Event function prototypes, require timing functions be installed */
STDLI_ERR_E stdlevt_init_log_event( 
  STDLI_EVENT_LOG_T         *firstEvt_p,  /* ptr to first event log entry */
  U8                        *endLog_p,    /* ptr to the end of the log */
  U8                        *eeprom_p);   /* ptr to first addr of eeprom */
void stdlevt_log_event( 
  U32                       eventId,      /* event id, includes event/file/line */
  U16                       data1,        /* event spec data */
  U16                       data2,        /* event spec data */
  BOOL                      kFatal);      /* TRUE if this is a k_fatal */
  
/*
 * ===============================================================================
 * 
 * Name: STDLI_K_FATAL_M
 * 
 * ===============================================================================
 */
/**
 * The K_FATAL macro
 * 
 * The K_FATAL macro fills out an event record with current fileId and lineNum.
 * The current time is grabbed, and the next unused event is located.
 * The log record is stored in the EEPROM.  The processor is reset.
 * 
 * @param   eventId     [in]    12 bit event identifier
 * @param   data1       [in]    16 bits of extra info which is event specific
 * @param   data2       [in]    16 bits of extra info which is event specific
 * @return  None
 * 
 * @pre  stdltime_start_timing_clock 
 * @note Processor is reset
 * 
 * ===============================================================================
 */
#define STDLI_K_FATAL_M(event, data1, data2)                    \
    stdlevt_log_event(((U32)(event) << 20) |                    \
      ((U32)(STDL_FILE_ID & 0xff) << 12) |                      \
      (((U32)__LINE__ & 0xfff) << 12),                          \
      (data1), (data2), TRUE)

/*
 * ===============================================================================
 * 
 * Name: STDLI_LOG_EVENT_M
 * 
 * ===============================================================================
 */
/**
 * The LOG_EVENT macro
 * 
 * The LOG_EVENT macro fills out an event record with current fileId and lineNum.
 * The current time is grabbed, and the next unused event is located.
 * The log record is stored in the EEPROM.
 * 
 * @param   eventId     [in]    12 bit event identifier
 * @param   data1       [in]    16 bits of extra info which is event specific
 * @param   data2       [in]    16 bits of extra info which is event specific
 * @return  None
 * 
 * @pre  stdltime_start_timing_clock 
 * @note None
 * 
 * ===============================================================================
 */
#define STDLI_LOG_EVENT_M(event, data1, data2)                  \
    stdlevt_log_event(((U32)(event) << 20) |                    \
      ((U32)(STDL_FILE_ID & 0xff) << 12) |                      \
      ((U32)__LINE__ & 0xfff),                                  \
      (data1), (data2), FALSE)

/* 
 * API for serial functions
 */
/* Serial interface structures/enumerations */
typedef enum
{
  STDLI_SER_PORT_1          = 0x00,
  STDLI_SER_PORT_2          = 0x01,
  STDLI_NUM_SER_PORT        = 0x02,
  STDLI_FAST_OSC            = 0x40,
  STDLI_POLL_SER_PORT       = 0x80,
} STDLI_SER_PORT_E;

typedef struct
{
  U8                        *txBuf_p;
  U8                        txBufSize;
  void                      (*rxSerChar_fp)(U16 cbParm, U8 data);
  U16                       cbParm;
  U8                        curTxHead;    /* Filled by utility */
  U8                        curTxTail;    /* Filled by utility */
  BOOL                      txAct;        /* Filled by utility */
  U8                        pollBit;      /* Filled by utility */
} STDLI_SER_INFO_T;

#define STDLI_CRC8_INIT_VAL 0xff

/* To install serial functions, add INTRPT_SCI1_RCV | INTRPT_SCI1_XMT
 * to POPULATED_INTS in projintrpts.h file for serial port 1.  Add
 * INTRPT_SCI2_RCV | INTRPT_SCI2_XMT to POPULATED_INTS for serial port 2.
 * Add the following lines to install the isr for serial port 1:
 *      interrupt void stdlser_rcv_port1_isr(void);
 *      #define vector17 stdlser_rcv_port1_isr
 *      interrupt void stdlser_xmt_port1_isr(void);
 *      #define vector18 stdlser_xmt_port1_isr
 * Add the following lines to install the isr for serial port 2:
 *      interrupt void stdlser_rcv_port2_isr(void);
 *      #define vector20 stdlser_rcv_port2_isr
 *      interrupt void stdlser_xmt_port2_isr(void);
 *      #define vector21 stdlser_xmt_port2_isr
 *
 * To install serial polled functions, call stdlser_init_ser_port with
 * STDLI_POLL_SER_PORT OR'd into portNum.  During main loop, call
 * either stdlser_port1_poll or stdlser_port2_poll.
 */
/* Serial port function prototypes */
void stdlser_ser_module_init(void);
void stdlser_init_ser_port(
  STDLI_SER_PORT_E          portNum,      /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
  STDLI_SER_INFO_T          *serInfo_p);  /* Ser state, txBuf addr, txBuf size, rx
                                           *  callback func.
                                           */
U16 stdlser_xmt_data(
  STDLI_SER_PORT_E          portNum,      /* Either STDLI_SER_PORT_1 or STDLI_SER_PORT_2 */
  BOOL                      blocking,     /* TRUE to block waiting to put xmt data on queue */
  U8                        *data_p,      /* Ptr to data to xmt */
  U16                       numChar);     /* Num chars to xmt */
void stdlser_calc_crc8(
  U8                        *crc8_p,      /* Ptr to crc8 */
  U16                       length,       /* Num chars in data stream */
  U8                        *data_p);     /* Ptr to data stream */
void stdlser_port1_poll(void);
void stdlser_port2_poll(void);
 
/* 
 * API for PWM functions
 */
/* PWM interface structures/enumerations */
typedef enum
{
  STDLI_TPM_1               = 0x00,
  STDLI_TPM_2               = 0x40,
  STDLI_PWM_CHAN_0          = 0x00,
  STDLI_PWM_CHAN_1          = 0x01,
  STDLI_PWM_CHAN_2          = 0x02,
  STDLI_PWM_CHAN_3          = 0x03,
  STDLI_PWM_CHAN_4          = 0x04,
  STDLI_PWM_CHAN_5          = 0x05,
  STDLI_MAX_PWM_CHAN        = 0x06,
  STDLI_PWM_CHAN_MASK       = 0x07,
  STDLI_TPM_MASK            = 0x40,       /* Note: Matches with HW addr offset */
  STDLI_TPM_DIG_SMALL_MODEL = 0x80,       /* set if PTAPE = 0x1840, PTBPE = 0x1844 */
} STDLI_TPM_CHAN_E;

typedef enum
{
  STDLI_CAP_IDLE            = 0x00,
  STDLI_CAP_START           = 0x01,
  STDLI_CAP_FIRST_SMPLE     = 0x02,
} STDLI_CAP_STATE_E;

#define STDLI_CAP_TIMEOUT   MAX_U16

typedef struct stdli_cap_s
{
  STDLI_TPM_CHAN_E          capChan;
  void                      (*capDone_fp)(U16 cbParm, U16 data);
  U16                       cbParm;
  U8                        maxTicks;
  U16                       startCnt;     /* Filled by utility */
  STDLI_CAP_STATE_E         state;        /* Filled by utility */
  U8                        tickCnt;      /* Filled by utility */
  struct stdli_cap_s        *next_p;      /* Filled by utility */
} STDLI_CAP_T;

/* To install PWM capture functions, add INTRPT_TPMx_CHANn
 * to POPULATED_INTS in projintrpts.h file for each capture channel.
 * (if x is 1, n is 0 to 5, if x is 2, n is 0 to 1).
 * Add the following lines to install the isr for each channel:
 *      interrupt void stdlser_rcv_tpmx_chann_isr(void);
 *      #define vectorz stdlser_rcv_tpmx_chann_isr
 * for TPM1:  chan0 = vector5, chan1 = vector6, ... chan5 = vector10
 * for TPM2:  chan0 = vector12, chan1 = vector13
 */
/* PWM function prototypes */
void stdlpwm_init_pwm_module(void);
void stdlpwm_set_tpm1_period(
  U16                       maxPeriod);   /* Max period in ticks */
STDLI_ERR_E stdlpwm_config_cap_chan(
  STDLI_CAP_T               *capCfg_p);   /* Capture cfg with TPM num, chan num,
                                           *    done func ptr, and callback param.
                                           */
STDLI_ERR_E stdlpwm_start_cap_chan(
  STDLI_TPM_CHAN_E          capChan);     /* TPM number and channel */
STDLI_ERR_E stdlpwm_start_pwm_chan(
  STDLI_TPM_CHAN_E          capChan,      /* TPM number and channel */
  U16                       onCount,
  STDLI_DIG_PORT_INFO_E     port,
  U8                        digPinMask) ;

/* 
 * API for I2C functions
 */
/* I2C interface structures/enumerations */
typedef enum
{
  I2C_POLL                  = 0x01,
  I2C_FREESCALE             = 0x02,
  I2C_SLAVE                 = 0x04,
} STDLI_I2C_E;

typedef enum
{
  STDLI_I2C_XFER_OK         = 0x00,
  STDLI_I2C_NO_RESP         = 0x01,
} STDLI_I2C_RESP_E;

typedef enum
{
  STDLI_I2C_WRITE_ADDR      = 0x00,
  STDLI_I2C_READ_ADDR       = 0x01,
} STDLI_I2C_ADDR_E;

typedef struct
{
  U8                        addr;
  U8                        *data_p;
  U8                        numDataBytes;
  void                      (*i2cDone_fp)(U16 cbParm, STDLI_I2C_RESP_E status);
  U16                       cbParm;
} STDLI_I2C_XFER_T;

typedef struct
{
  U8                        cmd;
  void                      (*slaveCmd_fp)(U8 cmd, U8 *cmdLen_p, U8 **dest_pp);
  void                      (*slaveRcvDone_fp)(U8 cmd, STDLI_I2C_XFER_T **i2cXfer_pp);
  U8                        cmdLen;
  U8                        *cmdDest_p;
} STDLI_I2C_SLAVE_T;

/* To install i2c functions, add INTRPT_I2C_CTL
 * to POPULATED_INTS in projintrpts.h file.
 * Add the following lines to install the isr:
 *      interrupt void stdli2c_i2c_isr(void);
 *      #define vector24 stdli2c_i2c_isr
 *
 * To install i2c polled functions, call stdli2c_i2c_complete_poll and
 * call stdli2c_init_i2c with poll set to TRUE. 
 */
/* I2c function prototypes */
void stdli2c_init_i2c(
  STDLI_I2C_E               params,       /* I2C_POLL,I2C_FREESCALE or I2C_SLAVE */
  U8                        addr,         /* Slave i2c addr */
  STDLI_I2C_SLAVE_T         *slave_p);    /* Slave i2c params */
STDLI_ERR_E stdli2c_send_i2c_msg(
  STDLI_I2C_XFER_T          *i2cXfer_p);  /* ptr to i2c xfer structure */
void stdli2c_i2c_complete_poll(void);

/* 
 * API for SPI functions
 */
/* SPI interface structures/enumerations */
typedef enum
{
  SPI_CLK_DIV2              = 0x00,
  SPI_CLK_DIV4              = 0x01,
  SPI_CLK_DIV8              = 0x02,
  SPI_CLK_DIV16             = 0x03,
  SPI_CLK_DIV32             = 0x04,
  SPI_CLK_DIV64             = 0x05,
  SPI_CLK_DIV128            = 0x06,
  SPI_CLK_DIV256            = 0x07,
  SPI_CLK_DIV_MASK          = 0x07,
  SPI_POLL                  = 0x80,
} STDLI_SPI_PARAM_E;

typedef enum
{
  STDLI_SPI_READ            = 0x00,
  STDLI_SPI_WRITE           = 0x01,
  STDLI_SPI_CPHA0           = 0x00,   /* First SCLK trans latches data */
  STDLI_SPI_CPHA1           = 0x04,   /* Sec SCLK trans latches data */
  STDLI_SPI_CPOL0           = 0x00,   /* SCLK idles low */
  STDLI_SPI_CPOL1           = 0x08,   /* SCLK idles high */
  STDLI_SPI_CPOL_CPHA_MASK  = 0x0c,
} STDLI_SPI_DIR_E;

typedef struct stldi_spi_xfer_s
{
  STDLI_SPI_DIR_E           dir;
  U8                        *data_p;
  U8                        numDataBytes;
  STDLI_DIG_PORT_INFO_E     csPort;
  U8                        csMask;
  void                      (*spiDone_fp)(U16 cbParm);
  U16                       cbParm;
  struct stldi_spi_xfer_s   *next_p;
} STDLI_SPI_XFER_T;

/* To install SPI functions, add INTRPT_SPI
 * to POPULATED_INTS in projintrpts.h file.
 * Add the following lines to install the isr:
 *      interrupt void stdlspi_spi_isr(void);
 *      #define vector15 stdlspi_spi_isr
 *
 * To install SPI polled functions, call stdlspi_spi_complete_poll and
 * call stdlspi_init_spi with poll set to TRUE. 
 */
/* SPI function prototypes */
void stdlspi_init_spi(
  STDLI_SPI_PARAM_E         param);       /* set poll mode and clk div */
void stdlspi_send_spi_msg(
  STDLI_SPI_XFER_T          *spiXfer_p);  /* ptr to SPI xfer structure */
void stdlspi_spi_complete_poll(void);
#endif
