
"""
GEAA Education Research Demonstration
Topic: Teacher digital competence and class mean achievement.

IMPORTANT:
This dataset is synthetic demonstration data, not real research evidence.
Do not interpret its results as findings about actual teachers or schools.
"""

from pathlib import Path

import pandas as pd


# Locate the CSV relative to this script, so the script can be run
# from different working directories.
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "geaa_synthetic_teacher_digital_competence.csv"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

COMPETENCE = "teacher_digital_competence_score"
ACHIEVEMENT = "current_class_mean_achievement_score"
BASELINE = "baseline_class_mean_score"
STATUS = "data_status"


def main():
    print("=" * 70)
    print("GEAA: SYNTHETIC EDUCATION RESEARCH DEMONSTRATION")
    print("Teacher digital competence and class mean achievement")
    print("=" * 70)
    print("\nWARNING: All records are synthetic, not real research data.")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Keep the CSV in the same folder as this Python script."
        )

    df = pd.read_csv(DATA_FILE)

    print("\n1. DATASET OVERVIEW")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print("\nColumn names:")
    print(df.columns.tolist())

    required_columns = [
        COMPETENCE,
        ACHIEVEMENT,
        BASELINE,
        STATUS,
        "school_id",
    ]
    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Required columns missing: {missing_columns}")

    if not df[STATUS].eq("SYNTHETIC_NOT_REAL").all():
        raise ValueError(
            "Data integrity check failed: every row must be labelled "
            "SYNTHETIC_NOT_REAL."
        )

    print("\n2. DATA QUALITY")
    print("Missing values by column:")
    print(df.isna().sum().to_string())
    print(
        "\nAll rows correctly labelled synthetic:",
        df[STATUS].eq("SYNTHETIC_NOT_REAL").all(),
    )
    print("Unique school IDs:", df["school_id"].nunique())

    numeric_columns = [
        column
        for column in [COMPETENCE, ACHIEVEMENT, BASELINE]
        if pd.api.types.is_numeric_dtype(df[column])
    ]

    print("\n3. DESCRIPTIVE STATISTICS")
    print(df[numeric_columns].describe().round(2).to_string())

    print("\n4. EXPLORATORY ASSOCIATION")
    valid = df[[COMPETENCE, ACHIEVEMENT]].dropna()

    if len(valid) >= 2:
        correlation = valid[COMPETENCE].corr(valid[ACHIEVEMENT])
        print(f"Pearson correlation (r): {correlation:.3f}")
        print(f"Records included: {len(valid)}")
    else:
        print("Insufficient complete records to calculate correlation.")

    print("\n5. SCHOOL-LEVEL RECORD COUNTS")
    print(df.groupby("school_id").size().describe().round(2).to_string())

    OUTPUT_DIR.mkdir(exist_ok=True)

    df[numeric_columns].describe().round(2).to_csv(
        OUTPUT_DIR / "descriptive_statistics.csv"
    )

    if len(valid) >= 2:
        pd.DataFrame(
            {
                "measure": ["Pearson correlation"],
                "variable_1": [COMPETENCE],
                "variable_2": [ACHIEVEMENT],
                "correlation": [correlation],
                "complete_records": [len(valid)],
                "data_status": ["SYNTHETIC_NOT_REAL"],
            }
        ).to_csv(OUTPUT_DIR / "exploratory_correlation.csv", index=False)

    print(f"\nSummary files saved in: {OUTPUT_DIR}")
    print("\nINTERPRETATION AND LIMITATIONS")
    print("- These are synthetic data, not observations from real schools.")
    print("- Any association is a property of the data-generation process.")
    print("- Correlation does not establish causation.")
    print("- Records are grouped within schools; independence cannot be assumed.")
    print("- Do not present these results as empirical research findings.")


if __name__ == "__main__":
    main()

