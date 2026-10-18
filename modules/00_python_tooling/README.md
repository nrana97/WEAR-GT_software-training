# Level 0: Python and tooling

The foundation for everything else on the software team: Python, the command line, git, numpy and pandas, and plotting. By the end you will be able to load a sensor recording, summarize it, clean it, and plot it.

## What you will learn

- Write and run Python scripts with functions, loops, and basic data structures
- Use the command line and git to manage your work and submit it
- Load, inspect, and transform tabular data with pandas, and do math on arrays with numpy
- Make labeled plots with matplotlib and explore data in a Jupyter notebook
- Run automated tests with `pytest` to check your own code

## Prerequisites

None. If you already write Python and use git comfortably, skip straight to the [checkpoint](checkpoint/README.md).

## Time estimate

About 6 to 10 hours for the lessons and project if you are starting from scratch.

## Setup

You need Python 3.10 or newer and git. From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Check that it worked:

```bash
python --version
pytest --version
```

## How to work through this module

1. Read the lessons in order. Type the examples yourself instead of copying them.
2. Do the guided [project](project/README.md). Run `pytest` until every test passes.
3. Attempt the [checkpoint](checkpoint/README.md). Passing it completes the module.

**Already know this material?** Go straight to the checkpoint. If you can pass it without the lessons, move on to Level 1.

## Lessons

1. [Python essentials](lessons/01_python_essentials.md)
2. [Command line and git](lessons/02_command_line_and_git.md)
3. [numpy and pandas](lessons/03_numpy_and_pandas.md)
4. [Plotting and notebooks](lessons/04_plotting_and_notebooks.md)

## Why synthetic data?

The project and checkpoint use fake walking data from a small generator script. That way you can practice the exact skills the team needs (loading, cleaning, summarizing, plotting sensor recordings) before we have real hardware data, and everyone gets identical results.

## How this module feeds the capstone

Level 0 builds the "clean" stage of the pipeline. The checkpoint's cleaning function (sort, de-duplicate, fill gaps) is the first version of what the capstone will run on every recording.
