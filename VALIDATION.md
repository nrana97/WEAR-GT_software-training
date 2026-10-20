# Validation of the completed training edition

- All 14 reference task suites passed: 25 existing Module 00 tests and 30 new tests.
- Each of the six new project example drivers ran successfully against its reference implementation.
- All Python files compiled successfully.
- All local Markdown navigation links resolved.
- Original Module 00 starter, lesson, generator, test, and solution files match the uploaded archive byte for byte.
- The generated session-review figure was visually inspected for labels, missing-data breaks, and layout.

Validation environment: Python 3.12. Student starter functions deliberately raise
NotImplementedError. The reference verifier runs in temporary copies and does
not fill in student exercises. No hardware or human data were used. These checks
do not validate real-time acquisition, real sensor calibration, or device safety.

## Expanded six-week curriculum revision

- All 18 replacement lessons contain approximately 640–800 whitespace-delimited
  words each, including code, compared with the shorter first-edition notes.
- Every Python example block executed successfully in lesson order; examples
  using the ML fixture were run with the supplied generator available.
- Worked examples, units, expected results, exercises, and onward navigation
  are included in each lesson.
- A six-week plan specifies weekly workload, submissions, review questions,
  final bridge experiment, and a seventh-week option for new programmers.
- Project/checkpoint APIs and implementation files are unchanged by this revision.
