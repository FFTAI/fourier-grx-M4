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

所需 fourier-grx 配置（示例片段）：

communication:
  enable: true
  period: 0.02
  type: "socket"

peripheral:
  use_virtual_joystick: true
  # 测试摇杆输入时建议关闭虚拟面板，因为面板输入会覆盖摇杆输入
  use_virtual_panel: false

⚠️ 使用前请阅读以下注意事项：
1. 修改配置后需要重启 fourier-grx 主程序
2. 行走任务的"开始运动"由摇杆按下（button_axis_left）触发，
   该字段未通过网络接口开放，因此仅用摇杆无法启动行走
3. 本示例运行期间会发送上位机心跳；示例退出后心跳停止，
   约 6 秒后控制器会按设计触发断连保护

Run this script by:
    python demo_virtual_joystick.py                # auto-discover the robot
    python demo_virtual_joystick.py --host 192.168.137.220
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fourier_udp_client import FourierUdpClient, HeartbeatSender

JOYSTICK_DURATION = 3.0  # seconds
JOYSTICK_PERIOD = 0.05   # 20 Hz


def demo_virtual_joystick(host=None):
    client = FourierUdpClient(host=host)
    print(f"已连接到机器人 {client.server_addr[0]}:{client.server_addr[1]}")

    try:
        with HeartbeatSender(client):
            try:
                # --------------------------------------------------
                # 推送虚拟摇杆状态示例：左摇杆前推 3 秒（20Hz 持续写入）
                # 轴值 -y（前推）归一化映射到任务范围：
                #   axis_left[1]  = -0.5 → 步长约 0.5 m（范围 [0.20, 0.80] m）
                #   axis_right[1] = -0.25 → 速度约 0.375 m/s（范围 [0.10, 1.20] m/s）
                print("写入虚拟摇杆状态：左/右摇杆前推，持续 3 秒...")
                t_start = time.time()
                while time.time() - t_start < JOYSTICK_DURATION:
                    client.publish("grx", {
                        "virtual_joystick_axis_left": [0.0, -0.5],   # 步长归一化输入（约 0.5 m）
                        "virtual_joystick_axis_right": [0.0, -0.25],  # 速度归一化输入（约 0.375 m/s）
                    })
                    time.sleep(JOYSTICK_PERIOD)
            finally:
                # --------------------------------------------------
                # 摇杆回中（包括 Ctrl+C / 异常退出的情况）
                client.publish("grx", {
                    "virtual_joystick_axis_left": [0.0, 0.0],
                    "virtual_joystick_axis_right": [0.0, 0.0],
                })
                print("摇杆回中")
                time.sleep(1)
    finally:
        client.close()
        print("心跳已停止；约 6 秒后控制器将触发断连保护。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP demo: virtual joystick input (纯 socket 实现)")
    parser.add_argument("--host", default=None, help="机器人 IP，缺省时自动发现")
    args = parser.parse_args()

    demo_virtual_joystick(host=args.host)
