---
layout: default
title: 示例代码
nav_order: 2
has_toc: true
---

# 示例代码

* TOC
{:toc}

本文档提供了丰富的示例代码，帮助您快速掌握 Fourier-GRX-M4 SDK 的使用方法。

- M4 系列机器人的示例代码位于 [Github Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy.git) 的 `FourierM4` 分支中。

示例代码包含用户接口（User API）和开发者接口（Developer API）两类。

## 示例程序下载

可以通过 git 同步机器人的二次开发接口示例程序，同步命令为：

### M4 系列机器人

```bash
# 在机器人主控电脑 $HOME 目录下执行
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4
cd $HOME/Wiki-GRx-Deploy
```

## 二次开发环境配置

`fourier-grx` 工具提供了 `fourier-grx setup_conda` 命令用于一键配置 conda 开发环境用于机器人二次开发。

```bash
# 在机器人主控电脑上：
fourier-grx setup_conda

# 程序运行完成后，会搭建出一个名为 `fourier-grx` 的 conda 环境，可以通过以下命令激活该环境
conda activate fourier-grx

# 如果希望自主搭建开发环境，可以在 $HOME/fourier-grx/whl 中找到依赖库文件进行手动安装。
```

---

## 用户接口示例（User API）

用户接口通过 [Zenoh](https://zenoh.io/) 协议与机器人通信，适用于高层应用开发。您可以在任何与机器人同一局域网的计算机上运行这些示例。

### 基础控制示例

| 示例名称  | 说明        | 代码路径                        |
|-------|-----------|-----------------------------|
| 机器人使能 | 控制机器人关节上电 | `user/demo_servo_on.py`     |
| 机器人失能 | 控制机器人关节下电 | `user/demo_servo_off.py`    |
| 重启机器人 | 重启机器人执行器  | `user/demo_servo_reboot.py` |
| 清除故障  | 清除机器人报警状态 | `user/demo_clear_fault.py`  |
| 设置零位  | 设置当前位置为零位 | `user/demo_set_home.py`     |

### 运动控制示例

| 示例名称 | 说明          | 代码路径                      |
|------|-------------|---------------------------|
| 关节测试 | 测试各关节运动功能   | `user/demo_test_joint.py` |
| 行走控制 | 使用手柄控制机器人行走 | `user/demo_walk.py`       |

### 运行方法

1. 在机器人主控电脑上启动 Fourier-GRX 主程序：
    ```bash
    # 激活 conda 环境
    conda activate fourier-grx
   
    # 运行具体机型的示例程序，配置文件需要根据具体机型进行修改，使用带 "_sdk.yaml" 后缀的配置文件
    python $HOME/fourier-grx/whl/run.py --config=$HOME/fourier-grx/config/{具体机型}/config_{具体机型}_sdk.yaml
    ```

2. 运行示例程序（可在远程电脑上执行）：
    ```bash
    # 激活 conda 环境
    conda activate fourier-grx
   
    # 运行具体机型的示例程序
    python $HOME/Wiki-GRx-Deploy/user/demo_{示例名称}.py
    ```

### 最佳实践

- 建议使用多个终端窗口同时运行和监控程序
- 远程控制时请确保网络连接稳定
- 运行示例前请仔细阅读相关安全说明

![终端示例](/fourier-grx-M4/assets/images/example_user_terminal.png)

---

## 开发者接口示例（Developer API）

开发者接口直接调用底层硬件接口，适用于底层开发。为确保实时性，这些示例必须在机器人主控电脑上运行。

### 系统控制示例

| 示例名称     | 说明          | 代码路径                             |
|----------|-------------|----------------------------------|
| 状态监控     | 打印机器人状态信息   | `developer/demo_print_state.py`  |
| 参数配置     | 设置关节 PID 参数 | `developer/demo_set_pid.py`      |
| 机器人执行器使能 | 控制机器人使能状态   | `developer/demo_servo_on.py`     |
| 机器人执行器失能 | 控制机器人失能状态   | `developer/demo_servo_off.py`    |
| 机器人执行器重启 | 重启机器人执行器    | `developer/demo_servo_reboot.py` |
| 零位设置     | 设置机器人零位     | `developer/demo_set_home.py`     |

### 运动控制示例

| 示例名称 | 说明           | 代码路径                           |
|------|--------------|--------------------------------|
| 移动关节 | 移动机器人关节到指定角度 | `developer/demo_move_joint.py` |

### 运行方法

```bash
# 激活 conda 环境
conda activate fourier-grx

# 运行具体机型的示例程序，配置文件需要根据具体机型进行修改，使用带 "_sdk.yaml" 后缀的配置文件
python $HOME/Wiki-GRx-Deploy/developer/demo_{示例名称}.py --config=$HOME/fourier-grx/config/{具体机型}/config_{具体机型}_sdk.yaml
```

### 注意事项

1. 开发者接口需要更深入的机器人知识
2. 建议先熟悉用户接口再使用开发者接口
3. 请注意备份重要的配置文件
4. 调试时建议在安全环境下进行
