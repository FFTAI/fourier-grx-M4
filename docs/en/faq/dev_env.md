---
layout: default
title: Development Environment Issues
nav_order: 6.6
parent: FAQ
nav_exclude: true
---

# Development Environment Issues

## User API Communication Issue

**Symptom**: The User API test program cannot communicate normally.

**Troubleshooting**:

1. Prefer the wired network interface — avoid connecting both wired and wireless networks at the same time
2. Confirm the robot IP and the local machine are on the same subnet
3. Verify SDK version compatibility

## Dependency Issue

**Symptom**: `ImportError: GLIBC_2.33 not found`

**Solution**:

```bash
sudo apt update && sudo apt install build-essential
```

System requirements:

- Recommended: Ubuntu 22.04 LTS
- Minimum: A Linux distribution supporting GLIBC 2.33
