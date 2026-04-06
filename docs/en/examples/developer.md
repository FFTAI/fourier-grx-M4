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

1. Start the example script directly on the robot controller to take control:
    ```bash
    # Activate the conda environment
    conda activate fourier-grx

    # Run the example script for your robot model.
    # The config file must be adjusted for your specific model; use a config file with the "_debug.yaml" suffix.
    python $HOME/Wiki-GRx-Deploy/developer/demo_{example_name}.py --config=$HOME/fourier-grx/config/{robot_model}/config_{robot_model}_debug.yaml
    ```

### Notes

1. The Developer Interface requires deeper knowledge of robot internals.
2. It is recommended to become familiar with the User Interface before using the Developer Interface.
3. Make sure to back up important configuration files.
4. When debugging, it is recommended to operate in a safe environment.

## Interface Examples

### System Control Examples

| Example Name   | Description                          | Code Path                            |
|----------------|--------------------------------------|--------------------------------------|
| Servo On       | Enable robot actuators               | `developer/demo_servo_on.py`         |
| Servo Off      | Disable robot actuators              | `developer/demo_servo_off.py`        |
| Servo Reboot   | Reboot robot actuators               | `developer/demo_servo_reboot.py`     |
| State Monitor  | Print robot state information        | `developer/demo_print_state.py`      |
| Parameter Config | Set joint PID parameters           | `developer/demo_set_pid.py`          |
| Set Home       | Set robot home (zero) position       | `developer/demo_set_home.py`         |

### Motion Control Examples

| Example Name  | Description                                   | Code Path                          |
|---------------|-----------------------------------------------|------------------------------------|
| Move Joint    | Move a robot joint to a specified angle       | `developer/demo_move_joint.py`     |
