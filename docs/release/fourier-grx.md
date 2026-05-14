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
| 2026-05-14 | **4.4.6** | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.6-linux-arm64-cpu-m4l-blaze.deb) | [详情](#446) | ✅ 支持中 |
| 2026-05-13 | 4.4.4 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.4-linux-arm64-cpu-m4l-blaze.deb) | [详情](#444) | ✅ 支持中 |
| 2026-05-11 | 4.4.3 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.3-linux-arm64-cpu-m4l-blaze.deb) | [详情](#443) | ✅ 支持中 |
| 2026-04-10 | 4.4.2 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.2-linux-arm64-cpu-m4l-blaze.deb) | [详情](#442) | ✅ 支持中 |
| 2026-04-08 | 4.4.1 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.1-linux-arm64-cpu-m4l-blaze.deb) | [详情](#441) | ✅ 支持中 |
| 2026-04-03 | 4.4.0 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.0-linux-arm64-cpu-m4l-blaze.deb) | [详情](#440) | ✅ 支持中 |

## 安装方法

固件安装流程请参考 [固件安装和更新](/fourier-grx-M4/docs/quickstart/firmware)。

---

## 更新内容

### 4.4.6

> 📅 2026-05-14 &nbsp;·&nbsp; 平台：`linux/arm64`

✨ **新增**

- **固件版本检测标志位**：新增 `flag_version_check_error`（`FlagState`，`0` = 正常，`1` = 异常）和 `version_check_error_info`（`List[str]`，异常详情列表）字段到 `DynalinkGRX`，并加入 `read_fields`，供上位机通过 Dynalink 接口实时轮询。检测范围涵盖 IOBoard、FSA 执行器、FSE 传感器的固件版本不一致、无响应及异常情况

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
