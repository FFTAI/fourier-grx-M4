---
layout: default
title: User Interface
nav_order: 2.1
parent: "Examples"
nav_exclude: true
toc: true
toc_min_header: 2
toc_max_header: 3
---

# User Interface

The Fourier-GRX User Interface communicates with the robot using the [Zenoh](https://zenoh.io/) protocol
and is designed for high-level application development.

You can run these examples on the robot controller or on any computer connected to the same LAN as the robot.

## How to Run

1. Configure `fourier-grx` to run in **developer mode** on the robot controller:
   ```
   # Edit the fourier-grx configuration
   fourier-grx config

   # Select developer mode as the run mode
   ```

2. Start the Fourier-GRX main program on the robot controller:
    ```bash
    # Start the `fourier-grx` main program
    fourier-grx start
    ```

3. Run the example script (can be executed on a remote host computer):
    ```bash
    # Activate the conda environment
    conda activate fourier-grx

    # Run the example script for your robot model
    python $HOME/Wiki-GRx-Deploy/user/demo_{example_name}.py
    ```

### Best Practices

- It is recommended to use multiple terminal windows to run and monitor programs simultaneously.
- Ensure a stable network connection when controlling the robot remotely.
- Read the relevant safety instructions carefully before running any example.

![Terminal Example](/fourier-grx-M4/assets/images/example_user_terminal.png)

## Interface Examples

### Basic Control Examples

| Example Name       | Description                        | Code Path                       |
|--------------------|------------------------------------|---------------------------------|
| Servo On           | Enable robot actuators             | `user/demo_servo_on.py`         |
| Servo Off          | Disable robot actuators            | `user/demo_servo_off.py`        |
| Servo Reboot       | Reboot robot actuators             | `user/demo_servo_reboot.py`     |
| Clear Fault        | Clear robot fault/alarm state      | `user/demo_clear_fault.py`      |
| Set Home           | Set current position as home (zero)| `user/demo_set_home.py`         |

### Motion Control Examples

| Example Name   | Description                              | Code Path                   |
|----------------|------------------------------------------|-----------------------------|
| Joint Test     | Test motion function of each joint       | `user/demo_test_joint.py`   |
| Walk Control   | Control robot walking with a joystick    | `user/demo_walk.py`         |
