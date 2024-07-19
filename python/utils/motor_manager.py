import time

import serial
from serial.serialutil import SerialException

width = 2000
height = 1500


class MotorManager:
    def __init__(self, serial_port_x, serial_port_y, serial_port_arduino, baud=115200):
        self.x = 0
        self.y = 0
        self.motor_x = None
        self.motor_y = None
        self.serial_arduino = None
        self.pos_listeners = []

        try:
            self.serial_arduino = serial.Serial(serial_port_arduino, baudrate=baud)
            self.motor_x = serial.Serial(serial_port_x, baudrate=baud)
            self.motor_y = serial.Serial(serial_port_y, baudrate=baud)

        except SerialException as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    def goto_absolute(self, x, y, allow_negative=False):
        # print("starting move")
        self.x = min(x, width)
        self.y = min(y, height)
        # min by 1 because 0 is error
        if not allow_negative:
            self.x = max(self.x, 1)
            self.y = max(self.y, 1)

        print(self.x, self.y)

        self.motor_x.write(f"{self.x}\n".encode())
        # Send the y angle to the Arduino for the y motor
        self.motor_y.write(f"{self.y}\n".encode())

        # Wait for both motors to reply with "OK"
        while True:
            x_response = self.motor_x.readline().decode().strip()
            y_response = self.motor_y.readline().decode().strip()
            # print(x_response, y_response)
            if x_response == "OK" and y_response == "OK":
                break

        for listener in self.pos_listeners:
            listener(self.x, self.y)

    def set_home(self):
        self.motor_x.write(bytes("HOME" + "\n", 'utf-8'))
        self.motor_y.write(bytes("HOME" + "\n", 'utf-8'))
        self.x = 0
        self.y = 0

        x = 0
        y = 0
        x_base = None
        y_base = None
        while True:
            try:
                self.serial_arduino.reset_input_buffer()
                str = self.serial_arduino.readline()
                print(str)
                x_base = chr(str[2])
                y_base = chr(str[6])

                print(x_base, y_base)

                if x_base != "1":
                    x -= 5
                if y_base != "1":
                    y -= 5

                if x_base == "1" and y_base == "1":
                    print("home")
                    self.motor_x.write(bytes("HOME" + "\n", 'utf-8'))
                    self.motor_y.write(bytes("HOME" + "\n", 'utf-8'))
                    self.x = 0
                    self.y = 0
                    break
                else:
                    # print("goto", x, y)
                    self.goto_absolute(x, y, True)
                    time.sleep(0.01)
            except IndexError:
                pass

    def get_current_position(self):
        return self.x, self.y

    def add_position_listener(self, listener):
        self.pos_listeners.append(listener)
        listener(self.x, self.y)
