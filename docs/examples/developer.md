---
layout: default
title: Developer 接口
nav_order: 2.2
parent: 示例代码
toc: true          # 启用目录
toc_min_header: 2  # 最小显示标题层级（如 H2）
toc_max_header: 3  # 最大显示标题层级（如 H3）
---

# Developer 接口

Fourier-GRX Developer 接口是针对开发者底层开发提供的二次开发接口，
直接调用底层硬件接口，
适用于底层开发。

为确保实时性，这些示例必须在机器人主控电脑上运行。

## 运行方法

1. 在机器人主控电脑上启动示例代码，直接进行控制：
    ```bash
    # 激活 conda 环境
    conda activate fourier-grx
    
    # 运行具体机型的示例程序，配置文件需要根据具体机型进行修改，使用带 "_developer.yaml" 后缀的配置文件
    python $HOME/Wiki-GRx-Deploy/developer/demo_{示例名称}.py --config=$HOME/fourier-grx/config/{具体机型}/config_{具体机型}_developer.yaml
    ```

### 注意事项

1. 开发者接口需要更深入的机器人知识
2. 建议先熟悉用户接口再使用开发者接口
3. 请注意备份重要的配置文件
4. 调试时建议在安全环境下进行

## 接口示例

### 系统控制示例

| 示例名称  | 说明          | 代码路径                             |
|-------|-------------|----------------------------------|
| 执行器使能 | 使能机器人执行器    | `developer/demo_servo_on.py`     |
| 执行器失能 | 失能机器人执行器    | `developer/demo_servo_off.py`    |
| 执行器重启 | 重启机器人执行器    | `developer/demo_servo_reboot.py` |
| 状态监控  | 打印机器人状态信息   | `developer/demo_print_state.py`  |
| 参数配置  | 设置关节 PID 参数 | `developer/demo_set_pid.py`      |
| 零位设置  | 设置机器人零位     | `developer/demo_set_home.py`     |

### 运动控制示例

| 示例名称 | 说明           | 代码路径                           |
|------|--------------|--------------------------------|
| 移动关节 | 移动机器人关节到指定角度 | `developer/demo_move_joint.py` |