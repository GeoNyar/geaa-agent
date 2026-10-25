
"""Tests for the Survey-to-Insight descriptive analysis module."""

import json
from pathlib import Path

import pandas as pd
import pytest

from analyse_survey import analyse_survey
from generate_synthetic_data import generate_data


def test_analysis_creates_expected_outputs(tmp_path: Path):
    """Valid data should produce the expected tables, charts and manifest."""
    input_csv = tmp_path / "responses.csv"
    output_dir = tmp_path / "outputs"

    data = generate_data(n=20, seed=123)
    data.to_csv(input_csv, index=False)

    manifest = analyse_survey(input_csv, output_dir)

    assert manifest["dataset_type"] == "SYNTHETIC_NOT_REAL"
    assert manifest["records_analysed"] == 20
    assert manifest["analysis_allowed_by_validator"] is True

    for filename in manifest["outputs"]:
        assert (output_dir / filename).exists(), (
            f"Expected output was not created: {filename}"
        )

    frequencies = pd.read_csv(
        output_dir / "categorical_frequencies.csv"
    )
    assert {"variable", "response", "count", "percentage"}.issubset(
        frequencies.columns
    )


def test_analysis_stops_when_validation_fails(tmp_path: Path):
    """Invalid data should be reported and must not be analysed."""
    input_csv = tmp_path / "invalid_responses.csv"
    output_dir = tmp_path / "outputs"

    data = generate_data(n=10, seed=456)
    data.loc[0, "role"] = "Invalid role"
    data.to_csv(input_csv, index=False)

    with pytest.raises(ValueError, match="critical errors"):
        analyse_survey(input_csv, output_dir)

    report_path = output_dir / "validation_report.json"
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["analysis_allowed"] is False
    assert report["critical_error_count"] > 0

    # No analysis tables should be produced after failed validation.
    assert not (output_dir / "categorical_frequencies.csv").exists()
    assert not (output_dir / "analysis_manifest.json").exists()


def test_analysis_reports_optional_text_missingness(tmp_path: Path):
    """Missing optional Q12 responses should be counted, not imputed."""
    input_csv = tmp_path / "responses.csv"
    output_dir = tmp_path / "outputs"

    data = generate_data(n=10, seed=789)
    data["q12_challenge"] = None
    data.loc[0, "q12_challenge"] = "A synthetic example response"
    data.to_csv(input_csv, index=False)

    manifest = analyse_survey(input_csv, output_dir)

    assert manifest["q12_missing_responses"] == 9

    completeness = pd.read_csv(
        output_dir / "q12_response_completeness.csv"
    )
    missing_row = completeness.loc[
        completeness["measure"] == "missing_q12_responses"
    ].iloc[0]

    assert missing_row["count"] == 9
    assert missing_row["percentage_of_records"] == 90.0
