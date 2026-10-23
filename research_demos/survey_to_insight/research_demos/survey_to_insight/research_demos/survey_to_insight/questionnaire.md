# Research and Data Skills Needs Assessment Questionnaire

## 1. Purpose

This proposed questionnaire is designed to demonstrate a reproducible survey-data workflow. It explores respondents' roles, experience, familiarity with research and data tasks, and perceived professional-development needs.

The questionnaire has not been administered. No actual participant responses or empirical findings are represented here.

## 2. Proposed Introduction and Consent

**Survey title:** Research and Data Skills Needs Assessment

**Introduction:** This questionnaire is intended to identify areas in research and data analysis where respondents may benefit from further training. Responses would be used for the stated assessment purpose.

Participation should be voluntary. Before administering the questionnaire, the researcher must specify who is conducting the assessment, its purpose, how responses will be used, whether participation is anonymous, how data will be stored, who can access it and whom participants can contact with questions.

Do not collect names, telephone numbers, email addresses or other identifying information unless they are necessary, justified and covered by appropriate consent and data-protection arrangements.

**Proposed consent question:** I have read the information provided and voluntarily agree to participate.

- Yes
- No

For a live survey, a response of "No" should end participation.

## 3. Questionnaire Items

### Section A: Background Information

**Q1. Which option best describes your current professional role?**

Select one.

- Teacher or lecturer
- School or institutional leader
- Education programme or project staff
- Research or monitoring and evaluation staff
- Student or trainee
- Other
- Prefer not to say

**Q2. How long have you worked in your current professional area?**

Select one.

- Less than 1 year
- 1–3 years
- 4–6 years
- 7–10 years
- More than 10 years
- Not applicable

### Section B: Familiarity with Research and Data Tasks

**Instructions:** Rate your current familiarity with each task.

Use the following five-point scale:

1. Not familiar
2. Slightly familiar
3. Moderately familiar
4. Very familiar
5. Extremely familiar

**Q3. Designing questionnaires for data collection.**

**Q4. Checking datasets for missing values, duplicates and invalid entries.**

**Q5. Using Excel to organise and summarise data.**

**Q6. Calculating and interpreting frequencies, percentages and descriptive statistics.**

**Q7. Producing and interpreting cross-tabulations.**

**Q8. Selecting and interpreting charts appropriate to the data.**

**Q9. Preparing evidence-based analytical reports.**

For Q3–Q9, each response should be recorded as an integer from 1 to 5. If an item is left unanswered, it should be represented as missing rather than automatically assigned a score.

### Section C: Experience and Development Needs

**Q10. Which of the following tasks have you personally undertaken in the past 12 months?**

Select all that apply.

- Designed a questionnaire.
- Collected survey data.
- Cleaned or validated a dataset.
- Analysed quantitative data.
- Produced charts or visualisations.
- Prepared a research or evaluation report.
- Used an interactive dashboard.
- None of the above.
- Prefer not to say.

The "None of the above" option should not be combined with other selections. "Prefer not to say" should also be exclusive.

**Q11. Which one area would you most like to improve?**

Select one.

- Questionnaire design
- Data cleaning and quality assurance
- Excel and spreadsheet analysis
- Descriptive statistics
- Cross-tabulations and interpretation
- Data visualisation and dashboards
- Report and presentation writing
- Other
- Prefer not to say

**Q12. What is the main challenge you face when working with research or data?**

Optional open-ended response.

## 4. Proposed Data Dictionary

| Variable | Description | Expected values |
|---|---|---|
| respondent_id | Anonymous record identifier generated for the dataset | Unique, non-empty identifier |
| role | Professional role | One valid Q1 category |
| experience | Experience category | One valid Q2 category |
| q3_questionnaire_design | Familiarity with questionnaire design | Integer 1–5 or missing |
| q4_data_validation | Familiarity with data validation | Integer 1–5 or missing |
| q5_excel | Familiarity with Excel | Integer 1–5 or missing |
| q6_descriptive_statistics | Familiarity with descriptive statistics | Integer 1–5 or missing |
| q7_crosstabs | Familiarity with cross-tabulations | Integer 1–5 or missing |
| q8_visualisation | Familiarity with data visualisation | Integer 1–5 or missing |
| q9_reporting | Familiarity with analytical reporting | Integer 1–5 or missing |
| q10_tasks | Selected tasks from Q10 | One or more valid coded selections |
| q11_development_need | Main development need | One valid Q11 category |
| q12_challenge | Optional open-ended challenge | Text or missing |

The dataset will use one row per respondent. The Q10 multiple-response item may initially be stored as a clearly documented delimited field; the analysis code must split and count selections correctly.

The respondent identifier will be generated for the demonstration dataset and must not be treated as a real participant identifier.

## 5. Planned Validation Rules

The future validation module should check:

1. Required columns are present and unexpected columns are reported.
2. Each respondent identifier is unique and non-empty.
3. Categorical responses match the documented response options.
4. Q3–Q9 contain only integer values from 1 to 5 or explicitly recognised missing values.
5. Q10 contains only valid selections and respects exclusive options.
6. Q12 is text or missing.
7. Missing values are reported by variable and record.
8. Duplicate records are flagged for review; records should not be deleted automatically without an explicit rule.
9. Invalid values and structural errors are recorded in a data-quality report.
10. The analysis stage does not proceed silently when critical validation errors remain.

## 6. Planned Analysis

Subject to adequate data quality, the workflow may generate:

- Counts and percentages for background characteristics.
- Frequencies and distributions for Q3–Q9.
- Missing-response summaries.
- Cross-tabulations between role, experience and selected skills responses.
- Counts of Q10 task selections.
- Summaries of Q11 development needs.
- Carefully selected charts and tables.

Any composite skill score must have a documented scoring rule and a justification before it is reported. Cross-sectional self-reported familiarity must not be described as demonstrated competence or proof of training effectiveness.

## 7. Administration and Limitations

This is a proposed demonstration instrument, not a validated psychometric scale. Its clarity, relevance, accessibility and suitability should be reviewed before any real administration.

The initial portfolio dataset will be synthetic. Findings from that dataset will demonstrate software behaviour only and must not be generalised to actual educators, institutions or populations.
