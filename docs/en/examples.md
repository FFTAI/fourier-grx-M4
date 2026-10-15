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
- The [User API Examples](/fourier-grx-M4/docs/en/examples/user) page also lists the **raw UDP socket examples**, which talk to the robot using only the Python standard library and need no `fourier_grx` SDK installation — useful for quickly checking the protocol on a machine without the SDK environment.
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

> ℹ️ Cloning into `$HOME` is recommended, so the examples sit next to the `fourier-grx` installation directory.

## Development Environment Setup

The `fourier-grx` tool provides the `fourier-grx setup_uv` command, which sets up a [uv](https://docs.astral.sh/uv/)-based Python 3.11 development environment for robot secondary development with a single command.

```bash
# 1. Build the development environment on the robot's main controller (internet access required)
fourier-grx setup_uv

# 2. Activate it (the virtual environment always lives in $HOME/fourier-grx/.venv)
source $HOME/fourier-grx/.venv/bin/activate

# 3. Check that fourier_grx imports cleanly — no output means success
python -c "import fourier_grx"
```

Notes:

- For a Python 3.10 environment, use `fourier-grx setup_uv_py310` instead; the virtual environment location stays the same.
- To set the environment up fully by hand, the `fourier_core` / `fourier_grx` wheels are in `$HOME/fourier-grx/whl`, and the remaining dependencies are listed in the `pyproject.toml` of the `fourier-grx` repository.
- To tell whether the environment is ready: if `python -c "import fourier_grx"` succeeds, the SDK examples in this repository will run. The examples under `demo/udp` do not need this environment at all.

For instructions on running specific example programs, refer to the respective interface pages:

- [User API](/fourier-grx-M4/docs/en/examples/user) (including the raw UDP socket examples)
- [Developer API](/fourier-grx-M4/docs/en/examples/developer)
