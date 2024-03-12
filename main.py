import motor_manager
import time

motor_manager.start()
time.sleep(2)
while True:
    motor_manager.goto(int(input("X : ")), int(input("Y : ")))
    time.sleep(1)
time.sleep(3)
motor_manager.stop()
