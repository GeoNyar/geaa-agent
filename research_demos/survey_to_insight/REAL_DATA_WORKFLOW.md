# Real Survey Data Workflow: Design and Safeguards

## Status

**Planned — not implemented.**

The existing Survey-to-Insight synthetic-data workflow remains unchanged. This document specifies safeguards to be considered before supporting real survey data.

## 1. Purpose

The proposed pathway will allow authorised survey data to be imported, validated and analysed separately from the synthetic demonstration dataset.

It will not collect survey responses or establish that an uploaded dataset is authentic. Dataset classification must be supported by documented source information.

## 2. Proposed processing sequence

1. Obtain an authorised CSV or Excel export from an approved data-collection process.
2. Record the dataset source, acquisition date and intended analytical purpose without unnecessarily recording personal information.
3. Classify the input explicitly as real survey data or synthetic demonstration data.
4. Check the file format, required columns, response categories, missingness and rating ranges.
5. Review the dataset for direct identifiers and unnecessary sensitive information before processing.
6. Produce a validation report that identifies issues without silently deleting, correcting or imputing responses.
7. Permit descriptive analysis only after the applicable validation checks have passed.
8. Label every output with its source classification, processing details and analytical limitations.
9. Store real-data outputs in an appropriately controlled location. Do not publish respondent-level data, identifying information or confidential reports in the public repository.

## 3. Reuse of existing validation rules

The existing `validate_data.py` module provides a starting point for checking required columns, categories, familiarity scores, missing values, duplicate identifiers and multiple-response selections.

Before using it with real data, the implementation must be reviewed for privacy-safe reporting. Error messages and validation reports should not unnecessarily expose respondent identifiers or actual response values.

A successful validation result indicates compliance with the implemented checks. It does not prove that a dataset is authentic, representative, ethically collected or suitable for every research question.

## 4. Dataset classification and provenance

The future implementation should record:

- Dataset classification.
- Source description and acquisition date.
- Input schema and validation outcome.
- Processing date and analysis version.
- Output locations and relevant limitations.

Classification must be explicitly supplied and recorded. A label alone must not be treated as proof of authenticity.

Synthetic test records must remain distinguishable from real participant responses throughout processing, reporting and storage.

## 5. Privacy and responsible data handling

Before processing real responses:

- Review the dataset for names, contact details, identification numbers and other unnecessary identifiers.
- Establish appropriate access controls, storage, retention and deletion arrangements.
- Review applicable ethical approval, consent and data-protection requirements.
- Avoid placing real participant data in public repositories, source-control history, public workflow logs or public downloadable artifacts.
- Use fabricated test records for automated tests.
- Keep any real-data analysis outputs in an appropriately controlled environment.

## 6. Separate testing

The real-data import pathway should have its own tests for:

- Valid CSV and Excel imports.
- Missing required columns.
- Invalid categories and out-of-range scores.
- Missing and duplicate identifiers.
- Malformed multiple-response selections.
- Privacy-safe validation reports.
- Refusal to proceed when critical validation checks fail.
- Correct labelling of source classification and generated outputs.

These tests should use fabricated data rather than actual participant records.

## 7. Implementation boundary

This document is a design specification, not evidence that a real-data import pathway exists.

The existing synthetic generator, analysis scripts, tests and GitHub Actions workflow should remain intact until a separately tested implementation is ready.

Any future real-data pathway must be reviewed and tested before being used with actual participant data.
