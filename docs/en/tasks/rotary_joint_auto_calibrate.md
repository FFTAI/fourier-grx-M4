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

| Task | Task ID (TID) | Control |
|---|---|---|
| Auto Calibrate (Rotary Joint) | **4120** | Calibration |

Task Description:

- Executes an automatic zero-point calibration sequence for the rotary joints (hip and knee joints), with no manual adjustment required.
- Calibration proceeds through three sequential steps:
  1. **Border detection and return** (TID 4104): Drives each joint to its mechanical limit, then automatically retracts to a safe position upon detecting the boundary.
  2. **Joint Servo Off**: Disables all actuators so the joints drop naturally to a resting position under gravity.
  3. **Set Home** (TID 4105): Samples joint position readings for approximately 1 second (cycle count derived from the control period) and takes the average, setting that average as the zero point (application-layer 0 rad reference position). **Runs only when the first two steps succeed and all sampled/written values are finite.**
- If border detection/return fails (or a measurement/command is non-finite during that phase), the zero point is not written and the task finish flag is not set; AutoCalibrate performs ServoOff and returns to IDLE.
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

> `flag_task_start` is set as a start event when the border detection phase begins; `flag_task_finish` is set **only after zero-point setting succeeds (end of step 3)**.
> On failure (border/return timeout, non-finite measurement/command, or SetHome non-finite sampling), `flag_task_finish` stays CLEAR; AutoCalibrate performs ServoOff and returns to IDLE without writing a home point successfully.

Command Interface:

This task requires no command parameters. Send the corresponding TID to trigger it.

## Internal Sub-Task Description

| Step | TID | Task Name | Description |
|------|-----|-----------|-------------|
| 1 | 4104 | Border detection and return | Drives hip joints toward MIN and knee joints toward MAX; retracts after detecting contact. A detection timeout or non-finite value enters failure and skips step 3. |
| 2 | — | Joint Servo Off | Executed on normal success and also after a failure abort as a safe shutdown; joints drop naturally under gravity. |
| 3 | 4105 | Set Home (software layer) | Executed only after steps 1 and 2 succeed: samples for approximately 1 second (50/100/200 cycles at 50/100/200 Hz), checks every measured sample is finite, validates the average before writing, and calls `set_home_position()` to write the zero point; non-finite values fail without commit. |

## Notes and Common Issues

### Prerequisites

1. All actuators are Servo On (TID=35).
2. The prismatic joints (leg length) have already been calibrated (TID=4210).
3. The robot is suspended (both feet off the ground), or the rotary joint range of motion is confirmed to be unobstructed.

### Failure and Timeout Handling

- The following conditions are **calibration failures**; the zero point is not written and `flag_task_finish` is not set:
  1. Phase-1 border detection does not find all mechanical limits within **60 seconds**;
  2. Phase-3 return does not reach its target, or the measured position does not settle within tolerance, within **60 seconds**;
  3. Measured position/velocity/effort or a joint command is NaN/inf during the calibration motion (border detection/return), or a rotary joint measured position is NaN/inf before entering SetHome;
  4. Any SetHome sampling cycle (PROCESS_02) has a non-finite measured position, the average is non-finite before writing, or SetHome reaches FINISH without a commit.
- Failure is not an early completion: no zero point is written, no commit is made, and the finish flag is not set:
  - **Auto Calibrate (TID 4120), border/return failure**: stops writing new PD targets; ServoOff then takes over. `flag_task_finish` stays CLEAR, finite measured positions are synchronized to the joint targets (non-finite values are skipped), and the task returns to IDLE. After ServoOff and before SetHome it checks the rotary joint measurements again; NaN/inf also aborts to IDLE without writing the zero point. The log shows algorithm `calibration failed: ...` plus composite `calibration aborted - ...`.
  - **Auto Calibrate (TID 4120), SetHome failure**: SetHome enters failure, does not accumulate non-finite samples, does not write home, and does not commit. AutoCalibrate does not print the success message; it logs `calibration aborted - SetHome failed: ...` and returns directly to TASK_IDLE (ServoOff is already active). Any provisional, uncommitted home write is rolled back on deactivation; `flag_task_finish` stays CLEAR.
  - **Standalone Border detection and return (TID 4104)**: stops writing new PD targets and requests ServoOff (TID=36), which then returns to IDLE; this task never writes the zero point, and `flag_task_finish` stays CLEAR. Its failure log is `calibration failed: ...` plus `border/return failed (...)`; it **does not** emit AutoCalibrate's `calibration aborted`. The normal success path is unchanged.
  - **SetHome used standalone or by another composite**: a failure keeps `STAGE_ERROR` / `flag_failure`, does not commit, does not set `robot.flag_calibration`, and does not set `flag_task_finish`; deactivation rolls back any uncommitted provisional home write. The log keyword is `home calibration failed: ...`.
- Re-sending the same task no longer resets component stages in the FSM; AutoCalibrate still explicitly sets the corresponding stage to `INIT` at every Border→ServoOff (normal/failure) and ServoOff→SetHome transition, and SetHome performs a full sample/failure reset at STAGE_START. Repeats/re-entry therefore cannot skip SERVO_OFF or reuse samples from a previous run; these resets happen only at transitions/START, not every cycle.
- After a failure:
  1. Check whether actuators have alarms (`grx.robot_error_codes`).
  2. Execute Clear Fault (TID=34) to clear the alarms.
  3. Servo On again (TID=35) and retry.
