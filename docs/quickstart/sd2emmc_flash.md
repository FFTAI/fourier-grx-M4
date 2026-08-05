---
layout: default
title: SD 卡批量烧录（sd2emmc）
nav_order: 1.15
parent: 快速开始
has_toc: true
---

# SD 卡批量烧录（sd2emmc）

* TOC
{:toc}

> ℹ️ **说明**
>
> 本页面适用于需要**批量烧录** LubanCat-RK3588 板卡 eMMC 的场景（如产线、多台设备）。通过一张 SD 卡即可自动完成 eMMC 刷写，无需 Windows 电脑和 RKDevTool。
>
> 单台设备的常规烧录（MASKROM 模式）请参考 [系统烧录镜像](/fourier-grx-M4/docs/quickstart/flash_image)。

## 镜像下载

| 文件 | 链接 |
|------|------|
| Ubuntu 22.04 sd2emmc 烧录镜像 | [20260805_ubuntu-22.04-desktop-arm64-lubancat-4-sd2emmc.img.xz](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/20260805_ubuntu-22.04-desktop-arm64-lubancat-4-sd2emmc.img.xz) |

> ℹ️ 该镜像具备 20260805 版本的全部特性：自动配置静态 IP `192.168.137.220`、内置 Web 终端（<http://192.168.137.220:7681>）。

## 使用方法

### 1. 写入 SD 卡

准备一张容量 **≥ 16 GB** 的 SD 卡，任选一种方式写入镜像：

- **balenaEtcher**（Windows / macOS / Linux 图形界面）：选择镜像文件（`.xz` 无需解压）→ 选择 SD 卡 → Flash；
- **命令行（Linux）**：

```bash
xzcat 20260805_ubuntu-22.04-desktop-arm64-lubancat-4-sd2emmc.img.xz | sudo dd of=/dev/sdX bs=4M status=progress
```

> ⚠️ **注意**：请将 `/dev/sdX` 替换为实际的 SD 卡设备名（可通过 `lsblk` 确认），写错设备会覆盖其他磁盘数据。

### 2. 插卡上电，自动刷写 eMMC

1. 将 SD 卡插入板卡并上电；
2. 系统启动后自动开始刷写 eMMC，期间可用浏览器打开 Web 终端 <http://192.168.137.220:7681>，执行以下命令实时查看进度：

```bash
journalctl -fu emmc-flash.service
```

### 3. 完成

- **板子自动关机 = 刷机成功**；
- 拔出 SD 卡，重新上电即可进入新系统。

## 失败处理与注意事项

- **刷机失败不会写坏设备**：如果刷写失败（例如找不到 eMMC、载荷校验失败），`emmc-flash.service` 会放弃刷写并在日志中说明原因，不会写坏任何设备。
- **引导顺序**：RK3588 的 BootROM 优先从 eMMC 引导，这套流程对**空 eMMC 的新板子**最可靠；如果某块板子的 eMMC 中已有系统、导致 SD 卡抢不到引导，需要先进入 MASKROM 模式擦除 eMMC 的 bootloader，再用 SD 卡刷写（MASKROM 操作见 [系统烧录镜像](/fourier-grx-M4/docs/quickstart/flash_image)）。

## 相关链接

- [系统烧录镜像](/fourier-grx-M4/docs/quickstart/flash_image)：单台设备常规烧录（MASKROM 模式）
- [网络连接与远程登录](/fourier-grx-M4/docs/usage/network_connection)：静态 IP 与 Web 终端说明
