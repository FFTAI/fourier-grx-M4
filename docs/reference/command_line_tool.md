---
layout: default
title: 命令行工具
nav_order: 3.7
parent: 参考指南
has_toc: true
---

# 命令行工具

安装 Fourier-GRX-M4 SDK 后，可用命令行工具 `fourier-grx` 管理和控制机器人。

在终端直接运行 `fourier-grx`，会列出全部子命令。支持的子命令如下：

| 子命令               | 说明                                             |
|-------------------|------------------------------------------------|
| `version`         | 显示当前 Fourier-GRX-M4 SDK 的版本信息                  |
| `install`         | 部署 Fourier-GRX-M4 SDK 运行环境，并配置机器人型号与运行模式        |
| `uninstall`       | 删除 `~/fourier-grx` 部署目录                        |
| `config`          | 重新配置 Fourier-GRX-M4 SDK 的启动参数                  |
| `list`            | 列出 Fourier-GRX-M4 SDK 的启动参数                    |
| `start`           | 启动 Fourier-GRX-M4 SDK 运行环境和机器人                 |
| `stop`            | 停止 Fourier-GRX-M4 SDK 运行环境和机器人 （强制杀死相关进程）      |
| `enable_service`  | 启用 Fourier-GRX-M4 SDK 的服务功能，电脑重启后会自动启动机器人控制程序  |
| `disable_service` | 禁用 Fourier-GRX-M4 SDK 的服务功能，电脑重启后不会自动启动机器人控制程序 |
| `background`      | 将 Fourier-GRX-M4 SDK 运行环境和机器人程序放到后台运行          |
| `setup_uv`        | 一键创建 uv 开发环境（Python 3.11）并安装依赖库                |
| `setup_uv_py310`  | 同上，使用 Python 3.10                             |
| `update`          | 检查服务器上是否有新版本的软件包，并交互式地选择版本进行安装                |
| `web`             | 启动 web 调试上位机，供同一局域网内的浏览器访问                    |

---

## 安装的两个层次

`fourier-grx` 的安装动作分两层，缺一不可：

| 层次 | 命令 | 作用 |
|------|------|------|
| 软件包层 | `sudo dpkg -i fourier-grx-<版本>-<变体>.deb` | 仅把程序包解压到 `/usr/share/fourier-grx/`，并安装 `fourier-grx` 这个命令行工具本身 |
| 部署层 | `fourier-grx install` | 把上面的 zip 部署到 `~/fourier-grx/`，搭建运行环境并询问机器人型号、版本、运行模式 |

> ⚠️ **注意**
>
> 只执行 `dpkg -i` 时机器人**不会**用上新版本 —— 实际运行的是 `~/fourier-grx/` 里的旧内容。`dpkg -i` 之后必须再执行 `fourier-grx install`。

`fourier-grx install` 的具体动作：

1. 若 `~/fourier-grx` 已存在，先整体备份为 `~/fourier-grx-bak`（旧备份会被覆盖）
2. 删除 `~/fourier-grx`，从 `/usr/share/fourier-grx/fourier-grx.zip` 重新解压
3. 执行 `setup.sh` 配置系统环境
4. 执行 `config.sh --from-bak`：如备份目录里有可用的旧配置，会询问是否沿用；选择否（或无旧配置）时进入交互式选择

---

## `fourier-grx update` 详细说明

`update` 从 Fourier 服务器检查新版本，并完成下载与 `dpkg` 安装。它**只覆盖上面的软件包层**，装完仍需执行 `fourier-grx install`。

### 用法

```bash
fourier-grx update                        # 探测可用新版本，交互式选择安装
fourier-grx update <version>              # 直接安装指定版本，机型变体自动从已安装包读取
fourier-grx update <version>-<渠道>        # 安装指定渠道的构建，如 4.4.53-prerelease
fourier-grx update --help                 # 显示帮助信息
```

机型变体指软件包的平台/机型标识符（deb 的 `X-Variant` 字段），例如 `linux-arm64-cpu-m4l-blaze`，由已安装的软件包自动提供，无需手动输入。

### 自动探测范围

不带参数执行时，按当前版本向更高版本探测：

