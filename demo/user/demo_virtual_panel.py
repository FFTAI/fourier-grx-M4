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
- virtual_panel_command_start:   开始运动（置 True 启动；启动后再置 False 不会停止）
- virtual_panel_command_stop:    停止运动（在步态循环边界生效，逐渐停止）
- virtual_panel_command_pause:   暂停运动（暂停后需重新进入任务才能继续）

注意：
- 使用前请确认机器人已使能（servo on），主程序已启动
- 服务端只更新收到的字段，stop / pause 不会自动清零；本 demo 会在启动任务前显式清零
- 默认 release / sdk 配置已开启 use_virtual_panel: true

Run this script by:
    python demo_virtual_panel.py
"""

import time

from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

import fourier_grx.sdk.user as fourier_grx


def demo_virtual_panel():
    # 初始化 socket 客户端（自动发现机器人）
    client = SyncClientSocket()
    walking = False

    try:
        # 等待自动发现服务端
        print("等待连接到机器人...")
        while not client.server_discovered():
            time.sleep(0.1)

        print(f"已连接到机器人 {client.server_host}:{client.server_port}")

        # --------------------------------------------------
        # 0. 先切到 IDLE。若行走任务正处于暂停锁存状态，切走会触发
        #    deactivate 并复位 pause 标志。任务与面板命令都没有 ACK，
        #    有限重发和等待只降低丢包/乱序风险，不能保证绝对送达。
        for _ in range(5):
            client.publish(key="task", value={
                "robot_task_command": fourier_grx.TaskCommand.TASK_IDLE,
                "flag_task_command_update": True,
            })
            time.sleep(0.02)
        # 等待 deactivate 完成，并给可能延迟到达的 IDLE 包留出处理时间
        time.sleep(0.2)

        # --------------------------------------------------
        # 1. 清除面板状态。服务端只按收到的字段更新，stop / pause 不会自动清零；
        #    pause 在任务运行期间读到 True 即会锁存，只有重新进入任务才复位。
        for _ in range(5):
            client.publish(key="grx", value={
                "virtual_panel_command_start": False,
                "virtual_panel_command_stop": False,
                "virtual_panel_command_pause": False,
            })
            time.sleep(0.02)
        # 等待 peripheral 同步，并吸收可能延迟到达的清零包
        time.sleep(0.1)

        # --------------------------------------------------
        # 2. 启动行走任务
        client.publish(key="task", value={
            "robot_task_command": fourier_grx.TaskCommand.TASK_WALK,
            "flag_task_command_update": True,
        })
        time.sleep(1)

        # --------------------------------------------------
        # 3. 通过虚拟面板设置步长 / 速度并开始行走
        #    步长范围 [0.20, 0.80] m，速度范围 [0.10, 1.20] m/s
        #    注意：开启 use_virtual_panel 后若不下发这两个字段，它们的值是 0.0
        #    而不是算法默认值 0.5，会被裁剪到范围下限（步长 0.20 m、速度 0.10 m/s）
        #    demo 使用较小值，便于安全验证
        walking = True
        client.publish(key="grx", value={
            "virtual_panel_command_param_1": 0.20,  # 步长 0.2 m
            "virtual_panel_command_param_2": 0.20,  # 行走速度 0.2 m/s
            "virtual_panel_command_start": True,
            # 启动前已清零；这里再声明一次 stop / pause，
            # 避免清除帧丢失后残留的 stop 让行走在第一步后停止
            "virtual_panel_command_stop": False,
            "virtual_panel_command_pause": False,
        })
        print("开始行走：步长 0.2 m，速度 0.2 m/s")

        # 行走 5 秒
        time.sleep(5)
    finally:
        # --------------------------------------------------
        # 4. 停止行走（包括 Ctrl+C / 异常退出的情况）
        try:
            if walking:
                client.publish(key="grx", value={
                    "virtual_panel_command_start": False,
                    "virtual_panel_command_stop": True,
                })
                print("停止行走")
                time.sleep(1)
        finally:
            client.close()


if __name__ == "__main__":
    demo_virtual_panel()
