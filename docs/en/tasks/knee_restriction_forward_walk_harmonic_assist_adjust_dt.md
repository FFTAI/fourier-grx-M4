---
layout: default
title: Assisted Forward Walking – Harmonic Fitting (Knee Restriction, dt Mode)
parent: Task Description
nav_order: 4.296
has_toc: true
nav_exclude: true
---

# Assisted Forward Walking – Harmonic Fitting (Knee Restriction, dt Mode)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted forward walking – harmonic fitting (knee restriction, dt mode) | **4311** | Assist (dt mode) |

Applicable models: M4L (P1 / T1 / T2). Planner counterpart: **4511**, which generates and reports references without driving the joints. The variant without virtual-user restriction is **4133**, with Planner **4409**.

Task description:

- Reuses the coefficient-table trajectory and dt assist of [Assisted Forward Walking – Harmonic Fitting (4133)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_dt), adding left/right virtual-user knee restrictions.
- `param_2` selects the table's built-in restriction. The virtual-user angle is an additional knee-angle floor; the stricter of the two restrictions applies.
- The assist ratio maps to 0.5–1.0× trajectory playback speed. `switch_1` enables automatic assist; PD remains at the medium tier.
- The harmonic curve is table-driven: step length, walking velocity, `param_6`, and the generic knee-task base-height calculation do not alter it.

Task Parameters:

| Panel/user parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Hip amplitude level | 2 | Levels 1–4 |
| `param_2` | Table knee-restriction level | 1 | Levels 1–4 corresponding to 0 / 5 / 10 / 15° |
| `param_3` | Cadence level | 3 | Levels 1–6; ≤0 keeps the current level |
| `param_4` | Assist ratio | 0 | Range [0.0, 1.0]; 0 = 0.5× speed, 1 = 1.0× speed |
| `switch_1` | Automatic assist | Disabled | Adjusts the assist ratio from measured hip torque |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` | 0.0 rad | The larger left/right value becomes an additional shared floor |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` | 0.0 rad | The larger left/right value becomes an additional shared floor |

> `param_1`–`param_3` and the virtual-user restriction apply before start; assist ratio and automatic assist update during walking. `rehab.gait_knee_restriction_deg` echoes only the table level from `param_2`, not the additional virtual-user floor.

## Interface Info

| Parameter | Interface Mapping |
|---|---|
| Amplitude / table restriction / cadence | `grx.virtual_panel_command_param_1` / `param_2` / `param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Automatic assist | `grx.virtual_panel_command_switch_1` |
| Left / right knee restriction angle | `grx.virtual_user_knee_restriction_left` / `right` |
| Start / stop | `grx.virtual_panel_command_start` / `stop` |
| Current assist ratio | `rehab.assist_ratio` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

## Principle Explanation

The trajectory is generated from the coefficient table selected by `param_1` and `param_2`. An additional floor `θ=max(θ_left,θ_right)` is then applied to both knee curves, and knee velocities are recomputed by differentiation. Hip curves and base height are not re-solved. See [Assisted Forward Walking – Harmonic Fitting (dt Mode)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_dt) for playback-speed and automatic assist.

### Rehabilitation and Clinical Use

The additional floor clips the table-driven knee curve and can change its shape. Preview with Planner 4511 before combining the table level, additional restriction and playback speed. Increased assist means faster playback, not a larger assistive torque.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.90: adds harmonic knee-restricted dt assist task 4311 and Planner 4511, combining table and virtual-user restrictions.
