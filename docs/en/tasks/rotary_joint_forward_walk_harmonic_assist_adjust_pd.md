---
layout: default
title: Harmonic-Coefficient Assist Forward Walk (PD Adjustment)
nav_order: 4.29
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Harmonic-Coefficient Assist Forward Walk (PD Adjustment)

## Task Info

Task ID (TID): **4132** (added in v4.4.79)

Applicable Models: M4L (P1 / T1 / T2)

Task Description:

- The gait source is identical to [Harmonic-Coefficient Forward Walk (4131)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic): a periodic joint curve sampled from pre-stored Fourier (harmonic) coefficients of the main walking tables. The **curve shape is fixed** (selected from 16 curves by the amplitude level and the knee restriction level); the **timing** is set by the cadence level.
- The assist semantics are identical to [Assist Forward Walk (PD Adjustment, 4116)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd): the assist ratio linearly interpolates the PD control gains between buttery (most compliant) and soft (least compliant). A smaller ratio makes the joints more compliant and leaves more room for the patient to actively contribute torque.
- Difference from 4116: **4118 generates its trajectory online with the LIPM model from step length / walking speed, while this task replays a fixed curve from the coefficient table**. Consequently there are no step-length / walking-speed / base-height / step-height / double-support-ratio parameters; the first three panel levels are exactly the same as 4131 (amplitude / knee restriction / cadence), and the assist ratio moves to `param_4`.
- Load detection and automatic PD ramping are disabled in this task (the assist level is set directly by the host).
- This task **commands joint angles only, not translation**: the forward travel of the base (pelvis) is not produced by the algorithm, so the actual distance covered depends on the user plus the exoskeleton as a whole.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Hip swing amplitude level | `int` | 2 | [1, 4] | Same as 4131: first axis of curve selection. The difference between the four levels is almost entirely the hip swing amplitude. Invalid or unsent values fall back to level 2. |
| Knee restriction level | `int` | 1 | [1, 4] | Same as 4131: levels 1/2/3/4 set the knee extension floor to 0 / 5 / 10 / 15°. Values are clipped to 1..4. |
| Cadence level | `int` | 3 | [1, 6] | Same as 4131: changes timing only, not the curve shape. Level 1 is the slowest (5.25 s per stride) up to level 6 (2.45 s per stride). Invalid or ≤ 0 values keep the current level. |
| Assist ratio | `float` | 0.0 | [0.0, 1.0] | PD stiffness adjustment ratio. 0 = buttery (most compliant), 1 = soft (least compliant). The interpolation formula and gain table are exactly the same as 4116 — see [its documentation](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd). Treated as 0 when unsent. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop after the current loop window. |

> **Parameters with no effect here**: upper/lower leg length, step length, walking speed, base height, step lift height and double-support ratio. This task replays a pre-computed coefficient table and performs no kinematic/dynamic inversion; pushing the joystick axes does not change the trajectory either, it only triggers start/stop.

> When it takes effect:
>
> - The **assist ratio** is written into the joint PD gains only while the task is in its start stage (`STAGE_INIT` / `STAGE_START`). Changing it during walking does not change the current stiffness — the task must be restarted (same as 4116).
> - The **amplitude / knee-restriction / cadence levels** apply to the current start when changed before pressing "start"; changing them during walking does not affect the running trajectory and takes effect on the next start (same as 4131).

## Module Info

This task has no dedicated module commands and does not support per-joint control through the module interface.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|-------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Motion ratio | `rehab.motion_ratio` |
| Step frequency | `rehab.step_frequency` |
| Current gait key | `rehab.gait_name` |
| Hip swing amplitude level | `rehab.gait_amplitude_level` |
| Knee restriction level | `rehab.gait_knee_restriction_deg` |
| Cadence level | `rehab.gait_speed_level` |
| Actual stride time | `rehab.gait_stride_time_s` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory position max | `rehab.reference_joint_position_max` |
| Reference trajectory position min | `rehab.reference_joint_position_min` |

> The five gait report fields have the same semantics as 4131; see the interface section of [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic).

Command interface:

| Parameter | Interface Mapping |
|-----------|-------------------|
| Hip swing amplitude level | `grx.virtual_panel_command_param_1` |
| Knee restriction level | `grx.virtual_panel_command_param_2` |
| Cadence level | `grx.virtual_panel_command_param_3` |
| Assist ratio | `grx.virtual_panel_command_param_4` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |

> ⚠️ Unlike 4116: the **assist ratio is on `param_4`** (`param_3` is taken by the cadence level); `param_1` / `param_2` are the amplitude / knee-restriction levels, not step length / walking speed. Host software must use the mapping in this table instead of reusing 4116's parameter positions.

## Changelog

- `fourier-grx` v4.4.79: task added (TID 4132). Gait source and the three panel levels are identical to 4131; PD-assist semantics are identical to 4116 (assist ratio interpolates between buttery and soft, written once at task start).
