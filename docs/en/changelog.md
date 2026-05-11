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
