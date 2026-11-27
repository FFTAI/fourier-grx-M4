---
layout: default
title: Assisted Marching in Place (Knee Restriction, dt Mode)
parent: Task Description
nav_order: 4.254
has_toc: true
nav_exclude: true
---

# Assisted Marching in Place (Knee Restriction, dt Mode)

* TOC
{:toc}

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Assisted Marching in Place (Knee Restriction, dt Mode) | **4306** | Assist (dt Mode) |

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for marching in place, and the actuators track that trajectory to achieve assisted mark time.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.
- Assist intensity is controlled by the assist ratio: a higher value speeds up trajectory playback (closer to a normal stepping cadence); a lower value slows playback down, giving the patient more time to follow the motion.
- An automatic assist mode is available. When the "auto assist mode flag" is enabled, the robot automatically adjusts the assist ratio based on measured joint torques, with no manual setting required.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Left knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Left restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Right knee restriction angle | `float` | 0.0 | [0.0, 1.0] | Right restriction input in rad. The larger of the left/right inputs becomes the common minimum flexion reference for both knees. 0.0 means no restriction (full extension allowed). |
| Step height | `float` | 0.1 | [0.1, 0.4] | The leg-lift height for each step, in m. |
| Step period | `float` | 1.0 | [0.5, 4.0] | The cycle duration for one complete stepping cycle, in s. A smaller value means a higher step frequency; a larger value means a slower step. |
| Assist ratio | `float` | 0.0 | [0.0, 1.0] | Scaling factor for trajectory playback speed, in the range [0.0, 1.0]. A higher value plays the trajectory faster (closer to normal stepping cadence); a lower value plays it slower, giving the patient more time to follow the motion. |
| Assist trigger force upper | `float` | 2.0 | [-∞, +∞] | Absolute torque threshold that triggers an **increase** in assist ratio, in Nm. When measured joint torque exceeds this value, assist ratio increases by 0.04. Only active in auto assist mode. |
| Assist trigger force lower | `float` | 1.0 | [-∞, +∞] | Absolute torque threshold that triggers a **decrease** in assist ratio, in Nm. When measured joint torque falls below this value, assist ratio decreases by 0.001. Only active in auto assist mode. |
| Auto assist mode flag | `bool` | false | (true, false) | Whether to enable automatic assist mode. When enabled, the system automatically adjusts the assist ratio each control cycle using absolute torque thresholds gated by swing state, gravity-term sign, and hip reference velocity; the cycle duration is set by the model's `control_period` (+0.04 when the patient pushes, −0.001 when the patient is not contributing), with no manual setting required; the assist ratio is always clamped to [0.0, 1.0]. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue stepping. |

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

> **Assist Ratio Explained**:
>
> The assist ratio controls pacing by adjusting the trajectory playback speed (play\_speed). The formula is:
>
> - An unsent virtual-panel value defaults to 0.0. Only an actual `None` input, when neither panel nor joystick supplies a value, falls back to 1.0.
> - **play\_speed** = 0.5 + assist ratio × 0.5, so play\_speed ∈ [0.5, 1.0]
> - Trajectory time advance per control cycle: Δt_motion = `control_period` × play\_speed
>
> | Assist Ratio | play\_speed | Effect |
> |--------------|-------------|--------|
> | 0.0 | 0.5 | Trajectory plays at 50% speed; each step takes twice the normal time — suitable for patients with weaker motor ability |
> | 0.5 | 0.75 | Trajectory plays at 75% speed; moderate step frequency |
> | 1.0 | 1.0 | Trajectory plays at normal speed — suitable for patients with near-normal motor ability |

