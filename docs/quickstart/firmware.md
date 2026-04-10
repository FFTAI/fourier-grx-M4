---
layout: default
title: 固件安装和更新
nav_order: 1.2
parent: 快速开始
has_toc: true
---

# 固件安装和更新

* TOC
{:toc}

> ℹ️ **说明**
>
> 本页面用于说明 Fourier-GRX-M4 SDK 的**固件安装、升级和首次型号配置**流程。
> 固件安装包请从 [固件发布](/fourier-grx-M4/docs/release) 页面获取。

## 视频教程

以下视频教程演示了完整的 `fourier-grx` 固件安装流程。

<video controls style="width: 100%; max-width: 800px;">
  <source src="/fourier-grx-M4/assets/videos/video_install_fourier_grx.mp4" type="video/mp4">
  您的浏览器不支持 HTML5 视频标签。
</video>

## 安装前准备

在开始安装前，请先确认以下条件：

- 已从 [固件发布](/fourier-grx-M4/docs/release) 页面下载对应版本的安装包
- 机器人主控电脑可以正常进入系统
- 建议使用**有线网络**连接，并确保设备可以联网
- 如果当前使用有线网络，请先将机器人的网络配置为 **DHCP 自动获取 IP 地址** 模式

> ℹ️ **说明**
>
> 安装程序执行过程中，会自动将机器人的有线网络配置为**静态 IP 地址模式**，以便程序后续能够正常运行。

## 安装步骤

下载完成后，按照以下步骤完成安装。

### 下载 `fourier-grx` 程序包

如果机器人主控电脑已经联网，也可以直接使用 `wget` 下载程序包。下面给出一个示例：

```bash
# 下载 fourier-grx 程序包（示例版本）
wget https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.1-linux-arm64-cpu-m4l-blaze.deb
```

> ℹ️ **说明**
>
> - 请根据 [固件发布](/fourier-grx-M4/docs/release) 页面中的最新版本链接，替换为实际需要下载的版本。
> - 如果已经提前手动下载好 `.deb` 安装包，可直接跳过此步骤。

### 安装 `fourier-grx` 程序包

```bash
# 安装 fourier-grx-xxx.deb 文件，安装完后系统中会提供 fourier-grx 程序工具
sudo dpkg -i fourier-grx-xxx.deb  # xxx 为具体版本号
```

### 安装运行所需内容

```bash
# 安装 fourier-grx 完整内容
fourier-grx install
```

> ℹ️ **说明**
>
> - 如果安装过程中由于网络或其他原因失败，可以重新运行上述安装命令。
> - 首次安装和版本升级都可以参考本页面执行。

## 机器人型号配置

安装过程中，会要求输入机器人型号。请根据实际机器人型号进行配置。

### 新版支持的型号

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

### 运行模式说明

> ℹ️ **说明**
>
> - 上表中的**开发者模式**（`sdk`）仅供二次开发使用，适用于通过 SDK 接口进行自定义开发的场景。
> - 对于**正式发布的机器**，应将运行模式配置为**发布模式**（`release`），以便通过上位机进行机器人控制。
> - 可通过 `fourier-grx config` 修改运行模式，详见 [运行模式](/fourier-grx-M4/docs/reference/run_type) 参考页。

### 重新配置与结果确认

如果配置过程中选择错误，可重新执行以下命令：

```bash
# 重新配置机器人型号或运行模式
fourier-grx config

# 查看当前配置信息
fourier-grx list
```

## 旧版 `fourier-m4` 安装方式（已废弃）

> ⚠️ **已废弃**：以下为旧版 `fourier-m4` 软件的安装方式，已停止积极维护。

```bash
# Fourier-M4 安装（旧版）
# 安装 fourier-m4-xxx.deb 文件，安装完后系统中会提供 fourier-m4 程序工具
sudo dpkg -i fourier-m4-xxx.deb  # xxx 为具体版本号

# 安装 fourier-m4 完整内容
fourier-m4 install
```

> ⚠️ **已废弃**：以下为旧版 `fourier-m4` 软件支持的机器人型号，已停止积极维护。

### 旧版支持型号

| 机器人型号 | 机器人版本 | 适配的机器人型号                                       |
|-------|-------|------------------------------------------------|
| M4L   | V2    | M4 8电机版本 傅利叶智能自研执行器V1版本，使用 RK3399 嵌入式板卡        |
| M4L   | V3    | M4 8电机版本 傅利叶智能自研执行器V1版本，使用 RK3588 嵌入式板卡（鲁班猫板卡） |

> ℹ️ **说明**
>
> `fourier-m4` 是 `fourier-grx` 的前置版本程序，简称 “旧版”，目前已不再积极维护。如果设备支持新版的 `fourier-grx`， 建议使用 `fourier-grx` 进行安装和使用。
