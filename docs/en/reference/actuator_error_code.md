---
layout: default
title: Actuator Error Codes
nav_order: 3.8
parent: "Reference Guide"
has_toc: true
nav_exclude: true
---

# Actuator Error Codes

* TOC
{:toc}

Actuator Error Codes consist of two parts: the primary error code and the extended error code. The primary error code indicates the basic error status of an actuator, while the extended error code provides more detailed error information.

- The primary error code is a 32-bit unsigned integer where each bit represents a specific error state. Bitwise operations can be used to quickly determine the current error status of an actuator.
- The extended error code does not currently expose any information and is reserved for internal use only.

## Primary Error Codes

The following is the list of primary actuator error codes:

| Error Code Name      | Bit | Value (Dec) | Value (Hex) | Description                                   | Detection Method | Motion Restriction    | Clear Method                                                       |
|----------------------|-----|-------------|-------------|-----------------------------------------------|------------------|-----------------------|--------------------------------------------------------------------|
| adccalfault          | 0   | 1           | 0x01        | Phase current bias calibration error          | Power-on check   | Cannot enable motor   | Investigate and repair hardware fault                             |
| CanComTimeOut        | 1   | 2           | 0x02        | ESP and STM handshake failure                 | Power-on check   | Cannot enable motor   | Check version compatibility and restart                           |
| OverCurrnt           | 2   | 4           | 0x04        | Overcurrent                                   | Real-time check  | Cannot enable motor   | Restart                                                           |
| OverVbus             | 3   | 8           | 0x08        | Bus voltage too high                          | Real-time check  | Cannot enable motor   | Restart                                                           |
| UnderVbus            | 4   | 16          | 0x10        | Bus voltage too low                           | Real-time check  | Cannot enable motor   | Restart                                                           |
| OverTempTrip         | 5   | 32          | 0x20        |                                               |                  |                       |                                                                   |
| OverTempMos          | 6   | 64          | 0x40        | MOS over-temperature                          | Real-time check  | Cannot enable motor   | Restart                                                           |
| OverPhaseACurrent    | 7   | 128         | 0x80        | Phase A overcurrent                           | Real-time check  | Cannot enable motor   | Restart                                                           |
| OverPhaseBCurrent    | 8   | 256         | 0x100       | Phase B overcurrent                           | Real-time check  | Cannot enable motor   | Restart                                                           |
| OverPhaseCCurrent    | 9   | 512         | 0x200       | Phase C overcurrent                           | Real-time check  | Cannot enable motor   | Restart                                                           |
| OverHardPhaseCurrent | 10  | 1024        | 0x400       | Driver chip hardware overcurrent              | Real-time check  | Cannot enable motor   | Investigate hardware fault, repair, and restart                   |
| OPDFault             | 11  | 2049        | 0x800       | Phase loss                                    |                  |                       |                                                                   |
| EncoderNotCali       | 12  | 4096        | 0x1000      | Electrical angle magnetic encoder not calibrated | Power-on check | Cannot enable motor   | Recalibrate                                                       |
| EncoderLoss          | 13  | 8192        | 0x2000      | Electrical angle magnetic encoder lost        | Real-time check  | Cannot enable motor   | Investigate hardware fault, repair, and restart                   |
| FlashErr             | 14  | 16384       | 0x4000      | Flash error                                   | Power-on check   | Cannot enable motor   | Restart                                                           |
| MotorStall           | 15  | 32768       | 0x8000      | Abnormal speed                                |                  |                       |                                                                   |
| PositionErr          | 16  | 65536       | 0x10000     | Position protection error                     |                  |                       |                                                                   |
| EncoderReversal      | 17  | 131072      | 0x20000     | Encoder reversal                              | Calibration check | Cannot enable motor  | Correct phase sequence and recalibrate                            |
| MotorTypeNULL        | 18  | 262144      | 0x40000     | Motor type is null                            | Power-on check   | Cannot enable motor   | Configure ESP32 parameters and restart                            |
| HardwareTypeNULL     | 19  | 524288      | 0x80000     | Hardware type is null                         | Power-on check   | Cannot enable motor   | Configure ESP32 parameters and restart                            |
| EncoderOthersErr     | 20  | 1048576     | 0x100000    | Other encoder errors                          | Calibration check | Cannot enable motor  | Investigate hardware fault, repair, and restart                   |
| OverTempCoil         | 21  | 2097152     | 0x200000    | Coil over-temperature                         | Real-time check  | Cannot enable motor   | Restart                                                           |
| AdcDmaInitErr        | 22  | 4194304     | 0x400000    | AdcDma initialization error                  | Power-on check   | Cannot enable motor   | Restart                                                           |
| DoubleEncoderErr     | 23  | 8388608     | 0x800000    | Dual encoder error                            | Calibration check | Cannot enable motor  | Check encoder installation, resolve installation issue, and recalibrate |
| LinerHallNotCali     | 24  | 16777216    | 0x1000000   | Linear Hall sensor not calibrated             | Power-on check   | Cannot enable motor   | Calibrate and restart                                             |
| LinerHallReversal    | 25  | 33554432    | 0x2000000   | Linear Hall sensor reversal                   | Calibration check | Cannot enable motor  | Correct phase sequence and recalibrate                            |
| LinerHallLoss        | 26  | 67108864    | 0x4000000   | Linear Hall sensor lost                       | Calibration check | Cannot enable motor  | Investigate hardware fault, repair, and restart                   |
| LinerHallWaveformErr | 27  | 134217728   | 0x8000000   | Linear Hall sensor waveform error             | Calibration check | Cannot enable motor  | Check magnetic ring installation and recalibrate                  |
| UPhaseloss           | 28  | 268435456   | 0x10000000  | Phase U missing                               | Real-time check  | Cannot enable motor   | Investigate hardware fault, repair, and restart                   |
| VPhaseloss           | 29  | 536870912   | 0x20000000  | Phase V missing                               | Real-time check  | Cannot enable motor   | Investigate hardware fault, repair, and restart                   |
| WPhaseloss           | 30  | 1073741824  | 0x40000000  | Phase W missing                               | Real-time check  | Cannot enable motor   | Investigate hardware fault, repair, and restart                   |
| EthComTimeOut        | 31  | 2147483648  | 0x80000000  | Ethernet communication timeout                | Real-time check  | Cannot enable motor   | User-initiated recovery / restart                                 |

> ℹ️ **Note**:
>
> Most error codes that can be cleared by restarting can also be cleared through the [Clear Fault](/fourier-grx-M4/docs/en/tasks/clear_fault) task.

## Extended Error Codes

Extended error codes do not currently expose any information and are reserved for internal use only.
