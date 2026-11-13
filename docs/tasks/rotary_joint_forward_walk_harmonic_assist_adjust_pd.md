---
layout: default
title: 谐波系数助力前向行走（调整 PD 参数）
nav_order: 4.29
parent: 任务描述
has_toc: true
---

# 谐波系数助力前向行走（调整 PD 参数）

## 任务信息

任务值 (TID): **4132**（v4.4.79 起新增）

适用机型：M4L（P1 / T1 / T2）

任务描述：

- 步态来源与[谐波系数前向行走（4131）](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)完全一致：回放 Fourier-GRX 主表（预存的 Fourier 谐波系数）采样出的周期性关节曲线，**曲线形状固定**（由幅度档与伸膝限制档从 16 条曲线中选定），**节奏**由步频档决定。
- 助力语义与[助力前向行走（调整 PD 参数，4116）](/fourier-grx-M4/docs/tasks/forward_walk_assist_adjust_pd)一致：助力系数在 buttery（最柔顺）与 soft（最软一档）之间对 PD 增益做线性插值，系数越小关节越柔顺、患者自主发力空间越大。
- 与 4116 的差别：**4116 的轨迹由 LIPM 模型按步长/步速在线生成，本任务的轨迹固定来自系数表**；因此本任务没有步长/步速/基座高度/抬腿高度/双支撑期占比参数，面板前三档与 4131 完全相同（幅度档 / 伸膝限制档 / 步频档），助力系数挪到 `param_4`。
- 负载检测与自动 PD 爬升在本任务中关闭（助力档位由上位机直接给定）。
- 本任务**只指令关节角度，不指令位移**：基座（骨盆）的前进量不由算法给出，实际走多远取决于使用者与外骨骼的整体运动。

任务参数：

| 接口参数       | 类型      | 默认值   | 参数范围       | 描述                                                                                     |
|------------|---------|-------|------------|----------------------------------------------------------------------------------------|
| 髋摆动幅度等级   | `int`   | 2     | [1, 4]     | 同 4131：选择轨迹形状的第一条轴，四档差异几乎全在髋的摆动幅度上。非法值或未发送时取默认档 2。                       |
| 伸膝限制等级    | `int`   | 1     | [1, 4]     | 同 4131：1/2/3/4 档对应膝关节伸直底线 0 / 5 / 10 / 15°。越界会被限幅到 1..4。                                     |
| 步频等级      | `int`   | 3     | [1, 6]     | 同 4131：只改节奏、不改曲线形状。1 档最慢（5.25 s/大步）到 6 档最快（2.45 s/大步）。非法值或 ≤ 0 时保持当前档不变。          |
| 助力系数      | `float` | 0.0   | [0.0, 1.0] | 关节 PD 控制刚度的调节系数。0 = buttery 最柔顺，1 = soft 最软一档（插值公式与档位表与 4116 完全相同，见[其文档](/fourier-grx-M4/docs/tasks/forward_walk_assist_adjust_pd)）。未发送时按 0 处理。 |
| 启动运动标志位   | `bool`  | false | (true, false) | 是否启动运动。true 表示启动（若已启动则不起作用）。                                                             |
| 停止运动标志位   | `bool`  | false | (true, false) | 是否停止运动。true 表示走满当前循环窗后停止。                                                                 |

> **不生效的参数**：大腿长度、小腿长度、步长长度、步行速度、基座高度、抬腿高度、双支撑期占比（本任务曲线来自预存系数表，不做运动学/动力学反解，摇杆左右推同样不改变轨迹，只用于触发启动/停止）。

> 生效时机：
>
> - **助力系数**只在任务进入启动阶段（`STAGE_INIT` / `STAGE_START`）时写入关节 PD 增益，行走过程中修改不会立即改变当前刚度，需停止后重新启动本任务才生效（与 4116 相同）。
> - **幅度档 / 伸膝限制档 / 步频档**在按下"启动"前修改立即用于本次起步；行走过程中修改不影响正在执行的轨迹，下一次起步才生效（与 4131 相同）。

## 模块信息

该任务暂无独立模块指令，不支持通过模块接口进行分关节控制。

## 接口信息

状态接口：

| 接口参数       | 接口映射关系                                    |
|------------|-------------------------------------------|
| 任务启动标志     | `task.flag_task_start`                    |
| 任务结束标志     | `task.flag_task_finish`                   |
| 运行比例       | `rehab.motion_ratio`                      |
| 步频         | `rehab.step_frequency`                    |
| 当前步态键名     | `rehab.gait_name`                         |
| 髋摆动幅度等级    | `rehab.gait_amplitude_level`              |
| 伸膝限制等级     | `rehab.gait_knee_restriction_deg`         |
| 步频等级       | `rehab.gait_speed_level`                  |
| 实际大步时间     | `rehab.gait_stride_time_s`                |
| 参考轨迹位置     | `rehab.reference_joint_position`          |
| 参考轨迹速度     | `rehab.reference_joint_velocity`          |
| 参考轨迹位置最大值  | `rehab.reference_joint_position_max`      |
| 参考轨迹位置最小值  | `rehab.reference_joint_position_min`      |

> 步态回显字段（`gait_name` 等 5 项）语义与 4131 相同，详见[谐波系数前向行走](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)的接口说明。

指令接口：

| 接口参数       | 接口映射关系                                    |
|------------|-------------------------------------------|
| 髋摆动幅度等级   | `grx.virtual_panel_command_param_1`       |
| 伸膝限制等级    | `grx.virtual_panel_command_param_2`       |
| 步频等级       | `grx.virtual_panel_command_param_3`       |
| 助力系数       | `grx.virtual_panel_command_param_4`       |
| 启动运动标志位    | `grx.virtual_panel_command_start`         |
| 停止运动标志位    | `grx.virtual_panel_command_stop`          |

> ⚠️ 与 4116 不同：本任务的**助力系数在 `param_4`**（`param_3` 已被步频等级占用）；`param_1` / `param_2` 也不是步长/步速，而是幅度档/伸膝限制档。上位机按本表映射，勿沿用 4116 的参数位置。

## 更新日志

- `fourier-grx` v4.4.79 版本：新增本任务（TID 4132）。步态来源、面板三档与 4131 一致，助力调 PD 语义与 4116 一致（assist_ratio 在 buttery ↔ soft 间插值，启动时一次性写入）。
