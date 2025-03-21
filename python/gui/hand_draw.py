import ast
import csv
import tkinter as tk
from tkinter import filedialog

from python.utils import motor_manager


class HandDrawInterface:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=motor_manager.width, height=motor_manager.height, bg="white")
        self.canvas.bind("<B1-Motion>", self.draw_pixels)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.save_button = tk.Button(master, text="Save", command=self.save)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load", command=self.load)
        self.load_button.pack()

        self.canvas.pack()

        self.pixel_list = []
        self.current_line = []

    def reset(self):
        self.canvas.delete("all")
        self.pixel_list = []
        self.current_line = []

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
        with open(file_path, 'r') as myfile:
            reader = csv.reader(myfile, quoting=csv.QUOTE_ALL)
            self.pixel_list = [[ast.literal_eval(point) for point in line] for line in reader]
        self.update_canvas()

    def draw_pixels(self, event):
        self.canvas.create_rectangle(event.x, event.y, event.x + 1, event.y + 1, fill="black")
        if not (event.x, event.y) in self.current_line:
            self.current_line.append((event.x, event.y))

    def end_line(self, event):
        if self.current_line:
            self.pixel_list.append(self.current_line)
            self.current_line = []
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        for line in self.pixel_list:
            previous = None
            for x, y in line:
                if previous:
                    self.canvas.create_line(previous[0], previous[1], x, y, fill="black")
                else:
                    self.canvas.create_rectangle(x, y, x + 1, y + 1, fill="black")
                previous = (x, y)
