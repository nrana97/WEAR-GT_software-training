# Lesson 2: Session files, metadata, and reliable writes

**Goal:** save a recording so a teammate can interpret it later, validate it before writing, and avoid overwriting an existing session.

**Allow 45–60 minutes**, plus time to inspect the files you create. The project uses a CSV/JSON teaching convention rather than a final WEAR storage standard.

## Why a CSV alone is insufficient

A table of numbers does not explain which sensor produced it, what units it uses, how it was placed, or which firmware generated the data. Those details are metadata: information about the recording.

For training, each new session directory contains:

- `samples.csv`: rows of samples with `timestamp_s` and numeric sensor columns.
- `metadata.json`: the session context in a human-readable structured format.

Required metadata keys are `session_id`, `subject_id`, `task`, `sensor_placement`, and `firmware_version`, each a nonempty string. Use synthetic identifiers in exercises.

```python
metadata = {
    "session_id": "demo_001",
    "subject_id": "synthetic_01",
    "task": "simulated_walk",
    "sensor_placement": "simulated_right_ankle",
    "firmware_version": "sim_1",
    "units": {"raw": "count", "signal": "a.u."},
    "schema_version": 1,
}
```

Units and schema version are useful additions even though the project only requires the five core strings. A real system also needs clock-domain, calibration, hardware identity, and processing-history decisions.

## JSON and CSV serve different purposes

CSV is simple to inspect and works with pandas, but its types and units are not self-describing. JSON handles dictionaries and lists well, but it is not an efficient choice for millions of individual sensor samples.

```python
import json
import pandas as pd
from pathlib import Path

samples = pd.DataFrame({"timestamp_s": [0, .01, .02], "raw": [2048, 2050, 2049]})
folder = Path("practice_session")
folder.mkdir(exist_ok=False)
samples.to_csv(folder / "samples.csv", index=False)
(folder / "metadata.json").write_text(json.dumps(metadata, indent=2, allow_nan=False))
```

Run this only for a new folder. `index=False` prevents the pandas row index becoming an accidental data column. `allow_nan=False` rejects nonstandard NaN/infinity metadata values. Convert NumPy scalar types to ordinary Python values before JSON serialization when needed.

## Validate before touching the destination

The task requires finite, strictly increasing timestamps and numeric sensor columns. Sensor NaNs can be retained because missingness is data-quality information; missing or repeated timestamps make the session timeline ambiguous.

```python
import numpy as np

t = samples.timestamp_s.to_numpy(dtype=float)
if len(t) < 2 or not np.isfinite(t).all() or (np.diff(t) <= 0).any():
    raise ValueError("Invalid session timeline")
if not isinstance(metadata.get("task"), str) or not metadata["task"].strip():
    raise ValueError("Missing task")
```

Also serialize metadata before creating the directory. Otherwise a bad value could leave a CSV with no metadata. Validate duplicate column names as well: two columns called `raw` make later processing ambiguous.

## Avoid overwrites and partial sessions

A new directory with `exist_ok=False` makes accidental reuse visible through `FileExistsError`. If the CSV write succeeds but the metadata write fails, a simple training writer should remove the directory it just created and raise the error.

Only remove a directory that this operation created. Never delete a preexisting session to make a retry succeed. For a production writer, temporary files, atomic rename, recovery markers, and disk-full behavior need additional design; this project is a smaller teaching exercise.

## Check that you can read the result back

```python
loaded = pd.read_csv(folder / "samples.csv")
loaded_meta = json.loads((folder / "metadata.json").read_text())
print(loaded.columns.tolist())
print(loaded_meta["task"])
```

CSV round-tripping may alter inferred dtypes or floating-point representation slightly. Verify values and schema appropriately rather than expecting every representation detail to remain identical.

## Try it

1. Save a three-row synthetic recording with complete metadata. Read both files back and compare them with the originals.
2. Try writing to the same directory twice. Explain why the second attempt should fail.
3. Try missing task metadata, repeated timestamps, and a sensor column containing strings. Confirm rejection happens before a directory appears.
4. Add a NumPy value to metadata and test serialization. Convert it to a Python type deliberately.
5. Write a metadata checklist for the hardware lead. Distinguish fields implemented now from fields awaiting a team decision.

**Ready for the project when:** you can explain every saved column and metadata field, demonstrate no-overwrite behavior, and describe recovery from a failed write.

Next: [Alignment and missing samples](03_alignment.md)
