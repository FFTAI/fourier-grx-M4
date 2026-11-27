---
layout: default
title: 助力前向行走 谐波拟合（膝受限，PD 模式）
parent: 任务描述
nav_order: 4.303
has_toc: true
---

# 助力前向行走 谐波拟合（膝受限，PD 模式）

## 任务信息

| 任务 | 任务值 (TID) | 控制方式 |
|---|---|---|
| 助力前向行走 谐波拟合（膝受限，PD 模式） | **4310** | 助力（PD 模式） |

适用机型：M4L（P1 / T1 / T2）。对应规划器 **4510**，只生成和上报参考轨迹，不驱动关节。无虚拟用户膝限版本为 **4132**，其规划器为 **4408**。

任务描述：

- 复用[助力前向行走 谐波拟合（4132）](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd)的系数表轨迹与 PD 助力逻辑，并增加虚拟用户左右伸膝限制输入。
- `param_2` 选择系数表自带的伸膝限制等级；虚拟用户角度作为额外双膝角下限，两者叠加，最终膝角不低于其中更严格的限制。
- 助力系数在 buttery 与 soft 之间插值 PD 增益，只在启动阶段写入一次；负载检测与自动 PD 爬升关闭。
- 谐波曲线由系数表决定，步长、步速、`param_6` 基座高度及膝限任务的基座高度计算均不改变轨迹。

任务参数：

| 面板/用户参数 | 含义 | 默认值 | 说明 |
|---|---|---|---|
| `param_1` | 髋摆动幅度等级 | 2 | 1～4 档 |
| `param_2` | 系数表伸膝限制等级 | 1 | 1～4 档，对应 0 / 5 / 10 / 15° |
| `param_3` | 步频等级 | 3 | 1～6 档；≤0 沿用当前档 |
| `param_4` | 助力系数 | 0 | 范围 [0.0, 1.0]；0 = buttery，1 = soft；启动阶段锁存 |
| 左腿膝关节受限角度 | `grx.virtual_user_knee_restriction_left` | 0.0 rad | 与右腿输入取较大值，作为额外共同下限 |
| 右腿膝关节受限角度 | `grx.virtual_user_knee_restriction_right` | 0.0 rad | 与左腿输入取较大值，作为额外共同下限 |

> `param_1`～`param_3` 与虚拟用户膝限在启动前生效；`param_4` 需重新启动任务后更新。`rehab.gait_knee_restriction_deg` 回显 `param_2` 的系数表档位，不包含额外虚拟用户膝限。

## 接口信息

| 参数 | 接口映射 |
|---|---|
| 幅度 / 系数表膝限 / 步频 | `grx.virtual_panel_command_param_1` / `param_2` / `param_3` |
| 助力系数 | `grx.virtual_panel_command_param_4` |
| 左 / 右腿膝关节受限角度 | `grx.virtual_user_knee_restriction_left` / `right` |
| 启动 / 停止 | `grx.virtual_panel_command_start` / `stop` |
| 当前助力系数 | `rehab.assist_ratio` |
| 参考轨迹、进度与步频 | `rehab.reference_joint_*`、`rehab.motion_ratio`、`rehab.step_frequency` |

## 原理解释

轨迹首先按 `param_1` 与 `param_2` 从系数表生成，再以 `θ=max(θ_left,θ_right)` 对左右膝角施加额外下限，并重新差分计算膝角速度。髋曲线和基座高度不因额外膝限重解。PD 助力原理见[助力前向行走 谐波拟合（PD 模式）](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd)。

### 康复临床使用建议

额外膝限会直接裁切系数表膝角，可能改变曲线形状；应先预览规划器 4510，再确认系数表档位、额外膝限与 PD 刚度的组合。出现疼痛或支撑侧不稳时，降低限制或助力目标并重新评估。

> 临床建议仅供专业人员参考，不替代医生/治疗师评估、产品说明书及医疗机构安全规范。

## 更新日志

- 开发中：新增谐波膝受限 PD 助力任务 4310 及规划器 4510，支持系数表膝限与虚拟用户额外膝限叠加。
