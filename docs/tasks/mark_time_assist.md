---
layout: default
title: 助力原地踏步
nav_order: 4.4
parent: 任务描述
has_toc: true
---

# 助力原地踏步

## 助力模式 A

任务 ID: `4117`

任务描述：

- 机器人通过给定参数，生成原地踏步的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。
- 助力强度由助力系数控制，系数越大，助力越强。(PD参数)

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
| 停止运动标志位 | `grx.virtual_panel_command_param_4`                                                      |

涉及状态接口：

| 接口参数   | 接口映射关系                           | 
|--------|----------------------------------|
| 参考轨迹位置 | `rehab.reference_joint_position` |
| 参考轨迹速度 | `rehab_reference_joint_velocity` |

## 助力模式 B

任务 ID: `4119`

任务描述：

- 机器人通过给定参数，生成原地踏步的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。
- 助力强度由助力系数控制，系数越大，助力越强。
- 可配置为自动助力模式，机器人会根据当前状态自动调整助力系数。
- 可配置为自动助力模式，发送“自动助力模式标志位”，机器人会根据当前状态自动调整助力系数。(运动速度)

任务参数：

| 接口参数      | 类型      | 默认值   | 参数范围          | 描述                             |
|-----------|---------|-------|---------------|--------------------------------|
| 大腿长度      | `float` | 0.5   | [0.4, 0.6]    | 机器人的大腿长度，单位为 m。                |
| 小腿长度      | `float` | 0.5   | [0.4, 0.6]    | 机器人的小腿长度，单位为 m。                |
| 步长长度      | `float` | 0.5   | [0.1, 0.5]    | 机器人每一步的长度，单位为 m。               |
| 步行速度      | `float` | 0.5   | [0.1, 0.5]    | 机器人前进的速度，单位为 m/s。              |
| 助力系数      | `float` | 0.5   | [0.0, 1.0]    | 助力模式的系数，表示助力的强度。               |
| 停止运动标志位   | `bool`  | false | (true, false) | 是否停止运动，true 表示停止，false 表示继续行走。 |
| 自动助力模式标志位 | `bool`  | false | (true, false) | 是否启用自动助力模式，根据当前状态自动调整助力系数。     |

涉及指令接口：

| 接口参数      | 接口映射关系                                                                                   |
|-----------|------------------------------------------------------------------------------------------|
| 大腿长度      | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, 取均值 |
| 小腿长度      | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, 取均值 |
| 步长长度      | `grx.virtual_panel_command_param_1`                                                      |
| 步行速度      | `grx.virtual_panel_command_param_2`                                                      |
| 助力系数      | `grx.virtual_panel_command_param_3`                                                      |
| 停止运动标志位   | `grx.virtual_panel_command_param_4`                                                      |
| 自动助力模式标志位 | `grx.virtual_panel_command_param_5`                                                      |

涉及状态接口：

| 接口参数   | 接口映射关系                           | 
|--------|----------------------------------|
| 参考轨迹位置 | `rehab.reference_joint_position` |
| 参考轨迹速度 | `rehab_reference_joint_velocity` |