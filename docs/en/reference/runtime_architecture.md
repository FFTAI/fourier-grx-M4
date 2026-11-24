---
layout: default
title: Runtime Architecture
parent: Reference Guide
nav_order: 3.91
has_toc: true
nav_exclude: true
---

# Runtime Architecture

* TOC
{:toc}

This page explains how `fourier-grx` processes, threads, control loops, and communication paths fit together. It is based on `fourier-grx` **v4.4.86**. Internal implementation may change; integrate against the stable interfaces described here, not private class or function names.

> ℹ️ This page is for integrators and developers who need to understand how the program runs. To operate the robot, start with [Quick Start](/fourier-grx-M4/docs/en/quickstart) and the on-site operating instructions.

## 1. Runtime overview

```text
┌──────────────────────────── External inputs ──────────────────────┐
│  Gamepad / keyboard   Browser    User API client    EEG / BCI     │
└───────┬─────────────────┬───────────────┬────────────────┬───────┘
        │ USB             │ HTTP/WS       │ UDP 5566/9527  │ TCP/custom
        ▼                 ▼               ▼                ▼
┌─────────────────────────────┐   ┌──────────────┐   ┌──────────────┐
│ fourier-grx main process    │   │ fourier-grx  │   │ external      │
│                             │   │ web process  │   │ decoder / UI  │
│  control loop               │   └──────┬───────┘   └──────┬───────┘
│  FSM → Task → Control       │          │ UDP              │
│  → Robot → Hardware         │◄─────────┴──────────────────┘
│  communication loop (50 Hz) │
│  subprocesses: sync / dds / │
│  record / rerun / teleop    │
│  peripheral threads         │
└──────────────┬──────────────┘
               │ EtherCAT / CAN / Ethernet
               ▼
┌─────────────────────────────┐
│ actuators / IO Board / IMU   │
└─────────────────────────────┘
```

| Component | Runs on | Relationship to the main program |
|-----------|---------|----------------------------------|
| `fourier-grx` main program | Robot controller computer | Owns the control loop, task manager, and hardware access |
| `fourier-grx web` | Robot controller or LAN computer | Separate FastAPI process; talks over UDP; does not directly control hardware |
| User API client | Any LAN computer | Reads/writes state and tasks over UDP 5566 |
| Developer API | Robot controller, standalone Python process | Initializes hardware and runs its own control loop; stop the main program first |
| EEG / BCI decoder | External computer or edge device | Sends high-level commands through the upper computer or User API |

> ⚠️ Developer API is not a remote interface. It initializes `ControlSystem` and hardware in the calling process. The same actuators cannot be controlled by two processes at once. Run `fourier-grx stop` before `demo/developer`.

## 2. One control cycle

| Model | Default period | Default rate |
|-------|----------------|--------------|
| M4L P1 | 20 ms | 50 Hz |
| M4L T1 | 10 ms | 100 Hz |
| M4L T2 | 5 ms | 200 Hz |
| Communication publish | 20 ms | 50 Hz |

```text
1. State update       sensors → actuators → joints / end effectors
2. Command update     heartbeat / e-stop → gamepad / keyboard
                      → task availability → task switch
3. Algorithm          old on_deactivate → new on_activate
                      → current on_enter → on_tick → on_exit
4. Protection         actuator error / torque / velocity / position
5. Hardware output    joint or actuator download()
6. State publish      shared state / Dynalink buffers
```

Main entry points:

- Control loop: `ControlSystem.robot_control_loop_run()`;
- State update: `control_loop_intf_update_state()`;
- Command update: `control_loop_update_command()` within the update steps;
- Task execution: `control_loop_intf_algorithm()` → `RobotBase.execute()` → `FSMManager.execute()`;
- Protection: `control_loop_protection()`;
- Output: `control_loop_intf_output_control()`;
- Communication: separate `communication_loop_intf_run()` at 50 Hz.

