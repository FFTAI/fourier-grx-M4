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

> If your issue is not listed here, please contact technical support: [xin.chen@fftai.com](mailto:xin.chen@fftai.com)

## Category Navigation

| Category | Questions |
|----------|-----------|
| 🔋 [Hardware](#-hardware-issues) | [Battery not charging](#battery-not-charging) |
| 📦 [Installation](#-installation-issues) | [Installation interrupted](#installation-interrupted) · [Model config failure](#robot-model-configuration-failure) |
| 🚀 [Initialization](#-initialization-issues) | [Config file error](#configuration-file-error) · [Actuator self-check failure](#actuator-self-check-failure) |
| 🌐 [Network](#-network-configuration) | [External network access](#external-network-access) · [WiFi hotspot](#wifi-hotspot-configuration) |
| ⚡ [Performance](#-performance) | [Control frequency](#control-frequency) · [Timeout warning](#timeout-warning) · [Gamepad sleep](#gamepad-sleep-issue) |
| 🛠️ [Development](#️-development-environment) | [Communication issue](#user-api-communication-issue) · [Missing dependency](#dependency-issue) |

---

## 🔋 Hardware Issues

### Battery Not Charging

**Symptom**: Robot is plugged in but battery is not charging; robot shuts off immediately on power-on even after a long time connected.

**Troubleshooting**:

1. Check that the charging cable is securely connected to the charging port
2. Verify charger status: red/blue light = charging, green light = fully charged
3. Confirm the battery switch is **pressed in** — only when pressed will the battery charge; otherwise the power cable supplies the robot only, without charging
4. Check if the fuse has blown (located inside the battery compartment); replace if blown

---

## 📦 Installation Issues

### Installation Interrupted

**Symptom**: The installer exits unexpectedly due to an error or accidental input.

**Solution**: Simply re-run the installer. Any partially installed content will be cleaned up automatically.

### Robot Model Configuration Failure

**Symptom**: The installer prompts for a number to configure the robot model, but reports a configuration error after input.

**Solution**:

1. Enter the correct **number** — do not type the option name as text
2. Restart the installer and reconfigure

---

## 🚀 Initialization Issues

### Configuration File Error

**Symptom**: Robot initialization fails with a configuration file error.

**Solution**:

1. Verify the robot model is configured correctly — see [Firmware Installation and Update](/fourier-grx-M4/docs/en/quickstart/firmware)
2. Restart the robot and try again

### Actuator Self-Check Failure

**Symptom**: `self-check` fails, reporting it cannot reach an actuator at the specified IP.

![Self-check error](/fourier-grx-M4/assets/images/self_check_error.png)

**Troubleshooting**:

1. Check actuator power status (should show a **purple breathing light**)
2. Confirm wired network connection and static IP configuration
3. Check integrity of all cable connections

---

## 🌐 Network Configuration

### External Network Access

**Question**: How do I configure the robot's main controller to access the internet?

The robot uses its wired Ethernet port with a static IP for actuator communication by default. To access the internet, temporarily switch to dynamic IP:

```bash
# Switch to dynamic IP (internet access)
sudo nmcli connection modify "Wired connection" ipv4.method auto
sudo systemctl restart NetworkManager

# Switch back to static IP (robot operation)
sudo nmcli connection modify "Wired connection" ipv4.method manual \
    ipv4.addresses 192.168.137.220/24
sudo systemctl restart NetworkManager
```

### WiFi Hotspot Configuration

**Question**: How do I disable the WiFi hotspot from starting automatically?

```bash
sudo systemctl stop rocs-wifi      # Temporarily disable
sudo systemctl disable rocs-wifi   # Permanently disable (takes effect after reboot)
```

---

## ⚡ Performance

### Control Frequency

| Interface | Data Update | Command Reception | Notes |
|-----------|-------------|-------------------|-------|
| User API | 50 Hz | 50 Hz | Fixed |
| Developer API | Default 400 Hz (up to 500 Hz) | Configurable | Algorithm rate should not exceed data update rate |

### Timeout Warning

**Symptom**: Program outputs `Timeout` warnings.

**Troubleshooting**:

1. Disable IPv6 on the main controller and other LAN devices
2. Check for loose actuator connection cables
3. Monitor network latency and packet loss

### Gamepad Sleep Issue

**Symptom**: Gamepad enters sleep mode after inactivity and cannot reconnect to control the robot.

**Solution**:

1. Use a gamepad that supports a longer sleep timeout or can be configured for no sleep:
   - Example: Gamesir G8+ Pro
   - Example: Betop Starflash gamepad
2. After reconnecting the gamepad, restart the robot control program

---

## 🛠️ Development Environment

### User API Communication Issue

**Symptom**: User API test program cannot communicate normally.

**Troubleshooting**:

1. Zenoh preferentially uses the wired network interface — avoid connecting both wired and wireless simultaneously
2. Confirm the robot IP and local machine are on the same subnet
3. Verify SDK version compatibility

### Dependency Issue

**Symptom**: `ImportError: GLIBC_2.33 not found`

**Solution**:

```bash
sudo apt update && sudo apt install build-essential
```

System requirements:
- Recommended: Ubuntu 22.04 LTS
- Minimum: A Linux distribution supporting GLIBC 2.33

---

## 💡 Best Practices

| Scenario | Recommendation |
|----------|----------------|
| Development setup | Use Ubuntu 22.04, install all dependencies, configure a static IP |
| Network management | Use static IP during operation; switch to dynamic only when internet access is needed |
| Troubleshooting | Check `~/fourier-grx/log/` first for runtime logs |
| Calibration | After every power-on, run prismatic joint calibration → rotary joint calibration in order |

---

## Getting Help

- 📖 [Reference Guide](/fourier-grx-M4/docs/en/reference)
- 📋 [Changelog](/fourier-grx-M4/docs/en/changelog)
- 📧 Technical support: [xin.chen@fftai.com](mailto:xin.chen@fftai.com)
