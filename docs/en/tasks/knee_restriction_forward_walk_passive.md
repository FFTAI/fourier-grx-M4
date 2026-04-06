---
layout: default
title: Passive Forward Walk (Knee Restriction)
nav_order: 4.14
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Passive Forward Walk (Knee Restriction)

## Task Info

Task ID (TID): **4301**

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for forward walking, and the actuators track that trajectory to achieve passive forward walking.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Minimum bend angle limit for the left knee joint, in rad. The knee joint angle in the motion trajectory will never fall below this value (i.e., it will not over-extend beyond this limit). 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Minimum bend angle limit for the right knee joint, in rad. The knee joint angle in the motion trajectory will never fall below this value (i.e., it will not over-extend beyond this limit). 0.0 means no restriction (full extension allowed). |
| Step length | `float` | 0.5 | [0.2, 0.8] | The length of each step, in m. |
| Walking speed | `float` | 0.5 | [0.1, 1.2] | The target forward speed, in m/s. Single-step duration = step length ÷ walking speed (e.g., with step length 0.5 m and speed 0.5 m/s, each step takes approximately 1.0 s). |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue walking. |


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

> Recommendation:
> - A step length between 0.5× and 1.0× the walking speed tends to produce good walking results. For example, at a walking speed of 0.5 m/s, a step length of 0.25 m to 0.5 m is recommended.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

Command interface:

- The upper leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.
- The lower leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.

| Parameter | Interface Mapping |
|-----------|------------------|
| Upper leg length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Lower leg length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` |
| Step length | `grx.virtual_panel_command_param_1` |
| Walking speed | `grx.virtual_panel_command_param_2` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Update Log

- Added in `fourier-grx` v4.2.2.
