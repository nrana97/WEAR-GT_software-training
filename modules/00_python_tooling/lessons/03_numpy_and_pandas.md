# Lesson 3: numpy and pandas

Goal: work with numeric arrays and tables of sensor data. These two libraries are the core of nearly everything else the team does.

## numpy: fast math on arrays

An array holds many numbers of one type, and math applies to every element at once. This is called **vectorization**, and it replaces most loops.

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0, 4.0])
a * 2                # [2. 4. 6. 8.]
a + a                # [2. 4. 6. 8.]
np.sqrt(a)           # element-wise square root
a.mean()             # 2.5
a.std()              # standard deviation
a.max(), a.min()
```

Useful constructors:

```python
np.zeros(5)                      # five zeros
np.arange(0, 1, 0.25)            # [0.   0.25 0.5  0.75]
np.linspace(0, 1, 5)             # 5 evenly spaced points from 0 to 1
```

### Boolean masks

Comparing an array gives an array of True/False. Use it to pick elements:

```python
x = np.array([0.1, 5.2, 3.3, 7.8])
x > 3                  # [False  True  True  True]
x[x > 3]               # [5.2 3.3 7.8]
(x > 3).sum()          # 3   (True counts as 1)
```

### Combining arrays

```python
acc = np.array([[0.1, 0.2, 9.8],
                [0.0, 0.3, 9.7]])      # 2 rows (samples) x 3 columns (axes)
acc.shape                # (2, 3)
np.sqrt((acc ** 2).sum(axis=1))   # magnitude of each row
```

`axis=1` means "collapse across columns, one result per row".

## pandas: labeled tables

A **DataFrame** is a table with named columns. It is how you will hold almost every recording.

```python
import pandas as pd

df = pd.read_csv("walk.csv")
df.head()            # first 5 rows
df.shape             # (rows, columns)
df.columns           # column names
df.dtypes            # type of each column
df.describe()        # count, mean, std, min, max per column
df.info()            # types and missing values at a glance
```

Always run `head()`, `shape`, and `describe()` on new data before doing anything else. Most data problems show up immediately.

### Selecting

```python
df["acc_z"]                       # one column (a Series)
df[["acc_x", "acc_z"]]            # several columns (a DataFrame)
df.iloc[0]                        # first row, by position
df.iloc[10:20]                    # rows 10 to 19
df[df["acc_z"] > 12]              # rows where a condition holds
```

### Creating and changing columns

```python
df["acc_mag"] = np.sqrt(df["acc_x"]**2 + df["acc_y"]**2 + df["acc_z"]**2)
df = df.rename(columns={"acc_mag": "magnitude"})
df = df.drop(columns=["gyro_z"])
```

### Sorting, duplicates, missing values

These three appear in almost every real recording.

```python
df = df.sort_values("timestamp_s")                        # order by time
df = df.drop_duplicates(subset="timestamp_s")             # one row per timestamp
df.isna().sum()                                           # missing values per column
df = df.interpolate()                                     # fill gaps linearly
df = df.reset_index(drop=True)                            # renumber rows 0..n-1
```

If you sort or drop rows and then use `df.iloc`, call `reset_index(drop=True)` first or the row labels will not match positions.

### Rolling windows

Smoothing a noisy signal by averaging neighbors:

```python
smooth = df["acc_z"].rolling(window=5, center=True, min_periods=1).mean()
```

`center=True` keeps the smoothed signal lined up with the original in time. `min_periods=1` avoids NaN at the edges.

### Working with time

Timestamps in seconds are fine for this module. The sampling rate is how many samples per second:

```python
dt = df["timestamp_s"].diff().median()     # typical time step
sample_rate_hz = 1.0 / dt
```

Use the **median** step rather than the mean, because a few large gaps (dropouts) would distort the mean.

## Common mistakes

- **Modifying a copy by accident.** `df2 = df` does not copy. Use `df2 = df.copy()`.
- **Looping over rows.** `for i in range(len(df))` is slow and usually unnecessary. Reach for a vectorized expression first.
- **Forgetting units.** Name columns with units where you can (`timestamp_s`, `acc_x` in m/s^2). A column of numbers with no unit is a future bug.
- **Trusting the data.** Check `shape`, `describe()`, and missing values every time.

## Try it

Using any small CSV (make one by hand with five rows if you like):

1. Load it and print `head()`, `shape`, and `describe()`.
2. Add a column that is the sum of two others.
3. Filter to rows where one column is above its own mean.
4. Introduce a missing value, find it with `isna()`, and fill it with `interpolate()`.

Next: [Plotting and notebooks](04_plotting_and_notebooks.md)
