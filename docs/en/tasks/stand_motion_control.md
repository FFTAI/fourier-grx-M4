---
layout: default
title: Stand Motion Control
nav_order: 4.6
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
- Supports torque protection: when the torque of any joint exceeds the configured threshold, the task will pause and set an overload flag.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. When enabled, if the torque of any joint exceeds the "torque protection limit", the task will pause and set the overload flag; the task must be restarted to continue. |
| Torque protection limit | `float` | — | [0.0, 200.0] | The maximum allowable output torque for any joint during the standing process, in Nm. Only effective when torque protection is enabled; disabled by default. |

> **Task Description**:
>
> The robot interpolates linearly from the current joint positions to the standing target posture (all joint angles at 0 rad) over approximately 5 seconds, then holds the standing posture until another task command is received.

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

- Added in `fourier-grx` v1.0.0.
