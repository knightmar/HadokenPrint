import tkinter as tk


class PrinterInterface:
    def __init__(self, master, motor_manager, slicer, file):
        self.master = master
        self.motor_manager = motor_manager
        self.slicer = slicer
        self.file = file

        self.print_source_frame = tk.Frame(self.master)

        self.selected_source = tk.IntVar()
        source_file = tk.Radiobutton(self.print_source_frame, text="Print from file", value=1,
                                     variable=self.selected_source)
        source_slicer = tk.Radiobutton(self.print_source_frame, text="Print from slicer tab", value=2,
                                       variable=self.selected_source)

        source_file.pack(expand=True, padx=100, pady=50)
        source_slicer.pack(expand=True, padx=100, pady=50)

        self.print_source_frame.pack()

        print_button = tk.Button(master, text="Print", command=self.print)
        print_button.pack()

    def print(self):
        if self.selected_source.get() == 1:  # Print from file
            point_list = self.file.pixel_list
        else:
            point_list = self.slicer.pixel_list[0]  # Print from slicer tab

        print(point_list)

        for point in point_list:
            self.motor_manager.goto_absolute(point[0], point[1])
