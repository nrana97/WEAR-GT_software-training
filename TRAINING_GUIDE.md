# Using the completed training modules

Modules 01–05 (including 03a and 03b) now contain three lessons, a guided
project, a separate checkpoint, deterministic synthetic-data generators,
automated behavioral tests, and standalone reference implementations.
Module 00 is preserved as supplied. New tests use unittest and also run under pytest.

## Pace and expectations

Follow [SIX_WEEK_PLAN.md](SIX_WEEK_PLAN.md) for the six-week route, about
6–8 hours per week. It includes both visualization and signal processing,
weekly artifacts, peer review, and a final handoff/bridge experiment.
The 18 expanded lessons contain explanations, worked code, exercises,
and expected results; reading alone does not complete the training.

## For learners

Install requirements.txt in a virtual environment. Open a module README,
read its lessons, then enter its project folder and run:

```bash
python generate_data.py
python -m unittest -v test_task
```

Starter functions deliberately raise NotImplementedError. Implement them to
pass tests; then do the checkpoint. Save your reasoning and requested plots
for review. Generated data and figures are ignored by git.

## For leads

```bash
python tools/verify_reference_solutions.py
```

This runs each task's tests against its reference implementation in an isolated
temporary directory; it does not overwrite student starter files. It includes
Module 00. New task files reuse the name test_task.py, so run tests per task
folder rather than collecting every module in one pytest invocation.

Checkpoint completion requires the automated tests **and** human review of
the requested report/plots. Tests are behavioral checks, not proof of hardware
readiness. All recordings and specifications are synthetic examples.

## Push these files

Extract this archive, then copy its contents into your local repository root.
Review the diff, commit the additions and README/requirements updates, and
push your branch. Do not place the containing wear-software-training folder
inside your repository as an extra nested folder.

The original ZIP is unchanged. No GitHub push has been performed.
