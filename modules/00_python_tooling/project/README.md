# Project: Walking Data Explorer

You have a recording from a wearable IMU worn by someone walking. Write a small toolkit that loads the recording, summarizes it, counts steps, and plots it. This is the first piece of the team's data pipeline.

## Setup

From this folder, with your virtual environment active:

```bash
python generate_data.py          # creates sample_walk.csv (30 s of fake walking)
pytest                           # every test fails until you write the code
```

The generated CSV has these columns:

| Column | Meaning | Unit |
|---|---|---|
| `timestamp_s` | time since start | seconds |
| `acc_x`, `acc_y`, `acc_z` | acceleration (z is vertical; about 9.81 when still) | m/s^2 |
| `gyro_x`, `gyro_y`, `gyro_z` | rotation rate | degrees/second |

The sensor samples 100 times per second (100 Hz).

## What to write

Open `explore.py` and fill in five functions. Work in this order, running `pytest` after each one.

### 1. `load_data(path)`

Read the CSV and return a DataFrame. (Lesson 3: `pd.read_csv`.)

### 2. `summarize(df)`

Return a dict with `n_samples`, `duration_s`, `sample_rate_hz`, and `column_means` (the mean of every sensor column, excluding `timestamp_s`). Compute the sample rate from the **median** time step so that a few dropouts do not throw it off.

### 3. `acc_magnitude(df)`

Return a Series with the length of the acceleration vector for each sample. Use vectorized numpy or pandas operations, not a loop.

### 4. `count_steps(df, window=5)`

Count steps using this method:

1. Take the acceleration magnitude.
2. Smooth it with a centered rolling mean of `window` samples.
3. Count the places where the smoothed signal crosses **upward** through its own mean.

*Hint:* make a boolean array `above = smooth > smooth.mean()`. An upward crossing is a position where `above` is True and the previous value was False. Why smooth first? Try it without and see what happens to the count.

### 5. `plot_signals(df, out_path)`

Save a PNG with three stacked panels sharing a time axis: acceleration, rotation rate, and acceleration magnitude. Label every axis with units and give the plot a title. Open the image and look at it. Does it look like walking?

## Checking your work

```bash
pytest -v
```

All tests passing means the project is done.

## Questions to think about

- The generator walks at 1.8 steps per second. Does your step count agree for a 30 second recording? What would make it wrong on real data?
- Why use the median time step instead of the mean?
- Look at your plot. Which channel shows the walking rhythm most clearly?

## Stretch goals

- Add a `cadence(df)` function that returns steps per minute.
- Make `count_steps` ignore tiny crossings caused by noise (for example by requiring a minimum time between steps).
- Run `python generate_data.py --seed 5` and check that your functions work on a different recording.

When you are done, move on to the [checkpoint](../checkpoint/README.md).
