# Repository instructions

## Build, test, and lint

- No repository-local build, test, or lint commands are checked in. There is no `Gemfile`, `package.json`, `Makefile`, or GitHub Actions workflow in this repo.
- Single-test execution is not applicable here because there is no checked-in test harness.
- Do not invent local validation commands. For documentation changes, validate by checking:
  - Jekyll front matter consistency
  - `docs/_data/navigation.yaml` alignment with added or moved pages
  - Internal link and asset path consistency

## High-level architecture

- This repository is a **documentation site** for the Fourier-GRX-M4 SDK, not the SDK implementation itself. The docs repeatedly point to runtime files under `$HOME/fourier-grx/...` and to example code in the external `Wiki-GRx-Deploy` repository, usually on the `FourierM4` branch.
- The site is a Jekyll docs site configured in `_config.yaml` with the `just-the-docs` remote theme and plugins such as `jekyll-relative-links`, `jekyll-remote-theme`, and `jekyll-seo-tag`.
- `index.md` is the landing page. The left-side documentation structure is defined in `docs/_data/navigation.yaml`, while individual pages also carry their own front matter for title, ordering, and hierarchy.
- Content is organized around the product workflow:
  - `docs/quickstart*` for robot bring-up and environment setup
  - `docs/examples*` for runnable User/Developer examples
  - `docs/reference*` for API, config, run mode, resource, and CLI details
  - `docs/tasks*` for task/module semantics and per-task reference pages
  - `docs/usage.md`, `docs/faq.md`, `docs/update.md`, `docs/changelog.md` for operations and maintenance
- The core conceptual split across the docs is:
  - **User API**: high-level control over Zenoh topics like `fourier-grx/dynalink_interface/{comm|robot|task|grx|rehab}/{server|client}`
  - **Developer API**: lower-level Python access via `fourier_core` and `fourier_grx`, intended to run on the robot controller
- Task documentation connects multiple surfaces: physical controller input, keyboard input, User API task/component updates, and Developer API task/component calls. When editing task docs, keep those mappings consistent across `docs/tasks.md`, per-task pages, and relevant reference pages.

## Key conventions

- Most pages use YAML front matter with `layout: default`, `title`, and `nav_order`. Child pages also use `parent`. Two TOC patterns are in use — follow whichever the surrounding pages use:
  - `toc: true` with `toc_min_header`/`toc_max_header` keys **and** `* TOC\n{:toc}` in the body (only `docs/update.md` uses this)
  - `has_toc: true` in front matter (all reference and task pages); some additionally include `* TOC\n{:toc}` in the body (e.g. quickstart pages), most do not
- `nav_order` for child pages uses a decimal format (`4.1`, `4.2`, … `4.99`). Match this pattern when inserting a new child; use the next available decimal in sequence. The last item in a section often uses `.99` as a "catch-all" slot (e.g. `planner` at `4.99`).
- Internal links and assets are usually written as absolute site paths rooted at `/fourier-grx-M4/...`. Keep new links in that form unless the surrounding file clearly uses another pattern.
- The documentation language is primarily Chinese. Keep headings, navigation labels, and prose aligned with the surrounding Chinese terminology instead of introducing mixed-language sections.
- Command examples are product commands, not repo-maintenance commands. The most important recurring commands are `fourier-grx start`, `fourier-grx config`, `fourier-grx list`, `fourier-grx install`, `fourier-grx enable_service`, `fourier-grx disable_service`, and `fourier-grx setup_conda`.
- Example commands assume a Conda environment named `fourier-grx` and filesystem paths such as `$HOME/fourier-grx/...` and `$HOME/Wiki-GRx-Deploy/...`. Keep those path conventions intact when editing example snippets.
- The examples docs distinguish where code runs:
  - User examples can run on the robot controller or another machine on the same LAN
  - Developer examples must run on the robot controller for real-time access
- The docs cover two robot variants: **M4** (branch `FourierM4`) and **M4L** (branch `FourierM4L`), both in `Wiki-GRx-Deploy`. When editing variant-specific pages, confirm the correct branch is referenced.
- `_config.yaml` `aux_links` points to `Wiki-GRx-Pipeline` (the SDK pipeline repo), which is a **different** repository from `Wiki-GRx-Deploy` (the example code repo). Do not conflate them.
- When a new task page is created under `docs/tasks/`, it must also be added to `docs/_data/navigation.yaml` to appear in the sidebar. Files that exist on disk but are absent from `navigation.yaml` are silently unreachable.
- Task detail pages under `docs/tasks/` follow a repeated template: task info, module info, interface info, and update log. Preserve that structure when adding or normalizing task pages.
- Startup/configuration docs assume `~/fourier-grx/run.sh` selects the active config using `robot_type`, `robot_version`, and `run_type`. Changes to config-related docs should stay consistent with that flow.
- Watch for stale copy-paste references to `N1`, `FourierN1`, or `/fourier-grx-N1/...` inside M4 docs. When touching those sections, prefer M4-specific names, links, and branches unless the page is intentionally cross-product.

