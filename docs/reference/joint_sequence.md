---
layout: default
title: 机器人关节序列
nav_order: 3.3
parent: 参考指南
has_toc: true
---

# 机器人关节序列

* TOC
{:toc}

在获取关节信息或是发送控制指令时，需要整体发送所有关节的信息。因此需要按照机器人的关节序列进行操作。

Fourier-GRX SDK 提供的关节序列与机器人 URDF 模型文件中的关节序列一致。用户在使用时需要注意关节序列的顺序。

Fourier-GRX SDK 中对于关节序列的定义如下。

## M4

- 总数：2 + 2 = 4
- 左腿：2
- 右腿：2

| 序号 | 关节名称                   | 具体描述        |
|----|------------------------|-------------|
| 0  | left_hip_pitch_joint   | 左髋 pitch 关节 |
| 1  | left_knee_pitch_joint  | 左膝 pitch 关节 |
| 2  | right_hip_pitch_joint  | 右髋 pitch 关节 |
| 3  | right_knee_pitch_joint | 右膝 pitch 关节 |

## M4L

- 总数：2 + 2 + 2 + 2 = 8
- 左腿：4
    - 旋转关节: 2
    - 直线关节: 2
- 右腿：4
    - 旋转关节: 2
    - 直线关节: 2

| 序号 | 关节名称                     | 具体描述        |
|----|--------------------------|-------------|
| 0  | left_hip_pitch_joint     | 左髋 pitch 关节 |
| 1  | left_knee_pitch_joint    | 左膝 pitch 关节 |
| 2  | right_hip_pitch_joint    | 右髋 pitch 关节 |
| 3  | right_knee_pitch_joint   | 右膝 pitch 关节 |
| 4  | left_thigh_length_joint  | 左大腿长度关节     |
| 5  | left_shank_length_joint  | 左小腿长度关节     |
| 6  | right_thigh_length_joint | 右大腿长度关节     |
| 7  | right_shank_length_joint | 右小腿长度关节     |
