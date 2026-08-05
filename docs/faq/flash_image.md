---
layout: default
title: 系统烧录问题
nav_order: 6.8
parent: 常见问题
---

# 系统烧录问题

> ℹ️ **说明**：以下问题与 [系统烧录镜像](/fourier-grx-M4/docs/quickstart/flash_image)（LubanCat-RK3588 控制板卡）操作相关。

## 电脑没有识别到设备怎么办？

请确认已正确安装 DriverAssistant 驱动，并使用具有数据传输功能的 Type-C 数据线连接板卡 OTG 接口。若仍无法识别，可尝试卸载旧驱动后重新安装，或更换 USB 端口。

## 运行 `network_scanner.ps1` 时提示无法加载脚本怎么办？

这是 Windows PowerShell 权限不足导致的常见问题。请关闭当前窗口，使用**管理员权限**重新打开 PowerShell 后，再执行脚本。

![PowerShell 权限报错示例](/fourier-grx-M4/assets/images/powershell_error.png)

## 鲁班猫已装到设备上但未配置 IP，`network_scanner.ps1` 扫描不到怎么办？

这种情况通常无法通过局域网脚本直接发现设备。建议先将鲁班猫从设备上拆下，使用电脑网线**直连板卡**，先完成 IP 配置；确认可以正常通信后，再重新装回设备。
