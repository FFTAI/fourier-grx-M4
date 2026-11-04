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
| `version`         | Display the SDK version plus provenance (branch, variant, release class, commit, build time)       |
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

Since **v4.4.77** the version list comes from the release index `grx/manifest.json` on the server (maintained by `scripts/release_meta.py` in the repository), and the downloaded file is verified against the `sha256` recorded there — a mismatch aborts the installation.

### Usage

```bash
fourier-grx update                        # List newer versions from the release index and install interactively
fourier-grx update <version>              # Install a specific version; the variant is read from the installed package
fourier-grx update <version>-<channel>    # Install a specific channel build, e.g. 4.4.53-prerelease
fourier-grx update --help                 # Show help information
```

The variant is the package's platform/model identifier (the deb `X-Variant` field), e.g. `linux-arm64-cpu-m4l-blaze`. It is supplied automatically by the installed package and never needs to be typed.

### Where the version list comes from

- **Release index (since v4.4.77)**: `grx/manifest.json` is fetched once and carries every published version of this variant together with its release class and `sha256`. Entries are listed in ascending version order with no window limit.
- **Fallback probing (when the index is unavailable)**: if the index cannot be fetched (offline, older server), the client falls back to HTTP HEAD probing version by version — `patch + 1` through `patch + 20` of the current minor version (stopping after 5 consecutive 404s), `minor + 1` (patch 0-10, stop after 3), and `minor 0` of `major + 1` (patch 0-5, stop after 3). Because of that window, some later patch versions may stay invisible to a device sitting on an old release; this is a known limitation of the fallback path only.
- When the index reports nothing newer, the client additionally spot-checks the immediately next version number with one HEAD request, in case a package was uploaded without updating the index.

### Workflow

1. Reads the currently installed version number and variant from the deb record
2. Fetches the release index and collects all versions of this variant that are newer than the installed one, together with their `sha256`
3. Falls back to version-by-version probing if the index is unavailable
4. Lists the candidates, marking the latest one and each entry's release class
5. Prompts the user to select a version number (press Enter to install the latest version, enter `n` to cancel)
6. Downloads the `.deb` package for the selected version and verifies its `sha256`
7. Completes the installation with `sudo dpkg -i`

### Example Output

```text
Current version : 4.4.71
Current variant  : linux-arm64-cpu-m4l-blaze
Checking for updates...

Found the following newer versions:
----------------------------------------------------
  [1] v4.4.72  fourier-grx-4.4.72-linux-arm64-cpu-m4l-blaze.deb  [正式版本 · 长期支持]
  [2] v4.4.73  fourier-grx-4.4.73-linux-arm64-cpu-m4l-blaze.deb  [内测构建]
  [3] v4.4.74  fourier-grx-4.4.74-linux-arm64-cpu-m4l-blaze.deb  [内测构建]
  [4] v4.4.75  fourier-grx-4.4.75-linux-arm64-cpu-m4l-blaze.deb  [内测构建]
  [5] v4.4.76  fourier-grx-4.4.76-linux-arm64-cpu-m4l-blaze.deb  [内测构建]
  [6] v4.4.77  fourier-grx-4.4.77-linux-arm64-cpu-m4l-blaze.deb  [内测构建]  ← latest
----------------------------------------------------

Select the version number to install (press Enter for latest [6], or n to cancel):
```

标签为中文输出：`[正式版本 · 长期支持]` = official release, long-term supported；`[内测构建]` = internal build；`[预发布]` = pre-release. After you pick a version the client prints `Downloading: …`, then `checksum ok: <sha256>` and `Installing: …`. If the index has no `sha256` for that release (older packages), it prints a note saying verification is skipped and continues.

### After Installation Completes

Run `fourier-grx install` to update the deployment layer — see [The Two Layers of Installation](#the-two-layers-of-installation) above.

### Pre-release Channel

Pre-release builds carry `prerelease` instead of `blaze` as the last segment of both the file name and the `X-Variant`, keeping the model segment unchanged — e.g. `fourier-grx-4.4.53-linux-arm64-cpu-m4l-prerelease.deb`. A `blaze` suffix identifies the delivery channel, not official status; only 4.4.40, 4.4.43, and 4.4.72 are official releases.

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

## `fourier-grx version` Detailed Instructions

Since **v4.4.78** the command also prints the provenance fields carried by the package:

```text
version: 4.4.78
branch:  m4-lfs
variant: linux-arm64-cpu-m4l-blaze
release: beta（内测构建 internal build）
commit:  1127cfbbd4fa-clean
built:   2026-11-04T03:27:13Z
```

| Field | Meaning |
|-------|---------|
| `version` | dpkg package version |
| `branch` | Branch the build was made from |
| `variant` | Platform / model / build type; decides which packages `fourier-grx update` matches |
| `release` | Release type: `stable` (official, long-term supported), `beta` (internal build), `prerelease` |
| `commit` | 12-character commit id; a `-dirty` suffix means the working tree had uncommitted changes, such packages must not be shipped |
| `built` | Build time (UTC) |

The values come from the deb metadata, so `dpkg -s fourier-grx` shows the same information. Packages from 4.4.77 and earlier lack `X-Release-Class` / `X-Commit`; the command then prints only what exists plus a note about the older package. If fourier-grx was not installed with dpkg it prints an error and exits non-zero.

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
