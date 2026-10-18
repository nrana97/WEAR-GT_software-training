# Level 4: ML for movement

**Status: stub. Not yet written.**

## Draft learning goals

- Frame a movement problem as a machine learning task (classification, regression, state estimation)
- Train classical models first, then neural networks, and compare them honestly
- Evaluate correctly: split by subject, not by random window, to avoid leakage
- Report results with uncertainty and know when a model is not good enough

## Prerequisites

Level 2 and Level 3a (or their checkpoints).

## Checkpoint idea

Given labeled feature data from several subjects, train and evaluate a model with a subject-wise split, and write a short, honest report of its performance and limits.

## Open questions before writing this module

- Which prediction targets matter first (gait phase, activity or terrain, joint angle or torque, intent from EMG)?
- Which ML framework the team standardizes on