## SDK source code architecture

The SDK runtime lives at `~/fourier-grx/src/fourier_grx/` (external to this repo). This section describes its architecture so documentation can be written accurately.

### Three-layer design: Robot → Task → Algorithm

Every motion capability is split across three layers:

```
RobotBase (FSMManager)
  └── RobotReal
        └── RobotM4L
              ├── RobotM4LP1   @RobotRegistry.register(RobotName.M4LP1, RobotBackend.Real)
              └── RobotM4LT1   @RobotRegistry.register(RobotName.M4LT1, RobotBackend.Real)

RobotBase (FSMManager)
  └── RobotZenoh
        └── RobotM4LZenoh     @RobotRegistry.register(RobotName.M4LZenoh, RobotBackend.Zenoh)
```

- **Robot** (`robot/m4l/`) — hardware lifecycle: actuator init, sensor polling, emergency stop (50-cycle actuator timeout). Holds all state buffers.
- **Task** (`task/m4l/`) — FSM unit: reads peripheral inputs, drives one algorithm model, writes outputs to `DynalinkManager`.
- **Algorithm** (`algorithm/m4l/`) — stateless math: trajectory generation, gait calculation, PD control.

### Hardware: 8 joints in two groups

| Index | Group | Type | Actuator model |
|-------|-------|------|---------------|
| 0–3 | Rotary joints (leg rotation) | FSA rotary | `FSA_TYPE_60_20_120B` (P1) |
| 4–7 | Prismatic joints (leg extension) | FSA linear | `FSA_TYPE_36_11_50` (P1) |

Robot variant names: `M4L`, `M4LP1`, `M4LT1`, `M4LZenoh`. Backend values: `Real`, `Zenoh`, `Aurora`.

Actuator IPs (M4L base): left rotary `.70/.71`, right rotary `.50/.51`, left prismatic `.72/.73`, right prismatic `.52/.53`. IO board: `.131`.

### Task ID (TID) system

Tasks are identified by `IntEnum` values from menu classes in `task/menu/`:

| Range | Class | Covers |
|-------|-------|--------|
| 0–100 | `TaskMenuRobotBase` | `IDLE=1`, joint control `11–14` |
| 31–41 | `TaskMenuRobotReal` | `SERVO_ON=35`, `SERVO_OFF=36`, `CLEAR_FAULT=34`, `SERVO_REBOOT=41`, `SET_HOME=32` |
| 4000–4999 | `TaskMenuM4L` | All M4L motion tasks (see below) |
| 5000+ | `TaskMenuGRX` | Application-layer tasks |

Key `TaskMenuM4L` values used in the docs:

```
TASK_STAND_CONTROL = 4020
TASK_ROTARY_JOINT_FORWARD_WALK = 4111
TASK_ROTARY_JOINT_MARK_TIME = 4112
TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_PD = 4116
TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_PD = 4117
TASK_ROTARY_JOINT_FORWARD_WALK_ASSIST_ADJUST_DT = 4118
TASK_ROTARY_JOINT_MARK_TIME_ASSIST_ADJUST_DT = 4119
TASK_STAND_CONTROL_KNEE_RESTRICTION = 4300
TASK_ROTARY_JOINT_KNEE_RESTRICTION_FORWARD_WALK = 4301
TASK_ROTARY_JOINT_KNEE_RESTRICTION_MARK_TIME = 4302
TASK_ROTARY_JOINT_KNEE_RESTRICTION_FORWARD_WALK_ASSIST_ADJUST_PD = 4303
TASK_ROTARY_JOINT_KNEE_RESTRICTION_MARK_TIME_ASSIST_ADJUST_PD = 4304
TASK_ROTARY_JOINT_KNEE_RESTRICTION_FORWARD_WALK_ASSIST_ADJUST_DT = 4305
TASK_ROTARY_JOINT_KNEE_RESTRICTION_MARK_TIME_ASSIST_ADJUST_DT = 4306
TASK_ROTARY_JOINT_PLANNER_FORWARD_WALK = 4401
TASK_PRISMATIC_JOINT_MOVE_LENGTH = 4206
TASK_PRISMATIC_JOINT_SET_HOME = 4203
```

### Task lifecycle pattern

Every task class follows this structure (the template all docs describe):

