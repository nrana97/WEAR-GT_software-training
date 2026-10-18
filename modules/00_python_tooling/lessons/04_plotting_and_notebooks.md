# Lesson 4: Plotting, notebooks, and tests

Goal: look at your data, explore it interactively, and check your code automatically.

## Plotting with matplotlib

The most common plot for sensor data is signal versus time:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["timestamp_s"], df["acc_z"], label="acc_z")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Acceleration (m/s^2)")
ax.set_title("Vertical acceleration while walking")
ax.legend()
fig.savefig("acc_z.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

Notes:

- `fig, ax = plt.subplots()` is the pattern to follow. You draw on `ax`.
- **Always label axes with units** and give the plot a title. An unlabeled plot cannot be reviewed.
- `plt.close(fig)` frees memory, which matters if you make many plots.

### Several panels

Stack related channels so they share a time axis:

```python
fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
for ax, col in zip(axes, ["acc_x", "acc_y", "acc_z"]):
    ax.plot(df["timestamp_s"], df[col])
    ax.set_ylabel(col)
axes[-1].set_xlabel("Time (s)")
fig.tight_layout()
```

### Plotting without a screen

When a script runs on a server or inside tests, there is no window to show. Select a non-interactive backend before importing pyplot:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

Then save to a file instead of calling `plt.show()`.

### What to look for in a plot

Plot data before you analyze it. Look for flat lines (dead sensor), sudden jumps (dropouts or glitches), values stuck at a limit (saturation), slow drift, and gaps. Many of these are invisible in summary statistics.

## Jupyter notebooks

A notebook mixes code, output, and notes in cells. It is great for exploring, not for reusable code.

```bash
jupyter notebook
```

This opens a browser. Create a notebook, type code in a cell, and press Shift+Enter to run it. The last expression in a cell is displayed automatically, so a bare `df.head()` shows a table.

Habits that save pain:

- **Restart and run all** before sharing a notebook, to be sure it works top to bottom. Out-of-order cell execution is the most common notebook bug.
- Move code you want to reuse into a `.py` file as functions, and import it into the notebook.
- Do not commit notebooks full of large outputs.

A good workflow: explore in a notebook, then turn what works into functions in a script with tests.

## Testing with pytest

A test is a small function that checks your code gives the right answer. Files named `test_*.py` are found automatically.

```python
# test_helpers.py
from helpers import cadence_per_min

def test_cadence():
    assert cadence_per_min(54, 30.0) == 108.0

def test_cadence_zero_steps():
    assert cadence_per_min(0, 30.0) == 0.0
```

Run all tests in the current folder:

```bash
pytest
```

Output shows passes and failures. A failure tells you the line, the expected value, and the actual value. Floating-point numbers are not exact, so compare them with a tolerance:

```python
import pytest
assert cadence_per_min(1, 3.0) == pytest.approx(20.0)
```

Why this matters: when a model or a pipeline depends on your function, a test is how you know it still works after someone changes it. The project and checkpoint in this module are graded by tests, so you will see this immediately.

## Try it

1. Plot any numeric column from a CSV against its row number, with labeled axes, and save it as a PNG.
2. Write `helpers.py` with a function from the earlier lessons and a `test_helpers.py` with two tests. Run `pytest`.
3. Deliberately break the function and read the failure message.

You are ready for the [guided project](../project/README.md).
