
"""
GEAA Education Research Demonstration
Topic: Teacher digital competence and class mean achievement.

IMPORTANT:
This is synthetic demonstration data, not real research evidence.
Do not interpret results as findings about actual teachers or schools.
"""

from pathlib import Path
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


# ---------------------------------------------------------------------
# 1. CONFIGURATION
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
    """Validate the structure, values and provenance of the dataset."""

    if df.empty:
        raise ValueError("The dataset is empty.")

    missing_columns = [
        col for col in EXPECTED_COLUMNS if col not in df.columns
    ]
    unexpected_columns = [
        col for col in df.columns if col not in EXPECTED_COLUMNS
    ]

    if missing_columns or unexpected_columns:
        raise ValueError(
            f"Schema check failed. Missing: {missing_columns}; "
            f"unexpected: {unexpected_columns}"
        )

    if len(df) != 120:
        raise ValueError(
            f"Expected 120 synthetic records; found {len(df)}."
        )

    if df.isna().any().any():
        counts = df.isna().sum()
        raise ValueError(
            "Missing values found:\n"
            + counts[counts > 0].to_string()
        )

    if df.duplicated().any():
        raise ValueError(
            f"Found {df.duplicated().sum()} duplicate rows."
        )

    for col in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[col], errors="coerce")

        if converted.isna().any():
            raise ValueError(
                f"'{col}' contains non-numeric or missing values."
            )

        if not converted.map(math.isfinite).all():
            raise ValueError(f"'{col}' contains infinite values.")

        df[col] = converted

    bounded_variables = {
        COMPETENCE: (0, 100),
        BASELINE: (0, 100),
        ACHIEVEMENT: (0, 100),
        "internet_reliability_rating_1_5": (1, 5),
        "device_access_rating_1_5": (1, 5),
    }

    for col, (lower, upper) in bounded_variables.items():
        if not df[col].between(lower, upper).all():
            raise ValueError(
                f"'{col}' must be between {lower} and {upper}."
            )

    if not df["digital_training_past_2_years"].isin([0, 1]).all():
        raise ValueError("Digital training must be coded as 0 or 1.")

    integer_columns = [
        "teacher_years_experience",
        "digital_training_past_2_years",
        "class_size",
    ]

    for col in integer_columns:
        if not df[col].mod(1).eq(0).all():
            raise ValueError(
                f"'{col}' must contain whole-number values."
            )

    if (df["teacher_years_experience"] < 0).any():
        raise ValueError("Teaching experience cannot be negative.")

    if (df["class_size"] <= 0).any():
        raise ValueError("Class size must be positive.")

    if (df["school_resource_access_index"] < 0).any():
        raise ValueError("Resource access index cannot be negative.")

    for col in ["school_id", "teacher_id", "subcounty_label", STATUS]:
        if df[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"'{col}' contains blank values.")

    if df["teacher_id"].duplicated().any():
        raise ValueError("Teacher IDs must be unique.")

    if df["school_id"].nunique() != 20:
        raise ValueError("Expected exactly 20 synthetic schools.")

    counts = df.groupby("school_id").size()
    if not counts.eq(6).all():
        raise ValueError("Each synthetic school must have 6 records.")

    school_level_columns = [
        "subcounty_label",
        "school_resource_access_index",
        "internet_reliability_rating_1_5",
        "device_access_rating_1_5",
    ]

    for col in school_level_columns:
        values_per_school = df.groupby("school_id")[col].nunique()
        if not values_per_school.eq(1).all():
            raise ValueError(
                f"'{col}' must have one consistent value per school."
            )

    if not df[STATUS].eq("SYNTHETIC_NOT_REAL").all():
        raise ValueError(
            "Every record must be labelled SYNTHETIC_NOT_REAL."
        )

    return df

# ---------------------------------------------------------------------
# 3. SCHOOL-LEVEL ANALYSIS
# ---------------------------------------------------------------------

def calculate_school_summaries(df):
    """Summarise selected variables for each fictional school."""

    summary = (
        df.groupby("school_id")
        .agg(
            records=("teacher_id", "count"),
            mean_teacher_digital_competence=(COMPETENCE, "mean"),
            mean_current_achievement=(ACHIEVEMENT, "mean"),
            mean_baseline_achievement=(BASELINE, "mean"),
            mean_school_resource_access=(
                "school_resource_access_index", "mean"
            ),
            mean_class_size=("class_size", "mean"),
        )
        .reset_index()
    )

    summary["data_status"] = "SYNTHETIC_NOT_REAL"

    return summary.round(3)


