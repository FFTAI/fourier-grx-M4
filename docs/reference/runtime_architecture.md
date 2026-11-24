---
layout: default
title: 运行时架构
parent: 参考指南
nav_order: 3.91
has_toc: true
---

# 运行时架构

* TOC
{:toc}

本页说明 `fourier-grx` 启动后各进程、线程、控制循环和通信链路之间的关系。内容以 `fourier-grx` **v4.4.86** 为基准整理；内部实现可能随版本变化，二次开发应优先依赖本文列出的稳定接口，而不是具体类名或函数名。

> ℹ️ 本页面向需要理解“程序如何跑起来”的集成商和开发者。只想操作机器人时，先阅读[快速开始](/fourier-grx-M4/docs/quickstart)和现场操作说明。

## 1. 运行时全景

```text
┌──────────────────────────── 外部输入 ────────────────────────────┐
│  手柄 / 键盘      浏览器        User API 客户端       EEG / BCI   │
└───────┬──────────────┬────────────────┬──────────────────┬───────┘
        │ USB          │ HTTP/WS        │ UDP 5566/9527    │ TCP/自定义
        │              │                │                  │
        ▼              ▼                ▼                  ▼
┌─────────────────────────────┐   ┌──────────────┐   ┌──────────────┐
│ fourier-grx 主进程           │   │ fourier-grx  │   │ 外部解码器    │
│                             │   │ web 进程      │   │ 或上位机      │
│  ┌───────────────────────┐  │   └──────┬───────┘   └──────┬───────┘
│  │ 控制循环               │  │          │ UDP               │
│  │ FSM → Task → Control  │  │◄─────────┴───────────────────┘
│  │ → Robot → Hardware    │  │
│  └───────────────────────┘  │
│  ┌───────────────────────┐  │
│  │ 通信循环（50 Hz）      │  │
│  └───────────────────────┘  │
│  ┌───────────────────────┐  │
│  │ 子进程                 │  │
│  │ sync / dds / record    │  │
│  │ rerun / teleoperation  │  │
│  └───────────────────────┘  │
│  ┌───────────────────────┐  │
│  │ 外设线程               │  │
│  │ 手柄 / 键盘            │  │
│  └───────────────────────┘  │
└──────────────┬──────────────┘
               │ EtherCAT / CAN / 以太网
               ▼
┌─────────────────────────────┐
│ 执行器 / IO Board / IMU      │
└─────────────────────────────┘
```

几个容易混淆的边界：

| 组件 | 运行位置 | 与主程序的关系 |
|------|----------|----------------|
| `fourier-grx` 主程序 | 机器人主控电脑 | 控制循环、任务管理和硬件访问都在这里 |
| `fourier-grx web` | 机器人主控电脑或同局域网电脑 | 独立 FastAPI 进程，通过 UDP 与主程序通信，不直接控制硬件 |
| User API 客户端 | 任意同局域网电脑 | 通过 UDP 5566 读写状态和任务，不进入控制进程 |
| Developer API | 机器人主控电脑、独立 Python 进程 | 自己初始化硬件并跑控制循环，运行前必须停止主程序 |
| EEG / BCI 解码器 | 外部电脑或边缘设备 | 通过上位机或 User API 发送高层命令，不应直接操作关节 |

> ⚠️ Developer API 不是远程接口。它会在调用进程内初始化 `ControlSystem` 和硬件；同一批执行器不能被两个进程同时控制。运行 `demo/developer` 前先执行 `fourier-grx stop`。

## 2. 一个控制周期里发生了什么

主程序通过调度器周期性执行控制循环。不同机型的默认周期不同：

| 机型 | 默认控制周期 | 默认控制频率 |
|------|--------------|--------------|
| M4L P1 | 20 ms | 50 Hz |
| M4L T1 | 10 ms | 100 Hz |
| M4L T2 | 5 ms | 200 Hz |
| 通信发布 | 20 ms | 50 Hz |

一个控制周期的顺序可以简化为：

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. 状态更新                                                 │
│    传感器 → 执行器 → 关节 / 末端执行器                       │
├─────────────────────────────────────────────────────────────┤
│ 2. 命令更新                                                 │
│    心跳 / 急停检查 → 手柄 / 键盘 → 任务可用性 → 任务切换      │
├─────────────────────────────────────────────────────────────┤
│ 3. 算法执行                                                 │
│    旧任务 on_deactivate → 新任务 on_activate                 │
│    → 当前任务 on_enter → on_tick → on_exit                   │
├─────────────────────────────────────────────────────────────┤
│ 4. 保护检查                                                 │
│    执行器错误 / 力矩 / 速度 / 位置保护                       │
├─────────────────────────────────────────────────────────────┤
│ 5. 硬件输出                                                 │
│    关节或执行器 download()                                   │
├─────────────────────────────────────────────────────────────┤
│ 6. 状态发布                                                 │
│    写入共享状态 / Dynalink 通信缓存                          │
└─────────────────────────────────────────────────────────────┘
```

对应的主要入口：

- 控制循环入口：`ControlSystem.robot_control_loop_run()`；
- 状态更新：`control_loop_intf_update_state()`；
- 命令更新：`control_loop_intf_update_state()` 中的 `control_loop_update_command()`；
- 任务执行：`control_loop_intf_algorithm()` → `RobotBase.execute()` → `FSMManager.execute()`；
- 保护：`control_loop_intf_algorithm()` 中的 `control_loop_protection()`；
- 输出：`control_loop_intf_output_control()`；
- 通信：独立的 `communication_loop_intf_run()`，默认 50 Hz。

> ℹ️ 通信循环和控制循环是两套调度。通信周期为 50 Hz，不代表控制频率只有 50 Hz；M4L T1 / T2 的控制循环分别可以到 100 / 200 Hz。

## 3. 任务管理器的位置

任务管理由 `FSMManager` 承担，位于控制循环和具体算法之间：

```text
手柄 / 键盘 / User API / Developer API
                │
                ▼
        set_task_command(TID)
                │
                ▼
