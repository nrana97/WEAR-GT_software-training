# Contributing and submitting work

## Submitting a checkpoint

1. Create a branch named `submit/<module>/<your-github-username>`, for example `submit/00_python_tooling/janedoe`.
2. Put your finished files in `submissions/<your-github-username>/<module>/`. Do not edit the starter files in `modules/` directly.
3. Run the checkpoint tests and make sure they pass:
   ```bash
   cd modules/<module>/checkpoint
   pytest
   ```
   (Tests import the starter file by name, so copy your solution next to the tests to run them, or follow the module's checkpoint instructions.)
4. Open a pull request using the template. A reviewer will read your code, not just run the tests.

## Reviewing

Anyone who has passed a module's checkpoint can review that module's submissions. When reviewing, check:

- Do the tests pass?
- Is the code readable? Would a new teammate understand it?
- Are there hard-coded values or assumptions that should be named constants or parameters?

Leave at least one specific suggestion and one thing done well. Approve when the checkpoint is genuinely passed.

## Improving the training material

Found a typo, a confusing explanation, or a broken test? Open a PR against the module directly. To add a new module, copy `modules/_template/` and fill it in.

## Reference solutions

`reference_solutions/` holds one worked solution per project and checkpoint. Try the task yourself first. Looking at a solution before attempting the problem defeats the purpose, and the checkpoint only means something if you did it on your own.

## Data and privacy

This repo is private. Even so, never commit raw data from human subjects, names, or anything that could identify a participant. Datasets live outside the repo and are described in `data/README.md`.
