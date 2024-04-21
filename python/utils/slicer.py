import csv
import tkinter as tk
from tkinter import filedialog

from python.utils import motor_manager


class SlicerInterface:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=motor_manager.width, height=motor_manager.height, bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.draw_pixels)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.save_button = tk.Button(master, text="Save", command=self.save)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load", command=self.load)
        self.load_button.pack()

        self.pixel_list = []

    def reset(self):
        self.canvas.delete("all")
        self.pixel_list = []

    def save(self):
        file_path = tk.filedialog.asksaveasfilename()
        if not file_path:
            return
        with open(file_path, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerows(self.pixel_list)

    def load(self):
        file_path = tk.filedialog.askopenfilename()
        if not file_path:
            return
        self.pixel_list = []
        with open(file_path, 'r') as myfile:
            reader = csv.reader(myfile, quoting=csv.QUOTE_ALL)
            for row in reader:
                x, y = map(int, row)
                self.pixel_list.append((x, y))
        self.update_canvas()

    def draw_pixels(self, event):
        if not (event.x, event.y) in self.pixel_list:
            self.pixel_list.append((event.x, event.y))
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        previous = None
        for x, y in self.pixel_list:
            if previous:
                self.canvas.create_line(previous[0], previous[1], x, y, fill="black")
            else:
                self.canvas.create_rectangle(x, y, x + 1, y + 1, fill="black")
            previous = (x, y)
