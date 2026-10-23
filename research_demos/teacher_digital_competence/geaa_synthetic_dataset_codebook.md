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
<CodeBlock language="markdown" editable>
- Documented generation seed: `20261021`. The current project structure does not list a dataset-generation script, so the seed alone is insufficient to reproduce the original CSV from scratch.

The achievement measure is a class mean score, not an individual student's score.

## 4. Variable codebook

| Variable | Description |
|---|---|
| `school_id` | Fictional school identifier; each school has six synthetic records. |
| `subcounty_label` | Illustrative subcounty label; not a verified sampling location. Held constant within each synthetic school. |
| `teacher_id` | Fictional teacher identifier; unique to each record. |
| `teacher_years_experience` | Synthetic years of teaching experience. |
| `teacher_digital_competence_score` | Synthetic digital competence score on a 0–100 scale. |
| `digital_training_past_2_years` | Indicator of synthetic participation in digital training during the previous two years. |
| `school_resource_access_index` | Synthetic index of school access to relevant digital resources; held constant within each synthetic school. |
| `internet_reliability_rating_1_5` | Synthetic internet reliability rating from 1 to 5; held constant within each synthetic school. |
| `device_access_rating_1_5` | Synthetic device access rating from 1 to 5; held constant within each synthetic school. |
| `class_size` | Synthetic number of learners in the class; may vary between records within a school. |
| `baseline_class_mean_score` | Synthetic baseline class mean achievement score. |
| `current_class_mean_achievement_score` | Synthetic current class mean achievement score. |
| `data_status` | Data provenance marker; all records are labelled `SYNTHETIC_NOT_REAL`. |

**Data structure note:** Each record represents a fictional teacher/class observation, with six records per synthetic school. The subcounty label and three school-level resource indicators are constant within each school. Other variables may vary between records. These design choices are illustrative and do not describe verified Kenyan schools or teachers.

## 5. Illustrative research question

What association exists between teacher digital competence scores and current class mean achievement scores in this synthetic dataset?

### Illustrative objectives

1. Describe the distribution of teacher digital competence and class mean achievement scores.
2. Examine the association between digital competence and current class mean achievement.
3. Demonstrate how baseline achievement, school resources, training and class size may be considered in a future exploratory statistical model. Regression modelling is a potential extension and is not implemented in the current analysis script.
4. Demonstrate data validation, reproducible analysis and responsible reporting.

## 6. Suggested analytical workflow

1. Load the CSV dataset.
2. Verify the number of records and variables.
3. Check missing values, duplicate records, data types and plausible score ranges.
4. Produce descriptive statistics for the main variables.
5. Compare baseline and current class mean scores descriptively, calculating the mean difference as current score minus baseline score and counting records with increases, decreases or no difference.
6. Visualise digital competence scores against current class mean achievement.
7. Calculate an appropriate correlation coefficient.
8. Consider regression modelling as a possible future extension. Before implementation, specify the research question, justify the model, assess relevant assumptions, account for the clustering of records within schools where appropriate, and document the limitations. The current analysis script does not fit a regression model.
9. Consider the clustering of records within schools when selecting statistical methods.
10. Report findings as properties of the synthetic dataset only.

## 7. Interpretation and research integrity

The dataset was generated using constructed relationships between selected variables and random variation. Any observed association is therefore an artefact of the data-generation process, not an empirical finding.

A regression coefficient must not be interpreted as proof that increasing digital competence causes higher achievement. Synthetic results cannot establish the existence, magnitude or direction of relationships in real schools.

A future empirical study would require an appropriate sampling design, ethical approval where applicable, informed permissions, valid measurement instruments, genuine observations and a defensible analysis plan.

## 8. Reproducibility and provenance

The dataset is intended for learning, software testing, research-methods demonstrations and portfolio development. Its synthetic status must remain visible in the data, documentation, figures and reports generated from it.

Any subsequent transformation or analysis should preserve the original dataset and document changes in a separate script or output file.

### Generated analysis outputs

The analysis script generates ten files in the `outputs/` directory:

**Statistical outputs**
- `descriptive_statistics.csv` — descriptive statistics for selected numerical variables.
- `exploratory_correlation.csv` — exploratory Pearson correlation results.
- `school_level_summary.csv` — descriptive summaries for each fictional school.
- `school_level_variation.csv` — exploratory estimates of between-school and within-school variation and the intraclass correlation coefficient (ICC).
- `baseline_current_comparison.csv` — mean baseline and current scores, their mean difference, and counts of records with increases, decreases or no difference.

**Visual outputs**
- `teacher_competence_vs_achievement.png` — scatter plot of digital competence and current achievement.
- `baseline_current_score_distributions.png` — distributions of baseline and current scores.
- `teacher_digital_competence_distribution.png` — distribution of digital competence scores.
- `school_level_achievement_means.png` — mean current achievement by fictional school.

**Research report**
- `synthetic_research_report.md` — generated report summarising the synthetic dataset, descriptive comparison, exploratory association, school-level variation and methodological limitations.

The baseline-to-current comparison is descriptive. The dataset documentation does not establish that the two scores are paired measurements of the same classes at defined time points. The comparison therefore cannot be interpreted as actual longitudinal change or intervention effectiveness.

The files are packaged into the `synthetic-education-research-results` artifact by the GitHub Actions workflow after a successful run. Generated outputs are not necessarily committed to the repository.

## 9. Intended portfolio contribution

This demonstration supports development of skills in education research design, data management, exploratory data analysis, statistical reasoning, visualisation, reproducibility and responsible interpretation. It does not claim that an empirical study has been conducted.

