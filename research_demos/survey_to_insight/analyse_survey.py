
"""Descriptive analysis for the Survey-to-Insight demonstration.

All outputs describe synthetic data unless the input is explicitly
replaced with an appropriately authorised real dataset.
The script does not make causal claims or silently modify records.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from validate_data import (
    FAMILIARITY_COLUMNS,
    validate_dataframe,
)


def analyse_survey(input_csv: Path, output_dir: Path) -> dict:
    """Validate input, then produce descriptive tables and charts."""

    data = pd.read_csv(input_csv)
    validation = validate_dataframe(data)

    output_dir.mkdir(parents=True, exist_ok=True)

    validation_path = output_dir / "validation_report.json"
    validation_path.write_text(
        json.dumps(validation, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if not validation["analysis_allowed"]:
        raise ValueError(
            "Analysis stopped because validation found critical errors. "
            f"See {validation_path}"
        )

    # 1. Sample profile: counts and percentages for single-choice items.
    profile_tables = []

    for column in ["role", "experience", "q11_development_need"]:
        counts = (
            data[column]
            .fillna("[Missing]")
            .value_counts(dropna=False)
            .rename_axis("response")
            .reset_index(name="count")
        )
        counts["percentage"] = (
            counts["count"] / len(data) * 100
        ).round(2)
        counts.insert(0, "variable", column)
        profile_tables.append(counts)

    profile = pd.concat(profile_tables, ignore_index=True)
    profile.to_csv(output_dir / "categorical_frequencies.csv", index=False)

    # 2. Familiarity ratings: descriptive statistics for Q3–Q9.
    familiarity = data[FAMILIARITY_COLUMNS].apply(
        pd.to_numeric, errors="coerce"
    )

    summary = familiarity.describe().T
    summary = summary.rename_axis("variable").reset_index()
    summary.to_csv(
        output_dir / "familiarity_descriptive_statistics.csv",
        index=False,
    )

    # 3. Role by familiarity: means and non-missing response counts.
    role_means = data[["role"]].join(familiarity).groupby(
        "role", dropna=False
    )[FAMILIARITY_COLUMNS].mean().round(2)

    role_means.to_csv(output_dir / "familiarity_means_by_role.csv")

    role_counts = data.groupby("role", dropna=False).size()
    role_counts.rename("respondent_count").to_csv(
        output_dir / "respondent_counts_by_role.csv"
    )

    # 4. Q10: count each selected activity separately.
    task_series = data["q10_tasks"].dropna().astype(str)
    task_responses = task_series.str.split(";").explode().str.strip()
    task_counts = (
        task_responses[task_responses.ne("")]
        .value_counts()
        .rename_axis("task")
        .reset_index(name="selection_count")
    )
    task_counts["percentage_of_respondents"] = (
        task_counts["selection_count"] / len(data) * 100
    ).round(2)
    task_counts.to_csv(
        output_dir / "q10_task_frequencies.csv", index=False
    )

    # 5. Q12: summarise missingness and available text responses.
    challenge = data["q12_challenge"]
    challenge_missing = int(challenge.isna().sum())
    challenge_available = int(challenge.notna().sum())

    challenge_summary = pd.DataFrame(
        [
            {
                "measure": "total_records",
                "count": len(data),
                "percentage_of_records": 100.0,
            },
            {
                "measure": "available_q12_responses",
                "count": challenge_available,
                "percentage_of_records": round(
                    challenge_available / len(data) * 100, 2
                ),
            },
            {
                "measure": "missing_q12_responses",
                "count": challenge_missing,
                "percentage_of_records": round(
                    challenge_missing / len(data) * 100, 2
                ),
            },
        ]
    )
    challenge_summary.to_csv(
        output_dir / "q12_response_completeness.csv", index=False
    )

    # 6. Chart: mean familiarity rating by skill area.
    means = familiarity.mean().sort_values()
    labels = [
        label.replace("q", "Q").replace("_", " ")
        for label in means.index
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels, means.values)
    ax.set_xlim(0, 5)
    ax.set_xlabel("Mean self-reported familiarity (1–5)")
    ax.set_title("Synthetic data: familiarity ratings by skill area")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(
        output_dir / "mean_familiarity_by_skill.png",
        dpi=160,
    )
    plt.close(fig)

    # 7. Chart: response counts by professional role.
    role_plot = (
        data["role"]
        .fillna("[Missing]")
        .value_counts()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(role_plot.index, role_plot.values)
    ax.set_xlabel("Number of synthetic records")
    ax.set_title("Synthetic data: records by professional role")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(
        output_dir / "respondents_by_role.png",
        dpi=160,
    )
    plt.close(fig)

    # Record provenance and processing details for reproducibility.
    manifest = {
        "input_file": input_csv.name,
        "dataset_type": "SYNTHETIC_NOT_REAL",
        "records_analysed": int(len(data)),
        "analysis_allowed_by_validator": True,
        "critical_validation_errors": 0,
        "validation_warnings": validation["warning_count"],
        "q12_missing_responses": challenge_missing,
        "outputs": [
            "validation_report.json",
            "categorical_frequencies.csv",
            "familiarity_descriptive_statistics.csv",
            "familiarity_means_by_role.csv",
            "respondent_counts_by_role.csv",
            "q10_task_frequencies.csv",
            "q12_response_completeness.csv",
            "mean_familiarity_by_skill.png",
            "respondents_by_role.png",
        ],
        "limitations": [
            "Data is simulated and is not evidence about real educators.",
            "Descriptive associations do not establish causation.",
            "Q12 is optional; missing responses are reported, not imputed.",
        ],
    }

    (output_dir / "analysis_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Validate and analyse Survey-to-Insight data."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent / "synthetic_responses.csv",
        help="Input survey CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "analysis_outputs",
        help="Directory for generated analysis outputs.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(
            f"Input CSV not found: {args.input}. "
            "Download the workflow artifact or generate the dataset first."
        )

    manifest = analyse_survey(args.input, args.output_dir)

    print("Descriptive analysis completed.")
    print("Dataset type: SYNTHETIC_NOT_REAL")
    print(f"Records analysed: {manifest['records_analysed']}")
    print(f"Outputs saved to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
