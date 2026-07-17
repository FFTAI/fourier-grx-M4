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
| `update`          | Check the server for a newer version of the package and interactively select a version to install  |

---

## `fourier-grx update` Detailed Instructions

The `update` command checks the Fourier server for a newer version of the package and guides the user through downloading and installing it.

### Usage

```bash
fourier-grx update                    # Automatically detect the installed package variant and check for updates
fourier-grx update <variant>          # Manually specify the variant (for older installed packages)
fourier-grx update --help             # Show help information
```

`<variant>` is the package's platform/model identifier, e.g. `linux-arm64-cpu-m4l-blaze`.

### Workflow

1. Reads the currently installed version number and variant information
2. Probes the server for available newer versions (via HTTP HEAD requests, version by version)
3. Lists all available newer versions and marks the latest one
4. Prompts the user to select a version number to install (press Enter to install the latest version by default, enter `n` to cancel)
5. Downloads the `.deb` package for the selected version
6. Completes the installation with `sudo dpkg -i`

### Example Output

```
Current version : 4.4.4
Current variant  : linux-arm64-cpu-m4l-blaze
Checking for updates...

Found the following newer versions:
----------------------------------------------------
  [1] v4.4.5  fourier-grx-4.4.5-linux-arm64-cpu-m4l-blaze.deb
  [2] v4.4.6  fourier-grx-4.4.6-linux-arm64-cpu-m4l-blaze.deb
  [3] v4.4.7  fourier-grx-4.4.7-linux-arm64-cpu-m4l-blaze.deb  ← latest
----------------------------------------------------

Select the version number to install (press Enter for latest [2], or n to cancel):
```

### After Installation Completes

After the download completes, run the following command to finish the full installation process:

```bash
fourier-grx install
```

### Notes

- **Older installed packages**: packages for version 4.4.4 and earlier do not include variant information, so you must pass the variant manually, e.g.:
  ```bash
  fourier-grx update linux-arm64-cpu-m4l-blaze
  ```
  After upgrading to a newer version, subsequent runs of `fourier-grx update` will automatically detect the variant and no longer require manual specification.

- **Network requirements**: the update process requires access to the Fourier package server; make sure the network connection is working.

- **Permission requirements**: the installation step requires `sudo` privileges; the system will prompt for a password.
