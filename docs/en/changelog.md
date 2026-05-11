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

## May 2026

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
