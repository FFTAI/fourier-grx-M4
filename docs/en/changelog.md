---
layout: default
title: Changelog
nav_order: 8
has_toc: true
nav_exclude: true
---

# Changelog

{:toc}

This document records all significant updates to the Fourier-GRX-M4 SDK and its documentation.

## August 2026

### v1.2.0 (2026-08-07)

**Documentation Updates**

- 📖 English documentation fully completed and synchronized:
  - All Task Description pages synced with the latest Chinese content, and missing English pages translated
  - English FAQ and Usage Guide restructured to match the Chinese child-page layout (from a single consolidated page to index + child pages)
  - Quickstart, Firmware Releases, and Examples pages synced with recent Chinese changes
- 📖 Firmware release support policy updated: on the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page, only the latest version is marked as "Active"; all historical versions are now marked "No longer supported" (downloads and release notes remain available for reference)
- 📖 New task pages: [Manual Calibrate (Rotary Joint)](/fourier-grx-M4/docs/en/tasks/rotary_joint_manual_calibrate) (TID 4121) and [Move by Offset (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_offset_prismatic_joint) (TID 4207); task index order updated accordingly
- 📖 New [Network Connection and Remote Login](/fourier-grx-M4/docs/en/usage/network_connection) guide: sharing a network without a router, automatic static IP (`192.168.137.220`) on the 20260805 image, web terminal (`:7681`), and SSH login credentials
- 📖 System image updated to 20260805; [Firmware Installation](/fourier-grx-M4/docs/en/quickstart/firmware_install) / [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update) pages now include network sharing + SSH login instructions
- 📖 Fixed 6 task documentation descriptions that were inconsistent with the code implementation

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.39` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page for the changes in versions 4.4.21 ~ 4.4.39)
- 📦 `ioboard` updated to `1.0.0.3` (see [IO Board Firmware](/fourier-grx-M4/docs/en/release/ioboard))

---

## June 2026

### v1.1.8 (2026-06-30)

**Changed**

- 🔧 **Stand task warm-up time shortened**: `STAGE_WARM_UP` damping transition duration reduced from `0.5 s` to `0.2 s`

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.20`

---

### v1.1.7 (2026-06-30)

**Added**

- ✨ **`fourier-grx update <version>` installs a specific version directly**: the variant is automatically read from the installed package, no manual specification needed. Example: `fourier-grx update 4.4.14`

**Improved**

- 🔧 **`fourier-grx update` probing range optimized**: patch probing expanded to +20 (miss=5); minor version only probes minor+1; major version only probes major+1.0.y; worst-case request count reduced from ~76 to ~36

**Fixed**

- 🐛 **`fourier-grx install` broken**: fixed an accidentally deleted `if [ $# -eq 0 ]` guard line that caused all subcommands to execute when the script was loaded

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.19`

---

### v1.1.6 (2026-06-30)

**Fixed**

- 🐛 **Stand task enable impact (complete fix)**: `STAGE_INIT`, `STAGE_START`, and `STAGE_WARM_UP` all set `kp=0`, ensuring a complete pure-damping transition regardless of the activation path. `STAGE_INIT` now also assigns `output_joint_position = measured_position`, preventing PD frames from targeting a zero-initialized stale cache; `STAGE_WARM_UP` lasts 0.5 s and, on timeout, interpolates from the current measured position into the motion stage. Log output now carries a stage prefix for easier field debugging

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.14`

---

### ~~v1.1.5 (2026-06-30)~~ *(revoked)*

> `STAGE_WARM_UP` was placed incorrectly (based on a misunderstanding of FSM stage management; `reset()` should not drive stage switching). Corrected in v1.1.6.

---

### ~~v1.1.4 (2026-06-29)~~ *(revoked)*

> `kp=0` lasted only one tick, which was not enough to suppress the impact; and `STAGE_INIT` no longer triggered on the second activation. Fully fixed in v1.1.6.

---

### ~~v1.1.3 (2026-06-29)~~ *(revoked)*

> The change in v1.1.3 that preset actuator target positions in `function_on_activate` was verified to be ineffective: the `SERVO_ON` communication frame only carries the enable command and no position data, so the change was reverted in v1.1.4.

---

## May 2026

### v1.1.2 (2026-05-14)

**New Features**

- 🔍 **Firmware version check flags**: `DynalinkGRX` gained `flag_version_check_error` (`0` = normal / `1` = error) and `version_check_error_info` (list of error details), automatically set when IOBoard / FSA / FSE firmware versions mismatch, do not respond, or fail to query, and synced to the host via Dynalink `read_fields`

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.6`

---

### v1.1.1 (2026-05-11)

**New Features**

- ⚙️ **Configurable assist trigger force interface for Mark Time Assist (DT mode)**: Added `assist_trigger_force_upper` (acceleration trigger force, default `2.0 Nm`) and `assist_trigger_force_lower` (deceleration trigger force, default `1.0 Nm`) as configurable parameters, set via upper-level panel `param_4` and `param_5`. Applicable tasks: TID 4119 (Assisted Marching in Place, adjust DT), TID 4306 (Knee Restriction Assisted Marching in Place, adjust DT). See [Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt) and [Knee Restriction Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

**Algorithm Fix**

- 🔧 **Assist trigger force threshold changed to absolute torque value**: Formula changed from `G[i] + offset` to `G[i] * 0.0 + offset` (gravity component zeroed). Experimental testing showed that including the gravity term `G[i]` caused system instability; it is now zeroed out and the configured value is used directly as the acceleration/deceleration trigger threshold

**Behavior Clarification**

- 📌 Clarified parameter update timing: all task parameters (step height, walk period, assist ratio, trigger forces, etc.) are read **once when the task is triggered** and do not refresh in real time; the task must be re-triggered for new values to take effect

**Documentation Updates**

- 📖 Updated [Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt): renamed parameters from "trigger force upper/lower offset" to "trigger force upper/lower", updated threshold description, added G[i] zeroing rationale
- 📖 Updated [Knee Restriction Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt): same as above
- 📖 Chinese documentation for both tasks updated in sync

---

### v1.1.0

**New Features**

- 🛡️ **M4LT2 Emergency Stop High-Damping Protection**: On M4LT2, when the hardware emergency stop switch (ioboard) is triggered, the robot no longer immediately cuts power. Instead, it automatically switches to the high-damping protection task (`TASK_ROTARY_JOINT_HIGH_DAMPING`, TID=4600). Joints remain powered and are controlled in a pure-damping PD mode (`kp=0`, `kd=80`) that prevents limbs from dropping instantly and gives operators a safer intervention window. See [High-Damping Protection Task](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping) for details.

**Documentation Updates**

- 📖 Added [High-Damping Protection Task page](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping)
- 📖 Updated [Task Description](/fourier-grx-M4/docs/en/tasks) task table with TID=4600
- 📖 Updated [M4L Quickstart](/fourier-grx-M4/docs/en/quickstart/m4l) with hardware emergency stop behavior notes

---

## July 2025

### v1.0.0 (2025-07-08)

**Major Milestone**

- 🎉 First official release of the Fourier-GRX-M4 SDK documentation
- 💡 Support for M4 series robot development
- 📖 Complete API documentation and usage guide
- ✨ Added common operations page
- 📚 Improved documentation structure and navigation
- 🔍 Enhanced search functionality

**Features**

- ✅ Core API interfaces
- ✅ Example code
- ✅ Developer guide
- ✅ Troubleshooting guide

**Notes**

- Currently focused on M4 series robots
- Support for other robot models will be added progressively
