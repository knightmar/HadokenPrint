#include <UstepperS32.h>

UstepperS32 stepper;

void setup() {
  stepper.setup();                   //Initialize uStepper S32
  stepper.checkOrientation(30.0);    //Check orientation of motor connector with +/- 30 microsteps movement
  stepper.setMaxAcceleration(5000);  //use an acceleration of 2000 fullsteps/s^2
  stepper.setMaxVelocity(1000);       //Max velocity of 500 fullsteps/s
  Serial.begin(115200);
}

void loop() {

  if (Serial.available() > 0 && !stepper.getMotorState()) {
    int angle = Serial.parseInt();
    delay(10);
    stepper.moveAngle(angle);

    float moved_angle = stepper.encoder.getAngleMoved();
    Serial.println(moved_angle);
  }
  delay(10);
}
