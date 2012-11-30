/* Include the derivative-specific header file */
#include <MC9S08DZ60.h>
/* Note:  DZ60 is used instead of AC16 because clearing the COP
 *  timer is more difficult for DZ60, and the DZ60 functions
 *  works for all currently supported processors.
 */

#define _Stop asm ( stop; )
  /*!< Macro to enter stop modes, STOPE bit in SOPT1 register must be set prior to executing this macro */

#define _Wait asm ( wait; )
  /*!< Macro to enter wait mode */


