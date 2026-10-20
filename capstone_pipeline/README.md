# Capstone pipeline: training integration plan

The individual stages now have training exercises and standalone reference
implementations. A production end-to-end pipeline is not supplied.

| Stage | Training API | Output |
|---|---|---|
| Calibrate/audit | Level 1 convert_counts / audit | calibrated array / diagnostics |
| Log | Level 2 write_session | samples.csv + metadata.json |
| Align | Level 2 align | timestamp_s, a, b on an explicit grid |
| Process | Level 3a lowpass / window_features / cycle_features | filtered trace / feature table |
| Review | Level 3b plot_session / review / visible_window | PNG + quality summary / replay slice |
| Model | Level 4 train_evaluate / evaluate_subjects | fitted pipeline + held-out metrics |
| Simulate | Level 5 infer / step / reset | simulated bounded output and reason |

## Bridge the stages deliberately

1. Preserve immutable raw counts; calibrate a copy and supply accurate units.
2. Rename raw sensor columns to the logger schema, using timestamp_s in seconds.
3. Alignment uses value columns per stream; record the offset and grid rate.
4. Do not send NaNs to filters or models. Split contiguous valid segments or
   document bounded interpolation. Never bridge arbitrary long gaps.
5. Add subject_id, session_id, task labels, and time bounds to feature tables.
   These provenance columns are not model features.
6. Keep the fitted scaler and model together. Level 5's predictor is a scalar
   simulation adapter; classification labels must not become actuator commands.

## Teaching convention, pending team review

A session directory holds samples.csv and metadata.json. Times are seconds in
one stated clock domain. Metadata keys are session_id, subject_id, task,
sensor_placement, firmware_version. Use synthetic subject IDs. Before real
collection, the team must decide units/schema version, clock synchronization,
hardware protocol, loss accounting, storage/access policies, participant-data
procedures, and device-specific safety controls. No training code should
operate a worn device.
