---
layout: default
title: Planner
parent: Task Description
nav_order: 4.33
has_toc: true
nav_exclude: true
---

# Planner

* TOC
{:toc}

The Planner is an auxiliary task for trajectory-tracking tasks. It generates joint motion trajectory sequences for display on the host computer along with possible trajectory generation results. Planner tasks use a lightweight activation/deactivation path rather than the executing task's full motion activation flow, so the robot itself does not execute trajectory-tracking motion.

> ⚠️ **Note**: before using the Planner, run Servo Off (TID=36) to make sure the device is de-energized, to avoid accidental injury.
>
> A Planner task does not drive the joints, but it still generates the trajectory every control cycle and merges it into the joint position protection envelope exactly as the executing task does (widening only, never narrowing; restored on reset).
>
> When a Planner task is deactivated, the step-frequency field (`rehab.step_frequency`) and the harmonic gait level echo fields (`rehab.gait_*`) reported to the host are cleared to zero.

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| Passive Forward Walking | **4401** | Planner preview |
| Passive Marching in Place | **4402** | Planner preview |
| Assisted Forward Walking (PD Mode) | **4403** | Planner preview |
| Assisted Marching in Place (PD Mode) | **4404** | Planner preview |
| Assisted Forward Walking (dt Mode) | **4405** | Planner preview |
| Assisted Marching in Place (dt Mode) | **4406** | Planner preview |
| Passive Forward Walking – Harmonic Fitting | **4407** | Planner preview |
| Assisted Forward Walking – Harmonic Fitting (PD Mode) | **4408** | Planner preview |
| Assisted Forward Walking – Harmonic Fitting (dt Mode) | **4409** | Planner preview |
| Passive Forward Walking – High-Lift | **4410** | Planner preview |
| Assisted Forward Walking – High-Lift (PD Mode) | **4411** | Planner preview |
| Assisted Forward Walking – High-Lift (dt Mode) | **4412** | Planner preview |
| Passive Forward Walking (Knee Restriction) | **4501** | Planner preview |
| Passive Marching in Place (Knee Restriction) | **4502** | Planner preview |
| Assisted Forward Walking (Knee Restriction, PD Mode) | **4503** | Planner preview |
| Assisted Marching in Place (Knee Restriction, PD Mode) | **4504** | Planner preview |
| Assisted Forward Walking (Knee Restriction, dt Mode) | **4505** | Planner preview |
| Assisted Marching in Place (Knee Restriction, dt Mode) | **4506** | Planner preview |
| Passive Forward Walking – High-Lift (Knee Restriction) | **4507** | Planner preview |
| Assisted Forward Walking – High-Lift (Knee Restriction, PD Mode) | **4508** | Planner preview |
| Assisted Forward Walking – High-Lift (Knee Restriction, dt Mode) | **4509** | Planner preview |
| Assisted Forward Walking – Harmonic Fitting (Knee Restriction, PD Mode) | **4510** | Planner preview |
| Assisted Forward Walking – Harmonic Fitting (Knee Restriction, dt Mode) | **4511** | Planner preview |

## Passive Forward Walking

Task Parameters: refer to [Passive Forward Walking](/fourier-grx-M4/docs/en/tasks/forward_walk_passive)

## Passive Marching in Place

Task Parameters: refer to [Passive Marching in Place](/fourier-grx-M4/docs/en/tasks/mark_time_passive)

## Assisted Forward Walking (PD Mode)

