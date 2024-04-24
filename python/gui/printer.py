import tkinter as tk

from python.utils import motor_manager


class PrinterInterface:
    def __init__(self, master):
        self.master = master

        self.print_source_frame = tk.Frame(self.master)

        source_file = tk.Radiobutton(self.print_source_frame, text="Print from file", value=1)
        source_slicer = tk.Radiobutton(self.print_source_frame, text="Print from slicer tab", value=2)

        source_file.pack(expand=True, padx=100, pady=50)
        source_slicer.pack(expand=True, padx=100, pady=50)

        self.print_source_frame.pack()

        print_button = tk.Button(master, text="Print")
        print_button.pack()
