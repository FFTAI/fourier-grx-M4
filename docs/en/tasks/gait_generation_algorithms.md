---
layout: default
title: Gait Generation Algorithms
parent: Task Description
nav_order: 4.35
has_toc: true
nav_exclude: true
---

# Gait Generation Algorithms

* TOC
{:toc}

## Task Info

This is an algorithm topic page with **no independent task ID (TID)**; it cannot be issued as a motion task. It compares the VHIP, FHIP, DSP, high-lift DSP, and harmonic-coefficient gait generators in the current M4L SDK and explains their relationship to assist, load-based gain adjustment, and actuator control.

Intended readers: developers and clinical technical staff who select motion tasks, tune gait parameters, build host-side trajectory previews, or read the `fourier-grx` gait source code.

## Module Info

This page registers no independent module. Algorithms are invoked through their corresponding motion or Planner tasks; the module interface cannot switch generators directly at runtime.

## Interface Info

Generator output consists primarily of intermediate data rather than actuator current:

- Left/right hip and knee reference positions and velocities;
- COM and foot trajectories for DSP/VHIP/FHIP/high-lift DSP;
- Swing and support flags for geometric generators;
- Step period, frame count, and start/loop/end time boundaries;
- Fields subsequently reported by the task layer, including `rehab.reference_joint_position`, `reference_joint_velocity`, `reference_joint_position_max/min`, and `step_frequency`.

These values describe the **reference trajectory**. Actual joint position, velocity, and torque are measured separately through actuator feedback and must not be conflated with references.

## Principle Explanation

### Algorithm Operation

#### 1. Common control chain: generators create references; task models execute them

The five schemes follow two generation routes:

```text
Geometric generation (VHIP / FHIP / DSP)
  Parameters → COM and foot trajectories → two-link inverse kinematics → URDF conversion
  → Knee restriction/scaling/smoothing → position differentiation → start/loop/end state machine → PD control

High-lift DSP
  Complete normal DSP output → FK evaluation of actual foot height → second swing-phase IK
  → Zero-phase smoothing → velocity recomputation → common execution state machine

Harmonic coefficients
  Stored Fourier coefficients → phase-based joint-curve reconstruction → period quantization and transitions
  → Joint clipping → common execution state machine
```

Every geometric generator uses planar two-link inverse kinematics. For foot displacement `dx,dz` relative to the COM:

- `d=sqrt(dx²+dz²)`, limited to the leg's reachable range;
- `q_knee=π−acos((L_thigh²+L_shank²−d²)/(2L_thigh·L_shank))`;
- Hip angle follows from `atan2(dz,dx)` and the second cosine relation;
- Geometric angles are converted to URDF direction, zero, and radians before final reference velocities are produced.

Three execution layers sit outside the generator and must be distinguished from it:

1. **Playback state machine**: measured positions are held before start, followed by entry to the first gait frame and start/loop/end segments. Stop is normally evaluated at a loop boundary.
2. **Feedback control**: smoothed and travel-limited positions enter PD. PD assist changes Kp/Kd, dt assist changes trajectory time advancement, and load detection changes tracking stiffness.
3. **Safety and reporting**: torque protection reads measured torque, reference envelopes come from generated trajectories, and tracking error is the difference between reference and measurement. These are different quantities.

#### 2. Core differences at a glance

| Scheme | Primary trajectory source | COM vertical trajectory | Double support | Foot-height control | Main current use |
|---|---|---|---|---|---|
| VHIP | LIPM + parameterized feet + online IK | Geometric relation from leg length to support distance | No separate DSP segment | Input `step_height` shapes the foot curve directly | In-place stepping and forward configurations explicitly selected by developers |
| FHIP | LIPM horizontally + parameterized vertical motion + online IK | Quadratic parabola | No separate DSP segment | Same as VHIP | Developer-selectable forward/in-place generator |
| DSP | LIPM in SSP + Hermite transfer in DSP + online IK | Geometric height in SSP, continuous Hermite effective distance in DSP | Explicit `T_dsp` allocation | `step_height` plus smoothed swing-foot velocity profile | Passive forward walking and knee-restricted variant |
| High-lift DSP | Secondary compensation after normal DSP output | Inherited from DSP | Inherited from DSP | FK evaluation followed by second IK for actual clearance | Forward walking requiring more swing-foot clearance |
| Harmonic | Joint curves reconstructed directly from stored Fourier coefficients | No COM calculation | Implicit in the fixed curve; no online ratio adjustment | Fixed into coefficient curves | Repeatable fixed-shape gait with adjustable rhythm |

