---
layout: default
title: Network Configuration
parent: FAQ
nav_order: 6.4
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

## Disable IPv6 on the Windows Host's Wired Adapter

**Question**: The Windows host is directly connected to the robot over Ethernet and shares its network, and domain name resolution fails, communication times out, or the robot stutters occasionally during operation.

**Solution**: Disable IPv6 on the wired adapter that connects the host to the robot.

1. Press `Win + R`, type `ncpa.cpl`, and press Enter to open Network Connections.
2. Find the **Ethernet** adapter connected to the robot, right-click it, and select **Properties**.
3. Clear the **Internet Protocol Version 6 (TCP/IPv6)** checkbox and click **OK**.

![The Internet Protocol Version 6 (TCP/IPv6) option in the Windows Ethernet Properties dialog](/fourier-grx-M4/assets/images/windows_ipv6_properties.png)

> The checkbox is shown selected; clear **Internet Protocol Version 6 (TCP/IPv6)** to disable it. Image: Microsoft, from Microsoft Learn [Guidance for configuring IPv6 in Windows for advanced users](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Alternatively, use an elevated PowerShell:

```powershell
# Check the IPv6 binding state of the wired adapter
Get-NetAdapterBinding -Name "Ethernet" -ComponentID ms_tcpip6

# Disable IPv6 (use the actual adapter name, e.g. "Ethernet 2")
Disable-NetAdapterBinding -Name "Ethernet" -ComponentID ms_tcpip6
```

> ℹ️ **Note**
>
> - Only disable IPv6 on the wired adapter connected to the robot; leave WiFi unchanged. Re-enable network sharing or reconnect the Ethernet cable for the change to take effect.
> - To restore, replace `Disable-NetAdapterBinding` with `Enable-NetAdapterBinding`, or re-check IPv6 in the adapter properties.
