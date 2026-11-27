---
layout: default
title: Passive Marching in Place (Knee Restriction)
parent: Task Description
nav_order: 4.238
has_toc: true
nav_exclude: true
---

# Passive Marching in Place (Knee Restriction)

* TOC
{:toc}

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Passive Marching in Place (Knee Restriction) | **4302** | PD |

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for marching in place, and the actuators track that trajectory to achieve passive mark time.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Left restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Right restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Step height | `float` | 0.1 | [0.1, 0.4] | The leg-lift height for each step, in m. |
| Step period | `float` | 1.0 | [0.5, 4.0] | The cycle duration for one complete stepping cycle, in s. A smaller value means a higher step frequency; a larger value means a slower step. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue stepping. |
| Pause motion flag | `bool` | false | (true, false) | Whether to pause motion. true = pause; the task must be restarted to continue stepping. |

> Note: `command_switch_1` / `command_param_9` take effect for this task from `fourier-grx` v4.4.54; once enabled, if the real-time torque of any joint exceeds the limit continuously for at least 0.1 s (since v4.4.75), the robot immediately exits this task and switches to the idle task (`TASK_IDLE`), and the torque-protection flag is set (v4.4.53 and earlier did not run this check). The base height is computed from the knee restriction angle and leg lengths, so `param_6` has no effect.
>
> **Knee Restriction Angle Explained**:
>
> Unsent virtual-user inputs default to 0.0 on both sides; when no virtual-user source is connected, missing values fall back to 0.2 rad (about 10°). The left/right inputs are candidate restrictions. Current code first computes `θ=max(θ_left,θ_right)`, then clamps both knee references to at least `θ`. This affects the algorithmic reference, not independent mechanical stops on the actual joints. When clinical restrictions differ by side, interpret device behavior using the larger restriction requirement.
>
> | Restriction Angle | Effect |
> |-------------------|--------|
> | 0.0 | No restriction; knee can fully extend (default) |
> | 0.3 | Knee maintains at least ~17° of bend throughout motion |
> | 0.5 | Knee maintains at least ~28.6° of bend throughout motion |
> | 1.0 | Knee maintains at least ~57.3° of bend throughout motion (strong restriction) |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Step frequency (steps/min) | `rehab.step_frequency` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

> Note: Starting from v4.4.32, `reference_joint_position_max`/`reference_joint_position_min` only cover the joint angle range of the steady-state "cyclic walking/stepping" phase, and do not include transient extremes from the start and end transition phases.

Command interface:

- The upper leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.
- The lower leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.

| Parameter | Interface Mapping |
|-----------|------------------|
| Upper leg length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Lower leg length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` |
| Step height | `grx.virtual_panel_command_param_1` |
| Step period | `grx.virtual_panel_command_param_2` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Pause motion flag | `grx.virtual_panel_command_pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Principle Explanation

### Algorithm Operation

Knee-restricted in-place stepping follows **common restriction → base height → periodic foot trajectory → IK and clipping → PD playback**:

1. **Common `θ` and `h`**: current code uses `θ=max(θ_left,θ_right)` for both knees. `α=atan2(L_s·sinθ,L_t+L_s·cosθ)`, `β=θ−α`, and `h=L_t·cosα+L_s·cosβ` determine base height; left/right inputs do not form independent bounds.
2. **In-place foot motion**: the COM does not advance relative to the support point and base height stays `h`. Swing height is `z=h_lift·(1−cos(2πτ))/2` and horizontal motion is `x=L_max·sin(πτ)`, returning to the original position each step. Step period directly sets alternation rhythm.
3. **IK and clipping**: `d=sqrt(dx²+dz²)` and cosine relations produce joint angles, followed by URDF conversion and `q_knee=max(q_knee,θ)`. Reference velocity is differentiated from the position sequence during inverse kinematics. Clipping changes the reference, not the measured-position feedback.
4. **Tracking and load adjustment**: after entering the first frame, two-step looping, outer first-order smoothing, and output clipping continue. Step energy above 70 J ramps PD toward hard without rewriting `θ` or the trajectory.
5. **Stop and protection**: stop enters the ending segment at a loop boundary, while sustained 0.1-second over-torque exits the task. Neither branch automatically reduces `θ` or moves the joint to a patient-comfortable posture.

### Rehabilitation and Clinical Use

- Passive stepping within a restricted range may be used under external support after assessing each knee's extension range and setting a margin. The larger input applies to both legs, so confirm that the other side also tolerates it; do not use the task to force improvement of extension restriction.
- Start with low foot lift and a longer period, observing left/right loading, pelvic compensation, and actual knee angles before progressing. Suspension or fall protection remains necessary even without forward travel.
- Enable torque protection and stop for pain, spasticity, abnormal resistance, or marked loading asymmetry. Clipping constrains the reference only; actual safety still requires measured states and clinical observation.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.2.6.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.54 restored the torque-protection check, so `command_switch_1` and `command_param_9` now take effect: on over-torque of any joint the task exits immediately to the idle task (`TASK_IDLE`); it also inherits the pause command handling of TID 4112, so `command_pause` now takes effect.
- `fourier-grx` v4.4.74: the `flag_robot_torque_protection` flag set by this task's torque protection is now **latched** — it is no longer cleared when the task exits and must be cleared by the host writing `clear_flag_robot_torque_protection`. The protection behaviour itself is unchanged: the task still exits immediately to the idle task (`TASK_IDLE`).
- `fourier-grx` v4.4.75: this task's software torque protection gains a **0.1 s debounce** — the limit must now be exceeded for 0.1 s in a row (5 cycles at 50 Hz, 10 at 100 Hz, 20 at 200 Hz) before protection trips, and a single cycle back at or below the limit resets the count. The action on tripping and the flag latching are unchanged. Protection used to act with zero delay, so a momentary torque spike could end the task by mistake.
- `fourier-grx` v4.4.76: the transition from the current posture into the gait start position is shortened from 5.0 s to **2.5 s**, so entering the gait is snappier (the parameter is defined in seconds, so the real duration is the same on 50 / 100 / 200 Hz models). The knee-restriction, assist and feedforward variants that share this control model are affected too.
