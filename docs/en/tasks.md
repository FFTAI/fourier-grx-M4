---
layout: default
title: Task Description
nav_order: 4
has_children: true
has_toc: true
nav_exclude: true
---

# Task Description

* TOC
{:toc}

> ⚠️ **Note**:
>
> Tasks not listed in this chapter may still appear when using a gamepad to control the robot and select tasks. This indicates the task may still be under development, or has been partially deprecated (not yet removed from the menu).
> Therefore, it is recommended that developers exercise caution when selecting tasks not listed in this chapter during gamepad operation. Only attempt the task commands listed in the [Task Description](/fourier-grx-M4/docs/en/tasks) section of this technical documentation.

## Task Commands

Robot task command list 🎏:

- Task commands are defined via enum classes: `fourier_grx.task.menu.TaskMenuM4L` for the M4L robots, and `fourier_grx.task.menu.TaskMenuRobotReal` for the common power-off / power-on / clear-fault commands, as detailed below.
- The specific `Task Value (TID)` may vary depending on the robot model or `fourier-grx` version. **Always refer to the actual task information for the authoritative values.**

Common task command examples for M4L robots:

| Task Command                                      | Task Value (TID) | Applicable Models | Task Description                                                          |
|---------------------------------------------------|------------------|-------------------|---------------------------------------------------------------------------|
| TASK_SERVO_OFF                                    | 36               | All               | Power off and disable all robot joints                                    |
| TASK_SERVO_ON                                     | 35               | All               | Power on and enable all robot joints                                      |
| TASK_SERVO_REBOOT                                 | 41               | All               | Reboot all robot joints and reload configuration                          |
| TASK_CLEAR_FAULT                                  | 34               | All               | Clear alarms on all robot joints                                          |
| TASK_STAND_CONTROL                                | 4020             | M4L               | Slowly move all joints back to standing posture                           |
| TASK_ROTARY_JOINT_SET_HOME                        | 4103             | M4L               | Set the current rotary joint position as the actuator-level zero (includes an actuator reboot) |
| TASK_ROTARY_JOINT_BORDER_AND_RETURN               | 4104             | M4L               | Rotary joint boundary detection: drive to mechanical limit then auto-return |
| TASK_ROTARY_JOINT_SET_HOME_POSITION               | 4105             | M4L               | Sample the mean, then set the current position as the rotary joint zero (software application layer, no reboot) |
| TASK_ROTARY_JOINT_MOVE_BACK                       | 4106             | M4L               | Return rotary joints to a safe position (enum placeholder only; no task implementation in the current firmware) |
| TASK_ROTARY_JOINT_AUTO_CALIBRATE                  | 4120             | M4L               | Automatic rotary joint calibration (boundary detection → power off → set zero, three sequential steps) |
| TASK_ROTARY_JOINT_MANUAL_CALIBRATE                | 4121             | M4L               | Manual rotary joint calibration (power off → user manually positions joints → set zero, two sequential steps) |
| TASK_ROTARY_JOINT_MANUAL_CALIBRATE_LEFT_LEG       | 4122             | M4L               | Manual rotary joint calibration for the left leg only (only the left leg powers off and sets its zero point; the right leg stays in support) |
| TASK_ROTARY_JOINT_MANUAL_CALIBRATE_RIGHT_LEG      | 4123             | M4L               | Manual rotary joint calibration for the right leg only (only the right leg powers off and sets its zero point; the left leg stays in support) |
| TASK_PRISMATIC_JOINT_AUTO_CALIBRATE               | 4210             | M4L               | Automatic prismatic joint calibration (must be performed first after power-on) |
| TASK_PRISMATIC_JOINT_MOVE_LENGTH                  | 4206             | M4L               | Leg-length adjustment (absolute position command)                         |
| TASK_PRISMATIC_JOINT_MOVE_OFFSET                  | 4207             | M4L               | Relative leg-length adjustment (offset from the current position, no re-calibration required) |
| TASK_ROTARY_JOINT_FORWARD_WALK                    | 4129             | M4L               | Passive forward walking (4111 before v4.4.69)                             |
| TASK_ROTARY_JOINT_FORWARD_WALK_HARMONIC           | 4131             | M4L               | Passive forward walking – harmonic fitting (pre-computed gait curves; amplitude / knee-restriction / cadence levels; 4113 before v4.4.69) |
| TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_PD   | 4116             | M4L               | Assisted forward walking (adjust PD parameters)                           |
| TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_DT   | 4118             | M4L               | Assisted forward walking (adjust dt parameters)                           |
| TASK_ROTARY_JOINT_FORWARD_WALK_HARMONIC_ASSIST_ADJUST_PD | 4132      | M4L               | Assisted forward walking – harmonic fitting (PD Mode; same three panel levels as 4131, assist ratio on param_4; added in v4.4.79) |
| TASK_ROTARY_JOINT_FORWARD_WALK_HARMONIC_ASSIST_ADJUST_DT | 4133      | M4L               | Assisted forward walking – harmonic fitting (dt Mode; same three panel levels as 4131, assist ratio on param_4; added in v4.4.79) |
| [TASK_ROTARY_JOINT_FORWARD_WALK_HIGH_LIFT](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift) | 4134 | M4L | Passive forward walking – high-lift (`param_3` sets the target lift peak in cm; added in v4.4.85) |
| [TASK_ROTARY_JOINT_FORWARD_WALK_HIGH_LIFT_PD_FF](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift) | 4135 | M4L | Passive forward walking – high-lift + velocity feedforward (added in v4.4.85) |
| [TASK_ROTARY_JOINT_FORWARD_WALK_HIGH_LIFT_ASSIST_ADJUST_PD](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist) | 4136 | M4L | Assisted forward walking – high-lift (PD Mode; added in v4.4.87) |
| [TASK_ROTARY_JOINT_FORWARD_WALK_HIGH_LIFT_ASSIST_ADJUST_DT](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist_adjust_dt) | 4137 | M4L | Assisted forward walking – high-lift (dt Mode; added in v4.4.87) |
| [TASK_ROTARY_JOINT_KNEE_RESTRICTION_FORWARD_WALK_HIGH_LIFT](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift) | 4307 | M4L | Passive forward walking – high-lift (knee restriction; added in v4.4.89) |
| [TASK_ROTARY_JOINT_PLANNER_FORWARD_WALK_HIGH_LIFT](/fourier-grx-M4/docs/en/tasks/planner) | 4410 | M4L | Passive forward walking – high-lift Planner (reference only, no joint output; added in v4.4.89) |
| [TASK_ROTARY_JOINT_PLANNER_KNEE_RESTRICTION_FORWARD_WALK_HIGH_LIFT](/fourier-grx-M4/docs/en/tasks/planner) | 4507 | M4L | Knee-restricted high-lift Planner (reference only, no joint output; added in v4.4.89) |
| TASK_ROTARY_JOINT_MARK_TIME                       | 4130             | M4L               | Passive marching in place (4112 before v4.4.69)                           |
| TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_PD      | 4117             | M4L               | Assisted marching in place (adjust PD parameters)                         |
| TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_DT      | 4119             | M4L               | Assisted marching in place (adjust dt parameters)                         |
| TASK_ROTARY_JOINT_HIGH_DAMPING                    | 4600             | M4LT2             | High-damping protection task triggered automatically on emergency stop (kp≈0, kd=20, soft braking) |

