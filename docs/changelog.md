---
layout: default
title: 更新日志
nav_order: 8
has_toc: true
---

# 更新日志

{:toc}

本文档记录了 Fourier-GRX-M4 SDK 及其文档的所有重要更新。

## 2026 年 5 月

### v1.1.0

**新增功能**

- 🛡️ **M4LT2 急停高阻尼保护**：M4LT2 机型在硬件急停开关（ioboard）触发时，不再直接断电失能，而是自动切换到高阻尼保护任务（`TASK_ROTARY_JOINT_HIGH_DAMPING`，TID=4600）。关节保持上电，以 `kp=0`、`kd=80` 的纯阻尼 PD 模式控制旋转关节，防止肢体瞬间跌落，为操作者提供更安全的保护时间窗口。详见 [高阻尼保护任务说明](/fourier-grx-M4/docs/tasks/emergency_stop_high_damping)。

**文档更新**

- 📖 新增 [高阻尼保护任务页面](/fourier-grx-M4/docs/tasks/emergency_stop_high_damping)
- 📖 更新 [任务描述](/fourier-grx-M4/docs/tasks) 中的任务列表，新增 TID=4600
- 📖 更新 [M4L 快速开始](/fourier-grx-M4/docs/quickstart/m4l)，补充硬件急停按钮行为说明

---

## 2025 年 7 月

### v1.0.0 (2025-07-08)

**重要里程碑**

- 🎉 发布 Fourier-GRX-M4 SDK 文档第一个正式版本
- 💡 支持 M4 系列机器人开发
- 📖 完整的 API 文档和使用指南
- ✨ 新增常用操作页面
- 📚 优化文档结构和导航
- 🔍 改进搜索功能

**功能特性**

- ✅ 基础 API 接口
- ✅ 示例代码
- ✅ 开发指南
- ✅ 故障排除指南

**说明**

- 目前主要支持 M4 系列机器人
- 其他机型支持将陆续添加
