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
            self.x = self.x + x
            self.y = self.y + y

            if self.x < 0:
                self.x = 0
            if self.y < 0:
                self.y = 0
            if self.x > width:
                self.x = width
            if self.y > height:
                self.y = height

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
        x_diff = x - self.x
        y_diff = y - self.y

        self.goto_relative(x_diff, y_diff)

    def get_current_position(self):
        return self.x, self.y

    def add_position_listener(self, listener):
        self.pos_listeners.append(listener)
        listener(self.x, self.y)
