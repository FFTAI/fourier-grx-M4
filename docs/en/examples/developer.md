---
layout: default
title: Developer Interface
nav_order: 2.2
parent: "Examples"
nav_exclude: true
toc: true
toc_min_header: 2
toc_max_header: 3
---

# Developer Interface

The Fourier-GRX Developer Interface is a secondary development interface provided for low-level development.
It calls the underlying hardware interfaces directly and is intended for low-level development work.

To guarantee real-time performance, these examples must be run on the robot controller.

## How to Run

> ⚠️ A Developer-interface example *is* the robot control program: it initializes the hardware and runs the control loop inside its own process.
> Stop the running `fourier-grx` main program first, otherwise two processes will contend for the same actuators:
>
> ```bash
> # Stop the main program on the robot controller
> fourier-grx stop
> ```

1. Start the example on the robot controller to take direct control:
    ```bash
    # Activate the development environment (virtual environment at $HOME/fourier-grx/.venv)
    source $HOME/fourier-grx/.venv/bin/activate

    # Clone the example code repository (if not already cloned)
    git clone https://github.com/FFTAI/fourier-grx-M4.git

    # Enter the demo directory and run an example; --config specifies the config file for your robot model
    cd fourier-grx-M4/demo/developer
    python demo_{example_name}.py --config=config_M4L_T1_developer.yaml
    ```

   On startup the script prints a dictionary with the `fourier_core` / `fourier_grx` versions, initializes the hardware from the `--config` file, and then runs the control loop on a background thread inside the example's own process; the process exits once the example's algorithm function returns.
   A relative `--config` path is resolved against the current working directory, so either run from `demo/developer` or pass an absolute path.

### Notes

1. The Developer Interface requires deeper knowledge of robot internals.
2. It is recommended to become familiar with the User Interface before using the Developer Interface.
3. Make sure to back up important configuration files.
4. When debugging, it is recommended to operate in a safe environment.

## Interface Examples

### System Control Examples

| Example Name   | Description                          | Code Path                            |
|----------------|--------------------------------------|--------------------------------------|
| Servo On       | Enable robot actuators               | `demo/developer/demo_servo_on.py`         |
| Servo Off      | Disable robot actuators              | `demo/developer/demo_servo_off.py`        |
| Servo Reboot   | Reboot robot actuators               | `demo/developer/demo_servo_reboot.py`     |
| State Monitor  | Print robot state information        | `demo/developer/demo_print_state.py`      |
| Parameter Config | Set joint PID parameters           | `demo/developer/demo_set_pid.py`          |
| Set Home       | Set robot home (zero) position       | `demo/developer/demo_set_home.py`         |

### Motion Control Examples

| Example Name  | Description                                   | Code Path                          |
|---------------|-----------------------------------------------|------------------------------------|
| Move Joint    | Move a robot joint to a specified angle       | `demo/developer/demo_move_joint.py`     |
