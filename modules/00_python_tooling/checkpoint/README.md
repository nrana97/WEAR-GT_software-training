# Checkpoint: clean a messy recording

Passing this checkpoint completes Level 0. If you already know Python, git, numpy, and pandas, start here. You get no step-by-step hints: the task is described below and `pytest` checks it.

## The situation

A recording came off a wearable sensor with three common problems: rows are **out of time order**, some rows are **duplicated**, and some sensor values are **missing** (NaN). Write code that fixes it and reports what it did.

Generate an example to look at:

```bash
python generate_messy_data.py        # creates messy_walk.csv
```

Columns are the same as in the project: `timestamp_s`, `acc_x`, `acc_y`, `acc_z`, `gyro_x`, `gyro_y`, `gyro_z`.

## What to write

Fill in `clean_report.py`.

### `clean(df)`

Takes a raw DataFrame and returns a **new** DataFrame (do not modify the input) that:

1. is sorted by `timestamp_s`, increasing
2. has exactly one row per `timestamp_s` (keep the first when there are duplicates)
3. has no missing values: fill gaps by **linear interpolation** along time order, and also fill any missing values at the very start or end with the nearest valid value
4. has a clean index numbered `0, 1, 2, ...`
5. keeps the same columns in the same order

### `report(raw, cleaned)`

Takes the raw DataFrame and the result of `clean`, and returns a dict with exactly these keys:

| Key | Meaning |
|---|---|
| `rows_raw` | number of rows in `raw` |
| `rows_clean` | number of rows in `cleaned` |
| `duplicates_removed` | `rows_raw - rows_clean` |
| `was_sorted` | `True` if `raw["timestamp_s"]` was already in increasing order, else `False` |
| `missing_filled` | the number of missing sensor values (NaN) that were filled, counted after sorting and removing duplicates and before interpolating |

## Passing

```bash
pytest -v
```

All tests must pass. Then submit a pull request following the root `CONTRIBUTING.md`: put your finished `clean_report.py` in `submissions/<your-github-username>/00_python_tooling/`.

A reviewer will also read your code. Clear names, short functions, and a docstring on each function count.

## Hints if you get stuck

You should not need these. If you do, it is a sign to read [lesson 3](../lessons/03_numpy_and_pandas.md) again. The tools you want are `sort_values`, `drop_duplicates`, `interpolate`, `ffill`/`bfill`, and `reset_index`.
