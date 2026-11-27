---
layout: default
title: Set Home
parent: Task Description
nav_order: 4.05
has_toc: true
nav_exclude: true
---

# Set Home (All Joints)

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Set Home | **999** | Zero setting |

> ⚠️ **This task is not yet implemented.** TID 999 is defined in the general robot task table `TaskMenuGRX.TASK_SET_HOME`; `TaskMenuM4L` (the 4000–4999 range) has no matching implementation.
>
> For the M4L robot, please use the following dedicated calibration tasks instead:
> - Rotary joint (hip/knee) automatic zero-point calibration → [Auto Calibrate (Rotary Joint) TID=4120](/fourier-grx-M4/docs/en/tasks/rotary_joint_auto_calibrate)
> - Rotary joint zero-point manual setting → [Set Home (Rotary Joint) TID=4103](/fourier-grx-M4/docs/en/tasks/set_home_rotary_joint)
> - Prismatic joint (leg length) calibration → [Auto Calibrate (Prismatic Joint) TID=4210](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint)
>
> For the complete calibration procedure, refer to [Joint Zero Calibration](/fourier-grx-M4/docs/en/usage/calibrate).

## Principle Explanation

### Algorithm Operation

TID 999 is only an enum placeholder. No executable M4L control model is registered for it, so there is no receive-sample-write pipeline and no joint can be calibrated through this TID.

M4L zero calibration has two distinct aspects:

- **Coordinate offset construction**: encoder positions are used to map a mechanical posture to application-layer `0 rad` or a prismatic reference, so that `q_application = f(q_encoder, home_offset, direction)` remains consistent across tasks.
- **Joint-specific procedures**: rotary joints require mechanical-boundary detection or a manually selected zero followed by position sampling. Prismatic joints establish leg-length coordinates through full-travel limit detection. Actuator direction, units, persistence, and reboot requirements differ, so one unimplemented generic TID cannot replace both.

M4L therefore requires the dedicated rotary- and prismatic-joint tasks. This page is not an executable calibration entry point.

### Rehabilitation and Clinical Use

- Do not try this placeholder while a patient is wearing the device, and do not interpret a lack of motion or errors as successful calibration. Select the dedicated task in the maintenance procedure with the patient off the device.
- Zero references determine the physical posture represented by later trajectories. An incorrect zero can produce asymmetry or move joints toward uncomfortable positions. Check the device unloaded after calibration before clinical preparation.
- Staff should not set an arbitrary zero to accommodate deformity, contracture, or a painful posture. Such needs require joint clinical and engineering assessment and the approved restriction and fitting parameters.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added interface placeholder in `fourier-grx` v2.2.14 (not yet implemented).
