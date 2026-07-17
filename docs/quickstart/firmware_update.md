---
layout: default
title: 固件更新
nav_order: 1.25
parent: 快速开始
has_toc: true
---

# 固件更新

* TOC
{:toc}

> ℹ️ **说明**
>
> 本页面用于说明**已经完成过首次安装**的设备（有线网络已配置为静态 IP，可正常运行 `fourier-grx`）升级到新版本固件的流程。
>
> 如果是**全新设备**或**尚未完成过首次安装**（网络仍为 DHCP 自动获取模式），请参考 [固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install)。

## 与首次安装的区别

固件更新与首次安装的主要流程是一致的（下载 `.deb` → `dpkg -i` → `fourier-grx install`），但有以下几点不同：

| 项目 | 首次安装 | 固件更新 |
|------|----------|----------|
| 网络前提 | 默认 **DHCP**，安装程序会自动切换为静态 IP | 默认**已经是静态 IP**（`192.168.137.220/24`），无需再切换 |
| 获取安装包 | 手动下载 / `wget`，或从其他设备拷贝 | 可直接使用 `fourier-grx update` 命令自动探测、下载并安装新版本 |
| 机器人型号配置 | 需要首次输入 | `fourier-grx install` 仍会重新询问一次，请提前用 `fourier-grx list` 记录当前配置，升级后按相同选项重新填写 |

> ⚠️ **注意**
>
> - `fourier-grx install` 无论是首次安装还是更新，都会**重新执行网络配置脚本**（`setup_static_ipv4.sh`）以及机器人型号 / 版本 / 运行模式的交互式配置。如果之前手动修改过静态 IP 地址（非默认的 `192.168.137.220`），会被重置为默认值，请更新前留意确认。
> - `fourier-grx update` 命令需要设备可以访问外网（用于探测云端最新版本），如果当前静态 IP 网络配置的网关 / DNS 无法访问外网，请改用[手动下载安装包](#方式二手动下载安装包)的方式。

## 更新前准备

- 确认设备当前可以正常运行 `fourier-grx`（已完成过首次安装）
- 建议先运行 `fourier-grx list` 记录当前的机器人型号、版本和运行模式配置，便于更新后核对：

```bash
fourier-grx list
```

## 方式一：使用 `fourier-grx update` 命令（推荐）

`fourier-grx update` 会自动读取当前安装的版本和机型变体，探测 [固件发布](/fourier-grx-M4/docs/release) 云存储中是否有更新版本，并支持交互式选择安装。

### 自动探测并交互式选择安装

```bash
fourier-grx update
```

执行后会列出探测到的可用新版本（同一 minor 版本的后续 patch、下一 minor 版本、下一 major 版本），可输入编号选择安装，直接回车安装最新版本，输入 `n` 取消。

### 直接安装指定版本

如果已经明确知道要安装的版本号（例如从 [固件发布](/fourier-grx-M4/docs/release) 页面查到的版本），可以直接指定：

```bash
fourier-grx update <version>

# 示例
fourier-grx update 4.4.25
```

机型变体会自动从当前已安装的软件包中读取，无需手动指定。

### 查看命令帮助

```bash
fourier-grx update --help
```

### 完成安装配置

`fourier-grx update` 只负责下载并通过 `dpkg -i` 安装新的 `.deb` 包，**安装完成后仍需运行以下命令完成配置生效**：

```bash
fourier-grx install
```

> ℹ️ **说明**
>
> - `fourier-grx install` 执行过程中会重新询问机器人型号、版本和运行模式，请按照更新前 `fourier-grx list` 记录的配置重新选择，避免配置不一致。
> - 如果配置选择错误，可随时重新运行 `fourier-grx config` 修正，详见下方[重新配置与结果确认](#重新配置与结果确认)。

## 方式二：手动下载安装包

如果设备暂时无法访问外网（`fourier-grx update` 探测失败），或需要安装指定的历史版本，可以手动下载 `.deb` 安装包完成更新，流程与首次安装基本一致，只是**无需再处理网络配置**（已经是静态 IP）。

### 下载 `fourier-grx` 程序包

```bash
# 下载 fourier-grx 程序包（示例版本）
wget https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.25-linux-arm64-cpu-m4l-blaze.deb
```

> ℹ️ **说明**
>
> 请根据 [固件发布](/fourier-grx-M4/docs/release) 页面中的版本链接，替换为实际需要安装的版本。

### 安装 `fourier-grx` 程序包

```bash
sudo dpkg -i fourier-grx-xxx.deb  # xxx 为具体版本号
```

### 安装运行所需内容

```bash
fourier-grx install
```

同样地，此步骤会重新询问机器人型号、版本和运行模式配置，请参照更新前记录的配置重新选择。

## 重新配置与结果确认

如果 `fourier-grx install` 过程中机器人型号或运行模式选择错误，可重新执行以下命令：

```bash
# 重新配置机器人型号或运行模式
fourier-grx config

# 查看当前配置信息，核对是否与更新前一致
fourier-grx list

# 查看当前安装的版本号
fourier-grx version
```

## 相关链接

- [固件发布](/fourier-grx-M4/docs/release)：查看所有版本及更新内容
- [固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install)：全新设备的完整安装流程
- [运行模式](/fourier-grx-M4/docs/reference/run_type)：开发者模式 / 发布模式说明
