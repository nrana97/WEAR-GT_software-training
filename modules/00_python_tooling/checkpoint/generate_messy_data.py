"""Generate a deliberately messy recording for the Level 0 checkpoint.

Real recordings have problems. This one has three of them:
  * some rows are out of time order
  * some rows are duplicated
  * some sensor values are missing (NaN)

You do not need to edit this file.

Usage:
    python generate_messy_data.py            # writes messy_walk.csv
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse the walking generator from the guided project.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "project"))
from generate_data import make_walk  # noqa: E402

SENSOR_COLUMNS = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]


def make_messy_walk(duration_s=20.0, seed=1):
    """Return a messy copy of a synthetic walk, plus the clean original.

    Returns:
        (messy_df, clean_df)
    """
    clean = make_walk(duration_s=duration_s, seed=seed)
    rng = np.random.default_rng(seed + 1000)
    messy = clean.copy()
    n = len(messy)

    # Missing values: about 3% of acc_z and 2% of gyro_x, away from the ends.
    interior = np.arange(5, n - 5)
    for col, frac in [("acc_z", 0.03), ("gyro_x", 0.02)]:
        idx = rng.choice(interior, size=int(frac * n), replace=False)
        messy.loc[idx, col] = np.nan

    # Duplicate rows (exact copies, appended at the end).
    dup_idx = rng.choice(n, size=15, replace=False)
    messy = pd.concat([messy, messy.iloc[dup_idx]], ignore_index=True)

    # Out-of-order rows: swap 20 random pairs.
    order = np.arange(len(messy))
    for _ in range(20):
        i, j = rng.choice(len(messy), size=2, replace=False)
        order[i], order[j] = order[j], order[i]
    messy = messy.iloc[order].reset_index(drop=True)

    return messy, clean


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="messy_walk.csv")
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    messy, _ = make_messy_walk(seed=args.seed)
    messy.to_csv(args.out, index=False)
    print(f"Wrote {len(messy)} rows to {args.out}")


if __name__ == "__main__":
    main()