```python
@TaskRegistry.register(RobotName.M4LP1, RobotName.M4LT1, RobotName.M4LZenoh)
class TaskM4LXxx(TaskM4LBase):
    def register(self, fsm_manager):
        self.task_model = AlgorithmM4LXxxControlModel(dt=fsm_manager.control_period)
        self.task_key = TaskMenuM4L.TASK_XXX

    def function_on_enter(self, **kwargs):   # reads joystick/keyboard/panel input
    def function_on_exit(self, **kwargs):    # writes to DynalinkManager
    def function_on_deactivate(self, **kwargs):  # calls self.task_model.reset()
    def function_standalone(self, **kwargs): # _input_buffer_normalization() → model.run() → _output_buffer_normalization()
```

FSM transition order: `on_activate` → `on_enter` → `on_tick` (loop) → `on_exit` → `on_deactivate`.

### Algorithm hierarchy (M4L)

```
AlgorithmBaseControlModel
  └── AlgorithmM4LBaseControlModel          # 8-joint buffers, PD params, configure_from_robot_param()
        ├── AlgorithmM4LRotaryJointControlModel       # indices 0-3, kp_soft/hard/buttery variants
        │     ├── AlgorithmM4LRotaryJointStandControlModel     # 5-second interpolation to [0,0,0,0]
        │     ├── AlgorithmM4LRotaryJointForwardWalkControlModel  # VHIP/FHIP gait, motion_ratio 0-1000
        │     │     ├── ...AssistAdjustPDControlModel  # adds assist_ratio 0.0-1.0
        │     │     └── ...AssistAdjustDTControlModel  # adjusts timing dt
        │     └── AlgorithmM4LRotaryJointMarkTime*     # marching-in-place variants
        └── AlgorithmM4LPrismaticJointControlModel    # indices 4-7, kp=10 kd=1
```

Gait generators used inside `ForwardWalk` and `MarkTime` algorithms: `GaitGeneratorVHIP` (virtual hip) and `GaitGeneratorFHIP` (fixed hip).

### Zenoh communication topics

Serialization: MessagePack. Priority: `REAL_TIME`. Congestion: `DROP`.

| Topic | Direction | Payload fields |
|-------|-----------|---------------|
| `fourier-grx/robot/state` | hardware → controller | `joint_position`, `joint_velocity`, `joint_effort`, `joint_current`, `imu_quat`, `imu_euler_angle`, `imu_angular_velocity`, `imu_acceleration` |
| `fourier-grx/robot/control` | controller → hardware | `position`, `velocity`, `effort`, `kp`, `kd`, `control_mode` |
| `fourier-grx/task/state` | controller → client | task state feedback |
| `fourier-grx/task/control` | client → controller | `task_command`, `component_command` |

The User API (dynalink interface) uses a separate topic namespace: `fourier-grx/dynalink_interface/{comm|robot|task|grx|rehab}/{server|client}`.

### DynalinkManager singleton

All inter-layer data flows through `DynalinkManager()` (singleton). Components relevant to M4L:

- `dynalink_robot` — joint positions/velocities (read by User API clients)
- `dynalink_task` — `flag_task_start`, `flag_task_finish`, `flag_task_pause`
- `dynalink_rehab` — `motion_ratio`, `reference_joint_position/velocity/position_max/position_min`
- `dynalink_hardware` — battery, emergency stop state

Tasks write to `dynalink_rehab` in `function_on_exit()`; User API clients read these values to display rehabilitation progress.

### Control system

- **Default control period**: `0.02 s` (50 Hz). Configurable via `robot.control_period` in YAML config.
- **SDK/Developer mode**: 400 Hz default.
- **Scheduling**: `ischedule` module for deterministic loop timing.
- **Modes**: `play_mode` (normal operation), `debug_mode` (enhanced logging), `developer_mode` (direct joint access), `sdk_mode` (headless SDK).

### Config file keys (M4L)

Loaded via `fourier-grx start --config <path>`. Key fields:

```yaml
robot:
  name: "M4LP1"          # M4L | M4LP1 | M4LT1 | M4LZenoh
  backend: "Real"        # Real | Zenoh | Aurora
  control_period: 0.02
peripheral:
  use_joystick: true
  joystick_type: "XBOX"  # XBOX | PS4 | PS5
  use_virtual_panel: false
zenoh:
  authentication: false
resource:
  path: "~/fourier-grx/resource/m4l"
```

### FSM input controls

Joystick (task selection): `L1` → next/prev task, `L2` double-click → execute, `Share` → reverse direction. Shortcuts: `triangle/square/circle/cross` → robot-specific quick-access tasks (e.g. M4LP1: `esc`→SERVO_OFF, `square`→STAND_CONTROL, `triangle`→FORWARD_WALK).

Keyboard: `Up/Down` → select task, `Enter` → execute, `F1–F4`/`ESC` → shortcuts.
