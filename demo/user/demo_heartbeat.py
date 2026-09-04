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
Demo code for the host heartbeat (comm topic)

上位机心跳机制说明：
- 上位机向 comm topic 持续写入 host_heartbeat_counter 字段（写固定值即可）
- 控制器从【第一次收到】该字段开始计时
- 若超过 host_heartbeat_timeout（默认 6 秒）没有收到新的写入，
  控制器判定上位机断连，自动触发断连保护
  （常规机型进入 SERVO_OFF，M4LT2 进入高阻尼软制动）

⚠️ 注意：一旦开始发送心跳，就必须持续发送；中途停止超过 6 秒
将触发断连保护，这正是该机制的设计目的。

Run this script by:
    python demo_heartbeat.py
"""

import time

from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

HEARTBEAT_INTERVAL = 0.5  # 心跳发送间隔（秒），远小于默认 6s 超时


def demo_heartbeat():
    # 初始化 socket 客户端（自动发现机器人）
    client = SyncClientSocket()

    # 等待自动发现服务端
    print("等待连接到机器人...")
    while not client.server_discovered():
        time.sleep(0.1)

    print(f"已连接到机器人 {client.server_host}:{client.server_port}")

    print(f"开始发送心跳（间隔 {HEARTBEAT_INTERVAL}s，按 Ctrl+C 停止）...")
    counter = 0
    try:
        while True:
            # 向 comm topic 写入心跳字段，写固定值或递增计数器均可
            client.publish(key="comm", value={"host_heartbeat_counter": counter})
            counter += 1
            if counter % 10 == 0:
                print(f"已发送心跳 {counter} 次")
            time.sleep(HEARTBEAT_INTERVAL)
    except KeyboardInterrupt:
        print("停止发送心跳。注意：约 6 秒后控制器将判定上位机断连并触发保护。")
    finally:
        client.close()


if __name__ == "__main__":
    demo_heartbeat()
