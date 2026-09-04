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
Demo code for clearing robot protection flags (robot topic), using only the
Python standard library (socket), without the fourier_grx SDK.

当机器人触发过载保护（flag_robot_over_load）或力矩保护
（flag_robot_torque_protection）后，可通过 robot topic 的
clear_flag_robot_over_load / clear_flag_robot_torque_protection
字段清除对应保护标志。

Run this script by:
    python demo_clear_protection.py                # auto-discover the robot
    python demo_clear_protection.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient


def demo_clear_protection(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    # 清除过载保护 / 力矩保护标志
    message = {
        "clear_flag_robot_over_load": 1,
        "clear_flag_robot_torque_protection": 1,
    }

    print("发送消息 (robot topic):", message)
    client.publish("robot", message)

    # 等待 1s（确保消息被发送）
    time.sleep(1)

    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: clear protection flags (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_clear_protection(host=args.host)
