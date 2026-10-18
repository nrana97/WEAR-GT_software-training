"""Tests for the Walking Data Explorer project. Run with `pytest`."""

import numpy as np
import pandas as pd
import pytest

from generate_data import make_walk
import explore


@pytest.fixture
def walk():
    return make_walk(duration_s=30.0, seed=0)


@pytest.fixture
def walk_csv(tmp_path, walk):
    path = tmp_path / "walk.csv"
    walk.to_csv(path, index=False)
    return path


def test_load_data_returns_dataframe(walk_csv, walk):
    df = explore.load_data(walk_csv)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == list(walk.columns)
    assert len(df) == len(walk)


def test_load_data_values_match(walk_csv, walk):
    df = explore.load_data(walk_csv)
    assert df["acc_z"].to_numpy() == pytest.approx(walk["acc_z"].to_numpy())


def test_summarize_basic_fields(walk):
    s = explore.summarize(walk)
    assert s["n_samples"] == 3000
    assert s["duration_s"] == pytest.approx(29.99)
    assert s["sample_rate_hz"] == pytest.approx(100.0)


def test_summarize_column_means(walk):
    s = explore.summarize(walk)
    means = s["column_means"]
    assert "timestamp_s" not in means
    assert set(means) == {"acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"}
    assert means["acc_z"] == pytest.approx(walk["acc_z"].mean())
    # Gravity: the vertical axis averages close to 9.81 m/s^2.
    assert means["acc_z"] == pytest.approx(9.81, abs=0.3)


def test_summarize_sample_rate_ignores_one_big_gap(walk):
    gappy = walk.drop(index=range(1000, 1100)).reset_index(drop=True)
    s = explore.summarize(gappy)
    # One 1-second gap must not change the typical sample rate.
    assert s["sample_rate_hz"] == pytest.approx(100.0)


def test_acc_magnitude_values():
    df = pd.DataFrame({
        "timestamp_s": [0.0, 0.01],
        "acc_x": [3.0, 0.0],
        "acc_y": [4.0, 0.0],
        "acc_z": [0.0, 9.81],
    })
    mag = explore.acc_magnitude(df)
    assert list(mag) == pytest.approx([5.0, 9.81])


def test_acc_magnitude_is_series_same_length(walk):
    mag = explore.acc_magnitude(walk)
    assert isinstance(mag, pd.Series)
    assert len(mag) == len(walk)


def test_count_steps_matches_expected(walk):
    # 30 s at 1.8 steps/s is about 54 steps.
    steps = explore.count_steps(walk)
    assert isinstance(steps, (int, np.integer))
    assert 52 <= steps <= 56


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_count_steps_other_recordings(seed):
    df = make_walk(duration_s=20.0, seed=seed)
    steps = explore.count_steps(df)
    # 20 s at 1.8 steps/s is about 36 steps.
    assert 34 <= steps <= 38


def test_count_steps_standing_still_is_zero():
    t = np.arange(0, 10, 0.01)
    df = pd.DataFrame({
        "timestamp_s": t,
        "acc_x": 0.0,
        "acc_y": 0.0,
        "acc_z": 9.81,
        "gyro_x": 0.0,
        "gyro_y": 0.0,
        "gyro_z": 0.0,
    })
    assert explore.count_steps(df) == 0


def test_plot_signals_writes_png(walk, tmp_path):
    out = tmp_path / "signals.png"
    result = explore.plot_signals(walk, out)
    assert result is None
    assert out.exists()
    assert out.stat().st_size > 1000
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
