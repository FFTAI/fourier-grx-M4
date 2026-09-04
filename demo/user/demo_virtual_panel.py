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
Demo code for virtual panel control (grx topic)

虚拟面板（virtual panel）是 fourier-grx 提供的通用输入通道，
行走任务中的典型用法：
- virtual_panel_command_param_1: 步长（米）
- virtual_panel_command_param_2: 行走速度（米/秒）
- virtual_panel_command_start:   开始运动（电平有效，True 期间持续行走）
- virtual_panel_command_stop:    停止运动

注意：
- 使用前请确认机器人已使能（servo on）并已进入行走任务
- 默认 release 配置已开启 use_virtual_panel: true

Run this script by:
    python demo_virtual_panel.py
"""

import time

from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

import fourier_grx.sdk.user as fourier_grx


def demo_virtual_panel():
    # 初始化 socket 客户端（自动发现机器人）
    client = SyncClientSocket()

    # 等待自动发现服务端
    print("等待连接到机器人...")
    while not client.server_discovered():
        time.sleep(0.1)

    print(f"已连接到机器人 {client.server_host}:{client.server_port}")

    # --------------------------------------------------
    # 1. 启动行走任务
    client.publish(key="task", value={
        "robot_task_command": fourier_grx.TaskCommand.TASK_WALK,
        "flag_task_command_update": True,
    })
    time.sleep(1)

    # --------------------------------------------------
    # 2. 通过虚拟面板设置步长 / 速度并开始行走
    client.publish(key="grx", value={
        "virtual_panel_command_param_1": 0.10,  # 步长 0.1 m
        "virtual_panel_command_param_2": 0.10,  # 行走速度 0.1 m/s
        "virtual_panel_command_start": True,
    })
    print("开始行走：步长 0.1 m，速度 0.1 m/s")

    # 行走 5 秒
    time.sleep(5)

    # --------------------------------------------------
    # 3. 停止行走
    client.publish(key="grx", value={
        "virtual_panel_command_start": False,
        "virtual_panel_command_stop": True,
    })
    print("停止行走")

    time.sleep(1)

    client.close()


if __name__ == "__main__":
    demo_virtual_panel()
