import time

from utils import motor_manager

radius = 200

x_port = "/dev/serial/by-id/usb-STMicroelectronics_USTEPPER_S32_CDC_in_FS_Mode_2050307F5632-if00"
y_port = "/dev/serial/by-id/usb-STMicroelectronics_USTEPPER_S32_CDC_in_FS_Mode_2058307B5632-if00"
arduino_port = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55737313231351B06080-if00"

manager = motor_manager.MotorManager(x_port, y_port, arduino_port)
try:
    manager.set_home()

    while True:
        manager.goto_absolute(int(input("X : ")), int(input("Y : ")))


except KeyboardInterrupt:
    time.sleep(3)

# 2500 x 1800
