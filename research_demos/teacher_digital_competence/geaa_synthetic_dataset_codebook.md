# Teacher Digital Competence and Student Achievement: Synthetic Research Demonstration

## 1. Purpose

This folder demonstrates a reproducible education research workflow using a clearly labelled synthetic dataset. The illustrative topic is the relationship between teacher digital competence and class-level student achievement in public secondary schools in Kilifi County, Kenya.

## 2. Important data disclaimer

**This is entirely synthetic data. It is not real research data.**

The 120 records were artificially generated for demonstration and portfolio development. School IDs, teacher IDs, observations, scores and resource indicators are fictional. Subcounty labels are illustrative and do not identify actual sampled schools.

The dataset must not be presented as evidence about real teachers, schools or students in Kilifi County or Kenya. It must not be used to make claims about actual educational outcomes or to support causal conclusions.

Every record is marked `SYNTHETIC_NOT_REAL` in the `data_status` variable.

## 3. Dataset description

- File: `geaa_synthetic_teacher_digital_competence.csv`
- Number of records: 120
- Number of variables: 13
- Unit of analysis: a synthetic teacher/class record
- School identifiers: 20 fictional school IDs
- Records per school: 6
- Reproducibility: the data-generation process used a fixed random seed of `20261021`

The achievement measure is a class mean score, not an individual student's score.

## 4. Variable codebook

| Variable | Description |
|---|---|
| `school_id` | Fictional school identifier |
| `subcounty_label` | Illustrative subcounty label; not a verified sampling location |
| `teacher_id` | Fictional teacher identifier |
| `teacher_years_experience` | Synthetic years of teaching experience |
| `teacher_digital_competence_score` | Synthetic digital competence score on a 0–100 scale |
| `digital_training_past_2_years` | Indicator of synthetic participation in digital training during the previous two years |
| `school_resource_access_index` | Synthetic index of school access to relevant digital resources |
| `internet_reliability_rating_1_5` | Synthetic internet reliability rating from 1 to 5 |
| `device_access_rating_1_5` | Synthetic device access rating from 1 to 5 |
| `class_size` | Synthetic number of learners in the class |
| `baseline_class_mean_score` | Synthetic baseline class mean achievement score |
| `current_class_mean_achievement_score` | Synthetic current class mean achievement score |
| `data_status` | Data provenance marker; all records are labelled `SYNTHETIC_NOT_REAL` |

## 5. Illustrative research question

What association exists between teacher digital competence scores and current class mean achievement scores in this synthetic dataset?

### Illustrative objectives

1. Describe the distribution of teacher digital competence and class mean achievement scores.
2. Examine the association between digital competence and current class mean achievement.
3. Demonstrate how baseline achievement, school resources, training and class size could be considered in an exploratory statistical model.
4. Demonstrate data validation, reproducible analysis and responsible reporting.

## 6. Suggested analytical workflow

1. Load the CSV dataset.
2. Verify the number of records and variables.
3. Check missing values, duplicate records, data types and plausible score ranges.
4. Produce descriptive statistics for the main variables.
5. Visualise digital competence scores against current class mean achievement.
6. Calculate an appropriate correlation coefficient.
7. Fit an exploratory regression model, clearly documenting its assumptions and limitations.
8. Consider the clustering of records within schools when selecting statistical methods.
9. Report findings as properties of the synthetic dataset only.

## 7. Interpretation and research integrity

The dataset was generated using constructed relationships between selected variables and random variation. Any observed association is therefore an artefact of the data-generation process, not an empirical finding.

A regression coefficient must not be interpreted as proof that increasing digital competence causes higher achievement. Synthetic results cannot establish the existence, magnitude or direction of relationships in real schools.

A future empirical study would require an appropriate sampling design, ethical approval where applicable, informed permissions, valid measurement instruments, genuine observations and a defensible analysis plan.

## 8. Reproducibility and provenance

The dataset is intended for learning, software testing, research-methods demonstrations and portfolio development. Its synthetic status must remain visible in the data, documentation, figures and reports generated from it.

Any subsequent transformation or analysis should preserve the original dataset and document changes in a separate script or output file.

## 9. Intended portfolio contribution

This demonstration supports development of skills in education research design, data management, exploratory data analysis, statistical reasoning, visualisation, reproducibility and responsible interpretation. It does not claim that an empirical study has been conducted.

