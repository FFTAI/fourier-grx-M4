---
layout: default
title: Changelog
nav_order: 8
has_toc: true
nav_exclude: true
---

# Changelog

{:toc}

This document records all significant updates to the Fourier-GRX-M4 SDK and its documentation.

## October 2026

### v1.2.44 (2026-10-26)

**Release**

- 📦 `fourier-grx` **v4.4.69 is now stable**: `fourier-grx-4.4.69-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-26 18:07, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.69`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.69 row and release notes; 4.4.68 moves to "No longer supported". Highlights: four new feedforward variants of the sinusoidal-trajectory and harmonic forward-walk tasks (feedforward family grows from 4 to 8); ⚠️ **the rotary-joint TIDs were regrouped** — the four basic action tasks move from 4110–4113 to 4128–4131 and PD + feedforward variants take over 4110–4113, so a given TID now maps to a different task and hosts must be updated; web task grouping is now segmented per block so locomotion and feedforward tasks are no longer mislabelled as calibration.
- 📄 The [tasks list](/fourier-grx-M4/docs/en/tasks) gains a "Rotary joint TID changes in v4.4.69" mapping table; the passive forward-walk, passive marching and harmonic forward-walk task pages have their TIDs and update logs updated; references in [run types](/fourier-grx-M4/docs/en/reference/run_type) and the [user-data interface](/fourier-grx-M4/docs/en/reference/user) corrected. Chinese and English pages updated in sync

### v1.2.43 (2026-10-26)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.69**: `fourier-grx-4.4.69-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-26 17:56, branch `m4-lfs`); install with `fourier-grx update 4.4.69-prerelease`
- ✨ **Four new feedforward tasks**: the sinusoidal-trajectory and harmonic-coefficient forward-walk tasks each gain POSITION and PD feedforward variants (TID 4124, 4110, 4127, 4113), growing the feedforward family from 4 to 8 tasks. The `JointControlMode.PD` that `sin_wave` had hardcoded is now a class attribute, which the POSITION variants override.
- ⚠️ **Rotary-joint TIDs regrouped (breaking change for integrators)**: the four basic action tasks at 4110–4113 (sinusoidal trajectory / passive forward walking / passive marching in place / harmonic forward walking) move to **4128–4131**, and the vacated 4110–4113 are taken by the corresponding PD + feedforward variants; the POSITION variants shift to 4125 / 4126. **A given TID now maps to a different task** — hosts must follow the [mapping table on the tasks page](/fourier-grx-M4/docs/en/tasks); otherwise a host that still calls 4111 will get the feedforward variant instead of passive forward walking. Assist tasks (4114–4119) and calibration tasks (4120–4123) are unchanged.
- 🐛 **Web task grouping fixed**: the grouping was derived from numeric ranges (`<4114` basic, `<4120` assist, `<4200` calibration), so after the regrouping all eight feedforward tasks and the four locomotion tasks at 4128–4131 would have shown up under "rotary joint · calibration". Now segmented per block.
- 🔧 Cleaned up references invalidated by the regrouping: harmonic planner docs 4113 → 4131, the harmonic feedforward variants' Zenoh registration note, and the menu's trailing annotations (which read the wrong way round); `user.md` now lists all four feedforward variants among the tasks that publish the gait fields, and "quantised to whole 20 ms frames" is corrected to scale with the control period (5 ms steps on the 200 Hz M4LT2).
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page points at 4.4.69; the [tasks list](/fourier-grx-M4/docs/en/tasks), [run types](/fourier-grx-M4/docs/en/reference/run_type), [user-data interface](/fourier-grx-M4/docs/en/reference/user) and the individual task pages have their TIDs updated (historical changelog bullets keep the numbering of their time). Chinese and English pages updated in sync

### v1.2.42 (2026-10-26)

**Documentation**

- 🐛 Corrected an inaccurate statement in the v4.4.68 notes: the docs said "the mark-time task keeps 0.12 s", but in fact **both the forward-walk and mark-time tasks were reduced to 0.06 s** (`fourier-grx` `8dda97da`).
- 📋 Why they differed: that change landed after the `v4.4.68` tag commit (the tag points at `ac193cf1`, where mark_time is still 0.12 s), but it **is present in the released deb binaries** (run.bin was built at 16:54 and 17:05, both after the change). The behaviour of the published 4.4.68 packages is as described here.
- 📄 Chinese and English pages updated in sync.

### v1.2.41 (2026-10-26)

**Release**

- 📦 `fourier-grx` **v4.4.68 is now stable**: `fourier-grx-4.4.68-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-26 17:08, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.68`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.68 row and release notes; 4.4.67 moves to "No longer supported". Highlights: the M4LT2 control rate is raised to 200 Hz (`control_period` 0.01 → 0.005; T1 stays at 100 Hz, P1 at 50 Hz); the hard tier is retuned to kp `[1000×4]` / kd `[60×4]` and the medium tier kp unified to `[500×4]`; the feedforward tasks (TID 4124–4127) now actually apply velocity feedforward, which never ran on their dispatch path; the joint home-position averaging window is defined in seconds; FSA v3 error codes are filtered by severity before they raise protection (⚠️ behaviour change: a level-1 warning no longer switches the task to IDLE)
- 📄 The passive forward-walk / mark-time task pages and the forward-walk / mark-time assist-adjust (adjust_dt) task pages document this release
- 📄 Chinese and English pages updated in sync

