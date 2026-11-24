---
layout: default
title: Clinical Use
nav_order: 5.6
has_children: true
has_toc: true
nav_exclude: true
---

# Clinical Use

This section is written for rehabilitation therapists, clinical instructors, and on-site therapy teams. It explains M4L preparation, training-mode selection, parameter interpretation, monitoring, and stop criteria in therapist-oriented language.

> ⚠️ **Important**
>
> This section is equipment usage guidance, not diagnosis, prescription, or treatment advice. Eligibility, training intensity, contraindications, and stop criteria must be determined by qualified clinicians, together with the patient's condition, the product manual, and local institutional policy.

## Start here

- [Therapist Guide](/fourier-grx-M4/docs/en/rehab/therapist_guide): end-to-end workflow from screening to documentation.
- [Joint Zero Calibration](/fourier-grx-M4/docs/en/usage/calibrate): required calibration sequence after M4L power-on.
- [M4L Robot](/fourier-grx-M4/docs/en/quickstart/m4l): power-on, login, and starting the control program.
- [Task Description](/fourier-grx-M4/docs/en/tasks): TIDs, parameters, and protection behavior.

## Roles

| Role | Focus | Should not decide alone |
|------|-------|--------------------------|
| Therapist | Patient assessment, goals, mode/intensity, monitoring, stopping | Changing low-level control parameters, bypassing protection, direct joint commands |
| Field engineer | Connectivity, calibration, firmware, network, logs, faults | Clinical judgment |
| Developer | User / Developer API, task extensions, data analysis | Using unvalidated code on patients |

Define locally who may change which parameters, who may press the emergency stop, and who may end a session.
