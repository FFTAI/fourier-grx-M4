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

> ⚠️ **Deprecated**: the `fourier-m4` software is no longer actively maintained. If your device supports the newer `fourier-grx`, it is recommended to install `fourier-grx` instead — see [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install) for first-time installation and [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update) for upgrades.

```bash
# Install the fourier-m4-xxx.deb file; the fourier-m4 program tool will be available on the system afterwards
sudo dpkg -i fourier-m4-xxx.deb  # xxx is the specific version number

# Install the full fourier-m4 content
fourier-m4 install
```

### Supported Models

| Robot Model | Robot Version | Compatible Robot Model                                       |
|-------|-------|------------------------------------------------|
| M4L   | V2    | M4 8-motor version, Fourier Intelligence proprietary actuator V1, using an RK3399 embedded board        |
| M4L   | V3    | M4 8-motor version, Fourier Intelligence proprietary actuator V1, using an RK3588 embedded board (LubanCat board) |

> ℹ️ **Note**
>
> `fourier-m4` is the predecessor program of `fourier-grx`, referred to as the "legacy version".

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
