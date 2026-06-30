---
layout: default
title: Fourier-GRX 固件
parent: 固件发布
nav_order: 1
has_toc: true
---

# Fourier-GRX 固件

* TOC
{:toc}

## 版本列表

| 发布日期 | 版本 | 下载 | 更新内容 | 支持状态 |
|----------|------|------|----------|----------|
| 2026-06-30 | **4.4.14** | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.14-linux-arm64-cpu-m4l-blaze.deb) | [详情](#4414) | ✅ 支持中 |
| 2026-06-30 | ~~4.4.13~~ | — | [详情](#4413) | ⚠️ 已撤销 |
| 2026-06-30 | ~~4.4.12~~ | — | [详情](#4412) | ⚠️ 已撤销 |
| 2026-06-30 | ~~4.4.11~~ | — | [详情](#4411) | ⚠️ 已撤销 |
| 2026-06-29 | ~~4.4.10~~ | — | [详情](#4410) | ⚠️ 已撤销 |
| 2026-06-29 | ~~4.4.9~~ | — | [详情](#449) | ⚠️ 已撤销 |
| 2026-05-22 | 4.4.8 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.8-linux-arm64-cpu-m4l-blaze.deb) | [详情](#448) | ✅ 支持中 |
| 2026-05-22 | 4.4.7 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.7-linux-arm64-cpu-m4l-blaze.deb) | [详情](#447) | ✅ 支持中 |
| 2026-05-14 | 4.4.6 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.6-linux-arm64-cpu-m4l-blaze.deb) | [详情](#446) | ✅ 支持中 |
| 2026-05-14 | 4.4.5 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.5-linux-arm64-cpu-m4l-blaze.deb) | [详情](#445) | ✅ 支持中 |
| 2026-05-13 | 4.4.4 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.4-linux-arm64-cpu-m4l-blaze.deb) | [详情](#444) | ✅ 支持中 |
| 2026-05-11 | 4.4.3 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.3-linux-arm64-cpu-m4l-blaze.deb) | [详情](#443) | ✅ 支持中 |
| 2026-04-10 | 4.4.2 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.2-linux-arm64-cpu-m4l-blaze.deb) | [详情](#442) | ✅ 支持中 |
| 2026-04-08 | 4.4.1 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.1-linux-arm64-cpu-m4l-blaze.deb) | [详情](#441) | ✅ 支持中 |
| 2026-04-03 | 4.4.0 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.0-linux-arm64-cpu-m4l-blaze.deb) | [详情](#440) | ✅ 支持中 |

## 安装方法

固件安装流程请参考 [固件安装和更新](/fourier-grx-M4/docs/quickstart/firmware)。

---

## 更新内容

### 4.4.14

> 📅 2026-06-30 &nbsp;·&nbsp; 平台：`linux/arm64`

🐛 **修复**

- **Stand 任务使能冲击（完整修复）**：`STAGE_INIT`、`STAGE_START`、`STAGE_WARM_UP` 三个阶段全面应用 `kp=0` 纯阻尼：
  - `STAGE_INIT`（从其他任务切换进来，1 tick）：新增 `output_joint_position = measured_position`，`kp=0`，避免 PD 帧以零位置为目标
  - `STAGE_START`（任意激活路径的入口 tick）：`kp=0`，目标位置跟随实测
  - `STAGE_WARM_UP`（持续 0.5 s）：`kp=0`，目标位置持续跟随实测；超时后以当前实测位置为插值起点，恢复正常增益，进入 `STAGE_PROCESS_01`
  - 日志输出添加 stage 名称前缀，便于调试
  - 同样覆盖 `TaskM4LRotaryJointKneeRestrictionStand`（继承同一 `_function_meta`）

---

### ~~4.4.13~~ *(已撤销)*

> ⚠️ `STAGE_INIT` 缺少 `output_joint_position` 赋值，PD 帧目标为零。已在 4.4.14 修复。

---

### ~~4.4.12~~ *(已撤销)*

> ⚠️ `STAGE_WARM_UP` 位置放置不正确（基于对 FSM stage 管理的误解）。已在后续版本中修正。

---

### ~~4.4.11~~ *(已撤销)*

> ⚠️ 同上，`STAGE_WARM_UP` 设计有误。

---

### ~~4.4.10~~ *(已撤销)*

> ⚠️ kp=0 仅持续一个 tick，不足以抑制冲击；且 `STAGE_INIT` 在第二次激活时不再触发。

---

### ~~4.4.9~~ *(已撤销)*

> 📅 2026-06-29 &nbsp;·&nbsp; 平台：`linux/arm64`

> ⚠️ 该版本中对 `function_on_activate` 预置执行器目标位置的修改经验证无效（`SERVO_ON` 通信帧仅发送使能指令，不携带位置数据），已在 4.4.10 中回退，请勿使用此版本。

---

### 4.4.8

> 📅 2026-05-22 &nbsp;·&nbsp; 平台：`linux/arm64`

🔧 **修复 / 调整**

- **直线关节行程下限收紧**：将 `min_thigh_length` 和 `min_shank_length` 由 `-0.100 m` 调整为 `-0.095 m`，进一步限制大腿和小腿直线关节的最大压缩行程

---

### 4.4.7

> 📅 2026-05-22 &nbsp;·&nbsp; 平台：`linux/arm64`

🔧 **修复 / 调整**

- **直线关节行程下限放宽**：将 `fi_task_m4l_prismatic_joint_move_length` 中 `min_thigh_length` 和 `min_shank_length` 由 `-0.090 m` 调整为 `-0.100 m`，允许大腿和小腿直线关节向更大压缩方向运动

---

### 4.4.6

> 📅 2026-05-14 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **固件版本检测标志位**：新增 `flag_version_check_error`（`FlagState`，`0` = 正常，`1` = 异常）和 `version_check_error_info`（`List[str]`，异常详情列表）字段到 `DynalinkGRX`，并加入 `read_fields`，供上位机通过 Dynalink 接口实时轮询。检测范围涵盖 IOBoard、FSA 执行器、FSE 传感器的固件版本不一致、无响应及异常情况

---

### 4.4.5

> 📅 2026-05-14 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **节点版本信息打印**：机器人初始化时查询并打印所有节点的固件版本信息，输出顺序为 IOBoard → FSA 执行器 → FSE 传感器，便于快速确认各硬件节点的实际固件状态
- **固件版本一致性校验**：配置文件新增 `expected_firmware_version` 字段（可选），启动时将节点实际版本与预期版本对比，版本不匹配时打印 `WARNING` 告警；省略该字段则不启用校验。M4LT2 各配置已预填 IOBoard 预期版本（`1.0.0.2`）及 FSA 预期版本（`3.104.225.222`）；M4LP1 / M4LT1 各配置已预填 IOBoard 预期版本（`1.0.0.2`）

---

### 4.4.4

> 📅 2026-05-13 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **`fourier-grx update` 命令**：新增命令行更新工具，可自动检测当前安装的软件包变体，向服务器探测可用的新版本，以交互式列表引导用户选择并完成下载安装。支持 `fourier-grx update`（自动检测变体）、`fourier-grx update <variant>`（手动指定变体，适用于旧版安装包）和 `fourier-grx update --help`。详见 [命令行工具 · update](/fourier-grx-M4/docs/reference/command_line_tool#fourier-grx-update-详细说明)
- **`X-Variant` deb 控制字段**：安装包的 deb 控制文件中新增 `X-Variant` 字段，记录平台/机型标识符（如 `linux-arm64-cpu-m4l-blaze`），供 `fourier-grx update` 自动识别当前变体

🔧 **修改**

- Makefile 新增 `BUILDTYPE` 目标级变量（`nuitka` / `pyinstaller` / `blaze` / `test`），修复各构建目标生成的 deb 包文件名中版本号错误的问题

---

### 4.4.3

> 📅 2026-05-11 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **M4LT2 急停高阻尼保护任务**（TID 4600）：硬件急停开关（ioboard）触发后，关节不再直接断电，自动切换到高阻尼模式（`kp=0`、`kd=80`），防止肢体瞬间跌落。详见 [高阻尼保护任务说明](/fourier-grx-M4/docs/tasks/emergency_stop_high_damping)
- **助力原地踏步（DT 模式）触发力配置接口**：新增 `assist_trigger_force_upper` / `assist_trigger_force_lower` 参数，默认值 `2.0 Nm` / `1.0 Nm`，通过面板 `param_4` / `param_5` 设置，适用于 TID 4119、TID 4306

🔧 **修改**

- 助力触发力阈值改为绝对力矩值：计算式由 `G[i] + offset` 改为 `G[i] * 0.0 + offset`（重力分量清零），经实验验证加入 `G[i]` 项会引发系统不稳定

---

### 4.4.2

> 📅 2026-04-10 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **HXC 全身 RL CPG 行走任务**（TID 3302，适用 HXCT1）：控制 12 个腿部关节（位置控制），4 个轮式关节（索引 12–15）以 PD 制动方式锁定零速度（`kp=0, kd=10`）

🐛 **修复**

- 修复 `fourier-core`：`fi_fsa_v2.5` 编码器零点无法写入的问题

---

### 4.4.1

> 📅 2026-04-08 &nbsp;·&nbsp; 平台：`linux/arm64`

🐛 **修复**

- 修复配置文件键名错误：机器人名称字段由 `robot_name` 改为 `name`，与 YAML 配置文件实际结构对齐

🔧 **修改**

- 将 `pdm` 和 `PyInstaller` 加入 `dependencies.sh` 依赖脚本
- 新增 `build_pyinstaller.py` 支持 M4L 打包构建
- 新增 `fi_fsa_v3` PyInstaller 运行时钩子（`rthook_fi_fsa_v3.py`），确保 M4LT2 所需库在打包后正常加载

---

### 4.4.0

> 📅 2026-04-03 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **M4LP1** 硬件型号支持（带直线关节的新变体）
  - 直线关节自动标定（自动检测行程上下限并归零）
  - 直线关节移动到指定长度任务
  - 旋转关节标定改为"到边界后返回"方案，提升可靠性
- **M4LT2** 硬件型号支持（FSA v3 异步通信协议），与 M4LT1 共用所有算法和任务
- **膝关节受限模式**任务集（Knee Restriction），适用于膝关节活动度受限场景：
  - 站立姿态控制（TID 4300）
  - 被动前向行走（TID 4301）、被动原地踏步（TID 4302）
  - 助力前向行走—PD（TID 4303）、助力原地踏步—PD（TID 4304）
  - 助力前向行走—DT（TID 4305）、助力原地踏步—DT（TID 4306）
- **助力模式细分**：PD 参数调节与 DT 时序调节拆分为独立任务：
  - 助力前向行走—PD（TID 4116）、助力原地踏步—PD（TID 4117）
  - 助力前向行走—DT（TID 4118）、助力原地踏步—DT（TID 4119）
- **规划器**（Planner）：轨迹规划附属任务，设备保持失能，供上位机展示关节轨迹（TID 4401–4406）
- 旋转关节自动标定任务（TID 4120）：三步完成边界检测 → 下电垂落 → 零点写入
- 键盘快捷键输入支持
- IO 板通信和读写支持

🐛 **修复**

- 修复直线关节长度标定中的多处问题
- 修复标志位设置与清除的异常
- 修复 `virtual_panel` 面板不工作的问题
- 修复行走过程中的若干问题

🔧 **修改**

- 优化助力模式（DT 算法）PD 参数，提升响应硬度
- 优化负载/能量检测算法，降低误触发率
- 改进步态生成器在膝关节受限场景下的稳定性
- 打包流程支持 `fi_fsa_v3` 库的 PyInstaller 打包
