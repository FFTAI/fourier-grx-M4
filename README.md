# Fourier-GRX-M4

Fourier-GRX-M4 SDK 的中英文开发文档与示例代码仓库，面向傅利叶智能 M4 和 M4L 系列机器人。内容涵盖设备安装、User / Developer 接口、运动与标定任务、配置、日常运维和固件发布。

> 本仓库提供文档和示例，不包含 `fourier-grx` SDK 的核心实现。正式固件及安装方式请查看[固件发布](docs/release.md)。

## 在线文档

- [中文文档](https://fftai.github.io/fourier-grx-M4/)
- [English Documentation](https://fftai.github.io/fourier-grx-M4/docs/en/)

## 文档导航

- [快速开始](docs/quickstart.md)：按设备状态选择系统烧录、首次安装、固件更新或机型快速开始流程。
- [示例代码](docs/examples.md)：了解 User、Developer 和 UDP 示例的运行方式与适用场景。
- [参考指南](docs/reference.md)：查阅通信接口、API、配置文件、运行模式和命令行工具。
- [任务描述](docs/tasks.md)：查阅任务 ID、触发方式、参数、状态接口与安全注意事项。
- [常用操作](docs/usage.md)：查阅校准、开机自启动、日志、数据记录和网络连接方法。
- [常见问题](docs/faq.md)：排查硬件、安装、初始化、网络与性能问题。
- [固件发布](docs/release.md)：获取正式固件、下载链接和版本历史。
- [更新日志](docs/changelog.md)：了解 SDK 与文档的重要更新。

## 示例代码

本仓库的 `demo/` 目录提供可直接查阅和运行的示例：

| 目录 | 示例类型 | 依赖与运行位置 |
|------|----------|----------------|
| [`demo/user/`](demo/user) | User API 高层控制与状态读取 | 需要 `fourier_grx` 开发环境；机器人主程序保持运行，可在主控电脑或同一局域网内的电脑上执行 |
| [`demo/developer/`](demo/developer) | Developer API 底层硬件控制 | 需要 `fourier_grx` 开发环境；只能在机器人主控电脑上执行，运行前需停止机器人主程序 |
| [`demo/udp/`](demo/udp) | 纯 Python socket 通信 | Python 3.10+，无第三方依赖；需要机器人主程序启用 UDP 通信 |

获取仓库：

```bash
git clone https://github.com/FFTAI/fourier-grx-M4.git
cd fourier-grx-M4
```

不同示例的启动顺序、配置要求和安全注意事项并不相同，运行前请阅读[示例代码文档](docs/examples.md)及对应接口页面。更多机型示例位于 [Wiki-GRx-Deploy](https://github.com/FFTAI/Wiki-GRx-Deploy) 仓库的 `FourierM4`（M4）和 `FourierM4L`（M4L）分支。

## 仓库结构

```text
├── index.md          # 中文文档首页
├── docs/             # 中文文档及 docs/en/ 英文文档
├── demo/             # User、Developer 与 UDP 示例
├── assets/           # 文档图片、脚本和视频
├── _includes/        # 文档站自定义组件
└── _config.yaml      # Jekyll 与 just-the-docs 配置
```

## 参与贡献

欢迎通过 [Issue](https://github.com/FFTAI/fourier-grx-M4/issues) 或 Pull Request 反馈问题、修正文档和改进示例。提交前请阅读[贡献指南](docs/contributing.md)，并注意中英文文档同步、导航元数据和站内链接检查。

## 许可证

本仓库采用 [MIT License](LICENSE)。