> ℹ️ Communication and control are scheduled separately. A 50 Hz communication rate does not mean the control loop is limited to 50 Hz; M4L T1/T2 run at 100/200 Hz.

## 3. Where the task manager sits

```text
gamepad / keyboard / User API / Developer API
                    │
                    ▼
            set_task_command(TID)
                    │
                    ▼
┌─────────────────────────────────────┐
│ FSMManager                          │
│  tasks: registered tasks             │
│  task_command: pending TID           │
│  task_execute: current TID           │
│  task_executed: previous TID         │
│  components: current task modules    │
└──────────────────┬──────────────────┘
                   │ execute()
                   ▼
        concrete Task / Algorithm model
                   │
                   ▼
            joint targets / control dict
```

Registration has two layers:

1. `@TaskRegistry.register(RobotName.M4LT1, ...)` attaches a task class to a robot model;
2. at robot initialization, registered tasks are converted into `FSMItem` objects and added to `FSMManager.tasks`.

A TID existing in an enum does **not** mean it is registered for the current model. An unregistered TID may be ignored or logged as “not registered for the current robot/FSM instance.”

See [Task Lifecycle and Switching](/fourier-grx-M4/docs/en/reference/task_lifecycle) for hook semantics and switch order.

## 4. Data paths

| Path | Direction | Typical data | Notes |
|------|-----------|--------------|-------|
| `task/server` | robot → client | task state, finish flags | 50 Hz |
| `task/client` | client → robot | `robot_task_command`, update flag | User API |
| `robot/server` | robot → client | joints, IMU, actuators, protection | position / velocity / effort |
| `robot/client` | client → robot | clear protection flags | latched flags must be cleared explicitly |
| `grx/server` | robot → client | versions, battery, error codes | generic robot data |
| `grx/client` | client → robot | virtual joystick, panel, user | high-level input |
| `comm` | bidirectional | host heartbeat, connection state | timeout triggers protection |
| `rehab/server` | robot → client | assist, cadence, reference trajectory | rehabilitation data |
| `rehab/client` | client → robot | not open in current version | do not write commands |

Field-level details: [User API](/fourier-grx-M4/docs/en/reference/user) and [Communication](/fourier-grx-M4/docs/en/reference/communication).

## 5. Stable boundaries

Prefer these boundaries:

- **User API**: cross-process / cross-machine, UDP + Dynalink topics;
- **Developer API**: same machine, same process, direct `ControlSystem`;
- **Task enums**: use `TaskCommand` or `TaskMenuM4L`, not unexplained numeric literals;
- **State dict**: use the keys actually returned by the installed version;
- **Protection flags**: velocity / position / torque / overload flags are latched and must be cleared explicitly.

Do not depend on:

- the internal `OrderedDict` order of `FSMManager`;
- private task methods or internal stage numbers;
- task switching completing in the same millisecond the command is sent;
- control and communication loops being phase-locked;
- Developer API and the main program controlling hardware simultaneously.

## 6. Source map

| Topic | Path |
|-------|------|
| Main entry | `src/fourier_grx/main/main.py` |
| Control loop | `src/fourier_grx/control_system/fi_control_system.py` |
| State / command / output steps | `src/fourier_grx/robot/robot_base/fi_robot_base.py` |
| Task manager | `src/fourier_grx/fsm/fi_fsm_manager.py` |
| Task registry | `src/fourier_grx/task/fi_task_registry.py` |
| Subprocess initialization | `src/fourier_grx/process/fi_process.py` |
| Peripheral threads | `src/fourier_grx/thread/peripheral/` |
| Web console | `src/fourier_grx/web/` |

## Related pages

- [Task Lifecycle and Switching](/fourier-grx-M4/docs/en/reference/task_lifecycle)
- [Communication Interface](/fourier-grx-M4/docs/en/reference/communication)
- [User API](/fourier-grx-M4/docs/en/reference/user)
- [Developer API](/fourier-grx-M4/docs/en/reference/developer)
- [Run Modes](/fourier-grx-M4/docs/en/reference/run_type)
