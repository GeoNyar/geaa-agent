
"""
Survey-to-Insight: Data Validation Module

Purpose:
    Validate survey CSV data before analysis.

Important:
    The module reports data-quality issues. It does not silently
    delete records, correct invalid answers, or impute missing values.
    The dataset is intended for a synthetic demonstration.
"""

import argparse
import json
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Define the expected survey structure
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "respondent_id",
    "role",
    "experience",
    "q3_questionnaire_design",
    "q4_data_validation",
    "q5_excel",
    "q6_descriptive_statistics",
    "q7_crosstabs",
    "q8_visualisation",
    "q9_reporting",
    "q10_tasks",
    "q11_development_need",
    "q12_challenge",
]

ROLE_OPTIONS = {
    "Teacher or lecturer",
    "School or institutional leader",
    "Education programme or project staff",
    "Research or monitoring and evaluation staff",
    "Student or trainee",
    "Other",
    "Prefer not to say",
}

EXPERIENCE_OPTIONS = {
    "Less than 1 year",
    "1–3 years",
    "4–6 years",
    "7–10 years",
    "More than 10 years",
    "Not applicable",
}

DEVELOPMENT_NEED_OPTIONS = {
    "Questionnaire design",
    "Data cleaning and quality assurance",
    "Excel and spreadsheet analysis",
    "Descriptive statistics",
    "Cross-tabulations and interpretation",
    "Data visualisation and dashboards",
    "Report and presentation writing",
    "Other",
    "Prefer not to say",
}

TASK_OPTIONS = {
    "Designed a questionnaire",
    "Collected survey data",
    "Cleaned or validated a dataset",
    "Analysed quantitative data",
    "Produced charts or visualisations",
    "Prepared a research or evaluation report",
    "Used an interactive dashboard",
    "None of the above",
    "Prefer not to say",
}

FAMILIARITY_COLUMNS = [
    "q3_questionnaire_design",
    "q4_data_validation",
    "q5_excel",
    "q6_descriptive_statistics",
    "q7_crosstabs",
    "q8_visualisation",
    "q9_reporting",
]


# ---------------------------------------------------------
# 2. Validation functions
# ---------------------------------------------------------

def is_missing(value):
    """Return True for a recognised missing value."""
    if pd.isna(value):
        return True

    if isinstance(value, str) and not value.strip():
        return True

    return False


