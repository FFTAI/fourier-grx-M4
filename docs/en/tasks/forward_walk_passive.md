---
layout: default
title: Passive Forward Walk
nav_order: 4.7
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Passive Forward Walk

## Task Info

Task ID (TID): **4111**

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for forward walking, and the actuators track that trajectory to achieve passive forward walking.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.
- If the task enters a torque protection state, the robot will pause motion and set the "task pause flag" to true. The task must be restarted to resume walking.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Step length | `float` | 0.5 | [0.2, 0.8] | The length of each step, in m. |
| Walking speed | `float` | 0.5 | [0.1, 1.2] | The target forward speed, in m/s. Single-step duration = step length ÷ walking speed (e.g., with step length 0.5 m and speed 0.5 m/s, each step takes approximately 1.0 s). |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue walking. |
| Pause motion flag | `bool` | false | (true, false) | Whether to pause motion. true = pause; the task must be restarted to resume walking. |
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. |
| Torque protection limit | `float` | None | [0.0, 200.0] | The maximum allowable output torque for any joint during walking, in Nm. If the real-time torque of any joint exceeds this limit, the task pauses and sets the "task pause flag". Takes effect only when torque protection is enabled; disabled by default. |

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
| Task pause flag | `task.flag_task_pause` |
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
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Pause motion flag | `grx.virtual_panel_command_pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Update Log

- Added in `fourier-grx` v4.0.0.
