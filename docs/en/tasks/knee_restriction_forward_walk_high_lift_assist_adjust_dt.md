---
layout: default
title: Assisted Forward Walking – High-Lift (Knee Restriction, dt Mode)
parent: Task Description
nav_order: 4.296
has_toc: true
nav_exclude: true
---

# Assisted Forward Walking – High-Lift (Knee Restriction, dt Mode)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted forward walking – high-lift (knee restriction, dt mode) | **4309** | Assist (dt mode) |

Applicable models: M4L (P1 / T1 / T2). Planner counterpart: **4509**, which generates and reports references without driving the joints. The variant without knee restriction is **4137**, with Planner **4412**.

Task description:

- Combines the high-lift trajectory and playback-speed assist of [Assisted Forward Walking – High-Lift (4137)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist_adjust_dt) with the user inputs and base-height calculation of [Forward Walking with Knee Restriction](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive).
- The larger left/right restriction becomes a shared minimum knee angle for both legs and remains enforced after high-lift IK and smoothing.
- The assist ratio maps to 0.5–1.0× trajectory playback speed. `switch_1` enables automatic assist; PD remains at the medium tier.
- `param_6` has no effect because base height is computed from the restriction and leg lengths. This task does not read `param_9` or provide a pause interface.

Task Parameters:

| Panel/user parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Step length | 0.5 m | Same as normal forward walk |
| `param_2` | Walking velocity | 0.5 m/s | Same as normal forward walk |
| `param_3` | Final actual ground-clearance target | 10 cm | Unit: cm, accepted range 5–25 cm; ≤0 or unsent keeps the current value |
| `param_4` | Assist ratio | 0 | Range [0.0, 1.0]; 0 = 0.5× speed, 1 = 1.0× speed |
| `param_6` | Base height | — | No effect; computed from the restriction and leg lengths |
| `param_7` | Original DSP foot-lift height | 0.10 m | Applies before high-lift compensation |
| `param_8` | Double-support ratio | 0.2 | DSP generation parameter |
| `switch_1` | Automatic assist | Disabled | Adjusts the assist ratio from measured hip torque |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` | 0.0 rad | The larger left/right value is used; 0.0 means no restriction |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` | 0.0 rad | The larger left/right value is used; 0.0 means no restriction |

> Trajectory parameters apply before start; assist ratio and automatic assist update during walking. A larger knee restriction can keep the actual lift below the target.

## Interface Info

| Parameter | Interface Mapping |
|---|---|
| Target lift peak | `grx.virtual_panel_command_param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Automatic assist | `grx.virtual_panel_command_switch_1` |
| Left / right knee restriction angle | `grx.virtual_user_knee_restriction_left` / `right` |
| Thigh / shank lengths | `grx.virtual_user_upper_leg_length_*` / `grx.virtual_user_lower_leg_length_*` |
| Start / stop | `grx.virtual_panel_command_start` / `stop` |
| Current assist ratio | `rehab.assist_ratio` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

## Principle Explanation

See [Passive Forward Walking – High-Lift (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_high_lift#principle-explanation) for trajectory generation and restriction handling, and [Assisted Forward Walking – High-Lift (dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist_adjust_dt#principle-explanation) for playback-speed and automatic assist. This task combines both paths. Planner 4509 uses the same model without writing control targets to the robot.

### Rehabilitation and Clinical Use

Confirm the knee restriction, lift target and playback speed independently before combining them. Increased assist means faster playback, not a larger assistive torque; automatic assist does not replace balance or fall protection.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.90: adds knee-restricted high-lift dt assist task 4309 and Planner 4509. The non-knee high-lift dt assist Planner is 4412.
