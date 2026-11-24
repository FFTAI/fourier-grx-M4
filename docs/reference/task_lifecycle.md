---
layout: default
title: 任务生命周期与切换
parent: 参考指南
nav_order: 3.92
has_toc: true
---

# 任务生命周期与切换

* TOC
{:toc}

本页说明一个任务从注册、选中、激活、运行到退出的完整过程，以及任务切换时 `fourier-grx` 实际做了什么。理解这些行为，可以避免“命令发出去了但机器人没动”“改了参数却没生效”“任务切换后模块消失”等常见问题。

> ℹ️ 本页以 `fourier-grx` **v4.4.86** 为基准。任务实现会随版本变化；TID、参数和任务页说明以当前固件为准。

## 1. 三层对象

| 层次 | 对象 | 作用 |
|------|------|------|
| 指令层 | `TaskMenuM4L` / `TaskCommand` | 对外暴露的 TID，例如 4020、4129、4210 |
| 管理层 | `FSMManager` / `FSMItem` | 保存已注册任务、待执行 TID、当前 TID、模块表 |
| 实现层 | `TaskBase` 子类 / Algorithm 模型 | 真正计算关节目标、写状态、处理保护 |

一个任务不是“一个函数”，而是：

```text
Task 类
  ├─ task_key       : 对外 TID
  ├─ task_model     : 算法模型 / 状态机
  ├─ task_component : 可组合的子任务列表
  ├─ on_activate    : 切入时调用一次
  ├─ on_deactivate  : 切出时调用一次
  ├─ on_enter       : 每个控制周期调用
  ├─ on_tick        : 每个控制周期调用（主逻辑）
  └─ on_exit        : 每个控制周期调用
```

## 2. 任务注册

任务通过装饰器登记到机型：

```python
@TaskRegistry.register(RobotName.M4LT1, RobotName.M4LT2)
class TaskM4LForwardWalk(TaskM4LBase):
    ...
```

机器人初始化时执行：

```text
RobotM4LT1._init_task()
  → TaskRegistry.get_tasks(RobotName.M4LT1)
  → 逐个 _register_task(task_cls)
  → TaskBase.add_task(task_type)
  → FSMManager.add_task(...)
  → FSMItem 放入 FSMManager.tasks
```

所以：

- TID 在枚举里存在，**不代表**当前机型注册了该任务；
- 同一 TID 在不同机型上可能对应不同实现；
- 未注册 TID 可能被静默忽略，或在日志中打印“not registered for the current robot/FSM instance”。

## 3. 回调语义

这是最容易误解的部分：

| 回调 | 调用时机 | 典型用途 |
|------|----------|----------|
| `on_activate` | 从其他任务切入时，调用一次 | 初始化模型、缓存当前姿态、下发初始控制模式 |
| `on_deactivate` | 从当前任务切出时，调用一次 | 清理前馈、恢复 PID、复位上报字段 |
| `on_enter` | **每个控制周期** | 读取输入、准备本周期的状态 |
| `on_tick` | **每个控制周期** | 推进轨迹 / 算法 / 状态机，写关节目标 |
| `on_exit` | **每个控制周期** | 收尾、发布状态、处理完成标志 |

`on_enter` / `on_tick` / `on_exit` 不是“进入任务一次、退出任务一次”的钩子，而是每个控制周期的三个阶段。真正的进入 / 退出钩子是 `on_activate` / `on_deactivate`。

## 4. 一次任务切换的完整顺序

假设当前执行任务 A，客户端发来任务 B：

```text
客户端 / 手柄 / 键盘
        │
        │ set_task_command(B)
        ▼
FSMManager.flag_task_command_update = SET
        │
        ▼  下一个控制周期 update()
┌─────────────────────────────────────────────────────┐
│ 1. 读取手柄 / 键盘输入                               │
│ 2. 若本次还有外部 task_command，覆盖待执行命令         │
│ 3. 检查任务 B 是否 available                         │
│    └─ 不可用：清除更新标志，保持任务 A               │
│ 4. 处理任务命令                                      │
│    ├─ 清除更新标志                                   │
│    ├─ 计算 stage：A != B → STAGE_INIT                │
│    ├─ 清空组件表 components                          │
│    ├─ 注册 B 的组件（如果有）                         │
│    └─ task_execute = B                               │
└─────────────────────────────────────────────────────┘
        │
        ▼  同一控制周期 execute()
┌─────────────────────────────────────────────────────┐
│ 5. 发现 task_executed(A) != task_execute(B)          │
│    ├─ A.on_deactivate()                              │
│    └─ B.on_activate()                                │
│ 6. B.on_enter()                                      │
│ 7. B.on_tick()                                       │
│ 8. B.on_exit()                                       │
│ 9. task_executed = B                                 │
└─────────────────────────────────────────────────────┘
```

关键点：

- 任务切换和任务执行在**同一个控制周期**内完成；
- 旧任务的 `on_deactivate` 先于新任务的 `on_activate`；
- 新任务的 `on_enter` / `on_tick` / `on_exit` 在激活当周期就会执行；
- 任务不可用时不会切换，且更新标志会被清除；
- 切换任务会清空当前任务的组件表，不能假设上一个任务的模块还在。

## 5. 不同 TID 与同一 TID

`FSMManager` 在计算算法 stage 时比较“旧执行 TID”和“新命令 TID”：

| 情况 | stage | 含义 |
|------|-------|------|
| A → B | `STAGE_INIT` | 从其他任务切入，需要完整初始化 |
| A → A | `STAGE_START` | 同一任务再次触发，通常表示重新开始 / 重新播放 |
| A → A（首次启动） | `STAGE_START` | 同上，不重新执行 `on_activate` |

这解释了两个常见现象：

