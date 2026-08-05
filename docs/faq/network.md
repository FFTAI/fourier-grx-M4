---
layout: default
title: 网络配置
nav_order: 6.4
parent: 常见问题
---

# 网络配置

## 外网访问配置

**问题**：如何让机器人主控电脑访问外网？

机器人默认使用有线网口连接执行器（静态 IP）。需要外网时，按以下步骤切换：

```bash
# 切换到动态 IP（访问外网）
sudo nmcli connection modify "有线连接" ipv4.method auto
sudo systemctl restart NetworkManager

# 使用完毕，切换回静态 IP（操作机器人）
sudo nmcli connection modify "有线连接" ipv4.method manual \
    ipv4.addresses 192.168.137.220/24
sudo systemctl restart NetworkManager
```

## WiFi 热点配置

**问题**：如何关闭 WiFi 热点自启动？

```bash
sudo systemctl stop rocs-wifi      # 临时关闭
sudo systemctl disable rocs-wifi   # 永久关闭（重启后生效）
```
