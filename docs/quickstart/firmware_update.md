---
layout: default
title: 固件更新
nav_order: 1.3
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
| 机器人型号配置 | 需要逐项交互选择 | 会先读取 `~/fourier-grx-bak` 中的旧配置并询问是否沿用，直接回车即沿用 |

> ⚠️ **注意**
>
> - `fourier-grx update` 只完成 `dpkg` 层的包安装，真正生效要靠 `fourier-grx install` 把新版本部署到 `~/fourier-grx/`。**两步都要做**，详见上文[安装的两个层次](/fourier-grx-M4/docs/reference/command_line_tool#安装的两个层次)。
> - `fourier-grx install` 会先把现有的 `~/fourier-grx` 备份为 `~/fourier-grx-bak`（旧备份被覆盖），再解压新版本。
> - `fourier-grx install` 无论首次安装还是更新，都会**无条件重跑网络配置脚本** `setup_static_ipv4.sh`，把有线网口重置为静态 IP `192.168.137.220/24`、网关 `192.168.137.1`、DNS `8.8.8.8,8.8.4.4`。如果此前手动改过这些参数，请先记录下来，更新后重新配置。
> - `fourier-grx update` 命令需要设备可以访问外网（用于探测云端最新版本），如果当前静态 IP 网络配置的网关 / DNS 无法访问外网，请改用[手动下载安装包](#方式二手动下载安装包)的方式，或参考 [网络连接与远程登录](/fourier-grx-M4/docs/usage/network_connection) 页面，通过笔记本/平板共享 WiFi 网络临时给机器人接入外网。

## 更新前准备

- 确认设备当前可以正常运行 `fourier-grx`（已完成过首次安装）
- 确认设备可以访问外网
- 建议先运行 `fourier-grx list` 记录当前的机器人型号、版本和运行模式配置，便于更新后核对：

```bash
fourier-grx list
```

## 方式一：使用 `fourier-grx update` 命令（推荐）

`fourier-grx update` 会自动读取当前安装的版本和机型变体，查询 [固件发布](/fourier-grx-M4/docs/release) 云存储中的发布索引，列出可升级的版本并支持交互式选择安装。

> ℹ️ 自 **v4.4.77** 起，`fourier-grx update` 改为读取发布索引 `manifest.json`：一次请求即可列出该变体的全部后续版本，列表里会标注每个版本的发布性质（**正式版本** / 内测构建 / 预发布），下载后还会按索引记录的 `sha256` 校验再安装。索引读不到时自动退回旧版「按版本号逐个探测」。
>
> 这次改动同时修掉一个升级盲区：旧版探测只看「当前版本号 + 20 个补丁号」，例如停在 4.4.53 的设备最多只能发现 4.4.73，其后的版本永远不会出现在列表里。索引没有这个窗口限制。
>
> 注意：这段逻辑在客户端脚本里，因此**要先用新包完成一次 `dpkg` 安装**才能用到新的检查方式；4.4.77 之前的客户端仍按旧方式探测。

### 列出可升级版本并交互式选择安装

```bash
fourier-grx update
```

执行后会列出该变体下所有比当前更新的版本（按版本号升序，末行标注 `← 最新 latest`），每行附带发布性质标注；输入编号选择安装，直接回车安装最新版本，输入 `n` 取消。

### 直接安装指定版本

如果已经明确知道要安装的版本号（例如从 [固件发布](/fourier-grx-M4/docs/release) 页面查到的版本），可以直接指定：

```bash
fourier-grx update <version>

# 示例
fourier-grx update 4.4.53
```

机型变体会自动从当前已安装的软件包中读取，无需手动指定。

### 安装预发布版本

预发布渠道的构建不会出现在上面的自动探测结果中，只能显式指定版本号和渠道：

```bash
fourier-grx update <version>-prerelease

# 示例
fourier-grx update 4.4.53-prerelease
```

机型部分仍从当前已安装的软件包读取，只有渠道段被替换为 `prerelease`。该语法自 v4.4.53 起可用，更早版本请用 `sudo dpkg -i <deb>` 手动安装。详见 [命令行工具 · 预发布渠道](/fourier-grx-M4/docs/reference/command_line_tool#预发布渠道)。

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
> - `fourier-grx install` 会先询问是否沿用 `~/fourier-grx-bak` 里的旧配置，直接回车即沿用；选 `n` 或不提供时会逐项重新询问机器人型号、版本和运行模式，请按更新前 `fourier-grx list` 记录的配置选择。
> - 如果配置选择错误，可随时重新运行 `fourier-grx config` 修正，详见下方[重新配置与结果确认](#重新配置与结果确认)。

## 方式二：手动下载安装包

如果设备暂时无法访问外网（`fourier-grx update` 探测失败），或需要安装指定的历史版本，可以手动下载 `.deb` 安装包完成更新，流程与首次安装基本一致，只是**无需再处理网络配置**（已经是静态 IP）。

### 下载 `fourier-grx` 程序包

```bash
# 下载 fourier-grx 程序包（示例版本）
wget https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.53-linux-arm64-cpu-m4l-blaze.deb
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

同样地，此步骤会先把现有的 `~/fourier-grx` 备份为 `~/fourier-grx-bak`，再询问是否沿用备份中的机器人型号、版本和运行模式配置；选择重新配置时，请参照更新前记录的配置重新选择。

## 重新配置与结果确认

如果 `fourier-grx install` 过程中机器人型号或运行模式选择错误，可重新执行以下命令：

```bash
# 重新配置机器人型号或运行模式
fourier-grx config

# 查看当前配置信息，核对是否与更新前一致
fourier-grx list

# 查看当前安装的版本号与可追溯信息（v4.4.78 起还会打印分支 / 变体 / 发布性质 / 提交号 / 构建时间）
fourier-grx version
```

```text
version: 4.4.78
branch:  m4-lfs
variant: linux-arm64-cpu-m4l-blaze
release: beta（内测构建 internal build）
commit:  1127cfbbd4fa-clean
built:   2026-11-04T03:27:13Z
```

## 相关链接

- [网络连接与远程登录](/fourier-grx-M4/docs/usage/network_connection)：无路由器环境下，通过笔记本/平板共享网络并 SSH 远程登录机器人主控电脑
- [固件发布](/fourier-grx-M4/docs/release)：查看所有版本及更新内容
- [固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install)：全新设备的完整安装流程
- [运行模式](/fourier-grx-M4/docs/reference/run_type)：开发者模式 / 发布模式说明
