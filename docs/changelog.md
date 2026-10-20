---
layout: default
title: 更新日志
nav_order: 8
has_toc: true
---

# 更新日志

{:toc}

本文档记录了 Fourier-GRX-M4 SDK 及其文档的所有重要更新。

## 2026 年 10 月

### v1.2.23 (2026-10-20)

**发布**

- 📦 `fourier-grx` **v4.4.59 正式发布**：`fourier-grx-4.4.59-linux-arm64-cpu-m4l-blaze.deb`（2026-10-20 14:48 构建，分支 `m4-lfs`），安装方式 `fourier-grx update`（自动探测）或 `fourier-grx update 4.4.59`
- 📋 [固件版本表](/fourier-grx-M4/docs/release/fourier-grx)补 4.4.59 行与更新内容小节，4.4.58 转不再支持。本版要点：修复直线关节自动校准电机不动与旋转标定扫掠位置保护误触发（均自 v4.4.49 起存在；**用 v4.4.49 ~ 4.4.58 做过直线关节自动校准的机器请升级后重新校准**）；其余与 4.4.58 相同
- 📄 [校准零点（直线关节）](/fourier-grx-M4/docs/tasks/calibrate_home_prismatic_joint)与[自动校准（旋转关节）](/fourier-grx-M4/docs/tasks/rotary_joint_auto_calibrate)页去掉「正式版待发布」标注并补发布页链接。中英文同步

### v1.2.22 (2026-10-20)

**发布**

- 📦 预发布渠道更新为 `fourier-grx` **v4.4.59**：`fourier-grx-4.4.59-linux-arm64-cpu-m4l-prerelease.deb`（2026-10-20 14:37 构建，分支 `m4-lfs`），安装方式 `fourier-grx update 4.4.59-prerelease`
- 🔧 本版内容：**修复直线关节自动校准电机不动**。v4.4.49 引入的任务层输出限位钳制（防步态生成器越界指令）破坏了标定扫掠任务「指令越过软件限位 ±0.2 m 以顶到机械硬限位」的设计——直线关节行程仅 0.098 m，目标被钳回后若关节已抵近限位，目标等于实测位置、电机完全不动，随后在纯速度判据下误报到位并直接归零。标定扫掠类任务（直线 MoveMin / MoveMax、旋转 BorderAndReturn）现豁免该钳制、恢复越界指令；旋转标定扫掠的位置保护边界由「激活时位置 ± 0.25 rad」放宽为「硬件限位 ± 裕量」，避免扫掠中途误触发位置保护而伺服下电；MoveMax 到位日志文案 min→max 修正；进度日志按 1% 步进限速（单次扫掠 6000 行 → 约 100 行）
- 📄 [校准零点（直线关节）](/fourier-grx-M4/docs/tasks/calibrate_home_prismatic_joint)与[自动校准（旋转关节）](/fourier-grx-M4/docs/tasks/rotary_joint_auto_calibrate)页更新日志同步，[Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx)页「当前预发布」指向 4.4.59。中英文同步

### v1.2.21 (2026-10-20)

**发布**

- 📦 `fourier-grx` **v4.4.58 正式发布**：`fourier-grx-4.4.58-linux-arm64-cpu-m4l-blaze.deb`（2026-10-20 13:34 构建，分支 `m4-lfs`），安装方式 `fourier-grx update`（自动探测）或 `fourier-grx update 4.4.58`
- 📋 [固件版本表](/fourier-grx-M4/docs/release/fourier-grx)补 4.4.58 行与更新内容小节，4.4.57 转不再支持。本版要点：直线关节到位判定的纯速度计时由 5 s 增至 25 s，消除校准行程末段在接触限位前约 3.5 mm 处的提前到位误判；其余功能与 4.4.57 相同
- 📄 [直线关节零点校准](/fourier-grx-M4/docs/tasks/calibrate_home_prismatic_joint)页去掉「正式版待发布」标注并补发布页链接。中英文同步

### v1.2.20 (2026-10-20)

**发布**

