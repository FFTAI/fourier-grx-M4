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
Demo code for testing joint of the robot

⚠️ 在 M4L 上此示例不会真正执行任何动作：
   SDK 常量 fourier_grx.TaskCommand.TASK_TEST_JOINT 对应 TID 902，
   M4L 没有注册该任务，机器人会打印
   "Task command value 902 is not supported." 并保持原任务不变。
   M4L 请改用以下专项任务（把下方 message 中的任务值替换即可）：
   - 4100 TASK_ROTARY_JOINT_TEST_JOINT_PD    旋转关节（髋/膝）PD 测试，往复 3 次
   - 4200 TASK_PRISMATIC_JOINT_TEST_JOINT_PD 直线关节（腿长）PD 测试
   测试任务会驱动关节运动，执行前请确认机器人已支撑稳定、周围无人。

Run this script by:
    python demo_xxx.py

"""

import time

from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket

import fourier_grx.sdk.user as fourier_grx


def demo_task():
    # 初始化 socket 客户端（自动发现机器人）
    client = SyncClientSocket()

    # 等待自动发现服务端
    print("等待连接到机器人...")
    while not client.server_discovered():
        time.sleep(0.1)

    print(f"已连接到机器人 {client.server_host}:{client.server_port}")

    # 构建消息
    message = {
        "robot_task_command": fourier_grx.TaskCommand.TASK_TEST_JOINT,
        "flag_task_command_update": True,
    }

    print("发送消息:", message)

    # 发布消息到 task topic
    client.publish(key="task", value=message)

    # 等待 1s（确保消息被发送）
    time.sleep(1)

    client.close()


if __name__ == "__main__":
    demo_task()
