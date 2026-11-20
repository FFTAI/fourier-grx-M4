---
layout: default
title: High-Lift DSP Forward Walk
nav_order: 4.29
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# High-Lift DSP Forward Walk

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| High-lift DSP forward walk | **4134** | PD |
| High-lift DSP forward walk + velocity feedforward | **4135** | PD + velocity feedforward |

Applicable models: M4L (P1 / T1 / T2).

Task description:

- Adds swing-foot lift compensation to normal DSP forward walking. The generator evaluates the actual foot position produced by the original DSP trajectory, re-solves hip / knee angles for a target ground clearance during swing, and applies zero-phase smoothing.
- The compensation addresses lift lost through hip-angle scaling and smoothing. It does not alter the support-leg trajectory or promise forward base travel.
- 4135 reuses the trajectory and panel parameters of 4134 and adds velocity feedforward. T2 sends it directly through FSA v3. FSA v2 fast frames on P1/T1 have no velocity field; the related reference compensation affects visualization only and does not modify actual joint targets.
- Start, stop, pause, torque protection and Dynalink reporting are inherited from [Passive Forward Walk](/fourier-grx-M4/docs/en/tasks/forward_walk_passive).

## Task Parameters

| Panel parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Step length | 0.5 m | Same as normal forward walk |
| `param_2` | Walking velocity | 0.5 m/s | Same as normal forward walk |
| `param_3` | Compensated target lift peak | 10 cm | Unit: cm, accepted range 5–25 cm; ≤0 or unsent keeps the current value |
| `param_6` | Base height | Automatic | Same as normal forward walk |
| `param_7` | Original DSP foot-lift height | 0.10 m | Applies before compensation and differs from the final ground-clearance target on `param_3` |
| `param_8` | Double-support ratio | 0.2 | DSP generation parameter |
| `param_9` | Torque-protection limit | Disabled | Requires `switch_1` to enable protection |

`lift_peak_phase` and `lift_smooth_time` are algorithm-development parameters controlling the peak phase within swing and final hip / knee smoothing time; they are not exposed through the panel.

> Parameters apply after task entry and before start. Changes during walking do not affect the current trajectory and are used at the next start. Near full leg extension or at joint travel limits, actual lift can remain below the target.

## Interface Info

4134 / 4135 use the same state and command interfaces as passive forward walking, with the additional lift target:

| Parameter | Interface Mapping |
|---|---|
| Target lift peak | `grx.virtual_panel_command_param_3` |
| Start / stop / pause | `grx.virtual_panel_command_start` / `stop` / `pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

## Update Log

- `fourier-grx` v4.4.85: added 4134 / 4135. The default lift target is 10 cm and can be raised to 15 cm; Harmonic / DSP / DSP+lift comparison tooling is included for offline trajectory inspection.
