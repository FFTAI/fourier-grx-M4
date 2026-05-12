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
| 2026-05-12 | **1.0.0.3** | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.3_20260512.zip) | [详情](#1003) | ✅ 支持中 |
| 2026-05-12 | 1.0.0.2 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.2_20260512.zip) | [详情](#1002) | ✅ 支持中 |

## 烧录方法

从上方下载对应版本的 zip 包，解压后按照包内 `RELEASE.md` 的说明运行 `setup_release_env.ps1` 和 `flash_release.ps1` 完成烧录。

硬件平台：ESP32-WROOM-32D

---

## 更新内容

### 1.0.0.3

> 📅 2026-05-12 &nbsp;·&nbsp; 平台：ESP32-WROOM-32D

🔧 **修改**

- **急停按键消抖**：GPIO 34 新增 50ms 软件消抖，防止机械抖动引发 TRIGGERED / released 反复打印

---

### 1.0.0.2

> 📅 2026-05-12 &nbsp;·&nbsp; 平台：ESP32-WROOM-32D

- 初始稳定版本
- 急停按键（GPIO 34）触发时切断 38V 继电器
- 电源按键（GPIO 35）本地开关机，带 5V 延时断电
- WS2812B LED 灯条电量柱状图显示
- UDP JSON API 远程读写控制
- HTTP OTA 固件升级支持
