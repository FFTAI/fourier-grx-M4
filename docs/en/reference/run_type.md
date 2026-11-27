---
layout: default
title: Run Modes
parent: Reference Guide
nav_order: 3.6
has_toc: true
nav_exclude: true
---

# Run Modes

* TOC
{:toc}

When installing or reconfiguring `fourier-grx`, you can select different run types. The relevant commands are:

- `fourier-grx list`: List the current configuration parameters, including the run type
- `fourier-grx install`: Install the program software; you will be prompted to select a run type during installation
- `fourier-grx config`: Reconfigure the startup parameters

The available run types are listed below:

- ✅ Available
- ❌ Not available
- ⚠️ Not yet released; functionality incomplete

| No. | Run Modes         | Config Value  | Description                                                                      | End User | Developer |
|-----|------------------|---------------|----------------------------------------------------------------------------------|----------|-----------|
| 1   | release mode     | release       | For factory-deployed robots; uses the **host PC** for robot control by default   | ✅       | ❌        |
| 2   | debug mode       | debug         | For developer debugging; shipped Real-backend M4L configs use the **keyboard** by default | ❌       | ✅        |
| 3   | Teleoperation    | teleoperation | For developer debugging; uses **Vision Pro** for robot control by default         | ❌       | ⚠️        |
| A   | developer mode   | sdk           | For developers using the **SDK** library for debugging                            | ❌       | ✅        |
| B   | server mode      | server        | For the SDK PubSub API; exchanges data with the server over Zenoh                    | ❌       | ✅        |
| C   | Offline debug    | offline       | For **offline** debugging; for internal testing only                              | ❌       | ❌        |

## Debug Mode

The shipped Real-backend M4L debug configs set `use_keyboard: true` and `use_joystick: false`, so the keyboard invokes internal algorithms by default. The currently selected and confirmed task status is printed in the terminal; to see it, start the program from a terminal window.
To use a joystick instead, set `use_joystick: true` and disable the keyboard in the active config. Task switching then uses combinations of the `L1`, `L2`, `R1`, and `R2` buttons.

- `L1` cycles through task selections; **double-click** `L2` within 0.3 s to confirm and execute a task
- `R1` cycles through module selections; **double-click** `R2` within 0.3 s to confirm and execute a module

> ℹ️ **Note**:
>
> For detailed descriptions of tasks and modules, and for more task function information, refer to the `task/client Interface Protocol (Command Information)` section of the [Reference Guide User API](/fourier-grx-M4/docs/en/reference/user).

The main features available via joystick in Fourier M4L debug mode include:

| Feature Name             | Task ID | Has Module | Description                              | Joystick Shortcut           |
|--------------------------|---------|------------|------------------------------------------|-----------------------------|
| Actuator disable (soft e-stop) | 36 | No        | Disable all robot actuators              | Logo button<br/>(XBOX layout) |
| Clear fault              | 34      | No         | Clear all robot joint alarms             | A<br/>(XBOX layout)          |
| Stand posture control    | 4020    | No         | Slowly move all joints back to standing posture | X<br/>(XBOX layout)   |
| Passive forward walking  | 4129    | No         | Passive forward walking task (4111 before v4.4.69) | Y<br/>(XBOX layout)          |

## Developer Mode

In developer mode, users can refer to the open development interface for secondary development.
The development interface and example programs can be found at:

- Development interface: [Reference Guide](/fourier-grx-M4/docs/en/reference)
- Example programs: [Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy)
