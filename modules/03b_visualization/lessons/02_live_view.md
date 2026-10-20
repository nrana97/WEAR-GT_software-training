# Replay and live views

This training uses Matplotlib and a CSV replay to avoid adding a web framework before the team chooses one. A rolling view keeps only the last N seconds visible. A real live view must use a bounded buffer and avoid blocking acquisition with drawing.

A replay is not live acquisition. Measure rendering cost and redraw at a slower rate than acquisition. Do not show stale values as if fresh; display last-update age and missing-data indicators. When timestamps are invalid, stop and explain the problem instead of drawing misleading traces.

**Try:** advance a replay cutoff in 0.5 s increments and show only the preceding 2 s. How many samples would a 100 Hz ring buffer need?
