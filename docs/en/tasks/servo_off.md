---
layout: default
title: Servo Off
nav_order: 4.2
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Servo Off

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

## Update Log

- Added in `fourier-grx` v1.0.0.
