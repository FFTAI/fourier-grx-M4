---
layout: default
title: Assist Mark Time (Adjust PD Parameter)
nav_order: 4.11
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Assist Mark Time (Adjust PD Parameter)

## Task Info

Task ID (TID): **4117**

Task Description:

- The robot generates a joint motion trajectory sequence for mark time based on the given parameters, and drives the actuators to track that trajectory, achieving Assist Mark Time.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Thigh length | `float` | 0.5 | [0.3, 0.6] | The robot's thigh length, in m. |
| Shank length | `float` | 0.5 | [0.3, 0.6] | The robot's shank length, in m. |
| Step lift height | `float` | 0.1 | [0.1, 0.4] | The leg lift height for each step, in m. |
| Step cycle | `float` | 1.0 | [0.5, 4.0] | The single-step cycle for mark time — the time required to complete one full stepping cycle, in s. A smaller value means a higher step frequency; a larger value means slower stepping. |
| Assist ratio | `float` | 0.5 | [0.0, 1.0] | The adjustment coefficient for joint PD control stiffness, in the range [0.0, 1.0]. A smaller value makes the joints more compliant, giving the patient more room for active effort; a larger value increases joint stiffness and trajectory-tracking capability. |
| Start motion flag | `bool` | false | (true, false) | Whether to start the motion. true = start; false = do not start (has no effect if already started). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop the motion. true = stop; false = continue stepping. |

> **Assist Ratio Explanation**:
>
> The assist ratio adjusts joint stiffness by linearly interpolating the actuator PD control gains. The formula is:
>
> - **Kp** = (200 − 100) × assist\_ratio + 100, so Kp ∈ [100, 200]
> - **Kd** = (20 − 10) × assist\_ratio + 10, so Kd ∈ [10, 20]
>
> Joint output torque: τ = Kp × (θ\_target − θ\_measured) + Kd × (ω\_target − ω\_measured)
>
> | Assist Ratio | Kp | Kd | Effect |
> |-------------|----|----|--------|
> | 0.0 | 100 | 10 | Most compliant joints; weakest correction force on trajectory deviation — patients can actively resist motion for active rehabilitation. |
> | 0.5 | 150 | 15 | Moderate stiffness — suitable for patients with some active motor ability. |
> | 1.0 | 200 | 20 | Normal stiffness with full trajectory-tracking capability — suitable for patients requiring completely passive guidance. |

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
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Update Log

- Added in `fourier-grx` v4.0.0.