- The robot may already be back in IDLE after a failure; **IDLE with `flag_task_finish` not set means a failed shutdown, not a successful calibration**.
- Reactivating the task from IDLE resets the failure state and SetHome sample cache, and starts calibration again from INIT.

### Calibration Failure Indicators

- Successful calibration: `flag_task_finish` is set, step 3 SetHome has committed, and `robot.flag_calibration` is set; each rotary joint position should be close to 0 rad (error < 0.1 rad).
- Calibration failure: `flag_task_finish` stays CLEAR and the log keywords are `calibration failed` / `calibration aborted` / `home calibration failed`; the robot returns to IDLE after ServoOff and the zero point is not written. Joint positions may still show a significant offset, or obvious asymmetry may appear during subsequent motion tasks.

### Usage Restrictions

- Running this task after each power-on is **optional** (rotary joint zero points are retained after power-off).
- Prismatic joint zero points **must** be recalibrated every power-on (TID=4210).
- This task cannot be triggered while a motion task is running — exit the current task before performing calibration.

## Principle Explanation

### Algorithm Operation

Automatic calibration chains three subtasks: **rate-limited boundary detection → return to a safe position → stationary sampling and software zeroing**.

1. **Boundary detection**: starting from measured positions, each command changes by at most `0.004 rad` per control cycle as hips move toward MIN and knees toward MAX. Each joint independently requires `|τ| ≥ threshold` and `|ω| ≤ 0.01 rad/s` for 0.2 s before freezing its target; joints need not all reach their limits in the same cycle. If not all boundaries are detected within 60 s, or a measurement/command is non-finite, the task enters failure instead of forcing a return.
2. **Return and disable**: after a normal detection, joints return by fixed angular offsets with a position tolerance. `SERVO_OFF` then lets them settle under gravity and mechanical constraints. A return that does not complete within 60 s also enters failure. The detected boundary is a machine reference, never a patient range-of-motion measurement.
3. **Average and set zero**: after successful detection and return, SetHome checks every measured sample is finite on each sampling cycle; a non-finite value enters failure immediately without accumulating, writing home, or committing. After approximately one second, `q̄ = (1/N) Σ q_i` is computed; before writing, `q̄` is checked again and then written to application-layer `home_position`; application directions and offsets are restored. SetHome performs a full sample/failure reset at STAGE_START; if the previous run did not commit and a backup exists, the original rollback backup is preserved and never overwritten by the provisional home=0/average; if the previous run committed or no backup exists, the current valid home/direction/offset is snapshotted for the new run. The transformed encoder coordinate then corresponds to the new `0 rad`.
4. **Prevent target jumps**: on AutoCalibrate success and on the ServoOff shutdown after a border/return failure, finite measured positions are synchronized to the joint targets so the next task cannot inherit sweep/return-era targets; a SetHome failure does not sync targets, it rolls back the uncommitted provisional home and lets the next task establish targets. Non-finite measurements are skipped so a sensor fault is never written as a NaN target. A failed calibration does not write the zero point or set the finish flag; an unfinished calibration can roll back the saved zero and direction configuration.

The algorithm estimates a device coordinate reference. It recognizes neither patient anatomy nor clinical range restrictions, and it does not alter the mechanical boundary to accommodate them.

### Rehabilitation and Clinical Use

- Calibration actively drives joints to mechanical limits and includes an unpowered settling phase. Perform it only with the patient off the device, both feet clear of the ground, and the motion space unobstructed. Never use it to measure or forcibly improve a patient's range of motion.
- After calibration, check the zero posture and left/right symmetry unloaded before fitting and standing preparation. For border/return timeout, excessive position error, or abnormal resistance, stop and follow the fault procedure rather than repeating sweeps to force completion.
- Standard mechanical calibration is still required for patients with contracture, bony block, or postoperative restrictions. Clinical adaptation belongs in the approved restriction and training parameters.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.4.0.
- `fourier-grx` v4.4.59 fixes two regressions affecting this task's sweep: since v4.4.49 the position-protection bounds were initialised as "position at activation ± 0.25 rad", so a sweep whose joint travel exceeds that margin was falsely flagged as out of range and the robot servoed off mid-way; and the task-layer target clamp (also v4.4.49) neutralised the beyond-limit overshoot commands, so the joint stopped at the software limit instead of pressing against the mechanical hard stop. From this version on, this task (and the prismatic calibration sweeps) initialise the protection bounds as hardware limits ± margin and regain their overshoot commands. The internal blaze build shipped on 2026-10-20 — see [Fourier-GRX firmware · 4.4.59](/fourier-grx-M4/docs/en/release/fourier-grx#4459).
- Development version: fixes the case where a border-detection/return timeout still continued to SetHome and wrote the zero point. Phase-1 timeout, Phase-3 timeout, or non-finite measurement/command now enters failure: the zero point is not written, `flag_task_finish` is not set, AutoCalibrate performs ServoOff and returns to IDLE, and the standalone BorderAndReturn task requests ServoOff. Also: non-finite SetHome samples/average abort without commit or finish; AutoCalibrate explicitly resets the ServoOff stage before every Border->ServoOff switch and the SetHome stage before every switch to SetHome, so repeated commands cannot skip ServoOff or reuse old samples. The normal success flow is unchanged.
