# Sampling and timestamps

At 100 Hz the nominal period is 0.01 s. Estimate rate as `1 / np.median(np.diff(t))` only after verifying finite, strictly increasing timestamps. A long gap is a dropout; duplicate timestamps are not a zero-duration movement.

The Nyquist limit is half the sampling rate. A 70 Hz component sampled at 100 Hz can appear as 30 Hz. Once aliased, filtering the stored recording cannot recover the original. Use appropriate acquisition filtering and sampling before recording.

**Try:** evaluate `sin(2*pi*70*t)` and `-sin(2*pi*30*t)` at 100 Hz. Compare arrays. Then remove a block of timestamps and compare mean versus median interval estimates.
