---
layout: default
title: Examples
nav_order: 2
has_toc: true
has_children: true
nav_exclude: true
---

# Examples

* TOC
{:toc}

This documentation provides a rich set of example code to help you quickly learn how to use the Fourier-GRX-M4 SDK.

- Example code for M4 series robots is located in the `FourierM4` branch of [Github Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy.git).
- Example code for M4L series robots is located in the `FourierM4L` branch of [Github Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy.git).

The examples cover both the User API and Developer API, catering to different levels of development needs.

## Example Entry Points

- [User API Examples](/fourier-grx-M4/docs/en/examples/user): For high-level application development. Can run on the robot's main controller or any other computer on the same LAN.
- [Developer API Examples](/fourier-grx-M4/docs/en/examples/developer): For low-level development. Must run on the robot's main controller.
- For interface field descriptions and protocol details, refer to the [Reference Guide](/fourier-grx-M4/docs/en/reference) alongside these examples.

## Example Code Repository

You can clone the robot secondary-development example programs via git:

### M4 Series Robots

```bash
# Run in the $HOME directory of the robot's main controller
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4
cd $HOME/Wiki-GRx-Deploy
```

### M4L Series Robots

```bash
# Run in the $HOME directory of the robot's main controller
git clone https://github.com/FFTAI/Wiki-GRx-Deploy.git --branch=FourierM4L
cd $HOME/Wiki-GRx-Deploy
```

## Development Environment Setup

The `fourier-grx` tool provides the `fourier-grx setup_conda` command to set up a conda development environment for robot secondary development with a single command.

```bash
# On the robot's main controller:
fourier-grx setup_conda

# After the command completes, a conda environment named `fourier-grx` will be created.
# Activate it with:
conda activate fourier-grx

# If you prefer to set up the environment manually, you can find the dependency wheel
# files under $HOME/fourier-grx/whl and install them manually.
```

It is recommended to clone the repository into the `$HOME` directory. After cloning, you can navigate to it with `cd $HOME/Wiki-GRx-Deploy`.

For instructions on running specific example programs, refer to the respective interface pages:

- [User API](/fourier-grx-M4/docs/en/examples/user)
- [Developer API](/fourier-grx-M4/docs/en/examples/developer)
