import tkinter as tk

import motor_manager

speed = 50

# direction enum
TOP = 1
BOTTOM = 2
LEFT = 3
RIGHT = 4

manager = motor_manager.MotorManager('/dev/ttyACM0', None)


def move(direction):
    if direction == 1:
        manager.goto(0, speed)
    elif direction == 2:
        manager.goto(0, -speed)
    elif direction == 3:
        manager.goto(speed, 0)
    elif direction == 4:
        manager.goto(-speed, 0)


def move_panel_setup(window):
    horizontal_move_frame = tk.Frame(window)
    vertical_move_frame = tk.Frame(window)

    up_button = tk.Button(vertical_move_frame, text="Up", command=lambda:move(1))
    down_button = tk.Button(vertical_move_frame, text="Down")

    up_button.pack(side=tk.TOP, expand=True)
    down_button.pack(side=tk.BOTTOM, expand=True)

    vertical_move_frame.pack(side=tk.RIGHT, expand=True)

    left_button = tk.Button(horizontal_move_frame, text="Left")
    right_button = tk.Button(horizontal_move_frame, text="Right")

    left_button.pack(side=tk.LEFT, expand=True)
    right_button.pack(side=tk.RIGHT, expand=True)

    horizontal_move_frame.pack(side=tk.LEFT, expand=True)


def run():
    window = tk.Tk()
    window.wm_minsize(300, 200)

    move_panel_setup(window)

    window.mainloop()


run()
