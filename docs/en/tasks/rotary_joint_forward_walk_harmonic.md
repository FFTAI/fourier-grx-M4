---
layout: default
title: Harmonic-Coefficient Forward Walk
nav_order: 4.28
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Harmonic-Coefficient Forward Walk

## Task Info

Task ID (TID): **4131** (since v4.4.69; previously 4113)

Applicable Models: M4L (P1 / T1 / T2)

Task Description:

- Compared with [Passive Forward Walk (4129)](/fourier-grx-M4/docs/en/tasks/forward_walk_passive), only the **gait source** differs: 4111 derives a joint trajectory online from the LIPM inverted-pendulum model using step length / walking speed, while this task replays a periodic joint curve sampled from pre-stored Fourier (harmonic) coefficients of the main walking tables.
- Consequently the **curve shape is fixed**, selected from 16 curves by the "hip swing amplitude level" and the "knee restriction level"; the **timing** is set independently by the "cadence level". The three levels are orthogonal.
- This task **commands joint angles only, not translation**: the forward travel of the base (pelvis) is not produced by the algorithm, so the actual distance covered depends on the user plus the exoskeleton as a whole. No step length is promised.
- When the "stop motion flag" is set to true, the robot stops gradually (it finishes the current loop window, then runs a 1 s ending transition) rather than halting immediately.
- If torque protection is triggered, the robot immediately leaves this task and switches to the idle task (`TASK_IDLE`) and sets the torque-protection flag; the task must be re-issued to continue walking.

Task Parameters:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| Hip swing amplitude level | `int` | 2 | [1, 4] | First axis of curve selection. The difference between the four levels is almost entirely the hip swing amplitude (see table below). Invalid or unsent values fall back to level 2. |
| Knee restriction level | `int` | 1 | [1, 4] | Second axis of curve selection: levels 1/2/3/4 set the knee extension floor to 0 / 5 / 10 / 15° (the whole knee curve is lifted, and the hip shifts forward by the same amount). Values are clipped to 1..4. |
| Cadence level | `int` | 3 | [1, 6] | Changes timing only, not the curve shape. Level 1 is the slowest (5.25 s per stride) up to level 6 (2.45 s per stride). Invalid or ≤ 0 values keep the current level. |
| Start motion flag | `bool` | false | (true, false) | Whether to start motion. true = start; false = do not start (has no effect if motion is already running). |
| Stop motion flag | `bool` | false | (true, false) | Whether to stop motion. true = stop after the current loop window. |
| Pause motion flag | `bool` | false | (true, false) | Whether to pause motion. The task must be restarted to resume walking. |
| Enable torque protection | `bool` | false | (true, false) | Whether to enable the torque protection feature. |
| Torque protection limit | `float` | None | [0.0, 200.0] | The maximum allowable output torque for any joint during walking, in Nm. Takes effect only when torque protection is enabled; disabled by default. |

> **Parameters with no effect here**: upper/lower leg length, step length, walking speed, base height, step lift height and double-support ratio. This task replays a pre-computed coefficient table and performs no kinematic/dynamic inversion, so none of those values (including `param_4`~`param_8` and `grx.virtual_user_*_leg_length_*`) participate in generation; pushing the joystick axes does not change the trajectory either, it only triggers start/stop.

**Hip swing amplitude level → joint angle range** (URDF frame, measured from the coefficient table; negative hip = forward swing, positive = backward extension; positive knee = flexion):

| Level | Hip forward peak | Hip backward peak | Hip span | Knee swing peak | Knee extension floor |
|---|---|---|---|---|---|
| 1 | 20.1° | 10.0° | 30.1° | 53.0° | 0° |
| 2 | 23.0° | 13.1° | 36.1° | 55.0° | 0° |
| 3 | 25.0° | 15.1° | 40.1° | 55.0° | 0° |
| 4 | 30.0° | 15.1° | 45.1° | 55.0° | 0° |

**Knee restriction level** (the knee swing peak stays at 55°; the hip shifts forward as the restriction grows):

| Level | Knee extension floor | Knee swing peak | Mean hip angle |
|---|---|---|---|
| 1 (0°) | 0° | 55° | −6.6° |
| 2 (5°) | 5.0° | 55° | −10.7° |
| 3 (10°) | 10.0° | 55° | −14.8° |
| 4 (15°) | 15.0° | 55° | −17.3° |

**Cadence level** ("stride" = one left step + one right step = one full left-right cycle; the requirement range is 2.45 ~ 5.25 s per stride):

| Level | 1 | 2 | 3 (default) | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Stride time (actual, quantised to whole 20 ms frames) | 5.24 s | 4.82 s | 3.98 s | 3.34 s | 2.84 s | 2.44 s |
| Step time | 2.62 s | 2.41 s | 1.99 s | 1.67 s | 1.42 s | 1.22 s |
| Step frequency | 22.9 | 24.9 | 30.2 | 35.9 | 42.3 | 49.2 steps/min |

> Joint ranges versus hardware travel: hip approximately −30°…+15° (travel −90°…+40°) and knee 0°…55° (travel 0°…110°); every level stays within the limits.