#### 3. VHIP: virtual-hip model with geometric height constraints

VHIP approximates horizontal COM motion with a linear inverted pendulum. For internal step length `S_g` and base height `h`:

- `T_step=S_g/v` and `ω=sqrt(g/h)`;
- In support-point coordinates, the COM moves from `−S_g/2` to `+S_g/2`;
- `x(t)=−(S_g/2)·cosh(ωt)+(x_dot0/ω)·sinh(ωt)`;
- Periodic boundary velocity is `x_dot0=(ωS_g/2)·coth(ωT_step/2)`.

Its defining feature is that vertical height is **not an independently fitted free curve**; it is calculated from the leg-length constraint:

`z(x)=sqrt((L_thigh+L_shank)²−x²)`

The COM is therefore higher mid-step and lower near support transitions. Vertical shape follows horizontal position and total leg length. Swing-foot height is `z=h_lift·(1−cos(2πτ))/2`, horizontal motion is linear by default, and IK produces hip/knee angles.

In-place stepping reuses the generator with three changes:

- Horizontal COM position and base height remain fixed, eliminating continuous forward travel;
- Swing-foot horizontal motion becomes `x=L_max·sin(πτ)`, returning to its origin at step end;
- Vertical motion remains half-cosine, while step period is given directly rather than derived from step length/speed.

**Strengths**: parameters have intuitive physical meanings, the same family supports forward and in-place gait, and integration with PD/dt assist is straightforward.

**Limitations**: there is no independent double-support segment. The foot and COM models are simplified geometry, not measurements of the patient's real COM or foot.

#### 4. FHIP: fixed-hip model with a parabolic vertical trajectory

FHIP shares VHIP's horizontal LIPM, half-cosine foot lift, and two-link IK. The most important clarification is that **“fixed hip” does not mean constant COM height**.

FHIP explicitly constructs vertical motion as a quadratic. With normalized phase `τ=t/T_step`, it can be understood as:

`z(τ)=h_min+4(h_max−h_min)·τ(1−τ)`

Endpoints return to `h_min` and the midpoint reaches `h_max`. Current code approximates `h_min` from total leg length and internal step length with a small height margin. By comparison:

- VHIP's `z(x)` comes from circular/leg-length geometry, so vertical shape varies with horizontal displacement;
- FHIP's `z(τ)` is a prescribed parabola, so vertical shape varies with time phase;
- Both retain LIPM horizontally—the difference is not two horizontal dynamics models.

No public TID currently selects FHIP by default. Developers can select `gait_generator_type="fhip"` in supported forward or in-place control models. Clinical and host-side comparisons should not assume its vertical trajectory is identical to the default VHIP task.

#### 5. DSP: explicit double support with continuous weight transfer

DSP (Double Support Phase) divides each step into single support (SSP) and double support (DSP):

- `T_step=S_g/v`;
- `T_dsp=r_dsp·T_step`;
- `T_ssp=T_step−T_dsp`.

**SSP**: the swing foot completes its step while the COM follows LIPM from `−a` to `+a`. Horizontal foot motion uses a smooth trapezoidal velocity profile with zero velocity at lift-off and touchdown; vertical motion remains half-cosine.

**DSP**: both feet remain planted while a cubic Hermite spline transfers the COM from `+a` to `+a+d`. Position and velocity match adjacent SSP segments at the boundaries to avoid support-transition jumps.

To satisfy periodic continuity, COM transfer distance `d` is not simply `r_dsp·S_g`; it comes from a closed-form relation:

- `K=r_com·T_dsp·ω·coth(ωT_ssp/2)`;
- `d=K·S_g/(2+K)`;
- `a=(S_g−d)/2`.

Here `r_com` controls mid-DSP transfer speed, with internal default `dsp_com_ratio=0.8`; swing acceleration/deceleration uses `swing_blend=0.3`. DSP also computes height from leg geometry and keeps effective distance and slope continuous across SSP/DSP boundaries.

**Strengths**: double-support ratio has explicit timing meaning and support transitions are smoother, making DSP suitable when this phase must be tunable.

**Limitations**: `r_dsp` changes reference timing only. It neither identifies the patient's actual double-support proportion nor guarantees whole-body balance.

#### 6. High-lift DSP: from commanded foot height to calibrated actual clearance

Normal DSP's `step_height` is a pre-IK foot target. Hip-angle scaling and smoothing subsequently change the actual foot height produced by the final joint trajectory. High-lift DSP therefore adds a second geometric pass:

