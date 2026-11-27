---
layout: default
title: Passive Marching in Place
parent: Task Description
nav_order: 4.14
has_toc: true
nav_exclude: true
---

# Passive Marching in Place

* TOC
{:toc}

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Passive marching in place | **4130** | PD |
| Passive marching in place + velocity feedforward | **4112** | PD + velocity feedforward |
| Passive marching in place · POSITION + velocity feedforward | **4126** | POSITION + velocity feedforward |

> The POSITION + velocity feedforward variant runs the actuator position loop; its parameters match the PD variants.

Task Description:

- The robot generates a joint motion trajectory sequence for mark time based on the given parameters, and drives the actuators to track that trajectory, achieving Passive Marching in Place.
- When the "stop motion flag" is set to true, the robot will gradually slow down and stop rather than halting immediately.
- Once torque protection is triggered, the robot immediately exits this task and switches to the idle task (`TASK_IDLE`), and the torque-protection flag is set. This task must be sent again before stepping can continue.
- 4112 shares the trajectory and panel parameters of 4130 and only adds reference velocity feedforward during execution; FSA v2 frames on P1/T1 have no velocity field, so PD feedforward is effective only on M4LT2.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Thigh length | `float` | 0.5 | [0.3, 0.6] | The robot's thigh length, in m. |
| Shank length | `float` | 0.5 | [0.3, 0.6] | The robot's shank length, in m. |
| Step lift height | `float` | 0.1 | [0.1, 0.4] | The leg lift height for each step, in m. |
| Step cycle | `float` | 1.0 | [0.5, 4.0] | The single-step cycle for mark time — the time required to complete one full stepping cycle, in s. A smaller value means a higher step frequency; a larger value means slower stepping. |
| Base height (pelvis height) | `float` | None | [0.6, 1.2] | The height of the base (pelvis) above the ground while stepping, in m. When ≤ 0 or not sent, it is automatically set to the sum of the thigh and shank lengths. Values outside the range are clipped. Takes effect at the next start of stepping (trajectory regeneration); changes made while stepping do not affect the trajectory currently being executed. |
| Start motion flag | `bool` | false | (true, false) | Whether to start the motion. true = start; false = do not start (has no effect if already started). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop the motion. true = stop; false = continue stepping. |
| Pause motion flag | `bool` | false | (true, false) | Whether to pause the motion. true = pause; the task must be restarted to continue stepping. |
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. |
| Torque protection limit | `float` | None | [0.0, 200.0] | The maximum allowable output torque for any joint during stepping, in Nm. If the real-time torque of any joint exceeds this limit continuously for at least 0.1 s (since v4.4.75), the robot immediately exits this task and switches to the idle task (`TASK_IDLE`), and the torque-protection flag is set. Only effective when torque protection is enabled; disabled by default. |

> Note: In this task, the step lift height is still set via the existing `grx.virtual_panel_command_param_1` interface (see the "Step lift height" row above); the new panel interfaces `param_7`/`param_8` have no effect on this task.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

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

Command Interface:

- Thigh length: only one value can be input in the algorithm; therefore the average of the left and right thigh lengths is used. Two values are passed, but only their average is used.
- Shank length: only one value can be input in the algorithm; therefore the average of the left and right shank lengths is used. Two values are passed, but only their average is used.

