---
layout: default
title: 脑电 / BCI 联合使用示例
parent: 设备集成
nav_order: 5.71
has_toc: true
---

# 脑电 / BCI 联合使用示例

* TOC
{:toc}

本页给出两条可落地的脑电 / BCI 联合使用路径：

1. **M4 上位机 EEG 接入模式**：脑电设备作为 TCP Server，M4 上位机作为 TCP Client；适合已经交付 M4 上位机的现场。
2. **自定义 BCI 解码器 → User API**：Python 解码器直接通过 UDP 与 `fourier-grx` 通信；适合研究 / 算法验证。

> ⚠️ **重要边界**
>
> - 本页是研究和工程集成示例，**不是**注册医疗功能，也不构成诊断、治疗或疗效声明；
> - 当前仓库不包含脑电采集、伪迹处理或分类算法；
> - 用于患者前，必须完成伦理审批、知情同意、风险评估和机构规定的临床验证；
> - 脑电信号不稳定、解码置信度不足或设备断连时，应默认停止机器人，而不是继续执行最后一次命令；
> - 硬件急停必须独立于脑电软件和上位机。

## 1. 两条路径怎么选

| 路径 | 适用场景 | 优点 | 限制 |
|------|----------|------|------|
| M4 上位机 EEG 模式 | 现场已有 m4-electron，脑电团队只负责 TCP 服务端 | 协议固定、上位机已有训练界面和报告 | 需要现场版本启用“外部设备连接”；控制映射由上位机定义 |
| 自定义 BCI → User API | 研究算法、需要自定义解码和实验协议 | 灵活，可直接记录、替换解码器 | 需要自己处理连接、心跳、任务、安全和日志 |

如果目标是“让脑电设备配合现有 M4 训练流程”，优先路径 1；如果目标是“验证一个新的 BCI 解码器”，使用路径 2，并先在机器人悬空 / 空载条件下跑通。

## 2. 路径一：M4 上位机 EEG TCP 协议

M4 上位机在“脑电接入模式”下主动连接脑电设备。脑电侧需要实现 **TCP Server**。

### 2.1 网络与编码

| 项 | 示例值 | 说明 |
|----|--------|------|
| 脑电设备 IP | `192.168.31.122` | 以现场配置为准 |
| 脑电监听端口 | `7070` | 以现场配置为准 |
| 传输层 | TCP | 长连接 |
| 应用层 | NDJSON | 每行一个 JSON，`\n` 结尾，UTF-8 |
| 心跳 | M4 每 3 s 发 `ping` | 脑电立即回 `pong` |
| 断连判定 | 10 s 未收到 `pong` | M4 自动重连 |

> ℹ️ 部分 M4 上位机版本默认隐藏“外部设备连接”入口，需要在 `feature-config.json` 中启用 `showExternalDeviceConnection`，或由现场交付版本提供。具体以现场版本为准。

### 2.2 消息类型

| 方向 | `type` | 作用 |
|------|--------|------|
| M4 → 脑电 | `ping` | 心跳 |
| 脑电 → M4 | `pong` | 心跳回复 |
| M4 → 脑电 | `command` + `cmd: start` | 训练开始，携带 `user_id` |
| M4 → 脑电 | `command` + `cmd: stop` | 训练停止，连接保持 |
| 脑电 → M4 | `eeg_stream` | 2 Hz 推送 `value`（0–100） |
| 脑电 → M4 | `threshold_update` | 行走 / 站立阈值 |

### 2.3 典型时序

```text
M4 上位机                                脑电设备（TCP Server）
    │                                          │
    │──── TCP connect ────────────────────────→│
    │──── ping ───────────────────────────────→│
    │←─── pong ────────────────────────────────│
    │──── {"cmd":"start","user_id":"U10086"} ─→│
    │←─── threshold_update ────────────────────│  立即回当前阈值
    │←─── eeg_stream {"value":45} ─────────────│  每 500 ms
    │←─── eeg_stream {"value":52} ─────────────│
    │←─── threshold_update（用户修改阈值）──────│
    │──── {"cmd":"stop"} ─────────────────────→│  停止推流，连接保持
    │──── ping / pong ────────────────────────→│
    │──── TCP disconnect ─────────────────────→│
```

