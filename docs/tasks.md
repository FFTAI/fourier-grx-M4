---
layout: default
title: 任务描述
nav_order: 4
has_toc: true
---

# 任务描述

* TOC
{:toc}

> ⚠️ **注意**：
>
> 本章中未列出的任务功能，在使用手柄进行机器人控制、选择任务时仍可能会显示，表明该任务可能仍处于开发中，或部分已废弃使用（未及时删去）。
> 因此，建议开发者在使用手柄进行机器人操作时，谨慎选择本章中未列出的任务进行执行，推荐只尝试本技术文档中 [任务描述](/fourier-grx-M4/docs/tasks) 部分列出的任务指令。

## 任务和模块

机器人任务指令列表 🎏：

- 任务指令通过 `fourier_grx.TaskCommand` 枚举类定义，具体定义如下：
- 具体 `任务值 (TID)` 可能会根据机器人的不同，或 `fourier-grx` 版本的不同而有所变化，**具体值以实际任务信息为准**。

M4 机器人常见任务指令示例：

| 任务指令                                          | 任务值 (TID) | 适用机型 | 任务描述                          |
|------------------------------------------------|-----------|------|-------------------------------|
| TASK_SERVO_OFF                                 | 36        | All  | 机器人全关节下电失能                    |
| TASK_SERVO_ON                                  | 35        | All  | 机器人全关节上电使能                    |
| TASK_SERVO_REBOOT                              | 41        | All  | 机器人全关节重启并重新加载配置               |
| TASK_CLEAR_FAULT                               | 34        | All  | 清除机器人全关节报警                    |
| TASK_STAND_CONTROL                             | 4020      | M4L  | 机器人缓慢移动各关节恢复到站立姿态             |
| TASK_ROTARY_JOINT_SET_HOME                     | 4103      | M4L  | 设置旋转关节当前位置为零点（手动）              |
| TASK_ROTARY_JOINT_BORDER_AND_RETURN            | 4104      | M4L  | 旋转关节边界检测：驱动至机械限位后自动回退        |
| TASK_ROTARY_JOINT_SET_HOME_POSITION            | 4105      | M4L  | 采样均值后将当前位置设为旋转关节零点（软件层）      |
| TASK_ROTARY_JOINT_MOVE_BACK                    | 4106      | M4L  | 旋转关节回退到安全位置                     |
| TASK_ROTARY_JOINT_AUTO_CALIBRATE               | 4120      | M4L  | 旋转关节自动校准（边界检测→下电→设置零点，三步连贯）  |
| TASK_PRISMATIC_JOINT_AUTO_CALIBRATE            | 4210      | M4L  | 腿长调节关节自动校准（上电后需首先执行）          |
| TASK_ROTARY_JOINT_FORWARD_WALK                 | 4111      | M4L  | 被动前向行走                        |
| TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_PD | 4116    | M4L  | 助力前向行走（调整 PD 参数）              |
| TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_DT | 4118    | M4L  | 助力前向行走（调整 dt 参数）              |
| TASK_ROTARY_JOINT_MARK_TIME                    | 4112      | M4L  | 被动原地踏步                        |
| TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_PD   | 4117      | M4L  | 助力原地踏步（调整 PD 参数）              |
| TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_DT   | 4119      | M4L  | 助力原地踏步（调整 dt 参数）              |

- All：表示所有傅利叶智能生产机型

---

## 任务文档索引

以下页面为当前仓库中已经整理出的主要任务说明，可作为任务说明入口；如需查看任务切换协议，请同时参考 [参考指南 User 接口](/fourier-grx-M4/docs/reference/user) 中的 `task/client 接口协议 (指令信息)` 章节。

### 基础控制任务

- [执行器使能](/fourier-grx-M4/docs/tasks/servo_on)
- [执行器失能](/fourier-grx-M4/docs/tasks/servo_off)
- [执行器重启](/fourier-grx-M4/docs/tasks/servo_reboot)
- [清除错误](/fourier-grx-M4/docs/tasks/clear_fault)
- [设置零点](/fourier-grx-M4/docs/tasks/set_home)

### 运动任务

- [站立姿态控制](/fourier-grx-M4/docs/tasks/stand_motion_control)
- [被动前向行走](/fourier-grx-M4/docs/tasks/forward_walk_passive)
- [助力前向行走（调整 PD 参数）](/fourier-grx-M4/docs/tasks/forward_walk_assist_adjust_pd)
- [助力前向行走（调整 dt 参数）](/fourier-grx-M4/docs/tasks/forward_walk_assist_adjust_dt)
- [被动原地踏步](/fourier-grx-M4/docs/tasks/mark_time_passive)
- [助力原地踏步（调整 PD 参数）](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_pd)
- [助力原地踏步（调整 dt 参数）](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_dt)

### 膝关节受限任务

- [站立姿态控制（膝关节受限）](/fourier-grx-M4/docs/tasks/knee_restriction_stand_motion_control)
- [被动前向行走（膝关节受限）](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_passive)
- [助力前向行走（膝关节受限，调整 PD 参数）](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_assist_adjust_pd)
- [助力前向行走（膝关节受限，调整 dt 参数）](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_assist_adjust_dt)
- [被动原地踏步（膝关节受限）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_passive)
- [助力原地踏步（膝关节受限，调整 PD 参数）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_pd)
- [助力原地踏步（膝关节受限，调整 dt 参数）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_dt)

### 专项与扩展任务

- [设置零点（旋转关节）](/fourier-grx-M4/docs/tasks/set_home_rotary_joint)
- [校准零点（直线关节）](/fourier-grx-M4/docs/tasks/calibrate_home_prismatic_joint)
- [调整长度（直线关节）](/fourier-grx-M4/docs/tasks/move_length_prismatic_joint)
- [规划器](/fourier-grx-M4/docs/tasks/planner)

机器人模块指令列表 🎏：

- 模块任务可以理解为任务下面的子任务模块，但是由于子任务之间可能存在 **互斥、组合** 的关系，因此，我们并不称其为子任务，而是以 **模块** 的形式进行管理。
- 相互互斥的几个模块其中一个被调用时，另一个在程序中自动被挂起。（由控制程序自动管理）
- 相互组合的模块，对方的调用和切换不会互相影响。
- 模块的运行管理全在控制程序中完成，上层无需关心模块的调起切换过程是否有风险。
- `模块值 (MID)` 跟机型绑定关系密切，因此，可能随版本变动。如果发现模块任务未正常执行，建议及时更新到最新固件，并 **以具体任务中关于模块信息的描述为准**。

## 任务切换

在使用不同方式进行机器人控制时，任务切换的方式可能会有所不同，以下是常见的任务切换方式：

|      | 物理手柄    | 物理键盘          | 通信 User 接口                                     | 通信 Developer 接口                                                       |
|------|---------|---------------|------------------------------------------------|-----------------------------------------------------------------------|
| 任务选择 | `L1` 按键 | `up`/`down` 键 | `task.robot_task_command` 发送 `任务值 (TID)`       |                                                                       |
| 任务确认 | `L2` 按键 | `enter` 键     | `task.flag_task_command_update` 发送 1 确认更新      | `control_system.robot_control_set_task_command(TID)` 发送 `任务值 (TID)`   |
| 模块选择 | `R1` 按键 |               | `task.robot_component_command` 发送 `模块值 (MID)`  |                                                                       |
| 模块确认 | `R2` 按键 |               | `task.flag_component_command_update` 发送 1 确认更新 | `control_system.robot_control_set_task_component(MID)` 发送 `模块值 (MID)` |
