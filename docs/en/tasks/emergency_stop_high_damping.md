---
layout: default
title: High-Damping Protection (Emergency Stop Response)
nav_order: 4.24
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# High-Damping Protection (Emergency Stop Response)

## Task Info

Task ID (TID): **4600**

Applicable Models: **M4LT2**

Task Description:

- When the robot detects that the **hardware emergency stop switch** (ioboard emergency button) has been triggered, the control program automatically switches to this task.
- Unlike direct power-off (`TASK_SERVO_OFF`), this task keeps the joints powered and controls the rotary joints in a **high-damping, zero-spring** PD mode:
  - `kp = 0`: No restoring spring force; joints can be passively moved by external force.
  - `kd = 80 (default)`: Velocity damping braking force is applied to dissipate kinetic energy and prevent limbs from dropping or swinging rapidly.
  - Target position tracks the current measured position every frame in real time — no snap-back effect.
- This mode significantly reduces the risk of uncontrolled limb movement after an emergency stop, providing operators with a safer intervention window.

> ⚠️ **Note**:
>
> This task is **triggered automatically** by the control program when `flag_emergent_stop` is set. It is not recommended to switch to this task manually via the gamepad or User API.
> After the emergency stop is cleared, the robot will continue to hold the high-damping state. You must manually switch to another task (e.g., `TASK_STAND_CONTROL`) to resume normal motion control.

Task Parameters:

This task has no configurable parameters. The `kd` value must be tuned by a hardware engineer in `fi_algorithm_m4l_rotary_joint_high_damping.py` based on actual joint inertia.

## Trigger Conditions

This task is triggered by either of the following emergency stop conditions (both set `flag_emergent_stop`):

| Trigger Source | Trigger Condition | Description |
|----------------|-------------------|-------------|
| ioboard emergency switch | `ioboard.emergency_state == True` | User presses the hardware emergency stop button on the robot backpack |
| All-actuator communication timeout | All actuators time out for ≥ 50 consecutive control cycles | Protective trigger due to communication anomaly |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping | Description |
|-----------|------------------|-------------|
| Emergency stop flag | `robot.flag_robot_emergent_stop` | Remains SET while the high-damping task is active |

Command Interface:

This task requires no additional command parameters and is triggered automatically by the control program. It cannot be activated manually by sending TID=4600.

## Comparison with Servo Off

| Feature | High-Damping Protection (4600) | Servo Off (36) |
|---------|-------------------------------|----------------|
| Trigger method | Hardware emergency switch, auto-triggered (M4LT2) | Gamepad logo key / User API, manual |
| Joint power state | Remains powered, outputs damping torque | Powered off, no torque output |
| Safety characteristic | Soft braking — limbs do not drop instantly | Robot goes limp immediately |
| Recovery method | Manually switch to another task | Requires re-powering and task switch |

## Update Log

- Added in `fourier-grx` v1.1.0 (M4LT2 only).
