---
layout: default
title: Therapist Guide
parent: Clinical Use
nav_order: 5.61
has_toc: true
nav_exclude: true
---

# Therapist Guide

* TOC
{:toc}

This guide translates `fourier-grx` tasks, parameters, and status fields into a therapy workflow. It does not replace clinician assessment, the product manual, or institutional safety rules.

> ⚠️ **Boundaries**
>
> - The robot is a training device, not a diagnostic device.
> - Tasks and parameters describe what the equipment can do, not a prescription.
> - Eligibility, intensity, contraindications, and stop criteria must be determined by qualified clinicians.
> - A trained person and a physical emergency stop take priority over software at all times.

## 1. Session flow

```text
Patient assessment
  → informed consent / contraindication screening
  → fitting and support
  → power-on, self-check, calibration
  → select mode and parameters
  → no-load / short trial
  → training
  → monitoring
  → stop, stand, remove support
  → documentation and handover
```

Print this flow in the treatment area and define who confirms each step.

## 2. Before treatment

### Patient

- Clinician completes eligibility, contraindication, and risk assessment;
- confirm the patient is fit for standing and walking training;
- obtain informed consent;
- ask about pain, spasticity, fatigue, dizziness, or other symptoms;
- check skin integrity and use padding if needed;
- confirm the patient understands how to signal stop.

### Environment and staff

- non-slip floor and clear space around the robot;
- enough room for the therapist to support and reach the emergency stop;
- at least one trained person with the patient throughout standing/walking;
- avoid unsupervised use.

### Equipment

- device powered on and actuator indicators normal;
- gamepad or upper computer connected;
- sufficient battery for the session;
- harness, braces, foot supports, and frame intact;
- calibration completed after this power-on.

## 3. Device preparation

### 3.1 Calibration

| Order | Task | TID | Purpose |
|-------|------|-----|---------|
| 1 | Prismatic-joint auto calibration | 4210 | Leg-length mechanism retracts and zeros |
| 2 | Rotary-joint auto calibration | 4120 | Hip/knee boundary detection and zeroing |

See [Joint Zero Calibration](/fourier-grx-M4/docs/en/usage/calibrate) for pins, safety distance, and failure handling.

### 3.2 Leg length and fitting

- set leg length from the patient's measurements;
- keep left/right length, straps, and foot supports symmetric;
- check for pressure or slippage at the knee, hip, and trunk;
- confirm stable weight bearing before standing/walking;
- follow the upper-computer instructions for leg-length adjustment.

### 3.3 Knee restriction

Knee restriction limits the knee extension angle in the reference trajectory. It is not an independent mechanical limit.

- determine the patient's actual knee range first;
- do not use higher stiffness to push the patient toward the restricted angle;
- if left and right limits differ, the current implementation takes the larger restriction requirement;
- observe actual knee angle and compensation, not just the UI number.

## 4. Choosing a training mode

| Goal | Task family | Examples | Effect |
|------|-------------|----------|--------|
| Early passive guidance | Passive walking / stepping | 4129 / 4130 | Device follows a precomputed trajectory |
| Precomputed gait with levels | Harmonic forward walking | 4131 | Amplitude, knee restriction, cadence levels |
| Active participation via stiffness | Assist PD | 4116 / 4117; harmonic 4132 | Assist ratio changes PD gains |
| Active participation via cadence | Assist DT | 4118 / 4119; harmonic 4133 | Assist ratio changes playback speed |
| Knee extension restriction | Knee-restricted tasks | 4301–4306 | Restricts knee extension in the reference |
| Trajectory preview | Planner | 4401–4409 | Computes and reports; does not drive joints |

> ⚠️ Task selection must follow the patient's condition and institutional protocol. The planner is for preview only.

### PD vs DT

- **PD assist** changes how strongly the joint follows the reference. Lower values are more compliant; higher values are closer to passive guidance.
- **DT assist** changes trajectory playback speed. Lower values give more response time; higher values are faster.
- Neither is a “percentage of assistive torque” or a “percentage of patient effort.”

## 5. Parameters in therapist language

