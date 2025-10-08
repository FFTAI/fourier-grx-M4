---
layout: default
title: 被动原地踏步
nav_order: 4.3
parent: 任务描述
has_toc: true
---

# 被动原地踏步

任务值 (TID): **4113**

任务描述：

- 机器人通过给定参数，生成原地踏步的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。
- 发送"停止运动标志位"为 true 时，机器人将逐渐停止运动，并不是立即停止。

任务参数：

| 接口参数    | 类型      | 默认值   | 参数范围          | 描述                             |
|---------|---------|-------|---------------|--------------------------------|
| 大腿长度    | `float` | 0.5   | [0.4, 0.6]    | 机器人的大腿长度，单位为 m。                |
| 小腿长度    | `float` | 0.5   | [0.4, 0.6]    | 机器人的小腿长度，单位为 m。                |
| 步长长度    | `float` | 0.5   | [0.1, 0.5]    | 机器人每一步的长度，单位为 m。               |
| 步行速度    | `float` | 0.5   | [0.1, 0.5]    | 机器人前进的速度，单位为 m/s。              |
| 助力系数    | `float` | 0.5   | [0.0, 1.0]    | 助力模式的系数，表示助力的强度。               |
| 停止运动标志位 | `bool`  | false | (true, false) | 是否停止运动，true 表示停止，false 表示继续行走。 |

涉及指令接口：

| 接口参数    | 接口映射关系                                                                                   |
|---------|------------------------------------------------------------------------------------------|
| 大腿长度    | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, 取均值 |
| 小腿长度    | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, 取均值 |
| 步长长度    | `grx.virtual_panel_command_param_1`                                                      |
| 步行速度    | `grx.virtual_panel_command_param_2`                                                      |
| 助力系数    | `grx.virtual_panel_command_param_3`                                                      |
| 停止运动标志位 | `grx.virtual_panel_command_stop`                                                         |

涉及状态接口：

| 接口参数   | 接口映射关系                           | 
|--------|----------------------------------|
| 参考轨迹位置 | `rehab.reference_joint_position` |
| 参考轨迹速度 | `rehab_reference_joint_velocity` |