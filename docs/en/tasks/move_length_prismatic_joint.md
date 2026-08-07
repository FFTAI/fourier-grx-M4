---
layout: default
title: Adjust Length (Prismatic Joint)
nav_order: 4.24
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Adjust Length (Prismatic Joint / Leg-Length Adjustment Joint)

## Task Info

Task ID (TID): **4206**

Task Description:

- Adjust the leg length.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Left thigh adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's thigh, in m. |
| Left shank adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's shank, in m. |
| Right thigh adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's thigh, in m. |
| Right shank adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's shank, in m. |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |

Command Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Left thigh adjustment length | `grx.virtual_panel_command_param_1` |
| Left shank adjustment length | `grx.virtual_panel_command_param_2` |
| Right thigh adjustment length | `grx.virtual_panel_command_param_3` |
| Right shank adjustment length | `grx.virtual_panel_command_param_4` |

## Update Log

- `fourier-grx` v4.4.7: The upper limit of the thigh/shank adjustment length was changed from `0.090 m` to `0.095 m`, and the parameter range was updated to `[0.0, 0.095]`.
- Added in `fourier-grx` v4.1.22.
