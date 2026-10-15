---
layout: default
title: Firmware Update
nav_order: 1.3
parent: "Quick Start"
has_toc: true
nav_exclude: true
---

# Firmware Update

* TOC
{:toc}

> ℹ️ **Note**
>
> This page describes how to upgrade to a new firmware version on a device that has **already completed first-time installation** (the wired network is already configured with a static IP and `fourier-grx` runs normally).
>
> If this is a **brand-new device** or first-time installation has not been completed yet (the network is still in DHCP mode), see [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install) instead.

## Differences from first-time installation

The firmware update flow largely follows the same steps as first-time installation (download `.deb` → `dpkg -i` → `fourier-grx install`), with a few key differences:

| Item | First-Time Installation | Firmware Update |
|------|--------------------------|------------------|
| Network prerequisite | Defaults to **DHCP**; the installer automatically switches to a static IP | Already **static IP** (`192.168.137.220/24`) by default; no need to switch again |
| Getting the package | Manual download / `wget`, or copy from another device | Can use the `fourier-grx update` command to automatically probe, download, and install newer versions |
| Robot model configuration | Entered for the first time | Reads the old configuration from `~/fourier-grx-bak` and asks whether to reuse it — press Enter to reuse |

> ⚠️ **Note**
>
> - `fourier-grx update` only installs the package at the `dpkg` layer. The new version takes effect once `fourier-grx install` deploys it into `~/fourier-grx/`. **Both steps are required** — see [The Two Layers of Installation](/fourier-grx-M4/docs/en/reference/command_line_tool#the-two-layers-of-installation).
> - `fourier-grx install` first backs the existing `~/fourier-grx` up to `~/fourier-grx-bak` (overwriting any previous backup), then unpacks the new version.
> - Whether it's a first-time install or an update, `fourier-grx install` **always re-runs the network configuration script** (`setup_static_ipv4.sh`) unconditionally, resetting the wired interface to static IP `192.168.137.220/24`, gateway `192.168.137.1`, DNS `8.8.8.8,8.8.4.4`. If you changed any of these manually, note them down and reconfigure after the update.
> - `fourier-grx update` requires the device to have internet access (to probe the cloud storage for the latest version). If your static IP network configuration (gateway / DNS) cannot reach the internet, use the [manual package download](#option-2-manual-package-download) method instead, or refer to the [Network Connection and Remote Login](/fourier-grx-M4/docs/en/usage/network_connection) page to temporarily give the robot internet access by sharing WiFi from a laptop/tablet.

## Before You Update

- Confirm the device currently runs `fourier-grx` normally (first-time installation has already been completed)
- Confirm the device can reach the internet
- It's recommended to run `fourier-grx list` first to record the current robot model, version, and run mode configuration for comparison after the update:

```bash
fourier-grx list
```

## Option 1: Use the `fourier-grx update` command (Recommended)

`fourier-grx update` automatically reads the currently installed version and hardware variant, probes the [Firmware Releases](/fourier-grx-M4/docs/en/release) cloud storage for newer versions, and supports interactive selection.

### Automatically probe and select interactively

```bash
fourier-grx update
```

This lists the newer versions found (subsequent patches of the same minor version, the next minor version, and the next major version). Enter a number to select a version to install, press Enter to install the latest version, or enter `n` to cancel.

### Install a specific version directly

If you already know the exact version you want to install (for example, from the [Firmware Releases](/fourier-grx-M4/docs/en/release) page), you can specify it directly:

```bash
fourier-grx update <version>

# Example
fourier-grx update 4.4.53
```

The hardware variant is automatically read from the currently installed package — no need to specify it manually.

### Install a pre-release build

Pre-release channel builds never show up in the automatic probe above; they can only be installed by naming both the version and the channel:

```bash
fourier-grx update <version>-prerelease

# Example
fourier-grx update 4.4.53-prerelease
```

The model part of the variant still comes from the currently installed package; only the channel segment is replaced with `prerelease`. This syntax is available since v4.4.53; on earlier versions, install with `sudo dpkg -i <deb>` instead. See [Command Line Tool · Pre-release Channel](/fourier-grx-M4/docs/en/reference/command_line_tool#pre-release-channel).

### View command help

```bash
fourier-grx update --help
```

### Complete the installation configuration

`fourier-grx update` only downloads and installs the new `.deb` package via `dpkg -i`. **You still need to run the following command afterward to complete the configuration**:

```bash
fourier-grx install
```

> ℹ️ **Note**
>
> - `fourier-grx install` first asks whether to reuse the configuration found in `~/fourier-grx-bak`; press Enter to reuse it. If you answer no, or no old configuration is available, it prompts for the robot model, version, and run mode — re-select the same values you recorded with `fourier-grx list` before the update.
> - If you select the wrong configuration, you can always rerun `fourier-grx config` to fix it — see [Reconfigure and Verify](#reconfigure-and-verify) below.

## Option 2: Manual package download

If the device temporarily cannot access the internet (`fourier-grx update` probing fails), or you need to install a specific historical version, you can manually download the `.deb` package to complete the update. The flow is largely the same as first-time installation, except **you no longer need to handle network configuration** (it's already a static IP).

### Download the `fourier-grx` package

```bash
# Download the fourier-grx package (example version)
wget https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.53-linux-arm64-cpu-m4l-blaze.deb
```

> ℹ️ **Note**
>
> Replace the URL with the actual version you need from the [Firmware Releases](/fourier-grx-M4/docs/en/release) page.

### Install the `fourier-grx` package

```bash
sudo dpkg -i fourier-grx-xxx.deb  # replace xxx with the actual version number
```

### Install the runtime content

```bash
fourier-grx install
```

Again, this step first backs the existing `~/fourier-grx` up to `~/fourier-grx-bak`, then asks whether to reuse the robot model, version, and run mode from the backup. If you choose to reconfigure, re-enter the configuration you recorded before the update.

## Reconfigure and Verify

If you selected the wrong robot model or run mode during `fourier-grx install`, run the following commands:

```bash
# Reconfigure the robot model or run mode
fourier-grx config

# View the current configuration and confirm it matches what you had before the update
fourier-grx list

# Check the currently installed version
fourier-grx version
```

## Related Links

- [Network Connection and Remote Login](/fourier-grx-M4/docs/en/usage/network_connection): share a network from a laptop/tablet and log in to the robot controller via SSH when no router is available
- [Firmware Releases](/fourier-grx-M4/docs/en/release): view all versions and release notes
- [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install): the complete installation workflow for a brand-new device
- [Run Mode](/fourier-grx-M4/docs/en/reference/run_type): Developer Mode vs. Release Mode
