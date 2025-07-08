---
layout: default
title: 被动前向行走
nav_order: 4.1
parent: 任务描述
has_toc: true
---

# 被动前向行走

任务 ID: 1

| 接口参数 | 类型      | 默认值 | 描述                |
|------|---------|-----|-------------------|
| 步长长度 | `float` | 0.5 | 机器人每一步的长度，单位为 m。  |
| 步行速度 | `float` | 0.5 | 机器人前进的速度，单位为 m/s。 |
| 大腿长度 | `float` | 0.5 | 机器人的大腿长度，单位为 m。   |
| 小腿长度 | `float` | 0.5 | 机器人的小腿长度，单位为 m。   |

| 接口参数 | 虚拟外设映射关系             |
|------|----------------------|
| 步长长度 | `robot.step_length`  |
| 步行速度 | `robot.walk_speed`   |
| 大腿长度 | `robot.thigh_length` |
| 小腿长度 | `robot.calf_length`  |