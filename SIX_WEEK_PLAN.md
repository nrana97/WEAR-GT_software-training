# Six-week WEAR software training program

This is a six-week learning program, with a target of **6–8 hours per week**
for someone new to these tools. That is roughly 36–48 hours of active work,
not six weeks of reading alone. The estimates include experiments, projects,
checkpoints, debugging, reports, and peer review. They are planning estimates,
not a guarantee of how long any student will need.

Module 00 is the foundation. The expanded Modules 01–05 have 18 lessons,
each with worked code, exercises, common failure cases, and checks for
understanding. Lessons generally take 45–75 minutes when the exercises are
actually completed. Both 3a and 3b are required for this six-week route;
visualization is distributed across Weeks 2–4 to avoid one overloaded week.

If most members are completely new to programming, allow a seventh week
by splitting Week 1 into two. Members with prior experience may demonstrate
competence through checkpoints, but should still join reviews and team work.

## Week 1 — Python and tooling (Module 00)

**Question:** Can you load a recording, explain your code, and submit a
reproducible change?

1. Set up the virtual environment and install requirements. Read Module 00's
   four lessons, running every example you do not already understand.
2. Complete its Python warmup and pandas/plotting exercises.
3. Generate the walking recording and implement the guided explorer project.
4. Complete the messy-data checkpoint. Preserve raw data and explain each
   cleaning choice rather than only seeking green tests.
5. Review a teammate's output or ask a lead to review your own.

**Submit:** implemented project/checkpoint, test output, labeled walking plot,
and a short explanation of one bug you encountered and how you diagnosed it.

**Discussion:** What information is lost when you fill every missing value?
Why is the median sample interval useful but insufficient?

**Suggested time:** lessons/practice 3 h; project 1.5 h; checkpoint 1.5 h;
review and environment troubleshooting 0.5–1.5 h.

## Week 2 — Sensors and first review plots (Module 01 + 3b Lesson 1/project)

**Question:** Can you translate a sensor recording into physical units and
show its quality problems clearly?

1. Complete Module 01's three lessons and exercises: conversion by hand,
   sampling experiment, and a structured quality report.
2. Implement calibration and sampling-rate functions, then the audit checkpoint.
3. Read visualization Lesson 1 and implement its guided plotting project.
   Use the same synthetic recording so interpretation and visualization agree.
4. Test another seed or a custom fixture with a timing gap and a saturated
   sample. Compare raw counts with calibrated units on separately labeled axes.

**Submit:** calibration/audit code, visualization project, quality table,
full-session and zoomed plots, and a half-page report distinguishing findings
from possible causes. Include evidence for NaNs, rails, and timestamp gaps.

**Discussion:** Why can a flat signal represent either stillness or failure?
What would you ask the hardware team before interpreting a real ankle IMU?

**Suggested time:** sensor lessons/practice 2.5 h; project/checkpoint 2 h;
visualization lesson/project 1.5 h; report/review 0.5–1 h.

## Week 3 — Logging, alignment, and replay (Module 02 + 3b Lesson 2)

**Question:** Can another person reconstruct how and when your samples were
recorded, including missing coverage?

1. Complete Module 02's stream, metadata, and alignment lessons.
2. Implement the session logger and demonstrate CSV/JSON round-tripping.
3. Complete stream alignment with different rates, a known clock offset,
   one missing value, and one long dropout. Plot the original observations
   as points and aligned data without concealing gaps.
4. Read visualization Lesson 2 and demonstrate three inclusive replay windows.
5. Design a collection/queue/writer plan with an observable overload policy.
   This is a design exercise; no hardware collector is required.

**Submit:** logger and alignment checkpoint, synthetic metadata example,
alignment plot, replay-window snapshots or a reproducible driver, and a short
loss-accounting/clock-assumption note. Do not commit generated raw recordings.

**Discussion:** What does host arrival time tell you that device time does
not? Why does a bounded display window not necessarily bound memory?

**Suggested time:** lessons/practice 2.5–3 h; project/checkpoint 2 h;
replay lesson/practice 1 h; report/review 0.5–1 h.

## Week 4 — Processing, events, and review (Module 3a + 3b Lesson 3/checkpoint)

**Question:** Can you extract repeatable information without hiding artifacts
or confusing sample indices with seconds?

1. Complete all three signal-processing lessons and the window-feature project.
2. Compare at least two cutoffs against a known synthetic target. Save raw,
   filtered, and residual comparisons; inspect boundaries separately.
3. Complete the cycle-feature checkpoint. Repeat detection at a second
   frequency or noise seed and explain false or missed peaks.
