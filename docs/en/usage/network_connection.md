---
layout: default
title: Network Connection and Remote Login
nav_order: 5.5
parent: "Usage Guide"
has_toc: true
nav_exclude: true
---

# Network Connection and Remote Login

* TOC
{:toc}

> ℹ️ **Note**
>
> This page explains how to **share a WiFi network from a laptop or tablet to its wired Ethernet port** when **no router / wireless-to-wired device** is available, providing network connectivity to the robot's controller computer and enabling remote login to the controller computer system via **SSH** or a **web terminal**.
>
> This method is commonly used in the following scenarios:
> - During [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install), internet access is required to download the installation packages (images before 20260805 use **DHCP** on the wired network by default; **images from 20260805 onward are automatically configured with the static IP `192.168.137.220` after flashing**)
> - During a [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update), temporary internet access is required to run `fourier-grx update`
> - No router/switch is available on site, so a laptop/tablet must be connected directly to the robot via an Ethernet cable

## Why Share the Network from a Laptop/Tablet

The robot's controller computer typically has only one wired Ethernet port, which serves two roles at the same time:

- **Connecting to the actuator LAN** (default static IP `192.168.137.220/24`; see [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence) for the actuator address range)
- **Accessing the internet** (downloading installation packages, probing for new versions via `fourier-grx update`, etc.)

On site there is often no router that can both "provide internet access" and "be on the same subnet as the robot". The simplest solution is to let the laptop or tablet you carry connect via its own WiFi, then **share** that network to its wired Ethernet port, and connect the robot's controller computer directly with a single Ethernet cable.

> ℹ️ **Tip**: Windows' "network sharing" feature (ICS, Internet Connection Sharing) sets the shared subnet to `192.168.137.0/24` by default (the host becomes `192.168.137.1`), which **happens to be the same subnet** as the robot's default static IP `192.168.137.220`. This is the origin of that default IP, and using this method requires no additional subnet configuration.

## Method 1: Share the Network from a Windows PC

1. Connect the laptop's **wired Ethernet port** (or a USB-to-Ethernet adapter) to the Ethernet port of the robot's controller computer with an Ethernet cable.
2. Open **Settings → Network & Internet → Dial-up / Change adapter options** (or Control Panel → Network and Sharing Center → Change adapter settings).
3. Find the **WiFi connection currently in use**, right-click it → **Properties**.
4. Switch to the **Sharing** tab and check **"Allow other network users to connect through this computer's Internet connection"**.
5. In the "Home networking connection" dropdown below, select the **Ethernet (wired) connection** that connects to the robot, then click **OK**.
6. Once sharing takes effect, the Ethernet adapter's IP automatically becomes `192.168.137.1`, and a DHCP service is enabled to assign `192.168.137.x` addresses to connected devices (the robot).

> ⚠️ **Caution**
>
> - If the PC has multiple wired ports/virtual adapters, make sure the one selected in step 5 is **the one actually connected to the robot** — choosing the wrong one will prevent connectivity.
> - **System images from 20260805 onward** are automatically configured with the static IP `192.168.137.220` after flashing — no scanning needed, the robot is directly reachable.
> - If the robot's network is still in **DHCP** mode (an older image that has not yet been installed), the robot will automatically obtain a dynamic IP from the `192.168.137.x` subnet once sharing takes effect; you can use the [`network_scanner.ps1`](/fourier-grx-M4/assets/scripts/network_scanner.ps1) script provided on the [Flash System Image](/fourier-grx-M4/docs/en/quickstart/flash_image) page to scan for the actual address.
> - If the robot already has a **static IP** (`192.168.137.220` — first-time installation completed, or flashed with a 20260805-or-later image), it is directly reachable at that fixed address once sharing takes effect, with no scanning required.

## Method 2: Share the Network from a macOS PC

