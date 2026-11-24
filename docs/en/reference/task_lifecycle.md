---
layout: default
title: Task Lifecycle and Switching
parent: Reference Guide
nav_order: 3.92
has_toc: true
nav_exclude: true
---

# Task Lifecycle and Switching

* TOC
{:toc}

This page describes how a task is registered, selected, activated, run, and deactivated, and what `fourier-grx` actually does during a task switch. It is based on **v4.4.86**.

## 1. Three layers

| Layer | Object | Role |
|-------|--------|------|
| Command | `TaskMenuM4L` / `TaskCommand` | TIDs such as 4020, 4129, 4210 |
| Management | `FSMManager` / `FSMItem` | Registered tasks, pending TID, current TID, modules |
| Implementation | `TaskBase` subclass / algorithm model | Computes joint targets and handles protection |

A task is not just a function:

```text
Task class
  ├─ task_key       : public TID
  ├─ task_model     : algorithm model / state machine
  ├─ task_component : composable sub-tasks
  ├─ on_activate    : once when entering
  ├─ on_deactivate  : once when leaving
  ├─ on_enter       : every control cycle
  ├─ on_tick        : every control cycle (main logic)
  └─ on_exit        : every control cycle
```

## 2. Registration

```python
@TaskRegistry.register(RobotName.M4LT1, RobotName.M4LT2)
class TaskM4LForwardWalk(TaskM4LBase):
    ...
```

At robot initialization:

```text
RobotM4LT1._init_task()
  → TaskRegistry.get_tasks(RobotName.M4LT1)
  → _register_task(task_cls)
  → TaskBase.add_task(task_type)
  → FSMManager.add_task(...)
  → FSMItem inserted into FSMManager.tasks
```

Therefore:

- a TID in an enum does not guarantee registration for the current model;
- the same TID may map to different implementations on different models;
- an unregistered TID may be ignored or logged.

## 3. Hook semantics

| Hook | When | Typical use |
|------|------|-------------|
| `on_activate` | Once when switching into the task | Initialize model, cache posture, set initial control mode |
| `on_deactivate` | Once when switching out | Clear feedforward, restore PID, reset reported fields |
| `on_enter` | **Every control cycle** | Read inputs, prepare this cycle |
| `on_tick` | **Every control cycle** | Advance trajectory / algorithm / state machine |
| `on_exit` | **Every control cycle** | Finalize, publish state, handle finish |

`on_enter` / `on_tick` / `on_exit` are per-cycle phases, not one-time enter/exit hooks. Use `on_activate` / `on_deactivate` for one-time work.

## 4. Switch sequence

```text
client / gamepad / keyboard
        │ set_task_command(B)
        ▼
flag_task_command_update = SET
        │ next control cycle: update()
┌─────────────────────────────────────────────────────┐
│ 1. Read gamepad / keyboard input                     │
│ 2. Apply external task_command if present            │
│ 3. Check task B availability                         │
│    └─ unavailable: clear flag, keep task A           │
│ 4. Process command                                   │
│    ├─ clear update flag                              │
│    ├─ A != B → STAGE_INIT                            │
│    ├─ clear components                               │
│    ├─ register B components                          │
│    └─ task_execute = B                               │
└─────────────────────────────────────────────────────┘
        │ same cycle: execute()
┌─────────────────────────────────────────────────────┐
│ 5. task_executed(A) != task_execute(B)               │
│    ├─ A.on_deactivate()                              │
│    └─ B.on_activate()                                │
│ 6. B.on_enter()                                      │
│ 7. B.on_tick()                                       │
│ 8. B.on_exit()                                       │
│ 9. task_executed = B                                 │
└─────────────────────────────────────────────────────┘
```

Key points:

- switching and execution happen in the same control cycle;
- old `on_deactivate` runs before new `on_activate`;
- new `on_enter` / `on_tick` / `on_exit` run in the activation cycle;
- unavailable tasks are not switched to; the update flag is cleared;
- task switching clears the component table.

## 5. Different TID vs same TID

