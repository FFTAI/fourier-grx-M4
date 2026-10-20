---
layout: default
title: Calibrate Home (Prismatic Joint)
nav_order: 4.9
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Auto Calibrate (Prismatic Joint / Leg-Length Adjustment Joint)

## Task Info

Task ID (TID): **4210**

Task Description:

- Launches the automatic calibration procedure for the leg-length adjustment joints: the prismatic joints are driven 0.2 m along the positive actuator axis (covering the whole adjustment travel) until they hit the mechanical limit, which is then recorded as the zero reference of the software coordinate frame (from then on a leg-length command of 0.0 corresponds to this limit, and larger values move toward the other end).
- Each time the robot is powered on, the leg-length information is lost and must be re-calibrated before the leg-length adjustment function can be used normally.
- When calibration completes, the task switches back to the idle task (`TASK_IDLE`) and syncs each joint's target position to the new measured position, preventing a target jump when the next task enables servo.

> ⚠️ **Note**: during calibration the prismatic joints push against their mechanical limits the whole time. Make sure both legs are free of external obstruction and the robot is suspended or stably supported, and never stand beneath it.
>
> Directions here are described in the actuator coordinate frame: because the M4L leg-length motor axis is opposite to the leg-length command direction (see the `× -1.0` convention of TID 4206), the positive actuator direction corresponds to decreasing leg length.

## Internal Sub-task Steps

| Step | TID | Task name | Description |
|----|-----|--------|----|
| 1 | 4204 | Move to maximum position (internal step) | Drives 0.2 m along the positive actuator axis over a 120 s S-curve profile and stops once the limit is detected |
| 2 | — | Actuator power off | Reuses `TaskRobotRealServoOff` to prepare for the software zeroing |
| 3 | 4203 | Set prismatic joint home | Writes the current measured position as the software-layer zero point |

Step 1 uses two arrival criteria — either one is enough:

| Criterion | Trigger condition |
|----|---------|
| Torque + velocity | Measured torque ≥ 6 Nm and velocity ≤ 0.001 m/s, held for 0.2 s |
| Velocity only | `motion_ratio` ≥ 0.20 and velocity ≤ 0.001 m/s, held for 25 s |

The velocity-only criterion covers contact cases where torque does not build up properly; the 0.20 lower bound exists because the S-curve reference velocity is itself below the velocity threshold at the very start of the travel, which would otherwise cause false detections. In the tail of the travel (r > 0.8295) the reference velocity likewise drops below the threshold and stays there for about 20.5 s, so since `fourier-grx` v4.4.58 the hold time is 25 s — longer than that tail window, which is what rules out premature "arrived" calls before the joint touches the limit. On v4.4.53 – v4.4.57 the hold was 5 s, which risked a false arrival call about 3.5 mm before the hard stop.

Task Parameters:

This task has no configurable parameters.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |

Command interface:

This task requires no command parameters. Send the corresponding TID to trigger it. The calibration cannot be interrupted or tuned from the panel parameters.

## Update Log

- Added in `fourier-grx` v4.1.17.
- `fourier-grx` v4.4.53 added a velocity-only arrival criterion that does not depend on torque (`motion_ratio` ≥ 0.20 with velocity ≤ 0.001 m/s held for 5 s), so arrival is still detected when contact torque does not build up.
- `fourier-grx` v4.4.58 raises the velocity-only hold time from 5 s to 25 s: 5 s is shorter than the ~20.5 s naturally slow tail of the profile, which risked declaring arrival before the joint touched the limit and zeroing about 3.5 mm short. The stable release shipped on 2026-10-20 — see [Fourier-GRX firmware · 4.4.58](/fourier-grx-M4/docs/en/release/fourier-grx#4458) for downloads and details.
