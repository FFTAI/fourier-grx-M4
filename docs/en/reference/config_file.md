---
layout: default
title: Configuration File
nav_order: 3.5
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Configuration File

* TOC
{:toc}

The Configuration File is used in the Fourier-GRX SDK to configure the startup parameters for the robot. Users can customize the robot behavior by modifying this file.

## Configuration File Path

When starting `fourier-grx`, the path to the Configuration File must be specified via the `--config` parameter.
When using `fourier-grx start` to launch the robot, the specific configuration file in use can be found in `~/fourier-grx/run.sh`.

Which configuration file is used depends on the `robot_type`, `robot_version`, and `run_type` fields in `run.sh`.
These fields can be changed either via the `fourier-grx config` command line tool or by editing `run.sh` directly.

For example, if you want to start the robot with a custom configuration file `config_M4L_T1_custom.yaml`, set the `run_type` field in `run.sh` to `custom`:

```bash
robot_type="M4L"
robot_version="T1"

run_type="custom"

# When starting the robot with `fourier-grx start`, ~/fourier-grx/config/m4l/config_M4L_T1_custom.yaml will be used as the configuration file.
```

## Configuration File Contents

The Configuration File is a YAML-formatted file that contains various robot configuration parameters. The following sections describe the available options.

### Logging

| Parameter  | Description                                                                              | Type    | Default  | Options                                          | User-editable |
|------------|------------------------------------------------------------------------------------------|---------|----------|--------------------------------------------------|---------------|
| log_config | Whether to print startup configuration information                                        | boolean | false    | true, false                                      | Yes           |
| log_level  | Log level                                                                                 | string  | "none"   | "none", "trace", "debug", "warning", "error"     | Yes           |
| log_file   | Log file storage path; applies only to content explicitly directed to the log file        | string  | ""       | "filename", null                                 | Yes           |

### Control System

| Parameter        | Description              | Type    | Default   | Options            | User-editable |
|------------------|--------------------------|---------|-----------|--------------------|---------------|
| device_connected | Whether a device is connected | boolean | true  | true, false        | Yes           |
| hardware_type    | Hardware type            | string  | "X64"     |                    | No            |
| system           | System type              | string  | "LINUX"   |                    | No            |
| mode             | Run mode                 | string  | "debug"   | "debug", "release" | No            |

### Debug

| Parameter                                       | Description                                                    | Type    | Default | Options     | User-editable |
|-------------------------------------------------|----------------------------------------------------------------|---------|---------|-------------|---------------|
| debug: print_imu_state                          | Whether to print raw IMU state information                     | boolean | false   | true, false | Yes           |
| debug: print_joint_position_state               | Whether to print raw joint position state information          | boolean | false   | true, false | Yes           |
| debug: print_joint_velocity_state               | Whether to print raw joint velocity state information          | boolean | false   | true, false | Yes           |
| debug: print_joint_kinetic_state                | Whether to print raw joint torque state information            | boolean | false   | true, false | Yes           |
| debug: print_joint_current_state                | Whether to print raw joint current state information           | boolean | false   | true, false | Yes           |
| debug: print_imu_urdf_state                     | Whether to print IMU pose state corresponding to the URDF file | boolean | false   | true, false | Yes           |
| debug: print_joint_urdf_position_state          | Whether to print joint position state corresponding to the URDF file | boolean | false | true, false | Yes        |
| debug: print_peripheral_virtual_joystick        | Whether to print virtual joystick peripheral state information | boolean | false   | true, false | Yes           |
| debug: print_peripheral_virtual_teleoperation   | Whether to print virtual teleoperation peripheral state information | boolean | false | true, false | Yes         |

### Sub-module Features

| Parameter             | Description                                                                               | Type    | Default | Options     | User-editable                          |
|-----------------------|-------------------------------------------------------------------------------------------|---------|---------|-------------|----------------------------------------|
| dynalink: enable      | Whether to enable the dynamic link data transfer feature                                  | boolean | false   | true, false | Yes                                    |
| sync: enable          | Whether to enable data synchronization (requires dynalink:enable=true)                    | boolean | false   | true, false | No (not yet available)                 |
| rerun: enable         | Whether to enable rerun plotting (requires dynalink:enable=true)                          | boolean | false   | true, false | Yes                                    |
| streamlit: enable     | Whether to enable streamlit plotting (requires dynalink:enable=true)                      | boolean | false   | true, false | No (not yet available)                 |
| comm: enable          | Whether to enable legacy communication adapter (requires dynalink:enable=true)            | boolean | false   | true, false | No (not yet available)                 |
| teleoperation: enable | Whether to enable teleoperation (requires dynalink:enable=true)                           | boolean | false   | true, false | Yes (contact technical support to use) |