- 重复发送当前 TID 不会重新走 `on_activate`，但会把算法 stage 复位到 `STAGE_START`；
- 某些任务（例如助力 PD）修改助力系数后需要“重启任务”，实际依赖的就是这次 stage 复位和 `on_activate` 的初始化路径。

## 6. 任务与模块

模块（component）是任务内部的子任务，用于表达互斥或可组合的子功能：

```text
任务 B
  ├─ component 1：某个关节组 / 子算法
  ├─ component 2：另一个子算法
  └─ component 3 ...
```

行为：

- 任务切换时 `components` 被清空；
- 新任务的 `task_component` 列表被递归注册；
- 模块可以有自己的 `stage` 和 `on_tick`；
- 手柄用 `R1` 选择模块、`R2` 双击确认；
- 模块值（MID）与机型、版本绑定，不能假设跨版本不变。

模块管理由控制程序负责，上层通常只需要下发任务；只有在调试或自定义任务时才需要直接操作模块。

## 7. 任务类型

| 类型 | 含义 | 运行特征 |
|------|------|----------|
| `IDLE` | 空闲 | 不产生运动输出 |
| `NORMAL` | 普通循环任务 | 持续执行，`flag_task_running` 置位 |
| `ONESHOT` | 一次性任务 | 执行完成后由任务自身切换到其他任务 |

按回调实现方式又可分为：

| 类型 | 含义 |
|------|------|
| `STANDALONE` | 独立任务，可使用全部关节 |
| `COMPONENT` | 组件任务，只控制关联关节，通常组合使用 |
| `META` | 元任务，用于推进模型 / 规划器，不一定直接驱动关节 |

## 8. 安全覆盖的优先级

任务命令不是最高优先级。每个控制周期在任务更新之前，会先检查：

1. 上位机心跳是否超时；
2. `flag_emergent_stop` 是否置位；
3. 是否有执行器错误 / 力矩 / 速度 / 位置保护。

处理方式：

| 条件 | 行为 |
|------|------|
| 心跳超时 | 常规机型切换到 `TASK_SERVO_OFF`；M4LT2 切换到高阻尼任务 |
| 硬件急停 | 常规机型失能；M4LT2 进入高阻尼软制动 |
| 执行器错误 | 切换到 `TASK_IDLE` 并置错误标志 |
| 力矩 / 速度 / 位置保护 | 切换到 `TASK_SERVO_OFF`，标志锁存，需显式清除 |

因此，客户端刚发送的任务可能被安全逻辑覆盖。排查“任务为什么没执行”时，要先看 `flag_emergent_stop`、`flag_host_heartbeat_timeout`、`flag_robot_fault` 和保护标志。

## 9. 手柄行为

当前 `fourier-grx` 的实际手柄逻辑与部分旧文档有差异：

| 操作 | 实际行为 |
|------|----------|
| `L1` | 单击切换任务选择 |
| `L2` | **0.3 秒内双击**确认任务 |
| `R1` | 单击切换模块选择 |
| `R2` | **0.3 秒内双击**确认模块 |
| `Share` | 反转任务选择方向 |
| `Option` | 反转模块选择方向 |

快捷键（例如 `logo` 失能、`square` 站立、`triangle` 被动行走）同样采用双击触发。不同手柄类型的按键名称映射可能不同，操作前应先用 `fourier-grx start` 的终端输出确认当前选中的任务。

## 10. 添加自定义任务的最小结构

```python
from fourier_grx.task import TaskBase
from fourier_grx.task.fi_task_registry import TaskRegistry
from fourier_grx.predefine import RobotName, TaskFunctionType
from fourier_core.predefine import FunctionResult

@TaskRegistry.register(RobotName.M4LT1)
class MyTask(TaskBase):
    def __init__(self, fsm_manager):
        super().__init__(
            fsm_manager=fsm_manager,
            task_type=TaskFunctionType.STANDALONE,
        )
        self.task_key = MyTaskMenu.MY_TASK

    def function_on_activate(self, **kwargs):
        # 只在这里做一次初始化
        return FunctionResult.SUCCESS

    def function_standalone(self, **kwargs):
        # 每个控制周期执行
        return FunctionResult.SUCCESS
```

实际实现还需要：

- 在任务枚举中增加 TID；
- 在对应机型的 `_init_task` 之前完成注册；
- 处理 `on_deactivate` 清理；
- 写清楚任务的前置条件、保护边界和退出路径；
- 在模拟器或空载环境下先验证。

## 11. 常见问题

### 命令发出后没有切换

检查：

- TID 是否在当前机型注册；
- 任务 `available` 是否返回 `False`；
- 是否被心跳超时、急停或保护覆盖；
- 是否在错误的运行模式（例如 release 模式不接受某些调试任务）。

### 修改参数后不生效

不同任务的参数生效时机不同：

- 有的每周期读取（例如部分助力系数）；
- 有的只在 `STAGE_INIT` / `STAGE_START` 写入（例如 PD 助力系数）；
- 有的需要重新进入任务才会重新生成轨迹。

以具体任务页的“参数生效时机”为准。

### 任务切换后模块消失

这是预期行为。任务切换会清空组件表；新任务会重新注册自己的组件。不要跨任务保存组件对象。

### 为什么 `on_enter` 被执行了很多次

因为它就是每个控制周期执行一次。需要“只执行一次”的逻辑应放在 `on_activate`。

## 相关页面

- [运行时架构](/fourier-grx-M4/docs/reference/runtime_architecture)
- [任务描述](/fourier-grx-M4/docs/tasks)
- [User 接口](/fourier-grx-M4/docs/reference/user)
- [运行模式](/fourier-grx-M4/docs/reference/run_type)
- [速度保护与位置保护](/fourier-grx-M4/docs/reference/protection)
