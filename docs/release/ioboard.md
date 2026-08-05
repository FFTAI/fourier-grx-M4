---
layout: default
title: IO Board 固件
parent: 固件发布
nav_order: 3
has_toc: true
---

# IO Board 固件

* TOC
{:toc}

## 版本列表

| 发布日期 | 版本 | 下载 | 更新内容 | 支持状态 |
|----------|------|------|----------|----------|
| 2026-07-21 | **1.0.0.3** | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.3_20260721.zip) | [详情](#1003) | ✅ 支持中 |
| 2026-05-12 | 1.0.0.2 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.2_20260512.zip) | [详情](#1002) | ✅ 支持中 |

## 烧录方法

从上方下载对应版本的 zip 包，解压后按照包内说明完成烧录：

- **1.0.0.3 及以后**：双击 `1_Setup_Flash_Env.bat` 安装环境（仅首次），再双击 `2_Flash_Firmware.bat` 一键烧录。`.bat` 启动器会自动解除文件下载阻止标记，执行完毕后窗口保持打开，方便查看结果。也可以直接在 PowerShell 中运行 `setup_release_env.ps1` 和 `flash_release.ps1`。快速开始见包内 `README.txt`，完整说明（中英双语）见 `RELEASE.md`。
- **1.0.0.2**：按照包内 `RELEASE.md` 的说明，在 PowerShell 中运行 `setup_release_env.ps1` 和 `flash_release.ps1` 完成烧录。

环境要求：Windows 10 / 11，PowerShell 5.1 或更高版本，USB 数据线连接开发板。

> ℹ️ **说明**
>
> 如果烧录脚本提示 `No serial ports detected`，或设备管理器中没有出现 COM 口，说明电脑未安装 USB 转串口驱动，请参考 [Windows 串口驱动安装](/fourier-grx-M4/docs/faq/serial_driver) 页面安装驱动后重试。

硬件平台：ESP32-WROOM-32D

---

## 更新内容

### 1.0.0.3

> 📅 2026-07-21 &nbsp;·&nbsp; 平台：ESP32-WROOM-32D

🔧 **修改**

- **急停按键消抖**：GPIO 34 新增 50ms 软件消抖，防止机械抖动引发 TRIGGERED / released 反复打印

📦 **安装包改进**

- 新增 `1_Setup_Flash_Env.bat` / `2_Flash_Firmware.bat` 双击启动器：自动解除 PowerShell 脚本下载阻止标记，执行完毕后窗口保持打开
- 新增 `README.txt` 快速开始说明，`RELEASE.md` 改为中英双语
- 环境安装脚本增强：Python 安装失败时输出具体原因（无网络 / 防火墙拦截 / Windows"应用执行别名"拦截等）

---

### 1.0.0.2

> 📅 2026-05-12 &nbsp;·&nbsp; 平台：ESP32-WROOM-32D

- 初始稳定版本
- 急停按键（GPIO 34）触发时切断 38V 继电器
- 电源按键（GPIO 35）本地开关机，带 5V 延时断电
- WS2812B LED 灯条电量柱状图显示
- UDP JSON API 远程读写控制
- HTTP OTA 固件升级支持
