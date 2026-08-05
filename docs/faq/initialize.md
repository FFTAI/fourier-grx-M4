---
layout: default
title: 初始化问题
nav_order: 6.3
parent: 常见问题
---

# 初始化问题

## 配置文件错误

**现象**：机器人初始化失败，提示配置文件错误。

**解决方案**：

1. 确认机器人型号配置正确，参见 [固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install)
2. 重启机器人后重试

## 执行器自检失败

**现象**：`self-check` 失败，提示无法访问指定 IP 的执行器。

![自检错误](/fourier-grx-M4/assets/images/self_check_error.png)

**排查步骤**：

1. 检查执行器电源状态（正常应显示**紫色呼吸灯**）
2. 确认有线网络连接和静态 IP 配置
3. 检查线路连接完整性
