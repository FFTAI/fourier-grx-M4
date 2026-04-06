---
layout: default
title: Task Description
nav_order: 4
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

## Tasks and Modules

Robot task command list 🎏:

- Task commands are defined via the `fourier_grx.TaskCommand` enum class, as detailed below.
- The specific `Task Value (TID)` may vary depending on the robot model or `fourier-grx` version. **Always refer to the actual task information for the authoritative values.**

Common task command examples for M4 robots:

| Task Command                                      | Task Value (TID) | Applicable Models | Task Description                                                          |
|---------------------------------------------------|------------------|-------------------|---------------------------------------------------------------------------|
| TASK_SERVO_OFF                                    | 36               | All               | Power off and disable all robot joints                                    |
| TASK_SERVO_ON                                     | 35               | All               | Power on and enable all robot joints                                      |
| TASK_SERVO_REBOOT                                 | 41               | All               | Reboot all robot joints and reload configuration                          |
| TASK_CLEAR_FAULT                                  | 34               | All               | Clear alarms on all robot joints                                          |
| TASK_STAND_CONTROL                                | 4020             | M4L               | Slowly move all joints back to standing posture                           |
| TASK_ROTARY_JOINT_SET_HOME                        | 4103             | M4L               | Set the current position of rotary joints as zero (manual)                |
| TASK_ROTARY_JOINT_BORDER_AND_RETURN               | 4104             | M4L               | Rotary joint boundary detection: drive to mechanical limit then auto-return |
| TASK_ROTARY_JOINT_SET_HOME_POSITION               | 4105             | M4L               | Sample mean, then set current position as rotary joint zero (software layer) |
| TASK_ROTARY_JOINT_MOVE_BACK                       | 4106             | M4L               | Return rotary joints to a safe position                                   |
| TASK_ROTARY_JOINT_AUTO_CALIBRATE                  | 4120             | M4L               | Automatic rotary joint calibration (boundary detection → power off → set zero, three sequential steps) |
| TASK_PRISMATIC_JOINT_AUTO_CALIBRATE               | 4210             | M4L               | Automatic prismatic joint calibration (must be performed first after power-on) |
| TASK_ROTARY_JOINT_FORWARD_WALK                    | 4111             | M4L               | Passive forward walking                                                   |
| TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_PD   | 4116             | M4L               | Assisted forward walking (adjust PD parameters)                           |
| TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_DT   | 4118             | M4L               | Assisted forward walking (adjust dt parameters)                           |
| TASK_ROTARY_JOINT_MARK_TIME                       | 4112             | M4L               | Passive marching in place                                                 |
| TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_PD      | 4117             | M4L               | Assisted marching in place (adjust PD parameters)                         |
| TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_DT      | 4119             | M4L               | Assisted marching in place (adjust dt parameters)                         |

- All: Indicates all Fourier Intelligence production robot models.

---

## Task Documentation Index

The pages below are the primary task descriptions organized in this repository and serve as entry points for each task. For task-switching protocol details, refer to the `task/client Interface Protocol (Command Information)` section in the [Reference Guide — User API](/fourier-grx-M4/docs/en/reference/user).

### Basic Control Tasks

- [Actuator Enable](/fourier-grx-M4/docs/en/tasks/servo_on)
- [Actuator Disable](/fourier-grx-M4/docs/en/tasks/servo_off)
- [Actuator Reboot](/fourier-grx-M4/docs/en/tasks/servo_reboot)
- [Clear Fault](/fourier-grx-M4/docs/en/tasks/clear_fault)
- [Set Home](/fourier-grx-M4/docs/en/tasks/set_home)

### Motion Tasks

- [Standing Posture Control](/fourier-grx-M4/docs/en/tasks/stand_motion_control)
- [Passive Forward Walking](/fourier-grx-M4/docs/en/tasks/forward_walk_passive)
- [Assisted Forward Walking (Adjust PD Parameters)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd)
- [Assisted Forward Walking (Adjust dt Parameters)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt)
- [Passive Marching in Place](/fourier-grx-M4/docs/en/tasks/mark_time_passive)
- [Assisted Marching in Place (Adjust PD Parameters)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_pd)
- [Assisted Marching in Place (Adjust dt Parameters)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt)

### Knee-Restriction Tasks

- [Standing Posture Control (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_stand_motion_control)
- [Passive Forward Walking (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive)
- [Assisted Forward Walking (Knee Restriction, Adjust PD Parameters)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_pd)
- [Assisted Forward Walking (Knee Restriction, Adjust dt Parameters)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_dt)
- [Passive Marching in Place (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_passive)
- [Assisted Marching in Place (Knee Restriction, Adjust PD Parameters)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_pd)
- [Assisted Marching in Place (Knee Restriction, Adjust dt Parameters)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

### Specialized & Extended Tasks

- [Set Home (Rotary Joints)](/fourier-grx-M4/docs/en/tasks/set_home_rotary_joint)
- [Calibrate Home (Prismatic Joints)](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint)
- [Move to Length (Prismatic Joints)](/fourier-grx-M4/docs/en/tasks/move_length_prismatic_joint)
- [Planner](/fourier-grx-M4/docs/en/tasks/planner)

Robot module command list 🎏:

- A module can be understood as a sub-task unit within a task. Because sub-tasks can have **mutually exclusive or combinable** relationships with each other, they are managed as **modules** rather than plain sub-tasks.
- When one of several mutually exclusive modules is activated, the others are automatically suspended by the control program.
- Combinable modules can be activated and switched independently without affecting each other.
- The lifecycle management of modules is handled entirely within the control program; the upper layer does not need to worry about the risks of module switching.
- The `Module Value (MID)` is closely tied to the robot model and may change with version updates. If a module task does not execute as expected, update to the latest firmware and **refer to the module information described in the specific task page for authoritative values**.

## Task Switching

The method for switching tasks differs depending on how the robot is being controlled. The following table summarizes common task-switching methods:

|                    | Physical Gamepad | Physical Keyboard  | User API (Communication)                                          | Developer API (Communication)                                                         |
|--------------------|------------------|--------------------|-------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Task Selection     | `L1` button      | `Up`/`Down` keys   | Send `Task Value (TID)` via `task.robot_task_command`            |                                                                                       |
| Task Confirmation  | `L2` button      | `Enter` key        | Send `1` via `task.flag_task_command_update` to confirm update   | Send `Task Value (TID)` via `control_system.robot_control_set_task_command(TID)`     |
| Module Selection   | `R1` button      |                    | Send `Module Value (MID)` via `task.robot_component_command`     |                                                                                       |
| Module Confirmation| `R2` button      |                    | Send `1` via `task.flag_component_command_update` to confirm update | Send `Module Value (MID)` via `control_system.robot_control_set_task_component(MID)` |
