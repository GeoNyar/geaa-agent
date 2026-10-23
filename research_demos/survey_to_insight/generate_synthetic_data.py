
"""Generate clearly labelled synthetic survey data for demonstration.

This dataset is simulated and must not be presented as empirical
evidence about actual teachers, lecturers, researchers, or institutions.
"""

import argparse
from pathlib import Path

import pandas as pd


SEED = 20261023
DEFAULT_RESPONDENTS = 100

ROLES = [
    "Teacher or lecturer",
    "School or institutional leader",
    "Education programme or project staff",
    "Research or monitoring and evaluation staff",
    "Student or trainee",
    "Other",
    "Prefer not to say",
]

EXPERIENCE = [
    "Less than 1 year",
    "1–3 years",
    "4–6 years",
    "7–10 years",
    "More than 10 years",
    "Not applicable",
]


DEVELOPMENT_NEEDS = [
    "Questionnaire design",
    "Data cleaning and quality assurance",
    "Excel and spreadsheet analysis",
    "Descriptive statistics",
    "Cross-tabulations and interpretation",
    "Data visualisation and dashboards",
    "Report and presentation writing",
    "Other",
    "Prefer not to say",
]


TASK_OPTIONS = [
    "Designed a questionnaire",
    "Collected survey data",
    "Cleaned or validated a dataset",
    "Analysed quantitative data",
    "Produced charts or visualisations",
    "Prepared a research or evaluation report",
    "Used an interactive dashboard",
    "None of the above",
    "Prefer not to say",
]

FAMILIARITY_COLUMNS = [
    "q3_questionnaire_design",
    "q4_data_validation",
    "q5_excel",
    "q6_descriptive_statistics",
    "q7_crosstabs",
    "q8_visualisation",
    "q9_reporting",
]

CHALLENGES = [
    "Difficulty interpreting statistical results",
    "Limited practice with data visualisation",
    "Need more experience cleaning survey data",
    "Difficulty presenting findings to decision-makers",
    "No major challenge reported",
]


def generate_data(
    n: int = DEFAULT_RESPONDENTS,
    seed: int = SEED,
) -> pd.DataFrame:
    """Generate reproducible synthetic questionnaire responses."""
    if n < 1:
        raise ValueError("The number of respondents must be at least 1.")

    rng = __import__("numpy").random.default_rng(seed)

    roles = rng.choice(ROLES, size=n)
    experience = rng.choice(EXPERIENCE, size=n)

    records = []

    for i in range(n):
        record = {
            "respondent_id": f"SYN{i + 1:04d}",
            "role": roles[i],
            "experience": experience[i],
        }

        # Simulate familiarity ratings on the questionnaire's 1–5 scale.
        for column in FAMILIARITY_COLUMNS:
            record[column] = int(rng.integers(1, 6))

        # Simulate one or more past-year activities.
        selected_count = int(rng.integers(1, 4))
        selected_tasks = list(
            rng.choice(
                TASK_OPTIONS[:7],
                size=selected_count,
                replace=False,
            )
        )
        record["q10_tasks"] = ";".join(selected_tasks)

        record["q11_development_need"] = str(
            rng.choice(DEVELOPMENT_NEEDS)
        )

        # Optional free-text response; some respondents leave it blank.
        record["q12_challenge"] = (
            str(rng.choice(CHALLENGES))
            if rng.random() >= 0.20
            else None
        )

        records.append(record)

    columns = [
        "respondent_id",
        "role",
        "experience",
        *FAMILIARITY_COLUMNS,
        "q10_tasks",
        "q11_development_need",
        "q12_challenge",
    ]

    return pd.DataFrame(records, columns=columns)


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic Survey-to-Insight data."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=DEFAULT_RESPONDENTS,
        help="Number of synthetic respondents (default: 100).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=SEED,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "synthetic_responses.csv",
        help="Output CSV path.",
    )
    args = parser.parse_args()

    data = generate_data(n=args.n, seed=args.seed)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.output, index=False)

    print("Synthetic dataset generated successfully.")
    print("IMPORTANT: These are simulated responses, not empirical data.")
    print(f"Respondent records: {len(data)}")
    print(f"Output file: {args.output}")
    print(f"Random seed: {args.seed}")


if __name__ == "__main__":
    main()
