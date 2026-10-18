# WEAR Software Training

Self-paced training for the WEAR @ GT software team. WEAR builds exoskeleton and prosthetic devices, and the software team's job is the data side of that: collecting sensor data reliably, logging it, visualizing it, and building machine learning models on top of it (in Python).

You do not need any prior experience. Start at Level 0. If you already know a topic, you can skip it by passing its checkpoint (see below).

## How the program works

Training is a **module ladder**, not a weekly schedule. Each module has the same three parts:

| Part | What it is |
|---|---|
| `lessons/` | Short written lessons. Read them in order. |
| `project/` | A guided project with starter code and automated tests. |
| `checkpoint/` | A harder, less guided task. **Passing it is how you skip ahead.** |

### Skipping ahead

Not sure where to start? Open the `checkpoint/` folder of the module you think you already know and try it first.

- If you can pass the checkpoint tests without reading the lessons, you have completed that module. Move on.
- If you get stuck, go back to the lessons and project for that module, then retry the checkpoint.

Nobody needs permission to skip. The checkpoint is the test.

### Submitting work

When you finish a checkpoint, open a pull request following [CONTRIBUTING.md](CONTRIBUTING.md). An experienced member reviews it. Reviewing other people's checkpoints is also part of the program.

## The ladder

| Level | Module | Status |
|---|---|---|
| 0 | [Python and tooling](modules/00_python_tooling/) | Written |
| 1 | [Sensors and time series](modules/01_sensors_timeseries/) | Stub |
| 2 | [Data collection and logging](modules/02_data_collection_logging/) | Stub |
| 3a | [Signal processing](modules/03a_signal_processing/) | Stub |
| 3b | [Visualization and dashboards](modules/03b_visualization/) | Stub |
| 4 | [ML for movement](modules/04_ml_for_movement/) | Stub |
| 5 | [Deployment and safety](modules/05_deployment_safety/) | Stub |

Levels 3a and 3b are parallel branches. Pick either, or do both. Level 4 needs Levels 2 and 3a.

## The capstone

Every module's project feeds one shared team pipeline in [`capstone_pipeline/`](capstone_pipeline/): collect, log, clean, visualize, model. The goal is that finishing the training means you have helped build something the team actually uses.

## Repo layout

```
modules/              the ladder (lessons, project, checkpoint per module)
  _template/          copy this to start a new module
capstone_pipeline/    the shared team pipeline
reference_solutions/  worked solutions for projects and checkpoints
data/                 pointers to datasets (the data itself is not committed)
```

## Getting set up

Each module lists what it needs. For Level 0, see [its README](modules/00_python_tooling/README.md). Python 3.10 or newer is required everywhere.

```bash
git clone <this repo's URL>
cd wear-software-training
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## A note on the hardware

The exact sensors WEAR will use are still being decided. Early modules use synthetic data and public datasets, so the skills transfer to whatever hardware the team ends up with.

## Credits

The module-with-project-and-reference-solution format was inspired by the [RoboJackets software training](https://github.com/RoboJackets/software-training) program. All content here is original.
