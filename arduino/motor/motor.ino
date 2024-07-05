#include <UstepperS32.h>

// Create a new instance of the uStepper class
UstepperS32 stepper;

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);

  // Setup the stepper motor
  stepper.setup();

  // Set the maximum velocity and acceleration
  stepper.setMaxAcceleration(5000);
  stepper.setMaxVelocity(1000);
  stepper.checkOrientation(30.0);
}

void loop() {
  // Check if there is new data in the serial buffer
  if (Serial.available() > 0) {
    // Read the input from the serial buffer
    String input = Serial.readStringUntil('\n');

    // Check if the input is "HOME"
    if (input == "HOME") {
      // Set the home position of the stepper motor
      stepper.encoder.setHome();
      Serial.println("Home position set");
    } else {
      // Try to parse the input as an angle
      int angle = input.toInt();

      // Check if the parsing was successful
      if (angle != 0) {
        // Move the stepper motor to the given angle
        stepper.moveToAngle(angle);

        if (abs(angle - stepper.angleMoved()) > 0.5) {
          Serial.println("Bad move");
          stepper.moveToAngle(angle);
        }
        Serial.println("OK");
      } else {
        // The input was not "HOME" and not a valid angle
        Serial.println("Invalid input");
      }
    }
  }
}