- 📦 预发布渠道更新为 `fourier-grx` **v4.4.58**：`fourier-grx-4.4.58-linux-arm64-cpu-m4l-prerelease.deb`（2026-10-20 13:23 构建，分支 `m4-lfs`），安装方式 `fourier-grx update 4.4.58-prerelease`
- 🔧 本版内容：**直线关节到位判定纯速度计时由 5 s 增至 25 s**。校准行程（120 s S 曲线）末段 r > 0.8295 的参考速度自然低于 0.001 m/s 判据门限且持续约 20.5 s，原 5 s 连续计时在关节尚未接触限位时即可能误判到位（最迟约在行程开始 + 104.5 s、距硬限位约 3.5 mm 处），污染零点标定；25 s 大于该末段窗口，自由跟踪全程不再触发，代价是力矩建立不足场景的兜底判定延迟变为接触后 + 25 s
- 📄 [直线关节零点校准](/fourier-grx-M4/docs/tasks/calibrate_home_prismatic_joint)页的到位判据表与更新日志同步，[Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx)页「当前预发布」指向 4.4.58。中英文同步

### v1.2.19 (2026-10-19)

**发布**

- 📦 `fourier-grx` **v4.4.57 正式发布**：`fourier-grx-4.4.57-linux-arm64-cpu-m4l-blaze.deb`（2026-10-19 17:49 构建，分支 `m4-lfs`），安装方式 `fourier-grx update`（自动探测）或 `fourier-grx update 4.4.57`
- 📋 [固件版本表](/fourier-grx-M4/docs/release/fourier-grx)补 4.4.57 行与更新内容小节，4.4.54 转不再支持。本版要点：M4LP1 启动即崩溃缺陷修复（影响面 v4.4.52 ~ 4.4.56-prerelease，**P1 请直接升级 v4.4.57**）；谐波系数前向行走 4113 与规划器 4407 正式提供；旋转关节 PD hard 档 kp 统一为 `[500,500,500,500]`（T1 / T2 起步刚度下降，⚠️ 行为变化）
- ℹ️ v4.4.55 / v4.4.56 周期的功能随本版一并正式发布，这两个版本号未单独发布正式版
- 📄 [谐波系数前向行走](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)与[规划器](/fourier-grx-M4/docs/tasks/planner)页去掉「正式版待发布」标注并补发布页链接。中英文同步

### v1.2.18 (2026-10-19)

**发布**

- 📦 预发布渠道更新为 `fourier-grx` **v4.4.57**：`fourier-grx-4.4.57-linux-arm64-cpu-m4l-prerelease.deb`（2026-10-19 17:35 构建，分支 `m4-lfs`），安装方式 `fourier-grx update 4.4.57-prerelease`
- 🔧 本版内容：**旋转关节 PD hard 档 kp 统一为 500**。M4LP1 与 M4LT1/T2 参数类的 hard 档由 `[600,500,600,500]`（髋/膝区分）调整为 `[500,500,500,500]`，kd 维持 `[30,30,30,30]`。M4LT1 / M4LT2 的 rotary 基线增益是 hard 档副本，全部旋转关节任务（站立 / 前向行走 / 原地踏步 / 标定 / 测试）的起步增益随之由髋 600 · 膝 500 变为统一 500，动作手感变软；M4LP1 基线仍为 `[250×4]` 软起步，仅负载爬升终点统一为 500。assist_adjust_pd 类的 buttery / soft 柔顺插值手感不受影响
- 📄 [谐波系数前向行走](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)、[规划器](/fourier-grx-M4/docs/tasks/planner) 与 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 页的版本标注同步更新。中英文同步

### v1.2.17 (2026-10-19)

**文档改进**

- 重写根目录 README，补充仓库定位、在线文档入口、文档导航、示例分类、目录结构与贡献说明
- 补齐中英文快速开始首页，按设备状态分流到现有安装、升级、烧录和机型流程，并说明安装后的使用路径
- 澄清本仓库 `demo/` 与外部 `Wiki-GRx-Deploy` 示例的来源和适用场景，修复中文示例总览的子页面导航配置
- 完善中英文贡献指南，补充问题反馈、双语同步、front matter 与提交前检查要求

### v1.2.16 (2026-10-16)

**发布与缺陷修正**

