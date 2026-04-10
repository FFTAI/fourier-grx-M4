---
layout: default
title: Usage Guide
nav_order: 5
has_toc: true
nav_exclude: true
---

# Usage Guide

* TOC
{:toc}

This document describes common operational workflows and important notes when using the Fourier-GRX-M4 SDK.

## Joint Zero Calibration

> ℹ️ **Note**
>
> Built-in calibration tasks can be selected and executed with a gamepad in **Debug Mode**, or by calling the corresponding task interface in **Developer Mode**.

### Pre-Startup Checklist

1. **Hardware Check**
    - ✅ Robot power is connected
    - ✅ Gamepad is properly connected
    - ✅ Network connection is normal
    - ✅ Locking pins are inserted into the robot joint positioning holes

2. **Software Preparation**
    - ✅ SDK is correctly installed

### Starting the Program

```bash
# Start the Fourier-GRX program
fourier-grx start
```

### Calibration Workflow

1. **Steps**
    - Use the gamepad `L1` button to select the **calibration task**
    - Use the gamepad `L2` button to confirm execution
    - Observe the terminal output

### M4L Power-On Calibration Sequence

> ⚠️ **M4L series robots must perform calibration in the following order after every power-on. Otherwise, joint position data will be invalid.**
>
> Rotary joints (hip/knee) save their zero point via absolute encoders and retain it across power cycles. Prismatic joints (leg length) use incremental encoders and **must be recalibrated after every power-on**.

| Step | Task Name                        | TID  | Description                                                                                      |
|------|----------------------------------|------|--------------------------------------------------------------------------------------------------|
| 1    | Auto Calibrate (Prismatic Joints) | 4210 | Prismatic joints automatically find their travel limits and reset to zero; leg length will contract to minimum then reset |
| 2    | Auto Calibrate (Rotary Joints)    | 4120 | Rotary joint boundary detection + auto zero-setting, consists of 3 sub-steps, takes approximately 60 s |

Detailed calibration task descriptions:

| Robot Model | Task                                  | Task ID | Description                      |
|-------------|---------------------------------------|---------|----------------------------------|
| M4L         | Auto Calibrate (Prismatic Joints)     | 4210    | Must be performed after every power-on |
| M4L         | Auto Calibrate (Rotary Joints)        | 4120    | Perform as needed after power-on |
| M4L         | Manual Set Home (Prismatic Joints)    | 4203    | Use after manually aligning pins |
| M4L         | Manual Set Home (Rotary Joints)       | 4103    | Use after manually aligning pins |

2. **Calibration Verification**
    - Success indicators:
        - Terminal displays an **all-zeros array**
        - All joint positions are correct
    - Failure indicators:
        - Array contains values greater than 1 (indicating joint deviation exceeding 1°)
        - Joint positions are abnormal

3. **Exiting the Program**

   Press `Ctrl+C` twice to exit the program.

### Important Notes

1. **Pin Management**
    - Manual calibration (TID=4103/4203): insert pins into the robot joint positioning holes first
    - Automatic calibration (TID=4120/4210): no pins needed during execution
    - After calibration, all pins must be removed before executing any motion task
    - If a pin is found still inserted, recalibration is required

2. **Safety Precautions**
    - During auto calibration (TID=4210), the leg-length mechanism will move automatically — maintain a safe distance
    - During auto calibration (TID=4120), rotary joints will slowly move to their mechanical limits — ensure joints are unobstructed
    - Keep the emergency stop button within reach, ready to stop the robot at any time

3. **Troubleshooting**
    - Auto calibration timed out without completing: check if the motor driver is reporting an alarm; execute Clear Fault (TID=34) and retry
    - Calibration completed but motion is abnormal: re-execute the calibration task for the affected direction
    - Multiple failures: contact technical support and save the terminal log for analysis

## Auto-Start on Boot

fourier-grx provides a boot auto-start configuration feature. Use the following commands to configure it:

```bash
fourier-grx enable_service  # Enable auto-start on boot
fourier-grx disable_service # Disable auto-start on boot
```

If the robot is configured for gamepad remote control, ensure the gamepad is connected to the main controller's USB port and is awake before powering on when auto-start is enabled.

## Enabling/Disabling Program Run Logging

fourier-grx includes a program run logging feature that is enabled by default and provides no built-in option to disable it.

If you absolutely need to disable run logging, modify the following section in the startup script `run.sh`:

> ⚠️ **Note**:
>
> Disabling run logging will prevent program activity from being recorded, which may hinder subsequent debugging and troubleshooting.

```bash
# Original script content
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee $FOURIER_GRX_HOME/log/${log_file_name}

# Modified script content
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee /dev/null
```

## Enabling/Disabling Robot Data Logging

fourier-grx provides a data logging feature that is **disabled by default** to reduce the impact on system performance.

To enable data logging, manually modify the **configuration file** as follows:

1. Create a startup configuration file for the robot:
    - Open the folder `~/fourier-grx/config/m4l` and find the currently used configuration file, for example `config_M4L_T1_debug.yaml`.
    - Copy it and name the copy `config_M4L_T1_record.yaml`.

2. Edit the configuration file:
    - Open `config_M4L_T1_record.yaml`.
    - Add the following content to the file:
        - This configuration enables data recording when `fourier-grx` is started with this config file, and saves the recorded data to the specified path.

   ```yaml
   record:
      enable: true
      path: "~/fourier-grx/record/m4l"
   ```

3. Edit the startup script:
    - Open the `~/fourier-grx` folder and find the `run.sh` file.
    - Locate the `run_type` field and change its value to `record`:

   ```bash
   run_type="record"
   ```

   > ⚠️ **Note**:
   >
   > To restore the robot to its normal operating mode later, use the `fourier-grx config` command to update the configuration, or manually change the `run_type` field in `run.sh` back to its original value.

4. Start the robot:
    - The robot will now enable data recording on startup and save the recorded data to the specified path.

    ```bash
    # Run the following command in Terminal 1
    fourier-grx start
    ```

5. Data Analysis:
    - Data is saved as comma-separated `.log` files, which can be analyzed with Excel or other data analysis tools.
    - When importing into Excel, be sure to select the correct delimiter (comma) and encoding (UTF-8).
    - The data files contain timestamps, IMU data, joint angles, velocities, and more for subsequent analysis:
        - `Timestamp`: Timestamp
        - `imu_quat_{i}`: IMU quaternion component i
        - `imu_euler_{i}`: IMU Euler angle component i
        - `imu_ang_vel_{i}`: IMU angular velocity component i
        - `imu_lin_acc_{i}`: IMU linear acceleration component i
        - `jm_pos_{i}`: Measured position of joint i
        - `jm_vel_{i}`: Measured velocity of joint i
        - `jm_tor_{i}`: Measured torque of joint i
        - `jm_cur_{i}`: Measured current of joint i
        - `jt_pos_{i}`: Target position of joint i
        - `jt_vel_{i}`: Target velocity of joint i
        - `jt_tor_{i}`: Target torque of joint i
        - For joint sequence reference, see the [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence) documentation.

> **Note**:
>
> To disable data recording, set `record.enable` to `false` in the configuration file, or remove the `record` field entirely.
