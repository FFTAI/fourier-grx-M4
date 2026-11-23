---
layout: default
title: Servo On
parent: Task Description
nav_order: 4.01
has_toc: true
nav_exclude: true
---

# Servo On

* TOC
{:toc}

## Task Info

Task ID (TID): **35**

Task Description:

- Enables all actuators; motors begin outputting torque.

Task Parameters:

This task has no configurable parameters.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping | Description |
|-----------|------------------|-------------|
| Task start flag | `task.flag_task_start` | SET while the Servo On process is in progress. |
| Task finish flag | `task.flag_task_finish` | SET after all actuators have been enabled. |

Command Interface:

This task requires no additional command parameters. Send TID=35 to trigger it.

## Principle Explanation

### Algorithm Operation

This task is an **actuator control-mode state machine**, with no trajectory generation or closed-loop posture control:

1. **Enable command**: on `STAGE_INIT`, the workspace switches to `ACTUATOR_SPACE`. Every actuator receives `SERVO_ON`, while position, velocity, effort, and current targets are cleared so the enable command is not combined with stale motion targets.
2. **End the transient command**: during `STAGE_START` / `STAGE_RUN`, control modes return to `NONE` and the actuators retain their enabled state. The task computes no new output from joint errors.
3. **Exit**: after `STAGE_FINISH`, the task switches to `TASK_IDLE`; a subsequent standing or gait task must supply the actual position targets and PD gains.

“Enable complete” therefore means that this control-mode sequence has executed. It does not establish a particular robot posture or stable patient weight-bearing.

### Rehabilitation and Clinical Use

- This is a preparation or shutdown step, not a rehabilitation exercise in itself. Before enabling, complete the patient assessment and check straps and joint alignment. Stabilize the device with suspension, a support frame, or manual guarding to prevent sudden movement as torque is established.
- Enter a standing or gait task only after this task finishes. For abnormal noise, pain, visible misalignment, or an alarm during enabling, stop using the facility's emergency procedure rather than repeatedly retrying.
- The finish flag only confirms actuator enablement; it does not establish that the patient can bear weight or begin training.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Provided since early `fourier-grx` versions (already present in v2.0.5, the earliest release in this repository’s public history).