Task Parameters: refer to [Assisted Forward Walking (PD Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd)

## Assisted Marching in Place (PD Mode)

Task Parameters: refer to [Assisted Marching in Place (PD Mode)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_pd)

## Assisted Forward Walking (dt Mode)

Task Parameters: refer to [Assisted Forward Walking (dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt)

## Assisted Marching in Place (dt Mode)

Task Parameters: refer to [Assisted Marching in Place (dt Mode)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt)

## Passive Forward Walking – Harmonic Fitting

Task Parameters: refer to [Passive Forward Walking – Harmonic Fitting](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic)

The three panel levels (`param_1` hip swing amplitude, `param_2` knee extension restriction, `param_3` step frequency) are identical to the executing task 4131 and are likewise applied every control cycle. On top of the reference trajectory, this Planner also echoes the levels, so the host can preview the joint envelopes of all 4 × 4 = 16 curves and the 6 rhythm levels before the patient starts moving:

| Reported field | Meaning |
| :--- | :--- |
| `rehab.reference_joint_position_max`<br>`rehab.reference_joint_position_min` | Trajectory extremes per joint over the cyclic segment (start/end transitions excluded), in rad, URDF frame (hip flexion is negative).<br>**Order: [hip_L, knee_L, hip_R, knee_R]**, per joint; the two legs are in opposite phase, so take the union of both legs yourself to show the full hip range |
| `rehab.reference_joint_position`<br>`rehab.reference_joint_velocity` | Reference position / velocity at the current tick (the Planner does not drive the joints, but this value still advances with time) |
| `rehab.gait_name` | Current coefficient-table key (e.g. `m4_5x4_land_3`), traceable back to the m4 source table; empty string after deactivation |
| `rehab.gait_amplitude_level` | Current `param_1` value (1–4) |
| `rehab.gait_knee_restriction_deg` | Current `param_2` value (0 / 5 / 10 / 15°) |
| `rehab.gait_speed_level` | Current `param_3` value (1–6) |
| `rehab.gait_stride_time_s` | Actual stride time in seconds, quantized to whole frames |
| `rehab.step_frequency` | Step frequency (steps/min) |

Hip and knee envelopes per level (union of both legs, degrees; each cell is "hip forward-swing peak … hip backward-swing peak", forward swing is negative):

| Knee restriction | Amplitude 1 | Amplitude 2 | Amplitude 3 | Amplitude 4 | Knee swing peak |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 (0°) | −20.1 … +10.0 | −23.0 … +13.1 | −25.0 … +15.1 | −30.0 … +15.1 | 53.0 / 55.0 |
| 2 (5°) | −25.0 … +5.0 | −26.5 … +8.1 | −27.5 … +10.1 | −30.0 … +10.1 | 53.0 / 55.0 |
| 3 (10°) | −30.0 … 0.0 | −30.0 … +3.1 | −30.0 … +5.1 | −30.0 … +5.1 | 53.0 / 55.0 |
| 4 (15°) | −30.0 … 0.0 | −30.0 … 0.0 | −30.0 … +0.1 | −30.0 … +0.1 | 53.0 / 55.0 |

The knee **extension floor** equals the restriction level of that row (0 / 5 / 10 / 15°); the knee swing peak is 53.0 for amplitude level 1 and 55.0 for levels 2–4.

> 📌 The hip forward-swing peak is capped at 30° (−30° in the URDF frame) in the source data tables: the larger the knee restriction, the further forward the whole hip curve sits, and at levels 3 and 4 the top of the curve is clipped flat, so **the angular range of the amplitude levels converges**. What remains distinguishable is the curve shape (swing timing and peak position). If the host needs the amplitude levels to be visually obvious, pair them with knee restriction levels 1 or 2.

## Assisted Forward Walking – Harmonic Fitting (PD Mode)

Task Parameters: refer to [Assisted Forward Walking – Harmonic Fitting (PD Mode)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd)

The panel mapping is identical to executing task 4132: `param_1` hip swing amplitude, `param_2` knee extension restriction, `param_3` cadence level, and `param_4` assist ratio. The Planner evaluates the assist-dependent PD level and generates and reports the reference trajectory, but does not send PD or position targets to the robot.

## Assisted Forward Walking – Harmonic Fitting (dt Mode)

Task Parameters: refer to [Assisted Forward Walking – Harmonic Fitting (dt Mode)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_dt)

The panel mapping is identical to executing task 4133: `param_1` hip swing amplitude, `param_2` knee extension restriction, `param_3` cadence level, and `param_4` assist ratio; `switch_1` enables automatic assist. The Planner adjusts reference-trajectory playback progress according to the assist ratio and also evaluates the torque-based automatic-assist logic when enabled, but does not send control targets to the robot.

## Passive Forward Walking – High-Lift

Task Parameters: refer to [Passive Forward Walking – High-Lift](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift). The panel mapping matches executing task 4134, with `param_3` setting the final actual ground-clearance target.

## Assisted Forward Walking – High-Lift (PD Mode)

Task Parameters: refer to [Assisted Forward Walking – High-Lift (PD Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist). Planner 4411 matches executing task 4136: `param_3` sets the lift target and `param_4` sets the assist ratio used to calculate the PD tier, but no PD or position targets are sent to the robot.

## Assisted Forward Walking – High-Lift (dt Mode)

Task Parameters: refer to [Assisted Forward Walking – High-Lift (dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist_adjust_dt). Planner 4412 matches executing task 4137: `param_4` and `switch_1` control reference playback and automatic-assist evaluation without sending control targets to the robot.

## Passive Forward Walking (Knee Restriction)

Task Parameters: refer to [Passive Forward Walking (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive)

## Passive Marching in Place (Knee Restriction)

Task Parameters: refer to [Passive Marching in Place (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_passive)

## Assisted Forward Walking (Knee Restriction, PD Mode)

Task Parameters: refer to [Assisted Forward Walking (Knee Restriction, PD Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_pd)

## Assisted Marching in Place (Knee Restriction, PD Mode)

Task Parameters: refer to [Assisted Marching in Place (Knee Restriction, PD Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_pd)

## Assisted Forward Walking (Knee Restriction, dt Mode)

Task Parameters: refer to [Assisted Forward Walking (Knee Restriction, dt Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_dt)

## Assisted Marching in Place (Knee Restriction, dt Mode)

Task Parameters: refer to [Assisted Marching in Place (Knee Restriction, dt Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

## Passive Forward Walking – High-Lift (Knee Restriction)

Task Parameters: refer to [Passive Forward Walking – High-Lift (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_high_lift). High-lift parameters match executing task 4307; user leg lengths and left/right knee restrictions are also read. The larger restriction becomes a shared minimum knee angle for both legs.

## Assisted Forward Walking – High-Lift (Knee Restriction, PD Mode)

Task Parameters: refer to [Assisted Forward Walking – High-Lift (Knee Restriction, PD Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_high_lift_assist_adjust_pd). Planner 4508 matches executing task 4308, combining the shared knee restriction, high-lift target and `param_4` PD assist ratio without driving the joints.

## Assisted Forward Walking – High-Lift (Knee Restriction, dt Mode)

Task Parameters: refer to [Assisted Forward Walking – High-Lift (Knee Restriction, dt Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_high_lift_assist_adjust_dt). Planner 4509 matches executing task 4309, combining the shared knee restriction, high-lift target, `param_4` playback speed and `switch_1` automatic assist without driving the joints.

## Assisted Forward Walking – Harmonic Fitting (Knee Restriction, PD Mode)

Task Parameters: refer to [Assisted Forward Walking – Harmonic Fitting (Knee Restriction, PD Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_harmonic_assist_adjust_pd). Planner 4510 matches executing task 4310, combining the table restriction, additional virtual-user restriction and `param_4` PD assist ratio without driving the joints.

## Assisted Forward Walking – Harmonic Fitting (Knee Restriction, dt Mode)

Task Parameters: refer to [Assisted Forward Walking – Harmonic Fitting (Knee Restriction, dt Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_harmonic_assist_adjust_dt). Planner 4511 matches executing task 4311, combining the table restriction, additional virtual-user restriction, `param_4` playback speed and `switch_1` automatic assist without driving the joints.

## Principle Explanation

### Algorithm Operation

The Planner inherits each executing task's algorithm while cutting actuator output out of the task lifecycle: **run only the control model's computation and reporting paths**.

1. **Same model**: each Planner inherits its executing counterpart, so DSP/VHIP COM and foot generation, IK, harmonic phase sampling, common knee restriction, PD interpolation, and dt playback clocks use the same code rather than a separate approximate preview.
2. **Replacement activation**: activation initializes buffers, model parameters, and the position-protection envelope without running the full motion activation sequence. `_function_meta()` still advances the algorithm every control cycle, so references advance in time and automatic dt assist evaluates current feedback.
3. **No robot write**: computed `joint_target_position` and Kp/Kd remain in model/report buffers instead of being written to robot joints. `rehab.reference_joint_position/velocity` is model output, not encoder measurement, and the Planner itself does not make patient or device follow it.
4. **Preview metrics**: per-joint `max/min` values cover the cyclic segment, cadence comes from the generated period, and harmonic tasks additionally report keys and levels. Deactivation clears reports and resets the protection envelope.

It answers “what reference would these inputs and model state produce?” It cannot validate actual tracking error, actuator torque, patient tolerance, or adequacy of external support.

### Rehabilitation and Clinical Use

- Before treatment, clinical and engineering staff can preview joint ranges, cadence, and left/right trajectories to screen obviously unsuitable parameter combinations before unloaded and supervised execution tests.
- Disable the actuators as required and retain device support. No Planner torque output does not make the whole preparation workflow risk-free; subsequent enabling and trajectory entry require separate assessment.
- A successful preview does not establish patient tolerance or verify actual foot clearance, dynamic balance, strap fitting, or torque safety. First execution still needs conservative parameters and external protection.
- Do not record Planner reference extrema, cadence, or assist calculations as the patient's measured range, walking ability, or treatment outcome.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Planner tasks (TID 4401–4406) added in `fourier-grx` v4.3.0.
- Since `fourier-grx` v4.4.47, planner tasks clear the reported step-frequency field on exit.
- `fourier-grx` v4.4.57 internal blaze build (previously available through the v4.4.55 – v4.4.57 prerelease builds; on P1 use v4.4.57 or later): added the Passive Forward Walking – Harmonic Fitting planner (TID 4407), and extended the planner deactivation clear to cover all harmonic gait level echo fields.
- `fourier-grx` v4.4.81 internal build: added harmonic-fitting assisted forward-walk planners for PD and dt adjustment (TID 4408 / 4409), with panel mappings identical to executing tasks 4132 / 4133.
- `fourier-grx` v4.4.89 internal build: added normal and knee-restricted high-lift Planners (TID 4410 / 4507), with panel and user-input mappings matching executing tasks 4134 / 4307.
- Development version: added high-lift PD / dt assist Planners 4411 / 4412 and knee-restricted counterparts 4508 / 4509, covering the inputs and algorithms of executing tasks 4136 / 4137 / 4308 / 4309.
- Development version: added harmonic knee-restricted PD / dt assist Planners 4510 / 4511, covering the table restriction, additional virtual-user restriction and assist inputs of executing tasks 4310 / 4311.