| Parameter | Interface Mapping |
|-----------|------------------|
| Thigh length | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, averaged |
| Shank length | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, averaged |
| Step lift height | `grx.virtual_panel_command_param_1` |
| Step cycle | `grx.virtual_panel_command_param_2` |
| Base height (pelvis height) | `grx.virtual_panel_command_param_6` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Pause motion flag | `grx.virtual_panel_command_pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Principle Explanation

### Algorithm Operation

In-place stepping uses the VHIP two-link geometry generator while fixing the COM and support point: **alternating periodic foot motion → hip/knee IK → cyclic playback**.

1. **Timing**: the input step period directly becomes `T_step`. One leg swings while the other supports, then roles reverse on the next step; reported cadence is `60/T_step` steps/min. Unlike forward walking, period is not derived from step length divided by speed.
2. **Foot trajectories**: support-foot position, horizontal COM position, and base height remain fixed. Swing-foot height is `z=h·(1−cos(2πτ))/2`, and fore/aft motion is `x=L_max·sin(πτ)`, where `L_max=min(2h,L_thigh)`. The foot returns to its original horizontal position at the end of each cycle, producing no continuing translation.
3. **Joint references**: each frame computes foot-to-COM distance `d`; the law of cosines gives knee angle, while `atan2` and another cosine relation give hip angle before URDF conversion. Knee restriction is applied during generation. The generator adds no further low-pass filter to avoid extra in-place delay; reference velocity comes from position differences.
4. **Execution**: measured posture is held before a 2.5-second move to the first frame and subsequent two-step looping. Outer `q_cmd[k]=(1−α)q_cmd[k−1]+αq_ref[k]` smoothing and clipping still apply. Stop enters the ending segment at a cycle boundary; pause holds current output.
5. **Load detection**: positive `P=τω` accumulates step energy with a `70 J` threshold, after which PD ramps toward hard. This energy includes both device and patient mechanical work and is not a direct measure of voluntary patient work.

### Rehabilitation and Clinical Use

- In-place stepping can provide passive joint motion and gait-rhythm familiarization without forward travel, but suspension or reliable support is still required. “In place” does not remove fall risk.
- Start with low foot lift and a longer step period. Progress only after checking hip/knee range, weight-bearing tolerance, and foot clearance. Keep the target within the patient's comfortable range rather than using it for forced stretching.
- Enable torque protection and observe actual symmetry, pain, spasticity, and fatigue. `motion_ratio` and cadence describe task execution, not active participation or functional walking ability.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.0.0.
- `fourier-grx` v4.4.46 added the `rehab.step_frequency` reporting interface (unit: steps/min).
- `fourier-grx` v4.4.48 added the base height parameter interface.
- `fourier-grx` v4.4.54 added the missing read of the pause command `command_pause`, so pausing now takes effect.
- `fourier-grx` v4.4.65 added two feedforward task variants: position loop + velocity feedforward (TID 4125) and PD + velocity feedforward (TID 4127). The velocity feedforward is derived by numerically differentiating the actually-commanded target; the POSITION variant runs the actuator position loop (PID values in the robot parameter class), the PD variant maps kd × target velocity to an equivalent feedforward torque (note: the FSA v2 protocol has no velocity field, so the PD feedforward only takes effect on M4LT2).
- `fourier-grx` v4.4.68: the M4LT2 control rate was raised to 200 Hz (`control_period` 0.01 → 0.005) and the hard tier was retuned to kp `[1000,1000,1000,1000]` / kd `[60,60,60,60]` (hip ζ=0.63 unloaded / 0.52 loaded, knee ζ=1.12 / 1.04 overdamped); this task's total reference-trajectory delay compensation was reduced from 0.12 s to 0.06 s as well. Also fixed: the feedforward variants of this task (TID 4125 / 4127) never applied velocity feedforward, because the tasks are scheduled as `STANDALONE` by default while the hook only covered `function_component`.
- `fourier-grx` v4.4.69: to group the feedforward variants by control mode, this task's TID changed from **4112** to **4130**, and **4112 now refers to this task's PD + velocity-feedforward variant** (previously 4127); the POSITION variant shifts from 4125 to **4126**. ⚠️ Hosts must be updated — calling 4112 now selects the feedforward variant rather than this task.
- `fourier-grx` v4.4.70: the hard tier rises to kp `[1500×4]` / kd `[90×4]` (hip ζ=0.77 unloaded / 0.64 loaded, knee ζ=1.37 / 1.28), widening this task's load-detection PD ramp, which now tops out in about 8.7 s (T2) / 10.1 s (T1); the gait smoothing filter cutoff moves from 2.5 to 8.0 Hz (group delay about 15–17 ms) and the total delay compensation from 0.06 s to 0.03 s. With the stiffer hard tier, the tracking error needed to trip the 140 N·m protection falls from about 8° to about 5.3°. The doubled keyboard walking-speed default does not apply here — marching in place has no forward velocity parameter.
- `fourier-grx` v4.4.71: **the v4.4.70 tuning is reverted** — the hard tier returns to kp `[1000×4]` / kd `[60×4]`, the gait smoothing filter cutoff to 2.5 Hz, the total delay compensation to 0.06 s and the load-detection PD ramp floor to 0.01; the tracking error needed to reach the 140 N·m protection goes back to about 8°. Marching in place has no velocity parameter, so the keyboard walking-speed item does not apply here.
- `fourier-grx` v4.4.74: the `flag_robot_torque_protection` flag set by this task's torque protection is now **latched** — it is no longer cleared when the task exits and must be cleared by the host writing `clear_flag_robot_torque_protection`. The protection behaviour itself is unchanged: the task still exits immediately to the idle task (`TASK_IDLE`).
- `fourier-grx` v4.4.75: this task's software torque protection gains a **0.1 s debounce** — the limit must now be exceeded for 0.1 s in a row (5 cycles at 50 Hz, 10 at 100 Hz, 20 at 200 Hz) before protection trips, and a single cycle back at or below the limit resets the count. The action on tripping and the flag latching are unchanged. Protection used to act with zero delay, so a momentary torque spike could end the task by mistake.
- `fourier-grx` v4.4.76: the transition from the current posture into the gait start position is shortened from 5.0 s to **2.5 s**, so entering the gait is snappier (the parameter is defined in seconds, so the real duration is the same on 50 / 100 / 200 Hz models). The knee-restriction, assist and feedforward variants that share this control model are affected too.
