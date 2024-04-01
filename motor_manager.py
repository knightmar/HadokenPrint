import threading
import time

import serial
from serial.serialutil import SerialException


class MotorManager:
    def __init__(self, serial_port_x, serial_port_y, baud=115200):
        self.x = 0
        self.y = 0
        self.motor_x = serial.Serial(serial_port_x, baudrate=baud)
        self.motor_y = serial.Serial(serial_port_y, baudrate=baud)

    def goto(self, x, y):
        delta_x = self.x - x
        delta_y = self.y - y
        try:
            self.motor_x.write(bytes(str(delta_x), 'utf-8'))
            self.motor_y.write(bytes(str(delta_y), 'utf-8'))
        except SerialException as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
