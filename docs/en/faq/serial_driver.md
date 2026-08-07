---
layout: default
title: Windows Serial Driver Installation
nav_order: 6.7
parent: FAQ
has_toc: true
nav_exclude: true
---

# Windows Serial Driver Installation

* TOC
{:toc}

> ℹ️ **Note**
>
> This page explains how to install USB-to-serial drivers (CP210x / CH340) on a **Windows PC**.
>
> When flashing the [IO Board firmware](/fourier-grx-M4/docs/en/release/ioboard), the PC communicates with the ESP32 through the USB-to-serial chip on the development board. If the corresponding driver is not installed, the system will not create a COM port, and the flashing script will report `No serial ports detected`, causing the flashing to fail.

## When Do You Need to Install the Driver

If any of the following occurs, the serial driver is probably not installed on your PC:

- The flashing script (`flash_release.ps1` / `2_Flash_Firmware.bat`) reports `No serial ports detected`
- After connecting the development board via USB, **no** new COM port appears under "Ports (COM & LPT)" in Device Manager
- Device Manager shows an unknown device with a ⚠️ yellow exclamation mark, named something like `USB-Serial Controller`, `USB2.0-Serial`, or `CP2102 USB to UART Bridge Controller`

## Step 1: Identify the USB-to-Serial Chip Model

Different batches of development boards may use different USB-to-serial chips, commonly **CP210x** (Silicon Labs) or **CH340** (WCH). You can identify it as follows:

- **Check Device Manager**: Right-click the Start menu → "Device Manager", and compare the newly added device name before and after plugging in the USB cable:
  - If the name contains `CP210x` or `Silicon Labs` → install the [CP210x driver](#cp210x-driver-silicon-labs)
  - If the name contains `CH340`, `USB-Serial`, or `USB2.0-Serial` → install the [CH340 driver](#ch340-driver-wch)
- **Check the chip marking on the board**: Look directly at the marking on the surface of the chip near the USB connector on the development board (e.g. `CP2102`, `CH340C`).

> ℹ️ **Note**
>
> If you are unsure of the chip model, installing both drivers will not cause any conflict.

## Step 2: Download and Install the Driver

### CP210x Driver (Silicon Labs)

1. Open the official Silicon Labs download page: [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers)
2. Download the **CP210x Windows Drivers** package and extract it
3. Run the installer matching your system architecture (run `CP210xVCPInstaller_x64.exe` on a 64-bit system) and follow the prompts to complete the installation

### CH340 Driver (WCH)

1. Open the official WCH download page: [CH341SER.EXE - Driver](https://www.wch.cn/downloads/ch341ser_exe.html) (CH341SER supports both CH340 / CH341, and Windows 11 / 10 / 8.1 / 8 / 7)
2. Download `CH341SER.EXE`
3. Double-click to run it, click the "Install" button, and finish when the "installation successful" prompt appears

> ⚠️ **Caution**: Be sure to download the drivers from the official pages above. Driver packages from third-party download sites may bundle unrelated software or be outdated.

## Step 3: Confirm the Installation

1. Unplug and replug the USB data cable
2. Open Device Manager and expand "Ports (COM & LPT)" — you should see an entry similar to:
   - `Silicon Labs CP210x USB to UART Bridge (COM3)`
   - `USB-SERIAL CH340 (COM4)`
3. Note down the COM port number and re-run the flashing script. If there are multiple COM ports on the PC, you can specify one manually:

```powershell
# Replace COM3 with the actual port number shown in Device Manager
.\flash_release.ps1 -Ports COM3
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Still no COM port after installing the driver | Try a different USB data cable (make sure it is a data cable, not a charge-only cable); try a different USB port (connect directly to the PC, avoid USB HUBs) |
| Device still shows a yellow exclamation mark | In Device Manager, right-click the device → "Uninstall device", then unplug and replug the USB cable; restart the PC if necessary |
| Multiple COM ports, unsure which one | Unplug the development board to see which COM port disappears, then plug it back in to confirm |
| Port appears but flashing fails | Retry with a lower baud rate: `.\flash_release.ps1 -Baud 460800`; or hold the **BOOT** button and press the **EN** button once to enter flashing mode |

## Related Links

- [IO Board Firmware](/fourier-grx-M4/docs/en/release/ioboard): Firmware version list and flashing instructions