### v1.2.40 (2026-10-26)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.68**: `fourier-grx-4.4.68-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-26 16:57, branch `m4-lfs`); install with `fourier-grx update 4.4.68-prerelease`
- ✨ **M4LT2 control rate raised to 200 Hz**: `control_period` changes from `0.01` to `0.005` in each config (M4LT1 stays at 100 Hz, M4LP1 at 50 Hz). The halved loop delay allows higher position gains; protection debouncing, emergency-stop confirmation, the load-detection filter and PD ramp, and the gait smoothing filter are all defined in seconds, so their durations are unchanged once converted to cycle counts
- 🔧 **hard tier retuned** (T1/T2): kp `[800,1000,...]` → `[1000×4]`, kd `[80,50,...]` → `[60×4]` (hip ζ=0.63 unloaded / 0.52 loaded, knee ζ=1.12 / 1.04 overdamped); medium tier kp unified to `[500×4]` (kd stays `[30×4]`). M4LP1 unchanged
- 🐛 **The feedforward tasks' velocity feedforward never actually ran**: `TaskM4LRotaryJointVelocityFeedforwardMixin` injected `v_ff` only in `function_component`, but these four tasks (TID 4124–4127) are scheduled as `STANDALONE` by default, so the hook was never called. A `function_standalone` hook has been added
- 🐛 **The joint home-position averaging window** is now defined in seconds (`position_sample_time = 1.0 s`): it was a fixed 50 cycles, so the averaging duration would have shrunk from 1.0 s to 0.25 s at the higher rate, leaving encoder noise under-averaged
- 🔧 The forward-walk and mark-time reference-trajectory total delay compensation is reduced from `0.12 s` to `0.06 s` for both tasks (converted to a frame index from the control period); the delay-compensation component terms in `forward_walk` / `mark_time`, which were overwritten by a later assignment and had no effect when changed, have been removed
- 🐛 [fourier-core](https://gitlab.fftaicorp.com/rehab/fourier-core) `f09669e`: the FSA v3 error-code parser now **filters by severity** — only entries with `err_level ≥ 2` (warning-that-limits-function / error) are raised as faults and trigger protection; plain warnings (level 1) and informational entries are logged only, and status bits undefined in the error dictionary (persistent actuator status bits) are not treated as faults by default (⚠️ behaviour change vs 4.4.67: a level-1 warning no longer switches the task to IDLE, which reduces nuisance trips)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.39 (2026-10-23)

**Release**

- 📦 `fourier-grx` **v4.4.67 is now stable**: `fourier-grx-4.4.67-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-23 08:57, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.67`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.67 row and release notes; 4.4.66 moves to "No longer supported". Highlights: the FSA v3 clear-fault interface is implemented (previously a no-op); the v3 error-code parser that always returned None is fixed, so the actuator-error protection works again on M4LT2 (⚠️ behaviour change)
- 📄 Chinese and English pages updated in sync

### v1.2.38 (2026-10-23)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.67**: `fourier-grx-4.4.67-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-23 08:46, branch `m4-lfs`); install with `fourier-grx update 4.4.67-prerelease`
- 🐛 What changed (fourier-core `46854a6`): **the FSA v3 clear-fault interface is now implemented** (it was a no-op; faults are now cleared via Disable → Enable(NONE)); **fixed the v3 error-code parser returning None unconditionally** — actuator error codes now propagate to the robot layer again, so the actuator-error protection actually triggers on M4LT2 (⚠️ behaviour change: an actuator fault on T2 now switches the task to IDLE); error codes are decoded and logged only on change, eliminating log spam at the 500 Hz subscription rate
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.37 (2026-10-22)

**Release**

- 📦 `fourier-grx` **v4.4.66 is now stable**: `fourier-grx-4.4.66-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-22 20:44, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.66`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.66 row and release notes; 4.4.65 moves to "No longer supported". Highlights: a new medium PD tier used end-to-end by the assist_adjust_dt tasks instead of hard (⚠️ behaviour change — the assist feel is softer); T1/T2 hard-tier hip kd raised to 80 (ζ 0.94)
- 📄 The assist-adjust task pages document the medium tier

### v1.2.36 (2026-10-22)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.66**: `fourier-grx-4.4.66-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-22 20:32, branch `m4-lfs`); install with `fourier-grx update 4.4.66-prerelease`
- ✨ What changed: **a new medium PD tier — the assist_adjust_dt Forward Walk / Mark Time tasks now use medium instead of hard for the whole task** — in the human-led, robot-follows assist scenario the hard tier was too stiff and fought the user; the medium tier is kp `[400,500,400,500]` / kd `[30×4]` on T1/T2 and kp `[350×4]` / kd `[30,25,30,25]` on M4LP1, and it no longer ramps with load detection; **T1/T2 hard-tier hip kd raised from 50 to 80**, eliminating the underdamped hard tier (no-load hip ζ 0.47 → 0.94, loaded 0.77)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.35 (2026-10-22)

**Release**

- 📦 `fourier-grx` **v4.4.65 is now stable**: `fourier-grx-4.4.65-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-22 12:00, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.65`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.65 row and release notes; 4.4.64 moves to "No longer supported". Highlights: new feedforward variants of Forward Walk / Mark Time (TID 4124–4127, POSITION_FF / PD_FF); hard tier retuned to kp `[800,1000]` / kd `[40,50]`; the POSITION chain forwards velocity_ff end to end
- 📄 The [Forward Walk (Passive)](/fourier-grx-M4/docs/en/tasks/forward_walk_passive) and [Mark Time (Passive)](/fourier-grx-M4/docs/en/tasks/mark_time_passive) pages document the new variants

### v1.2.34 (2026-10-22)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.65**: `fourier-grx-4.4.65-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-22 11:49, branch `m4-lfs`); install with `fourier-grx update 4.4.65-prerelease`
- ✨ What changed: **new feedforward variants of Forward Walk / Mark Time (TID 4124–4127)** — the velocity feedforward is derived by numerically differentiating the actually-commanded target and clamped to the protection velocity; the POSITION_FF variants run the position loop + v_ff (PID values centralised in the robot parameter class, M4LP1 tuned separately), the PD_FF variants keep PD + v_ff (kd × target velocity as an equivalent feedforward torque — note the FSA v2 fast protocol has no velocity field, so the feedforward is inert on P1/T1 and active on T2). Also: the POSITION chain now forwards velocity_ff end to end (fourier-core `ad7f1c0`); **the hard tier is retuned to kp `[800,1000]` / kd `[40,50]`** (knee ζ=0.93; hip ζ=0.47, underdamped — as tuned on the real robot); forward walk gains an optional track-deviation statistic (off by default)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.33 (2026-10-21)

**Release**

- 📦 `fourier-grx` **v4.4.64 is now stable**: `fourier-grx-4.4.64-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-21 16:00, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.64`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.64 row and release notes; 4.4.63 moves to "No longer supported". Highlights: zero-displacement guard for the prismatic move_length / move_offset tasks (fixes NaN commands); move_min / move_max command clamp relaxed 0.25 → 0.5 mm per cycle
- 📄 Chinese and English pages updated in sync

### v1.2.32 (2026-10-21)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.64**: `fourier-grx-4.4.64-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-21 15:47, branch `m4-lfs`); install with `fourier-grx update 4.4.64-prerelease`
- 🔧 What changed: **zero-displacement guard for the prismatic move_length / move_offset tasks** — with a zero target displacement the sweep period becomes 0 and the old code produced NaN position commands; the task now holds the current position and completes immediately; **the per-cycle command-change clamp of prismatic move_min / move_max is relaxed from 0.25 mm to 0.5 mm**, speeding up torque build-up once the joint is pressed against the hard stop (note the value is per-cycle: 25 mm/s on P1 at 50 Hz, 50 mm/s on T1/T2 at 100 Hz)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.31 (2026-10-20)

**Release**

- 📦 `fourier-grx` **v4.4.63 is now stable**: `fourier-grx-4.4.63-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-20 21:56, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.63`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.63 row and release notes; 4.4.62 moves to "No longer supported". Highlight: the gait smoothing filter and delay compensation are defined in physical units and scale with the control period, completing the adaptation to the T1/T2 100 Hz control rate (50 Hz models essentially unchanged)
- 📄 Chinese and English pages updated in sync

### v1.2.30 (2026-10-20)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.63**: `fourier-grx-4.4.63-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-20 21:35, branch `m4-lfs`); install with `fourier-grx update 4.4.63-prerelease`
- 🔧 What changed: **the gait-trajectory smoothing filter and delay compensation are now defined in physical units and scale with the control period** — the smoothing filter's hardcoded alpha=0.25 becomes a 2.5 Hz cutoff folded through a first-order EMA (equivalent to 0.2696 at 50 Hz, close to the old value; identical frequency response at 100 Hz), and the total delay compensation's hardcoded -6 frames becomes 0.12 s of physical time (still -6 frames at 50 Hz, -12 at 100 Hz — same delay in seconds). This completes the adaptation to the 100 Hz control rate introduced in 4.4.62; 50 Hz models are essentially unchanged
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.29 (2026-10-20)

**Release**

- 📦 `fourier-grx` **v4.4.62 is now stable**: `fourier-grx-4.4.62-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-20 20:38, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.62`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.62 row and release notes; 4.4.61 moves to "No longer supported". Highlights: the T1/T2 control rate goes to 100 Hz (⚠️ behaviour change, with the timing-adaptation prerequisites shipping in this same version); hard-tier hip kp raised to 700; the load-detection PD ramp rounding stall is fixed (kp/kd now reach the hard tier exactly); M4LP1 is unaffected
- 📄 Chinese and English pages updated in sync

### v1.2.28 (2026-10-20)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.62**: `fourier-grx-4.4.62-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-20 20:27, branch `m4-lfs`); install with `fourier-grx update 4.4.62-prerelease`
- 🔧 What changed: **M4LT1/T2 control rate raised from 50 Hz to 100 Hz** (`control_period: 0.02 → 0.01`; prerequisites included: calibration-task dt wiring fix and time-based protection debounce / load detection, so timing behaviour at 100 Hz matches 50 Hz; the 400 Hz SDK server configs and the 50 Hz communication loop are unchanged); **hard-tier hip kp raised from 500 to 700** (kd 50 unchanged); **the load-detection PD ramp no longer stalls on integer rounding** — previously kp froze at ~450 and kd never moved, now a 0.01 minimum step carries both exactly to the hard tier; T1/T2 baseline kd made symmetric `[35,25,35,25]`. M4LP1 is unaffected (control rate stays 50 Hz, baseline 250/25, hard hip kp 500 / kd 45)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.27 (2026-10-20)

**Release**

- 📦 `fourier-grx` **v4.4.61 is now stable**: `fourier-grx-4.4.61-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-20 18:59, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.61`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.61 row and release notes; 4.4.60 moves to "No longer supported". Highlights: the T1/T2 rotary baseline gain becomes a standalone medium tier (softer start-up — ⚠️ behaviour change); hard-tier hip kd raised to 50; M4LP1 unaffected
- 📄 Chinese and English pages updated in sync

### v1.2.26 (2026-10-20)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.61**: `fourier-grx-4.4.61-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-20 18:48, branch `m4-lfs`); install with `fourier-grx update 4.4.61-prerelease`
- 🔧 What changed: **the M4LT1/T2 rotary baseline gain becomes a standalone medium tier** (kp `[350×4]`, kd `[35,25,55,25]`, tuned per leg on real hardware) instead of starting directly from the hard tier — softer no-load start-up, more compliant feel; the load-detection auto-adjust still ramps toward the hard tier. Hard-tier hip kd goes from 45 to 50 (no-load ζ 0.67 → 0.75). A new `algo_rotary_pd_medium` tier is declared (not yet referenced by any task mapping). M4LP1 is unaffected (baseline stays 250/25, hard hip kd 45)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.25 (2026-10-20)

**Release**

- 📦 `fourier-grx` **v4.4.60 is now stable**: `fourier-grx-4.4.60-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-20 17:13, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.60`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.60 row and release notes; 4.4.59 moves to "No longer supported". Highlight: hip-joint hard-tier kd raised from 30 to 45, eliminating the no-load high-frequency vibration (ζ 0.45→0.67); ⚠️ behaviour change — all T1 / T2 rotary tasks get more hip damping and feel steadier
- 📄 Chinese and English pages updated in sync

### v1.2.24 (2026-10-20)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.60**: `fourier-grx-4.4.60-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-20 16:43, branch `m4-lfs`); install with `fourier-grx update 4.4.60-prerelease`
- 🔧 What changed: **hip-joint hard-tier kd raised from 30 to 45**, eliminating the no-load high-frequency vibration. Pinocchio CRBA analysis shows the hip's effective inertia is 2.25 kg·m² (about 3× the knee's); at kp=500 / kd=30 the hip's damping ratio was ζ=0.45 (underdamped, phase margin only 19°) — with kd=45 it becomes ζ=0.67, PM≈41°. The knee keeps kd=30 (J=0.72 kg·m², ζ=0.79 already adequate). M4LP1 baseline (250/25) unaffected; M4LT1/T2 baseline (hard copy) follows automatically. Stall torque unchanged (kp untouched); extra heat dissipation negligible (< 1 W during normal walking)
- 📄 The "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.23 (2026-10-20)

