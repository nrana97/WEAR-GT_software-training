# Level 5: Deployment and safety

**Status: stub. Not yet written.**

## Draft learning goals

- Run a trained model in a real-time loop and measure its latency
- Design a clean interface between software and the device controller
- Add fail-safes: limits, watchdogs, and safe-state behavior when data or models misbehave
- Understand what changes when software is attached to a person's body

## Prerequisites

Level 4 (or its checkpoint).

## Checkpoint idea

Given a trained model and a simulated device, build a loop that meets a latency budget and falls back to a safe state when input data is missing or out of range.

## Important

This level depends heavily on WEAR's hardware and safety practices. Write it in coordination with the hardware and controls leads, and do not run any code on a real worn device without their review.
