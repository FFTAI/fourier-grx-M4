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
Demo code for reading robot state, using only the Python standard library
(socket), without the fourier_grx SDK.

机器人（服务端）只会向"发过至少一个包"的客户端推送状态，
因此本示例先发送一个空的 task 写包注册客户端地址。

注册之后服务端每个通信周期都会推送 5 个 topic 各一个包（默认 50Hz，
即约 250 包/秒），所以必须持续把 socket 缓冲区读空，否则打印出来的
永远是几秒前的旧数据。本示例的做法是：不停接收，但最多每 0.5 秒打印一次。

Run this script by:
    python demo_get_state.py                # auto-discover the robot
    python demo_get_state.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient

PRINT_INTERVAL = 0.5  # 状态打印间隔（秒）


def demo_get_state(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    # 发送一个空写包，让服务端记录本客户端地址，之后才会收到状态推送
    client.publish("task", {})

    print("接收机器人状态（按 Ctrl+C 退出）...")
    last_print_time = 0.0
    latest = {}  # topic -> data，保存每个 topic 最新收到的一包
    try:
        while True:
            # 用很短的超时持续接收，把缓冲区里的积压包快速读完
            result = client.receive(timeout=0.05)
            if result is None:
                continue

            key, data = result
            if key is not None:
                latest[key] = data

            now = time.time()
            if now - last_print_time < PRINT_INTERVAL:
                continue
            last_print_time = now

            task = latest.get("task", {})
            comm = latest.get("comm", {})
            print(f"[task] robot_task_state = {task.get('robot_task_state')}, "
                  f"flag_task_running = {task.get('flag_task_running')}")
            print(f"[comm] host_heartbeat_connection_lost = {comm.get('host_heartbeat_connection_lost')}, "
                  f"flag_ethernet_connect_status = {comm.get('flag_ethernet_connect_status')}")
    except KeyboardInterrupt:
        pass
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: get robot state (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_get_state(host=args.host)
