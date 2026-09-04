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
Demo code for the host heartbeat, using only the Python standard library
(socket), without the fourier_grx SDK.

上位机心跳机制说明：
- 上位机向 comm topic 持续写入 host_heartbeat_counter 字段（写固定值即可）
- 控制器从【第一次收到】该字段开始计时
- 若超过 host_heartbeat_timeout（默认 6 秒）没有收到新的写入，
  控制器判定上位机断连，自动触发断连保护
  （常规机型进入 SERVO_OFF，M4LT2 进入高阻尼软制动）

⚠️ 注意：一旦开始发送心跳，就必须持续发送；中途停止超过 6 秒
将触发断连保护，这正是该机制的设计目的。

Run this script by:
    python demo_heartbeat.py                # auto-discover the robot
    python demo_heartbeat.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient

HEARTBEAT_INTERVAL = 0.5  # 心跳发送间隔（秒），远小于默认 6s 超时


def demo_heartbeat(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    print(f"开始发送心跳（间隔 {HEARTBEAT_INTERVAL}s，按 Ctrl+C 停止）...")
    counter = 0
    try:
        while True:
            client.send_heartbeat(counter)
            counter += 1
            if counter % 10 == 0:
                print(f"已发送心跳 {counter} 次")
            time.sleep(HEARTBEAT_INTERVAL)
    except KeyboardInterrupt:
        print("停止发送心跳。注意：约 6 秒后控制器将判定上位机断连并触发保护。")
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: host heartbeat (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_heartbeat(host=args.host)
