import threading
import time

import serial

current_x = 0
current_y = 0
wanted_x = 0
wanted_y = 0

run = True

serial_port_x = 'COM6'
serial_port_y = 'COM7'
baud = 115200

ser_x = serial.Serial(serial_port_x, baud)
ser_y = serial.Serial(serial_port_y, baud)


def goto(x=current_x, y=current_y):
    global wanted_x, wanted_y
    wanted_x = x
    wanted_y = y


def start():
    print("Starting...")
    goto(0, 0)
    threading.Thread(target=move_motors).start()


def stop():
    global run
    run = False


def move_motors():
    global current_x, current_y, wanted_x, wanted_y
    # Calculate the difference in angles
    while run:
        buffer_x = wanted_x
        buffer_y = wanted_y
        delta_x = buffer_x - current_x
        delta_y = buffer_y - current_y

        # Send the differences over serial
        ser_x.write(f"{delta_x}\n".encode())  # Convert to bytes and send
        ser_y.write(f"{delta_y}\n".encode())
        time.sleep(0.5)
        current_x = buffer_x
        current_y = buffer_y
