---
layout: default
title: 快速开始
nav_order: 1
has_toc: true
has_children: true
---

# 快速开始

请根据设备当前状态选择对应流程。首次操作机器人时，请先阅读所选页面中的安全说明，并做好支撑与急停准备。

## 按设备状态选择

| 设备状态 | 推荐入口 | 主要内容 |
|----------|----------|----------|
| 已完成安装，使用 M4L 系列机器人 | [M4L 机器人](/fourier-grx-M4/docs/quickstart/m4l) | 开机、登录、启动控制程序、网页调试和二次开发环境配置 |
| 全新设备，或尚未完成首次安装 | [固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install) | 下载安装包、部署运行内容并配置机器人型号 |
| 已完成首次安装，只需升级固件 | [固件更新](/fourier-grx-M4/docs/quickstart/firmware_update) | 使用 `fourier-grx update` 或手动安装包升级，并完成部署 |
| 系统损坏，或确需更换系统镜像 | [系统烧录镜像](/fourier-grx-M4/docs/quickstart/flash_image) | 为适用的 LubanCat-RK3588 控制板烧录系统；正常使用时无需烧录 |
| 使用旧版 M4 软件 | [M4 机器人](/fourier-grx-M4/docs/quickstart/m4) | 查阅旧版操作流程；该页面已废弃，支持新版软件的设备应改用 M4L 流程 |

## 完成安装后的使用流程

1. 按照 [M4L 机器人](/fourier-grx-M4/docs/quickstart/m4l) 页面完成开机、登录和控制程序启动。
2. 参考[示例代码](/fourier-grx-M4/docs/examples)配置二次开发环境，并选择与 User、Developer 或 UDP 接口对应的示例。
3. 开发过程中结合[参考指南](/fourier-grx-M4/docs/reference)查阅接口与配置字段，通过[任务描述](/fourier-grx-M4/docs/tasks)确认任务参数和注意事项。
4. 需要校准、查看日志或配置网络时，查阅[常用操作](/fourier-grx-M4/docs/usage)；遇到问题时先查阅[常见问题](/fourier-grx-M4/docs/faq)。
