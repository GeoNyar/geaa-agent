# Kenya Secondary School Enrolment: Open-Data Case Study

## Purpose and status

This case study demonstrates a reproducible workflow using a real, publicly available national-level education indicator. It retrieves Kenya's annual **school enrolment, secondary (% gross)** series from the World Bank's World Development Indicators (WDI), whose source metadata attributes the indicator to the UNESCO Institute for Statistics (UIS).

**This is a national trend analysis, not a county-level access study.** It cannot establish spatial inequality within Kenya, individual attendance, completion, learning outcomes, or causal effects.

## Research question

How has Kenya's reported gross secondary-school enrolment ratio changed over the available annual observations from 2000 to 2023, and which years are missing from the retrieved series?

## Data source and provenance

- Publisher/host: World Bank, World Development Indicators.
- Indicator: `SE.SEC.ENRR` — School enrollment, secondary (% gross).
- Country: Kenya (`KEN`).
- Requested period: 2000–2023.
- API endpoint: https://api.worldbank.org/v2/country/KEN/indicator/SE.SEC.ENRR?date=2000:2023&format=json&per_page=100
- Indicator page: https://data.worldbank.org/indicator/SE.SEC.ENRR?locations=KE
- Indicator definition: gross enrolment ratio compares total enrolment, regardless of age, with the population of the official age group for that education level. Values can exceed 100 because of under-age or over-age enrolment.
- Source notes and metadata: https://databank.worldbank.org/metadataglossary/World-Development-Indicators/series/page/30

The script retrieves the data at workflow runtime and records the retrieval timestamp and source URL in a provenance JSON file. Values may be revised by the source, so outputs should be interpreted with the retrieval date in mind.

## Analysis

The workflow will:
1. retrieve the official API response;
2. preserve the raw observations as CSV;
3. check expected fields, year range, duplicate years, and missing observations;
4. calculate the earliest/latest available observations and their descriptive difference when both exist;
5. create a time-series chart;
6. generate a concise Markdown report with explicit limitations; and
7. upload the outputs as a GitHub Actions artifact.

The analysis is descriptive. It will not interpolate missing years, infer causal effects, or treat gross enrolment as the same as attendance, completion, or education quality.

## Limitations

- National averages can conceal inequalities between counties, urban and rural communities, socioeconomic groups, and genders.
- Gross enrolment ratios are not direct measures of attendance, completion, learning, or school quality.
- Missing observations must be reported rather than silently filled.
- A trend alone cannot identify the causes of change.
- The dataset is real open data, but the analysis is limited to the published indicator and its definitions.

## Reproduce the analysis

The workflow is located at `.github/workflows/kenya-secondary-enrolment-case-study.yml`. Open **Actions**, select the workflow, choose **Run workflow** if available, and download the `kenya-secondary-enrolment-case-study` artifact from a successful run.

## Citation

World Bank. (n.d.). *School enrollment, secondary (% gross) — Kenya (SE.SEC.ENRR).* World Development Indicators. https://data.worldbank.org/indicator/SE.SEC.ENRR?locations=KE

The World Bank indicator metadata identifies UNESCO Institute for Statistics as the data source. Cite the source URL and the extraction date shown in the generated provenance file when reusing the outputs.
