# GEAA — George's Education & Analytics Agent

**An AI-assisted education, research and analytics project**

GEAA is a personal project exploring how artificial intelligence, knowledge retrieval and data analysis can support teaching, educational research, educational leadership and evidence-informed decision-making.

The project is being developed from the perspective of an educator with experience in Biology and Chemistry teaching, scientific research, and educational leadership and management. Its longer-term purpose is to support practical educational work while encouraging transparent, evidence-aware and responsible use of AI.
## Research Portfolio Highlights

For research-assistant, education research and monitoring-and-evaluation roles, the strongest evidence in this repository is summarised below.

### Featured research demonstration

**Teacher Digital Competence and Class Achievement: Synthetic Research Demonstration**

Location: `research_demos/teacher_digital_competence/`

This demonstration shows a complete, reproducible education research workflow using clearly labelled synthetic data.

It includes:

- a documented research question and analytical objectives;
- a structured synthetic dataset with a codebook and provenance documentation;
- automated data validation (schema, missing values, duplicates, ranges and integrity checks);
- descriptive statistics and exploratory correlation analysis;
- school-level summaries and exploratory intraclass correlation (ICC) estimation;
- automated generation of CSV outputs, visualisations and a Markdown report;
- GitHub Actions workflows for automated testing and reproducibility.

**Research integrity safeguards**

- Every record is labelled `SYNTHETIC_NOT_REAL`.
- The documentation explicitly distinguishes descriptive analysis from causal inference.
- The baseline/current comparison is reported as a descriptive difference between column means, not as evidence of longitudinal change.
- The repository documents the provenance limitations of the original demonstration dataset.

### Research skills demonstrated

- Research workflow documentation
- Data validation and quality assurance
- Python-based data analysis
- Descriptive statistics
- Exploratory correlation analysis
- School-level variance exploration (ICC)
- Data visualisation
- Reproducible research workflows using GitHub Actions
- Responsible reporting of methodological limitations

### Evidence available in this repository

| Evidence | Location |
|----------|----------|
| Research demonstration | `research_demos/teacher_digital_competence/` |
| Analysis script | `analyse_synthetic_data.py` |
| Synthetic dataset generator | `generate_synthetic_dataset.py` |
| Dataset codebook | `geaa_synthetic_dataset_codebook.md` |
| Automated research report | `outputs/synthetic_research_report.md` |
| GitHub Actions workflow | `.github/workflows/synthetic-research-demo.yml` |

This demonstration is a portfolio project illustrating reproducible research practice and responsible analytical reporting. It is not an empirical study of real schools.
## Project objectives

- Explore AI-assisted support for education and research tasks.
- Retrieve relevant information from a curated knowledge base.
- Support preliminary inspection and descriptive analysis of uploaded datasets.
- Encourage clear distinctions between source-based evidence, calculated results, inference and information requiring verification.
- Develop practical digital research capabilities relevant to education, monitoring and evaluation, and evidence-informed programme management.

## Current capabilities

The current application includes the following features:

- **Multiple working modes:** Teaching, Research, Analytics, Education Leadership, TVET and General.
- **Knowledge retrieval:** Searches a local collection of knowledge documents for material relevant to a user's task.
- **Dataset inspection:** Supports preliminary examination of uploaded CSV files, including data types, missing values, duplicate rows and descriptive statistics.
- **Exploratory visualisation:** Produces selected charts when requested and when the dataset structure supports them.
- **Evidence awareness:** Uses instructions designed to distinguish retrieved knowledge, uploaded data, general knowledge, proposed actions and inferences.
- **Retrieval testing:** Includes automated tests for aspects of knowledge retrieval and uses a GitHub Actions workflow to run tests.

These capabilities are being developed and evaluated. Their presence does not, by itself, establish the accuracy of every AI-generated response or the validity of every analytical conclusion.

## Research and professional relevance

GEAA is part of a broader professional development pathway connecting:

- Education research and research methods
- Educational leadership and management
- Science education and TVET
- Research data analysis and visualisation
- AI-assisted knowledge management
- Evidence-informed programme planning and decision-making

The project is intended to complement, not replace, established research methods, statistical analysis, source verification, professional judgement or ethical research practice.

## Technology

The current project uses Python, Streamlit, Google's Gemini API, local knowledge documents and automated testing with GitHub Actions.

## Repository structure

| File or directory | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `knowledge/` | Knowledge documents used by the retrieval workflow |
| `geaa_instructions.txt` | Application instructions and response safeguards |
| `requirements.txt` | Python package dependencies |
| `test_retrieval.py` | Automated retrieval tests |
| `.github/workflows/` | Automated testing workflow |

## Running the project

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Configure `GEMINI_API_KEY` using Streamlit secrets or another appropriate secret-management method.
5. Start the application using `streamlit run app.py`.

Do not commit API keys, passwords, confidential research data or other sensitive information to the repository.

## Responsible use and limitations

GEAA is an evolving prototype. AI-generated outputs require independent verification, and exploratory data analysis should not be treated as proof of causation or as a substitute for a suitable research design.

Use only data that you are authorised to process. Personal, confidential or identifiable educational data should not be uploaded to external AI services without the necessary permissions and appropriate privacy safeguards.

The project will continue to develop through testing, documentation, evaluation and refinement of its research and analytical workflows.

## Development priorities

Planned areas for further work include:

- Improving and systematically evaluating knowledge retrieval.
- Strengthening reproducible data-analysis workflows.
- Expanding documentation and testing.
- Developing education-focused research and decision-support demonstrations.
- Exploring the generation of editable educational presentations.

**Project status:** Under active development.

**Repository:** [GeoNyar/geaa-agent](https://github.com/GeoNyar/geaa-agent)
