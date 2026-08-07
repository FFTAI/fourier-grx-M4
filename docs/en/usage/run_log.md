---
layout: default
title: Program Run Logging
nav_order: 5.3
parent: "Usage Guide"
nav_exclude: true
---

# Program Run Logging

Program run logging is **enabled by default** and writes to `~/fourier-grx/log/`.

To disable it, modify the startup script `run.sh`:

> ⚠️ Once disabled, program activity will no longer be recorded, which may hinder later debugging and troubleshooting.

```bash
# Original (logging enabled)
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee $FOURIER_GRX_HOME/log/${log_file_name}

# Modified (logging disabled)
stdbuf -oL $FOURIER_GRX_HOME/run.bin --config=${config_file_path} \
| tee /dev/null
```
