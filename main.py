import tkinter as tk
from threading import Thread, Event, Lock
from threading import Semaphore
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
    'top': (window_width // 2 - 25, 0),
    'bottom': (window_width // 2 + 25, window_height - 15)
}

# Define car dimensions
CAR_WIDTH, CAR_HEIGHT = 30, 15


class TrafficSimulation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack()
        self.draw_intersection()
        self.intersection_crossed_counter = 0
        self.counter_lock = Lock()
        self.bind("<Key>", self.key_handler)  # Bind arrow keys to the key_handler method
        self.stop_event = Event()
        self.semaphore_top = Semaphore(1)  # Initially green
        self.semaphore_bottom = Semaphore(1)  # Initially green
        self.semaphore_left = Semaphore(0)  # Initially red
        self.semaphore_right = Semaphore(0)  # Initially red

        self.traffic_light_thread = Thread(target=self.change_traffic_lights)
        self.traffic_light_thread.start()

        self.cars = {'left': [], 'right': [], 'top': [], 'bottom': []}  # Cars by direction



        self.traffic_light_drawings = {
            'top': self.canvas.create_oval(window_width // 2 + 55, 10, window_width // 2 + 85, 40, fill="green"),
            'bottom': self.canvas.create_oval(window_width // 2 - 85, window_height - 40, window_width // 2 - 55,
                                              window_height - 10, fill="green"),

            'left': self.canvas.create_oval(10, window_height // 2 - 85, 40, window_height // 2 - 55, fill="red"),

            'right': self.canvas.create_oval(window_width - 40, window_height // 2 + 55, window_width - 10,
                                             window_height // 2 + 85, fill="red"),
        }

    def change_traffic_lights(self):
        while not self.stop_event.is_set():
            time.sleep(5)  # Change lights every 5 seconds
            print(f'{self.intersection_crossed_counter} cars has crossed the intersection')
            # Toggle the state of each traffic light
            self.toggle_semaphore(self.semaphore_top, 'top')
            self.toggle_semaphore(self.semaphore_bottom, 'bottom')
            self.toggle_semaphore(self.semaphore_left, 'left')
            self.toggle_semaphore(self.semaphore_right, 'right')

    def toggle_semaphore(self, semaphore, direction):
        if semaphore._value == 0:  # If the semaphore is "red"
            semaphore.release()  # Change to "green"
            color = "green"
        else:
            semaphore.acquire(False)  # Change to "red", non-blocking acquire
            color = "red"
            # Schedule the GUI update on the main thread
        self.after(0, lambda: self.canvas.itemconfig(self.traffic_light_drawings[direction], fill=color))

    def add_car(self, start_side):
        color = random.choice(COLORS)

        x, y = START_POSITIONS[start_side]
        orientation = 'horizontal' if start_side in ['left', 'right'] else 'vertical'
        if orientation == 'horizontal':
            car = self.canvas.create_rectangle(x, y, x + CAR_WIDTH, y + CAR_HEIGHT, fill=color)
            dx, dy = (5 if start_side == 'left' else -5), 0
        else:
            car = self.canvas.create_rectangle(x, y, x + CAR_HEIGHT, y + CAR_WIDTH, fill=color)
            dx, dy = 0, (5 if start_side == 'top' else -5)

        def move_func():
            self.cars[start_side].append(car)  # Store reference to car
            self.move_car(car, dx, dy, start_side, orientation)

        car_thread = Thread(target=move_func)
        car_thread.start()

    def move_car(self, car, dx, dy, start_side, orientation):
        semaphore = self.get_semaphore_for_side(start_side)
        approaching_intersection = False
        has_decided = False  # Flag to ensure the decision is made only once

        while not self.stop_event.is_set():
            self.check_collision_and_move(car, dx, dy, start_side)
            pos = self.canvas.coords(car)

            # Check if the car is near the intersection
            if not approaching_intersection and (
                    (start_side == 'top' and pos[3] > window_height // 2 - 60) or
                    (start_side == 'bottom' and pos[1] < window_height // 2 + 60) or
                    (start_side == 'left' and pos[2] > window_width // 2 - 60) or
                    (start_side == 'right' and pos[0] < window_width // 2 + 60)
            ):
                approaching_intersection = True
                semaphore.acquire()
                semaphore.release()

            if approaching_intersection and (
                    (start_side == 'top' and pos[3] > window_height // 2 - 10) or
                    (start_side == 'bottom' and pos[1] < window_height // 2 + 10) or
                    (start_side == 'left' and pos[2] > window_width // 2 - 10) or
                    (start_side == 'right' and pos[0] < window_width // 2 + 10)
            ):
                if not has_decided:
                    decision = random.choice(['straight', 'left', 'right'])

                    if decision == 'left':
                        dx, dy = -dy, dx
                        orientation = 'horizontal' if orientation == 'vertical' else 'vertical'
                        self.update_car_orientation(car, orientation, pos)
                    elif decision == 'right':
                        dx, dy = dy, -dx
                        orientation = 'horizontal' if orientation == 'vertical' else 'vertical'
                        self.update_car_orientation(car, orientation, pos)

                    has_decided = True

            # Car movement logic
            self.canvas.move(car, dx, dy)
            self.canvas.update()
            pos = self.canvas.coords(car)

            # Check if the car has exited the screen, and stop the thread if it has
            if pos[2] < 0 or pos[0] > window_width or pos[3] < 0 or pos[1] > window_height:
                with self.counter_lock:
                    self.intersection_crossed_counter += 1
                    self.cars[start_side].remove(car)
            time.sleep(0.01)

    def check_collision_and_move(self, car, dx, dy, start_side):
        idx = self.cars[start_side].index(car)
        if idx > 0:  # Check if there is a car in front
            prev_car = self.cars[start_side][idx - 1]
            index = 0
            while True:
                my_pos = self.canvas.coords(car)
                prev_pos = self.canvas.coords(prev_car)

                if self.calculate_distance(my_pos, prev_pos) < 45:
                    time.sleep(0.01)  # Halt for a second if too close
                    index += 1
                    if index > 400:
                        break
                    continue
                break
        self.canvas.move(car, dx, dy)

    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) if pos1[0] != pos2[0] else abs(pos1[1] - pos2[1])

    def update_car_orientation(self, car, orientation, pos):
        if orientation == 'horizontal':
            self.canvas.coords(car, pos[0], pos[1], pos[0] + CAR_WIDTH, pos[1] + CAR_HEIGHT)
        else:
            self.canvas.coords(car, pos[0], pos[1], pos[0] + CAR_HEIGHT, pos[1] + CAR_WIDTH)

    def get_semaphore_for_side(self, start_side):
        if start_side == 'top':
            return self.semaphore_top
        elif start_side == 'bottom':
            return self.semaphore_bottom
        elif start_side == 'left':
            return self.semaphore_left
        elif start_side == 'right':
            return self.semaphore_right

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
        if event.char in ('q', 'Q'):
            self.stop_event.set()  # Signal all threads to stop
            # Schedule the application to quit shortly, giving threads a moment to cease operations
            self.after(5000, self.quit_application)

    def quit_application(self):
        # Perform any necessary cleanup
        self.quit()  # Close the Tkinter window
        self.destroy()  # Ensure the application is terminated


def main():
    app = TrafficSimulation()
    app.title("Traffic Simulation")

    app.mainloop()


if __name__ == "__main__":
    main()
