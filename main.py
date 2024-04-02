import tkinter as tk
from threading import Thread, Event
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
        self.cars = []  # Keep track of cars (threads) for cleanup
        self.bind("<Key>", self.key_handler)  # Bind arrow keys to the key_handler method
        self.stop_event = Event()
        self.semaphore_top = Semaphore(1)  # Initially green
        self.semaphore_bottom = Semaphore(1)  # Initially green
        self.semaphore_left = Semaphore(0)  # Initially red
        self.semaphore_right = Semaphore(0)  # Initially red

        self.traffic_light_thread = Thread(target=self.change_traffic_lights)
        self.traffic_light_thread.start()

        self.traffic_light_drawings = {
            'top': self.canvas.create_oval(window_width // 2 + 55, 10, window_width // 2 + 85, 40, fill="green"),
            'bottom': self.canvas.create_oval(window_width // 2 - 85, window_height - 40, window_width // 2 - 55,
                                              window_height - 10, fill="green"),
            # Adjusting left traffic light to appear on the left side of the road
            'left': self.canvas.create_oval(10, window_height // 2 - 85, 40, window_height // 2 - 55, fill="red"),
            # Adjusting right traffic light to appear on the right side of the road
            'right': self.canvas.create_oval(window_width - 40, window_height // 2 + 55, window_width - 10,
                                             window_height // 2 + 85, fill="red"),
        }

    def start_simulation(self):
        pass

    def change_traffic_lights(self):
        while not self.stop_event.is_set():
            time.sleep(5)  # Change lights every 5 seconds
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

        if start_side == 'left':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x + CAR_WIDTH, y + CAR_HEIGHT, fill=color)
            dx, dy = 5, 0
        elif start_side == 'right':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x - CAR_WIDTH, y + CAR_HEIGHT, fill=color)
            dx, dy = -5, 0
        elif start_side == 'top':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x + CAR_HEIGHT, y + CAR_WIDTH, fill=color)
            dx, dy = 0, 5
        elif start_side == 'bottom':
            x, y = START_POSITIONS[start_side]
            car = self.canvas.create_rectangle(x, y, x + CAR_HEIGHT, y - CAR_WIDTH, fill=color)
            dx, dy = 0, -5
        else:
            print(f"Unexpected start_side: {start_side}")
            return  # Exit the function if start_side is not recognized

        def move_func():
            self.move_car(car, dx, dy, start_side)

        car_thread = Thread(target=move_func)
        car_thread.start()
        self.cars.append(car_thread)

    def move_car(self, car, dx, dy, start_side):

        semaphore = self.get_semaphore_for_side(start_side)
        approaching_intersection = False

        while not self.stop_event.is_set():
            pos = self.canvas.coords(car)

            if start_side == 'top' and not approaching_intersection:
                if pos[3] > window_height // 2 - 60:
                    approaching_intersection = True
                    semaphore.acquire()
                    semaphore.release()
            elif start_side == 'bottom' and not approaching_intersection:
                if pos[1] < window_height // 2 + 60:
                    approaching_intersection = True
                    semaphore.acquire()
                    semaphore.release()
            elif start_side == 'left' and not approaching_intersection:
                if pos[2] > window_width // 2 - 60:
                    approaching_intersection = True
                    semaphore.acquire()
                    semaphore.release()
            elif start_side == 'right' and not approaching_intersection:
                if pos[0] < window_width // 2 + 60:
                    approaching_intersection = True
                    semaphore.acquire()
                    semaphore.release()

            # Car movement logic
            self.canvas.move(car, dx, dy)
            self.canvas.update()
            pos = self.canvas.coords(car)

            # Check if car has exited the screen, and stop the thread if it has
            if pos[2] < 0 or pos[0] > window_width or pos[3] < 0 or pos[1] > window_height:
                break
            time.sleep(0.01)

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
