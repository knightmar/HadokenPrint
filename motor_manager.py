import threading
import time

import serial
from serial.serialutil import SerialException


class MotorManager:
    def __init__(self, serial_port_x, serial_port_y, baud=115200):
        self.current_x = 0
        self.current_y = 0
        self.wanted_x = 0
        self.wanted_y = 0
        self.run = True
        try:
            self.ser_x = serial.Serial(serial_port_x, baud)
            self.ser_y = serial.Serial(serial_port_y, baud)
        except SerialException as err:
            print("Error append while initiating the manager : ", err)
            self.stop()
            return

    def goto(self, x, y):
        self.wanted_x = x
        self.wanted_y = y

    def start(self):
        print("Starting the manager...")
        self.goto(0, 0)
        threading.Thread(target=self.move_motors).start()

    def stop(self):
        print("Stopping the manager...")
        self.run = False

    def move_motors(self):
        # Calculate the difference in angles
        while self.run:
            buffer_x = self.wanted_x
            buffer_y = self.wanted_y
            delta_x = buffer_x - self.current_x
            delta_y = buffer_y - self.current_y

            # Send the differences over serial
            self.ser_x.write(f"{delta_x}\n".encode())  # Convert to bytes and send
            self.ser_y.write(f"{delta_y}\n".encode())
            time.sleep(0.5)
            self.current_x = buffer_x
            self.current_y = buffer_y
