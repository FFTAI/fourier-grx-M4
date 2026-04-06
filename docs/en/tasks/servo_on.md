---
layout: default
title: Servo On
nav_order: 4.1
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Servo On

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

## Update Log

- Added in `fourier-grx` v1.0.0.
