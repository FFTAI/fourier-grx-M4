---
layout: default
title: Device Integration
nav_order: 5.7
has_children: true
has_toc: true
nav_exclude: true
---

# Device Integration

This section covers connecting third-party devices (EEG, BCI, external sensors, research clients) to `fourier-grx` or the M4 upper computer. “Integration” here means engineering and data links, not a medical claim.

## Pages

- [EEG / BCI Integration Example](/fourier-grx-M4/docs/en/integrations/eeg_bci): the M4 upper-computer EEG TCP protocol and a custom BCI decoder using the User API.

## Common requirements

- Complete robot calibration and no-load validation first;
- third-party devices may only send high-level task or virtual-peripheral commands, never direct joint torque;
- provide an independent hardware emergency stop and trained supervision;
- log device versions, protocol versions, timestamps, and exceptions;
- complete risk assessment, ethics review, and informed consent before patient use.

> ⚠️ Examples in this section are for **research / engineering validation**. Clinical product use requires separate regulatory, cybersecurity, and clinical validation work.
