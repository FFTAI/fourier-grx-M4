---
layout: default
title: 助力前向行走 高抬腿（膝受限，dt 模式）
parent: 任务描述
nav_order: 4.296
has_toc: true
---

# 助力前向行走 高抬腿（膝受限，dt 模式）

## 任务信息

| 任务 | 任务值 (TID) | 控制方式 |
|---|---|---|
| 助力前向行走 高抬腿（膝受限，dt 模式） | **4309** | 助力（dt 模式） |

适用机型：M4L（P1 / T1 / T2）。对应规划器 **4509**，只生成和上报参考轨迹，不驱动关节。无膝限版本为 **4137**，其规划器为 **4412**。

任务描述：

- 复用[助力前向行走 高抬腿（4137）](/fourier-grx-M4/docs/tasks/forward_walk_high_lift_assist_adjust_dt)的高抬腿轨迹与 dt 助力逻辑，并叠加[膝受限前向行走](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_passive)的用户输入和基座高度计算。
- 左右伸膝限制取较大值，作为双腿共同的最小膝角；高抬腿逆解和平滑后仍保持该限位。
- 助力系数映射为 0.5～1.0 倍轨迹回放速度，可用 `switch_1` 打开自动助力；PD 全程固定 medium 档。
- `param_6` 对本任务不生效，基座高度由膝限角度与腿长自动计算。本任务不读取 `param_9`，也不提供暂停接口。

任务参数：

| 面板/用户参数 | 含义 | 默认值 | 说明 |
|---|---|---|---|
| `param_1` | 步长 | 0.5 m | 与普通前向行走一致 |
| `param_2` | 步行速度 | 0.5 m/s | 与普通前向行走一致 |
| `param_3` | 最终实际离地峰值目标 | 10 cm | 单位 cm，允许范围 5～25 cm；≤0 或未发送时沿用当前值 |
| `param_4` | 助力系数 | 0 | 范围 [0.0, 1.0]；0 = 0.5 倍速，1 = 1.0 倍速 |
| `param_6` | 基座高度 | — | 本任务不生效，由膝限角度与腿长自动计算 |
| `param_7` | DSP 原始足端抬升高度 | 0.10 m | 作用于高抬腿补偿前的 DSP 轨迹 |
| `param_8` | 双支撑期占比 | 0.2 | DSP 生成参数 |
| `switch_1` | 自动助力模式 | 未启用 | 启用后按实测髋关节力矩自动增减助力系数 |
| 左腿膝关节受限角度 | `grx.virtual_user_knee_restriction_left` | 0.0 rad | 与右腿输入取较大值；0.0 表示不限制 |
| 右腿膝关节受限角度 | `grx.virtual_user_knee_restriction_right` | 0.0 rad | 与左腿输入取较大值；0.0 表示不限制 |

> 轨迹参数在启动前生效；助力系数与自动助力在行走过程中实时生效。膝限越大，实际抬脚峰值越可能低于目标。

## 接口信息

| 参数 | 接口映射 |
|---|---|
| 目标抬脚峰值 | `grx.virtual_panel_command_param_3` |
| 助力系数 | `grx.virtual_panel_command_param_4` |
| 自动助力模式 | `grx.virtual_panel_command_switch_1` |
| 左 / 右腿膝关节受限角度 | `grx.virtual_user_knee_restriction_left` / `right` |
| 大腿 / 小腿长度 | `grx.virtual_user_upper_leg_length_*` / `grx.virtual_user_lower_leg_length_*` |
| 启动 / 停止 | `grx.virtual_panel_command_start` / `stop` |
| 当前助力系数 | `rehab.assist_ratio` |
| 参考轨迹、进度与步频 | `rehab.reference_joint_*`、`rehab.motion_ratio`、`rehab.step_frequency` |

## 原理解释

轨迹生成与膝限处理见[被动前向行走 高抬腿（膝受限）](/fourier-grx-M4/docs/tasks/knee_restriction_forward_walk_high_lift#原理解释)，回放速度与自动助力见[助力前向行走 高抬腿（dt 模式）](/fourier-grx-M4/docs/tasks/forward_walk_high_lift_assist_adjust_dt#原理解释)。本任务将两部分组合：先按共同膝限生成高抬腿参考轨迹，再按 `param_4` 或自动助力结果推进轨迹时钟。规划器 4509 复用同一模型，但不向机器人写入控制目标。

### 康复临床使用建议

先分别确认膝限、抬脚目标与回放速度，再进行组合训练。“助力增加”表示回放加快，并不表示输出更大辅助力矩；自动助力也不能替代平衡与防跌倒保护。

> 临床建议仅供专业人员参考，不替代医生/治疗师评估、产品说明书及医疗机构安全规范。

## 更新日志

- `fourier-grx` v4.4.90：新增膝受限高抬腿 dt 助力任务 4309 及规划器 4509；无膝限高抬腿 dt 助力规划器为 4412。
