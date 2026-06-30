---
layout: default
title: 更新日志
nav_order: 8
has_toc: true
---

# 更新日志

{:toc}

本文档记录了 Fourier-GRX-M4 SDK 及其文档的所有重要更新。

## 2026 年 6 月

### v1.1.5 (2026-06-30)

**修复**

- 🐛 **Stand 任务使能冲击（完整修复）**：新增 `STAGE_WARM_UP` 阶段（0.5 s 纯阻尼过渡，`kp=0`，目标位置跟随实测）。`reset()` 覆写确保每次任务激活都重新经历此阶段，解决了 v1.1.4（4.4.10）中仅一个 tick 不足以抑制冲击、以及多次触发时阻尼阶段不复现的问题

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.11`

---

### ~~v1.1.4 (2026-06-29)~~ *(已撤销)*

> kp=0 仅持续一个 tick，不足以抑制冲击；且 `STAGE_INIT` 在第二次激活时不再触发。已在 v1.1.5 中完整修复。

---

### ~~v1.1.3 (2026-06-29)~~ *(已撤销)*

> v1.1.3 中对 `function_on_activate` 里预置执行器目标位置的修改经验证无效：`SERVO_ON` 通信帧仅发送使能指令，不携带位置数据，故该修改已在 v1.1.4 中回退。

---

## 2026 年 5 月

### v1.1.2 (2026-05-14)

**新增功能**

- 🔍 **固件版本检测标志位**：`DynalinkGRX` 新增 `flag_version_check_error`（`0` 正常 / `1` 异常）和 `version_check_error_info`（异常详情列表）字段，检测到 IOBoard / FSA / FSE 固件版本不匹配、无响应或查询异常时自动置位，通过 Dynalink `read_fields` 同步至上位机

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.6`

---

### v1.1.1 (2026-05-11)

**新增功能**

- ⚙️ **助力原地踏步（DT 模式）触发力配置接口**：新增 `assist_trigger_force_upper`（加速触发力）和 `assist_trigger_force_lower`（减速触发力）可配置参数，默认值分别为 `2.0 Nm` 和 `1.0 Nm`，通过上位机面板 `param_4`、`param_5` 设置。适用任务：TID 4119（助力原地踏步，调整 DT 参数）、TID 4306（膝关节受限助力原地踏步，调整 DT 参数）。详见 [助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_dt) 和 [膝关节受限助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_dt)

**算法修正**

- 🔧 **助力触发力阈值改为绝对力矩值**：原公式 `G[i] + offset` 改为 `G[i] * 0.0 + offset`（G 分量清零）。经实际实验测试，加入重力项 `G[i]` 会导致系统不稳定，故将其清零，直接以配置值作为加减速触发阈值

**行为澄清**

- 📌 明确参数更新时机：所有任务参数（步高、踏步周期、助力比例、触发力等）仅在**任务触发时**读取一次，不支持运行时实时刷新；需重新触发任务方可生效

**文档更新**

- 📖 更新 [助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_dt)：参数名由"助力触发力上/下限偏移"改为"助力触发力上/下限"，更新触发阈值说明，补充 G 项清零的实验依据
- 📖 更新 [膝关节受限助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_dt)：同上
- 📖 同步更新以上两个任务的英文文档

---

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
