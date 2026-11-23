---
layout: default
title: Clear Fault
parent: Task Description
nav_order: 4.04
has_toc: true
nav_exclude: true
---

# Clear Fault

* TOC
{:toc}

## Task Info

Task ID (TID): **34**

Task Description:

- Clears the fault state of the actuators. If the corresponding error code can be cleared by a reboot, the robot can resume operation; if the error code cannot be cleared by a reboot, the hardware fault must be diagnosed and repaired.

Task Parameters:

This task has no configurable parameters.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping | Notes |
|-----------|------------------|-------|
| Task start flag | `task.flag_task_start` | SET during the clearing process |
| Task finish flag | `task.flag_task_finish` | SET when the clear operation completes (confirm the result via `grx.robot_error_codes`) |

Command interface:

This task requires no additional command parameters; sending TID=34 triggers it. After clearing, check whether `grx.robot_error_codes` is an empty list to confirm the fault has been cleared. If error codes persist, the hardware fault must be diagnosed.

## Principle Explanation

### Algorithm Operation

This task asks the actuators to clear latched fault states and finishes according to their feedback. It resets fault flags only; it does not repair overcurrent, overtemperature, communication loss, mechanical obstruction, or other root causes. Faults that cannot be cleared remain visible in `grx.robot_error_codes`.

### Rehabilitation and Clinical Use

- Stop training and protect the patient before clearing a fault. Record the fault code, active task, posture, and symptoms. Clear only after the cause is understood and safe recovery has been confirmed.
- Successful clearing does not mean the patient can immediately resume the same intensity. Recheck straps, joint clearance, zero references, and device status, then restart with a low-risk preparation action.
- For recurrent or unexplained faults, or faults accompanied by pain or mechanical abnormalities, end the session and arrange engineering inspection. Do not force operation by clearing repeatedly.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Provided since early `fourier-grx` versions (already present in v2.0.5, the earliest release in this repository’s public history).