| UI / field | How to understand it | Do not interpret as |
|------------|----------------------|---------------------|
| Assist ratio (PD) | Joint following strength / compliance | Percentage of force provided by the robot |
| Assist ratio (DT) | Trajectory playback speed | Direct torque increase |
| Step length / cadence / height | Gait amplitude, rhythm, foot lift | Patient strength indicator |
| Knee restriction | Lower bound of knee extension in the reference | Mechanical hard limit |
| Overload protection | Maximum allowed joint load | Training-intensity target |
| `assist_ratio` | Currently effective assist coefficient | Patient active participation |
| `active_ratio` | **Reserved field, currently fixed at 0** | Patient effort percentage |

`active_ratio` cannot currently be used to assess active participation. `assist_ratio` is not a measure of patient effort either. Use clinical observation, patient report, movement quality, and fatigue.

## 6. Monitoring

Observe:

- facial expression, breathing, pain, spasticity, fatigue;
- trunk control, heel contact, knee alignment, compensation;
- straps and foot supports;
- unusual sound, vibration, acceleration, or pauses;
- errors, protection, or disconnection on screen/terminal.

Useful software data:

| Data | Use | Caveat |
|------|-----|--------|
| `rehab.assist_ratio` | Current assist coefficient | Not patient effort |
| `rehab.motion_ratio` | Motion completion ratio | Not treatment effect |
| `rehab.step_frequency` | Current cadence | For rhythm verification |
| `rehab.reference_joint_position` | Reference joint position | Not measured position |
| `rehab.reference_joint_position_*` | Reference envelope | For range preview |
| `grx.robot_error_codes` | Error codes | Stop training if present |
| `flag_robot_*_protection` | Protection flags | Latched; clear per procedure |

### Stop criteria

Stop and protect the patient if:

- pain, marked spasticity, resistance, or patient request;
- dizziness, color change, breathing abnormality, or fatigue;
- abnormal acceleration, vibration, noise, or stalling;
- joint approaches a mechanical limit or abnormal compensation appears;
- strap/foot support slippage or loss of support;
- upper-computer error, disconnection, protection, or e-stop;
- any uncertainty about safety.

After stopping, maintain support, switch to standing/servo-off as appropriate, and confirm stability before handling alarms.

## 7. Documentation

Record patient ID, date, duration, model/firmware/upper-computer versions, task/TID, mode, assist ratio, step length, cadence, step height, knee restriction, overload protection, actual steps/cadence, adverse events, patient-reported symptoms, and stop reason.

Verify patient, date, and parameters before exporting a PDF/Excel report.

## 8. Common questions

### “I don't feel assistance”

Check whether the task is PD or DT. PD changes stiffness; DT changes playback speed. Low assist does not mean zero torque. Confirm the parameter was actually sent and the task was restarted if required.

### “It is too fast”

In DT mode, lower the assist ratio to slow playback. Check the cadence level. Do not use higher stiffness only to “stabilize” the patient; it can increase interaction forces.

### Knee discomfort

Stop, check knee restriction, leg length, straps, and foot supports. Observe actual knee angle vs reference. Do not mask pain by increasing assist.

### Angle shows ERR or no data

Confirm the task is active and `rehab` data is arriving; check firmware support for `reference_joint_position_max/min`; record the error and contact the field engineer. Do not substitute local estimates.

## 9. Upper-computer recommendations

For therapist-facing use:

- hide TIDs, raw field names, and low-level parameters;
- use clinical language: passive walking / assisted walking / stepping / knee restriction;
- provide patient profiles, presets, and session summaries;
- keep assist, cadence, step length, and knee restriction on one page;
- keep “stop training” and “emergency stop” prominent;
- generate the session record automatically.

## Related pages

- [Clinical Use](/fourier-grx-M4/docs/en/rehab)
- [Joint Zero Calibration](/fourier-grx-M4/docs/en/usage/calibrate)
- [Task Description](/fourier-grx-M4/docs/en/tasks)
- [Velocity and Position Protection](/fourier-grx-M4/docs/en/reference/protection)
