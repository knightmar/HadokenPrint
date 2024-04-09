import tkinter as tk

from python.utils import motor_manager


class SlicerInterface:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=motor_manager.width, height=motor_manager.height, bg="white")
        self.canvas.pack()

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.save_button = tk.Button(master, text="Save", command=self.save)
        self.save_button.pack()

    def reset(self):
        pass

    def save(self):
        pass
