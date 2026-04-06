---
layout: default
title: Passive Mark Time (Knee Restriction)
nav_order: 4.17
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Passive Mark Time (Knee Restriction)

## Task Info

Task ID (TID): **4302**

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for marching in place, and the actuators track that trajectory to achieve passive mark time.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Minimum bend angle limit for the left knee joint, in rad. The knee joint angle in the motion trajectory will never fall below this value (i.e., it will not over-extend beyond this limit). 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Minimum bend angle limit for the right knee joint, in rad. The knee joint angle in the motion trajectory will never fall below this value (i.e., it will not over-extend beyond this limit). 0.0 means no restriction (full extension allowed). |
| Step height | `float` | 0.1 | [0.1, 0.4] | The leg-lift height for each step, in m. |
| Step period | `float` | 1.0 | [0.5, 4.0] | The cycle duration for one complete stepping cycle, in s. A smaller value means a higher step frequency; a larger value means a slower step. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue stepping. |

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
| Step height | `grx.virtual_panel_command_param_1` |
| Step period | `grx.virtual_panel_command_param_2` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Update Log

- Added in `fourier-grx` v4.2.2.
