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
Demo code for clearing robot protection flags (robot topic)

当机器人触发过载保护（flag_robot_over_load）或力矩保护
（flag_robot_torque_protection）后，可通过 robot topic 的
clear_flag_robot_over_load / clear_flag_robot_torque_protection
字段清除对应保护标志。

Run this script by:
    python demo_clear_protection.py
"""

import time

from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket


def demo_clear_protection():
    # 初始化 socket 客户端（自动发现机器人）
    client = SyncClientSocket()

    # 等待自动发现服务端
    print("等待连接到机器人...")
    while not client.server_discovered():
        time.sleep(0.1)

    print(f"已连接到机器人 {client.server_host}:{client.server_port}")

    # 构建消息：清除过载保护 / 力矩保护标志
    message = {
        "clear_flag_robot_over_load": 1,
        "clear_flag_robot_torque_protection": 1,
    }

    print("发送消息:", message)

    # 发布消息到 robot topic
    client.publish(key="robot", value=message)

    # 等待 1s（确保消息被发送）
    time.sleep(1)

    client.close()


if __name__ == "__main__":
    demo_clear_protection()