4. Finish visualization Lesson 3 and its review/dashboard checkpoint. Overlay
   event times in seconds and report missing/constant-channel summaries.
5. Attach subject/session provenance to a demonstration feature table without
   using those identifiers as predictors.

**Submit:** filter/window and cycle-feature code, review checkpoint,
feature-schema description, annotated plots, and a comparison report that
states which settings changed and what the effect was.

**Discussion:** Why is zero-phase filtering offline? Why are overlapping
windows not independent observations? Why is a peak not automatically heel strike?

**Suggested time:** processing lessons/practice 2.5 h; project/checkpoint
2–2.5 h; visualization lesson/checkpoint 1.5–2 h; report/review 0.5–1 h.
This is the densest week; move the visualization checkpoint to the beginning
of Week 5 if a learner needs extra debugging time.

## Week 5 — Subject-aware movement classification (Module 04)

**Question:** Is the model learning a movement relationship that transfers
across the synthetic subjects, or exploiting the evaluation setup?

1. Complete the framing, splitting, and evaluation lessons.
2. Implement held-out-subject training with a fitted preprocessing pipeline.
3. Compare model results with a training-majority baseline on the same test rows.
4. Complete leave-one-subject-out evaluation with fresh pipelines in each fold.
5. Run a separate robustness experiment: shift or add noise to one synthetic
   subject. Report the effect without tuning the final test to look better.
6. Review a peer's feature selection and split before reviewing their scores.

**Submit:** project/checkpoint, per-subject fold table, labeled confusion
matrix, model/baseline comparison, and a one-page report covering leakage,
class support, uncertainty terminology, and synthetic-data limitations.

**Discussion:** What changes if the deployment population is new sessions
from known people rather than new people? Why is fold standard deviation not
a confidence interval?

**Suggested time:** lessons/practice 2.5–3 h; project/checkpoint 2–2.5 h;
robustness experiment 1 h; report/review 0.5–1 h.

## Week 6 — Simulated deployment and final handoff (Module 05)

**Question:** Can your system explain when a result is unusable and retain
a fault until an explicit reset?

1. Complete inference, watchdog, and validation lessons.
2. Implement the measured-inference wrapper and simulated latched monitor.
3. Inject every documented fault, test boundaries, and prove rejected cases do
   not call the predictor where the contract requires that behavior.
4. Measure predictor latency separately from the injected-latency replay.
   State what is timed and report observed misses, not a hard guarantee.
5. Assemble the final training handoff described below.

**Submit:** project/checkpoint, fault matrix with expected/actual outcomes,
state traces including reset, latency summary, and final handoff.

**Discussion:** What remains untested if all unit tests pass? Which decisions
must the hardware and controls leads make before any worn-device integration?

**Suggested time:** lessons/practice 2.5–3 h; project/checkpoint 1.5–2 h;
fault experiments and handoff 1.5–2 h; review 0.5 h.

## Final handoff: connect the evidence

Create `REPORT.md` with links to your submitted code and these artifacts:

- A raw-data quality audit and documented calibration assumptions.
- A session metadata example and an alignment/missing-data policy.
- A processing comparison and a feature schema with provenance.
- A session-review figure with events and quality context.
- Subject-wise ML results with baseline and limitations.
- A simulated fault/recovery table and measured-latency summary.

Include a small, reproducible **bridge experiment**: run your logger on one
synthetic recording, read it back, use its finite `signal` channel for filtering
and window features, and save a labeled review plot. If copying functions into
a handoff script, identify their source modules. Do not modify the starter
interfaces to make imports convenient, and do not treat counts as calibrated
physical units. Module 04's labeled feature generator is a separate fixture;
this bridge does not create real activity labels or a production ML pipeline.

Explain every adaptation between stage schemas. The full production capstone
remains a team project; these standalone exercises do not constitute a finished
hardware pipeline. Keep all deployment work simulated.

## How completion is reviewed

Automated tests check specified behaviors, not understanding by themselves.
For each week a reviewer should be able to answer yes to these questions:

1. Does the implementation pass its tests, including a student-added edge case?
2. Can the student explain a worked example without reading a solution?
3. Are requested figures and outputs labeled and reproducible?
4. Does the report distinguish evidence, assumptions, and limitations?
5. Did the review identify and resolve at least one substantive question?

If an exercise takes longer than expected, use the extra time to debug and
understand it rather than skipping the report. Checkpoints remain the way to
skip material already mastered, while the weekly plan sets a shared pace.
