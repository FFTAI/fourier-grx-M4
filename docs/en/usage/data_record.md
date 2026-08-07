---
layout: default
title: Robot Data Recording
nav_order: 5.4
parent: "Usage Guide"
has_toc: true
nav_exclude: true
---

# Robot Data Recording

* TOC
{:toc}

Robot data recording (joint positions, velocities, torques, IMU, etc.) is **disabled by default**. To enable it:

**Step 1: Create a recording configuration file**

Copy your current config file and name it `config_M4L_T1_record.yaml`. Add the following at the end of the file:

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

## Data Format Reference

Recorded files are comma-separated `.log` files (UTF-8 encoding) that can be analyzed with Excel or other tools.

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
