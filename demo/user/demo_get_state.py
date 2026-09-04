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
Demo code for reading robot state (task / robot / grx topics)

服务端推送到客户端的数据保存在 client._dynalink_manager 中，
各 topic 对应 dynalink_comm / dynalink_robot / dynalink_task /
dynalink_grx / dynalink_rehab，字段名与《参考指南 - User 接口》一致。

Run this script by:
    python demo_get_state.py
"""

import time

from fourier_grx.process.sync.fi_sync_client_socket import SyncClientSocket


def demo_get_state():
    # 初始化 socket 客户端（自动发现机器人）
    client = SyncClientSocket()

    # 等待自动发现服务端
    print("等待连接到机器人...")
    while not client.server_discovered():
        time.sleep(0.1)

    print(f"已连接到机器人 {client.server_host}:{client.server_port}")

    # 客户端需要先发送一个数据包，服务端才会向本客户端推送状态
    client.publish(key="task", value={})

    manager = client._dynalink_manager

    print("接收机器人状态（按 Ctrl+C 退出）...")
    try:
        while True:
            # task topic：任务状态
            task = manager.dynalink_task
            # robot topic：机器人状态
            robot = manager.dynalink_robot
            # grx topic：版本 / 电池等信息
            grx = manager.dynalink_grx

            joint_position = robot.joint_measured_position
            imu_euler = robot.sensor_imus_euler_angle_value

            print("#################################################")
            print(f"fourier_grx_version = {grx.fourier_grx_version}")
            print(f"battery = {grx.robot_battery_percentage * 100:.1f}%")
            print(f"task_state = {task.robot_task_state}, running = {task.flag_task_running}")
            print(f"servo_on = {robot.flag_robot_servo_on}, fault = {robot.flag_robot_fault}")
            print(f"joint_position = {[round(p, 3) for p in joint_position]}")
            print(f"imu_euler_angle = {[round(a, 3) for a in imu_euler]}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()


if __name__ == "__main__":
    demo_get_state()
