---
layout: default
title: 示例代码
nav_order: 2
has_toc: true
has_children: true
---

# 示例代码

* TOC
{:toc}

本文档提供了丰富的示例代码，帮助您快速掌握 Fourier-GRX-M4 SDK 的使用方法。

示例代码来自两个位置：

- 本仓库的 `demo/` 目录提供 User API、Developer API 和 UDP 纯 socket 示例，各接口页面会说明具体的获取与运行方法。
- 外部 [Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy.git) 仓库的 `FourierM4` 和 `FourierM4L` 分支提供更多对应机型的示例。

这些示例适用于不同层次的开发需求，请根据接口类型、机器人型号和运行环境选择。

## 示例入口

- [User 接口示例](/fourier-grx-M4/docs/examples/user)：适用于高层应用开发，可在机器人主控电脑或同一局域网内的其他电脑上运行。
- [Developer 接口示例](/fourier-grx-M4/docs/examples/developer)：适用于底层开发，需要在机器人主控电脑上运行。
- [User 接口示例](/fourier-grx-M4/docs/examples/user) 页面还收录了 **UDP 纯 socket 示例**：只用 Python 标准库与机器人通信，不需要安装 `fourier_grx` SDK，适合在不想搭建 SDK 环境的电脑上快速验证协议。
- 如需查看接口字段和协议说明，请结合 [参考指南](/fourier-grx-M4/docs/reference) 一起阅读。

## 外部示例代码仓库

以下命令用于同步 `Wiki-GRx-Deploy` 中的机型示例；运行本仓库 `demo/` 中的示例时，无需再克隆该外部仓库。

### M4 系列机器人

```bash
# 在机器人主控电脑 $HOME 目录下执行
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4
cd $HOME/Wiki-GRx-Deploy
```

### M4L 系列机器人

```bash
# 在机器人主控电脑 $HOME 目录下执行
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4L
cd $HOME/Wiki-GRx-Deploy
```

> ℹ️ 建议同步到 `$HOME` 目录下，方便与 `fourier-grx` 的安装目录并列管理。

## 二次开发环境配置

`fourier-grx` 工具提供了 `fourier-grx setup_uv` 命令，用于一键搭建基于 [uv](https://docs.astral.sh/uv/) 的 Python 3.11 开发环境，供机器人二次开发使用。

```bash
# 1. 在机器人主控电脑上搭建开发环境（需联网）
fourier-grx setup_uv

# 2. 激活该环境（虚拟环境固定位于 $HOME/fourier-grx/.venv）
source $HOME/fourier-grx/.venv/bin/activate

# 3. 验证 fourier_grx 可以正常导入，无输出即为成功
python -c "import fourier_grx"
```

补充说明：

- 若需要 Python 3.10 环境，改用 `fourier-grx setup_uv_py310`，虚拟环境位置不变。
- 若希望完全手动搭建环境，可在 `$HOME/fourier-grx/whl` 中找到 `fourier_core` / `fourier_grx` 的 whl 包，其余依赖按 `fourier-grx` 仓库的 `pyproject.toml` 安装。
- 判断当前环境是否已就绪：`python -c "import fourier_grx"` 能成功导入即可运行本仓库的 SDK 示例；`demo/udp` 下的示例不需要该环境。

运行具体的示例程序，请参考各个接口页面中的说明：

- [User 接口](/fourier-grx-M4/docs/examples/user)（含 UDP 纯 socket 示例）
- [Developer 接口](/fourier-grx-M4/docs/examples/developer)
