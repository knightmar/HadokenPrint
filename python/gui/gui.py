import tkinter as tk
from tkinter import ttk

from python.gui.joystick import Joystick
from python.gui.printer import PrinterInterface
from python.utils import motor_manager
from python.gui.slicer import SlicerInterface

speed = 50

# direction enum
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

x_port = "/dev/ttyACM0"
y_port = None


class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_minsize(300, 200)
        self.motor_manager = motor_manager.MotorManager(x_port, y_port)

        self.move_panel_setup()

    def run(self):
        self.window.mainloop()

    def move(self, direction):
        if direction == UP:
            print("goto relative")
            self.motor_manager.goto_relative(0, -speed)
        elif direction == DOWN:
            self.motor_manager.goto_relative(0, speed)
        elif direction == LEFT:
            self.motor_manager.goto_relative(-speed, 0)
        elif direction == RIGHT:
            self.motor_manager.goto_relative(speed, 0)

    def move_panel_setup(self):
        notebook = ttk.Notebook(self.window)

        slicer_tab = ttk.Frame(notebook)
        joystick_tab = ttk.Frame(notebook)
        printer_tab = ttk.Frame(notebook)

        notebook.add(joystick_tab, text="Manual move")
        notebook.add(slicer_tab, text="Slicer")
        notebook.add(printer_tab, text="Printer")
        notebook.pack(expand=1, fill="both")

        buttons_move_frame = tk.Frame(joystick_tab)

        up_button = tk.Button(buttons_move_frame, text="Up", command=lambda: self.move(UP))
        down_button = tk.Button(buttons_move_frame, text="Down", command=lambda: self.move(DOWN))

        up_button.pack(side=tk.TOP, expand=True)
        down_button.pack(side=tk.BOTTOM, expand=True)

        left_button = tk.Button(buttons_move_frame, text="Left", command=lambda: self.move(LEFT))
        right_button = tk.Button(buttons_move_frame, text="Right", command=lambda: self.move(RIGHT))

        left_button.pack(side=tk.LEFT, expand=True)
        right_button.pack(side=tk.RIGHT, expand=True)

        buttons_move_frame.pack(side=tk.RIGHT, expand=True)

        self.window.bind("<Up>", lambda e: self.move(UP))
        self.window.bind("<Down>", lambda e: self.move(DOWN))
        self.window.bind("<Left>", lambda e: self.move(LEFT))
        self.window.bind("<Right>", lambda e: self.move(RIGHT))

        joystick = Joystick(joystick_tab, self.motor_manager)
        self.motor_manager.add_position_listener(joystick.set_position)

        SlicerInterface(slicer_tab)
        PrinterInterface(printer_tab)


if __name__ == '__main__':
    gui = Gui()
    gui.run()
