"""Generate a synthetic walking recording from a fake wearable IMU.

An IMU (inertial measurement unit) reports acceleration and rotation rate.
This script fakes a person walking at a steady pace so you can practice
without any hardware. You do not need to edit this file.

Usage:
    python generate_data.py                 # writes sample_walk.csv
    python generate_data.py --seed 3        # a different random recording
"""

import argparse

import numpy as np
import pandas as pd

SAMPLE_RATE_HZ = 100
STEP_FREQ_HZ = 1.8  # about 108 steps per minute

COLUMNS = ["timestamp_s", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]


def make_walk(duration_s=30.0, sample_rate_hz=SAMPLE_RATE_HZ,
              step_freq_hz=STEP_FREQ_HZ, seed=0):
    """Return a DataFrame of synthetic walking data.

    Columns:
        timestamp_s        time in seconds, starting at 0
        acc_x, acc_y, acc_z   acceleration in m/s^2 (z is vertical, ~9.81 at rest)
        gyro_x, gyro_y, gyro_z   rotation rate in degrees/second
    """
    rng = np.random.default_rng(seed)
    n = int(round(duration_s * sample_rate_hz))
    t = np.arange(n) / sample_rate_hz
    phase = 2 * np.pi * step_freq_hz * t

    acc_x = 0.8 * np.sin(phase) + rng.normal(0, 0.15, n)
    acc_y = 0.3 * np.sin(phase / 2) + rng.normal(0, 0.15, n)
    acc_z = 9.81 + 2.5 * np.sin(phase + np.pi / 4) + rng.normal(0, 0.2, n)

    gyro_x = 30 * np.sin(phase) + rng.normal(0, 3, n)
    gyro_y = 15 * np.sin(phase / 2) + rng.normal(0, 3, n)
    gyro_z = 8 * np.sin(phase + np.pi / 3) + rng.normal(0, 3, n)

    return pd.DataFrame({
        "timestamp_s": t,
        "acc_x": acc_x,
        "acc_y": acc_y,
        "acc_z": acc_z,
        "gyro_x": gyro_x,
        "gyro_y": gyro_y,
        "gyro_z": gyro_z,
    })[COLUMNS]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="sample_walk.csv", help="output CSV path")
    parser.add_argument("--duration", type=float, default=30.0, help="seconds")
    parser.add_argument("--seed", type=int, default=0, help="random seed")
    args = parser.parse_args()

    df = make_walk(duration_s=args.duration, seed=args.seed)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
