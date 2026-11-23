---
layout: default
title: Auto Calibrate (Rotary Joint)
parent: Task Description
nav_order: 4.07
has_toc: true
nav_exclude: true
---

# Auto Calibrate (Rotary Joint)

* TOC
{:toc}

## Task Info

Task ID (TID): **4120**

Task Description:

- Executes an automatic zero-point calibration sequence for the rotary joints (hip and knee joints), with no manual adjustment required.
- Calibration proceeds through three sequential steps:
  1. **Border detection and return** (TID 4104): Drives each joint to its mechanical limit, then automatically retracts to a safe position upon detecting the boundary.
  2. **Joint Servo Off**: Disables all actuators so the joints drop naturally to a resting position under gravity.
  3. **Set Home** (TID 4105): Samples joint position readings for approximately 1 second (cycle count derived from the control period) and takes the average, setting that average as the zero point (application-layer 0 rad reference position).
- It is recommended to run this task before starting any other motion task whenever the robot is powered on again or joint zero points are lost.

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

> `flag_task_start` is set while the border detection phase (step 1) is running; `flag_task_finish` is set after zero-point setting is complete (end of step 3).

Command Interface:

This task requires no command parameters. Send the corresponding TID to trigger it.

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

## Principle Explanation

### Algorithm Operation

Automatic calibration chains three subtasks: **rate-limited boundary detection → return to a safe position → stationary sampling and software zeroing**.

1. **Boundary detection**: starting from measured positions, each command changes by at most `0.004 rad` per control cycle as hips move toward MIN and knees toward MAX. Each joint independently requires `|τ| ≥ threshold` and `|ω| ≤ 0.01 rad/s` for 0.2 s before freezing its target; joints need not all reach their limits in the same cycle. A timeout prevents an indefinite sweep.
2. **Return and disable**: after detection, joints return by fixed angular offsets with a position tolerance. `SERVO_OFF` then lets them settle under gravity and mechanical constraints. The detected boundary is a machine reference, never a patient range-of-motion measurement.
3. **Average and set zero**: approximately one second of samples produces `q̄ = (1/N) Σ q_i`, which is written to application-layer `home_position`; application directions and offsets are restored. The transformed encoder coordinate then corresponds to the new `0 rad`.
4. **Prevent target jumps**: targets are synchronized with measured positions in the new coordinates so the next task cannot inherit sweep-era targets. An unfinished calibration can roll back the saved zero and direction configuration.

The algorithm estimates a device coordinate reference. It recognizes neither patient anatomy nor clinical range restrictions, and it does not alter the mechanical boundary to accommodate them.

### Rehabilitation and Clinical Use

- Calibration actively drives joints to mechanical limits and includes an unpowered settling phase. Perform it only with the patient off the device, both feet clear of the ground, and the motion space unobstructed. Never use it to measure or forcibly improve a patient's range of motion.
- After calibration, check the zero posture and left/right symmetry unloaded before fitting and standing preparation. For sweep timeout, excessive position error, or abnormal resistance, stop and follow the fault procedure rather than repeating sweeps to force completion.
- Standard mechanical calibration is still required for patients with contracture, bony block, or postoperative restrictions. Clinical adaptation belongs in the approved restriction and training parameters.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.4.0.
- `fourier-grx` v4.4.59 fixes two regressions affecting this task's sweep: since v4.4.49 the position-protection bounds were initialised as "position at activation ± 0.25 rad", so a sweep whose joint travel exceeds that margin was falsely flagged as out of range and the robot servoed off mid-way; and the task-layer target clamp (also v4.4.49) neutralised the beyond-limit overshoot commands, so the joint stopped at the software limit instead of pressing against the mechanical hard stop. From this version on, this task (and the prismatic calibration sweeps) initialise the protection bounds as hardware limits ± margin and regain their overshoot commands. The internal blaze build shipped on 2026-10-20 — see [Fourier-GRX firmware · 4.4.59](/fourier-grx-M4/docs/en/release/fourier-grx#4459).
