---
layout: default
title: 系统烧录镜像
nav_order: 1.1
parent: 快速开始
has_toc: true
---

# 系统烧录镜像

* TOC
{:toc}

> ℹ️ **说明**
>
> 本页面适用于控制板卡为 **LubanCat-RK3588**（鲁班猫）的机器人机型，包括 M4L V3 及后续版本（M4LP1、M4LT1、M4LT2 等）：
>
> - **M4LT2**：最新机型，搭载 **2.5 代 FSA 执行器**。
> - **M4LT1**：搭载 **2.0 代 FSA 执行器**。
> - **M4LP1**：搭载旧版 **1.0 代 FSA 执行器**，通过软件升级适配 2.0 代接口。
>
> 出厂时控制板卡已预装系统镜像，**正常情况下无需重新烧录**。仅在系统损坏或需要更换镜像版本时，才需要执行本页面的操作。

## 视频教程

以下视频教程演示了完整的 Ubuntu 系统烧录流程。

<video controls style="width: 360px; max-width: 100%;">
  <source src="/fourier-grx-M4/assets/videos/video_install_ubuntu.mp4" type="video/mp4">
  您的浏览器不支持 HTML5 视频标签。
</video>

## 工具获取与安装

烧录镜像到板卡 eMMC 需要在 **Windows 电脑** 上安装以下工具：

- **DriverAssistant**：RK 系列板卡 USB 驱动程序
- **RKDevTool**：瑞芯微专用 USB 烧录工具

点击链接下载：[百度网盘](https://pan.baidu.com/s/19t8AZV9SYTdjn2uObBiSGA)（提取码：`hslu`）

**快速下载：**

| 文件 | 链接 |
|------|------|
| Ubuntu 22.04 系统镜像 | [20260114_ubuntu-22.04-desktop-arm64-lubancat-4.img.xz](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/20260114_ubuntu-22.04-desktop-arm64-lubancat-4.img.xz) |
| RKDevTool v3.15（含 DriverAssistant）| [RKDevTool_v3.15_for_window.zip](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/RKDevTool_v3.15_for_window.zip) |
| network scanner IP 扫描脚本 | [network_scanner.ps1](/fourier-grx-M4/assets/scripts/network_scanner.ps1) |

### 安装 DriverAssistant

解压 DriverAssistant 压缩包，双击 `DriverInstall.exe` 进入驱动安装界面，点击 **驱动安装** 开始安装。

> ℹ️ 若不确定是否已安装旧版驱动，建议先点击 **驱动卸载** 移除旧版本，再重新安装。

### 安装 RKDevTool

解压压缩包后无需安装，直接双击 `RKDevTool.exe` 即可打开软件。软件界面包含三个功能区：**下载镜像**、**升级固件** 和 **高级功能**。

---

## MASKROM 模式烧录

> ⚠️ **注意**
>
> Ubuntu 22.04 镜像必须通过 **MASKROM 模式**烧录，适用于一切场景，包括板卡未烧录系统或系统已损坏无法启动的情况。

### 进入 MASKROM 模式

LubanCat-RK3588 板卡上有一个 **MASKROM 按键**，按照以下步骤让板卡进入烧录模式：

1. 准备一根 **Type-C 数据线**（用于镜像烧录）和一根**供电线**。
2. 断开所有可能给板卡供电的连接线。
3. 使用 Type-C 数据线，一端连接板卡的 **OTG 接口**，另一端连接 Windows 电脑的 USB 接口。
4. 打开 **RKDevTool** 烧录工具。
5. 按住 **MASKROM 按键**，然后用供电线为板卡上电。

   板卡上的 MASKROM 按键位置如下图所示：

   ![MASKROM 按键位置](https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/_images/3588-flash-3.png)

6. 等待 RKDevTool 提示 **"发现一个MASKROM设备"** 后，松开按键。
7. 若未成功识别，重复第 2～6 步。

### 烧录步骤

Ubuntu 22.04 镜像使用 **下载镜像** 模式烧录，需要额外提供 Loader 文件：

1. 成功识别到 MASKROM 设备后，切换到软件的 **下载镜像** 标签页。
2. 确认列表中有 `rkbin` 和 `firmware` 两行（如没有，可手动添加）：
   - **rkbin**：选择工具目录内自带的 `rk3588_MiniLoaderAll.bin` 文件作为 rkbin（Bootloader）。
   - **firmware**：选择下载好的镜像文件（压缩包 `*.xz` 需先解压为 `.img` 格式）。
3. 勾选底部的 **"强制按地址写"** 选项。

   烧写地址配置界面如下图所示：

   ![下载镜像配置界面](https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/_images/MR-5.png)

4. 点击 **执行**，等待烧录完成。

---

## 常见问题

**Q：电脑没有识别到设备怎么办？**

A：请确认已正确安装 DriverAssistant 驱动，并使用具有数据传输功能的 Type-C 数据线连接板卡 OTG 接口。若仍无法识别，可尝试卸载旧驱动后重新安装，或更换 USB 端口。

**Q：运行 `network_scanner.ps1` 时提示无法加载脚本怎么办？**

A：这是 Windows PowerShell 权限不足导致的常见问题。请关闭当前窗口，使用**管理员权限**重新打开 PowerShell 后，再执行脚本。

![PowerShell 权限报错示例](/fourier-grx-M4/assets/images/powershell_error.png)

**Q：鲁班猫已经装到设备上了，但还没有配置 IP，使用 `network_scanner.ps1` 也扫描不到，怎么办？**

A：这种情况通常无法通过局域网脚本直接发现设备。建议先将鲁班猫从设备上拆下，使用电脑网线**直连板卡**，先完成 IP 配置；确认可以正常通信后，再重新装回设备。

---

## 参考资源

- [野火 RK3588 快速入门 — 烧录镜像](https://doc.embedfire.com/linux/rk3588/quick_start/zh/latest/quick_start/flash1_img/flash1_img.html)
