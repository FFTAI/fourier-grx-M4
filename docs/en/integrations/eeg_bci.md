---
layout: default
title: EEG / BCI Integration Example
parent: Device Integration
nav_order: 5.71
has_toc: true
nav_exclude: true
---

# EEG / BCI Integration Example

* TOC
{:toc}

This page describes two practical integration paths:

1. **M4 upper-computer EEG mode**: the EEG device acts as a TCP server and the M4 upper computer connects as a TCP client.
2. **Custom BCI decoder → User API**: a Python decoder communicates with `fourier-grx` over UDP.

> ⚠️ **Important boundaries**
>
> - This is a research / engineering example, **not** a registered medical feature or a claim of efficacy.
> - This repository does not include EEG acquisition, artifact rejection, or classification algorithms.
> - Before patient use, complete ethics approval, informed consent, risk assessment, and institutional validation.
> - When the EEG signal is unstable or decoder confidence is low, stop the robot rather than repeating the last command.
> - The hardware emergency stop must be independent of the BCI software and upper computer.

## 1. Which path?

| Path | Use case | Advantages | Limits |
|------|----------|------------|--------|
| M4 upper-computer EEG mode | Existing m4-electron deployment; EEG team only implements TCP server | Fixed protocol, existing training UI and reports | Requires the external-device entry to be enabled; mapping is defined by the upper computer |
| Custom BCI → User API | Research algorithms, custom decoding, experimental protocols | Flexible; can record and replace the decoder | You must handle connection, heartbeat, tasks, safety, and logging |

## 2. Path 1: M4 upper-computer EEG TCP protocol

### 2.1 Network and encoding

| Item | Example | Notes |
|------|---------|-------|
| EEG device IP | `192.168.31.122` | Use the site configuration |
| EEG listen port | `7070` | Use the site configuration |
| Transport | TCP | Long-lived connection |
| Encoding | NDJSON | One JSON object per line, UTF-8, `\n` terminated |
| Heartbeat | M4 sends `ping` every 3 s | EEG replies `pong` immediately |
| Disconnect | No `pong` for 10 s | M4 reconnects |

> ℹ️ Some M4 upper-computer builds hide “External Device Connection” by default. Enable `showExternalDeviceConnection` in `feature-config.json` or use the build delivered for the site.

### 2.2 Messages

| Direction | `type` | Purpose |
|-----------|--------|---------|
| M4 → EEG | `ping` | Heartbeat |
| EEG → M4 | `pong` | Heartbeat reply |
| M4 → EEG | `command` + `cmd: start` | Training start with `user_id` |
| M4 → EEG | `command` + `cmd: stop` | Training stop; connection stays open |
| EEG → M4 | `eeg_stream` | 2 Hz `value` in [0, 100] |
| EEG → M4 | `threshold_update` | Walk / stand thresholds |

### 2.3 Sequence

```text
M4 upper computer                         EEG device (TCP server)
    │                                          │
    │──── TCP connect ────────────────────────→│
    │──── ping ───────────────────────────────→│
    │←─── pong ────────────────────────────────│
    │──── {"cmd":"start","user_id":"U10086"} ─→│
    │←─── threshold_update ────────────────────│  immediate
    │←─── eeg_stream {"value":45} ─────────────│  every 500 ms
    │←─── eeg_stream {"value":52} ─────────────│
    │←─── threshold_update (changed) ──────────│
    │──── {"cmd":"stop"} ─────────────────────→│  stop stream, keep TCP
    │──── ping / pong ────────────────────────→│
    │──── TCP disconnect ─────────────────────→│
```

### 2.4 Message examples

```json
{"type":"command","cmd":"start","user_id":"U10086","ts":1745123456789}
{"type":"command","cmd":"stop","ts":1745123456789}
{"type":"eeg_stream","ts":1745123456789,"value":73}
{"type":"threshold_update","ts":1745123456789,"walk_threshold":65,"stand_threshold":40}
```

### 2.5 Control mapping

- `value > walk_threshold`: start walking;
- `value < stand_threshold`: stop walking, remain standing;
- thresholds are in [0, 100]; out-of-range values are clipped;
- after `start`, send the current threshold once, then stream every 500 ms;
- after `stop`, stop streaming but keep the connection and heartbeat alive.

This is an upper-computer control policy. It does not mean the EEG value equals movement intent strength. Therapists / researchers must set thresholds for the individual and retain manual stop authority.

### 2.6 EEG-side checklist

- [ ] TCP server on the configured port; one active connection;
- [ ] one JSON object per line, UTF-8, `\n` terminated;
- [ ] `ts` in Unix milliseconds on every message;
- [ ] reply `pong` within 3 s;
- [ ] after `start`, send threshold once, then 2 Hz stream;
- [ ] after `stop`, stop streaming without disconnecting;
- [ ] keep values in [0, 100];
- [ ] after disconnect, resume listening;
- [ ] log raw EEG, decoder output, thresholds, and send events.

