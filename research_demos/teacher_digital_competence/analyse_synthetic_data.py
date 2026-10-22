
"""
GEAA Education Research Demonstration
Topic: Teacher digital competence and class mean achievement.

IMPORTANT:
This dataset is synthetic demonstration data, not real research evidence.
Results must not be interpreted as findings about actual teachers or schools.
"""

from pathlib import Path
import math

import matplotlib
matplotlib.use("Agg")  # Suitable for automated, non-interactive runs.
import matplotlib.pyplot as plt
import pandas as pd


# ---------------------------------------------------------------------
# 1. FILE PATHS AND CONFIGURATION
# ---------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "geaa_synthetic_teacher_digital_competence.csv"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

COMPETENCE = "teacher_digital_competence_score"
ACHIEVEMENT = "current_class_mean_achievement_score"
BASELINE = "baseline_class_mean_score"
STATUS = "data_status"

EXPECTED_COLUMNS = [
    "school_id",
    "subcounty_label",
    "teacher_id",
    "teacher_years_experience",
    COMPETENCE,
    "digital_training_past_2_years",
    "school_resource_access_index",
    "internet_reliability_rating_1_5",
    "device_access_rating_1_5",
    "class_size",
    BASELINE,
    ACHIEVEMENT,
    STATUS,
]

NUMERIC_COLUMNS = [
    "teacher_years_experience",
    COMPETENCE,
    "digital_training_past_2_years",
    "school_resource_access_index",
    "internet_reliability_rating_1_5",
    "device_access_rating_1_5",
    "class_size",
    BASELINE,
    ACHIEVEMENT,
]


# ---------------------------------------------------------------------
# 2. DATA VALIDATION
# ---------------------------------------------------------------------

def validate_dataset(df):
    """Validate dataset structure, values, identifiers and provenance."""

    if df.empty:
        raise ValueError("The dataset is empty.")

    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]
    unexpected_columns = [
        column for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns or unexpected_columns:
        raise ValueError(
            "Schema check failed. "
            f"Missing columns: {missing_columns}; "
            f"unexpected columns: {unexpected_columns}"
        )

    if len(df) != 120:
        raise ValueError(
            f"Expected 120 synthetic records, but found {len(df)}."
        )

    if df.isna().any().any():
        missing_counts = df.isna().sum()
        details = missing_counts[missing_counts > 0].to_string()
        raise ValueError(
            "Missing values were found:\n" + details
        )

    if df.duplicated().any():
        raise ValueError(
            f"Found {df.duplicated().sum()} duplicate rows."
        )

    # Convert numeric variables and reject non-numeric or infinite values.
    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[column], errors="coerce")

        if converted.isna().any():
            raise ValueError(
                f"'{column}' contains non-numeric or missing values."
            )

        if not converted.map(math.isfinite).all():
            raise ValueError(
                f"'{column}' contains infinite values."
            )

        df[column] = converted

    # Validate score ranges and other coding rules.
    bounded_variables = {
        COMPETENCE: (0, 100),
        BASELINE: (0, 100),
        ACHIEVEMENT: (0, 100),
        "internet_reliability_rating_1_5": (1, 5),
        "device_access_rating_1_5": (1, 5),
    }

    for column, (minimum, maximum) in bounded_variables.items():
        if not df[column].between(minimum, maximum).all():
            raise ValueError(
                f"'{column}' must be between {minimum} and {maximum}."
            )

    if not df["digital_training_past_2_years"].isin([0, 1]).all():
        raise ValueError(
            "Digital training indicator must contain only 0 or 1."
        )

    if (df["teacher_years_experience"] < 0).any():
        raise ValueError("Teaching experience cannot be negative.")

    if (df["class_size"] <= 0).any():
        raise ValueError("Class size must be positive.")

    if (df["school_resource_access_index"] < 0).any():
        raise ValueError("Resource access index cannot be negative.")

    for column in ["school_id", "teacher_id", "subcounty_label", STATUS]:
        if df[column].astype(str).str.strip().eq("").any():
            raise ValueError(
                f"'{column}' contains blank identifiers or labels."
            )

    if df["teacher_id"].duplicated().any():
        raise ValueError("Teacher IDs must be unique.")

    if df["school_id"].nunique() != 20:
        raise ValueError("Expected exactly 20 synthetic schools.")

    records_per_school = df.groupby("school_id").size()

    if not records_per_school.eq(6).all():
        raise ValueError(
            "Each synthetic school must have exactly 6 records."
        )

    if not df[STATUS].eq("SYNTHETIC_NOT_REAL").all():
        raise ValueError(
            "Every record must be labelled SYNTHETIC_NOT_REAL."
        )

    return df


