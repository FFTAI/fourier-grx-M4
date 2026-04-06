---
layout: default
title: Resource Files
nav_order: 3.4
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Resource Files

* TOC
{:toc}

Resource Files in the Fourier-GRX SDK are used to store and manage robot resource data, typically including model files (robot models, neural network models), reference data, and credential information.

## Resource File Path

Resource Files are typically stored in the `~/fourier-grx/resource/` directory. Each robot type has its own subdirectory.

For example, the Resource Files for the `FourierM4L` robot are stored in `~/fourier-grx/resource/m4l/`.

## Zenoh Resource Files

Zenoh Resource Files are used in the Fourier-GRX SDK to store and manage Zenoh-related resource data, typically including Zenoh configuration files, credentials, and authorization information.

Zenoh Resource Files are typically stored in `~/fourier-grx/resource/zenoh/`.

Currently, the Zenoh resource files include:
- `user.yaml`: Stores the Zenoh username and password (i.e., the local Zenoh credentials).
- `credentials.yaml`: Stores the Zenoh authorization information (i.e., accepted Zenoh usernames and passwords).

Under normal circumstances, the username and password in `user.yaml` and `credentials.yaml` are the same, to ensure that local communication works correctly.

For detailed information, refer to [https://zenoh.io/docs/manual/user-password/](https://zenoh.io/docs/manual/user-password/)