┌─────────────────────────────────────┐
│ FSMManager                          │
│  tasks: 已注册任务表                 │
│  task_command: 待执行 TID            │
│  task_execute: 当前执行 TID          │
│  task_executed: 上一周期执行 TID     │
│  components: 当前任务的模块表         │
└──────────────────┬──────────────────┘
                   │ execute()
                   ▼
        具体 Task / Algorithm 模型
                   │
                   ▼
            关节目标 / 控制字典
```

任务注册分两层：

1. `@TaskRegistry.register(RobotName.M4LT1, ...)` 把任务类登记到机型；
2. 机器人初始化时遍历本机型任务，通过 `TaskBase.add_task()` 转成 `FSMItem` 放入 `FSMManager.tasks`。

因此“任务枚举里有 TID”不等于“当前机型已注册该任务”。未注册的 TID 通常不会切换任务，并可能只在日志中留下错误信息。跨机型开发时要以实际注册表为准。

任务和模块的生命周期、切换顺序和常见误区，见[任务生命周期与切换](/fourier-grx-M4/docs/reference/task_lifecycle)。

## 4. 数据通路

| 通路 | 方向 | 典型数据 | 说明 |
|------|------|----------|------|
| `task/server` | 机器人 → 客户端 | 任务状态、完成标志 | 50 Hz 发布 |
| `task/client` | 客户端 → 机器人 | `robot_task_command`、更新标志 | 通过 User API 写入 |
| `robot/server` | 机器人 → 客户端 | 关节、IMU、执行器、保护标志 | 关节位置 / 速度 / 力矩 |
| `robot/client` | 客户端 → 机器人 | 清除保护标志 | 锁存标志需要显式清除 |
| `grx/server` | 机器人 → 客户端 | 版本、电量、错误码 | 通用机器人信息 |
| `grx/client` | 客户端 → 机器人 | 虚拟摇杆、虚拟面板、虚拟用户 | 高层控制输入 |
| `comm` | 双向 | 上位机心跳、连接状态 | 超时会触发保护 |
| `rehab/server` | 机器人 → 客户端 | 助力、步频、参考轨迹、进度 | 康复训练常用 |
| `rehab/client` | 客户端 → 机器人 | 当前版本未开放 | 不要向该 topic 写指令 |

字段级说明见 [User 接口](/fourier-grx-M4/docs/reference/user) 和[通信接口](/fourier-grx-M4/docs/reference/communication)。

## 5. 开发时的稳定边界

建议二次开发只依赖以下边界：

- **User API**：跨进程、跨电脑，使用 UDP 和 Dynalink topic；
- **Developer API**：同机、同进程，直接使用 `ControlSystem`；
- **任务枚举**：用 `TaskCommand` 或 `TaskMenuM4L` 取值，不硬编码来历不明的数字；
- **状态字典**：以实际返回的 key 为准，不要把字段名当作永久不变的协议；
- **保护标志**：速度 / 位置 / 力矩 / 过载标志是锁存的，需要显式清除。

不要依赖：

- `FSMManager` 内部 `OrderedDict` 的遍历顺序；
- 某个任务类的私有方法或内部 stage 编号；
- 任务切换发生在“发送命令的同一毫秒”；
- 控制循环与通信循环严格同相；
- Developer API 与主程序同时运行。

## 6. 代码位置

| 内容 | 路径 |
|------|------|
| 主程序启动 | `src/fourier_grx/main/main.py` |
| 控制循环 | `src/fourier_grx/control_system/fi_control_system.py` |
| 状态 / 命令 / 输出步骤 | `src/fourier_grx/robot/robot_base/fi_robot_base.py` |
| 任务管理器 | `src/fourier_grx/fsm/fi_fsm_manager.py` |
| 任务注册 | `src/fourier_grx/task/fi_task_registry.py` |
| 子进程初始化 | `src/fourier_grx/process/fi_process.py` |
| 外设线程 | `src/fourier_grx/thread/peripheral/` |
| Web 上位机 | `src/fourier_grx/web/` |

## 相关页面

- [任务生命周期与切换](/fourier-grx-M4/docs/reference/task_lifecycle)
- [通信接口](/fourier-grx-M4/docs/reference/communication)
- [User 接口](/fourier-grx-M4/docs/reference/user)
- [Developer 接口](/fourier-grx-M4/docs/reference/developer)
- [运行模式](/fourier-grx-M4/docs/reference/run_type)
