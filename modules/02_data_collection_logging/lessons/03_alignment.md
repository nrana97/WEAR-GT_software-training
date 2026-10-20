# Alignment and missing samples

Interpolation estimates values between observations; it does not create new measurements. Align streams onto an explicit reference grid. Never extrapolate beyond each stream's coverage. Reject unsorted or duplicate times before interpolation.

For the checkpoint, accept exact finite observations. For intermediate grid times, interpolate only if both neighboring values are finite and their time separation is at most `max_gap_s`. Leave all other values NaN. This prevents drawing a smooth line across a long disconnect.

**Review:** compare a missing-value count before and after alignment. What information is lost if you discard sequence numbers? A DataFrame replay cannot prove a real logger never drops packets; hardware work also needs buffer/backpressure and loss measurements.
