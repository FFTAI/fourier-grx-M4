---
layout: default
title: Planner
nav_order: 4.26
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Planner

The Planner is an auxiliary task for trajectory-tracking tasks. It generates joint motion trajectory sequences for display on the host computer along with possible trajectory generation results. Planner tasks do not run the task activate/deactivate flow, so the robot itself does not execute trajectory-tracking motion.

> ⚠️ **Note**: before using the Planner, run Servo Off (TID=36) to make sure the device is de-energized, to avoid accidental injury.
>
> A Planner task does not drive the joints, but it still generates the trajectory every control cycle and merges it into the joint position protection envelope exactly as the executing task does (widening only, never narrowing; restored on reset).
>
> When a Planner task is deactivated, the step-frequency field (`rehab.step_frequency`) and the harmonic gait level echo fields (`rehab.gait_*`) reported to the host are cleared to zero.

## Passive Forward Walk

Task ID (TID): **4401**

Task Parameters: refer to [Passive Forward Walk](/fourier-grx-M4/docs/en/tasks/forward_walk_passive)

## Passive Mark Time

Task ID (TID): **4402**

Task Parameters: refer to [Passive Mark Time](/fourier-grx-M4/docs/en/tasks/mark_time_passive)

## Assist Forward Walk (Adjust PD Parameter)

Task ID (TID): **4403**

Task Parameters: refer to [Assist Forward Walk (Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd)

## Assist Mark Time (Adjust PD Parameter)

Task ID (TID): **4404**

Task Parameters: refer to [Assist Mark Time (Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_pd)

## Assist Forward Walk (Adjust dt Parameter)

Task ID (TID): **4405**

Task Parameters: refer to [Assist Forward Walk (Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt)

## Assist Mark Time (Adjust dt Parameter)

Task ID (TID): **4406**

Task Parameters: refer to [Assist Mark Time (Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt)

## Harmonic-Coefficient Forward Walk

Task ID (TID): **4407**

Task Parameters: refer to [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic)

The three panel levels (`param_1` hip swing amplitude, `param_2` knee extension restriction, `param_3` step frequency) are identical to the executing task 4113 and are likewise applied every control cycle. On top of the reference trajectory, this Planner also echoes the levels, so the host can preview the joint envelopes of all 4 × 4 = 16 curves and the 6 rhythm levels before the patient starts moving:

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

## Passive Forward Walk (Knee Restriction)

Task ID (TID): **4501**

Task Parameters: refer to [Passive Forward Walk (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive)

## Passive Mark Time (Knee Restriction)

Task ID (TID): **4502**

Task Parameters: refer to [Passive Mark Time (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_passive)

## Assist Forward Walk (Knee Restriction, Adjust PD Parameter)

Task ID (TID): **4503**

Task Parameters: refer to [Assist Forward Walk (Knee Restriction, Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_pd)

## Assist Mark Time (Knee Restriction, Adjust PD Parameter)

Task ID (TID): **4504**

Task Parameters: refer to [Assist Mark Time (Knee Restriction, Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_pd)

## Assist Forward Walk (Knee Restriction, Adjust dt Parameter)

Task ID (TID): **4505**

Task Parameters: refer to [Assist Forward Walk (Knee Restriction, Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_dt)

## Assist Mark Time (Knee Restriction, Adjust dt Parameter)

Task ID (TID): **4506**

Task Parameters: refer to [Assist Mark Time (Knee Restriction, Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

## Update Log

- Planner tasks (TID 4401–4406) added in `fourier-grx` v4.3.0.
- Since `fourier-grx` v4.4.47, planner tasks clear the reported step-frequency field on exit.
- `fourier-grx` v4.4.57 stable release (previously available through the v4.4.55 – v4.4.57 prerelease builds; on P1 use v4.4.57 or later): added the Harmonic-Coefficient Forward Walk planner (TID 4407), and extended the planner deactivation clear to cover all harmonic gait level echo fields.
