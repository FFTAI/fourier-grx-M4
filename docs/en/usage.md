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

## Quick Reference

| Category | Operation | Description |
|----------|-----------|-------------|
| 🔧 Calibration & Startup | [Joint Zero Calibration](#joint-zero-calibration) | Required calibration sequence after every M4L power-on |
| 🔧 Calibration & Startup | [Auto-Start on Boot](#auto-start-on-boot) | Configure fourier-grx to start automatically with the system |
| 📋 Logging & Data | [Program Run Logging](#enablingdisabling-program-run-logging) | Control terminal log output from fourier-grx |
| 📋 Logging & Data | [Robot Data Recording](#enablingdisabling-robot-data-recording) | Enable CSV recording of joint/IMU data |

---

## 🔧 Calibration & Startup

### Joint Zero Calibration

> ℹ️ **Note**: Built-in calibration tasks can be selected and executed with a gamepad in **Debug Mode**, or by calling the corresponding task interface in **Developer Mode**.

#### Pre-Startup Checklist

**Hardware**

- ✅ Robot power is connected
- ✅ Gamepad is properly connected
- ✅ Network connection is normal
- ✅ Locking pins are inserted into the joint positioning holes (for manual calibration)

**Software**

- ✅ SDK is correctly installed and `fourier-grx start` runs successfully

#### M4L Power-On Calibration Sequence

> ⚠️ **M4L series robots must perform calibration in the following order after every power-on. Otherwise, joint position data will be invalid.**
>
> - Rotary joints (hip/knee) use absolute encoders — zero point is retained across power cycles
> - Prismatic joints (leg length) use incremental encoders — **must be recalibrated after every power-on**

| Step | Task Name | TID | Description |
|------|-----------|-----|-------------|
| 1 | Auto Calibrate (Prismatic Joints) | 4210 | Leg length contracts to minimum then resets to zero; takes ~20 s |
| 2 | Auto Calibrate (Rotary Joints) | 4120 | Boundary detection → power-off drop → zero-point write; takes ~60 s |

#### Calibration Task Reference

| Robot Model | Task | TID | Notes |
|-------------|------|-----|-------|
| M4L | Auto Calibrate (Prismatic Joints) | 4210 | Required after every power-on |
| M4L | Auto Calibrate (Rotary Joints) | 4120 | Perform as needed after power-on |
| M4L | Manual Set Home (Prismatic Joints) | 4203 | Use after manually aligning pins |
| M4L | Manual Set Home (Rotary Joints) | 4103 | Use after manually aligning pins |

#### Calibration Verification

After calibration, the terminal prints a joint deviation array:

- ✅ **Success**: all values near 0 (deviation < 1°)
- ❌ **Failure**: any value greater than 1 — re-run the calibration task for the affected joint

Press `Ctrl+C` twice to exit the program.

#### Important Notes

**Pin Management**

- Manual calibration (TID 4103 / 4203): insert pins before execution
- Automatic calibration (TID 4120 / 4210): no pins required
- After calibration, **remove all pins** before running any motion task

**Safety**

- TID 4210: the leg-length mechanism moves automatically — maintain a safe distance
- TID 4120: rotary joints slowly travel to their mechanical limits — ensure joints are unobstructed
- Keep the emergency stop button within reach at all times

**Troubleshooting**

- Auto calibration timed out: check if the motor driver is reporting an alarm; execute Clear Fault (TID 34) and retry
- Calibration succeeded but motion is abnormal: re-run the calibration task for the affected direction
- Repeated failures: contact technical support and save the terminal log

---

### Auto-Start on Boot

```bash
fourier-grx enable_service   # Enable auto-start on boot
fourier-grx disable_service  # Disable auto-start on boot
```

> ℹ️ If the robot is configured for gamepad control, ensure the gamepad is connected to the main controller's USB port and awake before powering on.

---

## 📋 Logging & Data

### Enabling/Disabling Program Run Logging

Program run logging is **enabled by default** and writes to `~/fourier-grx/log/`.

To disable it, modify the startup script `run.sh`:

> ⚠️ Disabling run logging will prevent program activity from being recorded, which may hinder debugging and troubleshooting.

```bash
# Original (logging enabled)
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee $FOURIER_GRX_HOME/log/${log_file_name}

# Modified (logging disabled)
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee /dev/null
```

---

### Enabling/Disabling Robot Data Recording

Robot data recording (joint positions, velocities, torques, IMU, etc.) is **disabled by default**. To enable it:

**Step 1: Create a recording configuration file**

Copy your current config file (e.g. `config_M4L_T1_debug.yaml`) and name it `config_M4L_T1_record.yaml`. Add the following at the end:

```yaml
record:
  enable: true
  path: "~/fourier-grx/record/m4l"
```

**Step 2: Switch the startup mode**

Open `~/fourier-grx/run.sh` and set `run_type` to `record`:

```bash
run_type="record"
```

**Step 3: Start**

```bash
fourier-grx start
```

> ℹ️ To restore normal mode: change `run_type` back to its original value, or use `fourier-grx config` to switch the config file.

#### Data Format Reference

Files are comma-separated `.log` files (UTF-8 encoding), compatible with Excel or any data analysis tool.

| Field | Description |
|-------|-------------|
| `Timestamp` | Timestamp |
| `imu_quat_{i}` | IMU quaternion component i |
| `imu_euler_{i}` | IMU Euler angle component i |
| `imu_ang_vel_{i}` | IMU angular velocity component i |
| `imu_lin_acc_{i}` | IMU linear acceleration component i |
| `jm_pos_{i}` | Measured position of joint i |
| `jm_vel_{i}` | Measured velocity of joint i |
| `jm_tor_{i}` | Measured torque of joint i |
| `jm_cur_{i}` | Measured current of joint i |
| `jt_pos_{i}` | Target position of joint i |
| `jt_vel_{i}` | Target velocity of joint i |
| `jt_tor_{i}` | Target torque of joint i |

For joint index mapping, see the [Joint Sequence](/fourier-grx-M4/docs/en/reference/joint_sequence) documentation.
