---
layout: default
title: Firmware Installation and Update
nav_order: 1.2
parent: "Quick Start"
has_toc: true
nav_exclude: true
---

# Firmware Installation and Update

* TOC
{:toc}

> ℹ️ **Note**
>
> This page describes the workflow for **firmware installation, upgrades, and initial robot model configuration** for the Fourier-GRX-M4 SDK.
> Download firmware packages from the [Firmware Releases](/fourier-grx-M4/docs/en/release) page.

## Video Tutorial

The following video demonstrates the complete `fourier-grx` firmware installation workflow.

<video controls style="width: 100%; max-width: 800px;">
  <source src="/fourier-grx-M4/assets/videos/video_install_fourier_grx.mp4" type="video/mp4">
  Your browser does not support the HTML5 video tag.
</video>

## Before You Start

Before starting the installation, make sure the following conditions are met:

- You have downloaded the required package version from the [Firmware Releases](/fourier-grx-M4/docs/en/release) page
- The robot controller can boot into the system normally
- A **wired network** connection is recommended, and the device should have internet access
- If you are using wired networking, first configure the robot network to **DHCP mode** so the device can access the internet

> ℹ️ **Note**
>
> During installation, the robot's wired network will be automatically reconfigured to use a **static IP address** so the system can operate normally afterward.

## Installation Steps

After preparing the environment, complete the installation with the steps below.

### Download the `fourier-grx` package

If the robot controller is already connected to the internet, you can download the package directly with `wget`. Example:

```bash
# Download the fourier-grx package (example version)
wget https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.1-linux-arm64-cpu-m4l-blaze.deb
```

> ℹ️ **Note**
>
> - Replace the URL with the actual version you need from the [Firmware Releases](/fourier-grx-M4/docs/en/release) page.
> - If you have already downloaded the `.deb` file manually, you can skip this step.

### Install the `fourier-grx` package

```bash
# Install the fourier-grx-xxx.deb package. After installation, the `fourier-grx` CLI will be available.
sudo dpkg -i fourier-grx-xxx.deb  # replace xxx with the actual version number
```

### Install the runtime content

```bash
# Install the full fourier-grx runtime content
fourier-grx install
```

> ℹ️ **Note**
>
> - If installation fails due to network or other issues, rerun the commands above.
> - Both first-time installation and version upgrades can follow this page.

## Robot Model Configuration

During installation, you will be prompted to select the robot model. Choose the option that matches your actual robot.

### Supported models for the current version

| Robot Model | Robot Version | Tested | [Run Mode](/fourier-grx-M4/docs/en/reference/run_type) | Compatible Robot |
|-------------|---------------|--------|--------------------------------------------------------|-----------------|
| M4          | T1            | No     | Developer Mode                                          | M4T1            |
| M4L         | T1            | No     | Developer Mode                                          | M4LT1           |
| M4L         | T2            | No     | Developer Mode                                          | M4LT2           |
| M4L         | P1            | No     | Developer Mode                                          | M4LP1           |

> ℹ️ **Robot Model Notes**
>
> - **M4LT2**: Latest model, equipped with **2.5th-generation FSA actuators**.
> - **M4LT1**: Equipped with **2.0th-generation FSA actuators**.
> - **M4LP1**: Equipped with legacy **1.0th-generation FSA actuators**, adapted to the 2.0-generation interface through a software upgrade.

### Run mode notes

> ℹ️ **Note**
>
> - The **Developer Mode** (`sdk`) in the table above is intended for secondary development through the SDK interfaces.
> - For **production robots**, configure the run mode as **Release Mode** (`release`) so the robot can be controlled from the upper-level application.
> - You can change the run mode with `fourier-grx config`. See [Run Mode](/fourier-grx-M4/docs/en/reference/run_type) for details.

### Reconfigure and verify

If you selected the wrong configuration during installation, run the following commands:

```bash
# Reconfigure the robot model or run mode
fourier-grx config

# View the current configuration
fourier-grx list
```

## Legacy `fourier-m4` installation method (deprecated)

> ⚠️ **Deprecated**: The following installation method is for the legacy `fourier-m4` software, which is no longer actively maintained.

```bash
# Fourier-M4 installation (legacy)
# Install the fourier-m4-xxx.deb package. After installation, the `fourier-m4` CLI will be available.
sudo dpkg -i fourier-m4-xxx.deb  # replace xxx with the actual version number

# Install the full fourier-m4 content
fourier-m4 install
```

> ⚠️ **Deprecated**: The following robot model list applies to the legacy `fourier-m4` software only.

### Supported legacy models

| Robot Model | Robot Version | Compatible Robot |
|-------------|---------------|------------------|
| M4L         | V2            | M4 8-motor version, Fourier Intelligence proprietary FSA V1 actuator, RK3399 embedded board |
| M4L         | V3            | M4 8-motor version, Fourier Intelligence proprietary FSA V1 actuator, RK3588 embedded board (LubanCat) |

> ℹ️ **Note**
>
> `fourier-m4` is the predecessor to `fourier-grx` and is no longer actively maintained. If your device supports `fourier-grx`, use `fourier-grx` for installation and operation.
