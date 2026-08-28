---
layout: default
title: Communication Interface
nav_order: 3.0
parent: Reference Guide
has_toc: true
nav_exclude: true
---

# Communication Interface

* TOC
{:toc}

This page describes the communication mechanism used by the Fourier-GRX-M4 SDK User API, including the underlying protocol, auto-discovery flow, data model, and configuration options.

---

## Architecture Overview

Communication follows a **server / client** model:

```
┌───────────────────────────────────┐       LAN (UDP)          ┌───────────────────────────────────┐
│        Robot Main Board           │  ─── State Data ────►    │       User Computer (SDK)          │
│        (SyncServer)               │  ◄── Control Cmds ────   │      (SyncClientSocket)            │
│                                   │                          │                                   │
│  • Broadcasts own IP:Port (9527)  │                          │  • Listens for broadcast,          │
│  • Publishes robot state (50 Hz)  │                          │    auto-discovers server           │
│  • Receives control commands      │                          │  • Receives state, sends commands  │
└───────────────────────────────────┘                          └───────────────────────────────────┘
```

- **Server**: `fourier-grx` runs on the robot's main board, starts `SyncServerSocket`, continuously pushes robot state to known clients, and receives control commands from them.
- **Client**: On the user's computer (or any host on the same LAN), instantiate `SyncClientSocket` via the Fourier-GRX-M4 SDK to exchange data bidirectionally.

---

## Transport Layer

| Property            | Value                              |
|---------------------|------------------------------------|
| Network protocol    | UDP (connectionless, low-latency)  |
| Serialization       | [msgpack](https://msgpack.org/)    |
| Data port           | `5566` (server listens)            |
| Auto-discovery port | `9527` (broadcast port)            |
| Max packet size     | 65,507 bytes (UDP theoretical max) |
| Default period      | 20 ms (50 Hz), configurable        |

> ℹ️ **Note**: UDP does not guarantee packet ordering or delivery. On a wired LAN with sufficient bandwidth, packet loss is typically negligible.

---

## Auto-Discovery Flow

After startup, the server broadcasts a msgpack packet containing its `IP` and `Port` to the LAN broadcast address (`255.255.255.255:9527`) approximately **once per second** in a background thread.

The client binds to a random local port and starts a background thread listening on broadcast port `9527`. As soon as the first broadcast packet is received, discovery is complete; all subsequent data is exchanged on the data port `5566`.

```
Server                          Client
  │                               │
  │── broadcast {host, port} ────►│  (every ~1 s, port 9527)
  │                               │  server discovered
  │◄────── control cmds (UDP 5566)│
  │──────► state data  (UDP 5566)─│
  │                               │
```

If the robot's IP is known and fixed, you can skip auto-discovery by passing `server_host` and `server_port` directly:

```python
from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

client = SyncClientSocket(
    server_host="192.168.1.100",
    server_port=5566,
    auto_discover=False,
)
```

---

## Topics and Data Direction

Communication is organized into 6 topic keys:

| Topic Key | Direction           | Description                                      |
|-----------|---------------------|--------------------------------------------------|
| `comm`    | Bidirectional       | Communication status and heartbeat               |
| `core`    | Server → Client     | Low-level core state (raw joint sensor data, etc.) |
| `robot`   | Server → Client     | Robot motion state (joint position/velocity/torque, etc.) |
| `task`    | Bidirectional       | Task state and task control commands             |
| `grx`     | Bidirectional       | fourier-grx generic robot data (mainly humanoid) |
| `rehab`   | Bidirectional       | Rehabilitation robot-specific data               |

**Data direction notes**:
- **Server → Client**: Current robot state, serialized via `read_to_dict()` / deserialized via `read_from_dict()`.
- **Client → Server**: Control commands, serialized via `write_to_dict()` / deserialized via `write_from_dict()`.

For per-topic field details, see the [User API Reference](/fourier-grx-M4/docs/en/reference/user).

---

## Heartbeat and Disconnect Protection

The `comm` topic includes a host heartbeat detection mechanism that automatically protects the robot when communication between the controller and the host is lost.

### How It Works

1. **Host continuously writes the heartbeat field**

   The client must write the `host_heartbeat_counter` field to the server's `comm` topic every communication cycle:

   ```python
   write_dict = {
       "comm": {
           "host_heartbeat_counter": 1,  # any fixed value or incrementing counter
       }
   }
   ```

   - The controller treats each received `host_heartbeat_counter` write as a valid heartbeat and refreshes its internal timer.
   - Writing a fixed value (e.g., always `1`) is sufficient; an incrementing counter makes it easier to verify that fresh data is arriving.

2. **Controller detects timeout**

   - The read-only field `host_heartbeat_timeout` is the timeout threshold, defaulting to **6.0 s**.
   - If no new `host_heartbeat_counter` write is received within `host_heartbeat_timeout`, the controller judges the host as disconnected.
   - On disconnect, `host_heartbeat_connection_lost` is set to `SET` and an emergent stop is triggered:
     - Standard robots: task switches to `TASK_SERVO_OFF`.
     - M4LT2: task switches to the high-damping task for soft braking.

3. **HEART_BEAT command compatibility**

   The `HEART_BEAT` command sent via the HEX protocol (ports 4196/4197) also refreshes the heartbeat timer, sharing the same timeout detection logic as the `comm` topic heartbeat.

### Related Fields

| Field | Direction | Description |
|-------|-----------|-------------|
| `host_heartbeat_counter` | Client → Server | Heartbeat counter; keep writing to maintain connection |
| `host_heartbeat_timeout` | Server → Client | Timeout threshold in seconds; default 1.0 s |
| `host_heartbeat_connection_lost` | Server → Client | Disconnect flag; `SET` means timeout occurred |
| `flag_ethernet_connect_status` | Server → Client | Ethernet connection status; set to `SET` on heartbeat |

---

## Configuration Parameters

In the `fourier-grx` configuration file (typically under `~/.fourier/fourier-grx/config/`), two blocks control communication behavior:

```yaml
# Controls whether SyncServer starts and the communication period
communication:
  enable: true        # true = start the communication server
  type: "socket"      # backend type; standard M4L uses "socket"
  period: 0.02        # publish period in seconds (default: 0.02 s = 50 Hz)

# Controls whether the SyncClient subprocess starts
sync:
  enable: true        # true = start the internal sync subprocess
  period: 0.02        # subprocess publish period in seconds
```

> ⚠️ **Note**: Both `communication.enable` and `sync.enable` must be set to `true` for communication to work. Both are enabled by default only in **Developer Mode**.

---

## Network Recommendations

| Recommendation                               | Details                                                  |
|----------------------------------------------|----------------------------------------------------------|
| Use a wired Ethernet connection              | Most stable, lowest latency                              |
| Avoid using both wired and wireless adapters | Dual NICs can cause routing conflicts that affect discovery and data delivery |
| Ensure robot and computer are on the same subnet | Broadcast packets do not cross routers; cross-subnet auto-discovery will fail |
| Disable firewall or open the required ports  | UDP 5566 (data), UDP 9527 (broadcast)                    |
