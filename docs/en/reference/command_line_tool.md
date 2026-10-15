---
layout: default
title: Command Line Tool
nav_order: 3.7
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Command Line Tool

After installing the Fourier-GRX-M4 SDK, use the `fourier-grx` command line tool to manage and control the robot.

Run `fourier-grx` in a terminal to list all sub-commands. The supported sub-commands are:

| Sub-command       | Description                                                                                         |
|-------------------|-----------------------------------------------------------------------------------------------------|
| `version`         | Display the current Fourier-GRX-M4 SDK version information                                          |
| `install`         | Deploy the Fourier-GRX-M4 SDK runtime environment; prompts for the robot model and run type         |
| `uninstall`       | Remove the `~/fourier-grx` deployment directory                                                     |
| `config`          | Configure the startup parameters for the Fourier-GRX-M4 SDK                                        |
| `list`            | List the current startup parameters for the Fourier-GRX-M4 SDK                                     |
| `start`           | Start the Fourier-GRX-M4 SDK runtime environment and robot                                          |
| `stop`            | Stop the Fourier-GRX-M4 SDK runtime environment and robot (forcefully kills related processes)      |
| `enable_service`  | Enable the Fourier-GRX-M4 SDK service so the robot control program starts automatically on reboot   |
| `disable_service` | Disable the Fourier-GRX-M4 SDK service so the robot control program does not start automatically on reboot |
| `background`      | Run the Fourier-GRX-M4 SDK runtime environment and robot program in the background                  |
| `setup_uv`        | Create the uv development environment (Python 3.11) and install the required dependencies          |
| `setup_uv_py310`  | Same as above, using Python 3.10                                                                    |
| `update`          | Check the server for a newer version of the package and interactively select a version to install   |
| `web`             | Start the web debugging host, accessed from a browser on the same LAN                               |

---

## The Two Layers of Installation

Installing `fourier-grx` involves two layers. Both are required:

| Layer | Command | Effect |
|-------|---------|--------|
| Package layer | `sudo dpkg -i fourier-grx-<version>-<variant>.deb` | Unpacks the archive into `/usr/share/fourier-grx/` and installs the `fourier-grx` tool itself |
| Deployment layer | `fourier-grx install` | Deploys the zip into `~/fourier-grx/`, sets up the runtime, and prompts for the robot model, version, and run type |

> ⚠️ **Note**
>
> Running `dpkg -i` alone does **not** make the robot use the new version — what actually runs is the content of `~/fourier-grx/`. Always run `fourier-grx install` after `dpkg -i`.

What `fourier-grx install` does:

1. If `~/fourier-grx` already exists, backs the whole directory up to `~/fourier-grx-bak` (any previous backup is overwritten)
2. Deletes `~/fourier-grx` and unpacks `/usr/share/fourier-grx/fourier-grx.zip` into it
3. Runs `setup.sh` to configure the system environment
4. Runs `config.sh --from-bak`: if the backup directory holds a usable configuration, you are asked whether to reuse it; otherwise you go through the interactive selection

---

## `fourier-grx update` Detailed Instructions

`update` checks the Fourier server for newer versions and handles the download and `dpkg` installation. It covers **only the package layer** above — you still need to run `fourier-grx install` afterwards.

### Usage

```bash
fourier-grx update                        # Probe available newer versions and install interactively
fourier-grx update <version>              # Install a specific version; the variant is read from the installed package
fourier-grx update <version>-<channel>    # Install a specific channel build, e.g. 4.4.53-prerelease
fourier-grx update --help                 # Show help information
```

The variant is the package's platform/model identifier (the deb `X-Variant` field), e.g. `linux-arm64-cpu-m4l-blaze`. It is supplied automatically by the installed package and never needs to be typed.

### Automatic probing range

Without arguments, versions newer than the current one are probed:

- Current minor version: `patch + 1` through `patch + 20`, stopping after 5 consecutive 404s
- Next versions: only `minor + 1` (patch 0-10, stopping after 3 consecutive 404s) and `minor 0` of `major + 1` (patch 0-5, stopping after 3 consecutive 404s)

### Workflow

1. Reads the currently installed version number and variant from the deb record
2. Probes the server for available newer versions, version by version (HTTP HEAD requests)
3. Lists all available newer versions and marks the latest one
4. Prompts the user to select a version number (press Enter to install the latest version, enter `n` to cancel)
5. Downloads the `.deb` package for the selected version
6. Completes the installation with `sudo dpkg -i`

### Example Output

```text
Current version : 4.4.4
Current variant  : linux-arm64-cpu-m4l-blaze
Checking for updates...

Found the following newer versions:
----------------------------------------------------
  [1] v4.4.5  fourier-grx-4.4.5-linux-arm64-cpu-m4l-blaze.deb
  [2] v4.4.6  fourier-grx-4.4.6-linux-arm64-cpu-m4l-blaze.deb
  [3] v4.4.7  fourier-grx-4.4.7-linux-arm64-cpu-m4l-blaze.deb  ← latest
----------------------------------------------------

Select the version number to install (press Enter for latest [3], or n to cancel):
```

### After Installation Completes

Run `fourier-grx install` to update the deployment layer — see [The Two Layers of Installation](#the-two-layers-of-installation) above.

### Pre-release Channel

Pre-release builds carry `prerelease` (instead of `blaze` for stable builds) as the last segment of both the file name and the `X-Variant`, keeping the model segment unchanged, e.g. `fourier-grx-4.4.53-linux-arm64-cpu-m4l-prerelease.deb`.

- The automatic probe above builds file names from the installed package's `X-Variant` (`...-blaze`), so it will **never** find a pre-release package.
- Pre-release builds can only be installed explicitly with `<version>-prerelease`:

```bash
fourier-grx update 4.4.53-prerelease
```

- This form replaces only the last segment of the variant with `prerelease`; the model part still comes from the installed package.
- The syntax is available since v4.4.53; on earlier versions, install pre-release packages manually with `sudo dpkg -i <deb>`.
- `fourier-grx install` is still required afterwards.

### Notes

- **Packages without variant information**: some much older packages have no `X-Variant` field in the deb. `fourier-grx update` then reports an error and exits, and there is no argument to pass the variant manually. Install a newer `.deb` with `sudo dpkg -i` first, then run `fourier-grx update`.

- **Network requirements**: the update process requires access to the Fourier package server; make sure the network connection is working.

- **Permission requirements**: the installation step requires `sudo` privileges; the system will prompt for a password.

---

## `fourier-grx web` Detailed Instructions

`web` starts a LAN web debugging interface on the robot's controller computer (see [M4L Robot · Web Debugging over the LAN](/fourier-grx-M4/docs/en/quickstart/m4l#web-debugging-over-the-lan)).

```bash
fourier-grx web                            # Auto-discover the robot, listen on 0.0.0.0:8000
fourier-grx web --host 192.168.137.220     # Skip auto-discovery and set the robot IP directly
fourier-grx web --port 8080                # Change the web service port
fourier-grx web --bind 127.0.0.1           # Change the web service bind address
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | none | **The robot's IP address**. When omitted, the robot is discovered automatically via UDP 9527 broadcasts |
| `--robot-port` | `5566` | The robot's UDP data port |
| `--bind` | `0.0.0.0` | **The web service bind address**; leave the default to allow LAN access |
| `--port` | `8000` | The web service listen port |

> ⚠️ **Note**: `--host` points at the robot, `--bind` at the web service itself. They are different things — do not mix them up.

Once started, open `http://<robot-IP>:8000` in a browser on any computer in the same LAN. Press `Ctrl+C` to quit.
