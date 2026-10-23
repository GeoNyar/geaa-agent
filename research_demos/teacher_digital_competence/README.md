# Teacher Digital Competence and Class Achievement: A Synthetic Research Demonstration

## 1. Project Overview

This project demonstrates a reproducible workflow for exploring a potential education research question: the relationship between teacher digital competence and class-level academic achievement.

The demonstration uses a clearly labelled **synthetic dataset** created for portfolio development and analytical practice. It does not contain observations collected from actual teachers, learners or schools.

The project is part of **GEAA — George's Education & Analytics Agent** and demonstrates selected skills in education research design, data validation, descriptive statistics, exploratory analysis, visualisation and reproducible research workflows.

## 2. Illustrative Research Question

What relationship, if any, exists between teacher digital competence scores and current class mean achievement scores in the synthetic dataset?

### Illustrative objectives

1. Validate the structure and basic quality of the synthetic dataset.
2. Summarise teacher digital competence and class mean achievement scores.
3. Visualise the distributions of selected variables.
4. Explore the association between teacher digital competence and current class mean achievement.
5. Document the limitations of interpreting analyses conducted on synthetic, clustered data.

These objectives demonstrate an analytical workflow; they do not constitute findings from an empirical education study.

## 3. Dataset Description

The dataset contains 120 synthetic records and 13 variables. It represents 20 fictional school identifiers, with six records per school.

The dataset includes variables relating to:

- Teacher digital competence scores.
- Teaching experience and digital training.
- School resource access.
- Internet reliability and device access.
- Class size.
- Baseline and current class mean achievement scores.
- School identifiers and illustrative subcounty labels.

The dataset uses a fixed random seed of `20261021` for its documented generation process.

**Data integrity statement:** All records are labelled `SYNTHETIC_NOT_REAL`. School identifiers and contextual labels are illustrative. The data must not be represented as observations from real Kenyan schools or teachers.

For variable definitions and additional methodological notes, see [`geaa_synthetic_dataset_codebook.md`](geaa_synthetic_dataset_codebook.md).

## 4. Project Structure

```text

teacher_digital_competence/
├── README.md
├── geaa_synthetic_dataset_codebook.md
├── geaa_synthetic_teacher_digital_competence.csv
├── analyse_synthetic_data.py
└── outputs/
    ├── descriptive_statistics.csv
    ├── exploratory_correlation.csv
    ├── school_level_summary.csv
    ├── school_level_variation.csv
    ├── baseline_current_comparison.csv
    ├── teacher_competence_vs_achievement.png
    ├── baseline_current_score_distributions.png
    ├── teacher_digital_competence_distribution.png
    ├── school_level_achievement_means.png
    └── synthetic_research_report.md

```

**Note:** The `outputs/` directory and its files are generated when the analysis script runs. The GitHub Actions workflow packages the generated CSV, PNG and Markdown files into a downloadable artifact named `synthetic-education-research-results`. These generated files are not necessarily committed to the repository.

## 5. Analytical Workflow

The Python script, `analyse_synthetic_data.py`, performs the following tasks:

1. Loads the dataset using a path relative to the script.
2. Checks required columns and verifies the synthetic-data status labels.
3. Reports the number of records and variables, duplicate rows, missing values and unique school identifiers.
4. Summarises selected numerical variables using descriptive statistics.
5. Calculates an exploratory Pearson correlation between teacher digital competence and current class mean achievement, using records with complete values for those variables.
6. Generates three descriptive visualisations.
7. Saves descriptive statistics, the baseline-to-current score comparison,
   exploratory correlation results, school-level summaries, school-level
   variation estimates, visualisations and a Markdown research report.


The correlation is an exploratory, unadjusted analysis. It does not account for the grouping of records within schools and should not be interpreted as evidence of a causal relationship.

## 6. Research Outputs

The analysis script generates ten output files.

### Statistical outputs

