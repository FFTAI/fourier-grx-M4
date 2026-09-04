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
Demo code for virtual joystick input (grx topic), using only the Python
standard library (socket), without the fourier_grx SDK.

本示例演示如何向 grx topic 写入虚拟摇杆字段：
- virtual_joystick_axis_left:  左摇杆 [x, y]，范围 [-1, 1]；
  行走任务中 -y 方向（前推）映射为归一化步长
- virtual_joystick_axis_right: 右摇杆 [x, y]，范围 [-1, 1]；
  行走任务中 -y 方向（前推）映射为归一化行走速度
- virtual_joystick_button_*:   按钮状态，0: 未按下，1: 按下

⚠️ 使用前请阅读以下注意事项：
1. 需要在机器人 fourier-grx 配置文件中开启 peripheral/use_virtual_joystick: true
2. 多个虚拟外设同时开启时存在优先级覆盖（越靠后的外设优先级越高），
   默认 release 配置开启了 use_virtual_panel，其输入会覆盖摇杆输入；
   如需使用摇杆控制行走，请关闭 use_virtual_panel
3. 行走任务的"开始运动"由摇杆按下（button_axis_left）触发，
   该字段未通过网络接口开放，因此仅用摇杆无法启动行走；
   可配合虚拟面板的 virtual_panel_command_start 使用

Run this script by:
    python demo_virtual_joystick.py                # auto-discover the robot
    python demo_virtual_joystick.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient


def demo_virtual_joystick(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    # --------------------------------------------------
    # 推送虚拟摇杆状态示例：左摇杆前推 3 秒（20Hz 持续写入）
    print("写入虚拟摇杆状态：左摇杆前推（y = -1.0），持续 3 秒...")
    t_start = time.time()
    while time.time() - t_start < 3.0:
        client.publish("grx", {
            "virtual_joystick_axis_left": [0.0, -1.0],   # 步长归一化输入（最大）
            "virtual_joystick_axis_right": [0.0, -0.5],  # 速度归一化输入（50%）
        })
        time.sleep(0.05)

    # --------------------------------------------------
    # 摇杆回中
    client.publish("grx", {
        "virtual_joystick_axis_left": [0.0, 0.0],
        "virtual_joystick_axis_right": [0.0, 0.0],
    })
    print("摇杆回中")

    time.sleep(1)

    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: virtual joystick input (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_virtual_joystick(host=args.host)
