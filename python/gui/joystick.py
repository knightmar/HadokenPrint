import tkinter as tk

from python.utils import motor_manager


class Joystick:
    def __init__(self, master, manager):
        self.master = master
        self.canvas = tk.Canvas(master, width=motor_manager.width, height=motor_manager.height, bg="white")
        self.canvas.pack()
        self.manager = manager

        # Joystick position
        self.x = motor_manager.width // 2
        self.y = motor_manager.height // 2

        # Draw joystick
        self.draw_joystick()

        # Bind mouse events
        self.canvas.bind("<B1-ButtonRelease>", self.release_joystick)
        self.canvas.bind("<B1-Motion>", self.move_joystick)

        # Display coordinates
        self.label = tk.Label(master, text="X: {} Y: {}".format(self.x, self.y))
        self.label.pack()

    def draw_joystick(self):
        self.canvas.delete("joystick")
        self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="red", tags="joystick")

    def release_joystick(self, event):
        self.x = event.x
        self.y = event.y
        self.draw_joystick()
        self.update_label()
        self.manager.goto_absolute(self.x, self.y)

    def move_joystick(self, event):
        self.x = event.x
        self.y = event.y
        self.draw_joystick()
        self.update_label()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.draw_joystick()
        self.update_label()

    def update_label(self):
        self.label.config(text="X: {} Y: {}".format(self.x, self.y))
