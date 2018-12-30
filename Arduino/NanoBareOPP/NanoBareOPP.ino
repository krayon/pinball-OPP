// Global stuff
typedef enum
{
  IDLE = 0,
  INIT_KICK = 1,
  PWM_OFF = 2,
  PWM_ON = 3,
  WAIT_SW_OFF = 4,
} SOL_STATE_E;

#define MAX_NUM_SOL 8
#define NUM_ANA_INP 2
#define FIRST_ANA_INP 6
#define ANA_INP_OFFSET 2

// Set ADMUX to use Vcc as voltage ref, and left justify conversion
#define ADMUX_INIT 0x60

// Set ADSRA to ADC enabled, no auto trigger, enable intrpt, prescalar to 128
#define ADCSRA_INIT 0x8f
#define ADCSRA_START_CONVERT 0x40

#define LOW_THRESH 0x40
#define HI_THRESH 0xc0

#define PWM_ALL_ON 7
#define LED_PIN 13
#define LED_BIT 0x20

typedef struct
{
  SOL_STATE_E   state;
  int           kickMs;
  int           pwm;  // Number from 0 to 7, 0 = No PWM, 1 = 12.5% PWM, 7 = 100% PWM
  unsigned long time;
} SOL_STATE_T;

SOL_STATE_T solState[MAX_NUM_SOL] = 
{
  {IDLE, 32, 0, 0}, {IDLE, 32, 0, 0}, {IDLE, 32, 0, 0}, {IDLE, 32, 0, 0},
  {IDLE, 32, 0, 0}, {IDLE, 32, 0, 0}, {IDLE, 32, 0, 0}, {IDLE, 32, 0, 0},
};

int currAdcInp = 0;
volatile unsigned char adcData = 0x0c;

const int INP_PIN_MAP[MAX_NUM_SOL] = { A4, A5, A6, A7, 9, 10, 11, 12 };
const int OUT_PIN_MAP[MAX_NUM_SOL] = { A0, A1, A2, A3, 5, 6, 7, 8 };

// Input pins PC4/ADC4, PC5/ADC5, ADC6, ADC7, PB1, PB2, PB3, PB4
// Output pins PC0, PC1, PC2, PC3, PD5, PD6, PD7, PB0

#define PORTC_MASK 0x30
#define PORTC_SHFT 4
#define PORTB_MASK 0x1e
#define PORTB_SHFT 3
#define DIG_INP_MASK 0xf3

void setup() 
{
  // put your setup code here, to run once:

  // setup ADC0 to ADC3 as digital outputs and low 
  for (int pin = A0; pin <= A3; pin++)
  {
    digitalWrite(pin, LOW);
    pinMode(pin, OUTPUT);
  }

  // setup PC4 to PC5 (pins 18-19) as digital inputs 
  for (int pin = 18; pin <= 19; pin++)
  {
    pinMode(pin, INPUT_PULLUP);
  }

  // setup ADC6, ADC7 as analog inputs
  for (int pin = A6; pin <= A7; pin++)
  {
    pinMode(pin, INPUT);
  }

  // setup PD5-7, PB0 (pins 5-8) as digital outputs and low 
  for (int pin = 5; pin <= 8; pin++)
  {
    digitalWrite(pin, LOW);
    pinMode(pin, OUTPUT);
  }
  
  // setup PB1 to PB4 (pins 9-12) as digital inputs 
  for (int pin = 9; pin <= 12; pin++)
  {
    pinMode(pin, INPUT_PULLUP);
  }

  // for debugging loop speed set LED pin 13 as output and off
  digitalWrite(LED_PIN, LOW);
  pinMode(LED_PIN, OUTPUT);

  // Setup ADC registers
  ADMUX = ADMUX_INIT + FIRST_ANA_INP; // Read first ADC input (ADC6), left justified
  ADCSRB = 0; // Unused, setting to 0
  ADCSRA = ADCSRA_INIT; // Free running mode

  // Enable intrpts
  sei();
 
  // Start ADC conversion
  ADCSRA |= ADCSRA_START_CONVERT;

#if DEBUG
  Serial.begin(9600);
#endif
}  

