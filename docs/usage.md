---
layout: default
title: 常用操作
nav_order: 5
has_toc: true
---

# 常用操作

* TOC
{:toc}

本文档介绍了使用 Fourier-GRX-M4 SDK 时的常用操作流程和注意事项。

## 固件安装和更新

Fourier-GRX-M4 SDK 安装文件请从 [固件更新](/fourier-grx-M4/docs/update) 下载。
下载完后，运行下面的指令完成安装过程：

```
# Fourier-M4 安装 (旧版)
# 安装 fourier-m4-xxx.deb 文件，安装完后系统中会提供 fourier-m4 程序工具
sudo dpkg -i fourier-m4-xxx.deb  # xxx 为具体版本号

# 安装 fourier-m4 完整内容
fourier-m4 install
```

```
# Fourier-GRX 安装 (新版)
# 安装 fourier-grx-xxx.deb 文件，安装完后系统中会提供 fourier-grx 程序工具
sudo dpkg -i fourier-grx-xxx.deb  # xxx 为具体版本号

# 安装 fourier-grx 完整内容
fourier-grx install
```

安装过程中，会要求输入机器人型号，请根据实际机器人型号进行配置，目前支持的型号如下：

`Fourier-M4 (旧版)` 机器人型号的配置选项：

| 机器人型号 | 机器人版本 | 适配的机器人型号                                       |
|-------|-------|------------------------------------------------|
| M4L   | V2    | M4 8电机版本 傅利叶智能自研执行器V1版本，使用 RK3399 嵌入式板卡        |
| M4L   | V3    | M4 8电机版本 傅利叶智能自研执行器V1版本，使用 RK3588 嵌入式板卡（鲁班猫板卡） |

`Fourier-GRX (新版)` 机器人型号的配置选项：

| 机器人型号 | 机器人版本 | 测试机型 | [运行模式](/fourier-grx-M4/docs/reference/run_type) | 适配的机器人型号 |
|-------|-------|------|-------------------------------------------------|----------|
| M4    | T1    | 否    | 开发者模式                                           | M4T1     |

如若配置错误，可运行 `fourier-grx config` 进行重新配置。当前的配置信息可以通过 `fourier-grx list` 查看。

> ℹ️ **说明**
>
> `fourier-m4` 是 `fourier-grx` 的前置版本程序，简称 “旧版”，目前已不再积极维护。如果设备支持新版的 `fourier-grx`， 建议使用 `fourier-grx` 进行安装和使用。

## 关节零位校准

> ℹ️ **说明**
>
> 使用内置校准任务，可以在【调试模式】下用手柄选中执行，也可以在【开发者模式】下通过调用对应任务接口执行。

### 启动前检查

1. **硬件检查**
    - ✅ 机器人电源已接通
    - ✅ 手柄正确连接
    - ✅ 网络连接正常
    - ✅ 插销已插入机器人关节定位孔

2. **软件准备**
    - ✅ SDK 已正确安装

### 启动程序

```bash
# 启动 Fourier-GRX 程序
fourier-grx start
```

### 校准流程

1. **操作步骤**
    - 使用手柄 L1 键选择 **校准任务**
    - 使用手柄 L2 键确认执行
    - 观察终端输出信息

校准任务对照表

| 机器人型号 | 校准任务          | 任务编号 | 说明      |
|-------|---------------|------|---------|
| M4    | TASK_SET_HOME | 999  | 全关节零位校准 |

2. **校准验证**
    - 成功标志
        - 终端显示 **全零数组**
        - 所有关节位置正确
    - 失败情况
        - 数组中出现大于 1 的值（意味着超过 1° 的关节偏差值）
        - 关节位置异常

3. **退出程序**

```bash
# 按两次 Ctrl+C 退出
⌨️ ctrl + c (×2)
```

### ⚠️ 重要注意事项

1. **插销管理**
    - 校准完成后必须拔出所有插销
    - 操作前检查插销是否完全移除
    - 如发现遗留插销，需重新校准

