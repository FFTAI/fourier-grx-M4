---
layout: default
title: Assist Mark Time (Adjust dt Parameter)
nav_order: 4.12
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Assist Mark Time (Adjust dt Parameter)

## Task Info

Task ID (TID): **4119**

Task Description:

- The robot generates a joint motion trajectory sequence for mark time based on the given parameters, and drives the actuators to track that trajectory, achieving Assist Mark Time.
- When the "stop motion flag" is set to true, the robot will gradually slow down and stop rather than halting immediately.
- The assist intensity is controlled by the assist ratio: a higher value causes the trajectory to play faster (closer to normal step frequency); a lower value plays more slowly, giving the patient more time to follow the motion.
- An automatic assist mode is available. When the "auto assist mode flag" is enabled, the robot automatically adjusts the assist ratio every control cycle based on measured joint torques, without requiring manual setting.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Thigh length | `float` | 0.5 | [0.3, 0.6] | The robot's thigh length, in m. |
| Shank length | `float` | 0.5 | [0.3, 0.6] | The robot's shank length, in m. |
| Step lift height | `float` | 0.1 | [0.1, 0.4] | The leg lift height for each step, in m. |
| Step cycle | `float` | 1.0 | [0.5, 4.0] | The single-step cycle for mark time — the time required to complete one full stepping cycle, in s. A smaller value means a higher step frequency; a larger value means slower stepping. |
| Assist ratio | `float` | 0.5 | [0.0, 1.0] | The adjustment coefficient for trajectory playback speed, in the range [0.0, 1.0]. A higher value plays the trajectory faster (closer to normal step frequency); a lower value plays more slowly, giving the patient more time to follow the motion. |
| Auto assist mode flag | `bool` | false | (true, false) | Whether to enable automatic assist mode. When enabled, the system automatically adjusts the assist ratio (±0.01) every control cycle (20 ms) based on the deviation between measured joint torques and the reference trajectory, without manual setting. The assist ratio is always clamped to [0.0, 1.0]. |
| Start motion flag | `bool` | false | (true, false) | Whether to start the motion. true = start; false = do not start (has no effect if already started). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop the motion. true = stop; false = continue stepping. |

> **Assist Ratio Explanation**:
>
> The assist ratio controls the pace by adjusting the trajectory playback speed (play\_speed). The formula is:
>
> - **play\_speed** = 0.5 + assist\_ratio × 0.5, so play\_speed ∈ [0.5, 1.0]
> - Trajectory time advance per control cycle: Δt = 0.02 s × play\_speed
>
> | Assist Ratio | play\_speed | Effect |
> |-------------|-------------|--------|
> | 0.0 | 0.5 | Trajectory plays at 50% speed; each step takes twice the normal duration — suitable for patients with weak motor ability. |
> | 0.5 | 0.75 | Trajectory plays at 75% speed; moderate step frequency. |
> | 1.0 | 1.0 | Trajectory plays at normal speed — suitable for patients with near-normal motor ability. |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

Command Interface:

- Thigh length: only one value can be input in the algorithm; therefore the average of the left and right thigh lengths is used. Two values are passed, but only their average is used.
- Shank length: only one value can be input in the algorithm; therefore the average of the left and right shank lengths is used. Two values are passed, but only their average is used.

| Parameter | Interface Mapping |
|-----------|------------------|
| Thigh length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Shank length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Step lift height | `grx.virtual_panel_command_param_1` |
| Step cycle | `grx.virtual_panel_command_param_2` |
| Assist ratio | `grx.virtual_panel_command_param_3` |
| Auto assist mode flag | `grx.virtual_panel_command_switch_1` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Update Log

- Added in `fourier-grx` v4.0.0.
