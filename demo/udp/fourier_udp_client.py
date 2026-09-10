"""
Copyright (C) [2024] [Fourier Intelligence Ltd.]

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

--------------------------------------------------
Minimal UDP client for the fourier-grx sync socket protocol, implemented with
only the Python standard library (socket) plus the local mini_msgpack codec.

Protocol summary (UDP + MessagePack):

- The robot (server) listens on UDP port 5566.
- The robot broadcasts {"host": <ip>, "port": 5566} to 255.255.255.255:9527
  about once per second (auto discovery).
- Client -> robot packet: {"key": <topic>, "data": {...writable fields...}}
- Robot -> client packets: {"key": <topic>, "data": {...readable fields...}},
  pushed at ~50 Hz to every client that has sent at least one packet
  (the server learns client addresses from incoming packets).

Topics: "comm", "robot", "task", "grx", "rehab"

Commonly used task topic fields (client -> robot):
    robot_task_command       int   task id, e.g. 35 = TASK_SERVO_ON
    flag_task_command_update int   1 = apply the command above

Comm topic heartbeat field (client -> robot):
    host_heartbeat_counter   int   keep writing to hold the connection;
                                   once started, stopping for more than
                                   host_heartbeat_timeout (default 6 s)
                                   triggers the disconnect protection
"""

import os
import socket
import sys
import threading

# allow running the demos from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mini_msgpack import packb, unpackb

SERVER_PORT = 5566          # fourier-grx sync server data port
BROADCAST_PORT = 9527       # auto-discovery broadcast port
MAX_PACKET_SIZE = 65507     # UDP theoretical max payload
HEARTBEAT_INTERVAL = 0.5    # seconds; well below the default 6 s timeout

# task commands (fourier-grx task menu values)
TASK_CLEAR_FAULT = 34
TASK_SERVO_ON = 35
TASK_SERVO_OFF = 36
TASK_SERVO_REBOOT = 41
TASK_WALK = 965                          # TASK_APPLICATION_WALK_MOTION_CONTROL
TASK_ROTARY_JOINT_FORWARD_WALK = 4111


class FourierUdpClient:
    """Tiny UDP client for the fourier-grx sync socket protocol."""

    def __init__(self, host: str = None, port: int = SERVER_PORT,
                 broadcast_port: int = BROADCAST_PORT, discover_timeout: float = 5.0):
        """
        :param host: robot IP; None means auto-discover via the broadcast port
        :param port: robot sync server port (default 5566)
        """
        if host is None:
            host, port = self._discover(broadcast_port, discover_timeout)

        self.server_addr = (host, port)

        self._send_lock = threading.Lock()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("", 0))  # any local port

    @staticmethod
    def _discover(broadcast_port: int, timeout: float):
        """Listen for the robot's broadcast and return (host, port)."""
        print(f"等待机器人广播（UDP {broadcast_port}）...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(timeout)
        try:
            sock.bind(("", broadcast_port))
            data, _ = sock.recvfrom(2048)
        except socket.timeout:
            raise TimeoutError(
                f"没有在 {timeout}s 内收到机器人广播，"
                f"请确认机器人在线且与本机在同一局域网，或使用 --host 直接指定机器人 IP"
            )
        finally:
            sock.close()

        info = unpackb(data)
        return info["host"], info["port"]

    def publish(self, key: str, data: dict):
        """Send one {"key": key, "data": data} packet to the robot."""
        packet = packb({"key": key, "data": data})
        with self._send_lock:
            self._socket.sendto(packet, self.server_addr)

    def receive(self, timeout: float = 1.0):
        """
        Receive one state packet from the robot.

        :return: (key, data) tuple, or None on timeout
        """
        self._socket.settimeout(timeout)
        try:
            body, _ = self._socket.recvfrom(MAX_PACKET_SIZE)
        except socket.timeout:
            return None
        packet = unpackb(body)
        return packet.get("key"), packet.get("data")

    def send_task_command(self, task_command: int):
        """Send a task command to the robot (task topic)."""
        self.publish("task", {
            "robot_task_command": task_command,
            "flag_task_command_update": 1,
        })

    def send_heartbeat(self, counter: int = 1):
        """Write the host heartbeat field (comm topic)."""
        self.publish("comm", {"host_heartbeat_counter": counter})

    def close(self):
        self._socket.close()


class HeartbeatSender:
    """
    Background sender for comm.host_heartbeat_counter.

    Starting the sender arms the robot's disconnect timer. Stopping it does not
    disarm that timer: after host_heartbeat_timeout (default 6 s), the robot
    intentionally triggers its disconnect protection.
    """

    def __init__(self, client: FourierUdpClient, interval: float = HEARTBEAT_INTERVAL):
        if interval <= 0:
            raise ValueError("heartbeat interval must be positive")
        self._client = client
        self._interval = interval
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread is not None:
            return self
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        if self._thread is None:
            return
        self._stop_event.set()
        self._thread.join(timeout=self._interval + 0.2)
        self._thread = None

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        return False

    def _run(self):
        counter = 0
        while not self._stop_event.is_set():
            try:
                self._client.send_heartbeat(counter)
            except OSError:
                break
            counter += 1
            self._stop_event.wait(self._interval)
