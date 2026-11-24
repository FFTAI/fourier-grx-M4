---
layout: default
title: Assisted Forward Walking (dt Mode)
parent: Task Description
nav_order: 4.16
has_toc: true
nav_exclude: true
---

# Assisted Forward Walking (dt Mode)

* TOC
{:toc}

## Task Info

Task ID (TID): **4118**

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for forward walking, and the actuators track that trajectory to achieve assisted forward walking.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.
- Assist intensity is controlled by the assist ratio: a higher value speeds up trajectory playback (closer to a normal walking pace); a lower value slows playback down, giving the patient more time to follow the motion.
- An automatic assist mode is available. When the "auto assist mode flag" is enabled, the robot automatically adjusts the assist ratio based on measured joint torques, with no manual setting required.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Step length | `float` | 0.5 | [0.2, 0.8] | The length of each step, in m. |
| Walking speed | `float` | 0.5 | [0.1, 1.2] | The target forward speed, in m/s. Single-step duration = step length ÷ walking speed (e.g., with step length 0.5 m and speed 0.5 m/s, each step takes approximately 1.0 s). |
| Assist ratio | `float` | 0.5 | [0.0, 1.0] | Scaling factor for trajectory playback speed, in the range [0.0, 1.0]. A higher value plays the trajectory faster (closer to normal walking pace); a lower value plays it slower, giving the patient more time to follow the motion. |
| Auto assist mode flag | `bool` | false | (true, false) | Whether to enable automatic assist mode. When enabled, the algorithm decides every control cycle (20 ms): during the swing phase, if the measured hip joint torque exceeds “gravity-compensated torque + 2.0 Nm” the assist ratio increases by 0.02, and if it falls below the gravity-compensated torque it decreases by 0.01; no manual setting is required. The assist ratio is always clamped to [0.0, 1.0]. While auto mode is on, `param_3` no longer applies. |
| Base height (pelvis height) | `float` | None | [0.6, 1.2] | The height of the base (pelvis) above the ground while walking, in m. When ≤ 0 or not sent, it is automatically set to the sum of the thigh and shank lengths. Values outside the range are clipped. Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Step lift height | `float` | 0.1 | [0.05, 0.2] | The maximum lift height of the swing foot, in m. When ≤ 0 or not sent, the default value is used. Values outside the range are clipped. Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Double-support ratio | `float` | 0.2 | [0.1, 0.3] | The proportion of the double-support phase within a single step cycle. When ≤ 0 or not sent, the default value is used. Values outside the range are clipped. **This task uses the DSP gait generator, and this parameter participates in trajectory generation**. Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue walking. |

> **Assist Ratio Explained**:
>
> The assist ratio controls pacing by adjusting the trajectory playback speed (play\_speed). The formula is:
>
> - **play\_speed** = 0.5 + assist ratio × 0.5, so play\_speed ∈ [0.5, 1.0]
> - Trajectory time advance per control cycle: Δt = 0.02 s × play\_speed
>
> | Assist Ratio | play\_speed | Effect |
> |--------------|-------------|--------|
> | 0.0 | 0.5 | Trajectory plays at 50% speed; each step takes twice the normal time — suitable for patients with weaker motor ability |
> | 0.5 | 0.75 | Trajectory plays at 75% speed; moderate step frequency |
> | 1.0 | 1.0 | Trajectory plays at normal speed — suitable for patients with near-normal motor ability |

> Recommendation:
> - A step length between 0.5× and 1.0× the walking speed tends to produce good walking results. For example, at a walking speed of 0.5 m/s, a step length of 0.25 m to 0.5 m is recommended.

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

> Note: Since v4.4.32, `reference_joint_position_max`/`reference_joint_position_min` only report the joint angle range during the steady-state phase of "cyclic walking/marking time", excluding transient extrema during the start-up and finishing transition phases.

Command interface:

- The upper leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.
- The lower leg length accepts a single value in the algorithm, so the average of the left and right values is used. Two values are passed, but only their mean is applied.

| Parameter | Interface Mapping |
|-----------|------------------|
| Upper leg length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Lower leg length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Step length | `grx.virtual_panel_command_param_1` |
| Walking speed | `grx.virtual_panel_command_param_2` |
| Assist ratio | `grx.virtual_panel_command_param_3` |
| Base height (pelvis height) | `grx.virtual_panel_command_param_6` |
| Step lift height | `grx.virtual_panel_command_param_7` |
| Double-support ratio | `grx.virtual_panel_command_param_8` |
| Auto assist mode flag | `grx.virtual_panel_command_switch_1` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

