---
layout: default
title: 参考指南
nav_order: 3
toc: true          # 启用目录
toc_min_header: 2  # 最小显示标题层级（如 H2）
toc_max_header: 3  # 最大显示标题层级（如 H3）
---

# 参考指南

本章节汇总 Fourier-GRX-M4 SDK 的核心参考文档，建议根据开发层级和排障场景按需查阅。

## 接口参考

- [User 接口](/fourier-grx-M4/docs/reference/user)：面向高层应用开发，基于 Zenoh 协议进行通信。
- [Developer 接口](/fourier-grx-M4/docs/reference/developer)：面向底层控制开发，直接调用 Python 开发库。

## 机器人与配置

- [机器人关节序列](/fourier-grx-M4/docs/reference/joint_sequence)：关节顺序、索引和数据字段说明。
- [资源文件](/fourier-grx-M4/docs/reference/resource_file)：资源目录、Zenoh 配置与相关文件说明。
- [启动配置文件](/fourier-grx-M4/docs/reference/config_file)：`run.sh`、`run_type` 与配置文件字段说明。
- [运行模式](/fourier-grx-M4/docs/reference/run_type)：发布模式、调试模式、开发者模式等运行方式说明。

## 工具与排障

- [命令行工具](/fourier-grx-M4/docs/reference/command_line_tool)：`fourier-grx` 常用子命令说明。
- [执行器错误码](/fourier-grx-M4/docs/reference/actuator_error_code)：常见错误码与处理方式。
