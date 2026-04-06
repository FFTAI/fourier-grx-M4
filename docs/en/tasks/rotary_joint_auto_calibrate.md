---
layout: default
title: Auto Calibrate (Rotary Joint)
nav_order: 4.23
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Auto Calibrate (Rotary Joint)

## Task Info

Task ID (TID): **4120**

Task Description:

- Executes an automatic zero-point calibration sequence for the rotary joints (hip and knee joints), with no manual adjustment required.
- Calibration proceeds through three sequential steps:
  1. **Border detection and return** (TID 4104): Drives each joint to its mechanical limit, then automatically retracts to a safe position upon detecting the boundary.
  2. **Joint Servo Off**: Disables all actuators so the joints drop naturally to a resting position under gravity.
  3. **Set Home** (TID 4105): Samples joint position readings for approximately 1 second (50 control cycles) and takes the average, setting that average as the zero point (application-layer 0 rad reference position).
- It is recommended to run this task before starting any other motion task whenever the robot is powered on again or joint zero points are lost.

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

> `flag_task_start` is set while the border detection phase (step 1) is running; `flag_task_finish` is set after zero-point setting is complete (end of step 3).

Command Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| | |

## Internal Sub-Task Description

| Step | TID | Task Name | Description |
|------|-----|-----------|-------------|
| 1 | 4104 | Border detection and return | Drives hip joints toward MIN and knee joints toward MAX; retracts along the same path after detecting contact. |
| 2 | — | Joint Servo Off | Executes ServoOff so joints drop naturally under gravity. |
| 3 | 4105 | Set Home (software layer) | Continuously samples 50 cycles and takes the average; calls `set_home_position()` to write the zero point. |

## Notes and Common Issues

### Prerequisites

1. All actuators are Servo On (TID=35).
2. The prismatic joints (leg length) have already been calibrated (TID=4210).
3. The robot is suspended (both feet off the ground), or the rotary joint range of motion is confirmed to be unobstructed.

### Timeout Handling

- The border detection step (step 1) has a maximum timeout of approximately **60 seconds**. If the mechanical limit is not detected within the timeout, the task will terminate and set `flag_task_finish`, but the zero point will not be written.
- After a timeout:
  1. Check whether actuators have alarms (`grx.robot_error_codes`).
  2. Execute Clear Fault (TID=34) to clear the alarms.
  3. Servo On again (TID=35) and retry.

### Calibration Failure Indicators

- Successful calibration: after `flag_task_finish` is set, each rotary joint position should be close to 0 rad (error < 0.1 rad).
- Signs of calibration failure: joint positions still show significant offset, or obvious asymmetry appears during motion tasks.

### Usage Restrictions

- Running this task after each power-on is **optional** (rotary joint zero points are retained after power-off).
- Prismatic joint zero points **must** be recalibrated every power-on (TID=4210).
- This task cannot be triggered while a motion task is running — exit the current task before performing calibration.

## Update Log

- Added in `fourier-grx` v4.2.0.
