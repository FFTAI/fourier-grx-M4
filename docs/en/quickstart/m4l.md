---
layout: default
title: M4L Robot
nav_order: 1.5
parent: "Quick Start"
has_toc: true
nav_exclude: true
---

# M4L Robot

* TOC
{:toc}

## Powering On

Once you have the robot, the first step is to power it on.

1. Turn on the robot's power switch. (The button on the backpack is the power supply 🔋 button.)
2. Make sure the robot's emergency stop button is released.
3. Confirm that the indicator lights on all joint actuators show a <span style="color: purple;">slow purple blink</span> (normal operating state).

## Logging In

### Local Login

Connect an HDMI monitor and a USB keyboard/mouse to the robot's controller computer. After booting, the system desktop will appear automatically. Credentials are:

- Username: `cat`
- Password: `temppwd`

### Remote Login

After the robot boots, you can connect to it over a wired network.
The wired network interface IP address of the robot's controller computer is `192.168.137.220`. You can log in via `ssh` using the same username and password as the local login.

> ℹ️ If no router is available on-site, refer to the [Network Connection and Remote Login](/fourier-grx-M4/docs/en/usage/network_connection) page to share WiFi from a laptop/tablet to the wired ethernet port and connect to the robot.

## Starting the Program

The `fourier-grx` software tool is installed by default when the robot ships from the factory.
If it is not installed, refer to the [Firmware Releases](/fourier-grx-M4/docs/en/release) page for download and installation instructions.

The tool provides the `fourier-grx start` command to launch the robot control program.

```bash
# On the robot's controller computer:
# 1. Prepare the gamepad and connect it to the robot controller's USB port.
# 2. Launch the fourier-grx main program
fourier-grx start
```

Once the program starts, you can use the gamepad to control the robot and perform the corresponding tasks. (The diagram shows an XBOX-layout gamepad; the specific button mapping depends on the type of gamepad used.)

After the control program starts, follow these steps to switch the robot into walking control mode:

1. Press the `Y` button on the gamepad to enter **Walking Mode**.
   - The robot will unlock its leg joints and prepare to walk.

2. If any abnormality occurs, press the `logo` button on the gamepad to trigger the **Emergency Stop**.
   - The robot will immediately stop all movements and `disable` all joints.
   - **(Note: The robot will go limp. Make sure proper protective measures are in place to prevent damage.)**

3. If the **hardware emergency stop button** (red emergency switch on the robot backpack) is pressed, M4LT2 will automatically switch to **High-Damping Protection mode** (`TASK_ROTARY_JOINT_HIGH_DAMPING`):
   - Joints remain powered and output damping torque — **limbs will not drop instantly**;
   - High-damping mode persists until you manually switch to another task (e.g., `TASK_STAND_CONTROL`);
   - This behavior differs from the gamepad `logo` key, which immediately cuts power (servo-off). See [High-Damping Protection Task](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping) for details.

---

## Web Debugging over the LAN

When you want to debug the robot without a gamepad and without writing code, use the browser. After the control program is running, execute the following on the robot's controller computer:

```bash
fourier-grx web
```

`fourier-grx web` discovers the robot automatically via UDP broadcasts, so no IP needs to be entered. If discovery fails (for example across subnets), pass the robot IP explicitly: `fourier-grx web --host 192.168.137.220`.

Then open `http://192.168.137.220:8000` in a browser on any computer in the same LAN. The interface provides:

| Feature | Description |
|---------|-------------|
| Live state | Connection state, current task, error codes, battery, IMU attitude, joint position / velocity / torque, refreshed at about 10 Hz |
| Task dispatch | All task buttons, grouped; risky commands (servo off, reboot, set home) require confirmation; a persistent emergency stop button sits in the lower-right corner |
| Virtual panel | Sliders, switches, and start / stop / pause, as a substitute for the gamepad when tuning parameters and starting or stopping tasks |
| Run log | Every dispatched task command, joystick, and panel value is printed to the terminal running `fourier-grx web` |

> ⚠️ **Note**
>
> - Panel changes are **not sent automatically** — click **Send** on the card to dispatch them.
> - Joystick and panel values are **latched** on the robot: the last value sent stays in effect until a new value overwrites it or the task changes. Pressing **Reset** in the interface only returns the pointer to zero — **it does not stop the robot**.

For options and port details, see [Command Line Tool · `fourier-grx web`](/fourier-grx-M4/docs/en/reference/command_line_tool#fourier-grx-web-detailed-instructions).

---

## Development Environment Setup

`fourier-grx setup_uv` builds the uv virtual environment (Python 3.11) required for secondary development in one step.

```bash
# On the robot's controller computer:
fourier-grx setup_uv

# The environment lives in $HOME/fourier-grx/.venv. Activate it with:
source $HOME/fourier-grx/.venv/bin/activate

# For Python 3.10, use: fourier-grx setup_uv_py310
```

> ℹ️ Make sure the robot's controller computer can reach the internet before running the command.

## Running Example Programs

Once the development environment is ready, clone the robot's secondary development interface examples via git.

```bash
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4L
```

It is recommended to clone into the `$HOME` directory. After cloning, navigate to the directory with `cd $HOME/Wiki-GRx-Deploy`.

Then, launch the example programs with the following commands:

```bash
# Open a Terminal on the robot's controller computer
# Activate the development environment
source $HOME/fourier-grx/.venv/bin/activate

# Launch the fourier-grx main program
$HOME/fourier-grx/run.bin --config=$HOME/fourier-grx/config/m4l/config_M4L_T1_sdk.yaml

# For the M4LP1 variant, use instead:
# $HOME/fourier-grx/run.bin --config=$HOME/fourier-grx/config/m4l/config_M4L_P1_sdk.yaml

# When you see the message "You can start playing with the robot right now.", the program has started successfully.
```

```bash
# Open a Terminal on the robot's controller computer or any computer on the same LAN
# Activate the development environment
source $HOME/fourier-grx/.venv/bin/activate

# Launch the example program to enter walking mode.
python $HOME/Wiki-GRx-Deploy/user/demo_walk.py
```

You have now completed the robot Quick Start. Next, explore the [Example Code](/fourier-grx-M4/docs/en/examples) to learn about more robot features. 🎆🎆🎆
