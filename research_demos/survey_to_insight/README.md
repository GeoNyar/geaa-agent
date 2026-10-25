# Survey-to-Insight: Research Data Analysis and Reporting Workflow

## 1. Project Overview

Survey-to-Insight is a research data-management and reporting demonstration within George's Education & Analytics Agent (GEAA) repository. It demonstrates how a structured survey dataset can be generated, validated, analysed and transformed into reproducible outputs for research review and decision support.

The current implementation uses clearly labelled synthetic data to demonstrate the analytical workflow. The generated records do not represent actual respondents, educators, schools or institutions. Consequently, the outputs are examples of the workflow's technical capabilities, not empirical research findings.

The project is designed to support the development of practical skills in education research, data quality assurance, descriptive analysis, visualisation and evidence-based reporting.

## 2. Project Objectives

The project aims to:

1. Establish a structured questionnaire and associated research variables.
2. Generate reproducible synthetic survey data for software testing and demonstration.
3. Validate datasets against documented data-quality rules.
4. Identify missing responses, duplicate records, invalid categories and out-of-range values.
5. Produce descriptive statistics, frequency tables and selected comparisons.
6. Generate charts and visual summaries appropriate to the data.
7. Export analysis outputs into a consolidated Excel workbook.
8. Generate a structured Word research report with embedded charts, interpretation and limitations.
9. Apply automated tests and continuous integration to improve reliability and reproducibility.
10. Provide a foundation for future interactive dashboards and presentation outputs.

## 3. Implemented Workflow

The current workflow connects data generation, validation, analysis and reporting through Python scripts and GitHub Actions.

1. **Synthetic data generation:** Creates a reproducible demonstration dataset using a specified sample size and random seed.
2. **Data validation:** Checks the generated dataset against defined structural and quality rules and produces a validation report.
3. **Descriptive analysis:** Produces frequency tables, descriptive statistics, selected comparisons, response-completeness summaries and charts.
4. **Excel workbook generation:** Consolidates the analysis tables and validation information into a reviewable workbook.
5. **Word report generation:** Produces a structured report containing methods, descriptive results, charts, interpretation, limitations and recommendations for a future real assessment.
6. **Automated testing:** Runs tests for key functions, expected outputs and selected failure conditions.
7. **Continuous integration and artifact generation:** GitHub Actions runs the tests and processing steps, then packages the resulting files into a downloadable workflow artifact.

The workflow is designed so that generated outputs can be recreated from the code rather than relying on manually prepared tables and reports.

## 4. Technology Stack

| Technology | Role in the project |
|---|---|
| Python | Workflow implementation and automation |
| pandas | Dataset processing and descriptive analysis |
| NumPy | Numerical operations and synthetic-data support |
| matplotlib | Charts and visual summaries |
| pytest | Automated testing |
| openpyxl | Excel workbook generation and handling |
| python-docx | Word report generation |
| GitHub Actions | Automated testing, workflow execution and artifact publication |

The project is maintained within the existing GEAA GitHub repository. The workflow uses Python 3.12 in GitHub Actions.

## 5. Current Outputs

The successful workflow produces a downloadable artifact named `survey-to-insight-analysis`.

| Output | Purpose | Status |
|---|---|---|
| `synthetic_responses.csv` | Generated demonstration survey records | Implemented |
| `validation_report.json` | Machine-readable dataset validation results | Implemented |
| `categorical_frequencies.csv` | Frequency summaries for categorical variables | Implemented |
| `familiarity_descriptive_statistics.csv` | Descriptive statistics for familiarity measures | Implemented |
| `familiarity_means_by_role.csv` | Descriptive comparisons by respondent role | Implemented |
| `respondent_counts_by_role.csv` | Counts by role | Implemented |
| `q10_task_frequencies.csv` | Task-response frequency summaries | Implemented |
| `q12_response_completeness.csv` | Response-completeness summaries | Implemented |
| `mean_familiarity_by_skill.png` | Chart of familiarity by skill | Implemented |
| `respondents_by_role.png` | Chart of respondent counts by role | Implemented |
| `analysis_manifest.json` | Records analysis provenance and dataset classification | Implemented |
| `survey_to_insight_workbook.xlsx` | Consolidated Excel workbook with eight worksheets | Implemented |
| `survey_to_insight_research_report.docx` | Structured Word report with embedded charts | Implemented |

