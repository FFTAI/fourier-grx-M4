---
layout: default
title: Joint Zero Calibration
nav_order: 5.1
parent: "Usage Guide"
has_toc: true
nav_exclude: true
---

# Joint Zero Calibration

* TOC
{:toc}

> ℹ️ **Note**: Built-in calibration tasks can be selected and executed with a gamepad in **Debug Mode**, or by calling the corresponding task interface in **Developer Mode**.

## Pre-Startup Checklist

**Hardware**

- ✅ Robot power is connected
- ✅ Gamepad is properly connected
- ✅ Network connection is normal
- ✅ Locking pins are inserted into the joint positioning holes (for manual calibration)

**Software**

- ✅ SDK is correctly installed and `fourier-grx start` runs successfully

## M4L Power-On Calibration Sequence

> ⚠️ **M4L series robots must perform calibration in the following order after every power-on. Otherwise, joint position data will be invalid.**
>
> - Rotary joints (hip/knee) use absolute encoders — the zero point is retained across power cycles
> - Prismatic joints (leg length) use incremental encoders — **must be recalibrated after every power-on**

| Step | Task Name | TID | Description |
|------|-----------|-----|-------------|
| 1 | Auto Calibrate (Prismatic Joints) | 4210 | Leg length contracts to minimum then resets to zero; takes ~20 s |
| 2 | Auto Calibrate (Rotary Joints) | 4120 | Boundary detection → power-off drop → zero-point write; takes ~60 s |

## Calibration Task Reference

| Robot Model | Task | TID | Notes |
|-------------|------|-----|-------|
| M4L | Auto Calibrate (Prismatic Joints) | 4210 | Required after every power-on |
| M4L | Auto Calibrate (Rotary Joints) | 4120 | Perform as needed after power-on |
| M4L | Manual Set Home (Prismatic Joints) | 4203 | Use after manually aligning pins |
| M4L | Manual Set Home (Rotary Joints) | 4103 | Use after manually aligning pins |

## Calibration Verification

After calibration, the terminal prints a deviation array for each joint:

- ✅ **Success**: all values near 0 (deviation < 1°)
- ❌ **Failure**: any value greater than 1 — re-run the corresponding calibration task

Press `Ctrl+C` twice to exit the program.

## Important Notes

**Pin Management**

- Manual calibration (TID 4103 / 4203): insert pins before execution
- Automatic calibration (TID 4120 / 4210): no pins required
- After calibration, **remove all pins** before running any motion task

**Safety**

- TID 4210: the leg-length mechanism moves automatically — maintain a safe distance
- TID 4120: rotary joints slowly travel to their mechanical limits — ensure joints are unobstructed
- Keep the emergency stop button within reach at all times

**Troubleshooting**

- Auto calibration timed out: check if the motor driver is reporting an alarm; execute Clear Fault (TID 34) and retry
- Calibration succeeded but motion is abnormal: re-run the calibration task for the affected direction
- Repeated failures: contact technical support and save the terminal log
