---
layout: default
title: Stand Motion Control
parent: Task Description
nav_order: 4.10
has_toc: true
nav_exclude: true
---

# Stand Motion Control

* TOC
{:toc}

## Task Info

Task ID (TID): **4020**

Task Description:

- The robot slowly moves all joints back to the standing posture.
- Typically used as a preparatory action before a motion task, or to restore the initial posture after motion ends.
- Supports torque protection: when the torque of any joint exceeds the configured threshold continuously for at least 0.1 s (since v4.4.75), the task exits immediately and switches to the idle task (`TASK_IDLE`), and sets the torque-protection flag; the task must be re-issued to continue.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. When enabled, if the torque of any joint exceeds the "torque protection limit" continuously for at least 0.1 s (since v4.4.75), the task exits immediately and switches to the idle task (`TASK_IDLE`), and sets the torque-protection flag; the task must be re-issued to continue. |
| Torque protection limit | `float` | None | [0.0, 200.0] | The maximum allowable output torque for any joint during the standing process, in Nm. Only effective when torque protection is enabled; disabled by default. |

> **Task Description**:
>
> After a 0.2 s warm-up in pure-damping mode (kp = 0), the robot interpolates from the current joint positions to the standing target posture (all four rotary joints at 0 rad) over approximately 5 seconds, then a **settle check** confirms the mechanics have actually stopped (position change below 0.01 rad and every joint below 0.05 rad/s for 0.2 s in a row, with a 2.5 s timeout fallback) before the hold stage. Since `fourier-grx` v4.4.76 the reported `motion_ratio` stays capped at 99.9% until the robot is settled, and the task-finished flag is delayed to match. The robot then holds the standing posture until another task command is received.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |

Command Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

## Principle Explanation

### Algorithm Operation

Standing control is a staged **damping takeover → timed interpolation → feedback settling check → stiffness-ramped hold**, not an immediate write of zero to all four joints:

1. **Damping warmup**: for the first 0.2 s, `Kp=0` and the position target follows `q_ref=q_meas`, leaving only `Kd` damping. This avoids a position jump when the previous task's target differs from the current posture.
2. **Posture interpolation**: measured `q0` is latched again at the end of warmup, followed by `r=min(t/5,1)` and `q_ref=q0+(q_stand−q0)r` for about five seconds. Normal standing uses `q_stand=[0,0,0,0]`, tracked by medium-tier PD feedback.
3. **Mechanical settling**: completed interpolation means only that the reference arrived. For 0.2 consecutive seconds, the algorithm requires `max|q_meas−q_window| ≤ 0.01 rad` and `max|ω_meas| ≤ 0.05 rad/s`. It checks stillness within a window rather than zero target error because loaded PD can retain steady-state error. A 2.5-second timeout permits continuation with a warning.
4. **Holding-stiffness ramp**: while holding the stance, Kp/Kd move from medium to rock over one second using `K=K_start+(K_rock−K_start)r`. Only then do `motion_ratio` and the finish flag reach completion.
5. **Independent protection**: the task layer separately counts measured torque above the limit for 0.1 s, exits to `TASK_IDLE`, and latches the protection flag. This branch is outside posture interpolation and does not automatically resume standing.

### Rehabilitation and Clinical Use

- Use this task to return to a neutral stance under supported conditions before or after training. For first use or unknown tolerance, provide suspension/fall protection and close therapist supervision; enable torque protection with an individualized limit.
- The task follows a preset stance. It detects neither the patient's intention to stand nor dynamic balance. `motion_ratio=100%` therefore does not establish safe standing or weight-bearing capacity.
- Zero radians is a device reference, not a suitable posture for every patient. For knee extension restriction, pain, spasticity, or marked alignment abnormalities, assess first and select the appropriate restricted task or reconsider suitability instead of forcing full extension.
- The holding phase is relatively stiff. Stop and reassess for pain, resistance, abnormal torque, or posture deviation rather than letting the patient continue to oppose the device.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v3.1.1.
- `fourier-grx` v4.4.72 switches this task from the baseline to the medium PD tier: M4LP1 uses kp `[350×4]` / kd `[25×4]`, and M4LT1 / M4LT2 use kp `[500×4]` / kd `[30×4]`. The 0.2 s pure-damping warm-up is unchanged, with the medium tier restored afterwards.
- `fourier-grx` v4.4.74: the `flag_robot_torque_protection` flag set by this task's torque protection is now **latched** — it is no longer cleared when the task exits and must be cleared by the host writing `clear_flag_robot_torque_protection`. The protection behaviour itself is unchanged: the task still exits immediately to the idle task (`TASK_IDLE`).
- `fourier-grx` v4.4.75: this task's software torque protection gains a **0.1 s debounce** — the limit must now be exceeded for 0.1 s in a row (5 cycles at 50 Hz, 10 at 100 Hz, 20 at 200 Hz) before protection trips, and a single cycle back at or below the limit resets the count. The action on tripping and the flag latching are unchanged. Protection used to act with zero delay, so a momentary torque spike could end the task by mistake.
- `fourier-grx` v4.4.76: this task's arrival check adds a **settle confirmation** on top of the interpolation time — once the target is pinned at the standing position it also needs 0.2 s in a row of «position change ≤ 0.01 rad within the window and |velocity| ≤ 0.05 rad/s on every joint» before the hold stage, with a 2.5 s timeout fallback that proceeds and logs a warning. Previously the switch happened the moment the timer expired, which discarded the support torque associated with the dynamic lag between measured and commanded position and showed up as a twitch. `motion_ratio` is capped at 99.9% and `flag_task_finish` is delayed until the robot is settled; setting `flag_settle_check` to False restores the time-only behaviour.
- `fourier-grx` v4.4.85: after settling, the robot holds the standing position while Kp/Kd ramp linearly from medium to rock over **1.0 s**. On every model, rock is kp `[5000,2500,5000,2500]` / kd `[120,60,120,60]`. `motion_ratio` remains capped at 99.9% during the ramp; 100% and task completion are reported only after rock is reached.
