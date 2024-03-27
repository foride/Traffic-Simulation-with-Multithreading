import tkinter as tk
from threading import Thread
import random
import time

# Define colors
RED = "#ff0000"
GREEN = "#00ff00"
GREY = "#a0a0a0"
WHITE = "#ffffff"
COLORS = [f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}' for _ in range(10)]

# Set the dimensions of the window
window_width = 1280
window_height = 720

# Define starting positions based on the side of the screen
START_POSITIONS = {
    'left': (0, window_height // 2 + 25),
    'right': (window_width - 30, window_height // 2 - 25),
    'top': (window_width // 2 + 25, 0),
    'bottom': (window_width // 2 - 25, window_height - 15)
}

# Define car dimensions
CAR_WIDTH, CAR_HEIGHT = 30, 15


class TrafficSimulation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack()
        self.draw_intersection()
        self.cars = []  # Keep track of cars (threads) for cleanup
        self.bind("<Key>", self.key_handler)  # Bind arrow keys to the key_handler method

    def start_simulation(self):
        pass

    def add_car(self, start_side):
        color = random.choice(COLORS)
        if start_side == 'left':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x + CAR_WIDTH, y + CAR_HEIGHT, fill=color)
            move_func = lambda: self.move_car(car, 5, 0)
        elif start_side == 'right':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x - CAR_WIDTH, y + CAR_HEIGHT, fill=color)
            move_func = lambda: self.move_car(car, -5, 0)
        elif start_side == 'top':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x + CAR_HEIGHT, y + CAR_WIDTH, fill=color)
            move_func = lambda: self.move_car(car, 0, 5)
        elif start_side == 'bottom':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x + CAR_HEIGHT, y - CAR_WIDTH, fill=color)
            move_func = lambda: self.move_car(car, 0, -5)

        car_thread = Thread(target=move_func)
        car_thread.start()
        self.cars.append(car_thread)

    def move_car(self, car, dx, dy):
        while True:
            self.canvas.move(car, dx, dy)
            self.canvas.update()
            pos = self.canvas.coords(car)
            # Check if car has exited the screen, and stop the thread if it has
            if pos[2] < 0 or pos[0] > window_width or pos[3] < 0 or pos[1] > window_height:
                break
            time.sleep(0.01)

    def draw_intersection(self):
        # Fill background with green
        self.canvas.create_rectangle(0, 0, window_width, window_height, fill=GREEN, outline=GREEN)

        # Draw the vertical road
        self.canvas.create_rectangle(window_width // 2 - 50, 0, window_width // 2 + 50, window_height, fill=GREY,
                                     outline=GREY)
        # Draw the horizontal road
        self.canvas.create_rectangle(0, window_height // 2 - 50, window_width, window_height // 2 + 50, fill=GREY,
                                     outline=GREY)

        # Draw the dashed lines in the vertical and horizontal roads
        for i in range(10, window_height, 40):
            self.canvas.create_line(window_width // 2, i, window_width // 2, i + 20, fill=WHITE, width=5)
        for i in range(10, window_width, 40):
            self.canvas.create_line(i, window_height // 2, i + 20, window_height // 2, fill=WHITE, width=5)

        # Draw the stop lines for the intersection
        # Horizontal stop lines
        self.canvas.create_line(0, window_height // 2 - 50, window_width // 2 - 50, window_height // 2 - 50, fill=WHITE,
                                width=5)
        self.canvas.create_line(window_width // 2 + 50, window_height // 2 - 50, window_width, window_height // 2 - 50,
                                fill=WHITE, width=5)
        self.canvas.create_line(0, window_height // 2 + 50, window_width // 2 - 50, window_height // 2 + 50, fill=WHITE,
                                width=5)
        self.canvas.create_line(window_width // 2 + 50, window_height // 2 + 50, window_width, window_height // 2 + 50,
                                fill=WHITE, width=5)
        # Vertical stop lines
        self.canvas.create_line(window_width // 2 - 50, 0, window_width // 2 - 50, window_height // 2 - 50, fill=WHITE,
                                width=5)
        self.canvas.create_line(window_width // 2 - 50, window_height // 2 + 50, window_width // 2 - 50, window_height,
                                fill=WHITE, width=5)
        self.canvas.create_line(window_width // 2 + 50, 0, window_width // 2 + 50, window_height // 2 - 50, fill=WHITE,
                                width=5)
        self.canvas.create_line(window_width // 2 + 50, window_height // 2 + 50, window_width // 2 + 50, window_height,
                                fill=WHITE, width=5)

    def key_handler(self, event):
        side_map = {'Up': 'top', 'Down': 'bottom', 'Left': 'left', 'Right': 'right'}
        if event.keysym in side_map:
            self.add_car(side_map[event.keysym])


def main():
    app = TrafficSimulation()
    app.title("Traffic Simulation")

    app.mainloop()


if __name__ == "__main__":
    main()
