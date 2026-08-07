---
layout: default
title: Performance
nav_order: 6.5
parent: FAQ
nav_exclude: true
---

# Performance

## Control Frequency

| Interface | Data Update | Command Reception | Notes |
|-----------|-------------|-------------------|-------|
| User API | 50 Hz | 50 Hz | Fixed frequency |
| Developer API | Default 400 Hz (up to 500 Hz) | Configurable | Algorithm rate should not exceed the data update rate |

## Timeout Warning

**Symptom**: The program outputs `Timeout` warnings.

**Troubleshooting**:

1. Disable IPv6 (on the main controller and other devices on the LAN)
2. Check for loose actuator connection cables
3. Monitor network latency and packet loss

## Gamepad Sleep Issue

**Symptom**: The gamepad enters sleep mode after a period of inactivity and cannot control the robot after waking up.

**Solution**:

1. Use a gamepad that supports a longer sleep timeout or can be configured for no sleep, for example:
   - Gamesir G8+ Pro
   - Betop Starflash gamepad
2. After reconnecting the gamepad, restart the robot control program
