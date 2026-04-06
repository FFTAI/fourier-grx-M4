---
layout: default
title: Run Type
nav_order: 3.6
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Run Type

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

| No. | Run Type         | Config Value  | Description                                                                      | End User | Developer |
|-----|------------------|---------------|----------------------------------------------------------------------------------|----------|-----------|
| 1   | release mode     | release       | For factory-deployed robots; uses the **host PC** for robot control by default   | ✅       | ❌        |
| 2   | debug mode       | debug         | For developer debugging; uses a **joystick** for robot control by default         | ❌       | ✅        |
| 3   | Teleoperation    | teleoperation | For developer debugging; uses **Vision Pro** for robot control by default         | ❌       | ⚠️        |
| A   | developer mode   | sdk           | For developers using the **SDK** library for debugging                            | ❌       | ✅        |
| B   | Offline debug    | offline       | For **offline** debugging; for internal testing only                              | ❌       | ❌        |

### Debug Mode

In debug mode, the robot primarily uses a **joystick** 🎮 to invoke internal algorithms and perform motion tasks.
Task switching is achieved using combinations of the `L1`, `L2`, `R1`, and `R2` buttons on the joystick.
The currently selected and confirmed task status is printed in the terminal; to see it, you must start the program from a terminal window.

- `L1` is used to cycle through task selections; `L2` is used to confirm and execute a task
- `R1` is used to cycle through module selections; `R2` is used to confirm and execute a module

> ℹ️ **Note**:
>
> For detailed descriptions of tasks and modules, and for more task function information, refer to the `task/client Interface Protocol (Command Information)` section of the [Reference Guide User API](/fourier-grx-M4/docs/en/reference/user).

The main features available via joystick in Fourier M4L debug mode include:

| Feature Name             | Task ID | Has Module | Description                              | Joystick Shortcut           |
|--------------------------|---------|------------|------------------------------------------|-----------------------------|
| Actuator disable (soft e-stop) | 36 | No        | Disable all robot actuators              | Logo button<br/>(XBOX layout) |
| Clear fault              | 34      | No         | Clear all robot joint alarms             | A<br/>(XBOX layout)          |
| Stand posture control    | 4020    | No         | Slowly move all joints back to standing posture | X<br/>(XBOX layout)   |
| Passive forward walking  | 4111    | No         | Passive forward walking task             | Y<br/>(XBOX layout)          |

### Developer Mode

In developer mode, users can refer to the open development interface for secondary development.
The development interface and example programs can be found at:

- Development interface: [Reference Guide](/fourier-grx-M4/docs/en/reference)
- Example programs: [Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy)
