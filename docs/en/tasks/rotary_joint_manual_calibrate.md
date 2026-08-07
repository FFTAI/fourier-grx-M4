---
layout: default
title: Manual Calibrate (Rotary Joint)
nav_order: 4.8
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Manual Calibrate (Rotary Joint)

## Task Info

Task ID (TID): **4121**

Task Description:

- Used to trigger the software-layer zero-point write after the user has **manually positioned the rotary joints at the desired zero posture**.
- Calibration proceeds through two sequential steps:
  1. **Joint Servo Off**: Executes ServoOff so the user can freely move the joints to the target posture and hold them still.
  2. **Set Home** (TID 4105): Samples joint position readings for approximately 1 second (50 control cycles) and takes the average, setting that average as the zero point (application-layer 0 rad reference position); afterwards, the joint target positions are automatically reset to the measured positions in the new coordinate frame, preventing a target-jump shock when the next task is enabled.
- Difference from Auto Calibrate (TID 4120):

  | | Manual Calibrate (TID 4121) | Auto Calibrate (TID 4120) |
  |---|---|---|
  | Zero-point determination | User manually positions the joints | The robot automatically drives to the mechanical limits and retracts |
  | Applicable scenarios | Quick on-site calibration, known zero posture | Standard power-on calibration, first-time use |
  | Suspension required | No (depends on the target zero posture) | Yes (both feet off the ground) |

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

> `flag_task_start` is set while the joint Servo Off phase (step 1) is running; `flag_task_finish` is set after zero-point setting is complete (end of step 2).

Command Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| | |

## Internal Sub-Task Description

| Step | TID | Task Name | Description |
|------|-----|-----------|-------------|
| 1 | — | Joint Servo Off | Executes ServoOff; the user manually positions the joints at the target zero posture. |
| 2 | 4105 | Set Home (software layer) | Continuously samples 50 cycles and takes the average; calls `set_home_position()` to write the zero point; resets the joint target positions afterwards. |

## Notes and Common Issues

### Prerequisites

1. All actuators are Servo On (TID=35).
2. The user has confirmed the desired zero posture of the rotary joints (after the task is triggered, ServoOff is executed and the joints are then moved manually).

### Operating Procedure

1. Trigger TID 4121 → the actuators power off automatically.
2. Manually position the rotary joints at the target zero posture and hold them still.
3. Wait approximately 1 second; the program automatically completes sampling and writes the zero point.
4. Calibration is complete once `flag_task_finish` is set; the task automatically switches back to IDLE.

### Calibration Failure Indicators

- Successful calibration: after `flag_task_finish` is set, each rotary joint's application-layer position should be close to 0 rad (error < 0.1 rad).
- If a joint shakes during sampling, re-trigger TID 4121 to recalibrate.

### Usage Restrictions

- Prismatic joint zero points **must** be recalibrated every power-on (TID=4210) and are not affected by this task.
- This task cannot be triggered while a motion task is running — exit the current task before performing calibration.

## Update Log

- Added in `fourier-grx` v4.4.22.
