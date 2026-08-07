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
| 2026-07-21 | **1.0.0.3** | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.3_20260721.zip) | [Details](#1003) | ✅ Active |
| 2026-05-12 | 1.0.0.2 | [⬇ Download](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.2_20260512.zip) | [Details](#1002) | ✅ Active |

## Flashing Instructions

Download the corresponding version's zip package above, extract it, and follow the included instructions to complete flashing:

- **1.0.0.3 and later**: double-click `1_Setup_Flash_Env.bat` to set up the environment (first time only), then double-click `2_Flash_Firmware.bat` for one-click flashing. The `.bat` launchers automatically remove the downloaded-file blocking mark, and the window stays open after completion so you can review the results. You can also run `setup_release_env.ps1` and `flash_release.ps1` directly in PowerShell. See the included `README.txt` for a quick start, and `RELEASE.md` for full instructions (bilingual, Chinese & English).
- **1.0.0.2**: follow the instructions in the included `RELEASE.md` and run `setup_release_env.ps1` and `flash_release.ps1` in PowerShell to complete flashing.

Requirements: Windows 10 / 11, PowerShell 5.1 or later, and a USB data cable connected to the board.

> ℹ️ **Note**
>
> If the flashing script reports `No serial ports detected`, or no COM port appears in Device Manager, the USB-to-serial driver is not installed on your computer. Please install the driver following the [Windows Serial Driver Installation](/fourier-grx-M4/docs/en/faq/serial_driver) page and try again.

Hardware platform: ESP32-WROOM-32D

---

## Release Notes

### 1.0.0.3

> 📅 2026-07-21 &nbsp;·&nbsp; Platform: ESP32-WROOM-32D

🔧 **Changed**

- **Emergency stop button debouncing**: added 50ms software debouncing on GPIO 34, preventing repeated TRIGGERED / released prints caused by mechanical bounce

📦 **Package Improvements**

- Added `1_Setup_Flash_Env.bat` / `2_Flash_Firmware.bat` double-click launchers: automatically remove the PowerShell script download blocking mark, and keep the window open after completion
- Added a `README.txt` quick-start guide; `RELEASE.md` is now bilingual (Chinese & English)
- Environment setup script enhancements: when Python installation fails, the specific reason is printed (no network / firewall blocking / Windows "app execution aliases" blocking, etc.)

---

### 1.0.0.2

> 📅 2026-05-12 &nbsp;·&nbsp; Platform: ESP32-WROOM-32D

- Initial stable release
- Emergency stop button (GPIO 34) cuts the 38V relay when triggered
- Power button (GPIO 35) for local power on/off, with a 5V delayed power-off
- WS2812B LED strip battery level bar display
- UDP JSON API for remote read/write control
- HTTP OTA firmware upgrade support
