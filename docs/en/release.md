---
layout: default
title: Firmware Releases
nav_order: 7
has_toc: true
nav_exclude: true
---

# Firmware Releases

* TOC
{:toc}

## Stable Releases

Stable releases contain the official release information for the Fourier-GRX-M4 SDK, including release dates, version numbers, download links, and release notes.

### Fourier-GRX Firmware

| Release Date | Version | Download                                                                                                                                                      | Release Notes                              | Support |
|--------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|---------|
| 2026-04-03   | 4.4.0   | [Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.0-linux-arm64-cpu-m4l-blaze.deb) | [Details](/fourier-grx-M4/docs/en/release#440) | ✅      |

### Fourier-M4 Firmware

| Release Date | Version | Download                                                                                                                   | Release Notes                              | Support |
|--------------|---------|----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|---------|
| 2025-07-22   | 2.0.6   | [Download](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.6.deb) | [Details](/fourier-grx-M4/docs/en/release#206) | ❌      |
| 2025-06-09   | 2.0.5   | [Download](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.5.deb) | [Details](/fourier-grx-M4/docs/en/release#205) | ❌      |

## Preview Releases

Preview releases are versions that have not yet been officially released. They may contain new features or fixes but are not guaranteed to be stable. Use with caution.

No preview releases available at this time.

## Installation

For the firmware installation process, refer to [Firmware Installation and Update](/fourier-grx-M4/docs/en/quickstart/firmware).

## Release Notes

### 4.4.0

Added:

- Added **M4LP1** hardware model support (new hardware variant with prismatic joints)
  - Added automatic prismatic joint calibration (automatically detects travel limits and resets to zero)
  - Added task for moving prismatic joints to a specified length
  - Improved rotary joint automatic calibration workflow (adopts a "travel to boundary then return" approach for better calibration reliability)
- Added **M4LT2** hardware model support (new hardware version using the FSA v3 asynchronous communication protocol)
  - Shares all algorithms and tasks with M4LT1; differs only in the motor communication protocol
- Added **Knee Restriction** task set for scenarios where knee joint range of motion is limited:
  - Knee restriction standing posture control (TID 4300)
  - Knee restriction passive forward walking (TID 4301)
  - Knee restriction passive marching in place (TID 4302)
  - Knee restriction assisted forward walking (adjust PD parameters, TID 4303)
  - Knee restriction assisted marching in place (adjust PD parameters, TID 4304)
  - Knee restriction assisted forward walking (adjust DT parameters, TID 4305)
  - Knee restriction assisted marching in place (adjust DT parameters, TID 4306)
- Added **Assisted Mode Subdivision**: split assisted walking/marching tasks into two independent modes — PD parameter adjustment and DT timing adjustment:
  - Assisted forward walking (adjust PD parameters, TID 4116)
  - Assisted marching in place (adjust PD parameters, TID 4117)
  - Assisted forward walking (adjust DT parameters, TID 4118)
  - Assisted marching in place (adjust DT parameters, TID 4119)
- Added **Planner** functionality: a trajectory planning auxiliary task that generates joint motion trajectory sequences for display on an upper-level system while keeping the device in a disabled state (TID 4401–4406)
- Added automatic rotary joint calibration task (TID 4120), which automatically completes boundary detection, power-off drop, and zero-point writing in three sequential steps
- Added keyboard shortcut input support (keyboard can now control assisted mode and other functions)
- IO board support (ioboard communication and read/write)

Fixed:

- Fixed multiple issues in the prismatic joint length automatic calibration
- Fixed issues with flag setting and clearing
- Fixed the virtual_panel not working
- Fixed several issues during walking

Changed:

- Optimized PD parameters for assisted mode (DT algorithm) to improve response stiffness
- Optimized the load/energy detection algorithm to reduce false triggers
- Improved stability of the gait generator in knee-restriction scenarios
- Improved packaging process to support PyInstaller packaging of the fi_fsa_v3 library (required for M4LT2)

### 2.0.6

Fixed:

- Fixed an issue where placing the device down while standing did not trigger force protection

Changed:

- Improved device operating speed and stepping cadence; the M4LV3 control cycle was corrected from 0.03 s to 0.025 s (a 1/6 improvement — may introduce operational stability risks, pending test verification)

Unchanged:

- Confirmed that force protection during walking is not implemented (this feature did not exist in previous code, and the requirement has not been confirmed as needed)
- Confirmed that position protection is active during walking, but cannot be triggered when moving backward (this issue cannot be easily fixed; pending after-sales engineer confirmation on occurrence frequency — if rare, it will not be corrected)

### 2.0.5

Fixed:

- Fixed an issue where assisted mode during marching in place could easily trigger unintended assisted movement
