---
layout: default
title: 固件安装和更新
nav_order: 1.4
parent: 快速开始
has_toc: true
---

# 固件安装和更新

* TOC
{:toc}

以下视频教程演示了完整的 `fourier-grx` 固件安装流程。

<video controls style="width: 100%; max-width: 800px;">
  <source src="/fourier-grx-M4/assets/videos/video_install_fourier_grx.mp4" type="video/mp4">
  您的浏览器不支持 HTML5 视频标签。
</video>

Fourier-GRX-M4 SDK 安装文件请从 [固件更新](/fourier-grx-M4/docs/update) 下载。
下载完后，运行下面的指令完成安装过程：

> ⚠️ **已废弃（Deprecated）**：以下为旧版 `fourier-m4` 软件的安装方式，已停止积极维护。

```bash
# Fourier-M4 安装 (旧版)
# 安装 fourier-m4-xxx.deb 文件，安装完后系统中会提供 fourier-m4 程序工具
sudo dpkg -i fourier-m4-xxx.deb  # xxx 为具体版本号

# 安装 fourier-m4 完整内容
fourier-m4 install
```

```bash
# Fourier-GRX 安装 (新版)
# 安装 fourier-grx-xxx.deb 文件，安装完后系统中会提供 fourier-grx 程序工具
sudo dpkg -i fourier-grx-xxx.deb  # xxx 为具体版本号

# 安装 fourier-grx 完整内容
fourier-grx install
```

> ℹ️ **说明**：
>
> - 安装过程中如果由于网络或其他原因导致安装失败，可以重新运行上面的安装指令。
> - 建议使用有线网络连接。
> - 如果使用有线网络连接，需要先将机器人的网络配置为 DHCP 自动获取 IP 地址模式，以使设备能够正常联网。
> - 安装程序过程中，会自动将机器人的有线网络配置为静态 IP 地址模式，以便程序后续能够正常运行。

安装过程中，会要求输入机器人型号，请根据实际机器人型号进行配置，目前支持的型号如下：

> ⚠️ **已废弃（Deprecated）**：以下为旧版 `fourier-m4` 软件支持的机器人型号，已停止积极维护。

`Fourier-M4 (旧版)` 机器人型号的配置选项：

| 机器人型号 | 机器人版本 | 适配的机器人型号                                       |
|-------|-------|------------------------------------------------|
| M4L   | V2    | M4 8电机版本 傅利叶智能自研执行器V1版本，使用 RK3399 嵌入式板卡        |
| M4L   | V3    | M4 8电机版本 傅利叶智能自研执行器V1版本，使用 RK3588 嵌入式板卡（鲁班猫板卡） |

`Fourier-GRX (新版)` 机器人型号的配置选项：

| 机器人型号 | 机器人版本 | 测试机型 | [运行模式](/fourier-grx-M4/docs/reference/run_type) | 适配的机器人型号 |
|-------|-------|------|-------------------------------------------------|----------|
| M4    | T1    | 否    | 开发者模式                                           | M4T1     |
| M4L   | T1    | 否    | 开发者模式                                           | M4LT1    |
| M4L   | T2    | 否    | 开发者模式                                           | M4LT2    |
| M4L   | P1    | 否    | 开发者模式                                           | M4LP1    |

> ℹ️ **机器人型号说明**
>
> - **M4LT2**：最新机型，搭载 **2.5 代 FSA 执行器**。
> - **M4LT1**：搭载 **2.0 代 FSA 执行器**。
> - **M4LP1**：搭载旧版 **1.0 代 FSA 执行器**，通过软件升级适配 2.0 代接口。

> ℹ️ **运行模式说明**
>
> - 上表中的**开发者模式**（`sdk`）仅供二次开发使用，适用于通过 SDK 接口进行自定义开发的场景。
> - 对于**正式发布的机器**，应将运行模式配置为**发布模式**（`release`），以便通过上位机进行机器人控制。
> - 可通过 `fourier-grx config` 修改运行模式，详见 [运行模式](/fourier-grx-M4/docs/reference/run_type) 参考页。

如若配置错误，可运行 `fourier-grx config` 进行重新配置。当前的配置信息可以通过 `fourier-grx list` 查看。

> ℹ️ **说明**
>
> `fourier-m4` 是 `fourier-grx` 的前置版本程序，简称 “旧版”，目前已不再积极维护。如果设备支持新版的 `fourier-grx`， 建议使用 `fourier-grx` 进行安装和使用。
