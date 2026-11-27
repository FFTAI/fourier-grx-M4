---
layout: default
title: Assisted Marching in Place (PD Mode)
parent: Task Description
nav_order: 4.21
has_toc: true
nav_exclude: true
---

# Assisted Marching in Place (PD Mode)

* TOC
{:toc}

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted Marching in Place (PD Mode) | **4117** | Assist (PD Mode) |

Task Description:

- The robot generates a joint motion trajectory sequence for mark time based on the given parameters, and drives the actuators to track that trajectory, achieving Assisted Marching in Place.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Thigh length | `float` | 0.5 | [0.3, 0.6] | The robot's thigh length, in m. |
| Shank length | `float` | 0.5 | [0.3, 0.6] | The robot's shank length, in m. |
| Step lift height | `float` | 0.1 | [0.1, 0.4] | The leg lift height for each step, in m. |
| Step cycle | `float` | 1.0 | [0.5, 4.0] | The single-step cycle for mark time — the time required to complete one full stepping cycle, in s. A smaller value means a higher step frequency; a larger value means slower stepping. |
| Assist ratio | `float` | 0.5 | [0.0, 1.0] | The adjustment coefficient for joint PD control stiffness, in the range [0.0, 1.0]. A smaller value makes the joints more compliant, giving the patient more room for active effort; a larger value increases joint stiffness and trajectory-tracking capability. |
| Base height (pelvis height) | `float` | None | [0.6, 1.2] | The height of the base (pelvis) above the ground while stepping, in m. When ≤ 0 or not sent, it is automatically set to the sum of the thigh and shank lengths. Values outside the range are clipped. Takes effect at the next start of stepping (trajectory regeneration); changes made while stepping do not affect the trajectory currently being executed. |
| Start motion flag | `bool` | false | (true, false) | Whether to start the motion. true = start; false = do not start (has no effect if already started). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop the motion. true = stop; false = continue stepping. |

> Note: In this task, the step lift height is still set via the existing `grx.virtual_panel_command_param_1` interface (see the "Step lift height" row above); the new panel interfaces `param_7`/`param_8` have no effect on this task.

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

> When it takes effect: the assist ratio is written into the joint PD gains only while the task is in its start stage (`STAGE_INIT` / `STAGE_START`). Changing it during walking or stepping does not change the current stiffness — the task must be restarted.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Current assist ratio | `rehab.assist_ratio` |
| Step frequency (steps/min) | `rehab.step_frequency` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

> Note: Since v4.4.32, `reference_joint_position_max`/`reference_joint_position_min` only report the joint angle range during the steady-state phase of "cyclic walking/marking time", excluding transient extrema during the start-up and finishing transition phases.

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
| Base height (pelvis height) | `grx.virtual_panel_command_param_6` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Principle Explanation

### Algorithm Operation

This task chains in-place geometric generation with adjustable PD stiffness:

1. **Reference action**: foot-lift height `h` determines the half-cosine vertical trajectory and fore/aft amplitude `L_max=min(2h,L_thigh)`; step period sets left/right alternation. Two-link IK converts the foot path to joint angles. Assist ratio plays no part here, so it changes neither lift height nor curve shape.
2. **Feedback gains**: startup maps `r∈[0,1]` to `Kp=100+100r` and `Kd=10+10r`, interpolating from buttery to soft. Feedback is approximately `τ=Kp(q_ref−q_meas)+Kd(ω_ref−ω_meas)`, so low `r` reduces corrective torque for the same deviation and high `r` constrains tracking more strongly.
3. **Cyclic execution**: position references retain outer first-order smoothing and travel limits before PD. Load detection and automatic gain ramping are disabled so measured energy cannot replace the chosen assist level with hard-tier gains.
4. **Latch timing**: Kp/Kd update only in `STAGE_INIT/STAGE_START`; changing `r` during motion requires a restart. `r=0` still retains minimum-tier PD rather than disabling the actuators or guaranteeing zero torque.

Active participation therefore comes from more compliant error feedback, not real-time assistive-torque modulation based on measured patient effort.

### Rehabilitation and Clinical Use

- For patients with some active stepping ability, reduce stiffness gradually under protection to encourage participation; increase it when clearer passive guidance is needed. Restart after every change and reassess quality and tolerance.
- Establish a stable action with low foot lift and a slow period before changing assist. Low stiffness does not reduce movement amplitude, and high stiffness does not inherently improve treatment effect.
- Tracking deviation and joint torque alone do not measure patient strength or effort. Interpret them with clinical observation, pain, and fatigue. External support and fall protection remain necessary for in-place stepping.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.0.0.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.48 added the base height parameter interface.