> **Assist Trigger Force Thresholds Explained**:
>
> These parameters are used directly as absolute torque thresholds to control automatic increases and decreases of the assist ratio.
>
> > **Note**: The design originally considered adding the gravity compensation torque G[i] to the thresholds (i.e., threshold = G[i] + offset) to make the trigger condition posture-adaptive.
> > However, experimental testing showed that including G[i] tended to cause system instability, so the G[i] coefficient has been set to zero for now.
> > The configured values are used directly as absolute thresholds.
>
> | Condition | Effect |
> |-----------|--------|
> | Measured torque > `assist_trigger_force_upper` | assist\_ratio += 0.04 (patient is actively pushing → increase assist) |
> | Measured torque < `assist_trigger_force_lower` | assist\_ratio -= 0.001 (patient is not contributing → decrease assist) |
> | Otherwise | assist\_ratio unchanged |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Current assist ratio | `rehab.assist_ratio` |
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
| Assist ratio | `grx.virtual_panel_command_param_3` |
| Assist trigger force upper | `grx.virtual_panel_command_param_4` |
| Assist trigger force lower | `grx.virtual_panel_command_param_5` |
| Auto assist mode flag | `grx.virtual_panel_command_switch_1` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Principle Explanation

### Algorithm Operation

This task first generates a commonly restricted in-place gait and then scales its playback clock:

1. **Common restriction**: `θ=max(θ_left,θ_right)` applies to both knees. Two-link relations `α=atan2(L_s·sinθ,L_t+L_s·cosθ)`, `β=θ−α`, and `h=L_t·cosα+L_s·cosβ` give base height; the inputs do not act independently.
2. **Fixed envelope**: half-cosine foot lift and sinusoidal fore/aft motion form an in-place cycle. After IK, `q_knee=max(q_knee,θ)` is applied; assist never recalculates these angles.
3. **Time scaling**: `v_play=0.5+0.5r` advances the trajectory clock by `Δt_control·v_play`, giving approximately `T_base/v_play`. Medium PD, restriction, and lift amplitude remain unchanged; slow playback only holds each frame longer.
4. **Automatic thresholds**: during target-leg swing with `G<0` and negative hip reference velocity, `τ>τ_upper` gives `r+=0.04` and `τ<τ_lower` gives `r−=0.001`, followed by clipping. Gravity compensation is zeroed and absolute thresholds come from `param_4/param_5`.
5. **Output boundary**: automatic assist changes subsequent indices only and adds no direct torque. The reference satisfies the lower bound, but actual knee motion still depends on PD tracking and patient interaction.

### Rehabilitation and Clinical Use

- Set restrictions for each knee's clinical range, then begin with low foot lift, a long period, and slow playback. Slower playback provides more following time but does not reduce the flexed posture imposed by restriction or device stiffness.
- Validate absolute torque thresholds carefully for each patient. Torque can also reflect spasticity, resistance, or device load and is not a direct measure of voluntary effort. Leave automatic mode for unexpected acceleration or instability and reassess.
- Continuously observe actual knee angles, left/right loading, pain, and fatigue with external support. Task completion or steady cadence alone does not demonstrate safe, effective treatment.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.2.6.
- `fourier-grx` v4.4.4 added the `Assist trigger force upper` / `Assist trigger force lower` parameters as configurable absolute torque thresholds for auto assist mode. Experimental testing showed that including the gravity compensation term G[i] in the threshold formula caused system instability; the G[i] coefficient has been set to zero and the configured values are used directly as absolute thresholds.
- `fourier-grx` v4.4.25 adjusted the auto-decrement applied when torque falls below the assist trigger force lower threshold from −0.01 to −0.001, avoiding assist instability caused by the assist ratio decaying too quickly in mark-time scenarios; the +0.02 increment for the upper threshold (since v4.4.24) remains unchanged.
- `fourier-grx` v4.4.30 raised the auto-increment applied when torque exceeds the assist trigger force upper threshold from +0.02 to +0.04, further speeding up the assist response when the patient pushes.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.72 unifies M4LP1 medium-tier kd from `[30,25,30,25]` to `[25×4]` (hip damping 30 → 25, knees unchanged; kp remains `[350×4]`). This task uses that tier throughout and inherits the change; T1/T2 are unchanged.
