---
layout: default
title: User Interface
nav_order: 2.1
parent: "Examples"
nav_exclude: true
toc: true
toc_min_header: 2
toc_max_header: 3
---

# User Interface

The Fourier-GRX User Interface is designed for high-level application development and communicates with the robot over the network.

You can run these examples on the robot controller or on any computer connected to the same LAN as the robot.

## How to Run

1. Configure the run mode of `fourier-grx` on the robot controller:
   ```bash
   # Edit the fourier-grx configuration
   fourier-grx config

   # Select "developer mode" (sdk) as the run mode
   ```

   The User-interface examples rely on the robot's UDP communication channel, so the config file actually used at startup must contain:

   ```yaml
   dynalink:
     enable: true

   communication:
     enable: true
     period: 0.02  # 50Hz
     type: "socket"
   ```

   The M4L `release` and `debug` config files already include these fields; the M4L `sdk` config file currently only has `dynalink.enable`, so you need to add the `communication` section yourself — otherwise the robot never listens on UDP 5566 and the examples stay at "等待连接到机器人..." forever.
   Run `fourier-grx list` to see which config file is currently in effect.

2. Start the Fourier-GRX main program on the robot controller:
    ```bash
    # Start the `fourier-grx` main program
    fourier-grx start
    ```

3. Run the example script (can be executed on a remote host computer):
    ```bash
    # Activate the development environment (virtual environment at $HOME/fourier-grx/.venv)
    source $HOME/fourier-grx/.venv/bin/activate

    # Clone the example code repository (if not already cloned)
    git clone https://github.com/FFTAI/fourier-grx-M4.git

    # Enter the demo directory and run an example
    cd fourier-grx-M4/demo/user
    python demo_{example_name}.py
    ```

   A successful run first prints `等待连接到机器人...`, then `已连接到机器人 <robot IP>:5566` followed by the message that was sent; the control examples (servo on/off, etc.) then exit on their own.
   If it stays at "等待连接到机器人..." for a long time, check that the robot has been started, that `communication.enable` is `true`, and that both machines are on the same LAN.

### Best Practices

- It is recommended to use multiple terminal windows to run and monitor programs simultaneously.
- Ensure a stable network connection when controlling the robot remotely.
- Read the relevant safety instructions carefully before running any example.

![Terminal Example](/fourier-grx-M4/assets/images/example_user_terminal.png)

## Interface Examples

### Basic Control Examples

| Example Name       | Description                        | Code Path                       |
|--------------------|------------------------------------|---------------------------------|
| Servo On           | Enable robot actuators             | `demo/user/demo_servo_on.py`         |
| Servo Off          | Disable robot actuators            | `demo/user/demo_servo_off.py`        |
| Servo Reboot       | Reboot robot actuators             | `demo/user/demo_servo_reboot.py`     |
| Clear Fault        | Clear robot fault/alarm state      | `demo/user/demo_clear_fault.py`      |
| Set Home           | Sends TID 999; M4L does not register this task — use 4103 / 4203 instead (see the notes in the script) | `demo/user/demo_set_home.py`         |
| Clear Protection   | Clear over-load / torque protection flags (robot topic) | `demo/user/demo_clear_protection.py` |
| Get State          | Read task state, joint positions, IMU, battery, etc. (task / robot / grx topics) | `demo/user/demo_get_state.py` |
| Host Heartbeat     | Keep writing the heartbeat field (comm topic); works with the disconnect protection | `demo/user/demo_heartbeat.py` |

### Motion Control Examples

| Example Name   | Description                              | Code Path                   |
|----------------|------------------------------------------|-----------------------------|
| Joint Test     | Sends TID 902; M4L does not register this task — use 4100 / 4200 instead (see the notes in the script) | `demo/user/demo_test_joint.py`   |
| Walk Control   | Sends TID 965 to enter the walk task; actual walking still needs joystick or virtual-panel input | `demo/user/demo_walk.py`         |
| Virtual Panel  | Set step length/velocity via the virtual panel and start/stop walking (grx topic) | `demo/user/demo_virtual_panel.py` |

### UDP Raw Socket Examples (No SDK Required)

The following examples use only the Python standard library (`socket` + `struct`) — no `fourier_grx` SDK or third-party packages needed. See `demo/udp/README.md` for details:

| Example Name | Description                                   | Code Path                    |
|--------------|-----------------------------------------------|------------------------------|
| Servo On     | Enable robot actuators over UDP               | `demo/udp/demo_servo_on.py`  |
| Servo Off    | Disable robot actuators over UDP              | `demo/udp/demo_servo_off.py` |
| Servo Reboot | Reboot robot actuators over UDP               | `demo/udp/demo_servo_reboot.py` |
| Clear Fault  | Clear robot fault/alarm state over UDP        | `demo/udp/demo_clear_fault.py` |
| Walk Control | Control robot walking over UDP                | `demo/udp/demo_walk.py`      |
| Get State    | Receive and print robot state (task / comm)   | `demo/udp/demo_get_state.py` |
| Clear Protection | Clear over-load / torque protection flags (robot topic) | `demo/udp/demo_clear_protection.py` |
| Virtual Panel | Set step length/velocity via the virtual panel and start/stop walking (grx topic) | `demo/udp/demo_virtual_panel.py` |
| Virtual Joystick | Write virtual joystick axis states (grx topic) | `demo/udp/demo_virtual_joystick.py` |
| Heartbeat    | Keep writing the heartbeat field; demos disconnect protection | `demo/udp/demo_heartbeat.py` |