**Release**

- 📦 `fourier-grx` **v4.4.59 is now stable**: `fourier-grx-4.4.59-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-20 14:48, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.59`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.59 row and release notes; 4.4.58 moves to "No longer supported". Highlights: fixes the prismatic-joint auto calibration not moving the motor and a position-protection false trigger mid-sweep in the rotary calibration (both present since v4.4.49 — **machines whose prismatic joints were auto-calibrated on v4.4.49 – 4.4.58 should be recalibrated after upgrading**); otherwise identical to 4.4.58
- 📄 The [Prismatic Joint Zero Calibration](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint) and [Rotary Joint Auto Calibration](/fourier-grx-M4/docs/en/tasks/rotary_joint_auto_calibrate) pages drop the "stable release pending" notes and link to the release page

### v1.2.22 (2026-10-20)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.59**: `fourier-grx-4.4.59-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-20 14:37, branch `m4-lfs`); install with `fourier-grx update 4.4.59-prerelease`
- 🔧 What changed: **fixed the prismatic-joint auto calibration not moving the motor**. The task-layer output clamp introduced in v4.4.49 (to stop gait generators from commanding beyond hardware limits) broke the calibration sweep design of "commanding ±0.2 m past the software limits to press the joint against the mechanical hard stop" — the prismatic stroke is only 0.098 m, so once the joint is at/near the limit the clamped target equals the measured position, the motor never moves, and the velocity-only criterion then falsely reports arrival and zeroes the wrong point. Calibration sweep tasks (prismatic MoveMin / MoveMax, rotary BorderAndReturn) are now exempt from the clamp and regain their overshoot commands; the rotary sweep's position-protection bounds are widened from "position at activation ± 0.25 rad" to "hardware limits ± margin" so a long sweep no longer trips the protection into servo-off mid-way; the MoveMax arrival log text is fixed (min→max); the progress log now prints in 1% steps instead of every control cycle (≈6000 → ≈100 lines per sweep)
- 📄 Update logs on the [Prismatic Joint Zero Calibration](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint) and [Rotary Joint Auto Calibration](/fourier-grx-M4/docs/en/tasks/rotary_joint_auto_calibrate) pages and the "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.21 (2026-10-20)

