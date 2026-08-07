---
layout: default
title: Network Configuration
nav_order: 6.4
parent: FAQ
nav_exclude: true
---

# Network Configuration

## External Network Access

**Question**: How do I let the robot's main controller access the internet?

By default, the robot uses its wired Ethernet port to communicate with the actuators (static IP). When internet access is needed, switch as follows:

```bash
# Switch to dynamic IP (internet access)
sudo nmcli connection modify "Wired connection" ipv4.method auto
sudo systemctl restart NetworkManager

# When finished, switch back to static IP (robot operation)
sudo nmcli connection modify "Wired connection" ipv4.method manual \
    ipv4.addresses 192.168.137.220/24
sudo systemctl restart NetworkManager
```

## WiFi Hotspot Configuration

**Question**: How do I disable the WiFi hotspot from starting automatically?

```bash
sudo systemctl stop rocs-wifi      # Temporarily disable
sudo systemctl disable rocs-wifi   # Permanently disable (takes effect after reboot)
```