| Case | Stage | Meaning |
|------|-------|---------|
| A → B | `STAGE_INIT` | Entering from another task; full initialization |
| A → A | `STAGE_START` | Re-triggering the same task; usually restart / replay |
| A → A (first start) | `STAGE_START` | Same; `on_activate` is not re-run |

Re-sending the current TID does not call `on_activate` again, but it resets the algorithm stage to `STAGE_START`. Some tasks require this restart for changed parameters to take effect.

## 6. Tasks and modules

A module (component) is a sub-task inside a task:

```text
Task B
  ├─ component 1
  ├─ component 2
  └─ component 3 ...
```

- switching tasks clears `components`;
- the new task's `task_component` list is registered recursively;
- modules can have their own stage and `on_tick`;
- gamepad `R1` selects a module, `R2` double-click confirms;
- MID values are model- and version-dependent.

## 7. Task types

| Type | Meaning | Behavior |
|------|---------|----------|
| `IDLE` | Idle | No motion output |
| `NORMAL` | Normal cyclic task | Runs continuously; `flag_task_running` is set |
| `ONESHOT` | One-shot task | Task switches itself when finished |

Function types:

| Type | Meaning |
|------|---------|
| `STANDALONE` | Independent task; may use all joints |
| `COMPONENT` | Controls only associated joints; usually combined |
| `META` | Advances a model / planner; may not drive joints directly |

## 8. Safety overrides

Before task update, each cycle checks:

1. host heartbeat timeout;
2. `flag_emergent_stop`;
3. actuator errors / torque / velocity / position protection.

| Condition | Behavior |
|-----------|----------|
| Heartbeat timeout | Standard models switch to `TASK_SERVO_OFF`; M4LT2 switches to high damping |
| Hardware e-stop | Standard models disable; M4LT2 enters high-damping braking |
| Actuator error | Switch to `TASK_IDLE`, set error flag |
| Torque / velocity / position protection | Switch to `TASK_SERVO_OFF`; flags latch until cleared |

A newly sent task can therefore be overridden by safety logic. When diagnosing “task did not run,” check `flag_emergent_stop`, `flag_host_heartbeat_timeout`, `flag_robot_fault`, and protection flags first.

## 9. Gamepad behavior

| Action | Actual behavior |
|--------|-----------------|
| `L1` | Single click cycles task selection |
| `L2` | **Double-click within 0.3 s** confirms task |
| `R1` | Single click cycles module selection |
| `R2` | **Double-click within 0.3 s** confirms module |
| `Share` | Reverse task selection direction |
| `Option` | Reverse module selection direction |

Shortcut buttons (for example `logo` servo-off, `square` stand, `triangle` passive walk) also require a double-click. Button names depend on the gamepad type; confirm the selected task in the terminal output.

## 10. Minimal custom task structure

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
        return FunctionResult.SUCCESS

    def function_standalone(self, **kwargs):
        return FunctionResult.SUCCESS
```

A real task also needs a TID, registration for the target model, cleanup in `on_deactivate`, explicit safety boundaries, and simulator / no-load validation.

## 11. Common issues

### Command sent but task did not switch

Check registration, `available`, heartbeat / e-stop / protection overrides, and run mode.

### Parameter changed but has no effect

Some parameters are read every cycle, some only at `STAGE_INIT` / `STAGE_START`, and some require trajectory regeneration. Follow the specific task page.

### Modules disappeared after switching

Expected. The component table is cleared on task switch and rebuilt for the new task. Do not keep component references across tasks.

### Why is `on_enter` called so often?

It runs every control cycle. Put one-time logic in `on_activate`.

## Related pages

- [Runtime Architecture](/fourier-grx-M4/docs/en/reference/runtime_architecture)
- [Task Description](/fourier-grx-M4/docs/en/tasks)
- [User API](/fourier-grx-M4/docs/en/reference/user)
- [Run Modes](/fourier-grx-M4/docs/en/reference/run_type)
- [Velocity and Position Protection](/fourier-grx-M4/docs/en/reference/protection)
