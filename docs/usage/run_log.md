---
layout: default
title: 程序运行日志
nav_order: 5.3
parent: 常用操作
---

# 程序运行日志

程序运行日志默认**开启**，记录位于 `~/fourier-grx/log/`。

如需关闭，修改启动脚本 `run.sh`：

> ⚠️ 关闭后将无法记录程序活动，可能影响后续调试排查。

```bash
# 原始（保留日志）
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee $FOURIER_GRX_HOME/log/${log_file_name}

# 修改后（丢弃日志）
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee /dev/null
```
