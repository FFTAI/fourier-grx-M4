---
layout: default
title: Developer API
nav_order: 3.2
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Reference Guide — Developer API

* TOC
{:toc}

> ℹ️ **Note**:
>
> Before using the Fourier-GRX-M4 SDK Developer API, configure `fourier-grx` to **developer mode**.
> For information on configuring the run type, see [Run Type](/fourier-grx-M4/docs/en/reference/run_type).

The Fourier-GRX Developer API is a secondary development interface for low-level hardware access, designed for developers who need direct control over the underlying hardware. It is suitable for low-level development.

You must install the `fourier_core` and `fourier_grx` libraries in your Python environment before calling the library functions.

---

## State Dictionary (state dict)

The Fourier-GRX Developer API returns the robot's current state information through a state dictionary. The keys and values are as follows:

| Key              | Description              | Type                         | Unit  | Details                                                                                     |
|------------------|--------------------------|------------------------------|-------|---------------------------------------------------------------------------------------------|
| `joint_position` | Robot joint position     | array(float * num_of_joints) | rad   | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `joint_velocity` | Robot joint velocity     | array(float * num_of_joints) | rad/s | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `joint_kinetic`  | Robot joint torque       | array(float * num_of_joints) | Nm    | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |

## Control Dictionary (control dict)

The Fourier-GRX Developer API sends control commands to the robot through a control dictionary. The keys and values are as follows:

| Key                   | Description                            | Type                         | Unit  | Details                                                                                     |
|-----------------------|----------------------------------------|------------------------------|-------|---------------------------------------------------------------------------------------------|
| `control_mode`        | Robot control mode                     | int (float * num_of_joints)  |       | 0: no control, 1: current control, 2: torque control, 3: velocity control, 4: position control, 6: PD control |
| `position`            | Robot joint position command           | array(float * num_of_joints) | rad   | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `velocity`            | Robot joint velocity command           | array(float * num_of_joints) | rad/s | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `effort`              | Robot joint torque command             | array(float * num_of_joints) | Nm    | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `current`             | Robot joint current command            | array(float * num_of_joints) | A     | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `position_control_kp` | P gain for joint position control      | array(float * num_of_joints) |       | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `velocity_control_kp` | P gain for joint velocity control      | array(float * num_of_joints) |       | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `velocity_control_ki` | I gain for joint velocity control      | array(float * num_of_joints) |       | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `pd_control_kp`       | P gain for joint PD control            | array(float * num_of_joints) |       | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
| `pd_control_kd`       | D gain for joint PD control            | array(float * num_of_joints) |       | See [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence)                      |