- `descriptive_statistics.csv` — descriptive statistics for selected numerical variables.
- `exploratory_correlation.csv` — exploratory Pearson correlation results, including the variables compared, number of complete records and synthetic-data status.
- `school_level_summary.csv` — summary measures for each fictional school.
- `school_level_variation.csv` — estimates of variation between and within fictional schools, supporting an exploratory examination of school-level clustering.

- `baseline_current_comparison.csv` — descriptive comparison of baseline and current scores, including the mean difference and counts of records with increases, decreases or no difference.

### Visual outputs

- `teacher_competence_vs_achievement.png` — scatter plot of teacher digital competence and current class mean achievement.
- `baseline_current_score_distributions.png` — comparison of baseline and current class mean score distributions.
- `teacher_digital_competence_distribution.png` — distribution of teacher digital competence scores.
- `school_level_achievement_means.png` — comparison of mean achievement across fictional schools.

### Research report

- `synthetic_research_report.md` — automatically generated Markdown report containing the dataset overview, descriptive statistics, baseline-to-current comparison, exploratory correlation, school-level variation, methodological limitations and requirements for a real study.

All outputs describe synthetic data only. The baseline/current score comparison does not establish actual change over time, and the correlation does not demonstrate causation. School-level summaries and variation estimates are also illustrative and cannot establish real differences between schools. The files are available in the downloadable GitHub Actions artifact after a successful workflow run.
## 7. Reproducibility

The project uses Python, pandas and Matplotlib.

From the repository root, run:

python -m pip install pandas matplotlib
python research_demos/teacher_digital_competence/analyse_synthetic_data.py

The script generates the output files in the demonstration's `outputs/` directory.

### Automated execution

The GitHub Actions workflow is located at:

`.github/workflows/synthetic-research-demo.yml`

It runs the analysis when relevant files in this demonstration or the workflow itself change. It also supports manual execution through GitHub Actions and uploads the generated CSV, PNG and Markdown report files as the downloadable artifact `synthetic-education-research-results`.

To download the results, open the repository's **Actions** tab, select a successful run of the synthetic research demonstration workflow, scroll to the **Artifacts** section, and download `synthetic-education-research-results`. Extract the downloaded archive to access the generated files.

The repository has a separate workflow for retrieval tests. The synthetic research demonstration is intended to remain separate from the existing GEAA application and its retrieval-testing workflow.

## 8. Methodological Limitations and Research Integrity

This demonstration has important limitations:

- **Synthetic data:** The dataset does not represent actual schools, teachers or learners.
- **No empirical generalisation:** Results cannot establish the prevalence of digital competence, the state of achievement or differences between schools in Kenya.
- **No causal inference:** A correlation cannot establish that digital competence causes higher or lower achievement.
- **School-level clustering:** Records share fictional school identifiers. An ordinary Pearson correlation does not account for this clustering.
- **Illustrative variables:** Variable definitions and generated values are intended for demonstration, not as validated measures of teacher competence or educational achievement.
- **No policy conclusions:** The outputs must not be used as evidence for education policy, resource allocation or school performance judgements.

An empirical study would require an appropriate research design, defensible sampling, valid measurement instruments, ethical approval where applicable, real and lawfully obtained data, and analytical methods aligned with the research questions and data structure.

## 9. Portfolio Contribution

This project demonstrates practical engagement with:

- Education research question formulation.
- Dataset documentation and variable interpretation.
- Python-based data validation and analysis.
- Descriptive statistics and exploratory correlation.
- Research visualisation.
- Reproducible analytical workflows using GitHub Actions.
- Transparent reporting of limitations and synthetic data provenance.

The demonstration is a foundation for developing more advanced education research workflows, including appropriate missing-data assessment, multilevel analysis, monitoring and evaluation indicators, and policy-oriented evidence synthesis when suitable real data and research questions are available.

## 10. Responsible Use

This project is an educational and technical demonstration. Its synthetic results are not empirical research findings and must not be presented as such in academic publications, job applications, policy reports or research proposals.

**Project:** GEAA — George's Education & Analytics Agent  
**Repository:** [GeoNyar/geaa-agent](https://github.com/GeoNyar/geaa-agent)  
**Demonstration status:** Synthetic research workflow; not an empirical study.
