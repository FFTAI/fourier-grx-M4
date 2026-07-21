---
layout: default
title: IO Board Firmware
parent: "Firmware Releases"
nav_order: 3
has_toc: true
nav_exclude: true
---

# IO Board Firmware

* TOC
{:toc}

## Version List

| Release Date | Version | Download | Release Notes | Support |
|---------------|---------|----------|----------------|---------|
| 2026-05-12 | **1.0.0.3** | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.3_20260721.zip) | [Details](#1003) | ✅ Active |
| 2026-05-12 | 1.0.0.2 | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.2_20260512.zip) | [Details](#1002) | ✅ Active |

## Flashing Instructions

Download the corresponding version's zip package above, extract it, and follow the instructions in the included `RELEASE.md` to run `setup_release_env.ps1` and `flash_release.ps1` to complete flashing.

Hardware platform: ESP32-WROOM-32D

---

## Release Notes

### 1.0.0.3

> 📅 2026-05-12 &nbsp;·&nbsp; Platform: ESP32-WROOM-32D

🔧 **Changed**

- **Emergency stop button debouncing**: added 50ms software debouncing on GPIO 34, preventing repeated TRIGGERED / released prints caused by mechanical bounce

---

### 1.0.0.2

> 📅 2026-05-12 &nbsp;·&nbsp; Platform: ESP32-WROOM-32D

- Initial stable release
- Emergency stop button (GPIO 34) cuts the 38V relay when triggered
- Power button (GPIO 35) for local power on/off, with a 5V delayed power-off
- WS2812B LED strip battery level bar display
- UDP JSON API for remote read/write control
- HTTP OTA firmware upgrade support