def calculate_one_way_icc(df, outcome):
    """
    Estimate a one-way random-effects ICC for a balanced design.

    The estimate describes the proportion of outcome variance
    associated with between-school differences under a simple
    random-intercept framework. It does not establish causation.
    """

    grouped = df.groupby("school_id")[outcome]
    school_means = grouped.mean()
    school_sizes = grouped.size()

    number_schools = len(school_means)
    total_records = len(df)

    if number_schools < 2 or total_records <= number_schools:
        return None

    if not school_sizes.eq(school_sizes.iloc[0]).all():
        return None

    group_size = int(school_sizes.iloc[0])
    grand_mean = df[outcome].mean()

    between_ss = sum(
        len(group) * (group.mean() - grand_mean) ** 2
        for _, group in grouped
    )

    within_ss = sum(
        ((group - group.mean()) ** 2).sum()
        for _, group in grouped
    )

    df_between = number_schools - 1
    df_within = total_records - number_schools

    if df_between <= 0 or df_within <= 0:
        return None

    ms_between = between_ss / df_between
    ms_within = within_ss / df_within

    # One-way balanced random-effects variance components.
    variance_between = (ms_between - ms_within) / group_size
    variance_within = ms_within

    total_variance = variance_between + variance_within

    if total_variance <= 0:
        return None

    icc = variance_between / total_variance

    # Negative estimates can arise from sampling variation.
    # Retain the raw estimate for transparency.
    return {
        "schools": number_schools,
        "records": total_records,
        "records_per_school": group_size,
        "between_school_variance_estimate": variance_between,
        "within_school_variance_estimate": variance_within,
        "icc_raw": icc,
        "icc_interpretation": (
            "Raw one-way random-effects ICC estimate; exploratory only."
        ),
        "data_status": "SYNTHETIC_NOT_REAL",
    }


# ---------------------------------------------------------------------
# 4. REPORT GENERATION
# ---------------------------------------------------------------------

