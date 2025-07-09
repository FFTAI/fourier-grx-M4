---
layout: default
title: 助力前向行走
nav_order: 4.2
parent: 任务描述
has_toc: true
---

# 助力前向行走

## 助力模式 A

任务 ID: `4116`

任务描述：

- 机器人通过给定参数，生成向前行走的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。

任务参数：

| 接口参数 | 类型      | 默认值 | 参数范围       | 描述                |
|------|---------|-----|------------|-------------------|
| 大腿长度 | `float` | 0.5 | [0.4, 0.6] | 机器人的大腿长度，单位为 m。   |
| 小腿长度 | `float` | 0.5 | [0.4, 0.6] | 机器人的小腿长度，单位为 m。   |
| 步长长度 | `float` | 0.5 | [0.1, 0.5] | 机器人每一步的长度，单位为 m。  |
| 步行速度 | `float` | 0.5 | [0.1, 0.5] | 机器人前进的速度，单位为 m/s。 |
| 助力系数 | `float` | 0.5 | [0.0, 1.0] | 助力模式的系数，表示助力的强度。  |

| 接口参数 | 虚拟外设映射关系                                                                                 |
|------|------------------------------------------------------------------------------------------|
| 大腿长度 | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, 取均值 |
| 小腿长度 | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, 取均值 |
| 步长长度 | `grx.virtual_panel_command_param_1`                                                      |
| 步行速度 | `grx.virtual_panel_command_param_2`                                                      |
| 助力系数 | `grx.virtual_panel_command_param_3`                                                      |

## 助力模式 B

任务 ID: `4118`

任务描述：

- 机器人通过给定参数，生成向前行走的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。

任务参数：

| 接口参数 | 类型      | 默认值 | 参数范围       | 描述                |
|------|---------|-----|------------|-------------------|
| 大腿长度 | `float` | 0.5 | [0.4, 0.6] | 机器人的大腿长度，单位为 m。   |
| 小腿长度 | `float` | 0.5 | [0.4, 0.6] | 机器人的小腿长度，单位为 m。   |
| 步长长度 | `float` | 0.5 | [0.1, 0.5] | 机器人每一步的长度，单位为 m。  |
| 步行速度 | `float` | 0.5 | [0.1, 0.5] | 机器人前进的速度，单位为 m/s。 |
| 助力系数 | `float` | 0.5 | [0.0, 1.0] | 助力模式的系数，表示助力的强度。  |

| 接口参数 | 虚拟外设映射关系                                                                                 |
|------|------------------------------------------------------------------------------------------|
| 大腿长度 | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, 取均值 |
| 小腿长度 | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, 取均值 |
| 步长长度 | `grx.virtual_panel_command_param_1`                                                      |
| 步行速度 | `grx.virtual_panel_command_param_2`                                                      |
| 助力系数 | `grx.virtual_panel_command_param_3`                                                      |
