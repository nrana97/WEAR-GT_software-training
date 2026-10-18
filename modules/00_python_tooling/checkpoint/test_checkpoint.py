"""Tests for the Level 0 checkpoint. Run with `pytest`."""

import numpy as np
import pandas as pd
import pytest

from generate_messy_data import make_messy_walk, SENSOR_COLUMNS
import clean_report


@pytest.fixture
def data():
    messy, clean_truth = make_messy_walk(duration_s=20.0, seed=1)
    return messy, clean_truth


@pytest.fixture
def cleaned(data):
    messy, _ = data
    return clean_report.clean(messy)


def test_clean_returns_new_dataframe(data):
    messy, _ = data
    before = messy.copy()
    result = clean_report.clean(messy)
    assert isinstance(result, pd.DataFrame)
    assert result is not messy
    pd.testing.assert_frame_equal(messy, before)  # input untouched


def test_sorted_by_time(cleaned):
    assert cleaned["timestamp_s"].is_monotonic_increasing


def test_one_row_per_timestamp(cleaned):
    assert cleaned["timestamp_s"].is_unique


def test_correct_number_of_rows(cleaned, data):
    _, truth = data
    assert len(cleaned) == len(truth)
    assert cleaned["timestamp_s"].to_numpy() == pytest.approx(truth["timestamp_s"].to_numpy())


def test_no_missing_values(cleaned):
    assert not cleaned.isna().any().any()


def test_clean_index(cleaned):
    assert list(cleaned.index) == list(range(len(cleaned)))


def test_same_columns_same_order(cleaned, data):
    messy, _ = data
    assert list(cleaned.columns) == list(messy.columns)


def test_filled_values_are_reasonable(cleaned, data):
    _, truth = data
    # Interpolated values should land near the true noisy signal.
    for col in SENSOR_COLUMNS:
        diff = np.abs(cleaned[col].to_numpy() - truth[col].to_numpy())
        # Untouched values must match exactly; filled ones only roughly.
        assert np.median(diff) == pytest.approx(0.0, abs=1e-9)
        assert diff.max() < 5 * truth[col].std()


def test_report_keys(data, cleaned):
    messy, _ = data
    rep = clean_report.report(messy, cleaned)
    assert set(rep) == {
        "rows_raw", "rows_clean", "duplicates_removed", "was_sorted", "missing_filled",
    }


def test_report_values(data, cleaned):
    messy, _ = data
    rep = clean_report.report(messy, cleaned)
    assert rep["rows_raw"] == len(messy)
    assert rep["rows_clean"] == len(cleaned)
    assert rep["duplicates_removed"] == len(messy) - len(cleaned)
    assert rep["duplicates_removed"] == 15
    assert rep["was_sorted"] is False

    expected_missing = int(
        messy.sort_values("timestamp_s", kind="stable")
        .drop_duplicates("timestamp_s")[SENSOR_COLUMNS]
        .isna()
        .sum()
        .sum()
    )
    assert rep["missing_filled"] == expected_missing
    assert rep["missing_filled"] > 0


def test_report_on_already_clean_data():
    _, truth = make_messy_walk(duration_s=5.0, seed=4)
    cleaned = clean_report.clean(truth)
    rep = clean_report.report(truth, cleaned)
    assert rep["was_sorted"] is True
    assert rep["duplicates_removed"] == 0
    assert rep["missing_filled"] == 0
    pd.testing.assert_frame_equal(cleaned, truth)


def test_missing_at_edges_is_filled():
    _, truth = make_messy_walk(duration_s=2.0, seed=5)
    broken = truth.copy()
    broken.loc[0, "acc_z"] = np.nan
    broken.loc[len(broken) - 1, "gyro_x"] = np.nan
    out = clean_report.clean(broken)
    assert not out.isna().any().any()
    assert out.loc[0, "acc_z"] == pytest.approx(out.loc[1, "acc_z"])
    assert out.loc[len(out) - 1, "gyro_x"] == pytest.approx(out.loc[len(out) - 2, "gyro_x"])
