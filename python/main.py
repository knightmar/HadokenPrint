import time

from python.utils import motor_manager

manager = motor_manager.MotorManager('/dev/ttyACM1', None)
try:
    while True:
        manager.goto_relative(int(input("X : ")), int(input("Y : ")))
except KeyboardInterrupt:
    time.sleep(3)
