# Sensors, counts, and units

An accelerometer measures specific force along sensor axes (including the effect of gravity at rest); a gyroscope measures angular velocity. EMG electrodes measure voltage related to muscle activity, not joint torque directly. Force sensors require a calibration that relates their electrical output to force. Placement and coordinate frame matter.

An ADC converts voltage to integer counts. For this exercise, a 12-bit ADC has counts 0–4095 and uses 3.3 V as its full-scale reference. A teaching accelerometer has zero at 1.65 V and sensitivity 0.33 V/g:

```python
voltage = counts / 4095 * 3.3
acceleration_g = (voltage - 1.65) / 0.33
```

These constants are invented for training. Real conversion requires the sensor datasheet, measured calibration, and signed/unsigned format. Never label counts as acceleration without calibration. Keep missing values missing.

**Try:** calculate the output for 0, 2047.5, and 4095 counts. Explain why the midpoint can be fractional even though ADC counts are integers.
