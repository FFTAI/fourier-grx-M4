---
layout: default
title: 常见问题
nav_order: 6
has_toc: true
has_children: true
---

# 常见问题解答（FAQ）

* TOC
{:toc}

> 如果您遇到的问题未在此列出，请联系技术支持：[xin.chen@fftai.com](mailto:xin.chen@fftai.com)

## 问题分类导航

| 分类 | 问题 |
|------|------|
| 🔋 [硬件问题](/fourier-grx-M4/docs/faq/hardware) | [电池充不进去](/fourier-grx-M4/docs/faq/hardware#电池充电充不进去) |
| 📦 [安装问题](/fourier-grx-M4/docs/faq/install) | [安装中断](/fourier-grx-M4/docs/faq/install#安装过程中断) · [机型配置失败](/fourier-grx-M4/docs/faq/install#机型配置失败) |
| 🚀 [初始化问题](/fourier-grx-M4/docs/faq/initialize) | [配置文件错误](/fourier-grx-M4/docs/faq/initialize#配置文件错误) · [执行器自检失败](/fourier-grx-M4/docs/faq/initialize#执行器自检失败) |
| 🌐 [网络配置](/fourier-grx-M4/docs/faq/network) | [外网访问](/fourier-grx-M4/docs/faq/network#外网访问配置) · [WiFi 热点](/fourier-grx-M4/docs/faq/network#wifi-热点配置) |
| ⚡ [性能相关](/fourier-grx-M4/docs/faq/performance) | [控制频率说明](/fourier-grx-M4/docs/faq/performance#控制频率说明) · [超时警告](/fourier-grx-M4/docs/faq/performance#超时警告处理) · [手柄休眠](/fourier-grx-M4/docs/faq/performance#手柄休眠问题) |
| 🛠️ [开发环境](/fourier-grx-M4/docs/faq/dev_env) | [通信问题](/fourier-grx-M4/docs/faq/dev_env#用户接口通信问题) · [依赖缺失](/fourier-grx-M4/docs/faq/dev_env#依赖问题) |
| 🔌 驱动安装 | [Windows 串口驱动安装](/fourier-grx-M4/docs/faq/serial_driver)（IO Board 烧录检测不到串口时） |

---

## 💡 最佳实践

| 场景 | 建议 |
|------|------|
| 开发环境 | 使用 Ubuntu 22.04，安装所有依赖，配置静态 IP |
| 网络管理 | 开发时使用静态 IP；需要外网时临时切换，用完恢复 |
| 故障排查 | 优先查看 `~/fourier-grx/log/` 下的运行日志 |
| 校准流程 | 每次上电后按顺序执行直线关节 → 旋转关节校准 |

---

## 获取帮助

遇到未列出的问题，可通过以下渠道寻求支持：

- 📖 [参考文档](/fourier-grx-M4/docs/reference)
- 📋 [更新日志](/fourier-grx-M4/docs/changelog)
- 📧 技术支持：[xin.chen@fftai.com](mailto:xin.chen@fftai.com)
