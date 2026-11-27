---
layout: default
title: High-Damping Protection (Emergency Stop Response, M4LT2)
parent: Task Description
nav_order: 4.34
has_toc: true
nav_exclude: true
---

# High-Damping Protection (Emergency Stop Response, M4LT2)

* TOC
{:toc}

## Task Info

| Task | Task ID (TID) | Control |
|---|---|---|
| High-Damping Protection (Emergency Stop Response, M4LT2) | **4600** | High damping |

Applicable Models: **M4LT2**

Task Description:

- When the robot detects that the **hardware emergency stop switch** (ioboard emergency button) has been triggered, the control program automatically switches to this task.
- Unlike direct power-off (`TASK_SERVO_OFF`), this task keeps the joints powered and controls the rotary joints in a **high-damping, zero-spring** PD mode:
  - `kp ≈ 0` (0.001 in the implementation, which the firmware does not allow to be exactly 0): no restoring spring force; joints can be passively moved by external force.
  - `kd = 20 (default)`: Velocity damping braking force is applied to dissipate kinetic energy and prevent limbs from dropping or swinging rapidly.
  - Target position tracks the current measured position every frame in real time — no snap-back effect.
- This mode significantly reduces the risk of uncontrolled limb movement after an emergency stop, providing operators with a safer intervention window.

> ⚠️ **Note**:
>
> This task is **triggered automatically** by the control program when `flag_emergent_stop` is set. It is not recommended to switch to this task manually via the gamepad or User API.
> After the emergency stop is cleared, the robot will continue to hold the high-damping state. You must manually switch to another task (e.g., `TASK_STAND_CONTROL`) to resume normal motion control.

Task Parameters:

This task has no configurable parameters. The `kd` value must be tuned by a hardware engineer in `fi_algorithm_m4l_rotary_joint_high_damping.py` based on actual joint inertia.

## Trigger Conditions

This task is triggered by any of the following three conditions:

| Trigger Source | Trigger Condition | Description |
|----------------|-------------------|-------------|
| ioboard emergency switch | `ioboard.emergency_state == True` (sets `flag_emergent_stop`) | User presses the hardware emergency stop button on the robot backpack |
| All-actuator communication timeout | All actuators time out for ≥ 1.0 s (cycle count derived from the control period; sets `flag_emergent_stop`) | Protective trigger due to communication anomaly |
| Host heartbeat timeout | `flag_host_heartbeat_timeout` is set | Protective trigger when the host loses communication with the robot |

## Module Info

This task has no independent module commands and does not support per-joint control via the module interface.

## Interface Info

State Interface:

| Parameter | Interface Mapping | Description |
|-----------|------------------|-------------|
| Emergency stop flag | `robot.flag_robot_emergent_stop` | Remains SET while the high-damping task is active |

Command Interface:

This task requires no additional command parameters and is triggered automatically by the control program. It is registered for M4LT2 and can be activated with TID=4600, but manual activation through the host API is not recommended.

## Comparison with Servo Off

| Feature | High-Damping Protection (4600) | Servo Off (36) |
|---------|-------------------------------|----------------|
| Trigger method | Hardware emergency switch, auto-triggered (M4LT2) | Gamepad logo key / User API, manual |
| Joint power state | Remains powered, outputs damping torque | Powered off, no torque output |
| Safety characteristic | Soft braking — limbs do not drop instantly | Robot goes limp immediately |
| Recovery method | Manually switch to another task | Requires re-powering and task switch |

## Principle Explanation

### Algorithm Operation

High-damping protection turns the normal PD controller into a **velocity-energy dissipator centered on the current position**:

1. **Trigger**: a hardware emergency stop, all-actuator communication timeout, or host heartbeat timeout sets the protection flag, and the task manager automatically switches to TID 4600 without waiting for a gait-loop boundary.
2. **Follow measured position each frame**: `q_ref[k]=q_meas[k]`, with `Kp=0.001` because zero is not accepted and `Kd=20`. PD torque can be approximated as `τ=Kp(q_ref−q_meas)+Kd(ω_ref−ω_meas)`.
3. **Damping torque**: position reference equals measurement, so the position term is nearly zero. With velocity reference cleared, the main output is `τ≈−20·ω_meas`, opposing current motion. Instantaneous mechanical power `P=τ·ω≈−20·ω²≤0` dissipates joint energy instead of injecting a return-to-posture spring force.
4. **Clear inherited output**: both component and standalone paths zero velocity and effort feedforward targets so previous-task terms cannot be added to damping torque. At zero speed, damping torque is also nearly zero; no active return to standing occurs.
5. **Remain after release**: clearing the emergency signal does not automatically leave this mode; a later task must explicitly take control. High damping can reduce rapid flailing but has no position term for continuous static support and provides neither fall prevention nor posture recognition.

### Rehabilitation and Clinical Use

- Treat high damping as soft braking that buys response time, not as safe standing or a mode for continuing treatment. Staff must still support the patient and device immediately and check pain, skin, joint positions, and possible mechanical injury.
- Releasing the emergency stop does not resume training. Identify the trigger and confirm communication and hardware status before disabling, transferring the patient, or entering a preparation task according to local procedure. Do not resume gait directly with the cause unresolved.
- TID 4600 is not recommended as a routine pause or active-relaxation exercise. Damping depends on speed and model, and the patient can still move or slowly fall; maintain external fall protection.
- Recurrent emergency stops or heartbeat timeouts during training require stopping clinical use and investigating configuration, network, and device issues.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Added in `fourier-grx` v4.4.3 (M4LT2 only).
- Since `fourier-grx` v4.4.43, a host heartbeat timeout also switches to this task (previously only the hardware emergency stop and the all-actuator timeout triggered it).
- `fourier-grx` v4.4.71: this task's log now **distinguishes the trigger**. Previously every cause logged "Emergency stop detected"; reasons are now derived from `flag_emergent_stop` and `flag_host_heartbeat_timeout` (joined with " and " when both hold, reported as a manual activation when neither does). Since `flag_emergent_stop` is shared by the ioboard stop button and the all-actuator communication timeout, `flag_all_actuator_timeout` is consulted too: when set it reports "Emergency stop or all-actuator communication timeout", otherwise "Emergency stop (ioboard button)". The same release fixes this page's stale "≥ 50 consecutive control cycles" wording — it is 1.0 s, with the cycle count derived from the control period (200 cycles at T2's 200 Hz).
- `fourier-grx` v4.4.73: the high-damping task clears velocity and effort targets on both the component and standalone control paths, preventing stale feedforward commands from surviving a task switch.
