---
layout: default
title: High-Lift DSP Passive Forward Walk
parent: Task Description
nav_order: 4.13
has_toc: true
nav_exclude: true
---

# High-Lift DSP Passive Forward Walk

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| High-lift DSP passive forward walk | **4134** | PD |
| High-lift DSP passive forward walk + velocity feedforward | **4135** | PD + velocity feedforward |

Applicable models: M4L (P1 / T1 / T2).

Task description:

- Adds swing-foot lift compensation to normal DSP forward walking. The generator evaluates the actual foot position produced by the original DSP trajectory, re-solves hip / knee angles for a target ground clearance during swing, and applies zero-phase smoothing.
- The compensation addresses lift lost through hip-angle scaling and smoothing. It does not alter the support-leg trajectory or promise forward base travel.
- 4135 reuses the trajectory and panel parameters of 4134 and adds velocity feedforward. T2 sends it directly through FSA v3. FSA v2 fast frames on P1/T1 have no velocity field; the related reference compensation affects visualization only and does not modify actual joint targets.
- The assist variants 4136 / 4137 reuse this trajectory and the DSP parameters, adding the assist ratio on `param_4`; they change only the execution layer (PD gains or playback speed). See [High-Lift DSP Assisted Forward Walk (PD / dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist).
- Start, stop, pause, torque protection and Dynalink reporting are inherited from [Passive Forward Walking](/fourier-grx-M4/docs/en/tasks/forward_walk_passive).

## Task Parameters

| Panel parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Step length | 0.5 m | Same as normal forward walk |
| `param_2` | Walking velocity | 0.5 m/s | Same as normal forward walk |
| `param_3` | Final actual ground-clearance target | 10 cm | Unit: cm, accepted range 5–25 cm; ≤0 or unsent keeps the current value. The generator solves the raw target so the smoothed actual peak lands within ±5 mm of the goal |
| `param_6` | Base height | Automatic | Same as normal forward walk |
| `param_7` | Original DSP foot-lift height | 0.10 m | Applies before compensation and differs from the final ground-clearance target on `param_3` |
| `param_8` | Double-support ratio | 0.2 | DSP generation parameter |
| `param_9` | Torque-protection limit | Disabled | Requires `switch_1` to enable protection |

`lift_peak_phase` and `lift_smooth_time` are algorithm-development parameters controlling the peak phase within swing and final hip / knee smoothing time; they are not exposed through the panel.

> Parameters apply after task entry and before start. Changes during walking do not affect the current trajectory and are used at the next start. Near full leg extension or at joint travel limits, actual lift can remain below the target.

## Interface Info

4134 / 4135 use the same state and command interfaces as passive forward walking:

| Parameter | Interface Mapping |
|---|---|
| Target lift peak | `grx.virtual_panel_command_param_3` |
| Start / stop / pause | `grx.virtual_panel_command_start` / `stop` / `pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

## Principle Explanation

### Algorithm Operation

High-lift walking adds **foot-height recompensation based on the actual joint trajectory** after a complete DSP generation pass; it does not simply amplify `param_7`:

1. **Original DSP result**: normal DSP has already performed COM/foot planning, two-link inverse kinematics, hip-extension scaling, and low-pass filtering. Those later operations change actual foot position, so the original `step_height` need not equal the final trajectory's real clearance peak.
2. **Forward-kinematics evaluation**: current joint angles give ankle position relative to the hip, for example `x_ankle=−L_t·sin(q_h)−L_s·sin(q_h+q_k)` and `z_ankle=−L_t·cos(q_h)−L_s·cos(q_h+q_k)`. The lower of the two feet defines the ground reference for actual swing clearance.
3. **Lift-only target window**: a Beta lift window is constructed within each swing interval with default `lift_shape=4.0` and peak phase `p=0.42`, separating the foot-lift peak from joint-velocity zero crossings. `clearance=smooth_max(base_clearance,H_lift·w(s))` never lowers an already-higher original trajectory; a 2 mm `smooth_max` transition reduces slope switching. `lift_shape=0` restores the original smootherstep.
4. **IK with horizontal position preserved**: swing-foot `x` remains fixed while `z` rises to the target, and two-link IK re-solves hip/knee angles before clipping to hip `−90°…40°` and knee `0°…110°`. Near full extension, `d→L_t+L_s`, knee angle is highly sensitive to foot height, and the achievable peak can fall below `H_lift`.
5. **Zero-phase smoothing and output**: a binomial kernel with default `0.10 × T_step` first removes per-frame IK corners, followed by Gaussian smoothing with default `sigma = 0.08 × T_step`. In actual mode, bisection finds the raw target needed to bring the final actual peak within ±5 mm of the goal. Acceleration is diagnostic by default, with an optional hard `lift_acc_limit`. Positions are differentiated again for velocity and actual foot-height diagnostics before entering the normal DSP start/loop/end and PD pipeline.

TID 4135 leaves this compensation unchanged and only adds velocity feedforward during execution; actuator effectiveness depends on the FSA protocol version.

### Rehabilitation and Clinical Use

- After the patient tolerates normal forward walking, this task can provide guidance when more swing-foot clearance is needed. Higher lift should not be equated directly with improved independent walking or fall prevention.
- Start at the default or a lower target and increase in small steps, evaluating each change separately rather than raising foot lift, step length, and speed together. Observe actual clearance, trunk compensation, pelvic posture, and stance-side stability instead of relying on `param_3` alone.
- The target is not a measurement of actual foot lift. For pain, restricted hip/knee motion, stance-side instability, or marked asymmetry, reduce the target or return to normal DSP walking and reassess fitting.
- Feedforward behavior depends on the model protocol, so clinical comparisons across models must not assume identical control action.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.85: added 4134 / 4135. The default lift target is 10 cm and can be raised to 15 cm; Harmonic / DSP / DSP+lift comparison tooling is included for offline trajectory inspection.
- `fourier-grx` v4.4.87: added Beta lift windows and angular-acceleration limits. The default peak phase is 0.42 and the target height is 15 cm; actual lift is about 10 cm in the current default scenario. The same version added assist variants 4136 / 4137, documented in [High-Lift DSP Assisted Forward Walk (PD / dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist).
- `fourier-grx` v4.4.88: switches to actual-height solving with a 10 cm target. Smoothing is normalized by step time (sigma 0.08×T_step, base smoothing 0.10×T_step); acceleration becomes a diagnostic, while peak mode preserves the original semantics.
