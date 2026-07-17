---
layout: default
title: Fourier-M4 固件
parent: 固件发布
nav_order: 2
has_toc: true
---

# Fourier-M4 固件

* TOC
{:toc}

## 版本列表

| 发布日期 | 版本 | 下载 | 更新内容 | 支持状态 |
|----------|------|------|----------|----------|
| 2025-07-22 | 2.0.6 | [⬇ 下载](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.6.deb) | [详情](#206) | ❌ 已停止 |
| 2025-06-09 | 2.0.5 | [⬇ 下载](https://fourier-m4-1302548221.cos.ap-shanghai.myqcloud.com/fourier-m4-2.0.5.deb) | [详情](#205) | ❌ 已停止 |

## 安装方法

固件首次安装流程请参考 [固件安装（首次安装）](/fourier-grx-M4/docs/quickstart/firmware_install)；已安装设备升级版本请参考 [固件更新](/fourier-grx-M4/docs/quickstart/firmware_update)。

---

## 更新内容

### 2.0.6

> 📅 2025-07-22

🐛 **修复**

- 修复站立状态下放下设备无法触发力量保护的问题

🔧 **修改**

- M4LV3 控制周期由 `0.03s` 修正为 `0.025s`（提速约 1/6），踏步速度相应提升；稳定性风险待进一步验证

⚠️ **已知限制**

- 行走过程中无力量保护（历史版本未实现，需求尚未确认）
- 位置保护在向后运动时无法触发（问题难以修复，出现频率待确认）

---

### 2.0.5

> 📅 2025-06-09

🐛 **修复**

- 修复原地踏步助力模式下容易误触发助力运动的问题