- 📦 预发布渠道更新为 `fourier-grx` **v4.4.56**：`fourier-grx-4.4.56-linux-arm64-cpu-m4l-prerelease.deb`（2026-10-16 12:35 构建，分支 `m4-lfs`），安装方式 `fourier-grx update 4.4.56-prerelease`
- 🐛 修正 M4LP1 控制线程启动即退出：关节保护的消抖计数器与门限原先在 `RobotM4L._init_actuator()` 里初始化，而 `RobotM4LP1` 整体覆盖了该方法且不调用 `super()`，导致 `flag_joint_over_load_protection_counter_threshold` 缺失，控制线程在第 1 个控制周期读该属性时抛 `AttributeError` 而终止。计数器改由基类构造统一初始化，机型覆盖 `_init_actuator()` 无法再绕过；限速与限位保护的计数器此前在同一风险面上（读取点被外层开关保护才未暴露），一并消除。M4LT1 / M4LT2 不覆盖该方法，不受影响
- ⚠️ **`4.4.55-prerelease` 请勿在 M4LP1 上安装**；该缺陷自 v4.4.52 起存在于 v4.4.52 ~ v4.4.55。P1 请使用 `4.4.56-prerelease` 及以上
- 📄 [谐波系数前向行走](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)、[规划器](/fourier-grx-M4/docs/tasks/planner) 与 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 页的版本标注同步更新。中英文同步

### v1.2.15 (2026-10-16)

**发布**

- 📦 `fourier-grx` **v4.4.55 预发布包**已构建并上传预发布渠道：`fourier-grx-4.4.55-linux-arm64-cpu-m4l-prerelease.deb`（2026-10-16 11:35，构建分支 `m4-lfs`，`X-Variant` = `linux-arm64-cpu-m4l-prerelease`）
- ⬇️ 安装方式：`fourier-grx update 4.4.55-prerelease`，随后执行 `fourier-grx install` 完成部署。该包不会被 `fourier-grx update` 的无参自动探测发现，也不列入[固件版本表](/fourier-grx-M4/docs/release/fourier-grx)
- ✨ 本版内容：谐波系数前向行走任务 [TID 4113](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic) 与其[规划器 TID 4407](/fourier-grx-M4/docs/tasks/planner)，`rehab/server` 新增 5 个步态档位回显字段，规划器停用时的清零范围扩展至 `rehab.gait_*`
- ✅ 正式版已随 **v4.4.57** 发布（2026-10-19），下载链接见[固件版本表](/fourier-grx-M4/docs/release/fourier-grx)（4.4.55 / 4.4.56 未单独发布正式版）

### v1.2.14 (2026-10-16)

**文档更新**

- ➕ [规划器](/fourier-grx-M4/docs/tasks/planner)页新增 **谐波系数前向行走规划器（TID 4407）**：4113 的只规划版本，面板三条档位（`param_1` 幅度 / `param_2` 伸膝限制 / `param_3` 步频）照常每个控制周期生效，但不向关节下发指令，供上位机在患者开始运动前预览 4 × 4 = 16 条曲线的关节包络与 6 档节奏；附完整上报字段表与 4 × 4 包络对照表。中英文同步
- 🔧 补充规划器页两处此前未记载的行为：规划器虽不驱动关节，每周期仍会并入关节位置保护包络（只放宽、不收窄，复位后恢复）；停用时清零范围已扩展至 `rehab.gait_*` 全部档位回显字段
- 📡 `rehab/server` 状态接口表中 5 个步态回显字段的发布方由「4113」改为「4113 / 4407」。中英文同步
- 🔧 修正 `rehab/server` 中 4 个参考轨迹数组字段的说明：补上数组顺序 **[左髋, 左膝, 右髋, 右膝]**（步态类任务长度均为 4，实测覆盖 4111 / 4112 / 4113 / 4116 / 4117 / 4301 / 4302 / 4401 / 4407 / 4501，全家族一致）；并把 `reference_joint_position_max/min` 的统计范围由「整段轨迹」更正为「循环段（不含起步与结束过渡段）」，与代码实际行为对齐。中英文同步
- ✅ 上述功能自 **v4.4.57** 起正式发布（2026-10-19；此前经 4.4.55 ~ 4.4.57 预发布包提供）

