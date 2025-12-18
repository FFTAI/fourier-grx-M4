---
layout: default
title: 被动原地踏步 (膝关节受限)
nav_order: 4.3
parent: 任务描述
has_toc: true
---

# 被动原地踏步 (膝关节受限)

任务值 (TID): **4302**

任务描述：

- 机器人通过给定参数，生成原地踏步的关节运动轨迹序列，通过执行器跟踪该轨迹，实现被动前向行走。
- 发送"停止运动标志位"为 true 时，机器人将逐渐停止运动，并不是立即停止。

任务参数：

| 接口参数      | 类型      | 默认值   | 参数范围          | 描述                             |
|-----------|---------|-------|---------------|--------------------------------|
| 大腿长度      | `float` | 0.5   | [0.4, 0.6]    | 机器人的大腿长度，单位为 m。                |
| 小腿长度      | `float` | 0.5   | [0.4, 0.6]    | 机器人的小腿长度，单位为 m。                |
| 左腿膝关节受限角度 | `float` | 0.0   | [0.0, 1.0]    | 左腿膝关节的最大受限角度，单位为弧度 rad。        |
| 右腿膝关节受限角度 | `float` | 0.0   | [0.0, 1.0]    | 右腿膝关节的最大受限角度，单位为弧度 rad。        |
| 抬腿高度      | `float` | 0.1   | [0.1, 0.5]    | 机器人每一步的长度，单位为 m。               |
| 步行周期      | `float` | 1.0   | [0.5, 4.0]    | 机器人前进的速度，单位为 s。                |
| 停止运动标志位   | `bool`  | false | (true, false) | 是否停止运动，true 表示停止，false 表示继续行走。 |

## 模块信息

| 模块值 (MID) | 模块指令 | 模块描述 | 涉及关节 |
|-----------|------|------|------|
|           |      |      |

## 接口信息

状态接口：

| 接口参数   | 接口映射关系                           | 
|--------|----------------------------------|
| 任务启动标志 | `task.flag_task_start`           |
| 任务结束标志 | `task.flag_task_finish`          |
| 运行比例   | `rehab.motion_ratio`             |
| 参考轨迹位置 | `rehab.reference_joint_position` |
| 参考轨迹速度 | `rehab.reference_joint_velocity` |

指令接口：

- 大腿长度 在算法运算中只能输入一个值，因此取左右大腿长度的均值。因此，传参时传入两个，但是实际只会取均值去使用。
- 小腿长度 在算法运算中只能输入一个值，因此取左右小腿长度的均值。因此，传参时传入两个，但是实际只会取均值去使用。

| 接口参数      | 接口映射关系                                                                                   |
|-----------|------------------------------------------------------------------------------------------|
| 大腿长度      | `grx.virtual_user_upper_leg_length_left`, `grx.virtual_user_upper_leg_length_right`, 取均值 |
| 小腿长度      | `grx.virtual_user_lower_leg_length_left`, `grx.virtual_user_lower_leg_length_right`, 取均值 |
| 左腿膝关节受限角度 | `grx.virtual_user_knee_restriction_left`                                                 |
| 右腿膝关节受限角度 | `grx.virtual_user_knee_restriction_right`                                                |
| 抬腿高度      | `grx.virtual_panel_command_param_1`                                                      |
| 步行周期      | `grx.virtual_panel_command_param_2`                                                      |
| 停止运动标志位   | `grx.virtual_panel_command_stop`                                                         |

## 更新日志

- `fourier-grx` v4.2.2 版本新增该功能。