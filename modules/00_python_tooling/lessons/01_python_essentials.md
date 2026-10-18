# Lesson 1: Python essentials

Goal: read and write small Python programs. This lesson covers only what the rest of the training needs.

## Running Python

Two ways to run code:

```bash
python                # interactive prompt, good for trying things out
python my_script.py   # run a file
```

At the interactive prompt, `exit()` quits.

## Values and variables

```python
steps = 54            # int
duration_s = 30.0     # float
name = "walk_01"      # str
is_valid = True       # bool

cadence = steps / duration_s * 60   # arithmetic: 108.0
print(f"{name}: {cadence:.1f} steps/min")
```

The `f"..."` form is an f-string. Anything in `{}` is evaluated, and `:.1f` means "one decimal place".

Name things for what they mean. `duration_s` (with the unit) is better than `d`. Units in names prevent a lot of bugs in sensor code.

## Collections

```python
channels = ["acc_x", "acc_y", "acc_z"]      # list: ordered, changeable
channels.append("gyro_x")
first = channels[0]                          # indexing starts at 0
last = channels[-1]                          # negative counts from the end
some = channels[1:3]                         # slice: items 1 and 2

settings = {"sample_rate_hz": 100, "units": "m/s^2"}   # dict: key -> value
rate = settings["sample_rate_hz"]
settings["subject"] = "S01"
```

## Loops and conditions

```python
for ch in channels:
    print(ch)

for i in range(3):          # 0, 1, 2
    print(i)

if cadence > 120:
    label = "fast"
elif cadence > 80:
    label = "normal"
else:
    label = "slow"
```

A list comprehension builds a list in one line:

```python
upper = [ch.upper() for ch in channels]
accel_only = [ch for ch in channels if ch.startswith("acc")]
```

## Functions

A function packages up a task so you can reuse it:

```python
def cadence_per_min(step_count, duration_s):
    """Return steps per minute."""
    return step_count / duration_s * 60

print(cadence_per_min(54, 30.0))   # 108.0
```

Write a short docstring (the triple-quoted line) saying what the function does. Functions that take input and return output, without changing anything else, are easy to test. Most of the code you write in this training should look like this.

Default values and keyword arguments:

```python
def smooth(values, window=5):
    ...

smooth(data)             # uses window=5
smooth(data, window=9)   # override by name
```

## Files and modules

You will use libraries written by others:

```python
import math
import numpy as np          # "np" is the standard nickname
import pandas as pd         # "pd" likewise

print(math.sqrt(16))
```

And you will split your own code across files. If `helpers.py` defines `cadence_per_min`, another file in the same folder can do:

```python
from helpers import cadence_per_min
```

This is exactly how the tests in this module load your code.

## Reading errors

When Python fails it prints a **traceback**. Read it from the bottom up: the last line is the error type and message, and the lines above show where it happened.

```
Traceback (most recent call last):
  File "demo.py", line 3, in <module>
    print(channels[5])
IndexError: list index out of range
```

Common ones: `IndexError` (bad position), `KeyError` (missing dict key), `NameError` (typo in a name), `TypeError` (wrong kind of value), `ModuleNotFoundError` (package not installed, or your virtual environment is not active).

## Try it

Write `warmup.py` containing a function `mean(values)` that returns the average of a list of numbers without using any library, and a few `print` calls that check it on lists you can verify by hand. Then write `above(values, threshold)` that returns a new list with only the values greater than `threshold`.

Next: [Command line and git](02_command_line_and_git.md)
