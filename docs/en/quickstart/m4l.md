---
layout: default
title: M4L Robot
nav_order: 1.2
parent: "Quick Start"
has_toc: true
nav_exclude: true
---

# M4L Robot

* TOC
{:toc}

## Video Tutorial

The following video tutorial demonstrates how to quickly get started with the M4L series robot.

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

---

## Development Environment Setup

In addition to launching the control program, the `fourier-grx` tool provides the `fourier-grx setup_conda` command to set up a conda development environment for robot secondary development with a single command.

```bash
# On the robot's controller computer:
fourier-grx setup_conda

# After the command completes, a conda environment named `fourier-grx` will be created.
# Activate it with:
conda activate fourier-grx

# If you prefer to set up the development environment manually, the dependency wheel files
# can be found under $HOME/fourier-grx/whl for manual installation.
```

## Running Example Programs

After setting up the conda environment, you can clone the robot's secondary development interface examples via git.

```bash
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4L
```

It is recommended to clone into the `$HOME` directory. After cloning, navigate to the directory with `cd $HOME/Wiki-GRx-Deploy`.

Then, launch the example programs with the following commands:

```bash
# Open a Terminal on the robot's controller computer
# 1. Launch the fourier-grx main program
# Activate the conda environment
conda activate fourier-grx

# Launch the fourier-grx main program
python $HOME/fourier-grx/whl/run.py --config=$HOME/fourier-grx/config/m4l/config_M4L_T1_sdk.yaml

# For the M4LP1 variant, use instead:
# python $HOME/fourier-grx/whl/run.py --config=$HOME/fourier-grx/config/m4l/config_M4L_P1_debug.yaml

# When you see the message "You can start playing with the robot right now.", the program has started successfully.
```

```bash
# Open a Terminal on the robot's controller computer or any computer on the same LAN
# 1. Launch the user interface example
# Activate the conda environment
conda activate fourier-grx  

# Launch the example program to enter walking mode.
python $HOME/Wiki-GRx-Deploy/user/demo_walk.py
```

You have now completed the robot Quick Start. Next, explore the [Example Code](/fourier-grx-M4/docs/en/examples) to learn about more robot features. 🎆🎆🎆
