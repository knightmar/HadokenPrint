import math
import time

from python.utils import motor_manager

radius = 200

# Side length of the equilateral triangle
side_length = 350
height = math.sqrt(3) / 2 * side_length

manager = motor_manager.MotorManager('/dev/ttyACM1', '/dev/ttyACM0')
try:
    while True:
        # manager.goto_relative(int(input("X : ")), int(input("Y : ")))

        for y in range(50):
            for x in range(50):
                manager.goto_absolute(x, y)
                time.sleep(0.01)




except KeyboardInterrupt:
    time.sleep(3)

# 2500 x 1800
