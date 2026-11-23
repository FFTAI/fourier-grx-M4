---
layout: default
title: Assist Forward Walk (Knee Restriction, Adjust PD Parameter)
parent: Task Description
nav_order: 4.22
has_toc: true
nav_exclude: true
---

# Assist Forward Walk (Knee Restriction, Adjust PD Parameter)

* TOC
{:toc}

## Task Info

Task ID (TID): **4303**

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for forward walking, and the actuators track that trajectory to achieve assisted forward walking.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Left restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Right restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Step length | `float` | 0.5 | [0.2, 0.8] | The length of each step, in m. |
| Walking speed | `float` | 0.5 | [0.1, 1.2] | The target forward speed, in m/s. Single-step duration = step length ÷ walking speed (e.g., with step length 0.5 m and speed 0.5 m/s, each step takes approximately 1.0 s). |
| Assist ratio | `float` | 0.5 | [0.0, 1.0] | Scaling factor for joint PD control stiffness, in the range [0.0, 1.0]. A lower value makes joints more compliant, leaving more room for the patient's own effort; a higher value increases joint stiffness and trajectory-tracking capability. |
| Step lift height | `float` | 0.1 | [0.05, 0.2] | The maximum lift height of the swing foot, in m. When ≤ 0 or not sent, the default value is used. Values outside the range are clipped. Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Double-support ratio | `float` | 0.2 | [0.1, 0.3] | The proportion of the double-support phase within a single step cycle. When ≤ 0 or not sent, the default value is used. Values outside the range are clipped. **This task uses the vhip gait generator, so this parameter has no effect** (only the DSP generator of TID 4129 / 4301 uses it). Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue walking. |

> Note: In this task, the base height is computed automatically from the knee restriction angle and leg lengths; the `grx.virtual_panel_command_param_6` (base height) interface has no effect on this task.

> **Knee Restriction Angle Explained**:
>
> The left/right inputs are candidate restrictions. Current code first computes `θ=max(θ_left,θ_right)`, then clamps both knee references to at least `θ`. This affects the algorithmic reference, not independent mechanical stops on the actual joints. When clinical restrictions differ by side, interpret device behavior using the larger restriction requirement.
>
> | Restriction Angle | Effect |
> |-------------------|--------|
> | 0.0 | No restriction; knee can fully extend (default) |
> | 0.3 | Knee maintains at least ~17° of bend throughout motion |
> | 0.5 | Knee maintains at least ~28.6° of bend throughout motion |
> | 1.0 | Knee maintains at least ~57.3° of bend throughout motion (strong restriction) |

> **Assist Ratio Explained**:
>
> The assist ratio adjusts joint stiffness by linearly interpolating the PD control gains of the actuators. The formula is:
>
> - **Kp** = (200 − 100) × assist ratio + 100, so Kp ∈ [100, 200]
> - **Kd** = (20 − 10) × assist ratio + 10, so Kd ∈ [10, 20]
>
> Joint output torque: τ = Kp × (θ\_target − θ\_measured) + Kd × (ω\_target − ω\_measured)
>
> | Assist Ratio | Kp  | Kd | Effect |
> |--------------|-----|----|--------|
> | 0.0 | 100 | 10 | Most compliant joints; weakest correction force for trajectory deviation — the patient can actively resist motion for active rehabilitation |
> | 0.5 | 150 | 15 | Moderate stiffness — suitable for patients with some voluntary movement ability |
> | 1.0 | 200 | 20 | Normal stiffness with full trajectory-tracking capability — suitable for patients requiring completely passive guidance |

> Recommendation:
> - A step length between 0.5× and 1.0× the walking speed tends to produce good walking results. For example, at a walking speed of 0.5 m/s, a step length of 0.25 m to 0.5 m is recommended.

> Note: from `fourier-grx` v4.4.54 the knee-restriction variant passes the assist ratio to the algorithm again, so `grx.virtual_panel_command_param_3` is adjustable once more, matching the parent task TID 4116 and TID 4306 (in v4.4.53 and earlier the parameter was not passed, the algorithm always received an assist ratio of 0, and joint stiffness was fixed at the most compliant level, Kp = 100, Kd = 10).
>
> Behavior change: when the virtual panel is enabled but this parameter was never sent, the panel default 0.0 still applies, as before; when a joystick is connected the assist ratio now follows the stick value, which the old firmware ignored — that omission is exactly what this fix addresses; when neither a joystick nor the virtual panel is connected the value is None and the algorithm treats it as "no adjustment" (equivalent to 1.0, Kp = 200, Kd = 20) instead of a fixed 0.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Step frequency (steps/min) | `rehab.step_frequency` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

> Note: Starting from v4.4.32, `reference_joint_position_max`/`reference_joint_position_min` only cover the joint angle range of the steady-state "cyclic walking/stepping" phase, and do not include transient extremes from the start and end transition phases.

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
| Assist ratio | `grx.virtual_panel_command_param_3` |
| Step lift height | `grx.virtual_panel_command_param_7` |
| Double-support ratio | `grx.virtual_panel_command_param_8` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Principle Explanation

### Algorithm Operation

Three distinct layers operate here: **common knee restriction and base geometry, VHIP trajectory generation, and startup PD interpolation**.

1. **Restriction preprocessing**: `θ=max(θ_left,θ_right)` feeds `α=atan2(L_s·sinθ,L_t+L_s·cosθ)`, `β=θ−α`, and `h=L_t·cosα+L_s·cosβ`. The same `θ` applies to both knees and `h` becomes generator base height, so current behavior is not independent left/right restriction.
2. **VHIP generation**: stance COM motion follows `ẍ=(g/h)x` while the swing foot advances and lifts through a half-cosine. After two-link IK, `q_knee=max(q_knee,θ)` is applied before smoothing and differentiation. No DSP double-support segmentation occurs, so `param_8` is ineffective.
3. **Startup stiffness**: `r` maps to `Kp=100+100r` and `Kd=10+10r`, and PD produces corrective torque from position/velocity errors. `θ` determines the reference lower bound; `r` determines how rigidly that reference is tracked.
4. **Fixed run parameters**: load detection and automatic PD ramping are disabled, and `r` is written only during startup. Changing restriction or assist values while running does not immediately rebuild the current trajectory or gains; restart the task as required.

With low `r`, actual positions can deviate further, so a reference satisfying `θ` does not guarantee that measured knee angle never falls below it. Safety still requires feedback and mechanical protection.

### Rehabilitation and Clinical Use

- Establish left/right restrictions from their respective clinical ranges before adjusting assist. Do not use higher stiffness to push a patient toward a restricted boundary or lower stiffness as a way to increase anatomical range.
- To encourage active participation, reduce the ratio gradually under external support and check that actual knee angles remain safe without pelvic or trunk compensation. Restart and reassess after each adjustment.
- Restricted posture changes base height and loading. Start with short steps, low speed, and low foot lift. Stop for pain, spasticity, marked resistance, or fatigue; neither reference deviation nor assist ratio directly measures strength or participation.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.2.6.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.48 added the step lift height / double-support ratio parameter interfaces (the base height is computed automatically from the knee restriction angle and leg lengths).
- `fourier-grx` v4.4.54 passes the assist ratio again, so `grx.virtual_panel_command_param_3` is adjustable once more, consistent with TID 4116 and TID 4306.
