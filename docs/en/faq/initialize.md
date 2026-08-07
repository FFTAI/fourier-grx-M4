---
layout: default
title: Initialization Issues
nav_order: 6.3
parent: FAQ
nav_exclude: true
---

# Initialization Issues

## Configuration File Error

**Symptom**: Robot initialization fails with a configuration file error.

**Solution**:

1. Confirm the robot model is configured correctly — see [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install)
2. Restart the robot and try again

## Actuator Self-Check Failure

**Symptom**: `self-check` fails, reporting that the actuator at the specified IP cannot be reached.

![Self-check error](/fourier-grx-M4/assets/images/self_check_error.png)

**Troubleshooting**:

1. Check actuator power status (normally it should show a **purple breathing light**)
2. Confirm the wired network connection and static IP configuration
3. Check the integrity of all cable connections
