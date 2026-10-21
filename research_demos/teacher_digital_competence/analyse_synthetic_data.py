
"""
GEAA Education Research Demonstration
Topic: Teacher digital competence and class mean achievement.

IMPORTANT:
This dataset is synthetic demonstration data, not real research evidence.
Do not interpret its results as findings about actual teachers or schools.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


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

    EXPECTED_COLUMNS = [
        "school_id",
        "subcounty_label",
        "teacher_id",
        "teacher_years_experience",
        "teacher_digital_competence_score",
        "digital_training_past_2_years",
        "school_resource_access_index",
        "internet_reliability_rating_1_5",
        "device_access_rating_1_5",
        "class_size",
        "baseline_class_mean_score",
        "current_class_mean_achievement_score",
        "data_status",
    ]

    NUMERIC_COLUMNS = [
        "teacher_years_experience",
        "teacher_digital_competence_score",
        "digital_training_past_2_years",
        "school_resource_access_index",
        "internet_reliability_rating_1_5",
        "device_access_rating_1_5",
        "class_size",
        "baseline_class_mean_score",
        "current_class_mean_achievement_score",
    ]

    print("\n1. DATASET OVERVIEW")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print("\nColumn names:")
    print(df.columns.tolist())

    # Check the expected dataset structure.
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
            f"Schema check failed. Missing columns: {missing_columns}; "
            f"unexpected columns: {unexpected_columns}"
        )

    if df.empty:
        raise ValueError("Data quality check failed: the dataset is empty.")

    if len(df) != 120:
        raise ValueError(
            f"Expected 120 synthetic records, but found {len(df)}."
        )

    # Check for missing values before analysis.
    if df.isna().any().any():
        missing_counts = df.isna().sum()
        raise ValueError(
            "Data quality check failed: missing values found.\n"
            + missing_counts[missing_counts > 0].to_string()
        )

    # Confirm that required numerical variables contain valid numbers.
    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[column], errors="coerce")

        if converted.isna().any():
            raise ValueError(
                f"Data quality check failed: "
                f"'{column}' contains non-numeric values."
            )

        df[column] = converted

    # Check variable ranges and coding rules.
    if not df[COMPETENCE].between(0, 100).all():
        raise ValueError(
            "Data quality check failed: digital competence "
            "scores must be between 0 and 100."
        )

    for column in [
        "internet_reliability_rating_1_5",
        "device_access_rating_1_5",
    ]:
        if not df[column].between(1, 5).all():
            raise ValueError(
                f"Data quality check failed: '{column}' "
                "must be between 1 and 5."
            )

    if not df["digital_training_past_2_years"].isin([0, 1]).all():
        raise ValueError(
            "Data quality check failed: digital training "
            "indicator must contain only 0 or 1."
        )

    if (df["teacher_years_experience"] < 0).any():
        raise ValueError(
            "Data quality check failed: teaching experience "
            "cannot be negative."
        )

    if (df["class_size"] <= 0).any():
        raise ValueError(
            "Data quality check failed: class size must be positive."
        )

    if (df["school_resource_access_index"] < 0).any():
        raise ValueError(
            "Data quality check failed: resource access index "
            "cannot be negative."
        )

    if not df["baseline_class_mean_score"].between(0, 100).all():
        raise ValueError(
            "Data quality check failed: baseline class mean scores "
            "must be between 0 and 100."
        )

    if not df[ACHIEVEMENT].between(0, 100).all():
        raise ValueError(
            "Data quality check failed: current class mean achievement "
            "scores must be between 0 and 100."
        )

    # Check identifiers and expected school structure.
    if df["teacher_id"].duplicated().any():
        raise ValueError(
            "Data quality check failed: duplicate teacher IDs found."
        )

    if df["school_id"].isna().any() or df["teacher_id"].isna().any():
        raise ValueError(
            "Data quality check failed: missing school or teacher IDs."
        )

    if df["school_id"].nunique() != 20:
        raise ValueError(
            "Data quality check failed: expected 20 synthetic schools."
        )

    records_per_school = df.groupby("school_id").size()

    if not records_per_school.eq(6).all():
        raise ValueError(
            "Data quality check failed: each synthetic school "
            "must have exactly 6 records."
        )

    # Protect the provenance of the demonstration dataset.
    if not df[STATUS].eq("SYNTHETIC_NOT_REAL").all():
        raise ValueError(
            "Data integrity check failed: every row must be labelled "
            "SYNTHETIC_NOT_REAL."
        )


    print("\n2. DATA QUALITY")
    print("Missing values: none")
    print("All expected columns are present; no unexpected columns.")
    print("Numeric variables and specified ranges: passed")
    print("Teacher IDs are unique: passed")
    print("School structure: 20 schools, 6 records per school")
    print("All rows correctly labelled synthetic: passed")
    print("Data-quality checks passed.")


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

    # All figures use synthetic data and must not be interpreted as real findings.
    
    # 1. Teacher digital competence versus current class mean achievement
    plt.figure(figsize=(8, 5))
    plt.scatter(
        df["teacher_digital_competence_score"],
        df["current_class_mean_achievement_score"],
        alpha=0.75
    )
    plt.xlabel("Teacher digital competence score")
    plt.ylabel("Current class mean achievement score")
    plt.title(
        "SYNTHETIC DATA — NOT REAL SCHOOL EVIDENCE\n"
        "Digital Competence and Class Mean Achievement"
    )
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "teacher_competence_vs_achievement.png",
        dpi=150
    )
    plt.close()
    
    # 2. Compare the distributions of baseline and current class mean scores
    plt.figure(figsize=(8, 5))
    plt.hist(
        df["baseline_class_mean_score"],
        bins=12,
        alpha=0.6,
        label="Baseline class mean score"
    )
    plt.hist(
        df["current_class_mean_achievement_score"],
        bins=12,
        alpha=0.6,
        label="Current class mean achievement score"
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
        dpi=150
    )
    plt.close()
    
    # 3. Distribution of teacher digital competence scores
    plt.figure(figsize=(8, 5))
    plt.hist(
        df["teacher_digital_competence_score"],
        bins=12,
        edgecolor="black"
    )
    plt.xlabel("Teacher digital competence score")
    plt.ylabel("Number of records")
    plt.title(
        "SYNTHETIC DATA — NOT REAL SCHOOL EVIDENCE\n"
        "Distribution of Teacher Digital Competence Scores"
    )
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "teacher_digital_competence_distribution.png",
        dpi=150
    )
    plt.close()
    
    print("\nSynthetic visualisations saved to:", OUTPUT_DIR)
    print("- teacher_competence_vs_achievement.png")
    print("- baseline_current_score_distributions.png")
    print("- teacher_digital_competence_distribution.png")

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
    print("-" * 60)
    print("1. DATA PROVENANCE")
    print(
        "   All records are synthetic and were created for "
        "demonstration purposes."
    )
    print(
        "   They are not observations from actual teachers, "
        "learners, or schools."
    )

    print("\n2. INTERPRETING THE RESULTS")
    print(
        "   Descriptive statistics summarise the generated "
        "dataset only."
    )
    print(
        "   The Pearson correlation describes a linear association "
        "within these synthetic records."
    )
    print(
        "   Any observed association reflects the data-generation "
        "process and must not be presented as an empirical finding."
    )

    print("\n3. METHODOLOGICAL LIMITATIONS")
    print(
        "   Correlation does not establish causation."
    )
    print(
        "   Records are grouped within schools, so observations "
        "may not be statistically independent."
    )
    print(
        "   The unadjusted correlation does not control for "
        "potential confounding variables or school-level clustering."
    )

    print("\n4. IMPLICATIONS FOR REAL EDUCATION RESEARCH")
    print(
        "   A real study would require authentic data, ethical "
        "approval where applicable, valid measures, and a justified "
        "sampling and analysis strategy."
    )
    print(
        "   Statistical results should be interpreted in light of "
        "the research design and data limitations."
    )

    print("\n" + "-" * 60)
    print("END OF SYNTHETIC RESEARCH DEMONSTRATION")



if __name__ == "__main__":
    main()

