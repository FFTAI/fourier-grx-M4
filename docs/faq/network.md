---
layout: default
title: 网络配置
parent: 常见问题
nav_order: 6.4
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

## 关闭 Windows 上位机有线网 IPv6

**问题**：Windows 上位机与机器人通过有线网直连并共享网络时，出现域名解析失败、通信超时或机器人运行过程中偶发卡顿。

**解决方案**：关闭上位机连接机器人所用有线网卡的 IPv6。

1. 按 `Win + R`，输入 `ncpa.cpl` 并回车，打开“网络连接”
2. 找到连接机器人的**以太网**适配器，右键点击 → **属性**
3. 取消勾选 **Internet 协议版本 6 (TCP/IPv6)**，点击 **确定**

![Windows 以太网属性中的 Internet 协议版本 6 (TCP/IPv6) 选项](/fourier-grx-M4/assets/images/windows_ipv6_properties.png)

> 图中 IPv6 选项处于勾选状态；操作时取消勾选 **Internet 协议版本 6 (TCP/IPv6)**。图片：Microsoft，来自 Microsoft Learn [为高级用户配置 IPv6](https://learn.microsoft.com/zh-cn/troubleshoot/windows-server/networking/configure-ipv6-in-windows)，遵循 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可。

也可以使用管理员 PowerShell：

```powershell
# 查看有线网卡的 IPv6 绑定状态
Get-NetAdapterBinding -Name "以太网" -ComponentID ms_tcpip6

# 关闭 IPv6（网卡名称以实际为准，如 "以太网 2"）
Disable-NetAdapterBinding -Name "以太网" -ComponentID ms_tcpip6
```

> ℹ️ **说明**
>
> - 只需关闭连接机器人的有线网卡，无需关闭 WiFi；修改后重新启用网络共享或重新插拔网线即可生效
> - 如需恢复，将 `Disable-NetAdapterBinding` 换成 `Enable-NetAdapterBinding`，或在网卡属性中重新勾选 IPv6
