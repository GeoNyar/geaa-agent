
"""Automated tests for the Survey-to-Insight validation module."""

import pandas as pd

from validate_data import REQUIRED_COLUMNS, validate_dataframe


def make_valid_data():
    """Create a small, valid synthetic test dataset."""
    return pd.DataFrame([
        {
            "respondent_id": "SYN001",
            "role": "Teacher or lecturer",
            "experience": "4–6 years",
            "q3_questionnaire_design": 3,
            "q4_data_validation": 4,
            "q5_excel": 4,
            "q6_descriptive_statistics": 3,
            "q7_crosstabs": 2,
            "q8_visualisation": 4,
            "q9_reporting": 3,
            "q10_tasks": "Collected survey data;Produced charts or visualisations",
            "q11_development_need": "Descriptive statistics",
            "q12_challenge": "Practice interpreting survey results",
        },
        {
            "respondent_id": "SYN002",
            "role": "Research or monitoring and evaluation staff",
            "experience": "More than 10 years",
            "q3_questionnaire_design": 5,
            "q4_data_validation": 4,
            "q5_excel": 5,
            "q6_descriptive_statistics": 4,
            "q7_crosstabs": 4,
            "q8_visualisation": 3,
            "q9_reporting": 5,
            "q10_tasks": "Designed a questionnaire",
            "q11_development_need": "Data visualisation and dashboards",
            "q12_challenge": None,
        },
    ])


def test_valid_dataset_passes():
    report = validate_dataframe(make_valid_data())

    assert report["analysis_allowed"] is True
    assert report["critical_error_count"] == 0


def test_missing_required_column_is_critical():
    data = make_valid_data().drop(columns=["role"])

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is False
    assert "role" in report["missing_required_columns"]
    
def test_fractional_familiarity_score_is_rejected():
    data = make_valid_data()
    data["q3_questionnaire_design"] = (
        data["q3_questionnaire_design"].astype(float)
    )
    data.loc[0, "q3_questionnaire_design"] = 2.5

    result = validate_dataframe(data)

    assert result["analysis_allowed"] is False
    assert any(
        "q3_questionnaire_design" in error
        for error in result["errors"]
    )


def test_duplicate_respondent_id_is_rejected():
    data = make_valid_data()
    data.loc[1, "respondent_id"] = "SYN001"

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is False
    assert any(
        error["type"] == "duplicate_respondent_id"
        for error in report["errors"]
    )


def test_invalid_role_is_rejected():
    data = make_valid_data()
    data.loc[0, "role"] = "Chief Data Wizard"

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is False
    assert any(
        error["type"] == "invalid_category"
        and error["column"] == "role"
        for error in report["errors"]
    )


def test_q10_exclusive_option_conflict_is_rejected():
    data = make_valid_data()
    data.loc[0, "q10_tasks"] = (
        "None of the above;Collected survey data"
    )

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is False
    assert any(
        error["type"] == "exclusive_option_conflict"
        for error in report["errors"]
    )


def test_missing_familiarity_response_is_allowed_and_reported():
    data = make_valid_data()
    data.loc[0, "q3_questionnaire_design"] = None

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is True
    assert report["missing_by_variable"]["q3_questionnaire_design"] == 1


def test_unexpected_column_generates_warning():
    data = make_valid_data()
    data["unexpected_field"] = "review"

    report = validate_dataframe(data)

    assert report["analysis_allowed"] is True
    assert "unexpected_field" in report["unexpected_columns"]
    assert any(
        warning["type"] == "unexpected_column"
        for warning in report["warnings"]
    )


def test_required_column_definition_is_complete():
    data = make_valid_data()

    assert list(data.columns) == REQUIRED_COLUMNS
