---
layout: default
title: Servo Off
parent: Task Description
nav_order: 4.02
has_toc: true
nav_exclude: true
---

# Servo Off

* TOC
{:toc}

## Task Info

Task ID (TID): **36**

Task Description:

- Disables all actuators; motors stop outputting torque.

Task Parameters:

This task has no configurable parameters.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping | Description |
|-----------|------------------|-------------|
| Task start flag | `task.flag_task_start` | SET while the Servo Off process is in progress. |
| Task finish flag | `task.flag_task_finish` | SET after all actuators have been disabled. |

Command Interface:

This task requires no additional command parameters. Send TID=36 to trigger it. After the actuators are disabled the robot will go limp — ensure mechanical support or safety measures are in place.

## Principle Explanation

### Algorithm Operation

This task sends a disable command to all actuators rather than planning joint motion. Torque output stops and the task state is updated. The joints are then no longer actively held by the motors and can move under gravity or external force; there is no controlled lowering, posture-holding, or damping algorithm in this task.

### Rehabilitation and Clinical Use

- Execute only after the patient and device are reliably supported by suspension, a support frame, or staff. In particular, disabling must not be used as a way to hold standing or end a session with controlled lowering.
- At the end of treatment, stop the gait task and place the patient in a stable, transferable posture before disabling. Remove straps or transfer the patient only afterwards, following the local procedure.
- Use the device's emergency-stop procedure for an emergency. If training is to resume after disabling, recheck posture, zero references, and fault status instead of directly continuing the previous gait cycle.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Provided since early `fourier-grx` versions (already present in v2.0.5, the earliest release in this repository’s public history).
