# Research and Data Skills Needs Assessment

**Status:** Draft instrument for review; not yet validated or administered.

## Purpose

This questionnaire is designed to explore respondents’ self-reported familiarity with selected research and data skills, their experience performing related tasks, and their perceived professional development needs.

The instrument is intended for a demonstration of the GEAA Survey-to-Insight workflow. Any responses collected in a future exercise must be handled separately from the synthetic dataset used to test the software.

## Participant information

Participation should be voluntary. Before administering this questionnaire, the researcher should provide an appropriate information statement explaining the purpose, intended use of responses, confidentiality arrangements, data retention, and contact details for questions.

Do not collect names, personal identification numbers, or other directly identifying information unless there is a clear, justified need and appropriate safeguards.

## Section A: Background information

### Q1. Which option best describes your current professional role?

*Select one.*

- Teacher or lecturer
- School or institutional leader
- Education programme or project staff
- Research or monitoring and evaluation staff
- Student or trainee
- Other
- Prefer not to say

**Data field:** `role`

### Q2. How long have you worked in education or a related field?

*Select one.*

- Less than 1 year
- 1–3 years
- 4–6 years
- 7–10 years
- More than 10 years
- Not applicable

**Data field:** `experience`

## Section B: Familiarity with research and data skills

### Instructions

For each area below, indicate how familiar you are with the skill. This is a self-assessment, not a test of competence.

Use the same scale for Q3–Q9:

1. Not familiar
2. Slightly familiar
3. Moderately familiar
4. Very familiar
5. Extremely familiar

If a platform permits unanswered items, respondents should be able to leave an item blank when they cannot provide a response.

### Q3. Designing questionnaires

How familiar are you with designing questionnaire items and response options for a research or evaluation exercise?

**Data field:** `q3_questionnaire_design`

### Q4. Data validation and quality assurance

How familiar are you with checking survey data for missing values, invalid responses, inconsistencies, and duplicate records?

**Data field:** `q4_data_validation`

### Q5. Excel and spreadsheet analysis

How familiar are you with using Excel or similar spreadsheet tools to organise, summarise, and examine data?

**Data field:** `q5_excel`

### Q6. Descriptive statistics

How familiar are you with interpreting frequencies, percentages, means, and measures of variation?

**Data field:** `q6_descriptive_statistics`

### Q7. Cross-tabulations

How familiar are you with comparing categories using cross-tabulations or contingency tables and interpreting the resulting patterns?

**Data field:** `q7_crosstabs`

### Q8. Data visualisation

How familiar are you with selecting and interpreting charts, graphs, or dashboards to communicate findings?

**Data field:** `q8_visualisation`

### Q9. Analytical reporting

How familiar are you with presenting data findings in a clear written report for research, evaluation, or decision-making?

**Data field:** `q9_reporting`

## Section C: Previous experience and development needs

### Q10. Which of the following activities have you personally undertaken during the past 12 months?

*Select all that apply. Select “None of the above” or “Prefer not to say” alone.*

- Designed a questionnaire
- Collected survey data
- Cleaned or validated a dataset
- Analysed quantitative data
- Produced charts or visualisations
- Prepared a research or evaluation report
- Used an interactive dashboard
- None of the above
- Prefer not to say

**Data field:** `q10_tasks`

### Q11. Which ONE area would you most like to develop at present?

*Select one.*

- Questionnaire design
- Data cleaning and quality assurance
- Excel and spreadsheet analysis
- Descriptive statistics
- Cross-tabulations and interpretation
- Data visualisation and dashboards
- Report and presentation writing
- Other
- Prefer not to say

**Data field:** `q11_development_need`

### Q12. What is the main challenge you face when working with research or data?

*Optional open-ended response. Please do not include names or confidential information.*

**Data field:** `q12_challenge`

## Notes for data management and analysis

- Q1 and Q2 are single-choice categorical items.
- Q3–Q9 use a five-point self-reported familiarity scale. These ratings should not automatically be interpreted as objective measures of skill or competence.
- Q10 is a multiple-response item. When exported to CSV for the current demonstration workflow, selected responses must be stored in one field and separated by semicolons.
- Q11 is a single-choice item.
- Q12 is optional free text. Blank responses should remain missing rather than being treated as evidence that a respondent has no challenge.
- The existing demonstration data use a generated `respondent_id`. This is a processing identifier, not a questionnaire item. Real respondent identifiers should be handled according to the approved data-management plan.
- The current analysis is descriptive. It does not establish causal relationships or support generalisation from synthetic records to real educators.
- This draft has not undergone formal content validation, piloting, or reliability assessment.

## Before administration

Review the wording and response options for relevance to the intended population. Check accessibility, estimated completion time, voluntary participation, privacy, and any institutional ethical-review or authorisation requirements. Pilot the instrument before wider use and document any revisions.

