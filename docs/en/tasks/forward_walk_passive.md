---
layout: default
title: Passive Forward Walk
parent: Task Description
nav_order: 4.11
has_toc: true
nav_exclude: true
steps:
  - Power-on self-check
  - Joint zero calibration
  - Standing posture
  - Passive forward walk
current_step: 4
---

# Passive Forward Walk

* TOC
{:toc}

## Task Info

Task ID (TID): **4129** (since v4.4.69; previously 4111)

Task Description:

- The robot uses the given parameters to generate a joint trajectory sequence for forward walking, and the actuators track that trajectory to achieve passive forward walking.
- When the "stop motion flag" is set to true, the robot will gradually stop rather than halt immediately.
- If the task enters a torque protection state, the robot will pause motion and set the "task pause flag" to true. The task must be restarted to resume walking.

> **Danger: prepare before entering walking mode**
>
> Before pressing Y to enter walking mode, confirm the emergency stop is available, the area around the robot is clear, and support is in place. Pressing the logo button disables the robot and it will go limp; prevent it from falling or hitting anything.

> ⚠️ **Version change: TID semantics**
>
> Since v4.4.69, 4111 maps to the PD + velocity feed-forward variant. Use 4129 for passive forward walking, and update the host task table after a firmware upgrade to avoid calling the wrong task.