**Release**

- 📦 `fourier-grx` **v4.4.58 is now stable**: `fourier-grx-4.4.58-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-20 13:34, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.58`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.58 row and release notes; 4.4.57 moves to "No longer supported". Highlight: the velocity-only arrival timer of the prismatic-joint calibration goes from 5 s to 25 s, removing the premature "arrived" call up to ~3.5 mm before the hard stop in the tail of the sweep; otherwise identical to 4.4.57
- 📄 The [Prismatic Joint Zero Calibration](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint) page drops the "stable release pending" note and links to the release page

### v1.2.20 (2026-10-20)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.58**: `fourier-grx-4.4.58-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-20 13:23, branch `m4-lfs`); install with `fourier-grx update 4.4.58-prerelease`
- 🔧 What changed: **the velocity-only arrival timer of the prismatic-joint calibration goes from 5 s to 25 s**. In the tail of the 120 s S-curve profile (r > 0.8295) the reference velocity naturally drops below the 0.001 m/s threshold for about 20.5 s, so with a 5 s continuous window a joint that had not yet touched the limit could be falsely declared "arrived" — at the latest around start + 104.5 s, roughly 3.5 mm before the hard stop — corrupting the zero calibration. A 25 s window exceeds that tail window and eliminates the false trigger; the cost is that the low-torque fallback now fires 25 s (instead of 5 s) after contact
- 📄 The arrival-criteria table and update log on the [Prismatic Joint Zero Calibration](/fourier-grx-M4/docs/en/tasks/calibrate_home_prismatic_joint) page and the "current pre-release" line on the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page updated accordingly

### v1.2.19 (2026-10-19)

**Release**

- 📦 `fourier-grx` **v4.4.57 is now stable**: `fourier-grx-4.4.57-linux-arm64-cpu-m4l-blaze.deb` (built 2026-10-19 17:49, branch `m4-lfs`); install with `fourier-grx update` (auto probe) or `fourier-grx update 4.4.57`
- 📋 The [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) gains the 4.4.57 row and release notes; 4.4.54 moves to "No longer supported". Highlights: the M4LP1 start-up crash is fixed (affected range v4.4.52 – 4.4.56-prerelease — **on P1, upgrade directly to v4.4.57**); the Harmonic-Coefficient Forward Walk task 4113 and planner 4407 become generally available; the rotary-joint PD hard-tier kp is flattened to `[500,500,500,500]` (lower T1 / T2 start-up stiffness — ⚠️ behaviour change)
- ℹ️ Everything from the v4.4.55 / v4.4.56 prerelease cycles ships as stable in this version; 4.4.55 and 4.4.56 never got their own stable releases
- 📄 The [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic) and [Planner](/fourier-grx-M4/docs/en/tasks/planner) pages drop the "stable release pending" notes and link to the release page

### v1.2.18 (2026-10-19)

