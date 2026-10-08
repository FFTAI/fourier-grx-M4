---
layout: default
title: Velocity & Position Protection
nav_order: 3.9
parent: Reference Guide
has_toc: true
---

# Velocity & Position Protection

* TOC
{:toc}

While the M4L device is running, it continuously monitors joint velocity and joint position. If abnormal over-speed occurs, or a joint position goes far beyond its reasonable motion range, the controller automatically enters the protection state (all actuators disabled) to avoid harming the user. The two protections are independent of each other, and both can be cleared by the host to resume operation.

---

## Trigger Conditions

| Protection | Monitored Object | Trigger Condition |
|-----------|------------------|-------------------|
| Velocity protection | Measured joint velocity of the 4 rotary joints (hip/knee) | Any rotary joint velocity exceeds the threshold (default 15 rad/s, tunable on hardware) for 5 consecutive control cycles |
| Position protection | Measured joint position | Any joint position stays outside the "reasonable motion range" (published by the active task, see below) for 5 consecutive control cycles |

Notes:

- **Debounce**: both protections require 5 consecutive control cycles beyond the limit before triggering, to avoid false triggers from measurement noise;
- **Velocity protection** only monitors the 4 rotary joints by default; the prismatic joints (leg-length adjustment) are not covered;
- **Normal gait never triggers the protections**: validated by full-parameter-range simulation — within the allowed command parameter ranges, the peak joint velocity of mark-time/forward-walk is at worst ~10 rad/s (threshold 15 rad/s), and the joint position always stays inside the task-published reasonable range.

### The "Reasonable Motion Range" of Position Protection

The reasonable range **varies automatically with the task and gait parameters**, and is published by the active task:

1. When the task is activated, the range is initialized to **current joint position ± margin** (default 0.35 rad);
2. While running, the task merges the **reference trajectory extremes** and the **current commanded target position** into the range every cycle (union, grow-only) — therefore mark-time and forward-walk have different ranges, and the range follows automatically when gait parameters change mid-run;
3. When the task exits, the range is reset to disabled (±inf).

Position protection triggers only when the joint position goes **far beyond every position the task has ever commanded, plus the margin** — i.e. a genuine runaway. Normal tracking errors and start-transition segments do not trigger it.

Tasks currently integrated with position protection: **stand, mark time, forward walk** and their derived tasks (knee-restriction series, application series, assist_adjust series). Calibration/test tasks are not integrated yet.

---

## Protection Behavior

Once triggered, the controller performs the following steps:

1. Prints an error log (joint index, measured value, threshold/range);
2. Sets the corresponding protection flag:
   - Velocity protection: `flag_robot_velocity_protection`
   - Position protection: `flag_robot_position_protection`
3. Switches to `TASK_SERVO_OFF`, disabling all actuators (the robot goes limp — make sure mechanical support is in place);
4. **Latching**: until the flag is cleared, any other task command sent by the host is overridden back to `TASK_SERVO_OFF`, keeping the robot in the protection state.

---

## Clearing Errors and Recovery

1. The host reads the protection flag from the `robot/server` topic and confirms it is `SET`;
2. After eliminating the abnormal condition, the host writes the corresponding clear field (write 1; the controller clears it automatically after processing):
   - `clear_flag_robot_velocity_protection`
   - `clear_flag_robot_position_protection`
3. The controller clears the robot-side flag and releases the latch;
4. The host sends task commands again (e.g. `TASK_SERVO_ON` or a control task), and the robot resumes normal operation.

> ℹ️ The two protections are independent: triggering and clearing one protection does not affect the other protection's flag.

---

## Related Fields

| Field | Direction | Description |
|-------|-----------|-------------|
| `flag_robot_velocity_protection` | Server → Client | Velocity protection flag, `SET` means triggered |
| `flag_robot_position_protection` | Server → Client | Position protection flag, `SET` means triggered |
| `clear_flag_robot_velocity_protection` | Client → Server | Write 1 to clear the velocity protection flag |
| `clear_flag_robot_position_protection` | Client → Server | Write 1 to clear the position protection flag |

For the complete protocol definitions, see [User Interface](/fourier-grx-M4/docs/en/reference/user).