{% include components/grx_steps.html steps=page.steps current=page.current_step %}

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Upper leg length | `float` | 0.5 | [0.3, 0.6] | The robot's upper leg (thigh) length, in m. |
| Lower leg length | `float` | 0.5 | [0.3, 0.6] | The robot's lower leg (shank) length, in m. |
| Step length | `float` | 0.5 | [0.2, 0.8] | The length of each step, in m. |
| Walking speed | `float` | 0.5 | [0.1, 1.2] | The target forward speed, in m/s. Single-step duration = step length ÷ walking speed (e.g., with step length 0.5 m and speed 0.5 m/s, each step takes approximately 1.0 s). |
| Base height (pelvis height) | `float` | None | [0.6, 1.2] | The height of the base (pelvis) above the ground while walking, in m. When ≤ 0 or not sent, it is automatically set to the sum of the thigh and shank lengths. Values outside the range are clipped. Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Step lift height | `float` | 0.1 | [0.05, 0.2] | The maximum lift height of the swing foot, in m. When ≤ 0 or not sent, the default value is used. Values outside the range are clipped. Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Double-support ratio | `float` | 0.2 | [0.1, 0.3] | The proportion of the double-support phase within a single step cycle. When ≤ 0 or not sent, the default value is used. Values outside the range are clipped. This task uses the DSP gait generator, so this parameter is effective (the PD / dt assist tasks use the vhip generator, where it has no effect). Takes effect at the next start of walking (trajectory regeneration); changes made while walking do not affect the trajectory currently being executed. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop; false = continue walking. |
| Pause motion flag | `bool` | false | (true, false) | Whether to pause motion. true = pause; the task must be restarted to resume walking. |
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. |
| Torque protection limit | `float` | None | [0.0, 200.0] | The maximum allowable output torque for any joint during walking, in Nm. If the real-time torque of any joint exceeds this limit continuously for at least 0.1 s (since v4.4.75), the task pauses and sets the "task pause flag". Takes effect only when torque protection is enabled; disabled by default. |

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
| Task pause flag | `task.flag_task_pause` |
| Motion ratio | `rehab.motion_ratio` |
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
| Base height (pelvis height) | `grx.virtual_panel_command_param_6` |
| Step lift height | `grx.virtual_panel_command_param_7` |
| Double-support ratio | `grx.virtual_panel_command_param_8` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Pause motion flag | `grx.virtual_panel_command_pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Principle Explanation

### Algorithm Operation

The control chain has four layers: **gait geometry → two-link inverse kinematics → trajectory conditioning → PD tracking with load-based gain adjustment**.

1. **Single/double support timing**: hip extension is scaled and internal step length is compensated to preserve the intended foot displacement. For compensated internal step length `S_g`, `T_step=S_g/v`, `T_dsp=r_dsp·T_step`, and `T_ssp=T_step−T_dsp`. Double support therefore reallocates the step timeline rather than appending a pause.
2. **COM and foot trajectories**: during single support (SSP), horizontal COM motion uses the linear inverted-pendulum approximation `ẍ=ω²x`, `ω=sqrt(g/h)`. During double support (DSP), both feet remain fixed while a cubic Hermite spline transfers the COM with position and velocity continuity. Swing-foot horizontal motion uses a smooth velocity profile; vertical motion is `z=h_lift·(1−cos(2πτ))/2`, returning to zero at both ends and peaking mid-swing.
3. **Foot position to joint angles**: for each frame, `dx,dz` locate the foot relative to the COM and `d=sqrt(dx²+dz²)` is limited to leg length. The law of cosines gives `q_knee=π−acos((L_thigh²+L_shank²−d²)/(2L_thighL_shank))`; hip angle follows from `atan2(dz,dx)` and the second cosine relation. Angles are converted to the URDF frame, scaled/restricted/smoothed, and differentiated to produce consistent reference velocities.
4. **State-machine playback**: measured positions are held before start. Starting triggers a 2.5-second linear move to the first gait frame, followed by start, loop, and ending segments. Each position passes through `q_cmd[k]=(1−α)q_cmd[k−1]+αq_ref[k]` and joint-limit clipping before PD control. Stop is evaluated at the loop-window boundary rather than freezing immediately.
5. **Load-based stiffness**: `P_i=τ_i·ω_i` is low-pass filtered, and positive power is accumulated as `E=Σ max(P_i,0)·Δt`. If `E>30 J` at the step boundary, load is declared and Kp/Kd ramp toward the hard tier. This changes tracking stiffness, not patient-weight estimates or the generated gait geometry.

### Rehabilitation and Clinical Use

- Passive guidance can help a therapist assess tolerance to low-load, repeatable joint motion, but it is not active walking practice. Start with shorter steps, lower speed and foot lift, and full external support; adjust one parameter at a time according to pain, fatigue, and movement quality.
- A larger double-support ratio lengthens that phase of the reference gait, but it does not replace suspension, fall protection, or manual guarding and does not prove whole-body balance.
- Enable and individualize torque protection. Continue to observe actual joint positions, foot clearance, straps, and skin. `reference_joint_*` describes commanded motion, not the patient's measured gait or treatment outcome.
- Stop and reassess for resistance, pain, increased spasticity, foot contact, or abnormal vital signs.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.0.0.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.48 added the base height / step lift height / double-support ratio parameter interfaces.
- `fourier-grx` v4.4.65 added two feedforward task variants: position loop + velocity feedforward (TID 4124) and PD + velocity feedforward (TID 4126). The velocity feedforward is derived by numerically differentiating the actually-commanded target; the POSITION variant runs the actuator position loop (PID values in the robot parameter class), the PD variant maps kd × target velocity to an equivalent feedforward torque (note: the FSA v2 protocol has no velocity field, so the PD feedforward only takes effect on M4LT2).
- `fourier-grx` v4.4.68: the M4LT2 control rate was raised to 200 Hz (`control_period` 0.01 → 0.005) and this task's total reference-trajectory delay compensation was reduced accordingly from 0.12 s to 0.06 s (converted to a frame index from the control period); the hard tier was retuned to kp `[1000,1000,1000,1000]` / kd `[60,60,60,60]` (hip ζ=0.63 unloaded / 0.52 loaded, knee ζ=1.12 / 1.04 overdamped). Also fixed: the feedforward variants of this task (TID 4124 / 4126) never applied velocity feedforward, because the tasks are scheduled as `STANDALONE` by default while the hook only covered `function_component`.
- `fourier-grx` v4.4.69: to group the feedforward variants by control mode, this task's TID changed from **4111** to **4129**, and **4111 now refers to this task's PD + velocity-feedforward variant** (previously 4126); the POSITION variant shifts from 4124 to **4125**. ⚠️ Hosts must be updated — calling 4111 now selects the feedforward variant rather than this task. The feedforward family grows from 4 to 8 tasks in this release (adding the sinusoidal-trajectory and harmonic variants).
- `fourier-grx` v4.4.70: the hard tier rises to kp `[1500×4]` / kd `[90×4]` (hip ζ=0.77 unloaded / 0.64 loaded, knee ζ=1.37 / 1.28), so this task's load-detection PD ramp covers a wider span and tops out in about 8.7 s (T2) / 10.1 s (T1); the gait smoothing filter cutoff moves from 2.5 to 8.0 Hz (group delay about 15–17 ms) and the total reference-trajectory delay compensation from 0.06 s to 0.03 s. ⚠️ The keyboard default walking speed doubles from 0.25 to 0.5 m/s, halving step duration at the same step length. With the stiffer hard tier, the tracking error needed to trip the 140 N·m over-torque protection falls from about 8° to about 5.3°.
- `fourier-grx` v4.4.71: **the v4.4.70 tuning is reverted** — the hard tier returns to kp `[1000×4]` / kd `[60×4]` (hip ζ=0.63 unloaded / 0.52 loaded, knee ζ=1.12 / 1.04), the gait smoothing filter cutoff to 2.5 Hz, the total delay compensation to 0.06 s and the load-detection PD ramp floor to 0.01. The tracking error needed to reach the 140 N·m over-torque protection goes back to about 8°. ⚠️ The keyboard default walking speed, however, **stays at 0.5 m/s and was not reverted** (cadence remains doubled relative to 4.4.69); use the panel or host velocity parameter for a slower pace.
- `fourier-grx` v4.4.74: the `flag_robot_torque_protection` flag set by this task's torque protection is now **latched** — it is no longer cleared when the task exits and must be cleared by the host writing `clear_flag_robot_torque_protection`. The protection behaviour itself is unchanged: the task still exits immediately to the idle task (`TASK_IDLE`).
- `fourier-grx` v4.4.75: this task's software torque protection gains a **0.1 s debounce** — the limit must now be exceeded for 0.1 s in a row (5 cycles at 50 Hz, 10 at 100 Hz, 20 at 200 Hz) before protection trips, and a single cycle back at or below the limit resets the count. The action on tripping and the flag latching are unchanged. Protection used to act with zero delay, so a momentary torque spike could end the task by mistake.
- `fourier-grx` v4.4.76: the transition from the current posture into the gait start position is shortened from 5.0 s to **2.5 s**, so entering the gait is snappier (the parameter is defined in seconds, so the real duration is the same on 50 / 100 / 200 Hz models). The knee-restriction, assist and feedforward variants that share this control model are affected too.
