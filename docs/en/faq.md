---
layout: default
title: FAQ
nav_order: 6
has_toc: true
has_children: true
nav_exclude: true
---

# Frequently Asked Questions (FAQ)

* TOC
{:toc}

> If your issue is not listed here, please contact technical support: [xin.chen@fftai.com](mailto:xin.chen@fftai.com)

## Category Navigation

| Category | Questions |
|----------|-----------|
| 🔋 [Hardware Issues](/fourier-grx-M4/docs/en/faq/hardware) | [Battery not charging](/fourier-grx-M4/docs/en/faq/hardware#battery-not-charging) |
| 📦 [Installation Issues](/fourier-grx-M4/docs/en/faq/install) | [Installation interrupted](/fourier-grx-M4/docs/en/faq/install#installation-interrupted) · [Model config failure](/fourier-grx-M4/docs/en/faq/install#robot-model-configuration-failure) |
| 🚀 [Initialization Issues](/fourier-grx-M4/docs/en/faq/initialize) | [Config file error](/fourier-grx-M4/docs/en/faq/initialize#configuration-file-error) · [Actuator self-check failure](/fourier-grx-M4/docs/en/faq/initialize#actuator-self-check-failure) |
| 🌐 [Network Configuration](/fourier-grx-M4/docs/en/faq/network) | [External network access](/fourier-grx-M4/docs/en/faq/network#external-network-access) · [WiFi hotspot](/fourier-grx-M4/docs/en/faq/network#wifi-hotspot-configuration) |
| ⚡ [Performance](/fourier-grx-M4/docs/en/faq/performance) | [Control frequency](/fourier-grx-M4/docs/en/faq/performance#control-frequency) · [Timeout warning](/fourier-grx-M4/docs/en/faq/performance#timeout-warning) · [Gamepad sleep](/fourier-grx-M4/docs/en/faq/performance#gamepad-sleep-issue) |
| 🛠️ [Development Environment](/fourier-grx-M4/docs/en/faq/dev_env) | [Communication issue](/fourier-grx-M4/docs/en/faq/dev_env#user-api-communication-issue) · [Missing dependency](/fourier-grx-M4/docs/en/faq/dev_env#dependency-issue) |
| 🔌 Driver Installation | [Windows Serial Driver Installation](/fourier-grx-M4/docs/en/faq/serial_driver) (when no serial port is detected during IO Board flashing) |
| 💿 System Flashing | [Device not detected / script cannot be loaded / device not found by scanner](/fourier-grx-M4/docs/en/faq/flash_image) |

---

## 💡 Best Practices

| Scenario | Recommendation |
|----------|----------------|
| Development setup | Use Ubuntu 22.04, install all dependencies, configure a static IP |
| Network management | Use a static IP during development; switch to dynamic temporarily when internet access is needed, then switch back |
| Troubleshooting | Check the runtime logs under `~/fourier-grx/log/` first |
| Calibration | After every power-on, run prismatic joint calibration → rotary joint calibration in order |

---

## Getting Help

If you encounter an issue not listed here, you can get support through the following channels:

- 📖 [Reference Guide](/fourier-grx-M4/docs/en/reference)
- 📋 [Changelog](/fourier-grx-M4/docs/en/changelog)
- 📧 Technical support: [xin.chen@fftai.com](mailto:xin.chen@fftai.com)
