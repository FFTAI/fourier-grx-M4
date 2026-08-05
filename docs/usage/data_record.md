---
layout: default
title: 机器人数据记录
nav_order: 5.4
parent: 常用操作
has_toc: true
---

# 机器人数据记录

* TOC
{:toc}

机器人数据记录（关节位置/速度/力矩、IMU 等）默认**关闭**，启用步骤如下：

**第一步：创建记录专用配置文件**

复制当前配置文件并命名为 `config_M4L_T1_record.yaml`，在文件末尾添加：

```yaml
record:
  enable: true
  path: "~/fourier-grx/record/m4l"
```

**第二步：切换启动模式**

打开 `~/fourier-grx/run.sh`，将 `run_type` 改为 `record`：

```bash
run_type="record"
```

**第三步：启动**

```bash
fourier-grx start
```

> ℹ️ 恢复正常模式：将 `run_type` 改回原值，或通过 `fourier-grx config` 切换配置文件。

## 数据格式说明

记录文件为逗号分隔的 `.log` 文件（UTF-8 编码），可用 Excel 或其他工具分析。

| 字段 | 含义 |
|------|------|
| `Timestamp` | 时间戳 |
| `imu_quat_{i}` | IMU 四元数分量 i |
| `imu_euler_{i}` | IMU 欧拉角分量 i |
| `imu_ang_vel_{i}` | IMU 角速度分量 i |
| `imu_lin_acc_{i}` | IMU 线加速度分量 i |
| `jm_pos_{i}` | 关节 i 测量位置 |
| `jm_vel_{i}` | 关节 i 测量速度 |
| `jm_tor_{i}` | 关节 i 测量力矩 |
| `jm_cur_{i}` | 关节 i 测量电流 |
| `jt_pos_{i}` | 关节 i 目标位置 |
| `jt_vel_{i}` | 关节 i 目标速度 |
| `jt_tor_{i}` | 关节 i 目标力矩 |

关节索引说明参见 [关节序列](/fourier-grx-M4/docs/reference/joint_sequence) 文档。
