---
layout: default
title: 规划器
nav_order: 4.26
parent: 任务描述
has_toc: true
---

# 规划器

规划器是针对轨迹跟踪任务的一种附属任务，用于生成关节运动轨迹序列，供上位机显示参数和可能的轨迹生成结果。规划器任务不会调用任务的激活/取消激活流程，机器本身并不执行轨迹跟踪运动。

> ⚠️ **注意**：使用规划器前请先执行执行器失能（TID=36），确保设备处于失能状态，以避免意外伤害。
>
> 规划器停用时会向上位机回零步频字段（`rehab.step_frequency`）。

## 被动前向行走

任务值 (TID): **4401**

任务参数：参考 [被动前向行走](/fourier-grx-M4/docs/tasks/forward_walk_passive)

## 被动原地踏步

任务值 (TID): **4402**

任务参数：参考 [被动原地踏步](/fourier-grx-M4/docs/tasks/mark_time_passive)

## 助力前向行走 (调整 PD 参数)

任务值 (TID): **4403**

任务参数：参考 [助力前向行走 (调整 PD 参数)](/fourier-grx-M4/docs/tasks/forward_walk_assist_adjust_pd)

## 助力原地踏步 (调整 PD 参数)

任务值 (TID): **4404**

任务参数：参考 [助力原地踏步 (调整 PD 参数)](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_pd)

## 助力前向行走 (调整 dt 参数)

任务值 (TID): **4405**

任务参数：参考 [助力前向行走 (调整 dt 参数)](/fourier-grx-M4/docs/tasks/forward_walk_assist_adjust_dt)

## 助力原地踏步 (调整 dt 参数)

任务值 (TID): **4406**

任务参数：参考 [助力原地踏步 (调整 dt 参数)](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_dt)

## 被动前向行走 (膝关节受限)

任务值 (TID): **4501**

任务参数：参考 [被动前向行走 (膝关节受限)](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_passive)

## 被动原地踏步 (膝关节受限)

任务值 (TID): **4502**

任务参数：参考 [被动原地踏步 (膝关节受限)](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_passive)

## 助力前向行走 (膝关节受限, 调整 PD 参数)

任务值 (TID): **4503**

任务参数：参考 [助力前向行走 (膝关节受限, 调整 PD 参数)](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_assist_adjust_pd)

## 助力原地踏步 (膝关节受限, 调整 PD 参数)

任务值 (TID): **4504**

任务参数：参考 [助力原地踏步 (膝关节受限, 调整 PD 参数)](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_pd)

## 助力前向行走 (膝关节受限, 调整 dt 参数)

任务值 (TID): **4505**

任务参数：参考 [助力前向行走 (膝关节受限, 调整 dt 参数)](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_assist_adjust_dt)

## 助力原地踏步 (膝关节受限, 调整 dt 参数)

任务值 (TID): **4506**

任务参数：参考 [助力原地踏步 (膝关节受限, 调整 dt 参数)](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_dt)

## 更新日志

- `fourier-grx` v4.3.0 版本新增规划器任务（TID 4401–4406）。
- `fourier-grx` v4.4.47 版本起，规划器任务退出时清零步频上报字段。