- All: Indicates all Fourier Intelligence production robot models.

### Rotary joint TID changes in v4.4.69

From `fourier-grx` v4.4.69 the rotary-joint tasks are regrouped by control mode, and **the task behind a given TID has changed** — integrators must update accordingly:

| Task | v4.4.68 and earlier | v4.4.69 onwards |
|------|---------------------|-----------------|
| Sinusoidal trajectory | 4110 | **4128** |
| Passive forward walking | 4111 | **4129** |
| Passive marching in place | 4112 | **4130** |
| Passive forward walking – harmonic fitting | 4113 | **4131** |
| Passive forward walking · POSITION + velocity feedforward | 4124 | **4125** |
| Passive marching in place · POSITION + velocity feedforward | 4125 | **4126** |
| Passive forward walking · PD + velocity feedforward | 4126 | **4111** |
| Passive marching in place · PD + velocity feedforward | 4127 | **4112** |
| Sinusoidal trajectory · POSITION + velocity feedforward | none (new) | **4124** |
| Sinusoidal trajectory · PD + velocity feedforward | none (new) | **4110** |
| Passive forward walking – harmonic fitting · POSITION + velocity feedforward | none (new) | **4127** |
| Passive forward walking – harmonic fitting · PD + velocity feedforward | none (new) | **4113** |

- ⚠️ **4110–4113 are redefinitions, not additions**: after upgrading, a host that still calls 4111 for passive forward walking will get the PD + feedforward variant instead. Use **4129**.
- Assist tasks (4114–4119) and calibration tasks (4120–4123) keep their TIDs.
- The feedforward family grows from 4 tasks to 8; POSITION variants run the actuator position loop, and the PD variants' velocity feedforward is effective only on M4LT2 (FSA v3) — it is silently dropped by the protocol on P1 / T1.

> Note:
>
> - `TaskMenuM4L` also contains several implemented tasks that are not expanded in this chapter; they are mainly used as internal calibration steps and for joint-level debugging: 4104 (border detection and return), 4105 (software-layer set home), 4110 (rotary joint sine wave test), 4100 / 4200 (joint PD test), 4203 / 4204 / 4205 (prismatic joint set home and end-limit moves, where 4204 is the internal step of the 4210 auto calibration).
> - The following enum entries have no implementation in the current firmware and are kept as placeholders only: 4000, 4010, 4011, 4101, 4102, 4106, 4114, 4115, 4201, 4202. They may still appear in the gamepad task list — do not use them in production workflows.

## Robot Modules

Robot module command list 🎏:

