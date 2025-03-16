import tkinter as tk
from tkinter import filedialog
import math

from matplotlib import pyplot as plt

from PIL import Image, ImageTk, ImageOps

from python.utils import motor_manager, image_manager


class FileInterface:
    def __init__(self, master):
        self.master = master
        load_file_button = tk.Button(master, text="Load file", command=self.load_file)
        load_file_button.pack()
        self.canevas = tk.Canvas(master, width=motor_manager.width, height=motor_manager.height, bg="white")
        self.canevas.pack()


        self.image = None
        self.pil_image = None

        self.file_frame = tk.Frame(self.master)
        self.pixel_list = []

        self.file_frame.pack()



    def load_file(self):
        file_path = tk.filedialog.askopenfilename(defaultextension=".svg",
                                                  filetypes=[("PNG files", "*.svg"), ("JPG files", "*.jpg")])
        if not file_path:
            return
        points = image_manager.extract_points_from_svg(file_path)
        self.pixel_list = points

        for point in points:
            self.canevas.create_oval(point[0], point[1], point[0] + 1, point[1] + 1, fill="black")