1. **FK evaluation**: current hip/knee angles produce ankle position relative to the hip. The lower of the two feet defines the ground reference for original-trajectory clearance.
2. **Target window**: swing uses a Beta lift window by default (`lift_shape=4.0`) with peak phase `lift_peak_phase=0.42`. The target is `smooth_max(base_clearance,H_lift·w(s))`, which raises but never lowers portions already above the target. `lift_shape=0` restores the original smootherstep.
3. **Second IK**: swing-foot horizontal `x` remains fixed while only `z` changes; swing-side hip/knee angles are re-solved. Normal high-lift tasks leave stance untouched, while the knee-restricted variant preserves the shared knee-angle floor on both legs.
4. **Constraints and smoothing**: angles are clipped to mechanical travel, smoothed by a centered binomial kernel with default duration `0.10×T_step`, then by Gaussian smoothing with default `sigma=0.08×T_step`. Velocities and actual foot-height diagnostics are recomputed.
5. **Actual-height solving**: in default `lift_height_mode="actual"`, bisection finds the raw IK target that brings the smoothed steady-state actual peak within ±5 mm of `param_3`. Angular acceleration is diagnostic by default, with an optional hard `lift_acc_limit`. `lift_height_mode="peak"` preserves the original raw-IK-target semantics.

Two height parameters must be distinguished:

- `param_7` / `step_height`: original DSP foot-lift target before compensation;
- `param_3` / `H_lift`: target clearance after evaluating actual joint trajectories, default 0.10 m with an allowed 0.05–0.25 m range.

Targets can be unreachable near full extension or joint limits, so `H_lift` does not guarantee actual clearance. TID 4135 only adds execution-stage velocity feedforward and leaves generation unchanged.

#### 7. Harmonic coefficients: joint-space fitting and phase playback

Harmonic generation computes no COM, foot, or IK trajectory. Stored coefficients directly produce joint angles:

`q(φ)=a0+Σ[k=1..K](a_k·cos(2πkφ)+b_k·sin(2πkφ))`

Current tables use `K=10` and `φ∈[0,1)`. Each joint has independent coefficients containing left/right phase relationships. URDF direction, zero, and radian conversion are completed before runtime.

The runtime sequence is:

1. **Select a curve**: four hip-amplitude levels × four knee-extension-restriction levels provide 16 coefficient sets, selected before starting.
2. **Add a time axis**: cadence selects target stride time `T_stride`, quantized to `N=round(T_stride/Δt)` frames and actual period `N·Δt`.
3. **Evaluate phase**: `φ=(n mod N)/N` produces four joint positions per frame; final positions are differentiated for velocity.
4. **Join transitions**: cubic Hermite segments connect standing to cycle frame zero, while complete left/right cycles provide phase-continuous wraparound.
5. **Clip and execute**: joint-travel clipping precedes the common start/loop/end and PD pipeline.

**Strengths**: highly repeatable gait, directly previewable joint envelopes, no online patient-leg-length IK, and independent shape/rhythm levels.

**Limitations**: step length, speed, leg lengths, base height, foot lift, and double-support ratio do not generate the curve, and Fourier coefficients are not adapted online to patient performance.

#### 8. Assist, load, and feedforward outside the generator

These functions affect execution without normally changing the selected generator's base scheme:

| Function | Where it acts | Effect on reference trajectory | Effect on control output |
|---|---|---|---|
| Passive-task load detection | Positive mechanical-power integration during loops | No change to geometric or harmonic curves | 30 J forward and 70 J in-place thresholds trigger PD ramp toward hard |
| PD assist | Kp/Kd interpolation during startup | No change to curve shape | `Kp=100+100r`, `Kd=10+10r`; changes error correction and disables automatic load ramping |
| dt assist | Trajectory clock during loops | Same angular envelope; actual period is approximately `T_base/v_play` | `v_play=0.5+0.5r`, medium PD fixed; automatic mode changes subsequent playback only |
| Knee restriction | Common input before generation and knee clipping after IK | `θ=max(θ_left,θ_right)` applies to both knees and affects geometric base height | No direct measured-joint clamp or independent mechanical stop |
| Velocity feedforward | Execution | No change to basic curve generation | Actual delivery depends on FSA v2/v3 protocol and robot model |

Task comparison therefore requires more than “VHIP or DSP”: also confirm PD tier, automatic assist, torque protection, and model protocol.

#### 9. Task-to-generator mapping

