import time

from python.utils import motor_manager

radius = 200

manager = motor_manager.MotorManager('/dev/ttyACM1', '/dev/ttyACM0')
try:
    manager.set_home()

    while True:
        manager.goto_absolute(int(input("X : ")), int(input("Y : ")))


except KeyboardInterrupt:
    time.sleep(3)

# 2500 x 1800
