---
layout: default
title: Set Home (Rotary Joint)
nav_order: 4.20
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Set Home (Rotary Joint)

## Task Info

Task ID (TID): **4103**

Task Description:

- Sets the current actuator angle as the zero-point position. Typically used to calibrate the actuator position.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| | | | | |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |

Command Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| | |

## Update Log

- Added in `fourier-grx` v4.0.0.
