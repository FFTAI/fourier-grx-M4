---
layout: default
title: 助力前向行走 (调整 dt 参数)
nav_order: 4.2
parent: 任务描述
has_toc: true
---

# 助力前向行走 (调整 dt 参数)

任务值 (TID): **4118**

任务描述：

- 机器人通过给定参数，生成向前行走的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。
- 发送"停止运动标志位"为 true 时，机器人将逐渐停止运动，并不是立即停止。
- 助力强度由助力系数控制，系数越大，助力越强。
- 可配置为自动助力模式，发送“自动助力模式标志位”，机器人会根据当前状态自动调整助力系数。(运动速度)

任务参数：

| 接口参数      | 类型      | 默认值   | 参数范围          | 描述                                         |
|-----------|---------|-------|---------------|--------------------------------------------|
| 大腿长度      | `float` | 0.5   | [0.3, 0.6]    | 机器人的大腿长度，单位为 m。                            |
| 小腿长度      | `float` | 0.5   | [0.3, 0.6]    | 机器人的小腿长度，单位为 m。                            |
| 步长长度      | `float` | 0.5   | [0.2, 0.8]    | 机器人每一步的长度，单位为 m。                           |
| 步行速度      | `float` | 0.5   | [0.1, 1.2]    | 机器人前进的速度，单位为 m/s。                          |
| 助力系数      | `float` | 0.5   | [0.0, 1.0]    | 助力模式的系数，表示助力的强度。                           |
| 自动助力模式标志位 | `bool`  | false | (true, false) | 是否启用自动助力模式，根据当前状态自动调整助力系数。                 |
| 启动运动标志位   | `bool`  | false | (true, false) | 是否启动运动，true 表示启动，false 表示不启动（如果已经启动，不会起作用） |
| 停止运动标志位   | `bool`  | false | (true, false) | 是否停止运动，true 表示停止，false 表示继续行走。             |

> 建议：
> - 步长为步速的 0.5 到 1.0 倍之间，能够获得较好的行走效果。例如，步速为 0.5 m/s 时，步长建议设置在 0.25 m 到 0.5 m 之间。

## 模块信息

| 模块值 (MID) | 模块指令 | 模块描述 | 涉及关节 |
|-----------|------|------|------|
|           |      |      |

## 接口信息

状态接口：

| 接口参数      | 接口映射关系                               | 
|-----------|--------------------------------------|
| 任务启动标志    | `task.flag_task_start`               |
| 任务结束标志    | `task.flag_task_finish`              |
| 运行比例      | `rehab.motion_ratio`                 |
| 参考轨迹位置    | `rehab.reference_joint_position`     |
| 参考轨迹速度    | `rehab.reference_joint_velocity`     |
| 参考轨迹位置最大值 | `rehab.reference_joint_position_max` |
| 参考轨迹位置最小值 | `rehab.reference_joint_position_min` |

指令接口：

- 大腿长度 在算法运算中只能输入一个值，因此取左右大腿长度的均值。因此，传参时传入两个，但是实际只会取均值去使用。
- 小腿长度 在算法运算中只能输入一个值，因此取左右小腿长度的均值。因此，传参时传入两个，但是实际只会取均值去使用。

| 接口参数      | 接口映射关系                                                                                   |
|-----------|------------------------------------------------------------------------------------------|
| 大腿长度      | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, 取均值 |
| 小腿长度      | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, 取均值 |
| 步长长度      | `grx.virtual_panel_command_param_1`                                                      |
| 步行速度      | `grx.virtual_panel_command_param_2`                                                      |
| 助力系数      | `grx.virtual_panel_command_param_3`                                                      |
| 自动助力模式标志位 | `grx.virtual_panel_command_switch_1`                                                     |
| 启动运动标志位   | `grx.virtual_panel_command_start`                                                        |
| 停止运动标志位   | `grx.virtual_panel_command_stop`                                                         |

## 更新日志

- `fourier-grx` v4.0.0 版本新增该功能。