---
layout: default
title: Stand Motion Control (Knee Restriction)
parent: Task Description
nav_order: 4.20
has_toc: true
nav_exclude: true
---

# Stand Motion Control (Knee Restriction)

* TOC
{:toc}

## Task Info

Task ID (TID): **4300**

Task Description:

- The robot slowly moves all joints back to the standing posture.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Left restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Right restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Enable torque protection | `bool` | false | (true, false) | Whether to enable torque protection. When enabled, if the torque of any joint exceeds the torque protection limit continuously for at least 0.1 s (since v4.4.75), the task exits immediately and switches to the idle task (`TASK_IDLE`), and sets the torque-protection flag; the task must be re-issued to continue. |
| Torque protection limit | `float` | None | [0.0, 200.0] | Maximum allowable output torque for any joint during the standing process, in Nm. Only effective when torque protection is enabled; disabled by default. |

> **Knee Restriction Angle Explained**:
>
> The left/right inputs are candidate restrictions. Current code first computes `θ=max(θ_left,θ_right)`, then sets both knee targets in the standing reference to the same `θ`. This affects the algorithmic reference, not independent mechanical stops on the actual joints. When clinical restrictions differ by side, interpret device behavior using the larger restriction requirement.
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

Command interface:

- The upper leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.
- The lower leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.

| Parameter | Interface Mapping |
|-----------|------------------|
| Upper leg length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Lower leg length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Left knee restriction angle | `grx.virtual_user_knee_restriction_left` |
| Right knee restriction angle | `grx.virtual_user_knee_restriction_right` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Principle Explanation

### Algorithm Operation

Restricted standing first uses two-link geometry to **construct a flexed standing target**, then reuses the normal standing state machine:

1. **Combine left/right inputs**: although the interface exposes `knee_restriction_left/right`, current code uses `θ=max(θ_left,θ_right)` for both legs. Restriction is not independent by side; the larger input determines both final knee targets.
2. **Standing geometry**: with thigh/shank lengths `L_t,L_s`, `α=atan2(L_s·sinθ,L_t+L_s·cosθ)` and `β=θ−α` decompose the posture, producing `q_stand=[−α,θ,−α,θ]`. Geometric base height is `h=L_t·cosα+L_s·cosβ`, explaining the forward inclination and lower stance associated with greater knee flexion.
3. **Damping and interpolation**: a 0.2-second `Kp=0` damping warmup is followed by latched `q0` and `q_ref=q0+(q_stand−q0)·min(t/5,1)`, avoiding a direct jump into the restricted stance.
4. **Settling and holding**: after interpolation, position-window change must stay within 0.01 rad and speed within 0.05 rad/s for 0.2 consecutive seconds. Kp/Kd then ramp from medium to rock over one second while the restricted target is held; only then does `motion_ratio` reach 100%.
5. **Protection boundary**: torque protection reads actual actuator feedback, not reference angles. Target `θ` cannot prevent additional motion caused by external forces and is no substitute for mechanical stops or clinical supervision.

### Rehabilitation and Clinical Use

- Assess passive knee extension, pain, and spasticity for each leg before setting the inputs with an individualized safety margin. Because the larger input applies to both legs, check the overall stance for the side needing more restriction; never use this parameter to force progressive extension.
- A larger restriction creates a more flexed support posture and changes loading and torque demand. Introduce it briefly under external support and observe actual knee angles, trunk compensation, and torque rather than relying on target angles alone.
- This is not active sit-to-stand or balance training; `motion_ratio=100%` only indicates completion of the device sequence. Stop for pain, resistance, or abnormal torque. Software clipping does not replace hardware limits or clinical supervision.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.2.6.
- `fourier-grx` v4.4.72 switches this task from the baseline to the medium PD tier: M4LP1 uses kp `[350×4]` / kd `[25×4]`, and M4LT1 / M4LT2 use kp `[500×4]` / kd `[30×4]`. This task shares the standing algorithm; the 0.2 s pure-damping warm-up is unchanged, with the medium tier restored afterwards.
- `fourier-grx` v4.4.74: the `flag_robot_torque_protection` flag set by this task's torque protection is now **latched** — it is no longer cleared when the task exits and must be cleared by the host writing `clear_flag_robot_torque_protection`. The protection behaviour itself is unchanged: the task still exits immediately to the idle task (`TASK_IDLE`).
- `fourier-grx` v4.4.75: this task's software torque protection gains a **0.1 s debounce** — the limit must now be exceeded for 0.1 s in a row (5 cycles at 50 Hz, 10 at 100 Hz, 20 at 200 Hz) before protection trips, and a single cycle back at or below the limit resets the count. The action on tripping and the flag latching are unchanged. Protection used to act with zero delay, so a momentary torque spike could end the task by mistake.
- `fourier-grx` v4.4.76: this task's arrival check adds a **settle confirmation** on top of the interpolation time — once the target is pinned at the standing position it also needs 0.2 s in a row of «position change ≤ 0.01 rad within the window and |velocity| ≤ 0.05 rad/s on every joint» before the hold stage, with a 2.5 s timeout fallback that proceeds and logs a warning. Previously the switch happened the moment the timer expired, which discarded the support torque associated with the dynamic lag between measured and commanded position and showed up as a twitch. `motion_ratio` is capped at 99.9% and `flag_task_finish` is delayed until the robot is settled; setting `flag_settle_check` to False restores the time-only behaviour.
- `fourier-grx` v4.4.85: as in the standing task, PD gains ramp linearly from medium to rock over **1.0 s** after settling (kp `[5000,2500,5000,2500]`, kd `[120,60,120,60]`). 100% and task completion are reported only after rock is reached; knee-restricted target positions remain unchanged.
