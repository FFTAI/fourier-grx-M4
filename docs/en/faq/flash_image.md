---
layout: default
title: System Flashing Issues
nav_order: 6.8
parent: FAQ
nav_exclude: true
---

# System Flashing Issues

> ℹ️ **Note**: The following issues are related to [Flashing the System Image](/fourier-grx-M4/docs/en/quickstart/flash_image) (LubanCat-RK3588 control board).

## What if the PC does not detect the device?

Confirm that the DriverAssistant driver is correctly installed and that you are using a Type-C data cable (with data transfer capability) connected to the OTG port of the board. If it is still not detected, try uninstalling the old driver and reinstalling it, or switch to a different USB port.

## What if `network_scanner.ps1` fails to load?

This is a common issue caused by insufficient Windows PowerShell permissions. Close the current window, reopen PowerShell with **administrator privileges**, and run the script again.

![PowerShell permission error example](/fourier-grx-M4/assets/images/powershell_error.png)

## What if the LubanCat is already mounted on the device without an IP configured, and `network_scanner.ps1` cannot find it?

In this case, the device usually cannot be discovered directly via the LAN script. It is recommended to remove the LubanCat from the device first, connect the board **directly to the PC** with an Ethernet cable, and complete the IP configuration first. After confirming that communication works properly, mount it back onto the device.
