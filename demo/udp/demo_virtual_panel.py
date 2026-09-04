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
Demo code for virtual panel control (grx topic), using only the Python
standard library (socket), without the fourier_grx SDK.

虚拟面板（virtual panel）是 fourier-grx 提供的通用输入通道，
行走任务（TASK_WALK = 965）中的典型用法：
- virtual_panel_command_param_1: 步长（米）
- virtual_panel_command_param_2: 行走速度（米/秒）
- virtual_panel_command_start:   开始运动（电平有效，True 期间持续行走）
- virtual_panel_command_stop:    停止运动

注意：
- 使用前请确认机器人已使能（servo on）
- 默认 release 配置已开启 use_virtual_panel: true

Run this script by:
    python demo_virtual_panel.py                # auto-discover the robot
    python demo_virtual_panel.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient, TASK_WALK


def demo_virtual_panel(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    # --------------------------------------------------
    # 1. 启动行走任务
    print(f"发送任务指令: TASK_WALK ({TASK_WALK})")
    client.send_task_command(TASK_WALK)
    time.sleep(1)

    # --------------------------------------------------
    # 2. 通过虚拟面板设置步长 / 速度并开始行走
    client.publish("grx", {
        "virtual_panel_command_param_1": 0.10,  # 步长 0.1 m
        "virtual_panel_command_param_2": 0.10,  # 行走速度 0.1 m/s
        "virtual_panel_command_start": True,
    })
    print("开始行走：步长 0.1 m，速度 0.1 m/s")

    # 行走 5 秒
    time.sleep(5)

    # --------------------------------------------------
    # 3. 停止行走
    client.publish("grx", {
        "virtual_panel_command_start": False,
        "virtual_panel_command_stop": True,
    })
    print("停止行走")

    time.sleep(1)

    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: virtual panel walk control (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_virtual_panel(host=args.host)
