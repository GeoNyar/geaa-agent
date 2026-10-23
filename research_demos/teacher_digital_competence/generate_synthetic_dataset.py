
"""
GEAA Synthetic Education Dataset Generator
Topic: Teacher digital competence and class mean achievement.

IMPORTANT:
This script creates synthetic demonstration data, not real research evidence.
The generated records must not be presented as findings about actual
teachers, learners or schools.

PROVENANCE:
This is a newly documented generator. It is not claimed to be the
original script used to create the existing demonstration CSV.
It writes to a separate filename to protect that existing dataset.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent

# A new filename protects the original analysis dataset.
OUTPUT_FILE = SCRIPT_DIR / "geaa_synthetic_teacher_digital_competence_regenerated.csv"

RANDOM_SEED = 20261023
NUMBER_OF_SCHOOLS = 20
RECORDS_PER_SCHOOL = 6

rng = np.random.default_rng(RANDOM_SEED)


# ---------------------------------------------------------------------
# 2. GENERATE SYNTHETIC RECORDS
# ---------------------------------------------------------------------

def generate_dataset():
    """Generate fictional school and teacher/class-level records."""

    records = []
    teacher_number = 1

    for school_number in range(1, NUMBER_OF_SCHOOLS + 1):
        school_id = f"SCH{school_number:03d}"

        # Fictional school-level characteristics.
        subcounty_label = f"Fictional_Subcounty_{((school_number - 1) % 4) + 1}"
        resource_index = round(float(rng.uniform(0.2, 0.95)), 2)
        internet_rating = int(rng.integers(1, 6))
        device_rating = int(rng.integers(1, 6))

        # A school-level achievement component creates clustering.
        school_effect = rng.normal(0, 7)

        for _ in range(RECORDS_PER_SCHOOL):
            experience = int(rng.integers(0, 36))
            competence = float(np.clip(rng.normal(65, 15), 0, 100))
            training = int(rng.integers(0, 2))
            class_size = int(rng.integers(20, 71))

            # These formulas create illustrative synthetic patterns only.
            baseline = float(np.clip(
                50 + school_effect + rng.normal(0, 8),
                0, 100
            ))

            current = float(np.clip(
                40
                + 0.18 * competence
                + 4 * training
                + 5 * resource_index
                + school_effect
                + rng.normal(0, 7),
                0, 100
            ))

            records.append({
                "school_id": school_id,
                "subcounty_label": subcounty_label,
                "teacher_id": f"TCH{teacher_number:04d}",
                "teacher_years_experience": experience,
                "teacher_digital_competence_score": round(competence, 2),
                "digital_training_past_2_years": training,
                "school_resource_access_index": resource_index,
                "internet_reliability_rating_1_5": internet_rating,
                "device_access_rating_1_5": device_rating,
                "class_size": class_size,
                "baseline_class_mean_score": round(baseline, 2),
                "current_class_mean_achievement_score": round(current, 2),
                "data_status": "SYNTHETIC_NOT_REAL",
            })

            teacher_number += 1

    return pd.DataFrame(records)


# ---------------------------------------------------------------------
# 3. VALIDATE AND SAVE
# ---------------------------------------------------------------------

def main():
    df = generate_dataset()

    expected_records = NUMBER_OF_SCHOOLS * RECORDS_PER_SCHOOL

    assert len(df) == expected_records
    assert df["school_id"].nunique() == NUMBER_OF_SCHOOLS
    assert df["teacher_id"].is_unique
    assert df["data_status"].eq("SYNTHETIC_NOT_REAL").all()
    assert not df.isna().any().any()
    assert not df.duplicated().any()

    # Write only to the separate regenerated filename.
    df.to_csv(OUTPUT_FILE, index=False)

    print("Synthetic dataset generated successfully.")
    print(f"Records: {len(df)}")
    print(f"Variables: {len(df.columns)}")
    print(f"Fictional schools: {df['school_id'].nunique()}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Output: {OUTPUT_FILE.name}")
    print("Data status: SYNTHETIC_NOT_REAL")
    print("The existing original CSV was not overwritten.")


if __name__ == "__main__":
    main()
