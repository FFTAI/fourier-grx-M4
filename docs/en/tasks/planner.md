---
layout: default
title: Planner
nav_order: 4.26
parent: "Task Description"
has_toc: true
nav_exclude: true
---

# Planner

The Planner is an auxiliary task for trajectory-tracking tasks. It generates joint motion trajectory sequences for display on the host computer along with possible trajectory generation results. Planner tasks do not run the task activate/deactivate flow, so the robot itself does not execute trajectory-tracking motion.

> ⚠️ **Note**: before using the Planner, run Servo Off (TID=36) to make sure the device is de-energized, to avoid accidental injury.
>
> When a Planner task is deactivated, the step-frequency field reported to the host (`rehab.step_frequency`) is cleared to zero.

## Passive Forward Walk

Task ID (TID): **4401**

Task Parameters: refer to [Passive Forward Walk](/fourier-grx-M4/docs/en/tasks/forward_walk_passive)

## Passive Mark Time

Task ID (TID): **4402**

Task Parameters: refer to [Passive Mark Time](/fourier-grx-M4/docs/en/tasks/mark_time_passive)

## Assist Forward Walk (Adjust PD Parameter)

Task ID (TID): **4403**

Task Parameters: refer to [Assist Forward Walk (Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_pd)

## Assist Mark Time (Adjust PD Parameter)

Task ID (TID): **4404**

Task Parameters: refer to [Assist Mark Time (Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_pd)

## Assist Forward Walk (Adjust dt Parameter)

Task ID (TID): **4405**

Task Parameters: refer to [Assist Forward Walk (Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/forward_walk_assist_adjust_dt)

## Assist Mark Time (Adjust dt Parameter)

Task ID (TID): **4406**

Task Parameters: refer to [Assist Mark Time (Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/mark_time_assist_adjust_dt)

## Passive Forward Walk (Knee Restriction)

Task ID (TID): **4501**

Task Parameters: refer to [Passive Forward Walk (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_passive)

## Passive Mark Time (Knee Restriction)

Task ID (TID): **4502**

Task Parameters: refer to [Passive Mark Time (Knee Restriction)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_passive)

## Assist Forward Walk (Knee Restriction, Adjust PD Parameter)

Task ID (TID): **4503**

Task Parameters: refer to [Assist Forward Walk (Knee Restriction, Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_pd)

## Assist Mark Time (Knee Restriction, Adjust PD Parameter)

Task ID (TID): **4504**

Task Parameters: refer to [Assist Mark Time (Knee Restriction, Adjust PD Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_pd)

## Assist Forward Walk (Knee Restriction, Adjust dt Parameter)

Task ID (TID): **4505**

Task Parameters: refer to [Assist Forward Walk (Knee Restriction, Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_forward_walk_assist_adjust_dt)

## Assist Mark Time (Knee Restriction, Adjust dt Parameter)

Task ID (TID): **4506**

Task Parameters: refer to [Assist Mark Time (Knee Restriction, Adjust dt Parameter)](/fourier-grx-M4/docs/en/tasks/knee_restriction_mark_time_assist_adjust_dt)

## Update Log

- Planner tasks (TID 4401–4406) added in `fourier-grx` v4.3.0.
- Since `fourier-grx` v4.4.47, planner tasks clear the reported step-frequency field on exit.
