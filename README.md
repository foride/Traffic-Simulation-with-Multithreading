# Traffic Simulation

This Python-based project uses Tkinter to simulate traffic at an intersection, demonstrating concepts of multithreading, semaphore-based synchronization, and user interaction.

## Features

- **Graphical Interface**: Utilizes Tkinter for a simple and intuitive display of an intersection with traffic lights.
- **Multithreading**: Employs multiple threads to manage independent vehicle movements and traffic light controls.
- **Semaphore Synchronization**: Uses semaphores to regulate traffic through the intersection, preventing collisions and ensuring smooth flow.
- **Dynamic User Interaction**: Cars can be spawned in real-time at the press of arrow keys, simulating traffic from various directions.
- **Safe Application Termination**: Implements a safe shutdown process by pressing "Q" keyboard key. All threads are stopped before the application exits, avoiding potential data corruption or crashes.

## Continuous development

New functions to be added soon:
- **Cars collision prevention**: cars will avoid collisions
- **Cars can make turns**: Cars will make turns and behave more unpredictable


