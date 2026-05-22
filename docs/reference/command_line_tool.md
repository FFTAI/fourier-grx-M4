---
layout: default
title: 命令行工具
nav_order: 3.7
parent: 参考指南
has_toc: true
---

# 命令行工具

在完成 Fourier-GRX-M4 SDK 的安装后，用户可以使用命令行工具 `fourier-grx` 来管理和控制机器人。

`fourier-grx` 是 Fourier-GRX-M4 SDK 的命令行工具，用于安装、配置和控制 Fourier M4 机器人。

通过在终端运行 `fourier-grx` 命令，会在终端中显示可用的子命令列表和帮助信息。

目前，支持的命令行工具子命令包括：

| 子命令               | 说明                                             |
|-------------------|------------------------------------------------|
| `version`         | 显示当前 Fourier-GRX-M4 SDK 的版本信息                  |
| `install`         | 安装 Fourier-GRX-M4 SDK 运行环境和依赖库                 |
| `uninstall`       | 卸载 Fourier-GRX-M4 SDK 运行环境和依赖库                 |
| `config`          | 配置 Fourier-GRX-M4 SDK 的启动参数                    |
| `list`            | 列出 Fourier-GRX-M4 SDK 的启动参数                    |
| `start`           | 启动 Fourier-GRX-M4 SDK 运行环境和机器人                 |
| `stop`            | 停止 Fourier-GRX-M4 SDK 运行环境和机器人 （强制杀死相关进程）      |
| `enable_service`  | 启用 Fourier-GRX-M4 SDK 的服务功能，电脑重启后会自动启动机器人控制程序  |
| `disable_service` | 禁用 Fourier-GRX-M4 SDK 的服务功能，电脑重启后不会自动启动机器人控制程序 |
| `background`      | 将 Fourier-GRX-M4 SDK 运行环境和机器人程序放到后台运行          |
| `setup_conda`     | 创建用于 Fourier-GRX-M4 SDK 的 Conda 环境，并安装所需的依赖库   |
| `update`          | 检查服务器上是否有新版本的软件包，并交互式地选择版本进行安装         |

---

## `fourier-grx update` 详细说明

`update` 命令用于从 Fourier 服务器检查是否有更新版本的软件包可用，并引导用户完成下载和安装。

### 用法

```bash
fourier-grx update                    # 自动检测当前安装包的变体并检查更新
fourier-grx update <variant>          # 手动指定变体（适用于旧版已安装包）
fourier-grx update --help             # 显示帮助信息
```

其中 `<variant>` 为软件包的平台/机型标识符，例如 `linux-arm64-cpu-m4l-blaze`。

### 运行流程

1. 读取当前已安装版本号和变体信息
2. 向服务器探测可用的新版本（通过 HTTP HEAD 请求逐版本探测）
3. 列出所有可用的更新版本，并标注最新版本
4. 提示用户选择要安装的版本编号（直接回车默认安装最新版本，输入 `n` 取消）
5. 下载所选版本的 `.deb` 软件包
6. 使用 `sudo dpkg -i` 完成安装

### 示例输出

```
当前版本 / Current version : 4.4.4
当前变体 / Current variant  : linux-arm64-cpu-m4l-blaze
正在检查更新... / Checking for updates...

发现以下新版本 / Found the following newer versions:
----------------------------------------------------
  [1] v4.4.5  fourier-grx-4.4.5-linux-arm64-cpu-m4l-blaze.deb
  [2] v4.4.6  fourier-grx-4.4.6-linux-arm64-cpu-m4l-blaze.deb
  [3] v4.4.7  fourier-grx-4.4.7-linux-arm64-cpu-m4l-blaze.deb  ← 最新 latest
----------------------------------------------------

请选择要安装的版本编号（直接回车安装最新 [2]，输入 n 取消）:
```

### 安装完成后

安装完成后需运行以下命令完成全部安装过程：

```bash
fourier-grx install
```

### 注意事项

- **旧版已安装包**：4.4.4 及更早版本的安装包不包含变体信息，需手动传入变体参数，例如：
  ```bash
  fourier-grx update linux-arm64-cpu-m4l-blaze
  ```
  升级到新版本后，后续执行 `fourier-grx update` 即可自动识别变体，无需再手动指定。

- **网络要求**：更新过程需要访问 Fourier 软件包服务器，请确保网络连接正常。

- **权限要求**：安装步骤需要 `sudo` 权限，系统会提示输入密码。