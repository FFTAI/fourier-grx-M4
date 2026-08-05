---
layout: default
title: Windows 串口驱动安装
nav_order: 6.7
parent: 常见问题
has_toc: true
---

# Windows 串口驱动安装

* TOC
{:toc}

> ℹ️ **说明**
>
> 本页面用于说明在 **Windows 电脑**上安装 USB 转串口驱动（CP210x / CH340）的方法。
>
> 烧录 [IO Board 固件](/fourier-grx-M4/docs/release/ioboard) 时，电脑通过开发板上的 USB 转串口芯片与 ESP32 通信。如果电脑没有安装对应驱动，系统不会生成 COM 串口，烧录脚本会提示 `No serial ports detected`，导致烧录失败。

## 什么时候需要安装驱动

出现以下任一情况时，说明电脑可能未安装串口驱动：

- 烧录脚本（`flash_release.ps1` / `2_Flash_Firmware.bat`）提示 `No serial ports detected`
- 用 USB 连接开发板后，设备管理器的"端口 (COM 和 LPT)"下**没有**出现新的 COM 口
- 设备管理器中出现带 ⚠️ 黄色感叹号的未知设备，名称类似 `USB-Serial Controller`、`USB2.0-Serial` 或 `CP2102 USB to UART Bridge Controller`

## 第一步：确认 USB 转串口芯片型号

不同批次的开发板使用的 USB 转串口芯片可能不同，常见为 **CP210x**（Silicon Labs）或 **CH340**（沁恒 WCH）两种。可通过以下方式确认：

- **查看设备管理器**：右键开始菜单 → "设备管理器"，在插入 USB 前后对比新增的设备名称：
  - 名称中包含 `CP210x`、`Silicon Labs` → 安装 [CP210x 驱动](#cp210x-驱动silicon-labs)
  - 名称中包含 `CH340`、`USB-Serial`、`USB2.0-Serial` → 安装 [CH340 驱动](#ch340-驱动沁恒-wch)
- **查看开发板芯片丝印**：直接查看开发板上 USB 接口附近芯片表面的丝印（如 `CP2102`、`CH340C`）。

> ℹ️ **说明**
>
> 如果不确定芯片型号，两个驱动都安装也不会有冲突。

## 第二步：下载并安装驱动

### CP210x 驱动（Silicon Labs）

1. 打开 Silicon Labs 官方下载页面：[CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers)
2. 下载 **CP210x Windows Drivers** 压缩包并解压
3. 根据系统位数运行安装程序（64 位系统运行 `CP210xVCPInstaller_x64.exe`），按提示完成安装

### CH340 驱动（沁恒 WCH）

1. 打开沁恒官方下载页面：[CH341SER.EXE - 驱动程序](https://www.wch.cn/downloads/ch341ser_exe.html)（CH341SER 同时支持 CH340 / CH341，支持 Windows 11 / 10 / 8.1 / 8 / 7）
2. 下载 `CH341SER.EXE`
3. 双击运行，点击"安装"按钮，弹出"安装成功"提示后完成

> ⚠️ **注意**：请务必从上述官方页面下载驱动，第三方下载站的驱动安装包可能捆绑无关软件或版本过旧。

## 第三步：确认安装成功

1. 重新拔插 USB 数据线
2. 打开设备管理器，展开"端口 (COM 和 LPT)"，应能看到类似以下条目：
   - `Silicon Labs CP210x USB to UART Bridge (COM3)`
   - `USB-SERIAL CH340 (COM4)`
3. 记下 COM 端口号，重新运行烧录脚本即可。如果电脑上有多个 COM 口，可以手动指定：

```powershell
# 将 COM3 替换为设备管理器中实际显示的端口号
.\flash_release.ps1 -Ports COM3
```

## 常见问题排查

| 问题 | 解决方法 |
|------|----------|
| 安装驱动后仍没有 COM 口 | 更换 USB 数据线（确认是数据线而非仅充电线）；换一个 USB 接口（建议直连电脑，不要经过 USB HUB） |
| 设备仍有黄色感叹号 | 在设备管理器中右键该设备 → "卸载设备"，重新拔插 USB；必要时重启电脑 |
| 有多个 COM 口，不确定是哪个 | 拔下开发板看哪个 COM 口消失，再插回确认 |
| 端口出现但烧录失败 | 降低波特率重试：`.\flash_release.ps1 -Baud 460800`；或按住 **BOOT** 键再按一下 **EN** 键进入烧录模式 |

## 相关链接

- [IO Board 固件](/fourier-grx-M4/docs/release/ioboard)：固件版本列表与烧录方法
