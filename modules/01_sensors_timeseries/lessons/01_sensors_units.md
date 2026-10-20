# Lesson 1: What sensors measure, calibration, and units

**Goal:** explain what the main wearable sensor types measure, convert raw ADC counts into a physical quantity, and keep track of units and coordinate frames.

**Allow 45–60 minutes:** read, run the examples, then complete the exercises. You only need Module 00's arrays and plotting tools.

## Start with the measurement, not the column name

An IMU (inertial measurement unit) commonly combines a three-axis accelerometer and a three-axis gyroscope. Each channel measures along or around a sensor-fixed axis. A channel named `acc_z` means the sensor's z-axis, which is not automatically the person's vertical direction.

| Sensor | Measures | Typical representation | What it does not directly tell you |
|---|---|---|---|
| Accelerometer | Specific force along an axis | g or m/s² | Position or joint angle |
| Gyroscope | Angular velocity around an axis | degrees/s or radians/s | Absolute orientation without integration/fusion |
| Surface EMG | Differential electrical voltage at electrodes | V, mV, µV, or raw counts | Muscle force or intended movement without interpretation |
| Force/pressure sensor | Load or pressure through a calibrated transducer | N, Pa, or counts | Whole-body force unless placement supports that interpretation |

At rest an accelerometer commonly has a magnitude near 1 g because its support opposes gravity. During movement it also reflects acceleration and orientation. You cannot remove gravity from a moving sensor by subtracting 9.81 from every axis.

For this training, `1 g = 9.81 m/s²` is an approximation. Convert degrees to radians with `np.deg2rad`; a model trained with degrees/s will receive very different numbers if deployment supplies radians/s.

## Raw counts are not physical units

An analog-to-digital converter (ADC) quantizes voltage. Our invented teaching sensor has:

- A 12-bit unsigned ADC, so valid integer counts are 0 through 4095.
- A 3.3 V reference.
- A zero-acceleration voltage of 1.65 V.
- Sensitivity of 0.33 V per g.

We use the endpoint convention below. Actual ADC scaling, signed encoding, and sensor transfer functions must come from hardware specifications and calibration.

```python
import numpy as np

counts = np.array([0, 2047.5, 2457, 4095], dtype=float)
voltage_v = counts / 4095 * 3.3
acceleration_g = (voltage_v - 1.65) / 0.33
acceleration_m_s2 = acceleration_g * 9.81

print(voltage_v)       # [0.   1.65 1.98 3.3 ]
print(acceleration_g)  # [-5.  0.  1.  5.]
```

The operation order matters: first counts → voltage, then subtract the zero point, then divide by sensitivity. The units cancel as V / (V/g) = g. The fractional midpoint is useful for explaining the transfer function even though an ADC normally emits integer counts.

## Calibration is an assumption you must record

Suppose a stationary axis that should read zero instead averages 0.08 g. That can indicate an offset. A known reference can estimate an offset correction; a second known reference can help estimate scale. But if you do not know orientation, the same observation may be physically expected.

```python
known_zero_g = np.array([0.07, 0.08, 0.09])
offset_g = known_zero_g.mean()
future_reading_g = 0.30
corrected_g = future_reading_g - offset_g  # 0.22 g
```

Record the original conversion constants, how the offset was measured, and whether correction happened before analysis. Do not estimate calibration from held-out ML test data merely to improve scores.

## Preserve missingness and validate range

```python
raw = np.array([2048, np.nan, 4095], dtype=float)
finite = np.isfinite(raw)
rail = finite & ((raw <= 0) | (raw >= 4095))
print(finite)  # [ True False  True]
print(rail)    # [False False  True]
```

NaN means unavailable; zero counts is a valid ADC endpoint. Converting missing values to zero invents a large negative acceleration. Infinity is invalid, not a special high measurement. Keep raw data unchanged and convert a separate array.

## Common mistakes

- Mixing g and m/s² in the same feature column.
- Treating the sensor frame as the body frame without a placement convention.
- Using a made-up sensitivity as if it were a datasheet specification.
- Assuming EMG amplitude gives force without calibration and an appropriate model.
- Correcting an apparent offset without knowing the physical reference condition.

## Try it

1. Reproduce the worked conversion. Convert 1.5 g back into expected counts: first calculate voltage, then reverse the ADC equation. Check the answer by converting forward.
2. Write `to_radians_per_second(values)` and test 0, 90, and 180 degrees/s.
3. Create a five-row DataFrame with raw counts and a calibrated column. Include a NaN and verify it stays missing.
4. Plot both columns on separate axes with units. Explain why sharing a y-axis would mislead.
5. Write three sentences describing the extra information needed to interpret a real ankle IMU recording: include placement, axes, and calibration.

**Check yourself:** the inverse conversion for 1.5 g is about 2661.75 counts; 180 degrees/s is π radians/s. Neither answer establishes the accuracy of a real sensor.

Next: [Sampling and timestamps](02_sampling.md)
