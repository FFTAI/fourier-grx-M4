---
layout: default
title: M4L 机器人
nav_order: 1.5
parent: 快速开始
has_toc: true
---

# M4L 机器人

* TOC
{:toc}

## 系统开机

当我们拿到机器人后，首先需要将机器人开机。

1. 接通机器人的电源开关。（背包上的按钮为 供电电源🔋 按钮）
2. 确保机器人的急停按钮处于松开状态。
3. 确认所有关节执行器的指示灯为 <span style="color: purple;">紫色慢闪</span> 状态（正常工作状态）。

## 登录系统

### 本地登录

连接机器人控制电脑的 HDMI 显示器和 USB 键盘鼠标，开机后会自动进入系统桌面。用户信息如下：

- 用户名为 `cat`
- 用户密码为 `temppwd`

### 远程登录

机器人开机后，用户可以通过有线网络方式连接机器人。
机器人主控电脑的有线网口 IP 地址为 `192.168.137.220`，可以通过 `ssh` 服务登录到机器人的主控电脑，登录用户名和密码与本地登录方式相同。

> ℹ️ 如果现场没有可用的路由器，可参考 [网络连接与远程登录](/fourier-grx-M4/docs/usage/network_connection) 页面，通过笔记本/平板共享 WiFi 网络到有线网口连接机器人。

## 程序启动

机器人出厂时默认已装好 `fourier-grx` 软件工具；若未安装，请到 [固件发布](/fourier-grx-M4/docs/release) 页面查看下载和安装流程。

用 `fourier-grx start` 启动机器人控制程序。

```bash
# 在机器人主控电脑上：
# 1. 准备好手柄，连接到机器人主控电脑的 USB 端口。
# 2. 启动 fourier-grx 主程序
fourier-grx start
```

程序启动完成后，即可使用手柄控制机器人完成相应的任务。（图片为 XBOX 键位手柄，具体按键功能对应关系与所用手柄种类相关）

在控制程序启动后，您可以按照如下步骤进行操作，将机器人切换为行走控制状态：

1. 按下手柄的 `Y` 键，进入 **行走状态**。
   - 此时机器人会解锁腿部关节，准备开始行走。

2. 如果遇到任何机器人的异常情况，可以按下手柄的 `logo` 键，进入 **急停任务**。
   - 此时机器人会立即停止所有动作，并 `失能` 所有关节 
   - **（注意：此时机器人会瘫软下去，请确保已做好相关保护措施，防止机器人磕坏）**。

3. 如果按下了机器人背包上的 **硬件急停按钮**（红色急停开关），M4LT2 机型将自动切换到 **高阻尼保护模式**（`TASK_ROTARY_JOINT_HIGH_DAMPING`）：
   - 关节保持上电，输出阻尼力矩，**肢体不会瞬间跌落**；
   - 高阻尼模式将持续保持，直到手动切换到其他任务（如 `TASK_STAND_CONTROL`）；
   - 此行为与手柄 `logo` 键的直接断电（失能）不同，详见 [高阻尼保护任务说明](/fourier-grx-M4/docs/tasks/emergency_stop_high_damping)。

## 局域网网页调试

不想连手柄、也不写代码时，可以用浏览器调试机器人。启动控制程序后，在机器人主控电脑上执行：

```bash
fourier-grx web
```

`fourier-grx web` 会通过 UDP 广播自动发现机器人，无需填写 IP。若跨网段等原因发现失败，加上机器人 IP：`fourier-grx web --host 192.168.137.220`。

随后在同一局域网内任意电脑的浏览器打开 `http://192.168.137.220:8000`，界面提供：

| 功能 | 说明 |
|------|------|
| 实时状态 | 连接状态、当前任务、错误码、电池、IMU 姿态、关节位置 / 速度 / 力矩，约 10 Hz 刷新 |
| 任务下发 | 按分组列出全部任务按钮；失能、重启、设零点等危险命令需二次确认；右下角常驻急停按钮 |
| 虚拟面板 | 滑条、开关与 start / stop / pause，可替代手柄调参与启停任务 |
| 运行日志 | 每次下发的任务命令、摇杆与面板数据会打印在 `fourier-grx web` 所在终端 |

> ⚠️ **注意**
>
> - 面板改动**不会自动下发**，需点击卡片上的「下发」按钮。
> - 摇杆与面板的值在机器人侧是**锁存**的，最后一次下发的值会一直生效，直到被新值覆盖或切换任务。界面上的「复位」只把指针归零，**不会让机器人停下**。

参数与端口说明见 [命令行工具 · `fourier-grx web`](/fourier-grx-M4/docs/reference/command_line_tool#fourier-grx-web-详细说明)。

---

## 二次开发环境配置

`fourier-grx` 提供 `setup_uv` 命令，一键搭建二次开发所需的 uv 虚拟环境（Python 3.11）。

```bash
# 在机器人主控电脑上：
fourier-grx setup_uv

# 环境位于 $HOME/fourier-grx/.venv，激活方式：
source $HOME/fourier-grx/.venv/bin/activate

# 需要 Python 3.10 时改用：fourier-grx setup_uv_py310
```

> ℹ️ 执行前请确保机器人主控电脑可以访问外网。

## 示例程序运行

开发环境搭好后，通过 git 同步机器人的二次开发接口示例程序。

```bash
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4L
```

建议同步到 `$HOME` 目录下，同步完成后，可以通过 `cd $HOME/Wiki-GRx-Deploy` 进入该目录查看。

然后，我们可以通过以下命令启动示例程序：

```bash
# 在机器人主控电脑上打开 Terminal
# 激活开发环境
source $HOME/fourier-grx/.venv/bin/activate

# 启动 fourier-grx 主程序
$HOME/fourier-grx/run.bin --config=$HOME/fourier-grx/config/m4l/config_M4L_T1_sdk.yaml

# M4LP1 机型请改用：
# $HOME/fourier-grx/run.bin --config=$HOME/fourier-grx/config/m4l/config_M4L_P1_sdk.yaml

# 当看到提示信息 ”You can start playing with the robot right now.“ 时，表示程序启动成功。
```

```bash
# 在机器人主控电脑上或与机器人同局域网内的任意一台电脑上打开 Terminal
# 1. 启动 user 接口示例
# 激活开发环境
source $HOME/fourier-grx/.venv/bin/activate

# 启动示例程序，进入行走状态.
python $HOME/Wiki-GRx-Deploy/user/demo_walk.py
```

至此，我们已经完成了机器人的快速开始。接下来，我们可以通过 [示例代码](/fourier-grx-M4/docs/examples) 来了解更多的机器人各项功能。🎆🎆🎆
