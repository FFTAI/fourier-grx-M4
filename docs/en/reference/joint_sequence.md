---
layout: default
title: Joint Sequence
nav_order: 3.3
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Joint Sequence

* TOC
{:toc}

When retrieving joint information or sending control commands, all joint data must be sent together. Therefore, operations must follow the robot's Joint Sequence.

The Joint Sequence provided by the Fourier-GRX SDK is consistent with the joint sequence defined in the robot's URDF model file. Users should pay attention to the order of the Joint Sequence when working with the API.

The Joint Sequence definitions in the Fourier-GRX SDK are as follows.

## M4

- Total: 2 + 2 = 4
- Left leg: 2
- Right leg: 2

| Index | Joint Name             | Description            | IP Address      |
|-------|------------------------|------------------------|-----------------|
| 0     | left_hip_pitch_joint   | Left hip pitch joint   | 192.168.137.70  |
| 1     | left_knee_pitch_joint  | Left knee pitch joint  | 192.168.137.71  |
| 2     | right_hip_pitch_joint  | Right hip pitch joint  | 192.168.137.50  |
| 3     | right_knee_pitch_joint | Right knee pitch joint | 192.168.137.51  |

## M4L

- Total: 2 + 2 + 2 + 2 = 8
- Left leg: 4
    - Rotary joints: 2
    - Prismatic joints: 2
- Right leg: 4
    - Rotary joints: 2
    - Prismatic joints: 2

| Index | Joint Name               | Description                 | IP Address      |
|-------|--------------------------|-----------------------------|-----------------|
| 0     | left_hip_pitch_joint     | Left hip pitch joint        | 192.168.137.70  |
| 1     | left_knee_pitch_joint    | Left knee pitch joint       | 192.168.137.71  |
| 2     | right_hip_pitch_joint    | Right hip pitch joint       | 192.168.137.50  |
| 3     | right_knee_pitch_joint   | Right knee pitch joint      | 192.168.137.51  |
| 4     | left_thigh_length_joint  | Left thigh length joint     | 192.168.137.72  |
| 5     | left_shank_length_joint  | Left shank length joint     | 192.168.137.73  |
| 6     | right_thigh_length_joint | Right thigh length joint    | 192.168.137.52  |
| 7     | right_shank_length_joint | Right shank length joint    | 192.168.137.53  |