**Release**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.57**: `fourier-grx-4.4.57-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-19 17:35, branch `m4-lfs`); install with `fourier-grx update 4.4.57-prerelease`
- 🔧 What changed: **the rotary-joint PD hard-tier kp is flattened to 500**. In the M4LP1 and M4LT1/T2 parameter classes the hard tier goes from `[600,500,600,500]` (hip/knee split) to `[500,500,500,500]`; kd stays `[30,30,30,30]`. On M4LT1 / M4LT2 the rotary baseline gain is a copy of the hard tier, so the start-up gain of every rotary task (stand / forward walk / mark time / calibration / test) drops from hip 600 · knee 500 to a flat 500 — the motion feels softer. M4LP1 keeps its soft `[250×4]` baseline; only its load-ramp target changes to a flat 500. The buttery / soft compliance interpolation of the assist_adjust_pd tasks is unaffected
- 📄 Version notes on the [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic), [Planner](/fourier-grx-M4/docs/en/tasks/planner) and [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) pages updated accordingly

### v1.2.17 (2026-10-19)

**Documentation Improvements**

- Rewrote the root README with the repository scope, online documentation links, documentation navigation, example categories, directory structure, and contribution information
- Completed the Chinese and English Quick Start indexes with device-state-based routes to the existing installation, upgrade, flashing, and model workflows, plus post-installation next steps
- Clarified the roles of the local `demo/` examples and the external `Wiki-GRx-Deploy` examples, and fixed child-page navigation configuration on the Chinese examples index
- Expanded the Chinese and English contributing guides with issue-reporting details, bilingual synchronization, front matter, and pre-submission check requirements

### v1.2.16 (2026-10-16)

**Release and defect fix**

- 📦 The pre-release channel moves to `fourier-grx` **v4.4.56**: `fourier-grx-4.4.56-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-16 12:35, branch `m4-lfs`); install with `fourier-grx update 4.4.56-prerelease`
- 🐛 Fixed the M4LP1 control thread exiting right after start: the joint-protection debounce counters and thresholds were initialised in `RobotM4L._init_actuator()`, but `RobotM4LP1` overrides that method wholesale without calling `super()`, so `flag_joint_over_load_protection_counter_threshold` was never created and the control thread raised `AttributeError` on the first control cycle. The counters are now initialised in the base constructor, where a variant override of `_init_actuator()` cannot skip them; the velocity and position protection counters sat on the same risk (hidden only because their reads are behind an enable switch) and are fixed the same way. M4LT1 / M4LT2 do not override the method and were never affected
- ⚠️ **Do not install `4.4.55-prerelease` on M4LP1**; the defect is present in v4.4.52 through v4.4.55. On P1 use `4.4.56-prerelease` or later
- 📄 Version notes on the [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic), [Planner](/fourier-grx-M4/docs/en/tasks/planner) and [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) pages updated accordingly

### v1.2.15 (2026-10-16)

**Release**

- 📦 A **prerelease build of `fourier-grx` v4.4.55** has been built and uploaded to the pre-release channel: `fourier-grx-4.4.55-linux-arm64-cpu-m4l-prerelease.deb` (built 2026-10-16 11:35, branch `m4-lfs`, `X-Variant` = `linux-arm64-cpu-m4l-prerelease`)
- ⬇️ Install with `fourier-grx update 4.4.55-prerelease`, then run `fourier-grx install` to deploy. The package is not found by the argument-free automatic probe of `fourier-grx update` and is not listed in the [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx)
- ✨ Contents: the [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic) task (TID 4113) and its [planner](/fourier-grx-M4/docs/en/tasks/planner) (TID 4407), 5 new gait level echo fields in `rehab/server`, and a widened deactivation clear covering `rehab.gait_*`
- ✅ Shipped as stable with **v4.4.57** (2026-10-19); the download link is in the [firmware version table](/fourier-grx-M4/docs/en/release/fourier-grx) (4.4.55 / 4.4.56 never got their own stable releases)

### v1.2.14 (2026-10-16)

**Documentation Updates**

- ➕ Added the **Harmonic-Coefficient Forward Walk planner (TID 4407)** to the [Planner](/fourier-grx-M4/docs/en/tasks/planner) page: the plan-only counterpart of 4113. The three panel levels (`param_1` amplitude / `param_2` knee restriction / `param_3` cadence) are still applied every control cycle, but no joint commands are sent, so the host can preview the joint envelopes of all 4 × 4 = 16 curves and the 6 cadence levels before the patient starts moving. Includes the full reported-field table and the 4 × 4 envelope table
- 🔧 Documented two previously undocumented planner behaviours: although the planner does not drive the joints, it still merges the trajectory into the joint position protection envelope every control cycle (widening only, restored on reset); and the deactivation clear now covers all `rehab.gait_*` level echo fields
- 📡 The publisher of the 5 gait echo fields in the `rehab/server` status table is now listed as "4113 / 4407" instead of "4113"
- 🔧 Fixed the description of the 4 reference-trajectory array fields in `rehab/server`: added the element order **[hip_L, knee_L, hip_R, knee_R]** (length 4 for every gait task — verified across 4111 / 4112 / 4113 / 4116 / 4117 / 4301 / 4302 / 4401 / 4407 / 4501, the whole family is consistent), and corrected the scope of `reference_joint_position_max/min` from "the entire trajectory" to "the cyclic segment (start and end transitions excluded)", matching what the code actually does
- ✅ The above became generally available with **v4.4.57** (2026-10-19; previously shipped through the 4.4.55 – 4.4.57 prerelease builds)

### v1.2.13 (2026-10-16)

**Documentation Updates**

- ➕ Added the task page [Harmonic-Coefficient Forward Walk](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic) (TID 4113, M4L): replays Fourier harmonic-coefficient gait curves with three orthogonal panel levels — **hip swing amplitude** (`param_1`), **knee restriction** (`param_2`) and **cadence** (`param_3`); cadence spans 22.9 ~ 49.2 steps/min, i.e. the required 2.45 ~ 5.25 s per stride. Chinese and English pages added, along with the task table and index entries
- 📡 Documented 5 new gait echo fields in the `rehab/server` status table: `gait_name`, `gait_amplitude_level`, `gait_knee_restriction_deg`, `gait_speed_level`, `gait_stride_time_s`
- ⚠️ This feature is available from `fourier-grx` v4.4.55 (this entry was written before the version number was assigned and said "later than v4.4.54"; it is now fixed as v4.4.55, see v1.2.15); once the stable release ships, add its download link to the [Fourier-GRX firmware](/fourier-grx-M4/docs/en/release/fourier-grx) table

### v1.2.12 (2026-10-15)

**Documentation Updates**

