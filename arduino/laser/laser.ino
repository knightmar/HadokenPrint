#include <TimerOne.h> // Include the Timer1 library

const int laserPin = 9;  // Laser connected to digital pin 9 (PWM pin)
const int potPin = A3;   // Potentiometer connected to analog pin A0

bool manual_mode = false;

void setup() {
  // Set PWM frequency to 1 kHz for pin 9
  Timer1.initialize(1000); // Initialize Timer1 with a frequency of 1 kHz
  Timer1.pwm(laserPin, 0); // Set pin 9 as PWM output
  
  pinMode(potPin, INPUT);
  Serial.begin(9600); // Initialize Serial communication
}

void loop() {
  // Check for Serial input
  while (Serial.available() > 0) {
    int inputPower = Serial.parseInt();  // Read the integer value from Serial

    if (inputPower == -1) {
      manual_mode = !manual_mode;
      Serial.println("Manual mode : " + String(manual_mode));
    } else if (!manual_mode) {
      // Map the input value from the range of 0-100 to the required power range of 0-255
      int laserIntensity = map(inputPower, 0, 100, 0, 255);

      // Ensure the mapped value is within the valid range (0-255)
      laserIntensity = constrain(laserIntensity, 0, 255);

      // Set the laser intensity using Timer1 PWM
      Timer1.setPwmDuty(laserPin, laserIntensity);

      // Print the intensity value for debugging
      Serial.print("Laser intensity set to: ");
      Serial.println(laserIntensity);
    }
  }

  if (manual_mode) {
    // Manual mode is enabled
    int potValue = analogRead(potPin);
    int laserIntensity = map(potValue, 0, 1023, 0, 255);

    // Set the laser intensity using Timer1 PWM
    Timer1.setPwmDuty(laserPin, laserIntensity);

    // Print the potentiometer value for debugging
    Serial.print("Pot value : ");
    Serial.println(potValue);
  }
}
