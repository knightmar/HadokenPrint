import tkinter as tk
from tkinter import filedialog
import math

from matplotlib import pyplot as plt

from PIL import Image, ImageTk, ImageOps

from python.utils import motor_manager


class FileInterface:
    def __init__(self, master):
        self.master = master
        self.canevas = tk.Canvas(master, width=motor_manager.width, height=motor_manager.height, bg="white")
        self.canevas.pack()

        self.canevas.bind("<Button-1>", self.update_canvas)
        self.canevas.bind("<B1-Motion>", self.update_canvas)
        self.canevas.bind("<Button-3>", self.rotate_image)
        self.canevas.bind("<B3-Motion>", self.rotate_image)

        self.image = None
        self.pil_image = None

        self.file_frame = tk.Frame(self.master)

        self.file_frame.pack()

        load_file_button = tk.Button(master, text="Load file", command=self.load_file)
        load_file_button.pack()

    def load_file(self):
        file_path = tk.filedialog.askopenfilename(defaultextension=".jpg",
                                                  filetypes=[("JPG files", "*.jpg"), ("PNG files", "*.png")])
        if not file_path:
            return
        self.pil_image = Image.open(file_path)
        self.pil_image = self.pil_image.convert('L')  # Convert image to black and white
        self.pil_image.thumbnail((motor_manager.width, motor_manager.height))
        print(self.pil_image.width)
        self.pil_image = crop_white_borders(self.pil_image)
        print(self.pil_image.width)
        self.image = ImageTk.PhotoImage(self.pil_image)  # Convert PIL.Image.Image to PhotoImage
        self.rotate_image(None)
        self.update_canvas(None)

    def rotate_image(self, event):
        if self.pil_image is not None:
            center_x = self.canevas.winfo_width() // 2
            center_y = self.canevas.winfo_height() // 2

            if event is None:
                x, y = center_x, center_y
            else:
                x, y = event.x, event.y

            # Calculate the angle
            dx = x - center_x
            dy = y - center_y
            angle = math.atan2(dy, dx)
            # Convert the angle to degrees
            angle = math.degrees(angle)

            # Add transparency layer
            pil_image = self.pil_image.convert("RGBA")

            # Create a new image with larger size
            larger_image = Image.new('RGBA', (pil_image.width * 2, pil_image.height * 2))

            # Paste the original image into the center of the new image
            larger_image.paste(pil_image, (pil_image.width // 2, pil_image.height // 2))

            # Rotate the larger image
            larger_image = larger_image.rotate(180 - angle)

            # Convert the rotated PIL image to a Tkinter PhotoImage
            self.image = ImageTk.PhotoImage(crop_white_borders(larger_image))

            # Update the canvas
            self.update_canvas(None)

    def update_canvas(self, event):
        if self.image is not None:
            self.canevas.delete("all")
            self.canevas.create_rectangle(0, 0, motor_manager.width, motor_manager.height,
                                          fill="white")

            # If there's no event, center the image
            if event is None:
                x = self.canevas.winfo_width() // 2
                y = self.canevas.winfo_height() // 2
            else:  # If there's an event, use the event's coordinates
                x = event.x
                y = event.y

            # Create the image at the event's coordinates
            self.canevas.create_image(x, y, image=self.image, anchor="center")


def crop_white_borders(img):
    min_x = img.width
    min_y = img.height
    max_x = 0
    max_y = 0

    for x in range(img.width):
        for y in range(img.height):
            if img.getpixel((x, y)) == 0:  # Black pixel
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    # Check if there are black pixels in the image
    if min_x <= max_x and min_y <= max_y:
        rect = (min_x, min_y, max_x, max_y)
        return img.crop(rect)
    else:
        # If there are no black pixels, return the original image
        return img
