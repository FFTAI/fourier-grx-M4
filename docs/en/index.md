---
layout: default
title: Fourier-GRX-M4 SDK
nav_order: 0
has_children: false
nav_exclude: true
---

# Welcome to the Fourier-GRX-M4 SDK Documentation

## Introduction

The Fourier-GRX-M4 SDK is a software development kit provided by Fourier Intelligence. It offers a set of APIs for installing, configuring, and controlling Fourier Intelligence's M4 and M4L series robot products.

The SDK is designed to be simple and easy to use, providing high-level interfaces to control robot motion and read sensor data. It currently focuses on Python-based secondary development.

## Getting Started

[Quick Start](/fourier-grx-M4/docs/en/quickstart) is the recommended way to begin using the Fourier-GRX-M4 SDK. This step-by-step guide will help you install the required libraries and run simple programs to control your robot.

[Examples](/fourier-grx-M4/docs/en/examples) demonstrates how to use the SDK library and can serve as a reference for developing your own applications.

[Reference Guide](/fourier-grx-M4/docs/en/reference) contains detailed API documentation for the SDK library and can be used as a reference while developing your applications.

[Usage Guide](/fourier-grx-M4/docs/en/usage) covers common operations such as robot calibration and switching between operating modes. For firmware installation, see [Quick Start - Firmware Installation and Update](/fourier-grx-M4/docs/en/quickstart/firmware).

[FAQ](/fourier-grx-M4/docs/en/faq) provides answers to common questions and can help you resolve frequent issues. If you encounter additional problems, you are also welcome to [contribute](/fourier-grx-M4/docs/en/contributing) and help us improve.

[Firmware Releases](/fourier-grx-M4/docs/en/release) lists published firmware versions together with their downloads and notes.

## Supported Platforms and Versions

| Hardware            | OS                   | Python Version | Tested | Passed |
|---------------------|----------------------|----------------|--------|--------|
| ARM RK3588          | Ubuntu 20.04 LTS     | Python 3.11    | ✅     | ✅     |
| X64 INTEL           | Ubuntu 22.04 LTS     | Python 3.11    | ✅     | ✅     |
| X64 AMD             | Ubuntu 22.04 LTS     | Python 3.11    | ✅     | ✅     |
|                     | Windows              | Python 3.11    |        |        |
|                     | MacOS                | Python 3.11    |        |        |

> ℹ️ **Note**:
>
> The Fourier-GRX-M4 SDK provides two levels of interfaces: User and Developer.
> - The User API is based on the [Zenoh](https://zenoh.io) protocol.
> - The Developer API is based on the Python library.
>
> Using the User API via the [Zenoh](https://zenoh.io) protocol has no strict platform or language restrictions, but development on Ubuntu is still recommended.

## Changelog

See the [Changelog](/fourier-grx-M4/docs/en/changelog) for the latest updates to the documentation.

## Contributing

Please read our [Contributing Guide](/fourier-grx-M4/docs/en/contributing) for more information.
