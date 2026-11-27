---
layout: default
title: Passive Forward Walking – High-Lift (Knee Restriction)
parent: Task Description
nav_order: 4.291
has_toc: true
nav_exclude: true
---

# Passive Forward Walking – High-Lift (Knee Restriction)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Passive forward walking – high-lift (knee restriction) | **4307** | PD |

Applicable models: M4L (P1 / T1 / T2). Planner counterpart: **4507**, which generates and reports references without driving the joints. Assist variants are **4308 (PD) / 4309 (dt)**, with Planners **4508 / 4509**.

Task description:

- Reuses the trajectory generation and panel parameters of [Passive Forward Walking – High-Lift (4134 / 4135)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift), combined with the knee-restriction inputs and base-height calculation of [Passive Forward Walking (Knee Restriction, 4301)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive).
- The larger of the left/right knee restrictions becomes a shared minimum knee angle for both legs and remains enforced after high-lift IK, base smoothing and Gaussian smoothing.
- `param_6` has no effect on this task: base height is computed automatically from the knee restriction angle and leg lengths.
- Start, stop, pause, torque protection and Dynalink reporting follow [Passive Forward Walking](/fourier-grx-M4/docs/en/tasks/forward_walk_passive).
- This task does not promise forward base travel; actual lift can be limited by the knee restriction and joint reachability.

Task Parameters:

| Panel/user parameter | Meaning | Default | Notes |
|---|---|---|---|
| `param_1` | Step length | 0.5 m | Same as normal forward walk |
| `param_2` | Walking velocity | 0.5 m/s | Same as normal forward walk |
| `param_3` | Final actual ground-clearance target | 10 cm | Unit: cm, accepted range 5–25 cm; ≤0 or unsent keeps the current value. The generator solves the raw target so the smoothed actual peak lands within ±5 mm of the goal |
| `param_6` | Base height | — | No effect on this task; base height is computed from the knee restriction angle and leg lengths |
| `param_7` | Original DSP foot-lift height | 0.10 m | Applies before compensation and differs from the final ground-clearance target on `param_3` |
| `param_8` | Double-support ratio | 0.2 | DSP generation parameter |
| `param_9` | Torque-protection limit | Disabled | Requires `switch_1` to enable protection |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` | 0.0 rad | The larger of the left/right inputs becomes the common minimum flexion reference for both knees; 0.0 means no restriction |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` | 0.0 rad | The larger of the left/right inputs becomes the common minimum flexion reference for both knees; 0.0 means no restriction |

> Parameters apply after task entry and before start. Changes during walking do not affect the current trajectory and are used at the next start. A larger knee restriction leaves less knee-angle room for lift compensation, so the actual peak can remain below the target.

## Interface Info

The state and command interfaces match passive forward walking; knee restriction and leg lengths use the knee-restriction task's user parameters:

| Parameter | Interface Mapping |
|---|---|
| Target lift peak | `grx.virtual_panel_command_param_3` |
| Left / right knee restriction angle | `grx.virtual_user_knee_restriction_left` / `right` |
| Thigh / shank lengths | `grx.virtual_user_upper_leg_length_*` / `grx.virtual_user_lower_leg_length_*` |
| Start / stop / pause | `grx.virtual_panel_command_start` / `stop` / `pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Reference trajectories, progress and cadence | `rehab.reference_joint_*`, `rehab.motion_ratio`, `rehab.step_frequency` |

> `param_6` (base height) has no effect in this task; base height is computed from the knee restriction angle and leg lengths.

## Principle Explanation

### Algorithm Operation

Trajectory generation reuses the full high-lift compensation flow of [Passive Forward Walking – High-Lift](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift#principle-explanation): it evaluates actual foot clearance on the original DSP trajectory, then re-solves hip / knee angles during swing and applies zero-phase smoothing. The knee-restricted variant adds a knee-angle floor:

1. **Shared knee limit**: the left/right inputs are candidate restrictions; `θ=max(θ_left,θ_right)` becomes the shared minimum knee angle for both legs.
2. **Clamp after IK**: high-lift IK keeps the knee angle at or above `θ`; the binomial base smoothing and Gaussian smoothing then re-apply the floor so post-processing cannot break the limit.
3. **Base-height coupling**: as in knee-restricted forward walking, base height is computed from the knee restriction angle and leg lengths; panel `param_6` is ignored.
4. **Lift-only policy**: if the original DSP trajectory is already higher than the target at a large knee angle, the lift window does not lower it and reports that the target was not reached.

The knee limit applies to the algorithmic reference, not independent mechanical stops on the actual joints; tracking error still depends on the actuators and patient loading.

### Rehabilitation and Clinical Use

- Use when knee over-extension must be limited while more swing-foot clearance is needed. Adjust the knee restriction and lift target in separate steps rather than raising both at once.
- When clinical restrictions differ by side, the device uses the larger value as the shared floor for both legs; assess behavior using the larger restriction requirement.
- A larger knee restriction leaves less knee-angle room for lift compensation, so actual clearance can remain below `param_3`; observe actual foot clearance, trunk compensation and stance-side stability.
- For pain, spasm, stance-side instability or marked asymmetry, reduce the target or the restriction and reassess fitting.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- `fourier-grx` v4.4.89: adds knee-restricted executing task 4307, reusing the 4134 high-lift trajectory with a shared knee-angle floor; the floor is re-applied after high-lift IK, base smoothing and Gaussian smoothing. Planner 4507 generates and reports references without driving the joints.