def validate_dataframe(df):
    """
    Validate a survey DataFrame.

    Returns a dictionary containing errors, warnings,
    missingness summaries and an overall validity decision.
    """

    errors = []
    warnings = []
    missing_by_variable = {}
    missing_by_record = []

    # Check structure first.
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column for column in df.columns
        if column not in REQUIRED_COLUMNS
    ]

    for column in missing_columns:
        errors.append({
            "type": "missing_required_column",
            "column": column,
            "message": f"Required column '{column}' is absent.",
        })

    for column in unexpected_columns:
        warnings.append({
            "type": "unexpected_column",
            "column": column,
            "message": f"Unexpected column '{column}' was found.",
        })

    # Do not attempt value checks for absent columns.
    available_columns = [
        column for column in REQUIRED_COLUMNS
        if column in df.columns
    ]

    # Report missing values by variable and record.
    for column in available_columns:
        missing_rows = []

        for index, value in df[column].items():
            if is_missing(value):
                missing_rows.append(index)

        missing_by_variable[column] = len(missing_rows)

        for index in missing_rows:
            missing_by_record.append({
                "row_index": int(index)
                if isinstance(index, int)
                else str(index),
                "respondent_id": (
                    str(df.at[index, "respondent_id"])
                    if "respondent_id" in df.columns
                    and not is_missing(df.at[index, "respondent_id"])
                    else None
                ),
                "column": column,
            })

    # A missing value is not automatically a critical error.
    # The rules below identify where missingness is unacceptable.

    # Validate respondent IDs.
    if "respondent_id" in df.columns:
        ids = df["respondent_id"]

        for index, value in ids.items():
            if is_missing(value):
                errors.append({
                    "type": "missing_respondent_id",
                    "row_index": str(index),
                    "column": "respondent_id",
                    "message": "Respondent ID is missing or blank.",
                })

        non_missing_ids = ids[
            ids.apply(lambda value: not is_missing(value))
        ]

        duplicate_mask = non_missing_ids.duplicated(keep=False)

        for index, value in non_missing_ids[duplicate_mask].items():
            errors.append({
                "type": "duplicate_respondent_id",
                "row_index": str(index),
                "column": "respondent_id",
                "value": str(value),
                "message": "Respondent ID is duplicated.",
            })

    # Validate single-choice categorical variables.
    categorical_options = {
        "role": ROLE_OPTIONS,
        "experience": EXPERIENCE_OPTIONS,
        "q11_development_need": DEVELOPMENT_NEED_OPTIONS,
    }

    for column, allowed_values in categorical_options.items():
        if column not in df.columns:
            continue

        for index, value in df[column].items():
            if is_missing(value):
                continue

            if not isinstance(value, str) or value not in allowed_values:
                errors.append({
                    "type": "invalid_category",
                    "row_index": str(index),
                    "column": column,
                    "value": str(value),
                    "message": (
                        f"Value is not a permitted response for {column}."
                    ),
                })

    # Validate Q3-Q9: integer values from 1 to 5, or missing.
    for column in FAMILIARITY_COLUMNS:
        if column not in df.columns:
            continue

        for index, value in df[column].items():
            if is_missing(value):
                continue

            valid_integer = (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and float(value).is_integer()
                and 1 <= float(value) <= 5
            )

            if not valid_integer:
                errors.append({
                    "type": "invalid_familiarity_score",
                    "row_index": str(index),
                    "column": column,
                    "value": str(value),
                    "message": (
                        "Expected an integer from 1 to 5 or a missing value."
                    ),
                })

    # Validate Q10 multiple-response selections.
    # Selections must be separated by semicolons.
    if "q10_tasks" in df.columns:
        for index, value in df["q10_tasks"].items():
            if is_missing(value):
                continue

            if not isinstance(value, str):
                errors.append({
                    "type": "invalid_multiple_response_format",
                    "row_index": str(index),
                    "column": "q10_tasks",
                    "value": str(value),
                    "message": "Q10 selections must be a delimited text field.",
                })
                continue

            selections = [item.strip() for item in value.split(";")]

            if any(not item for item in selections):
                errors.append({
                    "type": "empty_multiple_response_selection",
                    "row_index": str(index),
                    "column": "q10_tasks",
                    "value": value,
                    "message": "Q10 contains an empty selection.",
                })

            if len(selections) != len(set(selections)):
                errors.append({
                    "type": "duplicate_multiple_response_selection",
                    "row_index": str(index),
                    "column": "q10_tasks",
                    "value": value,
                    "message": "A Q10 selection appears more than once.",
                })

            invalid_selections = [
                item for item in selections
                if item not in TASK_OPTIONS
            ]

            if invalid_selections:
                errors.append({
                    "type": "invalid_multiple_response_selection",
                    "row_index": str(index),
                    "column": "q10_tasks",
                    "value": invalid_selections,
                    "message": "Q10 contains an unrecognised selection.",
                })

            exclusive_options = {
                "None of the above",
                "Prefer not to say",
            }

            if (
                len(selections) > 1
                and any(item in exclusive_options for item in selections)
            ):
                errors.append({
                    "type": "exclusive_option_conflict",
                    "row_index": str(index),
                    "column": "q10_tasks",
                    "value": value,
                    "message": (
                        "'None of the above' and 'Prefer not to say' "
                        "must each be selected alone."
                    ),
                })

    # Validate Q12 as text or missing.
    if "q12_challenge" in df.columns:
        for index, value in df["q12_challenge"].items():
            if is_missing(value):
                continue

            if not isinstance(value, str):
                errors.append({
                    "type": "invalid_text_response",
                    "row_index": str(index),
                    "column": "q12_challenge",
                    "value": str(value),
                    "message": "Q12 must contain text or a missing value.",
                })

    # Flag exact duplicate records for review.
    if len(available_columns) == len(REQUIRED_COLUMNS):
        duplicate_rows = df.duplicated(
            subset=REQUIRED_COLUMNS,
            keep=False,
        )

        for index in df.index[duplicate_rows]:
            warnings.append({
                "type": "duplicate_record_review",
                "row_index": str(index),
                "message": (
                    "Record matches another record across all survey "
                    "columns. Review manually; no record was deleted."
                ),
            })

    return {
        "dataset_rows": int(len(df)),
        "dataset_columns": int(len(df.columns)),
        "required_columns": REQUIRED_COLUMNS,
        "missing_required_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "missing_by_variable": missing_by_variable,
        "missing_by_record": missing_by_record,
        "errors": errors,
        "warnings": warnings,
        "critical_error_count": len(errors),
        "warning_count": len(warnings),
        "analysis_allowed": len(errors) == 0,
    }


# ---------------------------------------------------------
# 3. Command-line interface
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate Survey-to-Insight survey data."
    )

    parser.add_argument(
        "input_csv",
        help="Path to the survey CSV file.",
    )

    parser.add_argument(
        "--report",
        default="validation_report.json",
        help="Output JSON report path.",
    )

    args = parser.parse_args()

    input_path = Path(args.input_csv)
    report_path = Path(args.report)

    if not input_path.exists():
        parser.error(f"Input file does not exist: {input_path}")

    try:
        df = pd.read_csv(input_path)
    except Exception as exc:
        parser.error(f"Could not read CSV file: {exc}")

    report = validate_dataframe(df)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Survey data validation completed.")
    print(f"Rows checked: {report['dataset_rows']}")
    print(f"Critical errors: {report['critical_error_count']}")
    print(f"Warnings: {report['warning_count']}")
    print(f"Analysis allowed: {report['analysis_allowed']}")
    print(f"Report saved to: {report_path}")

    if not report["analysis_allowed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