### Resource Files

| Parameter      | Description                                                                                                          | Type    | Default                          | Options                | User-editable         |
|----------------|----------------------------------------------------------------------------------------------------------------------|---------|----------------------------------|------------------------|-----------------------|
| resource: path | Resource Files path                                                                                                  | string  | "~/fourier-grx/resource/m4l"    | "path/to/resource"     | Yes                   |
| zenoh: path    | Zenoh configuration file path                                                                                        | string  | "~/fourier-grx/resource/zenoh"  | "path/to/zenoh"        | No (not yet available)|
| record: enable | Whether to enable data logging (records joint positions, velocities, etc. for debugging; requires dynalink:enable=true) | boolean | false                          | true, false            | Yes                   |
| record: path   | Data log file path                                                                                                   | string  | "~/fourier-grx/record/m4l"      | "path/to/record_file"  | Yes                   |

### Peripherals

| Parameter                               | Description                       | Type    | Default    | Options                  | User-editable |
|-----------------------------------------|-----------------------------------|---------|------------|--------------------------|---------------|
| peripheral: use_joystick                | Whether to use joystick control   | boolean | false      | true, false              | Yes           |
| peripheral: joystick_type               | Joystick type                     | string  | "XBOX"     | "XBOX", "PS4", "PS5"     | Yes           |
| peripheral: use_keyboard                | Whether to use keyboard control   | boolean | false      | true, false              | Yes           |
| peripheral: keyboard_type               | Keyboard type                     | string  | "NORMAL"   | "NORMAL"                 | Yes           |
| peripheral: use_virtual_joystick        | Whether to use virtual joystick   | boolean | false      | true, false              | Yes           |
| peripheral: use_virtual_teleoperation   | Whether to use virtual teleoperation | boolean | false   | true, false              | Yes           |

### Robot

| Parameter             | Description       | Type   | Default   | Options                                                                 | User-editable |
|-----------------------|-------------------|--------|-----------|-------------------------------------------------------------------------|---------------|
| robot: name           | Robot name        | string | "M4LT1"   | "M4L" \| "M4LP1" \| "M4LT1" \| "M4LT2" \| "M4LZenoh"                 | No            |

> ℹ️ **Robot Model Notes**
>
> - **M4LT2**: Latest model, equipped with **2.5th-generation FSA actuators**.
> - **M4LT1**: Equipped with **2.0th-generation FSA actuators**.
> - **M4LP1**: Equipped with older **1.0th-generation FSA actuators**, adapted to the 2.0th-generation interface via software upgrade.

| Parameter                   | Description               | Type   | Default | Options         | User-editable |
|-----------------------------|---------------------------|--------|---------|-----------------|---------------|
| robot: backend              | Robot communication backend type | string | "Real" | "Real"      | No            |
| robot: control_period       | Control period            | float  | 0.02    | Unit: seconds   | No            |
| robot: communication_period | Communication period      | float  | 0.02    | Unit: seconds   | No            |

### Sensors

> ℹ️ The current version of the M4L series robots does not integrate external sensor configuration items such as IMU. Sensor data (e.g., battery status) is obtained via the IO board; see [IO Board](#io-board) for related configuration.

### Actuators

| Parameter              | Description                     | Type           | Default      | Options     | User-editable       |
|------------------------|---------------------------------|----------------|--------------|-------------|---------------------|
| actuator: comm_enable  | Whether to enable actuator communication | array(boolean) | [true, ...] | true, false | Yes (edit with care)|

| Parameter        | Description      | Type   | Default      | Options | User-editable |
|------------------|------------------|--------|--------------|---------|---------------|
| fi_fsa: version  | FSA library version | string | "v2_async" |         | No            |

### IO Board

The IO board (IOBoard) reads the robot's battery status and emergency stop button signal. Both M4LP1 and M4LT1 are equipped with an IO board.

| Parameter                          | Description                 | Type   | Default      | Options | User-editable |
|------------------------------------|-----------------------------|--------|--------------|---------|---------------|
| fi_ioboard: version                | IOBoard library version     | string | "v1_async"   |         | No            |
| fi_ioboard: data_upload_frequency  | IOBoard data upload frequency | int  | 1            | Hz      | No            |

| Debug Parameter                | Description                         | Type    | Default | Options     | User-editable |
|--------------------------------|-------------------------------------|---------|---------|-------------|---------------|
| debug: print_ioboard_state     | Whether to print raw IOBoard state  | boolean | false   | true, false | Yes           |