### v1.2.13 (2026-10-16)

**文档更新**

- ➕ 新增任务页 [谐波系数前向行走](/fourier-grx-M4/docs/tasks/rotary_joint_forward_walk_harmonic)（TID 4113，M4L）：回放 Fourier 谐波系数步态曲线，**髋摆动幅度档**（`param_1`）、**伸膝限制档**（`param_2`）、**步频档**（`param_3`）三条正交通道；步频 22.9 ~ 49.2 步/分，对应技术要求 2.45 ~ 5.25 s/大步。中英文同步，并已加入任务总表与任务索引
- 📡 `rehab/server` 状态接口表补充 5 个步态回显字段：`gait_name`、`gait_amplitude_level`、`gait_knee_restriction_deg`、`gait_speed_level`、`gait_stride_time_s`（中英文同步）
- ⚠️ 该功能自 `fourier-grx` v4.4.55 起提供（本条目撰写时尚未定版本号，写作「大于 v4.4.54」，现确定为 v4.4.55，见 v1.2.15）；正式发布后需在 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 版本表补录下载链接

### v1.2.12 (2026-10-15)

**文档更新**

- 📦 `fourier-grx` v4.4.54 正式发布（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx#4454) 发布页），v4.4.53 转为不再支持。本次为缺陷修复版本：膝关节受限任务 4301 / 4302 的力矩保护恢复生效、4303 / 4304 / 4305 的助力系数恢复可调、原地踏步 4112 支持面板暂停指令、`*_sdk.yaml` 补齐 `communication` 段使 SDK User API 的 UDP 通道可用
- 🔧 相应撤销 6 个任务页中的「本接口不生效」标注，并恢复 4112 页面被删除的「暂停运动标志位」参数行与接口映射行（中英文同步）

---

### v1.2.11 (2026-10-15)

**文档修正**

