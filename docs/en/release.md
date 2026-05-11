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

## Latest Release

> **Fourier-GRX `4.4.3`** · 2026-05-11 · Platform: `linux/arm64` · [Download Now](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.3-linux-arm64-cpu-m4l-blaze.deb)

## Stable Releases

### Fourier-GRX Firmware

| Release Date | Version | Download | Release Notes | Support |
|--------------|---------|----------|---------------|---------|
| 2026-05-11 | **4.4.3** | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.3-linux-arm64-cpu-m4l-blaze.deb) | [Details](#443) | ✅ Active |
| 2026-04-10 | 4.4.2 | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.2-linux-arm64-cpu-m4l-blaze.deb) | [Details](#442) | ✅ Active |
| 2026-04-08 | 4.4.1 | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.1-linux-arm64-cpu-m4l-blaze.deb) | [Details](#441) | ✅ Active |
| 2026-04-03 | 4.4.0 | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.0-linux-arm64-cpu-m4l-blaze.deb) | [Details](#440) | ✅ Active |

### Fourier-M4 Firmware

| Release Date | Version | Download | Release Notes | Support |
|--------------|---------|----------|---------------|---------|
| 2025-07-22 | 2.0.6 | [⬇ Download](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.6.deb) | [Details](#206) | ❌ EOL |
| 2025-06-09 | 2.0.5 | [⬇ Download](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.5.deb) | [Details](#205) | ❌ EOL |

## Preview Releases

No preview releases available at this time.

## Installation

For firmware installation instructions, refer to [Firmware Installation and Update](/fourier-grx-M4/docs/en/quickstart/firmware).

---

## Release Notes

### 4.4.3

> 📅 2026-05-11 &nbsp;·&nbsp; Platform: `linux/arm64`

✨ **Added**

- **M4LT2 emergency stop high-damping protection task** (TID 4600): when the hardware emergency stop switch (ioboard) is triggered, joints no longer cut power immediately — the system automatically switches to high-damping mode (`kp=0`, `kd=80`) to prevent limbs from dropping suddenly. See [High-Damping Protection Task](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping)
- **Configurable assist trigger force interface for Mark Time Assist (DT mode)**: new `assist_trigger_force_upper` / `assist_trigger_force_lower` parameters (defaults: `2.0 Nm` / `1.0 Nm`), configurable via panel `param_4` / `param_5`. Applies to TID 4119 and TID 4306

🔧 **Changed**

- Assist trigger force thresholds changed to absolute torque values: formula updated from `G[i] + offset` to `G[i] * 0.0 + offset` (gravity component zeroed). Experimental testing confirmed that including `G[i]` caused system instability

---

### 4.4.2

> 📅 2026-04-10 &nbsp;·&nbsp; Platform: `linux/arm64`

✨ **Added**

- **HXC whole-body RL CPG walk task** (TID 3302, for HXCT1): controls 12 leg joints (position control); 4 wheel joints (indices 12–15) are locked at zero velocity via PD braking (`kp=0, kd=10`)

🐛 **Fixed**

- Fixed `fourier-core`: `fi_fsa_v2.5` encoder zero point could not be written

---

### 4.4.1

> 📅 2026-04-08 &nbsp;·&nbsp; Platform: `linux/arm64`

🐛 **Fixed**

- Fixed configuration key mismatch: robot name field changed from `robot_name` to `name` to match the actual YAML config structure

🔧 **Changed**

- Added `pdm` and `PyInstaller` to the `dependencies.sh` install script
- Added `build_pyinstaller.py` to support M4L packaging builds
- Added `fi_fsa_v3` PyInstaller runtime hook (`rthook_fi_fsa_v3.py`) to ensure M4LT2 libraries load correctly after packaging

---

### 4.4.0

> 📅 2026-04-03 &nbsp;·&nbsp; Platform: `linux/arm64`

✨ **Added**

- **M4LP1** hardware model support (new variant with prismatic joints)
  - Automatic prismatic joint calibration (detects travel limits and resets to zero)
  - Task for moving prismatic joints to a specified length
  - Rotary joint calibration updated to a "travel to boundary then return" approach for improved reliability
- **M4LT2** hardware model support (FSA v3 async protocol); shares all algorithms and tasks with M4LT1
- **Knee Restriction** task set for limited knee range-of-motion scenarios:
  - Standing posture control (TID 4300)
  - Passive forward walking (TID 4301) · Passive marching in place (TID 4302)
  - Assisted forward walking — PD (TID 4303) · Assisted marching in place — PD (TID 4304)
  - Assisted forward walking — DT (TID 4305) · Assisted marching in place — DT (TID 4306)
- **Assisted mode subdivision**: split into separate PD and DT variants:
  - Assisted forward walking — PD (TID 4116) · Assisted marching in place — PD (TID 4117)
  - Assisted forward walking — DT (TID 4118) · Assisted marching in place — DT (TID 4119)
- **Planner** tasks: trajectory planning in a device-disabled state for upper-level display (TID 4401–4406)
- Automatic rotary joint calibration task (TID 4120): boundary detection → power-off drop → zero-point write
- Keyboard shortcut input support
- IO board communication and read/write support

🐛 **Fixed**

- Fixed multiple issues in prismatic joint length calibration
- Fixed flag set/clear inconsistencies
- Fixed `virtual_panel` not responding
- Fixed several issues during walking

🔧 **Changed**

- Tuned PD parameters for assisted mode (DT algorithm) to improve response stiffness
- Reduced false triggers in the load/energy detection algorithm
- Improved gait generator stability in knee-restriction scenarios
- Packaging now supports PyInstaller bundling of the `fi_fsa_v3` library (required for M4LT2)

---

### 2.0.6

> 📅 2025-07-22

🐛 **Fixed**

- Fixed: placing the device down while standing did not trigger force protection

🔧 **Changed**

- M4LV3 control cycle corrected from `0.03 s` to `0.025 s` (~1/6 speed improvement); stepping cadence increased accordingly. Stability impact pending verification

⚠️ **Known Limitations**

- Force protection during walking is not implemented (requirement not yet confirmed)
- Position protection cannot be triggered while moving backward (low-frequency issue; under review)

---

### 2.0.5

> 📅 2025-06-09

🐛 **Fixed**

- Fixed: assisted mode during marching in place could easily trigger unintended assisted movement