### 2.4 消息示例

```json
{"type":"command","cmd":"start","user_id":"U10086","ts":1745123456789}
{"type":"command","cmd":"stop","ts":1745123456789}
{"type":"eeg_stream","ts":1745123456789,"value":73}
{"type":"threshold_update","ts":1745123456789,"walk_threshold":65,"stand_threshold":40}
```

### 2.5 控制映射

M4 上位机当前协议中：

- `value > walk_threshold`：触发行走；
- `value < stand_threshold`：停止行走、保持站立；
- 阈值范围 `[0, 100]`，超出范围会被截断；
- 收到 `start` 后先发一次 `threshold_update`，再以 500 ms 间隔推流；
- 收到 `stop` 后停止推流，但连接和心跳保持。

这只是上位机的控制策略，不应直接解释为“脑电值等于运动意图强度”。阈值应由治疗师 / 研究人员结合受试者和任务设置，并保留人工停止权。

### 2.6 脑电侧实现检查表

- [ ] TCP Server 监听 `7070`，同一时间只接受一个有效连接；
- [ ] 每条消息一行 JSON，UTF-8，以 `\n` 结尾；
- [ ] 所有消息携带 Unix 毫秒时间戳 `ts`；
- [ ] 3 s 内回复 `pong`；
- [ ] 收到 `start` 后立即发送一次阈值，再开始 2 Hz 推流；
- [ ] 收到 `stop` 后停止推流，不主动断开；
- [ ] 不发送超出 `[0, 100]` 的值；
- [ ] 断线后恢复监听，等待下一次连接；
- [ ] 记录原始脑电、解码结果、阈值和发送日志，便于离线对齐。

## 3. 路径二：自定义 BCI → User API

### 3.1 架构

```text
脑电帽 / 放大器
      │
      ▼
采集与解码进程（LSL / BrainFlow / 厂商 SDK）
      │  运动想象 / SSVEP / 其他特征
      ▼
命令映射器（置信度、去抖、限速、超时）
      │  高层命令
      ▼
User API（SyncClientSocket，UDP 5566）
      │
      ▼
fourier-grx：任务 / 虚拟面板 / 虚拟摇杆
      │
      ▼
M4L 机器人
```

反馈可以回到屏幕、声音或触觉设备。反馈延迟和延迟抖动本身会影响 BCI 表现，应在实验设计中记录。

### 3.2 推荐映射

| BCI 输出 | 推荐机器人命令 | 不推荐 |
|----------|----------------|--------|
| 开始 / 停止 | `task` topic 切换任务 | 直接写关节力矩 |
| 助力增加 / 减少 | `grx` 虚拟面板参数 | 直接改 PD 增益数组 |
| 左 / 右方向 | `grx` 虚拟摇杆 | 直接写关节位置 |
| 急停 | `TASK_SERVO_OFF` + 硬件急停 | 只停止解码器 |

原则：BCI 只做“高层意图 → 高层命令”，底层轨迹、保护和限幅仍由 `fourier-grx` 负责。

### 3.3 最小 Python 骨架

以下代码只示意连接、心跳、任务和虚拟面板，不能直接用于患者。实际运行请以 `demo/user/` 中已验证的脚本为基础。

