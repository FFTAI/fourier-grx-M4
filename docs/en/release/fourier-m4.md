---
layout: default
title: Fourier-M4 Firmware
parent: "Firmware Releases"
nav_order: 2
has_toc: true
nav_exclude: true
---

# Fourier-M4 Firmware

* TOC
{:toc}

## Version List

| Release Date | Version | Download | Release Notes | Support |
|---------------|---------|----------|----------------|---------|
| 2025-07-22 | 2.0.6 | [⬇ Download](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.6.deb) | [Details](#206) | ❌ EOL |
| 2025-06-09 | 2.0.5 | [⬇ Download](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.5.deb) | [Details](#205) | ❌ EOL |

## Installation

For first-time installation, see [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install). To upgrade an already-installed device, see [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update).

---

## Release Notes

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
