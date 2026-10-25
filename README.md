# GEAA — George's Education & Analytics Agent

**An AI-assisted education, research and analytics project**

GEAA is a personal project exploring how artificial intelligence, knowledge retrieval and data analysis can support teaching, educational research, educational leadership and evidence-informed decision-making.

The project is being developed from the perspective of an educator with experience in teaching, scientific research, and educational leadership and management. Its longer-term purpose is to support practical educational work while encouraging transparent, evidence-aware and responsible use of AI.

**Repository:** [GeoNyar/geaa-agent](https://github.com/GeoNyar/geaa-agent)

## Research Portfolio Highlights

The repository includes two complementary research demonstrations. Together, they illustrate aspects of reproducible education research, data quality assurance, exploratory statistical analysis, automated reporting and responsible interpretation.

### 1. Survey-to-Insight: Research Data Analysis and Reporting Workflow

**Location:** [`research_demos/survey_to_insight/`](research_demos/survey_to_insight/)

[Read the Survey-to-Insight project documentation](research_demos/survey_to_insight/README.md)

Survey-to-Insight demonstrates how survey data can be transformed into validated, reproducible analysis outputs and structured reports.

The implemented workflow includes:

- Reproducible synthetic survey-data generation.
- Automated data validation and machine-readable quality reporting.
- Descriptive statistics, frequency tables and response-completeness analysis.
- Automated charts and visual summaries.
- An Excel workbook containing eight worksheets.
- A structured Word research report with embedded charts, interpretation, limitations and recommendations.
- Automated tests and GitHub Actions integration.
- Downloadable workflow artifacts containing generated data and analysis outputs.

**Research integrity safeguards**

- The demonstration dataset is synthetic and is not evidence from actual respondents.
- The questionnaire has not been established as a validated research instrument through field administration.
- Automated validation checks specified data-quality rules but does not establish overall methodological validity.
- Descriptive results from synthetic data must not be interpreted as empirical findings about educators, schools or institutions.

**Skills demonstrated:** Data management, validation, descriptive analysis, visualisation, reproducible reporting, Python automation and continuous integration.

### 2. Teacher Digital Competence and Class Achievement: Synthetic Research Demonstration

**Location:** [`research_demos/teacher_digital_competence/`](research_demos/teacher_digital_competence/)

This demonstration explores a reproducible analytical workflow around teacher digital competence and class mean achievement, using clearly labelled synthetic data.

It includes:

- A documented research question and analytical objectives.
- A structured synthetic dataset and codebook.
- Automated data validation, including schema, missing-value, duplicate, range and integrity checks.
- Descriptive statistics and exploratory correlation analysis.
- School-level summaries and exploratory intraclass correlation coefficient (ICC) estimation.
- Automated CSV outputs, visualisations and a Markdown research report.
- GitHub Actions automation for testing and reproducibility.

**Research integrity safeguards**

- The dataset is labelled `SYNTHETIC_NOT_REAL`.
- Descriptive analysis is distinguished from causal inference.
- Baseline/current column comparisons are treated as descriptive differences, not evidence of longitudinal change.
- The documentation identifies the limitations of the demonstration dataset.

**Skills demonstrated:** Research workflow documentation, quantitative data analysis, exploratory association analysis, school-level variance exploration, visualisation and responsible reporting.

This project is a portfolio demonstration, not an empirical study of real teachers or schools.

## Research Skills Evidence Matrix

The following matrix maps selected research-assistant competencies to evidence available in the repository. It distinguishes implemented technical work from areas requiring further development or separate evidence.

| Competency | Evidence | What it demonstrates |
|---|---|---|
| Research data management | Synthetic datasets and codebooks in both research demonstrations | Structured data, variable documentation and provenance labelling |
| Data validation and quality assurance | `validate_data.py`, `analyse_synthetic_data.py` and related tests | Programmatic checks and documented validation rules |
| Quantitative data analysis | `analyse_survey.py`, `analyse_synthetic_data.py` and generated tables | Descriptive statistics, frequency analysis and selected comparisons |
| Exploratory statistical interpretation | Correlation and ICC outputs in the teacher digital competence demonstration | Exploratory examination of associations and school-level variation |
| Data visualisation | Generated PNG charts in both demonstrations | Automated production of visual summaries |
| Research reporting | Excel and Word outputs in Survey-to-Insight; Markdown report in the teacher digital competence demonstration | Structured analytical outputs and documented limitations |
| Reproducible workflows | `.github/workflows/` | Automated tests and repeatable processing through GitHub Actions |
| Automated software testing | Test files in both research demonstrations and `test_retrieval.py` | Verification of specified behaviours and selected failure conditions |
| Knowledge retrieval | `test_retrieval.py` and `knowledge/` | Development and testing of an AI-assisted knowledge-retrieval component |
| Literature searching and evidence synthesis | Further portfolio work planned | A documented search strategy, source verification, evidence extraction and synthesis are still needed |
| Monitoring, evaluation and learning (MEL) | Further portfolio work planned | Indicator development, programme monitoring, disaggregation and evaluation reporting require further demonstration |
| Research ethics and data protection | `geaa_instructions.txt` and responsible-use documentation | Documented safeguards; practical application with authorised research data requires separate evidence |

### How to interpret this matrix

The matrix identifies evidence available in the GEAA portfolio; it is not a claim of mastery of every research-assistant competency.

The research demonstrations use synthetic data. They illustrate workflow development, data quality checks, exploratory analysis, automation and reporting, but do not establish empirical findings about actual schools, educators or programmes.

The portfolio complements, rather than replaces, evidence from academic qualifications, publications, research projects and professional experience. Suitability for a specific role should be assessed against its requirements and the evidence available for each competency.

## Project Objectives

GEAA aims to:

- Explore AI-assisted support for education and research tasks.
- Retrieve relevant information from a curated knowledge base.
- Support preliminary inspection and descriptive analysis of uploaded datasets.
- Encourage clear distinctions between source-based evidence, uploaded data, calculated results, general knowledge, proposals and inferences.
- Develop practical digital research capabilities relevant to education, monitoring and evaluation, and evidence-informed programme management.
- Build reproducible, testable demonstrations that can be inspected and improved over time.

## Current Application Capabilities

The main GEAA application includes the following features:

- **Multiple working modes:** Teaching, Research, Analytics, Education Leadership, TVET and General.
- **Knowledge retrieval:** Searches a local collection of knowledge documents for material relevant to a user's task.
- **Dataset inspection:** Supports preliminary examination of uploaded CSV files, including data types, missing values, duplicate rows and descriptive statistics.
- **Exploratory visualisation:** Produces selected charts when requested and when the dataset structure supports them.
- **Evidence awareness:** Uses instructions designed to distinguish retrieved knowledge, uploaded data, general knowledge, proposed actions and inferences.
- **Retrieval testing:** Includes automated tests for aspects of knowledge retrieval and a GitHub Actions workflow.

These capabilities are under development and evaluation. Their presence does not establish the accuracy of every AI-generated response or the validity of every analytical conclusion.

The research demonstrations are separate components of the repository. Their generated outputs should not be confused with the main application's live functionality.

## Research and Professional Relevance

GEAA supports a broader professional development pathway connecting:

- Education research and research methods.
- Educational leadership and management.
- Science education and TVET.
- Research data analysis and visualisation.
- AI-assisted knowledge management.
- Evidence-informed programme planning and decision-making.

The repository provides practical examples of technical work relevant to education research assistance, research data management, education analytics and research-programme reporting.

It is intended to complement, not replace, established research methods, statistical analysis, source verification, professional judgement or ethical research practice.

## Technology

The main GEAA application uses Python, Streamlit, Google's Gemini API, local knowledge documents and automated testing with GitHub Actions.

The research demonstrations additionally use relevant data-processing, visualisation, testing and document-generation libraries, including:

- pandas and NumPy.
- matplotlib.
- pytest.
- openpyxl.
- python-docx.
- GitHub Actions.

Individual components use only the dependencies required for their workflows.

## Repository Structure

| File or directory | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `knowledge/` | Knowledge documents used by the retrieval workflow |
| `geaa_instructions.txt` | Application instructions and response safeguards |
| `requirements.txt` | Main application dependencies |
| `test_retrieval.py` | Automated retrieval tests |
| `research_demos/teacher_digital_competence/` | Synthetic education research and statistical analysis demonstration |
| `research_demos/survey_to_insight/` | Survey validation, descriptive analysis and automated reporting demonstration |
| `.github/workflows/` | Automated testing and research workflow definitions |

## Running the Main Application

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Configure `GEMINI_API_KEY` through Streamlit secrets or another appropriate secret-management method.
5. Start the application using `streamlit run app.py`.

Do not commit API keys, passwords, confidential research data or other sensitive information to the repository.

For the research demonstrations, consult the README in each project folder for its scope, workflow and available outputs. The Survey-to-Insight workflow can also be inspected and run through GitHub Actions.

## Responsible Use and Limitations

GEAA is an evolving prototype. AI-generated outputs require independent verification, and exploratory data analysis should not be treated as proof of causation or as a substitute for an appropriate research design.

Use only data that you are authorised to process. Personal, confidential or identifiable educational data should not be uploaded to external AI services without the necessary permissions and appropriate privacy safeguards.

Synthetic datasets in this repository are intended for software development and portfolio demonstration. They must not be represented as actual participant responses, field research findings or evidence of programme effectiveness.

Future use with real participants would require suitable research design, ethical safeguards, consent where applicable, secure data handling and compliance with relevant data-protection requirements.

## Development Priorities

Planned areas for further work include:

- Improving and systematically evaluating knowledge retrieval.
- Strengthening reproducible data-analysis workflows.
- Expanding automated tests and methodological documentation.
- Developing education-focused research and decision-support demonstrations.
- Building editable PowerPoint reporting and interactive dashboards.
- Developing a documented literature-search and evidence-synthesis workflow.
- Demonstrating monitoring, evaluation and learning methods using appropriate, clearly documented data.

Planned enhancements will be marked as completed only after implementation and verification.

**Project status:** Under active development.

**Repository:** [GeoNyar/geaa-agent](https://github.com/GeoNyar/geaa-agent)
