---
layout: default
title: Auto Calibrate (Prismatic Joint)
nav_order: 4.21
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Auto Calibrate (Prismatic Joint / Leg-Length Adjustment Joint)

## Task Info

Task ID (TID): **4210**

Task Description:

- Launches the automatic calibration procedure for the leg-length adjustment joints.
- Each time the robot is powered on, the leg-length information is lost and must be re-calibrated before the leg-length adjustment function can be used normally.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
|           |      |         |       |             |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |

Command interface:

| Parameter | Interface Mapping |
|-----------|------------------|
|           |                   |

## Update Log

- Added in `fourier-grx` v4.1.22.
