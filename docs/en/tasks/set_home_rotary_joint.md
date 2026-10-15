---
layout: default
title: Set Home (Rotary Joint)
nav_order: 4.6
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Set Home (Rotary Joint)

## Task Info

Task ID (TID): **4103**

Task Description:

- Sets the mechanical zero point of the rotary joint actuators to their current position. Typically used to calibrate the actuator position.
- The task runs the following sequence automatically, takes about 11 seconds in total, and neither requires nor accepts command parameters:

| Step | Action | Description |
|----|----|----|
| 1 | Actuator power off (`SERVO_OFF`) | Torque output released; joints can be moved freely |
| 2 | Issue an absolute-encoder zeroing (`ABSOLUTE_ZERO`) | The actuator records the current position as its absolute zero |
| 3 | Hold for 1 second | Waits for the zero-point write to complete |
| 4 | Actuator reboot (`SERVO_REBOOT`) | The actuator is rebooted after the zeroing |
| 5 | Wait 10 seconds | Communication packet-loss warnings may appear during the reboot; this is normal |

> ⚠️ **Note**:
>
> - This task runs `SERVO_OFF` → `ABSOLUTE_ZERO` → `SERVO_REBOOT`; the joints produce no torque throughout, so keep the robot suspended or safely supported.
> - Brief communication packet-loss warnings may appear during the reboot; this is normal.
> - Difference from Manual Calibrate (Rotary Joint, TID=4121): this task zeroes the **actuator** absolute encoder and reboots the actuator, whereas 4121 only records a **software application-layer** zero offset without powering off or rebooting.

Task Parameters:

This task has no configurable parameters.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |

Command Interface:

This task requires no command parameters. Send the corresponding TID to trigger it.

## Update Log

- Added in `fourier-grx` v4.1.19.
