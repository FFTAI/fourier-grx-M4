---
layout: default
title: Move by Offset (Prismatic Joint)
nav_order: 4.25
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Move by Offset (Prismatic Joint / Leg-Length Adjustment Joint)

## Task Info

Task ID (TID): **4207**

Task Description:

- Adjusts the leg length by a relative offset **based on the current measured position** (target position = measured position at task entry + offset).
- Difference from [Adjust Length (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_length_prismatic_joint) (absolute position command):
  the relative offset is independent of the calibrated zero point in joint space, so **it can be used for small-range fine-tuning even when the leg-length full point has not been recalibrated after a software restart** (the patient does not need to dismount for recalibration).
- The sign convention is the same as the "Adjust Length" task (the command is converted by `× -1.0` before being sent).

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Left thigh adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |
| Left shank adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |
| Right thigh adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |
| Right shank adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |

> ⚠️ **Note**:
>
> - The offset of a single command is clamped to `±0.02 m`. For larger adjustments, send multiple commands, or use the [Adjust Length (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_length_prismatic_joint) task.
> - The task motion follows an open-loop time profile (S-curve), and the task finish flag is set according to the profile. Small offsets (on the order of 0.001 m) may not be reached exactly due to joint friction/self-locking; refer to the actual measured position.

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
| Left thigh adjustment offset | `grx.virtual_panel_command_param_1` |
| Left shank adjustment offset | `grx.virtual_panel_command_param_2` |
| Right thigh adjustment offset | `grx.virtual_panel_command_param_3` |
| Right shank adjustment offset | `grx.virtual_panel_command_param_4` |

## Update Log

- Added in `fourier-grx` v4.4.38.
