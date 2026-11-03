---
layout: default
title: Stand Motion Control
nav_order: 4.10
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Stand Motion Control

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

## Update Log

- Added in `fourier-grx` v3.1.1.
- `fourier-grx` v4.4.72 switches this task from the baseline to the medium PD tier: M4LP1 uses kp `[350×4]` / kd `[25×4]`, and M4LT1 / M4LT2 use kp `[500×4]` / kd `[30×4]`. The 0.2 s pure-damping warm-up is unchanged, with the medium tier restored afterwards.
- `fourier-grx` v4.4.74: the `flag_robot_torque_protection` flag set by this task's torque protection is now **latched** — it is no longer cleared when the task exits and must be cleared by the host writing `clear_flag_robot_torque_protection`. The protection behaviour itself is unchanged: the task still exits immediately to the idle task (`TASK_IDLE`).
- `fourier-grx` v4.4.75: this task's software torque protection gains a **0.1 s debounce** — the limit must now be exceeded for 0.1 s in a row (5 cycles at 50 Hz, 10 at 100 Hz, 20 at 200 Hz) before protection trips, and a single cycle back at or below the limit resets the count. The action on tripping and the flag latching are unchanged. Protection used to act with zero delay, so a momentary torque spike could end the task by mistake.
- `fourier-grx` v4.4.76: this task's arrival check adds a **settle confirmation** on top of the interpolation time — once the target is pinned at the standing position it also needs 0.2 s in a row of «position change ≤ 0.01 rad within the window and |velocity| ≤ 0.05 rad/s on every joint» before the hold stage, with a 2.5 s timeout fallback that proceeds and logs a warning. Previously the switch happened the moment the timer expired, which discarded the support torque associated with the dynamic lag between measured and commanded position and showed up as a twitch. `motion_ratio` is capped at 99.9% and `flag_task_finish` is delayed until the robot is settled; setting `flag_settle_check` to False restores the time-only behaviour.