def save_report(
    df,
    descriptive,
    correlation,
    school_summary,
    icc_result,
):
    """Write a reproducible Markdown report."""

    if correlation is None:
        correlation_text = "Not calculated: insufficient complete records."
    else:
        correlation_text = (
            f"Pearson correlation (r) = {correlation:.3f}, "
            f"based on {len(df[[COMPETENCE, ACHIEVEMENT]].dropna())} "
            "complete records."
        )

    if icc_result is None:
        icc_text = (
            "The ICC was not calculated because the data did not meet "
            "the requirements of the implemented balanced-design method."
        )
    else:
        icc_text = (
            f"- Schools: {icc_result['schools']}\n"
            f"- Records: {icc_result['records']}\n"
            f"- Records per school: {icc_result['records_per_school']}\n"
            f"- Between-school variance estimate: "
            f"{icc_result['between_school_variance_estimate']:.4f}\n"
            f"- Within-school variance estimate: "
            f"{icc_result['within_school_variance_estimate']:.4f}\n"
            f"- Raw ICC estimate: {icc_result['icc_raw']:.4f}\n"
        )

    report = f"""# GEAA Education Research Demonstration

## Research topic
Teacher digital competence and class mean achievement.

## 1. Data provenance

**This is synthetic demonstration data, not empirical evidence.**

- Records: {len(df)}
- Variables: {df.shape[1]}
- Fictional schools: {df["school_id"].nunique()}
- Data status: SYNTHETIC_NOT_REAL

No actual teachers, learners or schools were sampled. Results must not
be presented as findings about real schools.

## 2. Descriptive statistics

{descriptive.to_string()}

These statistics describe only the synthetic dataset.

## 3. Exploratory association

Variables:
- Teacher digital competence score
- Current class mean achievement score

{correlation_text}

This is an unadjusted exploratory Pearson correlation. It does not
establish causation or represent an empirical relationship.

## 4. School-level summaries

The school-level CSV reports the mean competence, current achievement,
baseline achievement, resource access and class size for each fictional
school. The school-level figure visualises the distribution of school
mean current achievement scores.

## 5. School-level variation and ICC

{icc_text}

The ICC is an exploratory one-way random-effects estimate for the
balanced synthetic dataset. It summarises the estimated between-school
variation relative to the total estimated variance under the specified
model. It does not identify the causes of school-level differences.

The estimate depends on the data-generating process and the
random-effects assumptions. A negative raw ICC can arise when the
estimated between-school variance component is negative. Such an
estimate should be reported transparently and interpreted as an
estimation result, not as a literal negative proportion of variance.
In applied research, the ICC interpretation should be checked against
the model, design and uncertainty in the estimate. This synthetic
analysis is not evidence about real schools.

## 6. Methodological limitations

- The data are synthetic and do not represent actual schools.
- Any patterns reflect the data-generation process.
- Correlation does not establish causation.
- Records are grouped within schools and may not be independent.
- The simple ICC does not adjust for confounding variables.
- The school-level summaries are descriptive, not causal analyses.
- The results do not establish intervention effectiveness or policy
  impact.

## 7. Requirements for real research

A real study would require authentic data, appropriate ethical review
and permissions, valid measures, a justified sampling strategy, and an
analysis plan suited to the research design and clustered observations.

## 8. Reproducibility

The script generates the CSV summaries, PNG figures and this report
from the synthetic dataset. Results are calculated when the script runs.

## 9. Conclusion

This demonstration illustrates reproducible education data analysis
and basic school-level variance estimation. It does not establish
whether teacher digital competence predicts or causes improved
achievement in real educational settings.
"""

    report_path = OUTPUT_DIR / "synthetic_research_report.md"
    report_path.write_text(report, encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------
# 5. MAIN WORKFLOW
# ---------------------------------------------------------------------

def main():
    print("=" * 70)
    print("GEAA: SYNTHETIC EDUCATION RESEARCH DEMONSTRATION")
    print("=" * 70)
    print("WARNING: All records are synthetic.")

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = validate_dataset(pd.read_csv(DATA_FILE))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n1. DATASET AND QUALITY CHECKS")
    print(f"Records: {len(df)}")
    print(f"Variables: {df.shape[1]}")
    print(f"Schools: {df['school_id'].nunique()}")
    print("Missing values: none")
    print("Duplicate rows: none")
    print("Numeric, range and provenance checks: passed")
    print("Six records per school: passed")

    # Descriptive statistics.
    descriptive_columns = [COMPETENCE, ACHIEVEMENT, BASELINE]
    descriptive = df[descriptive_columns].describe().round(2)

    print("\n2. DESCRIPTIVE STATISTICS")
    print(descriptive.to_string())

    descriptive.to_csv(OUTPUT_DIR / "descriptive_statistics.csv")

    # Descriptive baseline-to-current score comparison.
    # These are synthetic record-level differences, not evidence
    # of real longitudinal change or intervention effectiveness.
    score_difference = df[ACHIEVEMENT] - df[BASELINE]

    increase_count = int((score_difference > 0).sum())
    decrease_count = int((score_difference < 0).sum())
    unchanged_count = int((score_difference == 0).sum())
    total_comparisons = len(score_difference)

    change_summary = pd.DataFrame({
        "measure": [
            "Mean baseline score",
            "Mean current score",
            "Mean difference (current minus baseline)",
            "Records with increase",
            "Records with decrease",
            "Records with no difference",
        ],
        "value": [
            df[BASELINE].mean(),
            df[ACHIEVEMENT].mean(),
            score_difference.mean(),
            increase_count,
            decrease_count,
            unchanged_count,
        ],
        "data_status": ["SYNTHETIC_NOT_REAL"] * 6,
    })

    change_summary.to_csv(
        OUTPUT_DIR / "baseline_current_comparison.csv",
        index=False,
    )

    print("\n2A. SYNTHETIC BASELINE-TO-CURRENT COMPARISON")
    print(f"Mean baseline score: {df[BASELINE].mean():.2f}")
    print(f"Mean current score: {df[ACHIEVEMENT].mean():.2f}")
    print(f"Mean difference: {score_difference.mean():.2f}")
    print(
        f"Records with increase: {increase_count} "
        f"({increase_count / total_comparisons * 100:.1f}%)"
    )
    print(
        f"Records with decrease: {decrease_count} "
        f"({decrease_count / total_comparisons * 100:.1f}%)"
    )
    print(
        f"Records with no difference: {unchanged_count} "
        f"({unchanged_count / total_comparisons * 100:.1f}%)"
    )

    # Overall exploratory correlation.
    valid = df[[COMPETENCE, ACHIEVEMENT]].dropna()
    correlation = None

    if len(valid) >= 2:
        correlation = valid[COMPETENCE].corr(valid[ACHIEVEMENT])

        correlation_output = pd.DataFrame({
            "measure": ["Pearson correlation"],
            "variable_1": [COMPETENCE],
            "variable_2": [ACHIEVEMENT],
            "correlation": [correlation],
            "complete_records": [len(valid)],
            "data_status": ["SYNTHETIC_NOT_REAL"],
        })
    else:
        correlation_output = pd.DataFrame(columns=[
            "measure", "variable_1", "variable_2",
            "correlation", "complete_records", "data_status",
        ])

    correlation_output.to_csv(
        OUTPUT_DIR / "exploratory_correlation.csv",
        index=False,
    )

    print("\n3. EXPLORATORY ASSOCIATION")
    if correlation is None:
        print("Insufficient complete records for correlation.")
    else:
        print(f"Pearson correlation (r): {correlation:.3f}")
        print(f"Complete records: {len(valid)}")

    # School-level summary.
    school_summary = calculate_school_summaries(df)
    school_summary.to_csv(
        OUTPUT_DIR / "school_level_summary.csv",
        index=False,
    )

    print("\n4. SCHOOL-LEVEL SUMMARY")
    print(f"Schools summarised: {len(school_summary)}")
    print(
        "Mean school achievement range: "
        f"{school_summary['mean_current_achievement'].min():.2f} to "
        f"{school_summary['mean_current_achievement'].max():.2f}"
    )

    # School-level achievement figure.
    plotted = school_summary.sort_values("mean_current_achievement")

    plt.figure(figsize=(10, 6))
    plt.bar(
        plotted["school_id"].astype(str),
        plotted["mean_current_achievement"],
    )
    plt.xlabel("Fictional school ID")
    plt.ylabel("Mean current class achievement score")
    plt.title(
        "SYNTHETIC DATA — NOT REAL SCHOOL EVIDENCE\n"
        "Mean Achievement by Fictional School"
    )
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "school_level_achievement_means.png",
        dpi=150,
    )
    plt.close()

    # ICC analysis.
    icc_result = calculate_one_way_icc(df, ACHIEVEMENT)

    print("\n5. SCHOOL-LEVEL VARIATION")
    if icc_result is None:
        print("ICC not calculated; design requirements were not met.")
    else:
        print(
            "Between-school variance estimate: "
            f"{icc_result['between_school_variance_estimate']:.4f}"
        )
        print(
            "Within-school variance estimate: "
            f"{icc_result['within_school_variance_estimate']:.4f}"
        )
        print(f"Raw ICC estimate: {icc_result['icc_raw']:.4f}")

    icc_rows = (
        pd.DataFrame([icc_result])
        if icc_result is not None
        else pd.DataFrame(columns=[
            "schools", "records", "records_per_school",
            "between_school_variance_estimate",
            "within_school_variance_estimate", "icc_raw",
            "icc_interpretation", "data_status",
        ])
    )
    icc_rows.to_csv(
        OUTPUT_DIR / "school_level_variation.csv",
        index=False,
    )

    # Existing visualisations.
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

    report_path = save_report(
        df=df,
        descriptive=descriptive,
        correlation=correlation,
        school_summary=school_summary,
        icc_result=icc_result,
    )

    print("\n6. GENERATED OUTPUTS")
    for filename in [
        "descriptive_statistics.csv",
        "exploratory_correlation.csv",
        "teacher_competence_vs_achievement.png",
        "baseline_current_score_distributions.png",
        "teacher_digital_competence_distribution.png",
        "synthetic_research_report.md",
        "school_level_summary.csv",
        "school_level_achievement_means.png",
        "school_level_variation.csv",
    ]:
        print(f"- {OUTPUT_DIR / filename}")

    print("\nAnalysis completed successfully.")
    print("All outputs describe synthetic data only.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        raise SystemExit(f"ANALYSIS FAILED: {error}") from error