- A module can be understood as a sub-task unit within a task. Because sub-tasks can have **mutually exclusive or combinable** relationships with each other, they are managed as **modules** rather than plain sub-tasks.
- When one of several mutually exclusive modules is activated, the others are automatically suspended by the control program.
- Combinable modules can be activated and switched independently without affecting each other.
- The lifecycle management of modules is handled entirely within the control program; the upper layer does not need to worry about the risks of module switching.
- The `Module Value (MID)` is closely tied to the robot model and may change with version updates. If a module task does not execute as expected, update to the latest firmware and **refer to the module information described in the specific task page for authoritative values**.

---

## Task Documentation Index

The pages below are the primary task descriptions organized in this repository and serve as entry points for each task. For task-switching protocol details, refer to the `task/client Interface Protocol (Command Information)` section in the [Reference Guide — User API](/fourier-grx-M4/docs/en/reference/user).

### Basic Control Tasks

- [Servo On](/fourier-grx-M4/docs/en/tasks/servo_on)
- [Servo Off](/fourier-grx-M4/docs/en/tasks/servo_off)
- [Servo Reboot](/fourier-grx-M4/docs/en/tasks/servo_reboot)
- [Clear Fault](/fourier-grx-M4/docs/en/tasks/clear_fault)
- [Set Home](/fourier-grx-M4/docs/en/tasks/set_home)

### Home & Calibration Tasks

- [Set Home (Rotary Joint)](/fourier-grx-M4/docs/en/tasks/set_home_rotary_joint)
- [Auto Calibrate (Rotary Joint)](/fourier-grx-M4/docs/en/tasks/rotary_joint_auto_calibrate)
- [Manual Calibrate (Rotary Joint)](/fourier-grx-M4/docs/en/tasks/rotary_joint_manual_calibrate)
- [Auto Calibrate (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint)

### Passive Motion Control

- [Standing Posture Control](/fourier-grx-M4/docs/en/tasks/stand_motion_control)
- [Passive Forward Walking](/fourier-grx-M4/docs/en/tasks/forward_walk_passive)
- [Passive Forward Walking – Harmonic Fitting](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic)
- [Passive Forward Walking – High-Lift](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift)
- [Passive Marching in Place](/fourier-grx-M4/docs/en/tasks/mark_time_passive)

### Assisted Motion Control

- [Assisted Forward Walking (PD Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd)
- [Assisted Forward Walking (dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt)
- [Assisted Forward Walking – Harmonic Fitting (PD Mode)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd)
- [Assisted Forward Walking – Harmonic Fitting (dt Mode)](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_dt)
- [Assisted Forward Walking – High-Lift (PD Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist)
- [Assisted Forward Walking – High-Lift (dt Mode)](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift_assist_adjust_dt)
- [Assisted Marching in Place (PD Mode)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_pd)
- [Assisted Marching in Place (dt Mode)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt)

### Knee-Restriction Tasks

- [Standing Posture Control (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_stand_motion_control)
- [Passive Forward Walking (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive)
- [Assisted Forward Walking (Knee Restriction, PD Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_pd)
- [Assisted Forward Walking (Knee Restriction, dt Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_dt)
- [Passive Marching in Place (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_passive)
- [Assisted Marching in Place (Knee Restriction, PD Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_pd)
- [Assisted Marching in Place (Knee Restriction, dt Mode)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

### Leg-Length Adjustment Tasks

- [Adjust Length (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_length_prismatic_joint)
- [Move by Offset (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_offset_prismatic_joint)

### Planner

- [Planner](/fourier-grx-M4/docs/en/tasks/planner)

### Emergency Protection Tasks

- [High-Damping Protection (Emergency Stop Response, M4LT2)](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping)

### Algorithm Topics

- [Gait Generation Algorithms](/fourier-grx-M4/docs/en/tasks/gait_generation_algorithms)

## Task Switching

The method for switching tasks differs depending on how the robot is being controlled. The following table summarizes common task-switching methods:

|                    | Physical Gamepad | Physical Keyboard  | User API (Communication)                                          | Developer API (Communication)                                                         |
|--------------------|------------------|--------------------|-------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Task Selection     | `L1` button      | `Up`/`Down` keys   | Send `Task Value (TID)` via `task.robot_task_command`            |                                                                                       |
| Task Confirmation  | `L2` double-click | `Enter` key       | Send `1` via `task.flag_task_command_update` to confirm update   | Send `Task Value (TID)` via `control_system.robot_control_set_task_command(TID)`     |
| Module Selection   | `R1` button      |                    | Send `Module Value (MID)` via `task.robot_component_command`     |                                                                                       |
| Module Confirmation| `R2` double-click |                   | Send `1` via `task.flag_component_command_update` to confirm update | Send `Module Value (MID)` via `control_system.robot_control_set_task_component(MID)` |

> ℹ️ For task registration, switch order, hook lifecycle, and safety overrides, see [Task Lifecycle and Switching](/fourier-grx-M4/docs/en/reference/task_lifecycle).
