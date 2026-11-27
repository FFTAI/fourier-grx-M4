---
layout: default
title: Assisted Forward Walking – High-Lift (dt Mode)
parent: Task Description
nav_order: 4.20
has_toc: true
nav_exclude: true
---

# Assisted Forward Walking – High-Lift (dt Mode)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted forward walking – high-lift (dt Mode) | **4137** | dt-mode assist |

Applicable models: M4L (P1 / T1 / T2).

Task description:

- Uses exactly the same trajectory as [Passive Forward Walking – High-Lift (4134 / 4135)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift): swing-foot lift compensation on top of normal DSP forward walking. This page covers only the dt assist layer; trajectory generation, parameter meanings and algorithm details are on that page.
- The assist ratio maps to a 0.5–1.0× trajectory playback speed, closer to normal cadence at higher values, with automatic assist enabled by `switch_1`, matching [Assisted Forward Walking (dt Mode, 4118)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt).
- Start, stop, joystick and Dynalink reporting follow 4118. This task does not read `param_9` (torque protection) and does not provide a pause interface.
- For the PD variant, see [Assisted Forward Walking – High-Lift (PD Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist).

## Task Parameters

Panel parameters reuse the passive version's step length / velocity / lift target / base height / raw lift / double-support ratio, with the assist ratio moved to `param_4`:

| Panel parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Step length | 0.5 m | Same as normal forward walk |
| `param_2` | Walking velocity | 0.5 m/s | Same as normal forward walk |
| `param_3` | Final actual ground-clearance target | 10 cm | Unit: cm, accepted range 5–25 cm; ≤0 or unsent keeps the current value. The generator solves the raw target so the smoothed actual peak lands within ±5 mm of the goal |
| `param_4` | Assist ratio | 0 | Range [0.0, 1.0]; unsent is treated as 0. 0 = 0.5× slowest playback, 1 = 1.0× |
| `param_6` | Base height | Automatic | Same as normal forward walk |
| `param_7` | Original DSP foot-lift height | 0.10 m | Applies before compensation and differs from the final ground-clearance target on `param_3` |
| `param_8` | Double-support ratio | 0.2 | DSP generation parameter |
| `switch_1` | Automatic assist | Disabled | Adjusts the assist ratio from measured hip torque; `param_4` no longer applies when enabled (same as 4118) |

`lift_peak_phase` and `lift_smooth_time` are algorithm-development parameters controlling the peak phase within swing and final hip / knee smoothing time; they are not exposed through the panel.

> For 4137 the assist ratio and automatic assist take effect during walking, refreshing playback speed every control cycle (same as 4118).

> Trajectory-generation parameters (`param_1` / `param_2` / `param_3` / `param_6` / `param_7` / `param_8`) apply after task entry and before start. Changes during walking do not affect the current trajectory and are used at the next start. Near full leg extension or at joint travel limits, actual lift can remain below the target.

## Interface Info

The state and command interfaces match 4118, with the assist ratio moved to `param_4` because `param_3` carries the lift target:

| Parameter | Interface Mapping |
|---|---|
| Target lift peak | `grx.virtual_panel_command_param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Automatic assist | `grx.virtual_panel_command_switch_1` |
| Start / stop | `grx.virtual_panel_command_start` / `stop` |
| Current assist ratio | `rehab.assist_ratio` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

> ⚠️ Unlike 4118, the **assist ratio is on `param_4`** here because `param_3` carries the target lift peak; `param_1` / `param_2` remain step length / walking velocity. Map host commands to this table rather than reusing the 4118 positions.

## Principle Explanation

### Algorithm Operation

The high-lift trajectory shares the same generator as the passive version: it re-solves hip / knee angles for a target ground clearance during swing, applies zero-phase smoothing, then enters the normal DSP start/loop/end and PD pipeline. See [Passive Forward Walking – High-Lift · Principle Explanation](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift#principle-explanation). The assist variant changes only the execution layer:

**4137 (dt Mode)**: playback speed is `v_play=0.5+0.5r`, and trajectory time advances by `Δt_motion=Δt_control·v_play`, so a higher ratio shortens the gait period. Automatic assist adjusts the ratio from measured hip torque (same decision logic as 4118), while PD stays at the fixed medium tier.

### Rehabilitation and Clinical Use

- When more swing-foot clearance is needed while keeping active participation, set the target lift peak using the passive page first, then adjust the assist ratio; avoid large changes to both at once.
- “More assist” here means faster playback, not a larger assist torque. Automatic assist does not replace balance and fall protection.
- After tuning, check the actual gait period to confirm the effect. For pain, stance-side instability, or marked asymmetry, reduce the target or return to normal DSP walking and reassess.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.87: added 4137, a high-lift assist task in dt mode using the same trajectory as 4134. `param_3` sets the target lift height and `param_4` the assist ratio (unsent is treated as 0); the ratio maps to playback speed and `switch_1` enables automatic assist.
- `fourier-grx` v4.4.88: switches to actual-height solving with a 10 cm target. Smoothing is normalized by step time and acceleration becomes a diagnostic; these changes apply to the passive version as well.
