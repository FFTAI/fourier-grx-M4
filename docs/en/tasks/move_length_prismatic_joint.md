---
layout: default
title: Adjust Length (Prismatic Joint)
parent: Task Description
nav_order: 4.27
has_toc: true
nav_exclude: true
---

# Adjust Length (Prismatic Joint / Leg-Length Adjustment Joint)

* TOC
{:toc}

## Task Info

Task ID (TID): **4206**

Task Description:

- Adjust the leg length.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Left thigh adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's thigh, in m. |
| Left shank adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's shank, in m. |
| Right thigh adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's thigh, in m. |
| Right shank adjustment length | `float` | 0.0 | [0.0, 0.095] | The adjustment segment length of the robot's shank, in m. |

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
| Left thigh adjustment length | `grx.virtual_panel_command_param_1` |
| Left shank adjustment length | `grx.virtual_panel_command_param_2` |
| Right thigh adjustment length | `grx.virtual_panel_command_param_3` |
| Right shank adjustment length | `grx.virtual_panel_command_param_4` |

## Principle Explanation

### Algorithm Operation

The task clips the four panel length values, converts them into prismatic-actuator coordinates, and sends them as absolute target positions relative to the calibrated zero. It adjusts the mechanical thigh and shank extension segments; it does not derive anatomical leg lengths from height or imaging. `motion_ratio` reports command-sequence progress, not actual positioning error.

### Rehabilitation and Clinical Use

- Trained staff should fit leg lengths from patient measurements, joint alignment, and strap positions, preferably unloaded or reliably supported. Do not change lengths during gait.
- Check left/right thigh and shank targets against actual positions and align the exoskeleton hip and knee axes with the patient's joints. Do not alter lengths casually to compensate for zero errors, strap migration, or abnormal posture.
- After adjustment, inspect skin pressure, motion clearance, symmetry, and standing posture before starting a low-risk task. The finish flag does not replace actual-position and fitting checks.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.1.19.
- `fourier-grx` v4.4.7: The upper limit of the thigh/shank adjustment length was changed from `0.090 m` to `0.095 m`, and the parameter range was updated to `[0.0, 0.095]`.
