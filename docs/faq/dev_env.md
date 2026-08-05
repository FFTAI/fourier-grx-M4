---
layout: default
title: 开发环境问题
nav_order: 6.6
parent: 常见问题
---

# 开发环境问题

## 用户接口通信问题

**现象**：User API 测试程序无法正常通信。

**排查步骤**：

1. 优先使用有线网口，避免同时连接有线和无线网络
2. 确认机器人 IP 与本机网段一致
3. 确认 SDK 版本兼容性

## 依赖问题

**现象**：`ImportError: GLIBC_2.33 not found`

**解决方案**：

```bash
sudo apt update && sudo apt install build-essential
```

系统要求：

- 推荐：Ubuntu 22.04 LTS
- 最低：支持 GLIBC 2.33 的 Linux 发行版
