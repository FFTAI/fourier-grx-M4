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

所需 fourier-grx 配置（示例片段）：

communication:
  enable: true
  period: 0.02
  type: "socket"

peripheral:
  use_virtual_panel: true

注意：
- 使用前请确认机器人已使能（servo on）
- 默认 release 配置已开启 use_virtual_panel: true
- 本示例运行期间会发送上位机心跳；示例退出后心跳停止，
  约 6 秒后控制器会按设计触发断连保护

Run this script by:
    python demo_virtual_panel.py                # auto-discover the robot
    python demo_virtual_panel.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient, HeartbeatSender, TASK_WALK

WALK_DURATION = 5.0       # seconds
STEP_LENGTH = 0.20        # meters; valid range [0.20, 0.80]
WALK_SPEED = 0.20         # meters/second; valid range [0.10, 1.20]


def demo_virtual_panel(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    try:
        with HeartbeatSender(client):
            # --------------------------------------------------
            # 1. 启动行走任务
            print(f"发送任务指令: TASK_WALK ({TASK_WALK})")
            client.send_task_command(TASK_WALK)
            time.sleep(1)

            # --------------------------------------------------
            # 2. 通过虚拟面板设置步长 / 速度并开始行走
            #    demo 使用较小值，便于安全验证
            walking = False
            try:
                client.publish("grx", {
                    "virtual_panel_command_param_1": STEP_LENGTH,
                    "virtual_panel_command_param_2": WALK_SPEED,
                    "virtual_panel_command_start": True,
                    "virtual_panel_command_stop": False,
                    "virtual_panel_command_pause": False,
                })
                walking = True
                print(f"开始行走：步长 {STEP_LENGTH:.2f} m，速度 {WALK_SPEED:.2f} m/s")
                time.sleep(WALK_DURATION)
            finally:
                # --------------------------------------------------
                # 3. 停止行走（包括 Ctrl+C / 异常退出的情况）
                if walking:
                    client.publish("grx", {
                        "virtual_panel_command_start": False,
                        "virtual_panel_command_stop": True,
                    })
                    print("停止行走")
                    time.sleep(1)
    finally:
        client.close()
        print("心跳已停止；约 6 秒后控制器将触发断连保护。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: virtual panel walk control (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_virtual_panel(host=args.host)