```python
import threading
import time

import fourier_grx.sdk.user as fourier_grx
from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

client = SyncClientSocket()
while not client.server_discovered():
    time.sleep(0.1)

# 心跳：开启后必须持续发送；默认 6 s 超时会触发保护
def heartbeat():
    counter = 0
    while True:
        client.publish(key="comm", value={"host_heartbeat_counter": counter})
        counter += 1
        time.sleep(0.5)

threading.Thread(target=heartbeat, daemon=True).start()

# 启动行走任务；实际 TID 以当前机型任务表为准
client.publish(key="task", value={
    "robot_task_command": fourier_grx.TaskCommand.TASK_WALK,
    "flag_task_command_update": True,
})
time.sleep(1)

# 通过虚拟面板给出很小的步长和速度，先做低速验证
client.publish(key="grx", value={
    "virtual_panel_command_param_1": 0.20,
    "virtual_panel_command_param_2": 0.20,
    "virtual_panel_command_start": True,
})

try:
    while True:
        time.sleep(0.1)
        # 在这里读取 decoder 输出，做置信度判断、去抖和限速
except KeyboardInterrupt:
    client.publish(key="grx", value={
        "virtual_panel_command_start": False,
        "virtual_panel_command_stop": True,
    })
    client.publish(key="task", value={
        "robot_task_command": fourier_grx.TaskCommand.TASK_SERVO_OFF,
        "flag_task_command_update": True,
    })
    client.close()
```

> ⚠️ 这段代码省略了置信度过滤、命令超时、速率限制、状态检查和异常恢复，不能当作生产代码。实际示例请参考 `demo/user/demo_virtual_panel.py` 和 `demo/user/demo_heartbeat.py`。

### 3.4 必须实现的安全机制

- **置信度阈值**：低于阈值不产生命令；
- **连续确认**：连续 N 个解码窗口一致才触发；
- **命令超时**：超过 T 秒没有新命令，自动停止 / 回到站立；
- **速率限制**：助力、速度、方向变化有限幅；
- **死手开关**：操作者必须持续按住或持续给出有效信号；
- **硬件急停**：独立于 BCI、上位机和网络；
- **状态门控**：只有在已校准、已站立、无保护、无故障时才接受 BCI 命令；
- **双人操作**：治疗师 / 工程师可随时接管；
- **日志**：记录原始信号、解码结果、发送命令、机器人状态和急停事件。

## 4. 时序、同步与数据记录

脑电采样率通常远高于机器人 50 Hz 通信周期。建议：

- 在采集端记录每个解码窗口的开始 / 结束时间；
- 在机器人侧记录任务命令、状态包和 `ts`；
- 用同一台机器或同一时间源对齐，至少记录时钟偏差；
- 在屏幕 / 声音反馈上打标记，便于离线对齐；
- 统计端到端延迟：采集 → 解码 → 发送 → 机器人执行；
- 统计丢包、乱序、重连和命令拒绝次数；
- 不要把 2 Hz 的 `eeg_stream` 当成原始脑电采样率。

## 5. 验证流程

建议按以下顺序逐级验证：

1. **离线解码**：用录制数据验证分类器和阈值；
2. **假设备**：用 mock EEG / mock robot 验证协议、心跳和断连；
3. **机器人悬空 / 空载**：只观察任务切换和状态，不让人承重；
4. **低助力、短时、有人支撑**：在治疗师控制下验证；
5. **逐步增加复杂度**：只在前一步稳定后继续。

每一级都应记录：成功率、误触发率、延迟、重连次数、停止原因和受试者主观负担。

## 6. 故障排查

| 现象 | 优先检查 |
|------|----------|
| M4 上位机连不上脑电 | IP / 端口、TCP Server 是否监听、防火墙、是否只允许一个连接 |
| 连接后没有数据 | 是否收到 `start`、是否先发阈值、是否按 500 ms 推流 |
| 频繁断连 | `pong` 是否在 10 s 内、网络是否丢包、JSON 行是否完整 |
| 机器人不响应 BCI | 心跳、任务是否注册、是否被保护 / 急停覆盖、是否在正确运行模式 |
| 机器人动作与意图不一致 | 阈值、去抖、命令映射、虚拟面板锁存、任务是否已切换 |
| 训练报告缺少数据 | `rehab` 字段是否上报、固件版本是否支持、是否在正确任务 |

## 相关页面

- [通信接口](/fourier-grx-M4/docs/reference/communication)
- [User 接口](/fourier-grx-M4/docs/reference/user)
- [运行时架构](/fourier-grx-M4/docs/reference/runtime_architecture)
- [任务生命周期与切换](/fourier-grx-M4/docs/reference/task_lifecycle)
- [示例代码](/fourier-grx-M4/docs/examples)
