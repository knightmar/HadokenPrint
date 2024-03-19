import time

import motor_manager

manager = motor_manager.MotorManager('COM6', 'COM7')
time.sleep(2)
try:
    while manager.run:
        manager.goto(int(input("X : ")), int(input("Y : ")))
        time.sleep(1)
except KeyboardInterrupt:
    time.sleep(3)
    manager.stop()
