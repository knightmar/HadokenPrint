import serial
from serial.serialutil import SerialException

width = 2000
height = 1000


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

    def goto_absolute(self, x, y):
        if x == 0:
            x = 1
        if y == 0:
            y = 1

        print("starting move")
        self.x = min(x, width)
        self.y = min(y, height)
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)

        self.motor_x.write(f"{x}\n".encode())
        # Send the y angle to the Arduino for the y motor
        self.motor_y.write(f"{y}\n".encode())

        # Wait for both motors to reply with "OK"
        while True:
            x_response = self.motor_x.readline().decode().strip()
            y_response = self.motor_y.readline().decode().strip()
            print(x_response, y_response)
            if x_response == "OK" and y_response == "OK":
                break

    def set_home(self):
        self.motor_x.write(bytes("HOME" + "\n", 'utf-8'))
        self.motor_y.write(bytes("HOME" + "\n", 'utf-8'))

    def get_current_position(self):
        return self.x, self.y

    def add_position_listener(self, listener):
        self.pos_listeners.append(listener)
        listener(self.x, self.y)