# ---------------------------------------------------------------------
# 3. REPORT AND OUTPUT HELPERS
# ---------------------------------------------------------------------

def save_report(df, descriptive_summary, correlation, valid_records):
    """Create a Markdown report from the current analysis results."""

    if correlation is None:
        correlation_text = (
            "Not calculated because fewer than two complete records "
            "were available."
        )
    else:
        correlation_text = (
            f"Pearson correlation (r) = {correlation:.3f}, "
            f"based on {valid_records} complete records."
        )

    report = f"""# GEAA Education Research Demonstration

## Research topic
Teacher digital competence and class mean achievement.

## 1. Purpose
This demonstration illustrates a reproducible education data-analysis
workflow, including validation, descriptive statistics, exploratory
correlation, visualisation and cautious interpretation.

## 2. Data provenance

**IMPORTANT: This is synthetic demonstration data, not empirical evidence.**

- Records analysed: {len(df)}
- Variables: {df.shape[1]}
- Synthetic schools: {df["school_id"].nunique()}
- Duplicate rows: {df.duplicated().sum()}
- Data status: SYNTHETIC_NOT_REAL

No actual teachers, learners or schools were sampled for this dataset.
Results must not be presented as findings about real schools.

## 3. Descriptive statistics

The following statistics describe only the generated synthetic dataset.

```text
{descriptive_summary}
```

## 4. Exploratory association

Variables compared:
- Teacher digital competence score
- Current class mean achievement score

{correlation_text}

This is an unadjusted exploratory Pearson correlation. It describes
linear association in the synthetic records. It does not establish
causation or represent an empirical relationship.

## 5. Methodological limitations

- The dataset is synthetic and cannot provide evidence about actual
  teachers, learners or schools.
- Any patterns reflect the data-generation process.
- Correlation does not establish causation.
- Records are grouped within schools, so observations may not be
  statistically independent.
- The correlation does not adjust for potential confounding variables
  or school-level clustering.
- These analyses do not establish intervention effectiveness or policy
  impact.

## 6. Requirements for a real study

A real investigation would require authentic data, appropriate ethical
review and permissions, valid measures, a justified sampling strategy,
and an analysis plan suited to the research question and clustered data.

## 7. Generated outputs

- `descriptive_statistics.csv`
- `exploratory_correlation.csv`
- `teacher_competence_vs_achievement.png`
- `baseline_current_score_distributions.png`
- `teacher_digital_competence_distribution.png`
- `synthetic_research_report.md`

## 8. Reproducibility

This report is generated by `analyse_synthetic_data.py` from the
synthetic CSV dataset. Numerical results are calculated when the script
runs and are not manually entered research findings.

## 9. Conclusion

This demonstration shows a basic, reproducible education data-analysis
workflow. It does not establish whether teacher digital competence
predicts or causes improved learner achievement in real educational
settings.
"""

    report_file = OUTPUT_DIR / "synthetic_research_report.md"
    report_file.write_text(report, encoding="utf-8")
    return report_file


# ---------------------------------------------------------------------
# 4. MAIN ANALYSIS
# ---------------------------------------------------------------------

