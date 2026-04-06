---
layout: default
title: Servo Reboot
nav_order: 4.3
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Servo Reboot

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

## Update Log

- Added in `fourier-grx` v1.0.0.
