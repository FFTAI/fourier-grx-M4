---
layout: default
title: Assisted Forward Walking – Harmonic Fitting (Knee Restriction, PD Mode)
parent: Task Description
nav_order: 4.293
has_toc: true
nav_exclude: true
---

# Assisted Forward Walking – Harmonic Fitting (Knee Restriction, PD Mode)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted forward walking – harmonic fitting (knee restriction, PD mode) | **4310** | Assist (PD mode) |

Applicable models: M4L (P1 / T1 / T2). Planner counterpart: **4510**, which generates and reports references without driving the joints. The variant without virtual-user restriction is **4132**, with Planner **4408**.

Task description:

- Reuses the coefficient-table trajectory and PD assist of [Assisted Forward Walking – Harmonic Fitting (4132)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd), adding left/right virtual-user knee restrictions.
- `param_2` selects the table's built-in restriction. The virtual-user angle is an additional knee-angle floor; the stricter of the two restrictions applies.
- The assist ratio interpolates PD gains between buttery and soft once during startup. Load detection and automatic PD ramping are disabled.
- The harmonic curve is table-driven: step length, walking velocity, `param_6`, and the generic knee-task base-height calculation do not alter it.

Task Parameters:

| Panel/user parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Hip amplitude level | 2 | Levels 1–4 |
| `param_2` | Table knee-restriction level | 1 | Levels 1–4 corresponding to 0 / 5 / 10 / 15° |
| `param_3` | Cadence level | 3 | Levels 1–6; ≤0 keeps the current level |
| `param_4` | Assist ratio | 0 | Range [0.0, 1.0]; 0 = buttery, 1 = soft; latched during startup |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` | 0.0 rad | The larger left/right value becomes an additional shared floor |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` | 0.0 rad | The larger left/right value becomes an additional shared floor |

> `param_1`–`param_3` and the virtual-user restriction apply before start; restart to update `param_4`. `rehab.gait_knee_restriction_deg` echoes only the table level from `param_2`, not the additional virtual-user floor.

## Interface Info

| Parameter | Interface Mapping |
|---|---|
| Amplitude / table restriction / cadence | `grx.virtual_panel_command_param_1` / `param_2` / `param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Left / right knee restriction angle | `grx.virtual_user_knee_restriction_left` / `right` |
| Start / stop | `grx.virtual_panel_command_start` / `stop` |
| Current assist ratio | `rehab.assist_ratio` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

## Principle Explanation

The trajectory is generated from the coefficient table selected by `param_1` and `param_2`. An additional floor `θ=max(θ_left,θ_right)` is then applied to both knee curves, and knee velocities are recomputed by differentiation. Hip curves and base height are not re-solved. See [Assisted Forward Walking – Harmonic Fitting (PD Mode)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd) for PD assist.

### Rehabilitation and Clinical Use

The additional floor clips the table-driven knee curve and can change its shape. Preview with Planner 4510 before combining the table level, additional restriction and PD stiffness. Reduce the restriction or assist target if pain or stance-side instability occurs.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.90: adds harmonic knee-restricted PD assist task 4310 and Planner 4510, combining table and virtual-user restrictions.
