# Traffic Simulation

This Python-based project uses Tkinter to simulate traffic at an intersection, demonstrating concepts of multithreading, semaphore-based synchronization, user interaction, and collision avoidance.

## Features

- **Graphical Interface**: Utilizes Tkinter for a simple and intuitive display of an intersection with traffic lights.
- **Multithreading**: Employs multiple threads to manage independent vehicle movements and traffic light controls.
- **Semaphore Synchronization**: Uses semaphores to regulate traffic through the intersection, preventing collisions and ensuring smooth flow.
- **Dynamic User Interaction**: Cars can be spawned in real-time at the press of arrow keys, simulating traffic from various directions.
- **Safe Application Termination**: Implements a safe shutdown process by pressing the "Q" keyboard key. All threads are stopped before the application exits, avoiding potential data corruption or crashes.
- **Collision Avoidance**: Implements a non-blocking collision detection system using thread semaphores to prevent cars from getting too close to each other.
- **Dynamic Car Orientation**: Cars can make random turns at intersections, visually rotating to match their new direction of travel.

## The Project's Thread Breakdown

### Main Window Thread

- Responsible for drawing the interface.
- Processing events from the event queue.
- Updating the graphical components.

### Car Threads

Each car thread controls the movement of a car, including:
- Calculating positions.
- Checking semaphore status (traffic lights).
- Handling collision detection and avoidance.
- Redrawing the car in its new position with appropriate orientation after turns.

### Traffic Lights Thread

- Regularly toggles the state of the traffic lights from green to red and vice versa.
- Allows or prevents car threads from proceeding through the intersection based on semaphore state.

## The Project's Critical Section

### Variable: intersection_crossed_counter

Each car that drives through the intersection accesses and modifies the `intersection_crossed_counter`.

## Continuous Development

Upcoming features to enhance the simulation:
- **Enhanced Traffic Patterns**: Cars will drive at different speeds to simulate different traffic conditions.