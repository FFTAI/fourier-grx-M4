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

Demo code for Fourier robots

⚠️ 在 M4L 上此示例不会真正执行任何动作：
   SDK 常量 fourier_grx.TaskCommand.TASK_SET_HOME 对应 TID 999，
   M4L 没有注册该任务。Developer 接口是直接在进程内调用
   ControlSystem.robot_control_set_task_command()，任务切换前会先查已注册任务表，
   未命中时只打一条 warning 就跳过切换、保持原任务不变：
   "task command: 999 TASK_SET_HOME is not available at current state. Command update skipped."
   （若改用 User 接口 / UDP 下发同一个 TID，报错文本不同：
   "Task command value 999 is not supported."）
   M4L 请改用以下专项任务（把下方 task_command 替换即可）：
   - 4103 TASK_ROTARY_JOINT_SET_HOME    设置旋转关节（髋/膝）当前位置为零点
   - 4203 TASK_PRISMATIC_JOINT_SET_HOME 设置直线关节（腿长）零点
   详见文档《任务描述 - 设置零点》。

Run this script by:
    python demo_xxx.py --config=config_xxx.yaml
    - config_xxx.yaml is the configuration file for the Fourier robots

"""

import time

import fourier_grx.sdk.developer as fourier_grx

control_system = fourier_grx.ControlSystem()


def main():
    # 切换为开发者模式
    control_system.developer_mode(servo_on=False)

    # 打印版本信息
    print(control_system.get_info())

    # 算法任务
    algorithm()


def algorithm():
    control_system.robot_control_set_task_command(
        task_command=fourier_grx.TaskCommand.TASK_SET_HOME
    )

    # 等待算法任务执行完成
    time.sleep(10)


if __name__ == "__main__":
    main()
