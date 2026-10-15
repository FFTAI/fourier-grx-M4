---
layout: default
title: Fourier-GRX-M4 SDK
nav_order: 0
has_children: false
toc: true          # 启用目录
toc_min_header: 2  # 最小显示标题层级（如 H2）
toc_max_header: 3  # 最大显示标题层级（如 H3）
---

# 欢迎来到 Fourier-GRX-M4 SDK 开发文档

> 本页为中文首页，英文文档见 [English](/fourier-grx-M4/docs/en/)。

## 基本介绍

Fourier-GRX-M4 SDK 是傅利叶智能提供的一个软件开发工具包，
提供了一套 API 用于安装、配置、控制傅利叶智能的 M4 或 M4L 机器人产品的应用程序。

该 SDK 设计简洁易用，提供高级接口来控制机器人运动并读取传感器数据。
SDK 目前主要支持 Python 语言二次开发使用。

## 开始使用

[快速开始](/fourier-grx-M4/docs/quickstart) 是开始使用 Fourier-GRX-M4 SDK 库的推荐方式。
这份分步指南将帮助您安装所需库文件并运行简单程序来控制机器人。

[示例代码](/fourier-grx-M4/docs/examples) 演示了 SDK 库的使用方法，可作为您开发应用程序的参考程序。

[参考指南](/fourier-grx-M4/docs/reference) 包含了 SDK 库的详细 API 文档，可作为您开发应用程序的参考文档。

[任务描述](/fourier-grx-M4/docs/tasks) 逐个说明机器人可执行的运动与标定任务，包括触发方式、参数与注意事项。

[常用操作](/fourier-grx-M4/docs/usage) 说明关节零位校准、开机自启动、运行日志、数据记录和网络连接等日常操作。固件安装方法请参考 [快速开始 - 固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install)，固件升级方法请参考 [快速开始 - 固件更新](/fourier-grx-M4/docs/quickstart/firmware_update)。

[常见问题](/fourier-grx-M4/docs/faq) 收录硬件、安装、初始化、网络、性能等方面的排障问答。若问题仍未列出，欢迎通过[贡献](/fourier-grx-M4/docs/contributing)渠道向我们反馈。

[固件发布](/fourier-grx-M4/docs/release) 列出已发布的固件版本，以及对应的下载与更新说明。

## 支持平台与版本

| 硬件环境       | 系统环境             | Python 环境   | 已测试 | 测试通过 |
|------------|------------------|-------------|-----|------|
| ARM RK3588 | Ubuntu 20.04 LTS | Python 3.11 | ✅   | ✅    |
| X64 INTEL  | Ubuntu 22.04 LTS | Python 3.11 | ✅   | ✅    |
| X64 AMD    | Ubuntu 22.04 LTS | Python 3.11 | ✅   | ✅    |
|            | Windows          | Python 3.11 |     |      |
|            | MacOS            | Python 3.11 |     |      |

> ℹ️ **说明**:
>
> Fourier-GRX-M4 SDK 具备 User 和 Developer 两类不同层级的接口。
> - User 接口通过网络与机器人通信，无明确平台和语言限制，但仍推荐在 Ubuntu 系统上进行开发。
> - Developer 接口基于 Python 库开发。

## 更新日志

请查看 [更新日志](/fourier-grx-M4/docs/changelog) 以获取最新版本文档的更新内容。

## 贡献指南

请阅读我们的[贡献指南](/fourier-grx-M4/docs/contributing)以获取更多信息。
