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
#define NUM_ANA_INP 4

#define LOW_THRESH 200
#define HI_THRESH 800

#define PWM_ALL_ON 7
#define LED_PIN 13

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

const int INP_PIN_MAP[MAX_NUM_SOL] = { A4, A5, A6, A7, 9, 10, 11, 12 };
const int OUT_PIN_MAP[MAX_NUM_SOL] = { A0, A1, A2, A3, 6, 7, 8, 9 };

void setup() 
{
  // put your setup code here, to run once:

  // setup ADC0 to ADC3 as digital outputs and low 
  for (int pin = A0; pin <= A3; pin++)
  {
    digitalWrite(pin, LOW);
    pinMode(pin, OUTPUT);
  }
  
  // setup ADC4 to ADC7 as analog inputs
  for (int pin = A4; pin <= A7; pin++)
  {
    pinMode(pin, INPUT_PULLUP);
  }

  // setup PD5-7, PB0 (pins 9-12) as digital outputs and low 
  for (int pin = 9; pin <= 12; pin++)
  {
    digitalWrite(pin, LOW);
    pinMode(pin, OUTPUT);
  }
  
  // setup PB1 to PB4 (pins 13-16) as digital inputs 
  for (int pin = 13; pin <= 16; pin++)
  {
    digitalWrite(pin, LOW);
    pinMode(pin, OUTPUT);
  }

  // for debugging loop speed set LED pin 13 as output
  pinMode(LED_PIN, OUTPUT);
}  

void loop() 
{
  // put your main code here, to run repeatedly:
  for (int sol = 0; sol < MAX_NUM_SOL; sol++)
  {
    switch (solState[sol].state)
    {
      case IDLE:
      {
        bool changeState = false;
        
        // Check if switch is active
        if (sol < NUM_ANA_INP)
        {
          // Must read analog input instead of digital bit
          int value = analogRead(INP_PIN_MAP[sol]);
          if (value < LOW_THRESH)
          {
            changeState = true;
          }
        }
        else
        {
          // Check if input is low
          int value = digitalRead(INP_PIN_MAP[sol]);
          if (value == 0)
          {
            changeState = true;
          }
        }
        if (changeState)
        {
          solState[sol].state = INIT_KICK;
          digitalWrite(OUT_PIN_MAP[sol], 1);
          solState[sol].time = millis() + solState[sol].kickMs;
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
            digitalWrite(OUT_PIN_MAP[sol], 0);
            solState[sol].state = WAIT_SW_OFF;
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
        if (sol < NUM_ANA_INP)
        {
          // Must read analog input instead of digital bit
          int value = analogRead(INP_PIN_MAP[sol]);
          if (value > HI_THRESH)
          {
            solState[sol].state = IDLE;
            skipProc = true;
          }
        }
        else
        {
          // Check if input is high
          int value = digitalRead(INP_PIN_MAP[sol]);
          if (value == 1)
          {
            solState[sol].state = IDLE;
            skipProc = true;
          }
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
        if (sol < NUM_ANA_INP)
        {
          // Must read analog input instead of digital bit
          int value = analogRead(INP_PIN_MAP[sol]);
          if (value > HI_THRESH)
          {
            digitalWrite(OUT_PIN_MAP[sol], 0);
            solState[sol].state = IDLE;
            skipProc = true;
          }
        }
        else
        {
          // Check if input is high
          int value = digitalRead(INP_PIN_MAP[sol]);
          if (value == 1)
          {
            digitalWrite(OUT_PIN_MAP[sol], 0);
            solState[sol].state = IDLE;
            skipProc = true;
          }
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
        if (sol < NUM_ANA_INP)
        {
          // Must read analog input instead of digital bit
          int value = analogRead(INP_PIN_MAP[sol]);
          if (value > HI_THRESH)
          {
            solState[sol].state = IDLE;
          }
        }
        else
        {
          // Check if input is high
          int value = digitalRead(INP_PIN_MAP[sol]);
          if (value == 1)
          {
            solState[sol].state = IDLE;
          }
        }
        break;
      }
    }
  }

  // Strobe LED pin
  digitalWrite(LED_PIN, 1);
  digitalWrite(LED_PIN, 0);
}
