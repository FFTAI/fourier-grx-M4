---
layout: default
title: Servo Reboot
parent: Task Description
nav_order: 4.03
has_toc: true
nav_exclude: true
---

# Servo Reboot

* TOC
{:toc}

## Task Info

Task ID (TID): **41**

Task Description:

- Reboots all actuators, reloading their configuration and state.
- Note: after rebooting, all actuator states and configuration parameters will be reset to their default values.

Task Parameters:

This task has no configurable parameters.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping | Description |
|-----------|------------------|-------------|
| Task start flag | `task.flag_task_start` | SET while the reboot process is in progress. |
| Task finish flag | `task.flag_task_finish` | SET after all actuators have finished rebooting (may take several seconds). |

Command Interface:

This task requires no additional command parameters. Send TID=41 to trigger it. After the reboot is complete, actuators will return to the Servo Off state — send Servo On (TID=35) again to enable them.

## Principle Explanation

### Algorithm Operation

This task reboots the actuators through a complete state-reset sequence:

1. In `ACTUATOR_SPACE`, every actuator receives `SERVO_REBOOT` and all motion targets are cleared. The actuators then reload their internal configuration and state.
2. The task clears buffered position-loop, velocity-loop, effort-loop, and PD `Kp/Kd` targets so gains cached before reboot are not reused.
3. Control modes return to `NONE` and the task switches to `TASK_IDLE`. The actuators remain disabled until a later task enables them and writes new control parameters.

There is no trajectory interpolation and no training-state save/resume. Rebooting resets the device and command state; it does not remove the physical cause of a mechanical obstruction, overtemperature condition, or communication failure.

### Rehabilitation and Clinical Use

- Use rebooting only when actuator state explicitly needs resetting, not as a routine pause or a general fault-retry button during treatment. Preferably remove the patient from the device; otherwise provide full mechanical support and manual protection.
- After rebooting, recheck fault codes, joint zero references, leg-length calibration, and current posture before enabling and selecting a task. Do not continue directly from the previous gait cycle.
- If the same alarm or abnormality returns, stop clinical use and arrange engineering investigation rather than using repeated reboots in place of diagnosis.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Provided since early `fourier-grx` versions (already present in v2.0.5, the earliest release in this repository’s public history).
