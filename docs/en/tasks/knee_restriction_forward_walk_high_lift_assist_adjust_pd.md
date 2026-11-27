---
layout: default
title: Assisted Forward Walking – High-Lift (Knee Restriction, PD Mode)
parent: Task Description
nav_order: 4.295
has_toc: true
nav_exclude: true
---

# Assisted Forward Walking – High-Lift (Knee Restriction, PD Mode)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted forward walking – high-lift (knee restriction, PD mode) | **4308** | Assist (PD mode) |

Applicable models: M4L (P1 / T1 / T2). Planner counterpart: **4508**, which generates and reports references without driving the joints. The variant without knee restriction is **4136**, with Planner **4411**.

Task description:

- Combines the high-lift trajectory and PD assist of [Assisted Forward Walking – High-Lift (4136)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist) with the user inputs and base-height calculation of [Forward Walking with Knee Restriction](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive).
- The larger left/right restriction becomes a shared minimum knee angle for both legs and remains enforced after high-lift IK and smoothing.
- The assist ratio interpolates PD gains between buttery and soft once during startup. Load detection and automatic PD ramping are disabled.
- `param_6` has no effect because base height is computed from the restriction and leg lengths. This task does not read `param_9` or provide a pause interface.

Task Parameters:

| Panel/user parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Step length | 0.5 m | Same as normal forward walk |
| `param_2` | Walking velocity | 0.5 m/s | Same as normal forward walk |
| `param_3` | Final actual ground-clearance target | 10 cm | Unit: cm, accepted range 5–25 cm; ≤0 or unsent keeps the current value |
| `param_4` | Assist ratio | 0 | Range [0.0, 1.0]; 0 = buttery, 1 = soft; latched during startup |
| `param_6` | Base height | — | No effect; computed from the restriction and leg lengths |
| `param_7` | Original DSP foot-lift height | 0.10 m | Applies before high-lift compensation |
| `param_8` | Double-support ratio | 0.2 | DSP generation parameter |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` | 0.0 rad | The larger left/right value is used; 0.0 means no restriction |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` | 0.0 rad | The larger left/right value is used; 0.0 means no restriction |

> Trajectory parameters apply before start; restart the task to update the assist ratio. A larger knee restriction can keep the actual lift below the target.

## Interface Info

| Parameter | Interface Mapping |
|---|---|
| Target lift peak | `grx.virtual_panel_command_param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Left / right knee restriction angle | `grx.virtual_user_knee_restriction_left` / `right` |
| Thigh / shank lengths | `grx.virtual_user_upper_leg_length_*` / `grx.virtual_user_lower_leg_length_*` |
| Start / stop | `grx.virtual_panel_command_start` / `stop` |
| Current assist ratio | `rehab.assist_ratio` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

## Principle Explanation

See [Passive Forward Walking – High-Lift (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_high_lift#principle-explanation) for trajectory generation and restriction handling, and [Assisted Forward Walking – High-Lift (PD Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist#principle-explanation) for PD interpolation. This task combines both paths. Planner 4508 uses the same model without writing PD or position targets to the robot.

### Rehabilitation and Clinical Use

Confirm the knee restriction, lift target and assist ratio independently before combining them. For pain, stance-side instability or marked asymmetry, reduce the targets or return to a more conservative task and reassess fitting.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.90: adds knee-restricted high-lift PD assist task 4308 and Planner 4508. The non-knee high-lift PD assist Planner is 4411.
