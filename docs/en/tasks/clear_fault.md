---
layout: default
title: Clear Fault
nav_order: 4.4
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Clear Fault

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

## Update Log

- Added in `fourier-grx` v1.0.0.
