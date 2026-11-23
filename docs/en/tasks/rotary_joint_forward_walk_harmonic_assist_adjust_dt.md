---
layout: default
title: Harmonic-Coefficient Assist Forward Walk (dt Adjustment)
parent: Task Description
nav_order: 4.14
has_toc: true
nav_exclude: true
---

# Harmonic-Coefficient Assist Forward Walk (dt Adjustment)

* TOC
{:toc}

## Task Info

Task ID (TID): **4133** (added in v4.4.79)

Applicable Models: M4L (P1 / T1 / T2)

Task Description:

- The gait source is identical to [Harmonic-Coefficient Forward Walk (4131)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic): a periodic joint curve sampled from pre-stored Fourier (harmonic) coefficients of the main walking tables. The **curve shape is fixed** (selected from 16 curves by the amplitude level and the knee restriction level); the **timing** is set by the cadence level.
- The assist semantics are identical to [Assist Forward Walk (dt Adjustment, 4118)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt): the assist ratio maps to the trajectory **playback speed** (play_speed ∈ [0.5, 1.0]). A larger ratio plays faster (closer to the normal cadence of the selected level); a smaller ratio plays slower, giving the patient more time to follow the motion. An automatic assist mode is available, in which the algorithm raises or lowers the assist ratio from the measured joint torque.
- Difference from 4118: **4118 generates its trajectory online with the LIPM model from step length / walking speed, while this task replays a fixed curve from the coefficient table**. Consequently there are no step-length / walking-speed / base-height / step-height / double-support-ratio parameters; the first three panel levels are exactly the same as 4131 (amplitude / knee restriction / cadence), and the assist ratio moves to `param_4`.
- The PD gains are **fixed at the medium tier for the whole task** (same as 4118: in assist scenarios the human leads and the machine follows the cadence — the hard tier is too stiff and fights the user) and do not vary with load.
- This task **commands joint angles only, not translation**: the forward travel of the base (pelvis) is not produced by the algorithm, so the actual distance covered depends on the user plus the exoskeleton as a whole.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Hip swing amplitude level | `int` | 2 | [1, 4] | Same as 4131: first axis of curve selection. The difference between the four levels is almost entirely the hip swing amplitude. Invalid or unsent values fall back to level 2. |
| Knee restriction level | `int` | 1 | [1, 4] | Same as 4131: levels 1/2/3/4 set the knee extension floor to 0 / 5 / 10 / 15°. Values are clipped to 1..4. |
| Cadence level | `int` | 3 | [1, 6] | Same as 4131: sets the "normal timing" of the trajectory. Level 1 is the slowest (5.25 s per stride) up to level 6 (3.0 s per stride). Invalid or ≤ 0 values keep the current level. |
| Assist ratio | `float` | 0.0 | [0.0, 1.0] | Playback-speed adjustment ratio (play_speed = 0.5 + ratio × 0.5). 0 = 0.5× slowest, 1 = normal speed of the selected cadence level. Treated as 0 when unsent. |
| Automatic assist mode flag | `bool` | false | (true, false) | Whether to enable automatic assist mode (switch_1). Once enabled, the algorithm judges every control period: during the swing phase, if the measured hip torque exceeds "gravity-compensation torque + 2.0 Nm" the assist ratio is increased by +0.02, and if it falls below the gravity-compensation torque it is decreased by -0.01; the ratio is always clipped to [0.0, 1.0]. Once enabled, `param_4` no longer takes effect. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop after the current loop window. |

> **Parameters with no effect here**: upper/lower leg length, step length, walking speed, base height, step lift height and double-support ratio. This task replays a pre-computed coefficient table and performs no kinematic/dynamic inversion; pushing the joystick axes does not change the trajectory either, it only triggers start/stop.

> When it takes effect:
>
> - The **assist ratio / automatic assist mode** take effect in real time during walking (play_speed is refreshed every control period).
> - The **amplitude / knee-restriction / cadence levels** apply to the current start when changed before pressing "start"; changing them during walking does not affect the running trajectory and takes effect on the next start (same as 4131).

## Module Info

This task has no dedicated module commands and does not support per-joint control through the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|-------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Current assist ratio | `rehab.assist_ratio` |
| Step frequency | `rehab.step_frequency` |
| Current gait key | `rehab.gait_name` |
| Hip swing amplitude level | `rehab.gait_amplitude_level` |
| Knee restriction level | `rehab.gait_knee_restriction_deg` |
| Cadence level | `rehab.gait_speed_level` |
| Actual stride time | `rehab.gait_stride_time_s` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

> The five gait report fields have the same semantics as 4131; see the interface section of [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic).

Command interface:

| Parameter | Interface Mapping |
|-----------|-------------------|
| Hip swing amplitude level | `grx.virtual_panel_command_param_1` |
| Knee restriction level | `grx.virtual_panel_command_param_2` |
| Cadence level | `grx.virtual_panel_command_param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Automatic assist mode flag | `grx.virtual_panel_command_switch_1` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

> ⚠️ Unlike 4118: the **assist ratio is on `param_4`** (`param_3` is taken by the cadence level); `param_1` / `param_2` are the amplitude / knee-restriction levels, not step length / walking speed. Host software must use the mapping in this table instead of reusing 4118's parameter positions.

## Principle Explanation

### Algorithm Operation

This task changes the **phase timeline's playback speed**, not the harmonic curve itself:

1. **Base trajectory**: amplitude, restriction, and cadence first determine `q(φ)` and `T_stride` exactly as in TID 4131. Assist processing occurs after generation and does not refit the Fourier coefficients.
2. **Time scaling**: manual mode maps `r` to `v_play=0.5+0.5r` and advances `Δt_motion=Δt_control·v_play` each cycle. Actual period is approximately `T_actual=T_base/v_play`: `r=0` roughly doubles it and `r=1` restores the selected cadence. Kp/Kd remain at the medium tier regardless of `r`.
3. **Automatic decisions**: only during the loop and the relevant leg's swing, with `G>0` and negative hip reference velocity, `τ>G+2.0 Nm` gives `r←r+0.02`, while `τ<G` gives `r←r−0.01`. Other phases leave it unchanged before clipping to `[0,1]`. Unequal increments make acceleration faster than deceleration.
4. **Feedback location**: torque changes only subsequent trajectory-index progression. It adds no direct assistive torque and does not alter the angular envelope. Because measured torque includes both patient and device effects, this is a heuristic rhythm rule, not a general patient-intent detector or proof of assist-as-needed behavior.

### Rehabilitation and Clinical Use

- A low ratio means a slower, easier-to-follow rhythm, not lower joint stiffness or a smaller passive range. For patients who need more response time, reduce playback speed first and progress toward the selected level's normal rhythm as tolerated.
- Automatic assist uses total joint torque, which can also include device gravity, friction, and inertial effects. It is not a direct measure of voluntary muscle force or intention. Observe the changing rhythm and stop for unexpected acceleration, fatigue, or deteriorating movement quality.
- Select the fixed curve, knee restriction, and base cadence before adjusting playback. Do not raise cadence level and assist ratio together. External support and continuous clinical monitoring remain necessary.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Changelog

- `fourier-grx` v4.4.79: task added (TID 4133). Gait source and the three panel levels are identical to 4131; dt-assist semantics are identical to 4118 (assist ratio → play_speed ∈ [0.5, 1.0], automatic assist mode supported, PD fixed at the medium tier).