## 3. Path 2: custom BCI → User API

### 3.1 Architecture

```text
EEG cap / amplifier
      │
      ▼
acquisition + decoder (LSL / BrainFlow / vendor SDK)
      │  motor imagery / SSVEP / other features
      ▼
command mapper (confidence, debounce, rate limit, timeout)
      │  high-level commands
      ▼
User API (SyncClientSocket, UDP 5566)
      │
      ▼
fourier-grx: task / virtual panel / virtual joystick
      │
      ▼
M4L robot
```

Feedback may be visual, auditory, or haptic. Feedback latency and jitter affect BCI performance and should be recorded.

### 3.2 Recommended mapping

| BCI output | Recommended command | Avoid |
|------------|---------------------|-------|
| Start / stop | `task` topic | Direct joint torque |
| Assist up / down | `grx` virtual panel | Writing PD gain arrays |
| Left / right | `grx` virtual joystick | Direct joint position |
| Emergency stop | `TASK_SERVO_OFF` + hardware e-stop | Stopping only the decoder |

BCI should map intent to high-level commands; trajectory generation, limits, and protection remain in `fourier-grx`.

### 3.3 Minimal Python skeleton

```python
import threading
import time

import fourier_grx.sdk.user as fourier_grx
from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

client = SyncClientSocket()
while not client.server_discovered():
    time.sleep(0.1)

def heartbeat():
    counter = 0
    while True:
        client.publish(key="comm", value={"host_heartbeat_counter": counter})
        counter += 1
        time.sleep(0.5)

threading.Thread(target=heartbeat, daemon=True).start()

client.publish(key="task", value={
    "robot_task_command": fourier_grx.TaskCommand.TASK_WALK,
    "flag_task_command_update": True,
})
time.sleep(1)

client.publish(key="grx", value={
    "virtual_panel_command_param_1": 0.20,
    "virtual_panel_command_param_2": 0.20,
    "virtual_panel_command_start": True,
})

try:
    while True:
        time.sleep(0.1)
        # Read decoder output; apply confidence, debounce, and rate limits
except KeyboardInterrupt:
    client.publish(key="grx", value={
        "virtual_panel_command_start": False,
        "virtual_panel_command_stop": True,
    })
    client.publish(key="task", value={
        "robot_task_command": fourier_grx.TaskCommand.TASK_SERVO_OFF,
        "flag_task_command_update": True,
    })
    client.close()
```

> ⚠️ This skeleton omits confidence filtering, command timeout, rate limiting, state checks, and recovery. It is not production code. Use `demo/user/demo_virtual_panel.py` and `demo/user/demo_heartbeat.py` as validated starting points.

### 3.4 Required safety mechanisms

- confidence threshold;
- N consecutive consistent windows;
- command timeout / automatic stop;
- rate limiting for assist, speed, and direction;
- dead-man switch;
- independent hardware emergency stop;
- state gating: calibrated, standing, no protection, no fault;
- two-person operation with therapist/engineer takeover;
- logging of raw signal, decoder output, commands, robot state, and e-stop events.

## 4. Timing, synchronization, and logging

- record the start/end of each decoding window;
- record task commands, state packets, and `ts` on the robot side;
- align clocks or log clock offset;
- mark visual/auditory feedback events for offline alignment;
- measure end-to-end latency: acquisition → decoding → send → robot;
- count packet loss, reordering, reconnects, and rejected commands;
- do not treat the 2 Hz `eeg_stream` as the raw EEG sample rate.

## 5. Validation sequence

1. Offline decoding with recorded data;
2. Mock EEG / mock robot for protocol, heartbeat, and disconnect;
3. Robot suspended / no load; observe task switching only;
4. Low assist, short duration, supervised;
5. Increase complexity only after the previous step is stable.

Record success rate, false-trigger rate, latency, reconnects, stop reasons, and subjective workload.

## 6. Troubleshooting

| Symptom | Check first |
|---------|-------------|
| Upper computer cannot connect | IP/port, TCP server listening, firewall, single connection |
| No data after connect | `start` received, threshold sent first, 500 ms stream |
| Frequent disconnects | `pong` within 10 s, packet loss, complete JSON lines |
| Robot ignores BCI | heartbeat, task registration, protection/e-stop override, run mode |
| Motion does not match intent | thresholds, debounce, mapping, virtual-panel latching, task switched |
| Report missing data | `rehab` fields, firmware support, correct task |

## Related pages

- [Communication Interface](/fourier-grx-M4/docs/en/reference/communication)
- [User API](/fourier-grx-M4/docs/en/reference/user)
- [Runtime Architecture](/fourier-grx-M4/docs/en/reference/runtime_architecture)
- [Task Lifecycle and Switching](/fourier-grx-M4/docs/en/reference/task_lifecycle)
- [Examples](/fourier-grx-M4/docs/en/examples)
