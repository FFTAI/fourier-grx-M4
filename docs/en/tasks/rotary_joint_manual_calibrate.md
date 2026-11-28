---
layout: default
title: Manual Calibrate (Rotary Joint)
parent: Task Description
nav_order: 4.08
has_toc: true
nav_exclude: true
---

# Manual Calibrate (Rotary Joint)

* TOC
{:toc}

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Manual Calibrate (Rotary Joint) | **4121** | Calibration |

Task Description:

- Used to trigger the software-layer zero-point write after the user has **manually positioned the rotary joints at the desired zero posture**.
- Calibration proceeds through two sequential steps:
  1. **Joint Servo Off**: Executes ServoOff so the user can freely move the joints to the target posture and hold them still.
  2. **Set Home** (TID 4105): Samples joint position readings for approximately 1 second (cycle count derived from the control period) and takes the average, setting that average as the zero point (application-layer 0 rad reference position); every sample is checked for finiteness and the average is checked again before writing. Afterwards the joint target positions are automatically reset to the measured positions in the new coordinate frame, preventing a target-jump shock when the next task is enabled; on failure no zero point is written and the finish flag is not set.
- Difference from Auto Calibrate (TID 4120):

  | | Manual Calibrate (TID 4121) | Auto Calibrate (TID 4120) |
  |---|---|---|
  | Zero-point determination | User manually positions the joints | The robot automatically drives to the mechanical limits and retracts |
  | Applicable scenarios | Quick on-site calibration, known zero posture | Standard power-on calibration, first-time use |
  | Suspension required | No (depends on the target zero posture) | Yes (both feet off the ground) |
- Single-leg variants (TID 4122 / 4123): only the rotary joints of **that** leg are powered off and have their zero point set, while the other leg holds its position throughout — convenient for positioning one leg at a time by hand.
  - `TASK_ROTARY_JOINT_MANUAL_CALIBRATE_LEFT_LEG` (TID 4122): left-leg rotary joints, joint index 0-1
  - `TASK_ROTARY_JOINT_MANUAL_CALIBRATE_RIGHT_LEG` (TID 4123): right-leg rotary joints, joint index 2-3
  - Robot-wide calibration completion flag `flag_calibration`: each single-leg task records that leg as calibrated (`flag_calibration_left_leg` / `flag_calibration_right_leg`), and the robot-wide `flag_calibration` is set only **after both legs have been calibrated**; when TID 4121 is executed directly (both legs calibrated together), both are set at the same time. Therefore "4122 followed by 4123" and "one run of 4121" are equivalent in terms of the resulting flags.

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

> `flag_task_start` is set while the joint Servo Off phase (step 1) is running; `flag_task_finish` is set **only when SetHome has committed and no failure occurred**. If SetHome sampling/writing fails, the finish flag stays CLEAR, calibration flags are not set, and the task returns to TASK_IDLE (ServoOff is already active).

Command Interface:

This task requires no command parameters. Send the corresponding TID to trigger it.

## Internal Sub-Task Description

| Step | TID | Task Name | Description |
|------|-----|-----------|-------------|
| 1 | — | Joint Servo Off | Executes ServoOff; the user manually positions the joints at the target zero posture. |
| 2 | 4105 | Set Home (software layer) | Starts from INIT; samples for approximately 1 second and takes the average (50/100/200 cycles at 50/100/200 Hz); each sample is checked finite and the average is re-checked before writing; calls `set_home_position()` to write the zero point; resets joint targets on success, and does not commit/set finish on failure. |

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

- Successful calibration: `flag_task_finish` is set and SetHome has committed; each rotary joint's application-layer position should be close to 0 rad (error < 0.1 rad).
- The following are **calibration failures**: a SetHome sampling cycle (PROCESS_02) has a non-finite measured value, the average is non-finite before writing, or SetHome reaches FINISH without a commit.
  - ManualCalibrate detects `STAGE_ERROR` / `flag_failure` / FINISH-without-commit and does not print a success message or set calibration flags; it logs `calibration aborted - SetHome failed: ...` and returns directly to TASK_IDLE (ServoOff is already active).
  - SetHome's own failure log keyword is `home calibration failed: ...`; any provisional, uncommitted home write is rolled back on deactivation.
  - `flag_task_finish` stays CLEAR; do not treat a failure as success.
- If a joint shakes during sampling or produces non-finite readings, check the actuator state and re-trigger TID 4121 to recalibrate.
- Re-sending the same task no longer resets component stages in the FSM; ManualCalibrate still forces SetHome to start from INIT before ServoOff→SetHome, and SetHome fully resets samples/failure at STAGE_START, so samples from a previous run are not reused.

### Usage Restrictions

- Prismatic joint zero points **must** be recalibrated every power-on (TID=4210) and are not affected by this task.
- This task cannot be triggered while a motion task is running — exit the current task before performing calibration.

## Principle Explanation

### Algorithm Operation

Manual calibration assigns zero-posture selection to the operator and coordinate computation to the state machine:

1. **Scope selection**: the two-leg task handles all four rotary joints. Single-leg variants use joint indices to disable and calibrate only the selected side; the other side is outside that calibration flow.
2. **Disable and position**: after `SERVO_OFF`, the operator moves the joints to the intended mechanical zero and holds them there. The algorithm does not judge posture correctness; it only relies on stable readings during sampling.
3. **Average estimate**: approximately one second of encoder samples gives `q̄ = (1/N) Σ q_i`, reducing quantization and jitter compared with a single sample. Every sample is checked finite and `q̄` is checked again before writing; the mean is then written to application-layer `home_position`, and the original direction and application offset are restored. SetHome fully resets samples/failure at STAGE_START; if the previous run did not commit and a backup exists, the original rollback backup is preserved and never overwritten by the provisional home=0/average; if the previous run committed or no backup exists, current valid values are snapshotted for the new run.
4. **Commit and prevent jumps**: on success, targets are reset to measured positions in the new coordinates to prevent an old target from being restored at the next enable. An unfinished sequence can roll back the saved zero and direction configuration; a failure does not commit or set `flag_task_finish`.

Calibration quality therefore depends primarily on the manually selected posture and sampling stability. The algorithm does not convert a patient's comfortable posture into a standard mechanical zero.

### Rehabilitation and Clinical Use

- Staff familiar with the standard zero should perform manual calibration with the patient off the device. During single-leg calibration, the other leg may still hold torque, so support and guarding remain necessary.
- Do not use the patient's limb to define the device zero or treat the patient's current comfortable posture as the standard zero. Keep the device still during sampling and verify standing and gait reference postures unloaded afterwards.
- Use approved parameters such as knee restriction for patient-specific adaptation rather than changing the device zero, which would make coordinates inconsistent across tasks.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.4.22.
- Development version: SetHome sampling/writing now validates finite values and does not write home, commit, or set the finish flag on failure. ManualCalibrate detects SetHome failure, keeps `flag_task_finish` CLEAR, logs the actual error, and returns to TASK_IDLE; SetHome is forced to INIT before ServoOff→SetHome, and STAGE_START fully resets samples so repeated commands cannot reuse old samples. The normal success flow is unchanged.
- `fourier-grx` v4.4.53 added the left-leg / right-leg separate manual calibration variants (TID 4122 / 4123).