The workflow also retains the analysis outputs in the `analysis_outputs/` directory during execution. Generated files are packaged as a GitHub Actions artifact rather than being committed as if they were actual survey findings.

## 6. Automated Testing and Quality Assurance

Automated tests cover the main components of the workflow, including synthetic-data generation, validation, descriptive analysis, Excel workbook creation and Word report generation.

The tests include checks for:

- Expected outputs and required report content.
- Dataset validation and selected invalid-data conditions.
- Response-completeness calculations.
- Required Excel worksheets and report contents.
- Refusal to generate reporting outputs when required synthetic-data labels or validation conditions are not satisfied.
- Handling of missing required analysis files.

The workflow has passed GitHub Actions after integration of the Word report generator. This confirms that the configured tests and processing steps completed successfully in that run.

Passing tests does not establish that the questionnaire is psychometrically valid, that the synthetic data represent a real population, or that every possible analytical error has been eliminated. Methodological decisions and substantive interpretations still require human review.

## 7. Research Integrity and Methodological Limitations

This is an exploratory software and analytical workflow demonstration, not a completed empirical study.

The following limitations are important:

- **Synthetic records:** The dataset is generated for demonstration and is not evidence about actual educators or institutions.
- **Questionnaire status:** The questionnaire has not been established as a validated research instrument through field administration and appropriate validation procedures.
- **Descriptive scope:** The current workflow focuses on data quality and descriptive analysis. It does not establish causal relationships or support population-level conclusions about real educators.
- **Automated validation:** Passing validation checks confirms compliance with specified rules, not the overall suitability of data for every research purpose.
- **Report interpretation:** Narrative reporting and recommendations must be interpreted in light of the synthetic dataset and the demonstration's purpose.

Any future study using actual participants would require appropriate research design, ethical safeguards, consent where applicable, secure data handling and compliance with relevant data-protection requirements.

## 8. Reproducibility

The workflow is maintained in the `GeoNyar/geaa-agent` repository under:

`research_demos/survey_to_insight/`

The GitHub Actions workflow is located at:

`.github/workflows/survey-to-insight-tests.yml`

The workflow can run following qualifying repository changes or be started manually through GitHub Actions using **Run workflow**, where available.

During execution, it:

1. Sets up Python 3.12.
2. Installs the required dependencies.
3. Runs the automated tests.
4. Generates 100 synthetic survey records using a configured random seed.
5. Validates the dataset.
6. Performs the descriptive analysis.
7. Creates the Excel workbook and Word report.
8. Uploads the generated outputs as the `survey-to-insight-analysis` artifact.

To inspect the results, open the repository's **Actions** tab, select a successful workflow run and download its artifact. Artifact availability is subject to the workflow's configured retention period.

## 9. Future Development

The next stages will be considered separately and marked as implemented only after development and verification.

| Planned enhancement | Intended purpose |
|---|---|
| Editable PowerPoint presentation | Communicate selected results and recommendations to decision-makers |
| Interactive dashboard | Explore selected results through filters and visual summaries |
| Expanded cross-tabulations | Support additional research questions where the data and sample structure justify them |
| Enhanced methodological documentation | Explain variable definitions, analytical choices and interpretation boundaries |
| Real-data readiness review | Assess data protection, governance, validation and research requirements before any empirical use |

Future enhancements will preserve the existing GEAA application and its other demonstrations.

## 10. Professional Relevance

Survey-to-Insight demonstrates practical work relevant to education research assistance, education data analysis, monitoring and evaluation support, and research-programme reporting.

The project provides a public example of the ability to:

- Develop reproducible data-processing workflows.
- Apply structured data-quality checks.
- Produce descriptive statistical summaries and visualisations.
- Automate Excel and Word reporting.
- Implement automated tests and continuous integration.
- Document limitations and distinguish synthetic demonstrations from empirical evidence.

The repository demonstrates technical work and learning in progress. It should not be interpreted as evidence of completed field research, professional consultancy assignments or validated findings unless separate supporting evidence is available.

## 11. Relationship to GEAA

Survey-to-Insight is a component of the existing George's Education & Analytics Agent (GEAA) repository. It extends the repository's research and analytics capabilities while preserving the main application, existing knowledge files and previous demonstrations.

The longer-term aim is to develop a transparent, reproducible and research-aware workflow that supports the responsible transformation of survey data into useful analytical outputs.
