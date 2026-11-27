---
layout: default
title: Passive Forward Walking – Harmonic Fitting (Knee Restriction)
parent: Task Description
nav_order: 4.292
has_toc: true
nav_exclude: true
---

# Passive Forward Walking – Harmonic Fitting (Knee Restriction)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Passive forward walking – harmonic fitting | **4131** | PD |
| Passive forward walking – harmonic fitting + velocity feedforward | **4113** | PD + velocity feedforward |
| Passive forward walking – harmonic fitting · POSITION + velocity feedforward | **4127** | POSITION + velocity feedforward |

Applicable models: M4L (P1 / T1 / T2). Planner: **4407**. Assist variants are **4310 (PD) / 4311 (dt)** with Planners **4510 / 4511**.

> This page is an entry point for **4131 within the knee-restriction task group; it does not introduce a new TID**. Here the restriction comes from the coefficient table selected by `param_2`, not from the additional virtual-user knee floor used by 4310 / 4311.

Task description:

- The trajectory is identical to [Passive Forward Walking – Harmonic Fitting (4131)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic). It selects from 16 curves spanning four hip-amplitude levels and four coefficient-table knee-restriction levels, with cadence controlled independently.
- Levels 1 / 2 / 3 / 4 of `param_2` correspond to knee extension floors of **0 / 5 / 10 / 15°**. The hip curve changes as well; this is not merely a knee-angle clip.
- Virtual-user `knee_restriction_left/right` is not read, and base height is not recomputed from leg lengths. To add a virtual-user knee floor beyond the coefficient-table restriction, use **4310 / 4311**.
- Step length, walking speed, leg lengths, base height, foot lift and double-support ratio do not generate the curve; `param_6` has no effect.
- The POSITION variant uses the actuator position loop with the same parameters. PD velocity feedforward is effective only through T2's FSA v3 protocol; P1/T1 FSA v2 fast frames have no velocity field.

Task Parameters:

| Panel parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Hip swing amplitude level | 2 | Levels 1–4, selecting the coefficient-table curve |
| `param_2` | Coefficient-table knee-restriction level | 1 | Levels 1–4, corresponding to 0 / 5 / 10 / 15° |
| `param_3` | Cadence level | 3 | Levels 1–6; target stride time 5.25–3.0 s, ≤0 keeps the current level |
| `param_6` | Base height | — | No effect on this task |
| Start / stop / pause | Motion control | false | Same as 4131; restarting is required to resume after pause |
| `switch_1` / `param_9` | Torque protection | Disabled | After 0.1 s of continuous excess torque on any joint, the task exits and the protection flag latches |

> Levels apply after task entry and before start. Changes while walking do not alter the current trajectory and take effect at the next start. Actual period is quantized to the model's control period; use `rehab.gait_stride_time_s` for the resulting value.

## Interface Info

| Parameter | Interface Mapping |
|---|---|
| Amplitude / table knee restriction / cadence | `grx.virtual_panel_command_param_1` / `param_2` / `param_3` |
| Start / stop / pause | `grx.virtual_panel_command_start` / `stop` / `pause` |
| Torque protection | `grx.virtual_panel_command_switch_1` / `grx.virtual_panel_command_param_9` |
| Reference trajectory, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |
| Table knee-restriction echo | `rehab.gait_knee_restriction_deg` (0 / 5 / 10 / 15°) |
| Actual stride time | `rehab.gait_stride_time_s` |

## Principle Explanation

Task 4131 reconstructs joint curves directly from stored Fourier coefficients; it performs no online COM, foot or two-link IK calculation. `param_2` selects a table that already contains a particular knee extension floor rather than applying an additional post-generation clip. Virtual-user leg lengths and left/right restrictions do not participate.

Tasks 4310 / 4311 select the table in the same way, then apply an additional `θ=max(θ_left,θ_right)` floor to both knees and recompute knee velocities by differentiation. These are distinct mechanisms.

### Rehabilitation and Clinical Use

Select the coefficient-table level from the patient's measured knee-extension range and preview the joint envelope with Planner 4407. The level constrains the reference only; it is not an independent mechanical stop on the patient's actual joint and does not replace external support, torque protection or therapist assessment.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.82: target stride times for the six cadence levels changed to 5.25 / 5.00 / 4.50 / 4.00 / 3.50 / 3.00 s; curves and table knee-restriction levels are unchanged.
- `fourier-grx` v4.4.90: added this entry point to the knee-restriction task group and documented assist variants 4310 / 4311. Task 4131's TID and runtime behavior are unchanged.