| Generator | Corresponding task or entry point | Main adjustable parameters |
|---|---|---|
| VHIP | [Passive Marching in Place](/fourier-grx-M4/docs/en/tasks/mark_time_passive) and its assist/knee-restricted variants; developers can also select it explicitly in forward control models | Leg lengths, step period, foot lift, base height, assist ratio |
| FHIP | `gait_generator_type="fhip"` in developer control models; no independent public TID | Similar to VHIP, but vertical trajectory is quadratic |
| DSP | [Passive Forward Walking](/fourier-grx-M4/docs/en/tasks/forward_walk_passive), normal assisted forward walking [PD](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd) / [dt](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt), and corresponding knee-restricted tasks | Step length, speed, leg lengths, base height, foot lift, double-support ratio, assist ratio |
| High-lift DSP | [Passive Forward Walking – High-Lift](/fourier-grx-M4/docs/en/tasks/forward_walk_high_lift) (TID 4134–4137), [Passive Forward Walking – High-Lift (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_high_lift) (TID 4307–4309) | DSP parameters plus compensated target lift peak `param_3`; assist variants also use `param_4`, and knee-restricted variants read user leg lengths and left/right knee restrictions |
| Harmonic | [Passive Forward Walking – Harmonic Fitting](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic), [Harmonic Assist PD](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_pd), [Harmonic Assist dt](/fourier-grx-M4/docs/en/tasks/rotary_joint_forward_walk_harmonic_assist_adjust_dt), and knee-restricted variants 4310 / 4311 | Hip amplitude, table knee restriction, cadence, assist ratio; knee-restricted variants add a virtual-user knee-angle floor |
| Multi-scheme preview | [Planner](/fourier-grx-M4/docs/en/tasks/planner) | Reuses executing-task generators and reports references without driving joints |

Corresponding source files are under `src/fourier_grx/algorithm/m4l/` in the `fourier-grx` repository:

- `fi_algorithm_gait_generator_vhip.py`
- `fi_algorithm_gait_generator_fhip.py`
- `fi_algorithm_gait_generator_dsp.py`
- `fi_algorithm_gait_generator_dsp_high_lift.py`
- `fi_algorithm_gait_generator_harmonic.py`

### Rehabilitation and Clinical Use

Algorithm selection should combine engineering constraints with training goals, followed by physician/therapist confirmation of range, weight-bearing capacity, fatigue, and pain response. The table is a starting point, not a fixed prescription:

| Training or engineering need | Scheme to consider first | Rationale and cautions |
|---|---|---|
| Explicitly adjustable double support | DSP | Timing is clear, but ratio does not guarantee balance; external support remains necessary |
| In-place stepping or in-place PD/dt assist | VHIP | Intuitive parameters and direct task mapping for in-place assist; PD changes stiffness while dt changes rhythm |
| Normal forward PD/dt assist | DSP (default) | Normal forward assist and knee-restricted variants default to DSP since v4.4.86; PD changes stiffness while dt changes rhythm, and developers can still explicitly select another generator |
| Compare alternative COM vertical models | FHIP and VHIP | Useful for development evaluation; FHIP is not a default public task and needs unloaded validation |
| Insufficient actual clearance with normal DSP | High-lift DSP | Compensates the final joint trajectory; start conservatively and observe actual clearance and stance stability |
| Fixed-shape, repeatable joint curves | Harmonic | Repeatable across sessions, but no online personalization from leg length or patient performance |
| Different left/right knee extension restrictions | Corresponding restricted task plus selected generator | Larger input currently applies to both knees, so confirm tolerance on the other side |

Additional common precautions:

- Review reference envelopes with the Planner or an unloaded workflow before starting conservatively with full external protection. A successful preview does not establish patient tolerance.
- Do not treat `reference_joint_*` as measured patient gait, or cadence, double-support ratio, and assist ratio as direct measures of independent walking, voluntary strength, or treatment effect.
- No generator recognizes pain, spasticity, or fall risk. Stop and reassess for abnormal torque, pain, resistance, foot contact, left/right instability, or fatigue.
- When changing generator schemes, recheck PD tier, torque protection, feedforward protocol, and model differences instead of copying only the previous gait parameters.

> These clinical suggestions support professional judgement and do not replace assessment by a physician/therapist, the product instructions, or local safety procedures.

## Update Log

- Documentation added: consolidated implementation flows, equations, task mappings, and clinical selection differences for VHIP, FHIP, DSP, high-lift DSP, and harmonic-coefficient generators.
