#include <UstepperS32.h>

UstepperS32 stepper;

void setup() {
  stepper.setup();                   //Initialize uStepper S32
  stepper.checkOrientation(30.0);    //Check orientation of motor connector with +/- 30 microsteps movement
  stepper.setMaxAcceleration(2000);  //use an acceleration of 2000 fullsteps/s^2
  stepper.setMaxVelocity(500);       //Max velocity of 500 fullsteps/s
  Serial.begin(115200);
}

void loop() {

  if (Serial.available() > 0 && !stepper.getMotorState()) {
    int angle = Serial.parseInt();
    delay(50);
    stepper.moveAngle(angle);
  }

  float angle = stepper.encoder.getAngleMoved();
  Serial.print(angle);  //print out angle moved since last reset
}