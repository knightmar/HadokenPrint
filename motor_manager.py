import serial
from serial.serialutil import SerialException

width = 470
height = 350


class MotorManager:
    def __init__(self, serial_port_x, serial_port_y, baud=115200):
        self.x = 0
        self.y = 0
        self.motor_x = None
        self.motor_y = None
        self.pos_listeners = []

        try:
            self.motor_x = serial.Serial(serial_port_x, baudrate=baud)
            self.motor_y = serial.Serial(serial_port_y, baudrate=baud)

        except SerialException as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    def goto_relative(self, x, y):
        try:
            wanted_x = self.x + x
            wanted_y = self.y + y

            self.x = wanted_x
            self.y = wanted_y

            print("X : ", self.x, "Y : ", self.y)

            for listener in self.pos_listeners:
                listener(self.x, self.y)

            self.motor_x.write(bytes(str(x), 'utf-8'))
            self.motor_y.write(bytes(str(y), 'utf-8'))

        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    def goto_absolute(self, x, y):
        try:
            relative_x = min(max(0, x), width) - self.x
            relative_y = min(max(0, y), height) - self.y

            # Adjust relative_x and relative_y if either self.x or x is negative
            if self.x < 0 or x < 0:
                relative_x = x + abs(self.x)
            if self.y < 0 or y < 0:
                relative_y = y + abs(self.y)

            print(relative_x)
            self.goto_relative(relative_x, relative_y)

        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

    def get_current_position(self):
        return self.x, self.y

    def add_position_listener(self, listener):
        self.pos_listeners.append(listener)
        listener(self.x, self.y)