## Principle Explanation

### Algorithm Operation

This task adds **trajectory-time scaling feedback** to a DSP forward gait rather than providing assistance by reducing PD stiffness:

1. **Fixed geometry**: step length, speed, leg lengths, and foot lift first produce the complete COM, foot, and joint-reference arrays through the usual single-support/double-support segmentation, inverted-pendulum, and inverse-kinematics calculations. Assist only reads these arrays and does not change their angular envelope.
2. **Playback mapping**: `r` determines `v_play=0.5+0.5r`; motion time advances by `Δt_motion=Δt_control·v_play`, with index `floor(t_motion/Δt_control)`. Slowing playback holds each reference frame longer, approximately `T_actual=T_base/v_play`, rather than recomputing a slower gait.
3. **Automatic mode**: during the loop, only a swinging leg with `G>0` and negative hip reference velocity is evaluated. `τ_hip>G+2.0 Nm` gives `r+=0.02`; `τ_hip<G` gives `r−=0.01`, followed by `[0,1]` clipping. Pinocchio computes `G` from current posture, and unequal increments make acceleration and deceleration asymmetric.
4. **Control output**: positions retain outer smoothing and travel limits, tracked by medium-tier PD. Load detection and automatic stiffness ramping are disabled. Torque changes subsequent `v_play` only; it is never appended directly to actuator effort.

“More assist” therefore means faster reference playback and a shorter actual gait cycle, not higher Kp/Kd or a fixed percentage of assistive force.

### Rehabilitation and Clinical Use

- This mode can support rhythm-matching practice, but “more assist” here means faster playback, not greater assistive torque. Reduce the ratio when the patient needs more response time and increase gradually as tolerated.
- Measured torque reflects the patient and device together and cannot independently distinguish voluntary effort, spasticity, contact, or device load. Introduce automatic mode slowly and briefly with continuous observation; leave automatic mode for unexpected acceleration or rhythm fluctuations.
- Set step length, base speed, and foot lift for the patient's range and tolerance. Automatic adjustment is neither balance control nor a safety function. Assess actual gait, compensation, and fatigue as well.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.0.0.
- `fourier-grx` v4.4.24: Adjusted the auto assist mode increments from symmetric ±0.01 to +0.02 (increased when the user exerts effort) / -0.01 (decreased when the user's effort is insufficient), speeding up the assist response.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.48 added the base height / step lift height / double-support ratio parameter interfaces.
- `fourier-grx` v4.4.66 switches this task's PD gains from the hard tier to the medium tier for the whole task (T1/T2: kp `[400,500,400,500]` / kd `[30×4]`; M4LP1: kp `[350×4]` / kd `[30,25,30,25]`): in the human-led, robot-follows assist scenario the hard tier was too stiff and fought the user; the medium tier does not ramp with load detection.
- `fourier-grx` v4.4.68 unifies the medium tier kp from `[400,500,400,500]` to `[500,500,500,500]` (kd unchanged at `[30,30,30,30]`), so the assist feel is slightly firmer than in v4.4.66. The M4LT2 control rate was also raised to 200 Hz (`control_period` 0.01 → 0.005); this task's timing parameters (debouncing, load-detection filter and PD ramp, gait smoothing filter) are defined in seconds, so their durations are unchanged once converted to cycle counts.
- `fourier-grx` v4.4.70: ⚠️ the keyboard default walking speed doubles from 0.25 to 0.5 m/s (step duration halves at the same step length; the old 0.25 was below the gait generators' own 0.5 default and is now aligned). Panel and host settings still take precedence. This task keeps using the medium PD tier throughout, so the hard tier's rise to kp 1500 / kd 90 does not affect it; the inherited gait smoothing filter cutoff (2.5 → 8.0 Hz) and total delay compensation (0.06 → 0.03 s) do apply.
- `fourier-grx` v4.4.71: **the v4.4.70 tuning is reverted** — the inherited gait smoothing filter cutoff returns to 2.5 Hz and the total delay compensation to 0.06 s. This task still uses the medium tier throughout (kp `[500×4]` / kd `[30×4]`), so the hard tier's rise and reversion never reached it. ⚠️ The keyboard walking default stays at 0.5 m/s (not reverted); panel and host settings take precedence.
- `fourier-grx` v4.4.72 unifies M4LP1 medium-tier kd from `[30,25,30,25]` to `[25×4]` (hip damping 30 → 25, knees unchanged; kp remains `[350×4]`). This task uses that tier throughout and inherits the change; T1/T2 are unchanged.