void loop() 
{
  // Read inputs PC4, PC5, PB1, PB2, PB3, PB4
  unsigned char pcInp = (PINC & PORTC_MASK) >> PORTC_SHFT;
  unsigned char pbInp = (PINB & PORTB_MASK) << PORTB_SHFT;

  unsigned char currData = pcInp | pbInp | adcData;

  // put your main code here, to run repeatedly:
  for (int sol = 0; sol < MAX_NUM_SOL; sol++)
  {
    switch (solState[sol].state)
    {
      case IDLE:
      {
        // Check if switch is active
        if ((currData & (1 << sol)) == 0)
        {
          solState[sol].state = INIT_KICK;
          digitalWrite(OUT_PIN_MAP[sol], 1);
          solState[sol].time = millis() + solState[sol].kickMs;

#if DEBUG
          char tmp[16];
          sprintf(tmp, "Kick=%d", sol);
          Serial.println(tmp);
#endif
        }
        break;
      }
      case INIT_KICK:
      {
        unsigned long currTime = millis();
        if (currTime >= solState[sol].time)
        {
          if (solState[sol].pwm == 0)
          {
            // digitalWrite(OUT_PIN_MAP[sol], 0);
            solState[sol].state = WAIT_SW_OFF;
            
#if DEBUG
            char tmp[16];
            sprintf(tmp, "WaitOff=%d", sol);
            Serial.println(tmp);
#endif
          }
          else if (solState[sol].pwm == PWM_ALL_ON)
          {
            solState[sol].state = PWM_ON;
          }
          else
          {
            digitalWrite(OUT_PIN_MAP[sol], 0);
            solState[sol].state = PWM_OFF;
            solState[sol].time = currTime + (PWM_ALL_ON - solState[sol].pwm);
          }
        }
        break;
      }
      case PWM_OFF:
      {
        bool skipProc = false;
        
        // Check if switch is inactive
        if ((currData & (1 << sol)) != 0)
        {
            solState[sol].state = IDLE;
            skipProc = true;
        }

        if (!skipProc)
        {
          unsigned long currTime = millis();
          if (currTime >= solState[sol].time)
          {
            digitalWrite(OUT_PIN_MAP[sol], 1);
            solState[sol].state = PWM_ON;
            solState[sol].time = currTime + solState[sol].pwm;
          }
        }
        break;
      }
      case PWM_ON:
      {
        bool skipProc = false;
        
        // Check if switch is inactive
        if ((currData & (1 << sol)) != 0)
        {
          digitalWrite(OUT_PIN_MAP[sol], 0);
          solState[sol].state = IDLE;
          skipProc = true;
        }

        if (!skipProc)
        {
          unsigned long currTime = millis();
          if (currTime >= solState[sol].time)
          {
            if (solState[sol].pwm != PWM_ALL_ON)
            {
              digitalWrite(OUT_PIN_MAP[sol], 0);
              solState[sol].state = PWM_OFF;
              solState[sol].time = currTime + (PWM_ALL_ON - solState[sol].pwm);
            }
          }
        }
        break;
      }
      case WAIT_SW_OFF:
      {
        // Check if switch is inactive
        if ((currData & (1 << sol)) != 0)
        {
          solState[sol].state = IDLE;

#if DEBUG          
          char tmp[16];
          sprintf(tmp, "Idle=%d", sol);
          Serial.println(tmp);
#endif
        }
        break;
      }
    }
  }

  // Toggle LED bit twice so there is a rising pulse
  PINB = LED_BIT;
  PINB = LED_BIT;
}

// ADC interrupt routine
ISR(ADC_vect)
{
  // ADCH has bits eight bits of data since left justified
  unsigned char currVal = ADCH;

  if (currVal > HI_THRESH)
  {
    adcData |= (1 << (currAdcInp + ANA_INP_OFFSET));
  }
  else if (currVal < LOW_THRESH)
  {
    adcData &= ~(1 << (currAdcInp + ANA_INP_OFFSET));
  }

  currAdcInp++;
  if (currAdcInp >= NUM_ANA_INP)
  {
    currAdcInp = 0;
  }

  // Change to new ADC, start new conversion
  ADMUX = ADMUX_INIT + FIRST_ANA_INP + currAdcInp;
  ADCSRA |= ADCSRA_START_CONVERT;
}
