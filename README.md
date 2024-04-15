# Traffic Simulation

This Python-based project uses Tkinter to simulate traffic at an intersection, demonstrating concepts of multithreading, semaphore-based synchronization, and user interaction.

## Features

- **Graphical Interface**: Utilizes Tkinter for a simple and intuitive display of an intersection with traffic lights.
- **Multithreading**: Employs multiple threads to manage independent vehicle movements and traffic light controls.
- **Semaphore Synchronization**: Uses semaphores to regulate traffic through the intersection, preventing collisions and ensuring smooth flow.
- **Dynamic User Interaction**: Cars can be spawned in real-time at the press of arrow keys, simulating traffic from various directions.
- **Safe Application Termination**: Implements a safe shutdown process by pressing "Q" keyboard key. All threads are stopped before the application exits, avoiding potential data corruption or crashes.

## The project's thread breakdown

### Main Window Thread

- responsible for drawing the interface
- processing events from the even queue
- updating the graphical components

### Car Threads

Each car thread controls the movement of a car. This includes: 
- calculating positions
- checking semaphore stats ( traffic lights)
- redrawing the car in its new position

### Traffic lights Thread

- Regularly toggling the state of the traffic lights from green to red and vice versa
- allows or prevent car threads from proceeding through the intersection ( based on semaphore state )

## The project's critical section 

### Variable: intersection_crossed_counter

Each car that has drove through the intersection access and modifies the intersection_crossed_counter


## Continuous development

New functions to be added soon:
- **Cars collision prevention**: cars will avoid collisions
- **Cars can make turns**: Cars will make turns and behave more unpredictable


