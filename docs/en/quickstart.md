---
layout: default
title: Quick Start
nav_order: 1
has_toc: true
has_children: true
nav_exclude: true
---

# Quick Start

Choose the workflow that matches the current state of your device. Before operating the robot for the first time, read the safety notes on the relevant page and prepare appropriate support and emergency-stop measures.

## Choose by Device State

| Device state | Recommended page | Contents |
|--------------|------------------|----------|
| Installation is complete and the robot is an M4L model | [M4L Robot](/fourier-grx-M4/docs/en/quickstart/m4l) | Power-on, login, control-program startup, web debugging, and development-environment setup |
| The device is new or first-time installation is incomplete | [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install) | Download the package, deploy the runtime, and configure the robot model |
| First-time installation is complete and only a firmware upgrade is needed | [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update) | Upgrade with `fourier-grx update` or a manual package, then complete deployment |
| The system is damaged or the system image specifically needs replacing | [Flash System Image](/fourier-grx-M4/docs/en/quickstart/flash_image) | Flash supported LubanCat-RK3588 controller boards; flashing is not needed for normal use |
| The device uses the legacy M4 software | [M4 Robot](/fourier-grx-M4/docs/en/quickstart/m4) | Legacy workflow; this page is deprecated, and devices supporting the current software should use the M4L workflow |

## After Installation

1. Follow [M4L Robot](/fourier-grx-M4/docs/en/quickstart/m4l) to power on and log in to the robot, then start the control program.
2. Use [Examples](/fourier-grx-M4/docs/en/examples) to set up the development environment and choose a User, Developer, or UDP example.
3. While developing, use the [Reference Guide](/fourier-grx-M4/docs/en/reference) for interfaces and configuration fields, and [Task Description](/fourier-grx-M4/docs/en/tasks) for task parameters and precautions.
4. See the [Usage Guide](/fourier-grx-M4/docs/en/usage) for calibration, logs, and networking. If a problem occurs, start with the [FAQ](/fourier-grx-M4/docs/en/faq).
