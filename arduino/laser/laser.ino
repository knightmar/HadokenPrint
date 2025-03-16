#include <TimerOne.h>  // Include the Timer1 library

const int laserPin = 9;  // Laser connected to digital pin 9 (PWM pin)
const int potPin = A3;   // Potentiometer connected to analog pin A0

bool manual_mode = false;

void setup() {
  // Set PWM frequency to 1 kHz for pin 9
  Timer1.initialize(1000);  // Initialize Timer1 with a frequency of 1 kHz
  Timer1.pwm(laserPin, 0);  // Set pin 9 as PWM output

  pinMode(potPin, INPUT);
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  Serial.begin(9600);  // Initialize Serial communication
}

void loop() {

  int potValue = analogRead(potPin);
  int laserIntensity = map(potValue, 0, 1023, 0, 255);

  // Set the laser intensity using Timer1 PWM
  Timer1.setPwmDuty(laserPin, laserIntensity);


  Serial.println(String(digitalRead(2)) + String(digitalRead(3)));
}
