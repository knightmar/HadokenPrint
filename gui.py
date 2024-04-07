import tkinter as tk

import motor_manager

speed = 50

# direction enum
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


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
        self.canvas.bind("<B1-Motion>", self.move_joystick)

        # Display coordinates
        self.label = tk.Label(master, text="X: {} Y: {}".format(self.x, self.y))
        self.label.pack()

    def draw_joystick(self):
        self.canvas.delete("joystick")
        self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="red", tags="joystick")

    def move_joystick(self, event):
        self.x = event.x
        self.y = event.y
        self.draw_joystick()
        self.update_label()
        self.manager.goto_absolute(self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.draw_joystick()
        self.update_label()

    def update_label(self):
        self.label.config(text="X: {} Y: {}".format(self.x, self.y))


class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_minsize(300, 200)
        self.manager = motor_manager.MotorManager('/dev/ttyACM0', None)

        self.move_panel_setup()

    def run(self):
        self.window.mainloop()

    def move(self, direction):
        if direction == UP:
            self.manager.goto_relative(0, -speed)
        elif direction == DOWN:
            self.manager.goto_relative(0, speed)
        elif direction == LEFT:
            self.manager.goto_relative(-speed, 0)
        elif direction == RIGHT:
            self.manager.goto_relative(speed, 0)

    def move_panel_setup(self):
        buttons_move_frame = tk.Frame(self.window)

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

        joystick = Joystick(self.window, self.manager)
        self.manager.add_position_listener(joystick.set_position)

    def update_gui(self):
        pass


if __name__ == '__main__':
    gui = Gui()
    gui.run()
