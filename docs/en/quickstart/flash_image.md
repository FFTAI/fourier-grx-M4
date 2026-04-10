---
layout: default
title: Flash System Image
nav_order: 1.1
parent: "Quick Start"
has_toc: true
nav_exclude: true
---

# Flash System Image

* TOC
{:toc}

> ℹ️ **Note**
>
> This page applies to robot models whose control board is the **LubanCat-RK3588**, including M4L V3 and later variants (M4LP1, M4LT1, M4LT2, etc.):
>
> - **M4LT2**: The latest model, equipped with **2.5th-generation FSA actuators**.
> - **M4LT1**: Equipped with **2.0th-generation FSA actuators**.
> - **M4LP1**: Equipped with legacy **1.0th-generation FSA actuators**, adapted to the 2.0-generation interface via a software upgrade.
>
> The control board ships with a pre-installed system image. **Under normal circumstances, re-flashing is not required.** Only perform the steps on this page if the system is corrupted or you need to switch to a different image version.

## Obtaining and Installing the Tools

Flashing an image to the board's eMMC requires the following tools installed on a **Windows PC**:

- **DriverAssistant**: USB driver program for RK-series boards
- **RKDevTool**: Rockchip's dedicated USB flashing tool

Download link: [Baidu Netdisk](https://pan.baidu.com/s/19t8AZV9SYTdjn2uObBiSGA) (extraction code: `hslu`)

**Quick Download:**

| File | Link |
|------|------|
| Ubuntu 22.04 system image | [20260114_ubuntu-22.04-desktop-arm64-lubancat-4.img.xz](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/20260114_ubuntu-22.04-desktop-arm64-lubancat-4.img.xz) |
| RKDevTool v3.15 (includes DriverAssistant) | [RKDevTool_v3.15_for_window.zip](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/RKDevTool_v3.15_for_window.zip) |

### Installing DriverAssistant

Extract the DriverAssistant archive, double-click `DriverInstall.exe` to open the driver installation interface, then click **Install Driver** to begin.

> ℹ️ If you are unsure whether an older driver version is already installed, it is recommended to click **Uninstall Driver** first to remove the old version before reinstalling.

### Installing RKDevTool

After extracting the archive, no installation is needed — simply double-click `RKDevTool.exe` to launch the application. The interface contains three functional tabs: **Download Image**, **Upgrade Firmware**, and **Advanced Features**.

---

## Flashing via MASKROM Mode

> ⚠️ **Warning**
>
> The Ubuntu 22.04 image must be flashed using **MASKROM mode**. This method works in all scenarios, including when the board has no system installed or the existing system is corrupted and cannot boot.

### Entering MASKROM Mode

The LubanCat-RK3588 board has a **MASKROM button**. Follow these steps to put the board into flashing mode:

1. Prepare a **Type-C data cable** (for image flashing) and a **power cable**.
2. Disconnect all cables that may supply power to the board.
3. Using the Type-C data cable, connect the board's **OTG port** to a USB port on the Windows PC.
4. Open the **RKDevTool** flashing application.
5. Hold down the **MASKROM button**, then connect the power cable to power on the board.

   The location of the MASKROM button on the board is shown in the image below:

   ![MASKROM button location](https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/_images/3588-flash-3.png)

6. Wait until RKDevTool displays **"Found one MASKROM device"**, then release the button.
7. If the device is not recognized, repeat steps 2–6.

### Flashing Steps

The Ubuntu 22.04 image is flashed using **Download Image** mode, which also requires a Loader file:

1. After the MASKROM device is successfully recognized, switch to the **Download Image** tab in the application.
2. Confirm that the list contains two entries: `rkbin` and `firmware` (add them manually if they are missing):
   - **rkbin**: Select the `rk3588_MiniLoaderAll.bin` file included in the tool directory as the rkbin (Bootloader).
   - **firmware**: Select the downloaded image file (the `*.xz` archive must be extracted to `.img` format first).
3. Check the **"Write by address forcibly"** option at the bottom.

   The address configuration interface is shown in the image below:

   ![Download Image configuration interface](https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/_images/MR-5.png)

4. Click **Execute** and wait for flashing to complete.

---

## Frequently Asked Questions

**Q: The PC does not recognize the device. What should I do?**

A: Confirm that the DriverAssistant driver is correctly installed and that you are using a Type-C data cable with data transfer capability connected to the board's OTG port. If the device is still not recognized, try uninstalling and reinstalling the driver, or try a different USB port.

---

## Reference Resources

- [Embedfire RK3588 Quick Start — Flash Image](https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/quick_start/flash1_img/flash1_img.html)
