---
layout: default
title: Passive Mark Time
nav_order: 4.10
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Passive Mark Time

## Task Info

Task ID (TID): **4112**

Task Description:

- The robot generates a joint motion trajectory sequence for mark time based on the given parameters, and drives the actuators to track that trajectory, achieving Passive Mark Time.
- When the "stop motion flag" is set to true, the robot will gradually slow down and stop rather than halting immediately.
- When the task enters the torque protection state, the robot will pause motion and set the "task pause flag" to true. The task must be restarted to continue stepping.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Thigh length | `float` | 0.5 | [0.3, 0.6] | The robot's thigh length, in m. |
| Shank length | `float` | 0.5 | [0.3, 0.6] | The robot's shank length, in m. |
| Step lift height | `float` | 0.1 | [0.1, 0.4] | The leg lift height for each step, in m. |
| Step cycle | `float` | 1.0 | [0.5, 4.0] | The single-step cycle for mark time — the time required to complete one full stepping cycle, in s. A smaller value means a higher step frequency; a larger value means slower stepping. |
| Start motion flag | `bool` | false | (true, false) | Whether to start the motion. true = start; false = do not start (has no effect if already started). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop the motion. true = stop; false = continue stepping. |
| Pause motion flag | `bool` | false | (true, false) | Whether to pause the motion. true = pause; the task must be restarted to continue stepping. |
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. |
| Torque protection limit | `float` | None | [0.0, 200.0] | The maximum allowable output torque for any joint during stepping, in Nm. If the real-time torque of any joint exceeds this limit, the task will pause and set the task pause flag. Only effective when torque protection is enabled; disabled by default. |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

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

Command Interface:

- Thigh length: only one value can be input in the algorithm; therefore the average of the left and right thigh lengths is used. Two values are passed, but only their average is used.
- Shank length: only one value can be input in the algorithm; therefore the average of the left and right shank lengths is used. Two values are passed, but only their average is used.

| Parameter | Interface Mapping |
|-----------|------------------|
| Thigh length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Shank length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Step lift height | `grx.virtual_panel_command_param_1` |
| Step cycle | `grx.virtual_panel_command_param_2` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Pause motion flag | `grx.virtual_panel_command_pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Update Log

- Added in `fourier-grx` v4.0.0.
