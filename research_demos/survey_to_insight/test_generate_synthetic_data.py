
"""Tests for the reproducible synthetic survey data generator."""

import pandas as pd
import pytest

from generate_synthetic_data import generate_data
from validate_data import REQUIRED_COLUMNS, validate_dataframe


def test_generator_creates_requested_number_of_records():
    data = generate_data(n=25, seed=123)

    assert len(data) == 25


def test_generator_uses_required_columns_in_correct_order():
    data = generate_data(n=10, seed=123)

    assert list(data.columns) == REQUIRED_COLUMNS


def test_generated_respondent_ids_are_unique():
    data = generate_data(n=100, seed=123)

    assert data["respondent_id"].is_unique
    assert data["respondent_id"].notna().all()


def test_generated_data_passes_validation():
    data = generate_data(n=100, seed=123)

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is True, report["errors"]
    assert report["critical_error_count"] == 0


def test_same_seed_produces_identical_data():
    first = generate_data(n=20, seed=456)
    second = generate_data(n=20, seed=456)

    pd.testing.assert_frame_equal(first, second)


def test_different_seeds_produce_different_data():
    first = generate_data(n=20, seed=123)
    second = generate_data(n=20, seed=456)

    assert not first.equals(second)


def test_zero_respondents_is_rejected():
    with pytest.raises(ValueError):
        generate_data(n=0)


def test_negative_respondent_count_is_rejected():
    with pytest.raises(ValueError):
        generate_data(n=-5)
