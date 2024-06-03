# Traffic Simulation

This Python-based project uses Tkinter to simulate traffic at an intersection, demonstrating concepts of multithreading, semaphore-based synchronization, user interaction, and collision avoidance.

![Picture of Traffic Simulation](game.png)

## Features

- **Graphical Interface**: Utilizes Tkinter to visually represent an intersection complete with traffic lights, providing a simple and intuitive display.
- **Multithreading**: Leverages multiple threads to simulate independent vehicle movements and traffic light controls, enhancing the simulation's realism and complexity.
- **Semaphore Synchronization**: Employs semaphores to manage the flow of traffic through the intersection effectively. This ensures that traffic lights coordinate smoothly, preventing gridlock and enhancing safety.
- **Dynamic User Interaction**: Allows users to spawn cars in real-time by pressing arrow keys, simulating incoming traffic from different directions.
- **Safe Application Termination**: Provides a safe shutdown process by capturing the "Q" key event, ensuring all threads are gracefully stopped before the application exits to prevent data corruption or application crashes.
- **Collision Avoidance**: Uses a non-blocking collision detection system to maintain a safe distance between cars, thereby preventing accidents.
- **Dynamic Car Orientation**: Supports random directional changes at intersections, with visual representation reflecting the car's new travel direction.

## Detailed Thread and Synchronization Mechanism Description

### Main Window Thread

- Responsible for drawing the interface.
- Processing events from the event queue.
- Updating the graphical components.

### Car Threads

- Calculating positions.
- Checking semaphore status (traffic lights).
- Handling collision detection and avoidance.
- Redrawing the car in its new position with appropriate orientation after turns.

### Traffic Light Thread

- Regularly toggles the state of the traffic lights from green to red and vice versa.
- Allows or prevents car threads from proceeding through the intersection based on semaphore state.

### Semaphore Implementation and Usage

- **Semaphores** are used to control the traffic lights, which in turn regulate the flow of cars through the intersection. Each direction (top, bottom, left, right) has a corresponding semaphore that signals whether cars can proceed or must wait.
    - `semaphore_top` and `semaphore_bottom`: These semaphores are initialized to 1 (green light) to allow traffic flow from top to bottom or vice versa at the start of the simulation.
    - `semaphore_left` and `semaphore_right`: These are initialized to 0 (red light) preventing traffic from flowing left to right or vice versa initially.
- **Semaphore Usage**:
    - **Checking before entering the intersection**: When a car approaches the intersection, it needs to acquire the semaphore. If the semaphore is green (_value is 1), the semaphore is acquired (decremented to 0), allowing the car to proceed. After passing the intersection, the semaphore is released (incremented back to 1), signaling that another car can proceed.
    - **Traffic light switching**: The `change_traffic_lights` method toggles each semaphore state regularly, simulating the traffic light change from red to green and vice versa. This controls when cars are allowed to proceed.

### Mutex (Lock)

- **Mutex Usage**:
    - **Incrementing the car counter**: When a car leaves the screen, it is removed from its list, and the `intersection_crossed_counter` is incremented. The lock (`counter_lock`) ensures that this increment operation does not conflict with other threads trying to do the same, thus maintaining the integrity of the data.