- 🔧 **命令行工具**：删除实际不存在的 `setup_conda`，更正为 `setup_uv` / `setup_uv_py310` 并补上 `web` 子命令；`fourier-grx update <variant>` 更正为 `update <version>` 与 `update <version>-<渠道>`（机型变体一律自动读取，不能作为参数传入）；新增「安装的两个层次」，说明 `sudo dpkg -i` 只更新 `/usr/share/fourier-grx/`、`fourier-grx install` 才把新版本部署到 `~/fourier-grx/`；补充 `fourier-grx web` 参数表（`--host` 是机器人 IP，`--bind` 才是 web 监听地址，默认 `0.0.0.0:8000`）
- 📦 [固件发布](/fourier-grx-M4/docs/release) 页 Fourier-GRX 最新版本由 4.4.43 更正为 **4.4.53**；[Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx#预发布渠道) 新增「预发布渠道」小节 —— `-prerelease` 只替换 `X-Variant` 末段的构建类型，机型段保留，因此自动探测不会发现预发布包；v4.4.52 未正式发布，不提供下载链接
- 🆕 [M4L 机器人](/fourier-grx-M4/docs/quickstart/m4l#局域网网页调试) 新增「局域网网页调试」一节：`fourier-grx web` 启动与自动发现、实时状态、任务下发、虚拟面板、运行日志，以及面板值锁存的安全提示
- 🔧 **固件更新**：补充 `fourier-grx update <版本>-prerelease` 用法；说明 `fourier-grx install` 会先备份 `~/fourier-grx` 为 `~/fourier-grx-bak` 并优先沿用旧配置，以及网络参数会被无条件重置为静态 IP
- 🔧 **运行模式**：补上 `B` 服务器模式（`server`），离线调试模式（`offline`）的编号由 `B` 更正为 `C`
- 🔧 **启动配置文件**：修正 `dynalink: enable`、`joystick_type`、`keyboard_type`、`robot: name`、通信周期等项的默认值与可选项，补充 `use_virtual_panel` / `use_virtual_user`
- 🔧 开发环境 FAQ：GLIBC 最低版本由 2.33 更正为 2.34
- 🗑️ 移除 M4 / M4L 快速开始页中没有内容的「视频教程」小节
- 🔗 下载链接体检：早于 4.4.40 的安装包（含 4.4.41）已从下载服务器移除（实测 404），[固件发布页](/fourier-grx-M4/docs/release/fourier-grx)中这 32 个版本的下载列改为「已下架」占位，版本行与更新内容保留可查；快速开始页中作为示例的 `wget` 版本号改用仍在线的 4.4.53
- 🐞 **任务文档事实校正**：TID 4112 声明的「暂停运动」接口 `grx.virtual_panel_command_pause` 实际从未被该任务读取，已从参数表与接口映射表移除；膝关节受限系列的力矩保护（4301 / 4302）与助力系数（4303 / 4304 / 4305）在当前固件中未接入算法调用，已在对应页面标注为「不生效」并给出替代任务；力矩保护触发后的行为由「暂停任务」更正为「立即退出并回到 `TASK_IDLE`」；为 12 篇步态任务页补上遗漏的 `rehab.step_frequency` 状态接口；`dsp_ratio` 在使用 vhip 步态生成器的任务页更正为「不生效」
- 🔧 **示例代码**：`demo/user`、`demo/developer` 的 conda 相关说明改用 `setup_uv` 与 `source $HOME/fourier-grx/.venv/bin/activate`；`demo_set_home.py`、`demo_test_joint.py` 发送的 TID 999 / 902 在 M4L 上没有注册任何任务，已补充说明与替代任务（4103 / 4203、4100 / 4200）；`demo/udp/demo_get_state.py` 改为持续排空接收队列（状态推送约 250 包/秒，收一包睡一次会一直打印数秒前的旧数据）；`config_M4L_T1_developer.yaml` 补齐 `fi_ioboard` 段，并更正 `log_level: "none"` 的含义（等同输出全部日志，而非静默）
- 🔧 **任务页更新日志的版本归属**：按「首个包含该变更的发布版本」校正 —— 膝关节受限系列 v4.2.5 → v4.2.6、站立姿态控制 v3.0.3 → v3.1.1、4103 / 4206 v4.1.18 → v4.1.19；伺服上电 / 下电 / 重启与清除故障在公开版本历史的最早版本 v2.0.5 中即已存在，相应条目不再标注「新增」版本
- 🌐 **中英文切换**：修复中文首页（位于站点根目录）上「EN」按钮指向当前页、英文首页的「中文」按钮指向不存在页面的问题

---

### v1.2.10 (2026-10-14)

**文档更新**

- 📦 `fourier-grx` v4.4.53 正式发布：补录发布说明与下载链接，v4.4.51 转为不再支持（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）
- 📖 预发布渠道 `fourier-grx update <版本>-prerelease` 语法自 v4.4.53 起可用，更早版本需 `sudo dpkg -i` 手动安装
- ℹ️ v4.4.52 未正式发布，版本号由 4.4.51 直接进入 4.4.53

---

### v1.2.9 (2026-10-14)

**文档更新**

- 📖 **固件发布条目补齐**：补录 v4.4.49（内置 web 调试上位机、升级保留配置）、v4.4.50（web 界面二级分组/中文参数标签/虚拟用户腿长下发）、v4.4.51（虚拟面板草稿模式）三个已正式发布版本的中英文发布说明
- 🆕 **新增任务文档**：左腿 / 右腿旋转关节单独手动校准 `TASK_ROTARY_JOINT_MANUAL_CALIBRATE_LEFT_LEG`（4122）/ `TASK_ROTARY_JOINT_MANUAL_CALIBRATE_RIGHT_LEG`（4123），中英文任务索引与手动校准任务页同步更新；这两个任务自 v4.4.53 起提供
- ℹ️ **关于 v4.4.52 / v4.4.53**：这两个版本目前仅提供预发布构建（不在本页下载列表中）。预发布构建不会被 `fourier-grx update` 的自动探测发现，需显式安装：`fourier-grx update <版本>-prerelease`（例如 `fourier-grx update 4.4.53-prerelease`）。正式发布后将按本页惯例补录下载链接

---

### v1.2.8 (2026-10-10)

**文档更新**

- 📖 新增步态任务参数接口说明（对应 `fourier-grx` v4.4.48）：基座高度 base_height（`grx.virtual_panel_command_param_6`）、抬腿高度 step_height（`grx.virtual_panel_command_param_7`，仅前向行走类任务）、双支撑期占比 dsp_ratio（`grx.virtual_panel_command_param_8`，仅前向行走类任务且仅 DSP 步态生成器生效）；涉及前向行走、助力前向行走、膝限位前向行走、原地踏步、助力原地踏步等任务页面，中英文文档同步更新

---

### v1.2.7 (2026-10-10)

**新增功能**

- 📈 `rehab/server` 接口新增 `step_frequency` 字段：步态任务（前向行走/原地踏步系列）与轨迹规划（Planner）任务自动生成并实时上报步频（步/分钟），随步长/速度指令变化更新，任务退出自动清零，上位机可用于步频显示与训练量统计（详见 [User 接口](/fourier-grx-M4/docs/reference/user)）

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.47`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

### v1.2.6 (2026-10-10)

**优化**

- ⚙️ 过力保护（over_load）加入 5 周期消抖：关节力矩连续 5 个控制周期（100 ms）超过阈值才触发失能，避免电流/力矩测量尖峰误触发；持续过力场景保持每 5 周期重复强制失能的安全语义

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.46`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

### v1.2.5 (2026-10-10)

**优化**

- ⚙️ 速度保护阈值由 15 rad/s 标定为 **4.5 rad/s**（约 258°/s）：依据真机实测正常步态峰值约 3.5 rad/s、人工拉扯极限约 240~260°/s；旧值超过执行器物理速度上限，实际无法触发
- ⚙️ 位置保护裕量由 0.35 rad 标定为 **0.25 rad**（约 14.3°）：依据真机实测超出 15° 即为极限，覆盖最差跟踪偏差约 0.21 rad
- ⚙️ 位置保护边界与任务层目标位置均钳制到硬件限位，防止极端参数组合指令越界

**修复**

- 🐛 修复步态生成器 `atan2` 分支跳变导致关节猛甩的安全隐患：大步长+慢速停车过渡时关节实测速度可达 12.5 rad/s，现按帧序列 unwrap 消除跳变后降至 0.95 rad/s

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.45`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

### v1.2.4 (2026-10-08)

**新增功能**

- 🛡️ 新增关节速度保护：持续监测 4 个旋转关节速度，连续 5 个控制周期超过阈值（默认 15 rad/s，可真机标定）时自动失能进入保护态
- 🛡️ 新增关节位置保护：关节位置大幅超出任务发布的合理运动范围（随任务与步态参数自动调整）时自动失能进入保护态
- 🔧 两种保护均置位独立标志位（`flag_robot_velocity_protection` / `flag_robot_position_protection`），并锁存保护态；上位机可通过 `clear_flag_robot_velocity_protection` / `clear_flag_robot_position_protection` 清错并恢复控制
- 📖 详见 [速度保护与位置保护](/fourier-grx-M4/docs/reference/protection) 文档

**修复**

- 🐛 修复过载保护（`flag_robot_over_load`）清错请求不生效的问题：此前上位机写入 `clear_flag_robot_over_load` 后，机器人侧标志位未被清除，下一通信周期即被重新置位

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.44`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

## 2026 年 9 月

### v1.2.3 (2026-09-01)

**优化**

- ⚙️ 上位机心跳计时逻辑优化：心跳超时计时从**第一次收到** `host_heartbeat_counter` 时开始，在此之前不触发断连保护

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.43`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

## 2026 年 8 月

### v1.2.2 (2026-08-28)

**新增功能**

- 🛡️ 新增上位机心跳与断连保护机制：
  - `comm` topic 新增可写字段 `host_heartbeat_counter`，上位机持续写入即可维持连接
  - 新增可读字段 `host_heartbeat_timeout`（默认 6.0 s）与 `host_heartbeat_connection_lost`
  - 超时未收到心跳时自动触发急停（常规机型进入 `TASK_SERVO_OFF`，M4LT2 进入高阻尼软制动）
  - HEX 协议的 `HEART_BEAT` 命令同样刷新心跳计时器
  - 详见 [通信接口](/fourier-grx-M4/docs/reference/communication) 文档

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.42`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

### v1.2.1 (2026-08-12)

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.40`（详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）

---

### v1.2.0 (2026-08-07)

**文档更新**

- 📖 英文文档全面补齐与同步：
  - 任务文档全部页面与中文最新内容同步，并补译了缺失的英文页面
  - 英文 FAQ、常用操作（Usage Guide）对齐中文子页面结构（由单页合并改为索引 + 子页面）
  - 快速开始、固件发布、示例等页面同步中文近期改动
- 📖 固件发布页支持策略调整：[Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 仅最新版本标记为「支持中」，历史版本统一标记为「不再支持」（保留下载链接与更新内容供查阅）
- 📖 新增任务页面：[手动校准（旋转关节）](/fourier-grx-M4/docs/tasks/rotary_joint_manual_calibrate)（TID 4121）、[相对调节长度（直线关节）](/fourier-grx-M4/docs/tasks/move_offset_prismatic_joint)（TID 4207），任务索引顺序同步调整
- 📖 新增 [网络连接与远程登录](/fourier-grx-M4/docs/usage/network_connection) 指南：无路由器环境下共享网络、20260805 镜像自动静态 IP（`192.168.137.220`）、Web 终端（`:7681`）、SSH 登录凭据说明
- 📖 系统镜像更新至 20260805；[固件安装](/fourier-grx-M4/docs/quickstart/firmware_install) / [固件更新](/fourier-grx-M4/docs/quickstart/firmware_update) 页面补充网络共享 + SSH 登录说明
- 📖 修正 6 处任务文档与代码实现不一致的描述

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.39`（4.4.21 ~ 4.4.39 各版本更新内容详见 [Fourier-GRX 固件](/fourier-grx-M4/docs/release/fourier-grx) 发布页）
- 📦 `ioboard` 更新至 `1.0.0.3`（详见 [IO Board 固件](/fourier-grx-M4/docs/release/ioboard)）

---

## 2026 年 6 月

### v1.1.8 (2026-06-30)

**调整**

- 🔧 **Stand 任务 warm-up 时间缩短**：`STAGE_WARM_UP` 阻尼过渡时长由 `0.5 s` 调整为 `0.2 s`

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.20`

---

### v1.1.7 (2026-06-30)

**新增**

- ✨ **`fourier-grx update <version>` 直接安装指定版本**：变体自动从已安装包读取，无需手动指定。例：`fourier-grx update 4.4.14`

**改进**

- 🔧 **`fourier-grx update` 探测范围优化**：patch 探测扩大至 +20（miss=5）；次版本只探 minor+1；主版本只探 major+1.0.y，最坏请求数由 ~76 降至 ~36

**修复**

- 🐛 **`fourier-grx install` 失效**：修复插入新函数时意外删除 `if [ $# -eq 0 ]` 守卫行的问题

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.19`

---

### v1.1.6 (2026-06-30)

**修复**

- 🐛 **Stand 任务使能冲击（完整修复）**：`STAGE_INIT`、`STAGE_START`、`STAGE_WARM_UP` 三阶段均设 `kp=0`，确保从任意激活路径进入时都有完整的纯阻尼过渡。`STAGE_INIT` 补充 `output_joint_position = measured_position`，防止 PD 帧以零初始化的旧缓存为目标；`STAGE_WARM_UP` 持续 0.5 s，超时后以当前实测位置为插值起点进入运动阶段。日志添加 stage 前缀，便于现场调试

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.14`

---

### ~~v1.1.5 (2026-06-30)~~ *(已撤销)*

> `STAGE_WARM_UP` 放置位置不正确（基于对 FSM stage 管理的误解，`reset()` 不应主导 stage 切换）。已在 v1.1.6 中修正。

---

### ~~v1.1.4 (2026-06-29)~~ *(已撤销)*

> kp=0 仅持续一个 tick，不足以抑制冲击；且 `STAGE_INIT` 在第二次激活时不再触发。已在 v1.1.6 中完整修复。

---

### ~~v1.1.3 (2026-06-29)~~ *(已撤销)*

> v1.1.3 中对 `function_on_activate` 里预置执行器目标位置的修改经验证无效：`SERVO_ON` 通信帧仅发送使能指令，不携带位置数据，故该修改已在 v1.1.4 中回退。

---

## 2026 年 5 月

### v1.1.2 (2026-05-14)

**新增功能**

- 🔍 **固件版本检测标志位**：`DynalinkGRX` 新增 `flag_version_check_error`（`0` 正常 / `1` 异常）和 `version_check_error_info`（异常详情列表）字段，检测到 IOBoard / FSA / FSE 固件版本不匹配、无响应或查询异常时自动置位，通过 Dynalink `read_fields` 同步至上位机

**版本更新**

- 📦 `fourier-grx` 更新至 `4.4.6`

---

### v1.1.1 (2026-05-11)

**新增功能**

- ⚙️ **助力原地踏步（DT 模式）触发力配置接口**：新增 `assist_trigger_force_upper`（加速触发力）和 `assist_trigger_force_lower`（减速触发力）可配置参数，默认值分别为 `2.0 Nm` 和 `1.0 Nm`，通过上位机面板 `param_4`、`param_5` 设置。适用任务：TID 4119（助力原地踏步，调整 DT 参数）、TID 4306（膝关节受限助力原地踏步，调整 DT 参数）。详见 [助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_dt) 和 [膝关节受限助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_dt)

**算法修正**

- 🔧 **助力触发力阈值改为绝对力矩值**：原公式 `G[i] + offset` 改为 `G[i] * 0.0 + offset`（G 分量清零）。经实际实验测试，加入重力项 `G[i]` 会导致系统不稳定，故将其清零，直接以配置值作为加减速触发阈值

**行为澄清**

- 📌 明确参数更新时机：所有任务参数（步高、踏步周期、助力比例、触发力等）仅在**任务触发时**读取一次，不支持运行时实时刷新；需重新触发任务方可生效

**文档更新**

- 📖 更新 [助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/mark_time_assist_adjust_dt)：参数名由"助力触发力上/下限偏移"改为"助力触发力上/下限"，更新触发阈值说明，补充 G 项清零的实验依据
- 📖 更新 [膝关节受限助力原地踏步（DT）](/fourier-grx-M4/docs/tasks/knee_restriction_mark_time_assist_adjust_dt)：同上
- 📖 同步更新以上两个任务的英文文档

---

### v1.1.0

**新增功能**

- 🛡️ **M4LT2 急停高阻尼保护**：M4LT2 机型在硬件急停开关（ioboard）触发时，不再直接断电失能，而是自动切换到高阻尼保护任务（`TASK_ROTARY_JOINT_HIGH_DAMPING`，TID=4600）。关节保持上电，以 `kp=0`、`kd=80` 的纯阻尼 PD 模式控制旋转关节，防止肢体瞬间跌落，为操作者提供更安全的保护时间窗口。详见 [高阻尼保护任务说明](/fourier-grx-M4/docs/tasks/emergency_stop_high_damping)。

**文档更新**

- 📖 新增 [高阻尼保护任务页面](/fourier-grx-M4/docs/tasks/emergency_stop_high_damping)
- 📖 更新 [任务描述](/fourier-grx-M4/docs/tasks) 中的任务列表，新增 TID=4600
- 📖 更新 [M4L 快速开始](/fourier-grx-M4/docs/quickstart/m4l)，补充硬件急停按钮行为说明

---

## 2025 年 7 月

### v1.0.0 (2025-07-08)

**重要里程碑**

- 🎉 发布 Fourier-GRX-M4 SDK 文档第一个正式版本
- 💡 支持 M4 系列机器人开发
- 📖 完整的 API 文档和使用指南
- ✨ 新增常用操作页面
- 📚 优化文档结构和导航
- 🔍 改进搜索功能

**功能特性**

- ✅ 基础 API 接口
- ✅ 示例代码
- ✅ 开发指南
- ✅ 故障排除指南

**说明**

- 目前主要支持 M4 系列机器人
- 其他机型支持将陆续添加
