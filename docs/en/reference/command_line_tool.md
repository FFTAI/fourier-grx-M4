---
layout: default
title: Command Line Tool
nav_order: 3.7
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Command Line Tool

After installing the Fourier-GRX-M4 SDK, you can use the command line tool `fourier-grx` to manage and control the robot.

`fourier-grx` is the command line tool for the Fourier-GRX-M4 SDK, used to install, configure, and control the Fourier M4 robot.

Running `fourier-grx` in a terminal will display a list of available sub-commands and help information.

Currently supported sub-commands are:

| Sub-command       | Description                                                                                         |
|-------------------|-----------------------------------------------------------------------------------------------------|
| `version`         | Display the current Fourier-GRX-M4 SDK version information                                          |
| `install`         | Install the Fourier-GRX-M4 SDK runtime environment and dependency libraries                         |
| `uninstall`       | Uninstall the Fourier-GRX-M4 SDK runtime environment and dependency libraries                       |
| `config`          | Configure the startup parameters for the Fourier-GRX-M4 SDK                                        |
| `list`            | List the current startup parameters for the Fourier-GRX-M4 SDK                                     |
| `start`           | Start the Fourier-GRX-M4 SDK runtime environment and robot                                          |
| `stop`            | Stop the Fourier-GRX-M4 SDK runtime environment and robot (forcefully kills related processes)      |
| `enable_service`  | Enable the Fourier-GRX-M4 SDK service so the robot control program starts automatically on reboot   |
| `disable_service` | Disable the Fourier-GRX-M4 SDK service so the robot control program does not start automatically on reboot |
| `background`      | Run the Fourier-GRX-M4 SDK runtime environment and robot program in the background                  |
| `setup_conda`     | Create a Conda environment for the Fourier-GRX-M4 SDK and install the required dependency libraries |
