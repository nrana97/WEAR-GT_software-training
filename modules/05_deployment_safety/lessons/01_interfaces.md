# Prediction and controller interfaces

A classifier output is not a torque command. Keep model inference separate from controller decisions, unit conversion, and device actuation. This module produces a simulated normalized output only; it never opens a hardware interface.

An inference wrapper accepts a finite feature vector, calls a prediction function, measures elapsed time with `time.perf_counter`, and checks its result. A late result is unusable even if numerically correct. Reproducible unit tests can inject a fake clock, while real latency measurements need representative load and many trials.

**Try:** define a predictor returning twice its first input. Test wrong shapes, NaNs, exceptions, and a result outside the permitted interval. Which failures can Python catch, and which require external supervision?
