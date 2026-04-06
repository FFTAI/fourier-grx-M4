---
layout: default
title: Assist Forward Walk (Adjust dt Parameter)
nav_order: 4.9
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Assist Forward Walk (Adjust dt Parameter)

## Task Info

Task ID (TID): **4118**

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for forward walking, and the actuators track that trajectory to achieve assisted forward walking.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.
- Assist intensity is controlled by the assist ratio: a higher value speeds up trajectory playback (closer to a normal walking pace); a lower value slows playback down, giving the patient more time to follow the motion.
- An automatic assist mode is available. When the "auto assist mode flag" is enabled, the robot automatically adjusts the assist ratio based on measured joint torques, with no manual setting required.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Step length | `float` | 0.5 | [0.2, 0.8] | The length of each step, in m. |
| Walking speed | `float` | 0.5 | [0.1, 1.2] | The target forward speed, in m/s. Single-step duration = step length ÷ walking speed (e.g., with step length 0.5 m and speed 0.5 m/s, each step takes approximately 1.0 s). |
| Assist ratio | `float` | 0.5 | [0.0, 1.0] | Scaling factor for trajectory playback speed, in the range [0.0, 1.0]. A higher value plays the trajectory faster (closer to normal walking pace); a lower value plays it slower, giving the patient more time to follow the motion. |
| Auto assist mode flag | `bool` | false | (true, false) | Whether to enable automatic assist mode. When enabled, the system automatically adjusts the assist ratio by ±0.01 each control cycle (20 ms) based on the deviation between measured joint torques and the reference trajectory, with no manual setting required; the assist ratio is always clamped to [0.0, 1.0]. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue walking. |


> **Assist Ratio Explained**:
>
> The assist ratio controls pacing by adjusting the trajectory playback speed (play\_speed). The formula is:
>
> - **play\_speed** = 0.5 + assist ratio × 0.5, so play\_speed ∈ [0.5, 1.0]
> - Trajectory time advance per control cycle: Δt = 0.02 s × play\_speed
>
> | Assist Ratio | play\_speed | Effect |
> |--------------|-------------|--------|
> | 0.0 | 0.5 | Trajectory plays at 50% speed; each step takes twice the normal time — suitable for patients with weaker motor ability |
> | 0.5 | 0.75 | Trajectory plays at 75% speed; moderate step frequency |
> | 1.0 | 1.0 | Trajectory plays at normal speed — suitable for patients with near-normal motor ability |

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
| Step length | `grx.virtual_panel_command_param_1` |
| Walking speed | `grx.virtual_panel_command_param_2` |
| Assist ratio | `grx.virtual_panel_command_param_3` |
| Auto assist mode flag | `grx.virtual_panel_command_switch_1` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Update Log

- Added in `fourier-grx` v4.0.0.