def main():
    print("=" * 70)
    print("GEAA: SYNTHETIC EDUCATION RESEARCH DEMONSTRATION")
    print("Teacher digital competence and class mean achievement")
    print("=" * 70)
    print("WARNING: All records are synthetic, not real research data.")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Keep the CSV in the same folder as this Python script."
        )

    df = pd.read_csv(DATA_FILE)
    df = validate_dataset(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Dataset overview and consolidated quality report.
    print("\n1. DATASET OVERVIEW")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Schools: {df['school_id'].nunique()}")
    print(f"Unique teacher IDs: {df['teacher_id'].nunique()}")

    print("\n2. DATA QUALITY")
    print("Schema and column names: passed")
    print("Missing values: none")
    print("Duplicate rows: none")
    print("Numeric and finite-value checks: passed")
    print("Specified ranges and coding rules: passed")
    print("Teacher IDs: unique")
    print("School structure: 20 schools, 6 records per school")
    print("Synthetic provenance labels: passed")

    # Descriptive statistics.
    numeric_columns = [COMPETENCE, ACHIEVEMENT, BASELINE]
    descriptive = df[numeric_columns].describe().round(2)

    print("\n3. DESCRIPTIVE STATISTICS")
    print(descriptive.to_string())

    descriptive.to_csv(OUTPUT_DIR / "descriptive_statistics.csv")

    # Exploratory Pearson correlation.
    valid = df[[COMPETENCE, ACHIEVEMENT]].dropna()
    correlation = None

    print("\n4. EXPLORATORY ASSOCIATION")

    if len(valid) >= 2:
        correlation = valid[COMPETENCE].corr(valid[ACHIEVEMENT])
        print(f"Pearson correlation (r): {correlation:.3f}")
        print(f"Complete records included: {len(valid)}")

        correlation_output = pd.DataFrame({
            "measure": ["Pearson correlation"],
            "variable_1": [COMPETENCE],
            "variable_2": [ACHIEVEMENT],
            "correlation": [correlation],
            "complete_records": [len(valid)],
            "data_status": ["SYNTHETIC_NOT_REAL"],
        })

        correlation_output.to_csv(
            OUTPUT_DIR / "exploratory_correlation.csv",
            index=False,
        )
    else:
        print("Insufficient complete records for correlation.")
        pd.DataFrame(columns=[
            "measure", "variable_1", "variable_2",
            "correlation", "complete_records", "data_status",
        ]).to_csv(
            OUTPUT_DIR / "exploratory_correlation.csv",
            index=False,
        )

    print("\n5. SCHOOL-LEVEL RECORD COUNTS")
    print(df.groupby("school_id").size().describe().round(2).to_string())

    # Figure 1: Competence versus achievement.
    plt.figure(figsize=(8, 5))
    plt.scatter(df[COMPETENCE], df[ACHIEVEMENT], alpha=0.75)
    plt.xlabel("Teacher digital competence score")
    plt.ylabel("Current class mean achievement score")
    plt.title(
        "SYNTHETIC DATA — NOT REAL SCHOOL EVIDENCE\n"
        "Digital Competence and Class Mean Achievement"
    )
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "teacher_competence_vs_achievement.png",
        dpi=150,
    )
    plt.close()

    # Figure 2: Baseline and current score distributions.
    plt.figure(figsize=(8, 5))
    plt.hist(
        df[BASELINE],
        bins=12,
        alpha=0.6,
        label="Baseline class mean score",
    )
    plt.hist(
        df[ACHIEVEMENT],
        bins=12,
        alpha=0.6,
        label="Current class mean achievement score",
    )
    plt.xlabel("Class mean score")
    plt.ylabel("Number of records")
    plt.title(
        "SYNTHETIC DATA — NOT REAL SCHOOL EVIDENCE\n"
        "Baseline and Current Score Distributions"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "baseline_current_score_distributions.png",
        dpi=150,
    )
    plt.close()

    # Figure 3: Distribution of competence scores.
    plt.figure(figsize=(8, 5))
    plt.hist(df[COMPETENCE], bins=12, edgecolor="black")
    plt.xlabel("Teacher digital competence score")
    plt.ylabel("Number of records")
    plt.title(
        "SYNTHETIC DATA — NOT REAL SCHOOL EVIDENCE\n"
        "Distribution of Teacher Digital Competence Scores"
    )
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "teacher_digital_competence_distribution.png",
        dpi=150,
    )
    plt.close()

    descriptive_summary = descriptive.to_string()

    report_file = save_report(
        df,
        descriptive_summary,
        correlation,
        len(valid),
    )

    print("\n6. OUTPUTS")
    for filename in [
        "descriptive_statistics.csv",
        "exploratory_correlation.csv",
        "teacher_competence_vs_achievement.png",
        "baseline_current_score_distributions.png",
        "teacher_digital_competence_distribution.png",
        report_file.name,
    ]:
        print(f"Created: {OUTPUT_DIR / filename}")

    print("\nINTERPRETATION AND LIMITATIONS")
    print("- All records are synthetic, not observations from real schools.")
    print("- Descriptive statistics summarise the generated dataset only.")
    print("- Pearson correlation is exploratory and unadjusted.")
    print("- Correlation does not establish causation.")
    print("- Records are clustered within schools.")
    print("- No causal, intervention-effectiveness or policy-impact claims "
          "can be made from this demonstration.")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        raise SystemExit(f"ANALYSIS FAILED: {error}") from error