- 📦 `fourier-grx` v4.4.54 officially released (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx#4454) release page); v4.4.53 moved to unsupported. This is a bug-fix release: torque protection works again in the knee-restriction tasks 4301 / 4302, the assist coefficient is adjustable again in 4303 / 4304 / 4305, mark time (4112) honours the panel pause command, and the `communication` section was added to `*_sdk.yaml` so the SDK User API UDP channel works again
- 🔧 Retracted the "this interface has no effect" notes on the 6 affected task pages and restored the "Pause motion flag" parameter and interface-mapping rows that had been removed from the 4112 page (both languages)

---

### v1.2.11 (2026-10-15)

**Documentation fixes**

- 🔧 **Command Line Tool**: removed the non-existent `setup_conda` in favour of `setup_uv` / `setup_uv_py310` and added the `web` sub-command; corrected `fourier-grx update <variant>` to `update <version>` and `update <version>-<channel>` (the variant is always read automatically and cannot be passed as an argument); added "The Two Layers of Installation" explaining that `sudo dpkg -i` only updates `/usr/share/fourier-grx/` while `fourier-grx install` deploys the new version into `~/fourier-grx/`; added the `fourier-grx web` option table (`--host` is the robot IP, `--bind` is the web listen address, `0.0.0.0:8000` by default)
- 📦 The Fourier-GRX latest version on the [Firmware Releases](/fourier-grx-M4/docs/en/release) page corrected from 4.4.43 to **4.4.53**; added a "Pre-release Channel" section to the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx#pre-release-channel) page — `-prerelease` replaces only the build-type segment at the end of `X-Variant`, keeping the model segment, which is why the automatic probe never finds pre-release builds; v4.4.52 was never officially released and has no download link
- 🆕 Added a "Web Debugging over the LAN" section to the [M4L Robot](/fourier-grx-M4/docs/en/quickstart/m4l#web-debugging-over-the-lan) quick start: starting `fourier-grx web` and auto discovery, live state, task dispatch, the virtual panel, the run log, and a safety note about latched values
- 🔧 **Firmware Update**: documented `fourier-grx update <version>-prerelease`; noted that `fourier-grx install` first backs `~/fourier-grx` up to `~/fourier-grx-bak` and prefers to reuse the old configuration, and that network parameters are reset unconditionally to the static IP
- 🔧 **Run Type**: added run type `B` server mode (`server`); the offline debug mode (`offline`) number corrected from `B` to `C`
- 🔧 **Configuration File**: corrected the defaults and options of `dynalink: enable`, `joystick_type`, `keyboard_type`, `robot: name` and the communication period, and added `use_virtual_panel` / `use_virtual_user`
- 🔧 Development environment FAQ: minimum GLIBC corrected from 2.33 to 2.34
- 🗑️ Removed the empty "Video Tutorial" sections from the M4 / M4L quick start pages
- 🔗 Download link audit: builds earlier than 4.4.40 (including 4.4.41) have been removed from the download server (404 confirmed); the Download column of those 32 versions on the [Firmware Releases page](/fourier-grx-M4/docs/en/release/fourier-grx) now reads "Delisted" while the version rows and their release notes stay available; the `wget` examples in the quick start pages now use 4.4.53, which is still online
- 🐞 **Task documentation corrections**: the "pause motion" interface `grx.virtual_panel_command_pause` documented for TID 4112 is never read by that task and has been removed from its parameter and interface tables; in the knee-restriction family, torque protection (4301 / 4302) and the assist coefficient (4303 / 4304 / 4305) are not wired into the algorithm call in the current firmware, and the pages now state this explicitly together with a substitute task; the behaviour after a torque-protection trigger is corrected from "pauses the task" to "exits immediately and returns to `TASK_IDLE`"; the missing `rehab.step_frequency` state interface was added to 12 gait task pages; `dsp_ratio` is now marked as not applicable on tasks that use the vhip gait generator
- 🔧 **Sample code**: the conda instructions in `demo/user` and `demo/developer` were replaced with `setup_uv` and `source $HOME/fourier-grx/.venv/bin/activate`; `demo_set_home.py` and `demo_test_joint.py` send TID 999 / 902, which no M4L task registers, and now explain this and point to the substitutes (4103 / 4203, 4100 / 4200); `demo/udp/demo_get_state.py` now drains the receive queue continuously (state is pushed at roughly 250 packets/s, so receiving one packet per sleep only ever prints data that is seconds old); `config_M4L_T1_developer.yaml` gained the missing `fi_ioboard` section, and the meaning of `log_level: "none"` is corrected (it means every message is logged, not silence)
- 🔧 **Version attribution in task changelogs**: corrected to "the first release that contains the change" — the knee-restriction family v4.2.5 → v4.2.6, stand motion control v3.0.3 → v3.1.1, 4103 / 4206 v4.1.18 → v4.1.19; servo on / off / reboot and clear-fault already existed in v2.0.5, the earliest release in the public history, so those entries no longer claim an "added in" version
- 🌐 **Language switching**: fixed the "EN" button on the Chinese home page (which sits at the site root) pointing back at the current page, and the "中文" button on the English home page pointing at a page that does not exist

---

### v1.2.10 (2026-10-14)

**Documentation Updates**

- 📦 `fourier-grx` v4.4.53 officially released: its release notes and download link have been added, and v4.4.51 moved to unsupported (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)
- 📖 The pre-release channel syntax `fourier-grx update <version>-prerelease` is available since v4.4.53; earlier versions must install manually with `sudo dpkg -i`
- ℹ️ v4.4.52 was never officially released; the version number goes directly from 4.4.51 to 4.4.53

---

### v1.2.9 (2026-10-14)

**Documentation Updates**

- 📖 **Release entries backfilled**: added the Chinese and English release notes for the three already officially released versions v4.4.49 (built-in web debugging host, configuration preserved on upgrade), v4.4.50 (web UI second-level grouping / Chinese parameter labels / virtual user leg length commands), and v4.4.51 (virtual panel draft mode)
- 🆕 **New task documentation**: left-leg / right-leg separate manual rotary joint calibration `TASK_ROTARY_JOINT_MANUAL_CALIBRATE_LEFT_LEG` (4122) / `TASK_ROTARY_JOINT_MANUAL_CALIBRATE_RIGHT_LEG` (4123); the Chinese and English task indexes and the manual calibration task page are updated accordingly; these two tasks are available since v4.4.53
- ℹ️ **About v4.4.52 / v4.4.53**: these two versions currently provide pre-release builds only (not listed in the download lists on this page). Pre-release builds are not discovered by the automatic probing of `fourier-grx update` and must be installed explicitly: `fourier-grx update <version>-prerelease` (e.g. `fourier-grx update 4.4.53-prerelease`). Download links will be added following this page's conventions once they are officially released

---

### v1.2.8 (2026-10-10)

**Documentation Updates**

- 📖 Added documentation for the new gait task parameter interfaces (corresponding to `fourier-grx` v4.4.48): Base height base_height (`grx.virtual_panel_command_param_6`), step lift height step_height (`grx.virtual_panel_command_param_7`, forward-walk tasks only), and double-support ratio dsp_ratio (`grx.virtual_panel_command_param_8`, forward-walk tasks only, effective only for the DSP gait generator); covers the forward walk, assist forward walk, knee-restriction forward walk, mark time, and assist mark time task pages, with Chinese and English documentation updated in sync

---

### v1.2.7 (2026-10-10)

**New Features**

- 📈 The `rehab/server` interface adds a `step_frequency` field: gait tasks (forward-walk / mark-time families) and trajectory Planner tasks automatically derive and report cadence (steps/min) in real time, updating with step length / speed commands and automatically cleared to 0 on task exit. The host PC can use it for cadence display and training-volume statistics (see [User Interface](/fourier-grx-M4/docs/en/reference/user) for details)

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.47` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

### v1.2.6 (2026-10-10)

**Improvements**

- ⚙️ Overload protection (over_load) now debounced by 5 control cycles: the protection triggers only when the joint effort exceeds the threshold for 5 consecutive control cycles (100 ms), preventing false triggers from current/torque measurement spikes; for sustained overload, the safety semantics of re-forcing servo-off every 5 cycles are preserved

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.46` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

### v1.2.5 (2026-10-10)

**Improvements**

- ⚙️ Velocity protection threshold calibrated from 15 rad/s to **4.5 rad/s** (~258°/s): based on hardware measurements — normal gait peaks at ~3.5 rad/s and the maximum manual pull speed is ~240–260°/s; the old value exceeded the actuator's physical speed limit and could never trigger
- ⚙️ Position protection margin calibrated from 0.35 rad to **0.25 rad** (~14.3°): based on hardware measurements — a deviation beyond 15° is already the extreme, covering the worst-case tracking error of ~0.21 rad
- ⚙️ Position protection bounds and task-layer target positions are now clamped to the hardware joint limits, preventing out-of-limit commands under extreme parameter combinations

**Fixes**

- 🐛 Fixed a safety hazard where the gait generator's `atan2` branch jump caused violent joint whipping: during long-step + slow-speed stop transitions the measured joint velocity could reach 12.5 rad/s; per-frame unwrap reduces it to 0.95 rad/s

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.45` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

### v1.2.4 (2026-10-08)

**New Features**

- 🛡️ Added joint velocity protection: continuously monitors the velocity of the 4 rotary joints; if the velocity exceeds the threshold (default 15 rad/s, tunable on hardware) for 5 consecutive control cycles, all actuators are disabled and the robot enters the protection state
- 🛡️ Added joint position protection: if a joint position goes far beyond the reasonable motion range published by the active task (which adapts automatically to the task and gait parameters), all actuators are disabled and the robot enters the protection state
- 🔧 Both protections set independent flags (`flag_robot_velocity_protection` / `flag_robot_position_protection`) and latch the protection state; the host can clear them via `clear_flag_robot_velocity_protection` / `clear_flag_robot_position_protection` to resume control
- 📖 See the [Velocity & Position Protection](/fourier-grx-M4/docs/en/reference/protection) documentation

**Fixes**

- 🐛 Fixed the overload protection (`flag_robot_over_load`) clear request not taking effect: previously, after the host wrote `clear_flag_robot_over_load`, the robot-side flag was never cleared and was set again at the next communication cycle

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.44` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

## September 2026

### v1.2.3 (2026-09-01)

**Optimizations**

- ⚙️ Refined host heartbeat timing logic: the heartbeat timeout now starts counting from the **first** received `host_heartbeat_counter`; before that, disconnect protection is not triggered

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.43` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

## August 2026

### v1.2.2 (2026-08-28)

**New Features**

- 🛡️ Added host heartbeat and disconnect protection:
  - New writable field `host_heartbeat_counter` in the `comm` topic; the host keeps writing it to maintain the connection
  - New read-only fields `host_heartbeat_timeout` (default 6.0 s) and `host_heartbeat_connection_lost`
  - Automatically triggers emergent stop on timeout: standard robots enter `TASK_SERVO_OFF`, M4LT2 enters high-damping soft braking
  - The HEX protocol `HEART_BEAT` command also refreshes the heartbeat timer
  - See the [Communication Interface](/fourier-grx-M4/docs/en/reference/communication) documentation for details

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.42` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

### v1.2.1 (2026-08-12)

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.40` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page)

---

### v1.2.0 (2026-08-07)

**Documentation Updates**

- 📖 English documentation fully completed and synchronized:
  - All Task Description pages synced with the latest Chinese content, and missing English pages translated
  - English FAQ and Usage Guide restructured to match the Chinese child-page layout (from a single consolidated page to index + child pages)
  - Quickstart, Firmware Releases, and Examples pages synced with recent Chinese changes
- 📖 Firmware release support policy updated: on the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) page, only the latest version is marked as "Active"; all historical versions are now marked "No longer supported" (downloads and release notes remain available for reference)
- 📖 New task pages: [Manual Calibrate (Rotary Joint)](/fourier-grx-M4/docs/en/tasks/rotary_joint_manual_calibrate) (TID 4121) and [Move by Offset (Prismatic Joint)](/fourier-grx-M4/docs/en/tasks/move_offset_prismatic_joint) (TID 4207); task index order updated accordingly
- 📖 New [Network Connection and Remote Login](/fourier-grx-M4/docs/en/usage/network_connection) guide: sharing a network without a router, automatic static IP (`192.168.137.220`) on the 20260805 image, web terminal (`:7681`), and SSH login credentials
- 📖 System image updated to 20260805; [Firmware Installation](/fourier-grx-M4/docs/en/quickstart/firmware_install) / [Firmware Update](/fourier-grx-M4/docs/en/quickstart/firmware_update) pages now include network sharing + SSH login instructions
- 📖 Fixed 6 task documentation descriptions that were inconsistent with the code implementation

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.39` (see the [Fourier-GRX Firmware](/fourier-grx-M4/docs/en/release/fourier-grx) release page for the changes in versions 4.4.21 ~ 4.4.39)
- 📦 `ioboard` updated to `1.0.0.3` (see [IO Board Firmware](/fourier-grx-M4/docs/en/release/ioboard))

---

## June 2026

### v1.1.8 (2026-06-30)

**Changed**

- 🔧 **Stand task warm-up time shortened**: `STAGE_WARM_UP` damping transition duration reduced from `0.5 s` to `0.2 s`

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.20`

---

### v1.1.7 (2026-06-30)

**Added**

- ✨ **`fourier-grx update <version>` installs a specific version directly**: the variant is automatically read from the installed package, no manual specification needed. Example: `fourier-grx update 4.4.14`

**Improved**

- 🔧 **`fourier-grx update` probing range optimized**: patch probing expanded to +20 (miss=5); minor version only probes minor+1; major version only probes major+1.0.y; worst-case request count reduced from ~76 to ~36

**Fixed**

- 🐛 **`fourier-grx install` broken**: fixed an accidentally deleted `if [ $# -eq 0 ]` guard line that caused all subcommands to execute when the script was loaded

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.19`

---

### v1.1.6 (2026-06-30)

**Fixed**

- 🐛 **Stand task enable impact (complete fix)**: `STAGE_INIT`, `STAGE_START`, and `STAGE_WARM_UP` all set `kp=0`, ensuring a complete pure-damping transition regardless of the activation path. `STAGE_INIT` now also assigns `output_joint_position = measured_position`, preventing PD frames from targeting a zero-initialized stale cache; `STAGE_WARM_UP` lasts 0.5 s and, on timeout, interpolates from the current measured position into the motion stage. Log output now carries a stage prefix for easier field debugging

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.14`

---

### ~~v1.1.5 (2026-06-30)~~ *(revoked)*

> `STAGE_WARM_UP` was placed incorrectly (based on a misunderstanding of FSM stage management; `reset()` should not drive stage switching). Corrected in v1.1.6.

---

### ~~v1.1.4 (2026-06-29)~~ *(revoked)*

> `kp=0` lasted only one tick, which was not enough to suppress the impact; and `STAGE_INIT` no longer triggered on the second activation. Fully fixed in v1.1.6.

---

### ~~v1.1.3 (2026-06-29)~~ *(revoked)*

> The change in v1.1.3 that preset actuator target positions in `function_on_activate` was verified to be ineffective: the `SERVO_ON` communication frame only carries the enable command and no position data, so the change was reverted in v1.1.4.

---

## May 2026

### v1.1.2 (2026-05-14)

**New Features**

- 🔍 **Firmware version check flags**: `DynalinkGRX` gained `flag_version_check_error` (`0` = normal / `1` = error) and `version_check_error_info` (list of error details), automatically set when IOBoard / FSA / FSE firmware versions mismatch, do not respond, or fail to query, and synced to the host via Dynalink `read_fields`

**Version Updates**

- 📦 `fourier-grx` updated to `4.4.6`

---

### v1.1.1 (2026-05-11)

**New Features**

- ⚙️ **Configurable assist trigger force interface for Mark Time Assist (DT mode)**: Added `assist_trigger_force_upper` (acceleration trigger force, default `2.0 Nm`) and `assist_trigger_force_lower` (deceleration trigger force, default `1.0 Nm`) as configurable parameters, set via upper-level panel `param_4` and `param_5`. Applicable tasks: TID 4119 (Assisted Marching in Place, adjust DT), TID 4306 (Knee Restriction Assisted Marching in Place, adjust DT). See [Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt) and [Knee Restriction Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

**Algorithm Fix**

- 🔧 **Assist trigger force threshold changed to absolute torque value**: Formula changed from `G[i] + offset` to `G[i] * 0.0 + offset` (gravity component zeroed). Experimental testing showed that including the gravity term `G[i]` caused system instability; it is now zeroed out and the configured value is used directly as the acceleration/deceleration trigger threshold

**Behavior Clarification**

- 📌 Clarified parameter update timing: all task parameters (step height, walk period, assist ratio, trigger forces, etc.) are read **once when the task is triggered** and do not refresh in real time; the task must be re-triggered for new values to take effect

**Documentation Updates**

- 📖 Updated [Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt): renamed parameters from "trigger force upper/lower offset" to "trigger force upper/lower", updated threshold description, added G[i] zeroing rationale
- 📖 Updated [Knee Restriction Mark Time Assist (DT)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt): same as above
- 📖 Chinese documentation for both tasks updated in sync

---

### v1.1.0

**New Features**

- 🛡️ **M4LT2 Emergency Stop High-Damping Protection**: On M4LT2, when the hardware emergency stop switch (ioboard) is triggered, the robot no longer immediately cuts power. Instead, it automatically switches to the high-damping protection task (`TASK_ROTARY_JOINT_HIGH_DAMPING`, TID=4600). Joints remain powered and are controlled in a pure-damping PD mode (`kp=0`, `kd=80`) that prevents limbs from dropping instantly and gives operators a safer intervention window. See [High-Damping Protection Task](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping) for details.

**Documentation Updates**

- 📖 Added [High-Damping Protection Task page](/fourier-grx-M4/docs/en/tasks/emergency_stop_high_damping)
- 📖 Updated [Task Description](/fourier-grx-M4/docs/en/tasks) task table with TID=4600
- 📖 Updated [M4L Quickstart](/fourier-grx-M4/docs/en/quickstart/m4l) with hardware emergency stop behavior notes

---

## July 2025

### v1.0.0 (2025-07-08)

**Major Milestone**

- 🎉 First official release of the Fourier-GRX-M4 SDK documentation
- 💡 Support for M4 series robot development
- 📖 Complete API documentation and usage guide
- ✨ Added common operations page
- 📚 Improved documentation structure and navigation
- 🔍 Enhanced search functionality

**Features**

- ✅ Core API interfaces
- ✅ Example code
- ✅ Developer guide
- ✅ Troubleshooting guide

**Notes**

- Currently focused on M4 series robots
- Support for other robot models will be added progressively
