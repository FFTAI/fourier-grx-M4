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
> 规划器虽然不驱动关节，但每个控制周期仍会照常生成轨迹，并按与执行版任务相同的方式并入关节位置保护包络（只放宽、不收窄，复位后恢复）。
>
> 规划器停用时会向上位机回零步频字段（`rehab.step_frequency`）与谐波系数步态的档位回显字段（`rehab.gait_*`）。

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

## 谐波系数前向行走

任务值 (TID): **4407**

任务参数：参考 [谐波系数前向行走](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)

面板三条档位（`param_1` 髋幅度档 / `param_2` 伸膝限制档 / `param_3` 步频档）与执行版 4113 完全一致，且同样每个控制周期生效。除参考轨迹外，该规划器还会回显档位，供上位机在患者开始运动之前预览 4 × 4 = 16 条曲线的关节包络与 6 档节奏：

| 上报字段 | 含义 |
| :--- | :--- |
| `rehab.reference_joint_position_max`<br>`rehab.reference_joint_position_min` | 循环段（不含起步/结束过渡段）内各关节轨迹极值，单位 rad，URDF 帧（髋前屈为负）。<br>**顺序为 [左髋, 左膝, 右髋, 右膝]**，逐关节独立；左右腿相位相反，若要显示"髋的总范围"需自行取两腿并集 |
| `rehab.reference_joint_position`<br>`rehab.reference_joint_velocity` | 当前时刻的参考位置 / 速度（规划器不驱动关节，此值仍随时间推进） |
| `rehab.gait_name` | 当前系数表键名（如 `m4_5x4_land_3`），可反查 m4 来源表；停用后回空串 |
| `rehab.gait_amplitude_level` | `param_1` 轴当前值（1–4） |
| `rehab.gait_knee_restriction_deg` | `param_2` 轴当前值（0 / 5 / 10 / 15°） |
| `rehab.gait_speed_level` | `param_3` 轴当前值（1–6） |
| `rehab.gait_stride_time_s` | 实际一个大步时间（s），已量化到整帧 |
| `rehab.step_frequency` | 步频（步/分钟） |

各档髋、膝轨迹包络（两腿并集，单位 °；每格为「髋前摆峰值 … 髋后摆峰值」，前摆为负）：

| 伸膝限制档 | 髋幅度档 1 | 髋幅度档 2 | 髋幅度档 3 | 髋幅度档 4 | 膝抬摆峰值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 (0°) | −20.1 … +10.0 | −23.0 … +13.1 | −25.0 … +15.1 | −30.0 … +15.1 | 53.0 / 55.0 |
| 2 (5°) | −25.0 … +5.0 | −26.5 … +8.1 | −27.5 … +10.1 | −30.0 … +10.1 | 53.0 / 55.0 |
| 3 (10°) | −30.0 … 0.0 | −30.0 … +3.1 | −30.0 … +5.1 | −30.0 … +5.1 | 53.0 / 55.0 |
| 4 (15°) | −30.0 … 0.0 | −30.0 … 0.0 | −30.0 … +0.1 | −30.0 … +0.1 | 53.0 / 55.0 |

膝的**伸直底线**即该档伸膝限制值（0 / 5 / 10 / 15°），抬摆峰值 53.0 对应髋幅度档 1，55.0 对应档 2–4。

> 📌 髋前摆峰值在源数据表上以 30°（URDF 帧 −30°）封顶：伸膝限制越大，整条髋曲线越偏前屈，到档 3、4 时顶端已被截平，**髋幅度档 1–4 的角度范围随之趋同**，仍可辨别的差别落在曲线形状（摆腿时序与峰值位置）上。若上位机需要让幅度档直观可辨，建议配合伸膝限制档 1、2 使用。

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
- `fourier-grx` v4.4.57 正式发布（此前经 v4.4.55 ~ v4.4.57 预发布包提供；P1 请使用 v4.4.57 及以上）：新增谐波系数前向行走规划器（TID 4407），并扩展规划器停用时的清零范围至谐波步态的全部档位回显字段。
