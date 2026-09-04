# UDP 示例（纯 Python socket 实现）

本目录下的示例演示如何**不依赖 `fourier_grx` SDK**，仅使用 Python 标准库
（`socket` + `struct`）通过 UDP 与机器人通信。

## 运行环境

- Python 3.10+，无需安装任何第三方包
- 机器人已启动 `fourier-grx` 主程序，且配置中 `communication.enable: true`、`type: "socket"`

## 协议简介（UDP + MessagePack）

- 机器人（服务端）监听 UDP **5566** 端口
- 机器人每秒向 `255.255.255.255:9527` 广播一次 `{"host": <ip>, "port": 5566}`（自动发现）
- 客户端 → 机器人数据包：`{"key": <topic>, "data": {...可写字段...}}`
- 机器人 → 客户端数据包：`{"key": <topic>, "data": {...可读字段...}}`，
  约 50 Hz 推送给所有"发过至少一个包"的客户端
- topic 包括：`comm`、`robot`、`task`、`grx`、`rehab`

MessagePack 编解码由本目录下的 `mini_msgpack.py` 用标准库 `struct` 实现，
与官方 `msgpack` 库完全兼容。

## 示例列表

**任务指令（task topic）**

| 示例 | 说明 |
|------|------|
| `demo_servo_on.py` | 执行器使能（TASK_SERVO_ON = 35） |
| `demo_servo_off.py` | 执行器失能（TASK_SERVO_OFF = 36） |
| `demo_servo_reboot.py` | 执行器重启（TASK_SERVO_REBOOT = 41） |
| `demo_clear_fault.py` | 清除故障（TASK_CLEAR_FAULT = 34） |
| `demo_walk.py` | 行走控制（TASK_ROTARY_JOINT_FORWARD_WALK = 4111） |

**状态读取（server → client 推送）**

| 示例 | 说明 |
|------|------|
| `demo_get_state.py` | 接收并打印机器人状态（task / comm topic） |

**保护标志清除（robot topic）**

| 示例 | 说明 |
|------|------|
| `demo_clear_protection.py` | 清除过载 / 力矩保护标志 |

**虚拟外设输入（grx topic）**

| 示例 | 说明 |
|------|------|
| `demo_virtual_panel.py` | 虚拟面板：设置步长/速度并控制行走开始停止（默认配置可用） |
| `demo_virtual_joystick.py` | 虚拟摇杆：写入摇杆轴状态（需在配置中开启 use_virtual_joystick） |

**心跳（comm topic）**

| 示例 | 说明 |
|------|------|
| `demo_heartbeat.py` | 上位机心跳（持续写 `comm.host_heartbeat_counter`） |

## 运行方法

```bash
cd demo/udp

# 自动发现机器人（默认）
python demo_servo_on.py

# 或直接指定机器人 IP
python demo_servo_on.py --host 192.168.137.220
```

## 上位机心跳注意事项

`demo_heartbeat.py` 演示断连保护机制：

- 控制器从**第一次收到** `host_heartbeat_counter` 开始计时
- 超过 `host_heartbeat_timeout`（默认 6 秒）未收到新的心跳写入，
  控制器自动触发断连保护（常规机型 SERVO_OFF，M4LT2 高阻尼软制动）
- 因此一旦开始发送心跳就必须持续发送；中途停止约 6 秒后会触发保护，
  这正是该机制的设计目的
