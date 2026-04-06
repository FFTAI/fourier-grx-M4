---
layout: default
title: User API
nav_order: 3.1
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Reference Guide — User API

* TOC
{:toc}

> ℹ️ **Note**:
>
> Before using the Fourier-GRX-M4 SDK User API, configure `fourier-grx` to **developer mode**.
> For information on configuring the run type, see [Run Type](/fourier-grx-M4/docs/en/reference/run_type).

The Fourier-GRX User API communicates with the robot using the [Zenoh](https://zenoh.io/) protocol and is suitable for high-level application development.

The User API is divided into five categories:

- `comm`: Communication-related information
- `robot`: Robot state information
- `task`: Task-related information
- `grx`: fourier-grx library information; general robot content (primarily humanoid)
- `rehab`: Rehabilitation robot information

The Zenoh topic key format for these interfaces is:

- key can be one of ["comm", "robot", "task", "grx", "rehab"]
- `fourier-grx/dynalink_interface/{key}/server`: State information published by the robot main control program **[robot acts as server]**
- `fourier-grx/dynalink_interface/{key}/client`: Command information received by the robot main control program **[user machine acts as client]**

---

## State Information

### comm/server Interface Protocol (State Information)

Key description list:

| Key                              | Description                                    | Type | Details                             |
|----------------------------------|------------------------------------------------|------|-------------------------------------|
| `flag_heart_beat`                | Heartbeat flag                                 | bool | 1: robot has started                |
| `flag_ethernet_connect_status`   | Host-to-robot Ethernet connection status       | bool | 0: not connected, 1: connected      |

### robot/server Interface Protocol (State Information)

**Sensor Information**

| Key                                     | Description                  | Type         | Details                                                           |
|-----------------------------------------|------------------------------|--------------|-------------------------------------------------------------------|
| `sensor_imus_quat_value`                | IMU quaternion               | array(float) | Concatenated quaternions [x, y, z, w] for each IMU               |
| `sensor_imus_euler_angle_value`         | IMU Euler angles             | array(float) | Euler angles [roll, pitch, yaw] for each IMU, unit: radians       |
| `sensor_imus_angular_velocity_value`    | IMU angular velocity         | array(float) | Angular velocity [x, y, z] for each IMU, unit: rad/s             |
| `sensor_imus_linear_acceleration_value` | IMU linear acceleration      | array(float) | Linear acceleration [x, y, z] for each IMU, unit: m/s²           |

**Actuator Flags**

| Key                        | Description                        | Type        | Details                                      |
|----------------------------|------------------------------------|-------------|----------------------------------------------|
| `flag_actuator_installed`  | Actuator installation status       | array(bool) | Whether each actuator is installed           |
| `flag_actuator_accessible` | Actuator accessibility status      | array(bool) | Whether each actuator is accessible via communication |
| `flag_actuator_enables`    | Actuator enable status             | array(bool) | Whether each actuator is enabled             |
| `flag_actuator_error`      | Actuator error status              | array(bool) | Whether each actuator has an error           |

**Actuator Measured Information**

| Key                              | Description                      | Type         | Details                                               |
|----------------------------------|----------------------------------|--------------|-------------------------------------------------------|
| `actuator_measured_control_mode` | Actuator control mode            | array(int)   | Current control mode of each actuator                 |
| `actuator_measured_position`     | Actuator measured position       | array(float) | Measured position, unit: radians or meters            |
| `actuator_measured_velocity`     | Actuator measured velocity       | array(float) | Measured velocity, unit: rad/s or m/s                 |
| `actuator_measured_acceleration` | Actuator measured acceleration   | array(float) | Measured acceleration, unit: rad/s²                   |
| `actuator_measured_effort`       | Actuator measured torque         | array(float) | Measured torque, unit: Nm                             |
| `actuator_measured_current`      | Actuator measured current        | array(float) | Measured current, unit: A                             |

**Actuator Command Information**

| Key                             | Description                       | Type         | Details                                               |
|---------------------------------|-----------------------------------|--------------|-------------------------------------------------------|
| `actuator_output_control_mode`  | Actuator command control mode     | array(int)   | Command control mode of each actuator                 |
| `actuator_output_position`      | Actuator command position         | array(float) | Command position, unit: radians or meters             |
| `actuator_output_velocity`      | Actuator command velocity         | array(float) | Command velocity, unit: rad/s or m/s                  |
| `actuator_output_acceleration`  | Actuator command acceleration     | array(float) | Command acceleration, unit: rad/s²                    |
| `actuator_output_effort`        | Actuator command torque           | array(float) | Command torque, unit: Nm                              |
| `actuator_output_current`       | Actuator command current          | array(float) | Command current, unit: A                              |

**Joint Status Words**

| Key                       | Description             | Type       | Details                              |
|---------------------------|-------------------------|------------|--------------------------------------|
| `joint_mode_of_operation` | Joint operation mode    | array(int) | Current operation mode of each joint |
| `joint_control_word`      | Joint control word      | array(int) | Control word of each joint           |
| `joint_status_word`       | Joint status word       | array(int) | Status word of each joint            |

**Joint Application-Layer Information**

| Key                          | Description                          | Type         | Details                                                          |
|------------------------------|--------------------------------------|--------------|------------------------------------------------------------------|
| `joint_application_position` | Joint application-layer target position | array(float) | Target joint position written by the application layer, unit: radians or meters |
| `joint_application_velocity` | Joint application-layer target velocity | array(float) | Target joint velocity written by the application layer, unit: rad/s or m/s     |
| `joint_application_effort`   | Joint application-layer target torque   | array(float) | Target joint torque written by the application layer, unit: Nm                 |

**Joint Measured Information**

| Key                           | Description                    | Type         | Details                                  |
|-------------------------------|--------------------------------|--------------|------------------------------------------|
| `joint_measured_control_mode` | Joint measured control mode    | array(int)   | Current control mode of each joint       |
| `joint_measured_position`     | Joint measured position        | array(float) | Measured position, unit: radians         |
| `joint_measured_velocity`     | Joint measured velocity        | array(float) | Measured velocity, unit: rad/s           |
| `joint_measured_acceleration` | Joint measured acceleration    | array(float) | Measured acceleration, unit: rad/s²      |
| `joint_measured_effort`       | Joint measured torque          | array(float) | Measured torque, unit: Nm                |
| `joint_measured_current`      | Joint measured current         | array(float) | Measured current, unit: A                |

**Joint Command Information**

| Key                         | Description                  | Type         | Details                                  |
|-----------------------------|------------------------------|--------------|------------------------------------------|
| `joint_output_control_mode` | Joint command control mode   | array(int)   | Command control mode of each joint       |
| `joint_output_position`     | Joint command position       | array(float) | Command position, unit: radians          |
| `joint_output_velocity`     | Joint command velocity       | array(float) | Command velocity, unit: rad/s            |
| `joint_output_acceleration` | Joint command acceleration   | array(float) | Command acceleration, unit: rad/s²       |
| `joint_output_effort`       | Joint command torque         | array(float) | Command torque, unit: Nm                 |
| `joint_output_current`      | Joint command current        | array(float) | Command current, unit: A                 |

**End-Effector Measured Information**

| Key                                  | Description                         | Type         | Details                                       |
|--------------------------------------|-------------------------------------|--------------|-----------------------------------------------|
| `end_effector_measured_position`     | End-effector measured position      | array(float) | Measured position, unit: meters               |
| `end_effector_measured_velocity`     | End-effector measured velocity      | array(float) | Measured velocity, unit: m/s                  |
| `end_effector_measured_acceleration` | End-effector measured acceleration  | array(float) | Measured acceleration, unit: m/s²             |
| `end_effector_measured_effort`       | End-effector measured torque        | array(float) | Measured torque, unit: Nm                     |

**Robot Status Flags**

| Key                            | Description                        | Type | Details                                     |
|--------------------------------|------------------------------------|------|---------------------------------------------|
| `flag_robot_self_check`        | Robot self-check success flag      | bool | 0: self-check failed, 1: self-check passed  |
| `flag_robot_calibration`       | Robot calibration complete flag    | bool | 0: calibration failed, 1: calibration passed |
| `flag_robot_servo_on`          | Robot servo enable flag            | bool | 0: servo not enabled, 1: servo enabled      |
| `flag_robot_emergent_stop`     | Robot emergency stop flag          | bool | 0: not e-stopped, 1: e-stopped              |
| `flag_robot_fault`             | Robot fault flag                   | bool | 0: no fault, 1: fault present               |
| `flag_robot_error`             | Robot error flag                   | bool | 0: no error, 1: error present               |
| `flag_robot_pinched`           | Robot pinch flag                   | bool | 0: not pinched, 1: pinched                  |
| `flag_robot_over_load`         | Robot overload flag                | bool | 0: not overloaded, 1: overloaded            |
| `flag_robot_torque_protection` | Robot torque protection flag       | bool | 0: not triggered, 1: triggered              |

**Robot Basic Information**

| Key                | Description            | Type   | Details                                  |
|--------------------|------------------------|--------|------------------------------------------|
| `robot_name`       | Robot name             | string | Current robot model name                 |
| `robot_work_space` | Robot workspace        | int    | Current robot workspace index            |

### task/server Interface Protocol (State Information)

**Task State Information**

| Key                      | Description                | Type | Details                                                                                                                                                     |
|--------------------------|----------------------------|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `flag_task_start`        | Task start flag            | bool | 0: task not started, 1: task started                                                                                                                        |
| `flag_task_running`      | Task running flag          | bool | 0: task not running, 1: task running                                                                                                                        |
| `flag_task_finish`       | Task finish flag           | bool | 0: task not finished, 1: task finished                                                                                                                      |
| `flag_task_pause`        | Task pause flag            | bool | 0: task not paused, 1: task paused                                                                                                                          |
| `robot_task_state`       | Robot task state           | int  | Current robot task state (TID value). If `flag_task_command_update` in task/client is set to True, this value is updated to `robot_task_command` from task/client |
| `robot_task_state_data`  | Robot task state data      | dict | Additional state data for the current task; content varies by task                                                                                          |

**Module State Information**

| Key                          | Description                 | Type | Details                                         |
|------------------------------|-----------------------------|------|-------------------------------------------------|
| `flag_component_start`       | Module start flag           | bool | 0: module not started, 1: module started        |
| `flag_component_in_process`  | Module running flag         | bool | 0: module not running, 1: module running        |
| `flag_component_finish`      | Module finish flag          | bool | 0: module not finished, 1: module finished      |
| `robot_component_state`      | Robot module state          | int  | Current robot module state (MID value)          |
| `robot_component_state_data` | Robot module state data     | dict | Additional state data for the current module; content varies by module |

### grx/server Interface Protocol (State Information)

Key description list:

| Key                        | Description               | Type         | Details                                                        |
|----------------------------|---------------------------|--------------|----------------------------------------------------------------|
| `fourier_core_version`     | Core library version      | string       | Core library version number                                    |
| `fourier_grx_version`      | GRX library version       | string       | GRX library version number                                     |
| `robot_error_codes`        | Robot error codes         | array(int)   | Robot error code list; 0: no error, other: specific error code |
| `robot_battery_percentage` | Battery percentage        | float        | Current battery level, range [0.0, 1.0]; 1.0 = fully charged  |
| `robot_charging_level`     | Battery level grade       | int          | Battery level grade, range 1–3; 3 is the highest              |
| `robot_charging_state`     | Battery charging state    | float        | 0.0: not charging, 1.0: charging                               |

### rehab/server Interface Protocol (State Information)

Key description list:

| Key                            | Description                        | Type         | Details                                                                                                                                 |
|--------------------------------|------------------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `reference_joint_position`     | Joint reference position           | array(float) | Target joint positions planned in the current control cycle, unit: radians. Updated every control cycle; can be used for visualization or trajectory recording on the host PC. |
| `reference_joint_velocity`     | Joint reference velocity           | array(float) | Target joint velocities planned in the current control cycle, unit: rad/s. Updated synchronously with `reference_joint_position`.       |
| `reference_joint_position_max` | Joint reference maximum position   | array(float) | Maximum target position for each joint over the entire motion trajectory, unit: radians. Can be used to display joint range of motion on the host PC. |
| `reference_joint_position_min` | Joint reference minimum position   | array(float) | Minimum target position for each joint over the entire motion trajectory, unit: radians. Can be used to display joint range of motion on the host PC. |
| `motion_ratio`                 | Motion progress ratio              | float        | Completion ratio of the current task's motion, range [0, 1]. Can be used for progress display or multi-device synchronization.          |

---

## Command Information

### comm/client Interface Protocol (Command Information)

> ℹ️ **This interface is not yet open.** The comm/client channel is used for system-level communication commands. The current version has no writable fields; it exists as a reserved interface only.

### robot/client Interface Protocol (Command Information)

Key description list:

| Key                                  | Description                          | Type | Details                    |
|--------------------------------------|--------------------------------------|------|----------------------------|
| `clear_flag_robot_over_load`         | Clear overload flag                  | bool | 0: do not clear, 1: clear  |
| `clear_flag_robot_torque_protection` | Clear torque protection flag         | bool | 0: do not clear, 1: clear  |

### task/client Interface Protocol (Command Information)

The task command send interface is as follows. Commands must be sent in this order:

- Task command send:
    1. Send `robot_task_command` and `robot_task_command_data` with task-related information
    2. Send `flag_task_command_update` to confirm the task command update
- Module command send:
    1. Send `robot_component_command` and `robot_component_command_data` with module-related information
    2. Send `flag_component_command_update` to confirm the module command update

Key description list:

| Key                             | Description                         | Type | Details                          |
|---------------------------------|-------------------------------------|------|----------------------------------|
| `flag_task_command_update`      | Task command request update flag    | bool | 0: do not update, 1: update      |
| `robot_task_command`            | Task command                        | int  | Robot task command (TID value)   |
| `robot_task_command_data`       | Task command data                   | dict | Robot task command data          |
| `flag_component_command_update` | Module command request update flag  | bool | 0: do not update, 1: update      |
| `robot_component_command`       | Module command                      | int  | Robot module command (MID value) |
| `robot_component_command_data`  | Module command data                 | dict | Robot module command data        |

### grx/client Interface Protocol (Command Information)

Key description list:

- To standardize high-level control command input from users, inputs have been encapsulated and abstracted. The concept of "virtual peripherals" is defined for robot control:
    - Virtual joystick (virtual joystick)
    - Virtual keyboard (virtual keyboard)
    - Virtual mouse (virtual mouse)
    - Virtual teleoperation controller (virtual teleoperation)
    - Virtual user (virtual user) — for storing user information
    - Virtual panel (virtual panel) — for more general information input
- When a virtual peripheral is needed, set the corresponding flag to `True` in the `config_xxx.yaml` file used at program startup, for example:
    - `peripheral/use_virtual_joystick`
    - `peripheral/use_virtual_keyboard`
    - `peripheral/use_virtual_mouse`
    - `peripheral/use_virtual_teleoperation`
    - `peripheral/use_virtual_user`
    - `peripheral/use_virtual_panel`
- A task may allow multiple virtual peripherals for control. However, because input data is unique, peripheral inputs will overwrite each other. Users should refer to the priority description for each specific task.
    - Higher-priority peripherals overwrite lower-priority peripheral input data.

| Key                             | Description                      | Type                | Details                          |
|---------------------------------|----------------------------------|---------------------|----------------------------------|
| `virtual_joystick_button_up`    | Virtual joystick up button state    | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_down`  | Virtual joystick down button state  | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_left`  | Virtual joystick left button state  | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_right` | Virtual joystick right button state | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_l1`    | Virtual joystick L1 button state    | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_l2`    | Virtual joystick L2 button state    | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_r1`    | Virtual joystick R1 button state    | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_button_r2`    | Virtual joystick R2 button state    | int              | 0: not pressed, 1: pressed       |
| `virtual_joystick_axis_left`    | Virtual joystick left stick state   | array(float, float) | Stick value range: [-1, 1]   |
| `virtual_joystick_axis_right`   | Virtual joystick right stick state  | array(float, float) | Stick value range: [-1, 1]   |

| Key                          | Description                       | Type | Details                    |
|------------------------------|-----------------------------------|------|----------------------------|
| `virtual_keyboard_key_up`    | Virtual keyboard up key state     | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_down`  | Virtual keyboard down key state   | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_left`  | Virtual keyboard left key state   | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_right` | Virtual keyboard right key state  | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_enter` | Virtual keyboard Enter key state  | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_esc`   | Virtual keyboard ESC key state    | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_f1`    | Virtual keyboard F1 key state     | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_f2`    | Virtual keyboard F2 key state     | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_f3`    | Virtual keyboard F3 key state     | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_f4`    | Virtual keyboard F4 key state     | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_q`     | Virtual keyboard Q key state      | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_w`     | Virtual keyboard W key state      | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_e`     | Virtual keyboard E key state      | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_a`     | Virtual keyboard A key state      | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_s`     | Virtual keyboard S key state      | int  | 0: not pressed, 1: pressed |
| `virtual_keyboard_key_d`     | Virtual keyboard D key state      | int  | 0: not pressed, 1: pressed |

| Key                           | Description                    | Type                | Details                                |
|-------------------------------|--------------------------------|---------------------|----------------------------------------|
| `virtual_mouse_button_left`   | Virtual mouse left button state   | int              | 0: not pressed, 1: pressed             |
| `virtual_mouse_button_right`  | Virtual mouse right button state  | int              | 0: not pressed, 1: pressed             |
| `virtual_mouse_button_middle` | Virtual mouse middle button state | int              | 0: not pressed, 1: pressed             |
| `virtual_mouse_axis`          | Virtual mouse coordinate state    | array(float, float) | Mouse coordinates in [x, y] format |

| Key                                       | Description                                     | Type                                                    | Details                                                    |
|-------------------------------------------|-------------------------------------------------|---------------------------------------------------------|------------------------------------------------------------|
| `virtual_teleoperation_head_pose`         | Virtual teleoperation head pose                 | array(float, float, float)                              | Head pose [roll, pitch, yaw], unit: radians                |
| `virtual_teleoperation_left_handle_pose`  | Virtual teleoperation left controller pose      | array(float, float, float, float, float, float, float)  | Left controller pose [x, y, z, qw, qx, qy, qz]            |
| `virtual_teleoperation_right_handle_pose` | Virtual teleoperation right controller pose     | array(float, float, float, float, float, float, float)  | Right controller pose [x, y, z, qw, qx, qy, qz]           |
| `virtual_teleoperation_button_left`       | Virtual teleoperation left controller button    | int                                                     | 0: not pressed, 1: pressed                                 |
| `virtual_teleoperation_button_right`      | Virtual teleoperation right controller button   | int                                                     | 0: not pressed, 1: pressed                                 |

| Key                                   | Description                      | Type  | Details                          |
|---------------------------------------|----------------------------------|-------|----------------------------------|
| `virtual_user_upper_leg_length_left`  | Left upper leg length            | float | Unit: meters, default: 0.5       |
| `virtual_user_upper_leg_length_right` | Right upper leg length           | float | Unit: meters, default: 0.5       |
| `virtual_user_lower_leg_length_left`  | Left lower leg length            | float | Unit: meters, default: 0.5       |
| `virtual_user_lower_leg_length_right` | Right lower leg length           | float | Unit: meters, default: 0.5       |
| `virtual_user_upper_arm_length_left`  | Left upper arm length            | float | Unit: meters, default: 0.5       |
| `virtual_user_upper_arm_length_right` | Right upper arm length           | float | Unit: meters, default: 0.5       |
| `virtual_user_lower_arm_length_left`  | Left lower arm length            | float | Unit: meters, default: 0.5       |
| `virtual_user_lower_arm_length_right` | Right lower arm length           | float | Unit: meters, default: 0.5       |
| `virtual_user_knee_restriction_left`  | Left knee joint restriction      | float | Unit: radians, default: 0.0      |
| `virtual_user_knee_restriction_right` | Right knee joint restriction     | float | Unit: radians, default: 0.0      |

| Key                              | Description                  | Type  | Details                                           |
|----------------------------------|------------------------------|-------|---------------------------------------------------|
| `virtual_panel_command_param_1`  | Panel command parameter 1    | float | Panel command parameter 1; meaning defined by task |
| `virtual_panel_command_param_2`  | Panel command parameter 2    | float | Panel command parameter 2; meaning defined by task |
| `virtual_panel_command_param_3`  | Panel command parameter 3    | float | Panel command parameter 3; meaning defined by task |
| `virtual_panel_command_param_4`  | Panel command parameter 4    | float | Panel command parameter 4; meaning defined by task |
| `virtual_panel_command_param_5`  | Panel command parameter 5    | float | Panel command parameter 5; meaning defined by task |
| `virtual_panel_command_param_6`  | Panel command parameter 6    | float | Panel command parameter 6; meaning defined by task |
| `virtual_panel_command_param_7`  | Panel command parameter 7    | float | Panel command parameter 7; meaning defined by task |
| `virtual_panel_command_param_8`  | Panel command parameter 8    | float | Panel command parameter 8; meaning defined by task |
| `virtual_panel_command_param_9`  | Panel command parameter 9    | float | Panel command parameter 9; meaning defined by task |
| `virtual_panel_command_switch_1` | Panel command switch 1       | bool  | 0: off, 1: on; meaning defined by task             |
| `virtual_panel_command_switch_2` | Panel command switch 2       | bool  | 0: off, 1: on; meaning defined by task             |
| `virtual_panel_command_switch_3` | Panel command switch 3       | bool  | 0: off, 1: on; meaning defined by task             |
| `virtual_panel_command_switch_4` | Panel command switch 4       | bool  | 0: off, 1: on; meaning defined by task             |
| `virtual_panel_command_switch_5` | Panel command switch 5       | bool  | 0: off, 1: on; meaning defined by task             |
| `virtual_panel_command_picker_1` | Panel command picker 1       | int   | Panel picker 1; meaning defined by task            |
| `virtual_panel_command_picker_2` | Panel command picker 2       | int   | Panel picker 2; meaning defined by task            |
| `virtual_panel_command_picker_3` | Panel command picker 3       | int   | Panel picker 3; meaning defined by task            |
| `virtual_panel_command_start`    | Panel command start flag     | bool  | 0: do not start, 1: start; meaning defined by task |
| `virtual_panel_command_stop`     | Panel command stop flag      | bool  | 0: do not stop, 1: stop; meaning defined by task   |
| `virtual_panel_command_pause`    | Panel command pause flag     | bool  | 0: do not pause, 1: pause; meaning defined by task |

### rehab/client Interface Protocol (Command Information)

> ℹ️ **This interface is not yet open.** The rehab/client command channel is not implemented in the current version. Do not send commands to this Zenoh topic. A real-time write interface for rehabilitation training parameters will be provided here in a future version.
