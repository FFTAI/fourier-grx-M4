---
layout: default
title: FAQ
nav_order: 6
has_toc: true
nav_exclude: true
---

# Frequently Asked Questions (FAQ)

* TOC
{:toc}

This document collects common questions and solutions encountered when using the Fourier-GRX-M4 SDK. If your issue is not listed here, please contact technical support.

## Hardware Issues

### Battery Not Charging

**Problem**: The robot is plugged in but the battery is not charging. After a long time charging, the robot still shuts off immediately upon powering on.

**Solution**:

1. Check that the charging cable is properly and securely connected to the charging port.
2. Check that the charger is functioning normally (red or blue light indicates charging; green light indicates fully charged).
3. Check that the battery switch button is pressed. **Only when pressed** will the battery charge. Otherwise, the power cable only supplies power to the robot without charging the battery.
4. Check whether the fuse has blown.
    - The fuse is located inside the battery compartment. Open the compartment to inspect the fuse.
    - If blown, the fuse must be replaced.

## Installation Issues

### Installation Interrupted

**Problem**: The installation program exits unexpectedly due to an accident or user error.

**Solution**:

1. Simply re-run the installation program. Any previously installed content will be cleaned up automatically.

### Robot Model Configuration Failure

**Problem**: During installation, the program prompts for a number to configure the robot model, but after entering it, a configuration error is reported and the installation exits.

**Solution**:

1. Verify that you entered the correct **number**, not the option name as text.
2. Restart the installation program and reconfigure.

## Initialization Issues

### Configuration File Error

**Problem**: Robot initialization fails with a configuration file error.

**Solution**:

1. Verify that the robot model is configured correctly. See [Firmware Installation and Update](/fourier-grx-M4/docs/en/quickstart/firmware).
2. Restart the robot and try again.

### Actuator Self-Check Failure

**Problem**: The robot self-check fails, indicating it cannot reach an actuator at the specified IP address.

![Self-check error](/fourier-grx-M4/assets/images/self_check_error.png)

**Solution**:

1. Check the actuator power status (should show a purple breathing light).
2. Confirm wired network connection and static IP configuration.
3. Check the integrity of all cable connections.

## Network Configuration

### External Network Access

**Problem**: How do I configure the robot to access the internet?

**Solution**:

1. Connect an external network via the wired Ethernet port.

2. Configuration steps:

```bash
# 1. Switch to dynamic IP (for internet access)
sudo nmcli connection modify "Wired connection" ipv4.method auto
   
# 2. Switch back to static IP (for robot operation)
sudo nmcli connection modify "Wired connection" ipv4.method manual \
    ipv4.addresses 192.168.137.220/24
   
# 3. Restart network service
sudo systemctl restart NetworkManager
```

### WiFi Hotspot Configuration

**Problem**: How do I disable the WiFi hotspot from starting automatically?

**Solution**:

```bash
# Temporarily disable
sudo systemctl stop rocs-wifi

# Permanently disable
sudo systemctl disable rocs-wifi

# Restart to apply
sudo reboot
```

## Performance

### Control Frequency

- **User API**:
    - Control frequency: 50 Hz
    - State output: 50 Hz
    - Command reception: 50 Hz

- **Developer API**:
    - Data update frequency: configurable, default 400 Hz (up to 500 Hz)
    - Algorithm execution frequency: configurable, recommended not to exceed the data update frequency

### Timeout Warning

**Problem**: The program reports a Timeout warning.

**Solution**:

1. Disable IPv6 (on the main controller and other devices on the LAN).
2. Check whether any actuator connection cables are loose.
3. Monitor network latency and packet loss.

### Gamepad Sleep Issue

**Problem**: The gamepad enters sleep mode after a period of inactivity and cannot reconnect to control the robot afterward.

**Solution**:

1. Use a gamepad that supports a longer sleep timeout or can be configured for no sleep:
    - Example: Gamesir G8+ Pro
    - Example: Betop Starflash gamepad
2. After reconnecting the gamepad, restart the robot control program.

## Development Environment Issues

### User API Communication Issue

**Problem**: The User API test program cannot communicate normally.

**Solution**:

1. Verify network configuration:
    - Zenoh preferentially uses the wired network interface.
    - Avoid connecting both wired and wireless networks simultaneously.
2. Check network connection status.
3. Confirm SDK version compatibility.

### Dependency Issue

**Problem**: `ImportError: GLIBC_2.33 not found`

**Solution**:

1. Install the necessary build tools:

```bash
sudo apt update
sudo apt install build-essential
```

2. System requirements:
    - Recommended: Ubuntu 22.04 LTS
    - Minimum: A Linux distribution that supports GLIBC 2.33

## Best Practices

1. **Development Environment Preparation**
    - Use the recommended operating system version.
    - Configure the network environment correctly.
    - Install all required dependencies.

2. **Network Configuration**
    - Use a static IP during development.
    - Switch to dynamic IP when internet access is needed.
    - Periodically check network connection status.

3. **Troubleshooting**
    - Review log files.
    - Check hardware connections.
    - Monitor system resources.

## Getting Help

If you encounter an issue not listed in this document:

1. Check the [Reference Guide](/fourier-grx-M4/docs/en/reference).
2. Review the [Changelog](/fourier-grx-M4/docs/en/changelog).
3. Contact technical support: [xin.chen@fftai.com](mailto:xin.chen@fftai.com)
