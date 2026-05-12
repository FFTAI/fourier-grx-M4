---
layout: default
title: 固件发布
nav_order: 7
has_toc: true
---

# 固件发布

* TOC
{:toc}

## 最新版本

> **Fourier-GRX `4.4.3`** · 2026-05-11 · 平台：`linux/arm64` · [立即下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.3-linux-arm64-cpu-m4l-blaze.deb)

## 正式版本

### Fourier-GRX 固件

| 发布日期 | 版本 | 下载 | 更新内容 | 支持状态 |
|----------|------|------|----------|----------|
| 2026-05-11 | **4.4.3** | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.3-linux-arm64-cpu-m4l-blaze.deb) | [详情](#443) | ✅ 支持中 |
| 2026-04-10 | 4.4.2 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.2-linux-arm64-cpu-m4l-blaze.deb) | [详情](#442) | ✅ 支持中 |
| 2026-04-08 | 4.4.1 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.1-linux-arm64-cpu-m4l-blaze.deb) | [详情](#441) | ✅ 支持中 |
| 2026-04-03 | 4.4.0 | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/fourier-grx-4.4.0-linux-arm64-cpu-m4l-blaze.deb) | [详情](#440) | ✅ 支持中 |

### Fourier-M4 固件

| 发布日期 | 版本 | 下载 | 更新内容 | 支持状态 |
|----------|------|------|----------|----------|
| 2025-07-22 | 2.0.6 | [⬇ 下载](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.6.deb) | [详情](#206) | ❌ 已停止 |
| 2025-06-09 | 2.0.5 | [⬇ 下载](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.5.deb) | [详情](#205) | ❌ 已停止 |

### IO Board 固件

| 发布日期 | 版本 | 下载 | 更新内容 | 支持状态 |
|----------|------|------|----------|----------|
| 2026-05-11 | **1.0.0.3** | [⬇ 下载](https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/m4/ioboard_v1.0.0.3_20260511.zip) | [详情](#1003) | ✅ 支持中 |

## 安装方法

固件安装流程请参考 [固件安装和更新](/fourier-grx-M4/docs/quickstart/firmware)。

---

## 更新内容

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

�� **修复**

- 修复直线关节长度标定中的多处问题
- 修复标志位设置与清除的异常
- 修复 `virtual_panel` 面板不工作的问题
- 修复行走过程中的若干问题

🔧 **修改**

- 优化助力模式（DT 算法）PD 参数，提升响应硬度
- 优化负载/能量检测算法，降低误触发率
- 改进步态生成器在膝关节受限场景下的稳定性
- 打包流程支持 `fi_fsa_v3` 库的 PyInstaller 打包

---

### 1.0.0.3

> 📅 2026-05-11 &nbsp;·&nbsp; 平台：ESP32-WROOM-32D

🔧 **修改**

- **急停按键消抖**：GPIO 34 新增 50ms 软件消抖，防止机械抖动引发 TRIGGERED / released 反复打印

---

### 2.0.6

> 📅 2025-07-22

🐛 **修复**

- 修复站立状态下放下设备无法触发力量保护的问题

🔧 **修改**

- M4LV3 控制周期由 `0.03s` 修正为 `0.025s`（提速约 1/6），踏步速度相应提升；稳定性风险待进一步验证

⚠️ **已知限制**

- 行走过程中无力量保护（历史版本未实现，需求尚未确认）
- 位置保护在向后运动时无法触发（问题难以修复，出现频率待确认）

---

### 2.0.5

> 📅 2025-06-09

🐛 **修复**

- 修复原地踏步助力模式下容易误触发助力运动的问题