- 当前次版本：`patch + 1` 至 `patch + 20`，连续 5 次 404 即停止
- 下一主/次版本：只探 `minor + 1`（patch 0~10，连续 3 次 404 停止）与 `major + 1` 的 `minor 0`（patch 0~5，连续 3 次 404 停止）

### 运行流程

1. 从 deb 记录中读取当前版本号和机型变体
2. 向服务器逐版本探测可用的新版本（HTTP HEAD 请求）
3. 列出所有可用的更新版本，标注最新一个
4. 提示选择版本编号（直接回车安装最新，输入 `n` 取消）
5. 下载所选版本的 `.deb` 软件包
6. 执行 `sudo dpkg -i` 完成安装

### 示例输出

```text
当前版本 / Current version : 4.4.4
当前变体 / Current variant  : linux-arm64-cpu-m4l-blaze
正在检查更新... / Checking for updates...

发现以下新版本 / Found the following newer versions:
----------------------------------------------------
  [1] v4.4.5  fourier-grx-4.4.5-linux-arm64-cpu-m4l-blaze.deb
  [2] v4.4.6  fourier-grx-4.4.6-linux-arm64-cpu-m4l-blaze.deb
  [3] v4.4.7  fourier-grx-4.4.7-linux-arm64-cpu-m4l-blaze.deb  ← 最新 latest
----------------------------------------------------

请选择要安装的版本编号（直接回车安装最新 [3]，输入 n 取消）:
```

### 安装完成后

执行 `fourier-grx install` 完成部署层的更新，详见上文[安装的两个层次](#安装的两个层次)。

### 预发布渠道

预发布构建的文件名与 `X-Variant` 末段为 `prerelease`（正式版为 `blaze`），机型段保持不变，例如 `fourier-grx-4.4.53-linux-arm64-cpu-m4l-prerelease.deb`。

- 上述自动探测按已安装包的 `X-Variant`（`...-blaze`）拼文件名，**永远不会**发现预发布包。
- 只能通过 `<version>-prerelease` 显式安装：

```bash
fourier-grx update 4.4.53-prerelease
```

- 该写法会把机型变体末段替换为 `prerelease`，机型部分仍取自当前安装包。
- 该语法自 v4.4.53 起可用；更早版本请用 `sudo dpkg -i <deb>` 手动安装预发布包。
- 装完同样需要执行 `fourier-grx install`。

### 注意事项

- **缺少变体信息的旧包**：更早的部分安装包 deb 中没有 `X-Variant` 字段，此时 `fourier-grx update` 会直接报错退出，且无法用参数补传变体。请先用 `sudo dpkg -i` 安装一个较新版本的 `.deb`，再执行 `fourier-grx update`。

- **网络要求**：更新过程需要访问 Fourier 软件包服务器，请确保网络连接正常。

- **权限要求**：安装步骤需要 `sudo` 权限，系统会提示输入密码。

---

## `fourier-grx web` 详细说明

`web` 在机器人主控电脑上启动一个局域网网页调试界面（详见 [M4L 机器人 · 局域网网页调试](/fourier-grx-M4/docs/quickstart/m4l#局域网网页调试)）。

```bash
fourier-grx web                            # 自动发现机器人，监听 0.0.0.0:8000
fourier-grx web --host 192.168.137.220     # 跳过自动发现，直接指定机器人 IP
fourier-grx web --port 8080                # 修改 web 服务端口
fourier-grx web --bind 127.0.0.1           # 修改 web 服务监听地址
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--host` | 无 | **机器人的 IP 地址**。不填时通过 UDP 9527 广播自动发现 |
| `--robot-port` | `5566` | 机器人的 UDP 数据端口 |
| `--bind` | `0.0.0.0` | **web 服务的监听地址**，保持默认即可供局域网访问 |
| `--port` | `8000` | web 服务的监听端口 |

> ⚠️ **注意**：`--host` 指向机器人，`--bind` 指向 web 服务自身，两者含义不同，不要混用。

启动后，同一局域网内的电脑浏览器访问 `http://<机器人IP>:8000` 即可打开界面。`Ctrl+C` 退出。
