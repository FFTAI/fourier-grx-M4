---
layout: default
title: Stand Motion Control (Knee Restriction)
nav_order: 4.13
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Stand Motion Control (Knee Restriction)

## Task Info

Task ID (TID): **4300**

Task Description:

- The robot slowly moves all joints back to the standing posture.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Minimum bend angle limit for the left knee joint, in rad. The knee joint angle in the motion trajectory will never fall below this value (i.e., it will not over-extend beyond this limit). 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Minimum bend angle limit for the right knee joint, in rad. The knee joint angle in the motion trajectory will never fall below this value (i.e., it will not over-extend beyond this limit). 0.0 means no restriction (full extension allowed). |

> **Knee Restriction Angle Explained**:
>
> This parameter sets the minimum bend angle the knee joint must maintain throughout the entire motion (unit: rad). The algorithm clamps any knee joint angle in the trajectory that falls below this value to the specified value, ensuring the knee never extends beyond the set limit. Designed for patients whose knee extension function is restricted and who cannot fully straighten the knee.
>
> | Restriction Angle | Effect |
> |-------------------|--------|
> | 0.0 | No restriction; knee can fully extend (default) |
> | 0.3 | Knee maintains at least ~17° of bend throughout motion |
> | 0.5 | Knee maintains at least ~28.6° of bend throughout motion |
> | 1.0 | Knee maintains at least ~57.3° of bend throughout motion (strong restriction) |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |

Command interface:

- The upper leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.
- The lower leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.

| Parameter | Interface Mapping |
|-----------|------------------|
| Upper leg length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Lower leg length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Update Log

- Added in `fourier-grx` v1.0.0.