2. **安全预防**
    - 校准过程中保持安全距离
    - 确保紧急停止按钮可及
    - 观察机器人异常行为

3. **故障处理**
    - 校准失败时重新执行流程
    - 多次失败请联系技术支持
    - 记录错误信息以便分析

## 程序开机自启动

fourier-grx 提供了程序开机自启动的配置功能，可以通过以下指令进行配置：

```bash
fourier-grx enable_service  # 开启程序开机自启动
fourier-grx disable_service # 关闭程序开机自启动
```

如果机器人已经配置为用手柄进行遥控操作。
开启开机自启动后，请确保机器人手柄在开机前已连接到主控电脑的 USB 端口，并处于唤醒状态。

## 启用/关闭 程序运行日志记录功能

fourier-grx 提供了程序运行日志记录功能，默认情况下是开启的，且不提供关闭功能。

如果一定希望关闭程序运行日志记录功能，可以修改程序启动脚本 `run.sh` 中的以下字段：

> ⚠️ **注意**：
>
> 修改该脚本会导致无法记录程序运行日志，可能会影响后续的调试和问题排查。

```bash
# 原始脚本内容
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee $FOURIER_GRX_HOME/log/${log_file_name}

# 修改后的脚本内容
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee /dev/null
```

## 启用/关闭 机器人数据日志记录功能

fourier-grx 提供了数据日志记录功能，但是默认情况下是关闭的，以减少对系统性能的影响。

如果需要启用数据日志记录功能，需要对 **配置文件** 进行手动修改，具体修改步骤如下：

1. 创建机器人的启动配置文件：
    - 打开文件夹 `~/fourier-grx/config/m4` 文件夹，找到当前使用的配置文件，比如 `config_M4_T1_debug.yaml`。
    - 将该文件复制一份，命名为 `config_M4_T1_record.yaml`。

2. 修改配置文件：
    - 打开 `config_M4_T1_record.yaml` 文件。
    - 在配置文件中，添加以下内容：
        - 该配置表示在使用该配置文件启动 `fourier-grx` 时，启用数据记录功能，并将记录数据保存到指定路径。

   ```yaml
   record:
      enable: true
      path: "~/fourier-grx/record/m4"
   ```

3. 修改启动脚本：
    - 打开文件夹 `~/fourier-grx`，找到 `run.sh` 文件。
    - 找到 `run_type` 字段，将其修改为 `record`：

   ```bash
   run_type="record"
   ```

   > ⚠️ **注意**：
   >
   > 如果后续希望机器人恢复为正常的操作模式，可以通过 `fourier-grx config` 命令来修改配置文件，或是修改 `run.sh` 文件中的 `run_type` 字段为原来的值。

4. 启动机器人：
    - 此时，机器人将会在启动时启用数据记录功能，并将记录的数据保存到指定路径。

    ```bash
    # 在 终端1 中执行以下命令
    fourier-grx start
    ```

5. 数据分析：
    - 数据保存格式为 CSV 文件，可以使用 Excel 或其他数据分析工具进行分析。
    - Excel 导入时需要注意选择正确的分隔符（逗号）和编码格式（UTF-8）。
    - 数据文件中包含时间戳、关节角度、速度等信息，方便进行后续分析。
        - `Timestamp`: 时间戳
        - `jm_pos_{i}`: 关节 i 的测量位置
        - `jm_vel_{i}`: 关节 i 的测量速度
        - `jm_tor_{i}`: 关节 i 的测量扭矩
        - `jm_cur_{i}`: 关节 i 的测量电流
        - `jt_pos_{i}`: 关节 i 的目标位置
        - `jt_vel_{i}`: 关节 i 的目标速度
        - `jt_tor_{i}`: 关节 i 的目标扭矩
        - 关节序列参考 [关节序列](/fourier-grx-M4/docs/reference/joint_sequence) 文档。

> **说明**：
>
> 如果需要关闭数据记录功能，可以将配置文件中的 `record.enable` 设置为 `false`，或是删除 `record` 字段。

