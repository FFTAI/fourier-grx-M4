---
layout: default
title: Performance
parent: FAQ
nav_order: 6.5
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

1. Disable IPv6 (on the main controller, host PC, and other devices on the LAN); for a Windows host, see [Disable IPv6 on the Windows Host's Wired Adapter](/fourier-grx-M4/docs/en/faq/network#disable-ipv6-on-the-windows-hosts-wired-adapter)
2. Check for loose actuator connection cables
3. Monitor network latency and packet loss

## Occasional Stutter During Operation

**Symptom**: The robot occasionally stutters or pauses briefly during operation, causing short interruptions in control commands or data updates; this may be accompanied by `Timeout` warnings.

**Cause**: IPv6 is not disabled on the host PC or other devices on the LAN.

**Solution**:

1. Disable IPv6 on the main controller, host PC, and other devices on the LAN; for a Windows host, see [Disable IPv6 on the Windows Host's Wired Adapter](/fourier-grx-M4/docs/en/faq/network#disable-ipv6-on-the-windows-hosts-wired-adapter)
2. Re-run the task after disabling IPv6 and check whether the stutter is gone
3. If the stutter persists, continue troubleshooting loose cables, network latency, and packet loss as described in [Timeout Warning](#timeout-warning)

## Gamepad Sleep Issue

**Symptom**: The gamepad enters sleep mode after a period of inactivity and cannot control the robot after waking up.

**Solution**:

1. Use a gamepad that supports a longer sleep timeout or can be configured for no sleep, for example:
   - Gamesir G8+ Pro
   - Betop Starflash gamepad
2. After reconnecting the gamepad, restart the robot control program
