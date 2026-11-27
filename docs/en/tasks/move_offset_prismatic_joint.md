---
layout: default
title: Move by Offset (Prismatic Joint)
parent: Task Description
nav_order: 4.31
has_toc: true
nav_exclude: true
---

# Move by Offset (Prismatic Joint / Leg-Length Adjustment Joint)

* TOC
{:toc}

## Task Info

Task ID (TID): **4207**

Task Description:

- Adjusts the leg length by a relative offset **based on the current measured position** (target position = measured position at task entry + offset).
- Difference from [Adjust Length (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_length_prismatic_joint) (absolute position command):
  the relative offset is independent of the calibrated zero point in joint space, so **it can be used for small-range fine-tuning even when the leg-length full point has not been recalibrated after a software restart** (the patient does not need to dismount for recalibration).
- The sign convention is the same as the "Adjust Length" task (the command is converted by `× -1.0` before being sent).

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Left thigh adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |
| Left shank adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |
| Right thigh adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |
| Right shank adjustment offset | `float` | 0.0 | [-0.02, 0.02] | Adjustment offset relative to the current position, in m. |

> ⚠️ **Note**:
>
> - The offset of a single command is clamped to `±0.02 m`. For larger adjustments, send multiple commands, or use the [Adjust Length (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_length_prismatic_joint) task.
> - The task motion follows an open-loop time profile (S-curve), and the task finish flag is set according to the profile. Small offsets (on the order of 0.001 m) may not be reached exactly due to joint friction/self-locking; refer to the actual measured position.

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |

Command Interface:

| Parameter | Interface Mapping |
|-----------|------------------|
| Left thigh adjustment offset | `grx.virtual_panel_command_param_1` |
| Left shank adjustment offset | `grx.virtual_panel_command_param_2` |
| Right thigh adjustment offset | `grx.virtual_panel_command_param_3` |
| Right shank adjustment offset | `grx.virtual_panel_command_param_4` |

## Principle Explanation

### Algorithm Operation

Relative adjustment shares the absolute task's S-curve executor but constructs its targets differently:

1. **Direction and offset clipping**: panel offsets are multiplied by `−1` for actuator direction and each is clipped to `[-0.02,+0.02] m`. This limits one command, not accumulated position or remaining mechanical travel.
2. **Target from measured position**: startup latches `x0=x_measured` and computes `x_target=x0+Δx`. Both use the same coordinate system, so zero offset cancels in the subtraction and small relative moves do not depend on the absolute zero's numerical value.
3. **Synchronized duration**: `T=max_i(|Δx_i|/0.0015)`, then `r=clip(t/T,0,1)`, `s=6r⁵−15r⁴+10r³`, and `x_ref=x0+Δx·s(r)` produce smooth synchronized motion.
4. **Timeline completion**: PD tracks the reference, but there is no measured-arrival tolerance; the task holds the target and completes when time expires. Friction, self-locking, or load can prevent a small command from producing equal actual displacement, and repeated commands can accumulate toward a mechanical boundary.

“Independent of zero” therefore describes only relative-displacement mathematics. It permits neither skipped travel checks nor the assumption that completion proves actual adjustment.

### Rehabilitation and Clinical Use

- Use for small fitting adjustments under supported conditions, not while the patient is walking or bearing weight through the device. Availability after a software restart does not remove the need for normal leg-length calibration and fitting checks before treatment.
- Make only the necessary small adjustment and verify actual positions and joint alignment afterwards. Repeated relative commands accumulate, so confirm remaining mechanical travel rather than relying on the single-command ±0.02 m clip.
- Small offsets may not produce actual motion because of friction. Do not keep stacking commands to force numerical agreement. Stop for binding, abnormal resistance, pressure, or pain and inspect the mechanism and straps.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.4.37.
