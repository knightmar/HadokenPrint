import tkinter as tk
from tkinter import filedialog
import math

from matplotlib import pyplot as plt

from python.utils import motor_manager
from PIL import Image, ImageTk, ImageOps


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
        self.pil_image.thumbnail((motor_manager.width, motor_manager.height))
        self.pil_image = crop_white_borders(self.pil_image)
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
            # Rotate the PIL image
            pil_image = pil_image.rotate(360 - angle, expand=True)
            self.pil_image = crop_white_borders(self.pil_image)
        # Replace black color (also shades of blacks)
            # (0, 0, 0, 255) is black
            datas = pil_image.getdata()
            newData = []
            for item in datas:
                # change all black (also shades of blacks) pixels to transparent
                if item[0] < 10 and item[1] < 10 and item[2] < 10:  # Adjusted condition
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            pil_image.putdata(newData)
            # Convert the rotated PIL image to a Tkinter PhotoImage
            self.image = ImageTk.PhotoImage(pil_image)
            # Update the canvas
            self.update_canvas(None)

    def update_canvas(self, event):
        print("update canvas")
        if self.image is not None:
            self.canevas.delete("all")
            self.canevas.create_rectangle(0, 0, motor_manager.width, motor_manager.height, fill="white")
            if event is None:
                self.canevas.create_image(0, 0, image=self.image, anchor="nw")
            else:
                # Calculate the center of the image
                image_center_x = self.pil_image.width // 2
                image_center_y = self.pil_image.height // 2
                # Create the image at a position that is offset by half the width and height of the image from the mouse position
                self.canevas.create_image(event.x - image_center_x, event.y - image_center_y, image=self.image, anchor="nw")


def crop_white_borders(img):
    # Convert the image to grayscale
    grayscale_img = img.convert("L")
    # Invert the grayscale image
    inverted_img = ImageOps.invert(grayscale_img)
    # Get the bounding box
    box = inverted_img.getbbox()
    # Crop the image to the contents of the bounding box
    cropped_img = img.crop(box)
    return cropped_img