**When parameters take effect**: panel parameters are read every control cycle, but **the whole trajectory is generated once after the task is entered and before "start" is pressed**. Therefore:

- Changing levels before start → applied immediately for this walk session;
- Changing levels while walking → does not affect the trajectory being executed; it takes effect on the **next start** (stop and re-start the task);
- The cadence level likewise only sets the sampling rate of the trajectory generated at the next start.

## Module Info

This task has no dedicated module commands; per-joint control through the module interface is not supported.

## Interface Info

Status interface:

| Parameter | Interface Mapping |
|-----------|-------------------|
| Task start flag | `task.flag_task_start` |
| Task finish flag | `task.flag_task_finish` |
| Task pause flag | `task.flag_task_pause` |
| Motion ratio | `rehab.motion_ratio` |
| Step frequency | `rehab.step_frequency` |
| Current gait key name | `rehab.gait_name` |
| Hip swing amplitude level | `rehab.gait_amplitude_level` |
| Knee restriction level | `rehab.gait_knee_restriction_deg` |
| Cadence level | `rehab.gait_speed_level` |
| Actual stride time | `rehab.gait_stride_time_s` |
| Reference trajectory position | `rehab.reference_joint_position` |
| Reference trajectory velocity | `rehab.reference_joint_velocity` |
| Reference trajectory maximum position | `rehab.reference_joint_position_max` |
| Reference trajectory minimum position | `rehab.reference_joint_position_min` |

> Note: `gait_name` is the internal key used to trace a curve back to its source table (format `m4_<suffix>_land_<N>`, where the suffix x4/5x4/10x4/15x4 encodes the knee restriction 0/5/10/15° and `land_N` encodes the hip amplitude level). **It is not intended for end-user display**; hosts should show `gait_amplitude_level` / `gait_knee_restriction_deg` / `gait_speed_level` instead. These five fields are cleared when a task deactivates (`gait_name` becomes an empty string) so that "no gait task running" is unambiguous.

Command interface:

| Parameter | Interface Mapping |
|-----------|-------------------|
| Hip swing amplitude level | `grx.virtual_panel_command_param_1` |
| Knee restriction level | `grx.virtual_panel_command_param_2` |
| Cadence level | `grx.virtual_panel_command_param_3` |
| Start motion flag | `grx.virtual_panel_command_start` |
| Stop motion flag | `grx.virtual_panel_command_stop` |
| Pause motion flag | `grx.virtual_panel_command_pause` |
| Enable torque protection | `grx.virtual_panel_command_switch_1` |
| Torque protection limit | `grx.virtual_panel_command_param_9` |

> `grx.virtual_panel_command_param_4` ~ `param_8` (including base height, step lift height and double-support ratio) and `grx.virtual_user_*_leg_length_*` have no effect in this task; see "Parameters with no effect here" above.

## Update Log

- v4.4.55: this task was added (TID 4113).
- v4.4.56: fixed the M4LP1 control thread exiting right after start — **on P1, use v4.4.56 or later**.
- v4.4.57: stable release shipped (2026-10-19); this task is now generally available — see [Fourier-GRX firmware · 4.4.57](/fourier-grx-M4/docs/en/release/fourier-grx#4457) for downloads and details. This version also flattens the rotary-joint PD hard-tier kp to `[500,500,500,500]`; the T1 / T2 baseline start-up gain drops from hip 600 / knee 500 to a flat 500. **On M4LP1, upgrade to v4.4.57** (or install `4.4.56-prerelease` or later).
- `fourier-grx` v4.4.69: to group the feedforward variants by control mode, this task's TID changed from **4113** to **4131**, and **4113 now refers to this task's PD + velocity-feedforward variant** (a new task). Two feedforward variants of this task are added: POSITION + velocity feedforward (**4127**) and PD + velocity feedforward (**4113**), both inheriting this task's gait source and three panel levels; the POSITION variant disables load detection and auto-adjust, the PD variant keeps this task's gains and load-driven PD ramp. ⚠️ Hosts must update their task IDs.
- `fourier-grx` v4.4.70: the hard tier rises to kp `[1500×4]` / kd `[90×4]` (hip ζ=0.77 unloaded / 0.64 loaded, knee ζ=1.37 / 1.28). This task keeps forward walking's load detection and PD ramp (it does not disable them), so the wider ramp now tops out in about 8.7 s (T2) / 10.1 s (T1); the inherited smoothing filter cutoff (2.5 → 8.0 Hz) and total delay compensation (0.06 → 0.03 s) apply. The tracking error needed to reach the 140 N·m over-torque protection falls from about 8° to about 5.3°. This task's cadence comes from the fitted `stride_time` and is independent of `step_length / walk_velocity`, so the doubled keyboard walking-speed default does not affect it.
- `fourier-grx` v4.4.71: **the v4.4.70 tuning is reverted** — the hard tier returns to kp `[1000×4]` / kd `[60×4]`, the inherited gait smoothing filter cutoff to 2.5 Hz, the total delay compensation to 0.06 s and the load-detection PD ramp floor to 0.01; the tracking error needed to reach the 140 N·m protection goes back to about 8°. This task's cadence comes from the fitted `stride_time`, so whether the keyboard walking default stays at 0.5 m/s does not affect it.