1. Connect the Mac to the Ethernet port of the robot's controller computer using a USB-to-Ethernet adapter (most MacBooks have no built-in Ethernet port).
2. Open **System Settings → General → Sharing** (on older macOS versions: **System Preferences → Sharing**).
3. Click **Internet Sharing**, set "Share your connection from" to **Wi-Fi**, and check the option corresponding to the **Ethernet adapter** under "To computers using".
4. Turn on the toggle in the upper-right corner to enable Internet Sharing.

> ℹ️ **Note**: The subnet assigned by macOS Internet Sharing may not be `192.168.137.x` (it is usually `192.168.2.x`). If the robot is already configured with the static IP `192.168.137.220`, they may not be able to communicate directly. In this case, it is recommended to use **Method 1 (Windows PC)** instead, or temporarily configure the Mac's adapter with a manual static IP in the `192.168.137.x` subnet (e.g. `192.168.137.1/24`) before connecting.

## Method 3: Use a Phone Hotspot

Some phones support sharing a hotspot as a wired network via a USB data cable (e.g. Android's "USB tethering"). The procedure is similar to sharing from a PC — refer to your phone system's settings documentation for the exact entry point. Likewise, make sure the shared subnet is on the same subnet as the robot's current IP.

## Verifying the Network Connection

After connecting the Ethernet cable and completing the sharing configuration, you can verify connectivity from the PC with:

```bash
# Windows: run in PowerShell / CMD
ping 192.168.137.220

# macOS / Linux: run in a terminal
ping 192.168.137.220
```

If you receive replies, the network is connected and you can proceed with SSH login.

If the robot has not yet been configured with a static IP (still in DHCP mode — only the case for an older image that has not been installed), use the [`network_scanner.ps1`](/fourier-grx-M4/assets/scripts/network_scanner.ps1) script to scan the LAN for the actual assigned IP address; see the [Flash System Image](/fourier-grx-M4/docs/en/quickstart/flash_image) page for detailed usage.

## Web Terminal Login (20260805 and Later Images)

System images from version 20260805 onward include a built-in web terminal service. Once the network is connected, **no SSH client is required** — simply open in a browser:

```text
http://192.168.137.220:7681
```

This is the login terminal of the robot's controller computer; log in as prompted (the system username/password is the same as for SSH login).

## SSH Remote Login

Once the network is connected, you can log in remotely to the robot's controller computer via SSH, with no need to connect an HDMI monitor, keyboard, or mouse.

```bash
ssh cat@192.168.137.220
```

- Username: **`cat`**
- Password: **`temppwd`**
- If the robot is still in DHCP mode (only the case for an older image that has not been installed), replace the IP above with the actual address found by scanning with `network_scanner.ps1`.

On the first connection, the terminal will ask you to confirm the remote host fingerprint (host key); enter `yes` to continue:

```text
The authenticity of host '192.168.137.220 (192.168.137.220)' can't be established.
...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

> ⚠️ **Common issue: `REMOTE HOST IDENTIFICATION HAS CHANGED` warning**
>
> If the robot's controller computer has been **re-flashed with a system image** or **had its system reinstalled**, its SSH host key will change. When you connect again via the same IP, your local PC will refuse the connection because the recorded old host key does not match, showing a warning like:
>
> ```text
> WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
> ...
> Someone could be eavesdropping on you right now (man-in-the-middle attack)!
> ```
>
> This is **normal** (you are not actually being attacked). Clear the old host key saved locally and reconnect:
>
> ```bash
> ssh-keygen -R 192.168.137.220
> ssh cat@192.168.137.220
> ```

## Related Links

- [Firmware Installation (First-Time Setup)](/fourier-grx-M4/docs/en/quickstart/firmware_install): complete installation procedure for a brand-new device
- [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update): version upgrade procedure for an already-installed device
- [Flash System Image](/fourier-grx-M4/docs/en/quickstart/flash_image): detailed usage of the `network_scanner.ps1` script
- [Communication Interface](/fourier-grx-M4/docs/en/reference/communication): recommendations for network communication between the robot and the SDK
