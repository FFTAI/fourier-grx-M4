---
layout: default
title: User 接口
nav_order: 3.1
parent: 参考指南
has_toc: true
---

# 参考指南 User 接口

* TOC
{:toc}

> ℹ️ **说明**：
>
> 使用 Fourier-GRX-M4 SDK User API 前，请将 `fourier-grx` 配置为 **开发者模式**。
> 关于运行模式的配置，请参见 [运行模式](/fourier-grx-M4/docs/reference/run_type)。

Fourier-GRX User 接口使用 [Zenoh](https://zenoh.io/) 协议与机器人通信，
适用于高层应用开发。

user 接口主要分为以下5类：

- `comm`：通信相关信息
- `robot`：机器人状态信息
- `task`：任务相关信息
- `grx`：fourier-grx 库相关信息，通用机器人相关内容（主要是人形）
- `rehab`：康复机器人相关信息

对应的 zenoh 接口 topic 的 key 格式为：

- key 可以是 ["comm", "robot", "task", "grx", "rehab"]
- `fourier-grx/dynalink_interface/{key}/server` ：机器人主控程序发出的状态信息 **[机器人作为服务器]**
- `fourier-grx/dynalink_interface/{key}/client` ：机器人主控程序接收的指令信息 **[用户机作为客户端]**

---

## 状态信息

### comm/server 接口协议 (状态信息)

key 说明列表：

| key                          | 说明              | 数据类型 | 具体描述                |
|------------------------------|-----------------|------|---------------------|
| `flag_heart_beat`            | 心跳标志            | bool | 1: 机器人已启动           |
| `flag_ethernet_connect_status` | 主机与机器人以太网连接状态 | bool | 0: 未连接，1: 已连接       |

### robot/server 接口协议 (状态信息)

**传感器信息**

| key                                      | 说明          | 数据类型         | 具体描述                                  |
|------------------------------------------|-------------|--------------|---------------------------------------|
| `sensor_imus_quat_value`                 | IMU 四元数     | array(float) | 各 IMU 四元数 [x, y, z, w] 拼接             |
| `sensor_imus_euler_angle_value`          | IMU 欧拉角     | array(float) | 各 IMU 欧拉角 [roll, pitch, yaw]，单位为弧度    |
| `sensor_imus_angular_velocity_value`     | IMU 角速度     | array(float) | 各 IMU 角速度 [x, y, z]，单位为弧度/秒          |
| `sensor_imus_linear_acceleration_value`  | IMU 线性加速度   | array(float) | 各 IMU 线性加速度 [x, y, z]，单位为米/秒²        |

**执行器标志**

| key                        | 说明        | 数据类型        | 具体描述              |
|----------------------------|-----------|-------------|-------------------|
| `flag_actuator_installed`  | 执行器安装状态   | array(bool) | 各执行器是否已安装         |
| `flag_actuator_accessible` | 执行器可访问状态  | array(bool) | 各执行器是否可通信访问       |
| `flag_actuator_enables`    | 执行器使能状态   | array(bool) | 各执行器是否已使能         |
| `flag_actuator_error`      | 执行器错误状态   | array(bool) | 各执行器是否存在错误        |

**执行器测量信息**

| key                               | 说明       | 数据类型         | 具体描述              |
|-----------------------------------|----------|--------------|-------------------|
| `actuator_measured_control_mode`  | 执行器控制模式  | array(int)   | 执行器当前控制模式         |
| `actuator_measured_position`      | 执行器测量位置  | array(float) | 执行器测量位置，单位为弧度或米   |
| `actuator_measured_velocity`      | 执行器测量速度  | array(float) | 执行器测量速度，单位为弧度/秒或米/秒 |
| `actuator_measured_acceleration`  | 执行器测量加速度 | array(float) | 执行器测量加速度，单位为弧度/秒² |
| `actuator_measured_effort`        | 执行器测量力矩  | array(float) | 执行器测量力矩，单位为牛顿米    |
| `actuator_measured_current`       | 执行器测量电流  | array(float) | 执行器测量电流，单位为安培     |

**执行器指令信息**

| key                              | 说明       | 数据类型         | 具体描述              |
|----------------------------------|----------|--------------|-------------------|
| `actuator_output_control_mode`   | 执行器指令控制模式 | array(int)  | 执行器指令控制模式         |
| `actuator_output_position`       | 执行器指令位置  | array(float) | 执行器指令位置，单位为弧度或米   |
| `actuator_output_velocity`       | 执行器指令速度  | array(float) | 执行器指令速度，单位为弧度/秒或米/秒 |
| `actuator_output_acceleration`   | 执行器指令加速度 | array(float) | 执行器指令加速度，单位为弧度/秒² |
| `actuator_output_effort`         | 执行器指令力矩  | array(float) | 执行器指令力矩，单位为牛顿米    |
| `actuator_output_current`        | 执行器指令电流  | array(float) | 执行器指令电流，单位为安培     |

**关节状态字**

| key                       | 说明      | 数据类型       | 具体描述              |
|---------------------------|---------|------------|-------------------|
| `joint_mode_of_operation` | 关节操作模式  | array(int) | 各关节当前操作模式         |
| `joint_control_word`      | 关节控制字   | array(int) | 各关节控制字            |
| `joint_status_word`       | 关节状态字   | array(int) | 各关节状态字            |

**关节应用层信息**

| key                          | 说明        | 数据类型         | 具体描述                       |
|------------------------------|-----------|--------------|----------------------------|
| `joint_application_position` | 关节应用层目标位置 | array(float) | 应用层写入的关节目标位置，单位为弧度或米       |
| `joint_application_velocity` | 关节应用层目标速度 | array(float) | 应用层写入的关节目标速度，单位为弧度/秒或米/秒   |
| `joint_application_effort`   | 关节应用层目标力矩 | array(float) | 应用层写入的关节目标力矩，单位为牛顿米        |

**关节测量信息**

| key                           | 说明       | 数据类型         | 具体描述               |
|-------------------------------|----------|--------------|----------------------|
| `joint_measured_control_mode` | 关节测量控制模式 | array(int)   | 各关节当前控制模式            |
| `joint_measured_position`     | 关节测量位置   | array(float) | 关节测量位置，单位为弧度         |
| `joint_measured_velocity`     | 关节测量速度   | array(float) | 关节测量速度，单位为弧度/秒       |
| `joint_measured_acceleration` | 关节测量加速度  | array(float) | 关节测量加速度，单位为弧度/秒²     |
| `joint_measured_effort`       | 关节测量力矩   | array(float) | 关节测量力矩，单位为牛顿米        |
| `joint_measured_current`      | 关节测量电流   | array(float) | 关节测量电流，单位为安培         |

**关节指令信息**

| key                          | 说明       | 数据类型         | 具体描述               |
|------------------------------|----------|--------------|----------------------|
| `joint_output_control_mode`  | 关节指令控制模式 | array(int)   | 各关节指令控制模式            |
| `joint_output_position`      | 关节指令位置   | array(float) | 关节指令位置，单位为弧度         |
| `joint_output_velocity`      | 关节指令速度   | array(float) | 关节指令速度，单位为弧度/秒       |
| `joint_output_acceleration`  | 关节指令加速度  | array(float) | 关节指令加速度，单位为弧度/秒²     |
| `joint_output_effort`        | 关节指令力矩   | array(float) | 关节指令力矩，单位为牛顿米        |
| `joint_output_current`       | 关节指令电流   | array(float) | 关节指令电流，单位为安培         |

**末端执行器测量信息**

| key                                   | 说明         | 数据类型         | 具体描述            |
|---------------------------------------|------------|--------------|-------------------|
| `end_effector_measured_position`      | 末端执行器测量位置  | array(float) | 末端执行器测量位置，单位为米   |
| `end_effector_measured_velocity`      | 末端执行器测量速度  | array(float) | 末端执行器测量速度，单位为米/秒 |
| `end_effector_measured_acceleration`  | 末端执行器测量加速度 | array(float) | 末端执行器测量加速度，单位为米/秒² |
| `end_effector_measured_effort`        | 末端执行器测量力矩  | array(float) | 末端执行器测量力矩，单位为牛顿米 |

**机器人状态标志**

| key                            | 说明        | 数据类型 | 具体描述              |
|--------------------------------|-----------|------|-------------------|
| `flag_robot_self_check`        | 机器人自检成功标志 | bool | 0: 自检失败，1: 自检成功   |
| `flag_robot_calibration`       | 机器人完成校准标志 | bool | 0: 校准失败，1: 校准成功   |
| `flag_robot_servo_on`          | 机器人伺服使能标志 | bool | 0: 伺服未使能，1: 伺服已使能 |
| `flag_robot_emergent_stop`     | 机器人急停标志   | bool | 0: 未急停，1: 急停      |
| `flag_robot_fault`             | 机器人故障标志   | bool | 0: 无故障，1: 有故障     |
| `flag_robot_error`             | 机器人错误标志   | bool | 0: 无错误，1: 有错误     |
| `flag_robot_pinched`           | 机器人夹持标志   | bool | 0: 未夹持，1: 夹持      |
| `flag_robot_over_load`         | 机器人过载标志   | bool | 0: 未过载，1: 过载      |
| `flag_robot_torque_protection` | 机器人力矩保护标志 | bool | 0: 未触发，1: 触发      |

**机器人基本信息**

| key                | 说明       | 数据类型   | 具体描述          |
|--------------------|----------|--------|---------------|
| `robot_name`       | 机器人名称    | string | 当前机器人型号名称     |
| `robot_work_space` | 机器人工作空间  | int    | 当前机器人工作空间编号   |

### task/server 接口协议 (状态信息)

**任务状态信息**

| key                    | 说明         | 数据类型 | 具体描述                                                                                                                      |
|------------------------|------------|------|---------------------------------------------------------------------------------------------------------------------------|
| `flag_task_start`      | 任务启动标志     | bool | 0: 任务未启动，1: 任务已启动                                                                                                         |
| `flag_task_running`    | 任务运行中标志    | bool | 0: 任务未运行，1: 任务运行中                                                                                                         |
| `flag_task_finish`     | 任务完成标志     | bool | 0: 任务未完成，1: 任务已完成                                                                                                         |
| `flag_task_pause`      | 任务暂停标志     | bool | 0: 任务未暂停，1: 任务已暂停                                                                                                         |
| `robot_task_state`     | 机器人任务状态    | int  | 当前机器人任务状态 (TID 值)，如果设置了 task/client 中的 `flag_task_command_update` 为 True，会更新此值，更新值为 task/client 接口中的 `robot_task_command` |
| `robot_task_state_data` | 机器人任务状态数据 | dict | 当前任务的附加状态数据，内容因任务不同而异                                                                                                     |

**模块状态信息**

| key                       | 说明       | 数据类型 | 具体描述                      |
|---------------------------|----------|------|---------------------------|
| `flag_component_start`    | 模块启动标志   | bool | 0: 模块未启动，1: 模块已启动         |
| `flag_component_in_process` | 模块运行中标志 | bool | 0: 模块未运行，1: 模块运行中         |
| `flag_component_finish`   | 模块完成标志   | bool | 0: 模块未完成，1: 模块已完成         |
| `robot_component_state`   | 机器人模块状态  | int  | 当前机器人模块状态 (MID 值)          |
| `robot_component_state_data` | 机器人模块状态数据 | dict | 当前模块的附加状态数据，内容因模块不同而异  |

### grx/server 接口协议 (状态信息)

key 说明列表：

| key                        | 说明       | 数据类型         | 具体描述                         |
|----------------------------|----------|--------------|------------------------------|
| `fourier_core_version`     | 核心库版本    | string       | 核心库版本号                       |
| `fourier_grx_version`      | GRX库版本   | string       | GRX库版本号                      |
| `robot_error_codes`        | 机器人错误码   | array(int)   | 机器人错误码列表，0: 无错误，其他: 具体错误码     |
| `robot_battery_percentage` | 电池电量百分比  | float        | 电池当前电量，范围 [0.0, 1.0]，1.0 为满电 |
| `robot_charging_level`     | 电池电量等级   | int          | 电量等级，范围 1-3，3 为最高            |
| `robot_charging_state`     | 电池充电状态   | float        | 0.0: 未充电，1.0: 充电中            |

### rehab/server 接口协议 (状态信息)

key 说明列表：

| key                             | 说明       | 数据类型         | 具体描述                                                                                |
|---------------------------------|----------|--------------|--------------------------------------------------------------------------------------|
| `reference_joint_position`      | 关节参考位置   | array(float) | 当前控制周期规划的关节目标位置，单位为弧度。该数组每个控制周期更新，可用于上位机可视化或录制运动轨迹                               |
| `reference_joint_velocity`      | 关节参考速度   | array(float) | 当前控制周期规划的关节目标速度，单位为弧度/秒。与 `reference_joint_position` 同步更新                          |
| `reference_joint_position_max`  | 关节参考最大位置 | array(float) | 整段运动轨迹中各关节的最大目标位置，单位为弧度。可用于上位机显示关节活动范围                                            |
| `reference_joint_position_min`  | 关节参考最小位置 | array(float) | 整段运动轨迹中各关节的最小目标位置，单位为弧度。可用于上位机显示关节活动范围                                            |
| `motion_ratio`                  | 运动进度比例   | float        | 当前任务的运动完成比例，范围 [0, 1]。可用于进度显示或多设备协同同步                                              |

---

## 指令信息

### comm/client 接口协议 (指令信息)

> ℹ️ **该接口暂未开放。** comm/client 通道用于系统级通信指令，当前版本暂无可写字段，仅作为保留接口存在。

### robot/client 接口协议 (指令信息)

key 说明列表：

| key                                  | 说明       | 数据类型 | 具体描述         |
|--------------------------------------|----------|------|--------------|
| `clear_flag_robot_over_load`         | 清除过载标志   | bool | 0: 不清除，1: 清除 |
| `clear_flag_robot_torque_protection` | 清除力矩保护标志 | bool | 0: 不清除，1: 清除 |

### task/client 接口协议 (指令信息)

任务指令发送接口如下，发送指令时要求按照以下流程执行：

- 任务指令发送：
    1. 发送 robot_task_command 和 robot_task_command_data，任务相关信息
    2. 发送 flag_task_command_update 指令更新标志位，确认更新任务指令
- 模块指令发送：
    1. 发送 robot_component_command 和 robot_component_command_data，模块相关信息
    2. 发送 flag_component_command_update 指令更新标志位，确认更新模块指令

key 说明列表：

| key                             | 说明         | 数据类型 | 具体描述            |
|---------------------------------|------------|------|-----------------|
| `flag_task_command_update`      | 任务指令请求更新标志 | bool | 0: 不更新，1: 更新    |
| `robot_task_command`            | 任务指令       | int  | 机器人任务指令 (TID 值) |
| `robot_task_command_data`       | 任务指令数据     | dict | 机器人任务指令数据       |
| `flag_component_command_update` | 模块指令请求更新标志 | bool | 0: 不更新，1: 更新    |
| `robot_component_command`       | 模块指令       | int  | 机器人模块指令 (MID 值) |
| `robot_component_command_data`  | 模块指令数据     | dict | 机器人模块指令数据       |

### grx/client 接口协议 (指令信息)

key 说明列表：

- 为规范用户的高层控制指令传入，对输入参数进行了封装和抽象。主要定义了“虚拟外设”的概念来进行机器人的控制。
    - 虚拟摇杆 (virtual joystick)
    - 虚拟键盘 (virtual keyboard)
    - 虚拟鼠标 (virtual mouse)
    - 虚拟遥操作手柄 (virtual teleoperation)
    - 虚拟用户 (virtual user) 用于存储用户信息
    - 虚拟面板 (virtual panel) 用于更通用的信息输入
- 在需要使用到对应虚拟设备时，需要在主程序启动时调用的 `config_xxx.yaml` 文件中，设置虚拟外设为 `True`，如：
    - `peripheral/use_virtual_joystick`
    - `peripheral/use_virtual_keyboard`
    - `peripheral/use_virtual_mouse`
    - `peripheral/use_virtual_teleoperation`
    - `peripheral/use_virtual_user`
    - `peripheral/use_virtual_panel`
- 一个任务可能允许使用多个虚拟外设进行控制，但是由于输入数据的唯一性，外设之间输入数据会互相覆盖，因此，建议用户参看具体任务中关于外设数据优先级的说明。
    - 优先级高的外设会覆盖优先级低的外设输入数据。

| key                             | 说明           | 数据类型            | 具体描述             |
|---------------------------------|--------------|-----------------|------------------|
| `virtual_joystick_button_up`    | 虚拟手柄上按钮状态    | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_down`  | 虚拟手柄下按钮状态    | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_left`  | 虚拟手柄左按钮状态    | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_right` | 虚拟手柄右按钮状态    | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_l1`    | 虚拟手柄 L1 按钮状态 | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_l2`    | 虚拟手柄 L2 按钮状态 | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_r1`    | 虚拟手柄 R1 按钮状态 | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_button_r2`    | 虚拟手柄 R2 按钮状态 | int             | 0: 未按下，1: 按下     |
| `virtual_joystick_axis_left`    | 虚拟手柄左摇杆状态    | array(float, float) | 摇杆状态值范围为 [-1, 1] |
| `virtual_joystick_axis_right`   | 虚拟手柄右摇杆状态    | array(float, float) | 摇杆状态值范围为 [-1, 1] |

| key                          | 说明           | 数据类型 | 具体描述         |
|------------------------------|--------------|------|--------------|
| `virtual_keyboard_key_up`    | 虚拟键盘上键状态     | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_down`  | 虚拟键盘下键状态     | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_left`  | 虚拟键盘左键状态     | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_right` | 虚拟键盘右键状态     | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_enter` | 虚拟键盘回车键状态    | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_esc`   | 虚拟键盘 ESC 键状态 | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_f1`    | 虚拟键盘 F1 键状态  | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_f2`    | 虚拟键盘 F2 键状态  | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_f3`    | 虚拟键盘 F3 键状态  | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_f4`    | 虚拟键盘 F4 键状态  | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_q`     | 虚拟键盘 Q 键状态   | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_w`     | 虚拟键盘 W 键状态   | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_e`     | 虚拟键盘 E 键状态   | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_a`     | 虚拟键盘 A 键状态   | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_s`     | 虚拟键盘 S 键状态   | int  | 0: 未按下，1: 按下 |
| `virtual_keyboard_key_d`     | 虚拟键盘 D 键状态   | int  | 0: 未按下，1: 按下 |

| key                           | 说明       | 数据类型            | 具体描述                   |
|-------------------------------|----------|-----------------|------------------------|
| `virtual_mouse_button_left`   | 虚拟鼠标左键状态 | int             | 0: 未按下，1: 按下           |
| `virtual_mouse_button_right`  | 虚拟鼠标右键状态 | int             | 0: 未按下，1: 按下           |
| `virtual_mouse_button_middle` | 虚拟鼠标中键状态 | int             | 0: 未按下，1: 按下           |
| `virtual_mouse_axis`          | 虚拟鼠标坐标状态 | array(float, float) | 鼠标坐标值，格式为 [x, y] |

| key                                       | 说明             | 数据类型                                                       | 具体描述         |
|-------------------------------------------|----------------|------------------------------------------------------------|--------------|
| `virtual_teleoperation_head_pose`         | 虚拟遥操作头部姿态      | array(float, float, float)                                 | 头部姿态 [roll, pitch, yaw]，单位为弧度 |
| `virtual_teleoperation_left_handle_pose`  | 虚拟遥操作左手柄姿态     | array(float, float, float, float, float, float, float)     | 左手柄位姿 [x, y, z, qw, qx, qy, qz] |
| `virtual_teleoperation_right_handle_pose` | 虚拟遥操作右手柄姿态     | array(float, float, float, float, float, float, float)     | 右手柄位姿 [x, y, z, qw, qx, qy, qz] |
| `virtual_teleoperation_button_left`       | 虚拟遥操作左手柄按钮状态   | int                                                        | 0: 未按下，1: 按下 |
| `virtual_teleoperation_button_right`      | 虚拟遥操作右手柄按钮状态   | int                                                        | 0: 未按下，1: 按下 |

| key                                   | 说明     | 数据类型  | 具体描述           |
|---------------------------------------|--------|-------|----------------|
| `virtual_user_upper_leg_length_left`  | 左上肢长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_upper_leg_length_right` | 右上肢长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_lower_leg_length_left`  | 左下肢长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_lower_leg_length_right` | 右下肢长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_upper_arm_length_left`  | 左上臂长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_upper_arm_length_right` | 右上臂长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_lower_arm_length_left`  | 左下臂长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_lower_arm_length_right` | 右下臂长度  | float | 单位为米，默认值为 0.5  |
| `virtual_user_knee_restriction_left`  | 左膝关节限制 | float | 单位为弧度，默认值为 0.0 |
| `virtual_user_knee_restriction_right` | 右膝关节限制 | float | 单位为弧度，默认值为 0.0 |

| key                              | 说明       | 数据类型  | 具体描述                   |
|----------------------------------|----------|-------|------------------------|
| `virtual_panel_command_param_1`  | 面板命令参数1  | float | 面板命令参数1，具体含义由任务决定      |
| `virtual_panel_command_param_2`  | 面板命令参数2  | float | 面板命令参数2，具体含义由任务决定      |
| `virtual_panel_command_param_3`  | 面板命令参数3  | float | 面板命令参数3，具体含义由任务决定      |
| `virtual_panel_command_param_4`  | 面板命令参数4  | float | 面板命令参数4，具体含义由任务决定      |
| `virtual_panel_command_param_5`  | 面板命令参数5  | float | 面板命令参数5，具体含义由任务决定      |
| `virtual_panel_command_param_6`  | 面板命令参数6  | float | 面板命令参数6，具体含义由任务决定      |
| `virtual_panel_command_param_7`  | 面板命令参数7  | float | 面板命令参数7，具体含义由任务决定      |
| `virtual_panel_command_param_8`  | 面板命令参数8  | float | 面板命令参数8，具体含义由任务决定      |
| `virtual_panel_command_param_9`  | 面板命令参数9  | float | 面板命令参数9，具体含义由任务决定      |
| `virtual_panel_command_switch_1` | 面板命令开关1  | bool  | 0: 不开，1: 开，具体含义由任务决定   |
| `virtual_panel_command_switch_2` | 面板命令开关2  | bool  | 0: 不开，1: 开，具体含义由任务决定   |
| `virtual_panel_command_switch_3` | 面板命令开关3  | bool  | 0: 不开，1: 开，具体含义由任务决定   |
| `virtual_panel_command_switch_4` | 面板命令开关4  | bool  | 0: 不开，1: 开，具体含义由任务决定   |
| `virtual_panel_command_switch_5` | 面板命令开关5  | bool  | 0: 不开，1: 开，具体含义由任务决定   |
| `virtual_panel_command_picker_1` | 面板命令选择器1 | int   | 面板选择器1，具体含义由任务决定       |
| `virtual_panel_command_picker_2` | 面板命令选择器2 | int   | 面板选择器2，具体含义由任务决定       |
| `virtual_panel_command_picker_3` | 面板命令选择器3 | int   | 面板选择器3，具体含义由任务决定       |
| `virtual_panel_command_start`    | 面板命令开始标志 | bool  | 0: 不开始，1: 开始，具体含义由任务决定 |
| `virtual_panel_command_stop`     | 面板命令停止标志 | bool  | 0: 不停止，1: 停止，具体含义由任务决定 |
| `virtual_panel_command_pause`    | 面板命令暂停标志 | bool  | 0: 不暂停，1: 暂停，具体含义由任务决定 |

### rehab/client 接口协议 (指令信息)

> ℹ️ **该接口暂未开放。** 当前版本 rehab/client 指令通道尚未实现，请勿向该 Zenoh topic 发送指令。后续版本将在此处提供康复训练参数的实时写入接口。
