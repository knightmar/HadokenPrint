import time

import motor_manager

manager = motor_manager.MotorManager('/dev/ttyACM0', None)
try:
    while True:
        manager.goto(int(input("X : ")), int(input("Y : ")))
        time.sleep(1)
except KeyboardInterrupt:
    time.sleep(3)
