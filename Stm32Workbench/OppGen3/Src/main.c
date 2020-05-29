/* USER CODE BEGIN Header */
/*
 *===============================================================================
 *
 *                         OOOOOO
 *                       OOOOOOOOOO
 *      PPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *  PPP          PPP   OOO        OOO   PPP          PPP
 *   PPP         PPP   OOO        OOO   PPP         PPP
 *    PPPPPPPPPPPPPP   OOO        OOO   PPPPPPPPPPPPPP
 *     PPPPPPPPPPPPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP   OOO        OOO   PPP
 *               PPP    OOO      OOO    PPP
 *               PPP     OOOOOOOOOO     PPP
 *              PPPPP      OOOOOO      PPPPP
 *
 * @file:   main.c
 * @author: Hugh Spahr
 * @date:   9/21/2019
 *
 * @note:   Open Pinball Project
 *          Copyright© 2019, Hugh Spahr
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
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "Common/stdtypes.h"
#define GEN2G_INSTANTIATE
#include "Common/gen2glob.h"
#include "Common/neointf.h"
#include "Common/stdlintf.h"
#define INSTANTIATE_PROC
#include "Common/procdefs.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);

/* USER CODE BEGIN PFP */
/* HRS:  Debug */
void debug_save_nv_cfg();

/* Prototype declarations */
void timer_init();
void timer_overflow_isr();

void main_copy_flash_to_ram();
void main_call_wing_inits();

void digital_init();
void digital_task(void);
void digital_write_outputs();

void rs232proc_init();
void rs232proc_task();

void incand_task(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
   /* USER CODE BEGIN 1 */

   /* USER CODE END 1 */


   /* MCU Configuration--------------------------------------------------------*/

   /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
   HAL_Init();
#if GEN2G_DEBUG_PORT == 0
   __HAL_AFIO_REMAP_SWJ_DISABLE();
#endif

   /* USER CODE BEGIN Init */

   /* USER CODE END Init */

   /* Configure the system clock */
   SystemClock_Config();

   /* USER CODE BEGIN SysInit */

   /* USER CODE END SysInit */

   /* Initialize all configured peripherals */
   MX_GPIO_Init();
   MX_USB_DEVICE_Init();

   // HRS:  Start code here
   appStart.codeVers = GEN2G_CODE_VERS;

   /* Used for forcing the standard configuration onto the board.  If this is left on,
    * the programmed configuration will always be overwritten.
    */
#if 0
   debug_save_nv_cfg();
#endif

   main_copy_flash_to_ram();
   main_call_wing_inits();

   stdlser_init();
   rs232proc_init();

   /* Initialize tasks */
   timer_init();

   EnableInterrupts; /* Enable global interrupts. */

   /* USER CODE END 2 */

   /* Infinite loop */
   /* USER CODE BEGIN WHILE */

   while (1)
   {
      /* USER CODE END WHILE */

      /* USER CODE BEGIN 3 */
      timer_overflow_isr();
      neo_task();
      digital_task();
      incand_task();
      rs232proc_task();
      digital_write_outputs();
      /* USER CODE END 3 */
   }
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
   RCC_OscInitTypeDef RCC_OscInitStruct = {0};
   RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
   RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

   /** Initializes the CPU, AHB and APB busses clocks
   */
   RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
   RCC_OscInitStruct.HSEState = RCC_HSE_ON;
   RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
   RCC_OscInitStruct.HSIState = RCC_HSI_ON;
   RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
   RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
   RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL6;
   if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
   {
      Error_Handler();
   }
   /** Initializes the CPU, AHB and APB busses clocks
   */
   RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
   RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
   RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
   RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
   RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

   if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
   {
      Error_Handler();
   }
   PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USB;
   PeriphClkInit.UsbClockSelection = RCC_USBCLKSOURCE_PLL;
   if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
   {
      Error_Handler();
   }
}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
   /* GPIO Ports Clock Enable */
   __HAL_RCC_GPIOC_CLK_ENABLE();
   __HAL_RCC_GPIOD_CLK_ENABLE();
   __HAL_RCC_GPIOB_CLK_ENABLE();
   __HAL_RCC_GPIOA_CLK_ENABLE();
}

/* USER CODE BEGIN 4 */
/*
 * ===============================================================================
 *
 * Name: main_copy_flash_to_ram
 *
 * ===============================================================================
 */
/**
 * Copy flash to RAM
 *
 * Check if the flash settings are valid.  If so, copy the information into RAM.
 *
 * @param   None
 * @param   None
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void main_copy_flash_to_ram()
{
   U8                         crc;
   U32                        *src_p;
   U32                        *dst_p;

   /* Init gen2g structure */
   gen2g_info.typeWingBrds = 0;
   gen2g_info.crcErr = 0;
   gen2g_info.error = NO_ERRORS;
   gen2g_info.validCfg = FALSE;
   gen2g_info.haveNeo = FALSE;
   gen2g_info.freeCfg_p = &gen2g_info.nvCfgInfo.cfgData[0];
   gen2g_info.prodId = gen2g_persist_p->prodId;
   gen2g_info.serNum = gen2g_persist_p->serNum;

   while (!gen2g_info.validCfg)
   {
      /* Test if wing cfg have valid settings */
      crc = 0xff;
      stdlser_calc_crc8(&crc, GEN2G_NV_PARM_SIZE, (U8 *)gen2g_nv_cfg_p->wingCfg);
      if (crc == gen2g_nv_cfg_p->nvCfgCrc)
      {
         gen2g_info.validCfg = TRUE;

         /* Copy the wing configuration */
         for (src_p = (U32 *)gen2g_nv_cfg_p, dst_p = (U32 *)&gen2g_info.nvCfgInfo;
            src_p < (U32 *)(GEN2G_CFG_TBL + sizeof(GEN2G_NV_CFG_T)); )
         {
            *dst_p++ = *src_p++;
         }
      }
      else
      {
         /* Config CRC8 failed, save a valid configuration */
         debug_save_nv_cfg();
         gen2g_info.validCfg = FALSE;
      }
   }
} /* End main_copy_flash_to_ram */

/*
 * ===============================================================================
 *
 * Name: main_call_wing_inits
 *
 * ===============================================================================
 */
/**
 * Call wing board init functions
 *
 * If the configuration is valid, create wing board type mask, and call init
 * functions.
 *
 * @param   None
 * @param   None
 * @return  None
 *
 * @pre     None
 * @note    None
 *
 * ===============================================================================
 */
void main_call_wing_inits()
{
   INT                        index;

   if (gen2g_info.validCfg)
   {
      /* Walk through the wing boards and create bit mask of wing board types */
      for (index = 0; index < RS232I_NUM_WING; index++)
      {
         if (gen2g_info.nvCfgInfo.wingCfg[index] != WING_UNUSED)
         {
            gen2g_info.typeWingBrds |= (1 << gen2g_info.nvCfgInfo.wingCfg[index]);
         }
      }

      /* Walk through types and call init functions using jump table */
      digital_init();
      for (index = WING_UNUSED + 1; index < MAX_WING_TYPES; index++)
      {
         if (((gen2g_info.typeWingBrds & (1 << index)) != 0) &&
            (GEN2G_INIT_FP[index] != NULL))
         {
            GEN2G_INIT_FP[index]();
         }
      }
   }
} /* End main_call_wing_inits */
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
