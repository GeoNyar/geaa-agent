"""Reproducible descriptive analysis of Kenya's secondary enrolment indicator.

Source: World Bank WDI indicator SE.SEC.ENRR (source metadata: UNESCO UIS).
This script downloads real open data at runtime; no observations are fabricated.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
START_YEAR, END_YEAR = 2000, 2023
SOURCE_URL = (
    "https://api.worldbank.org/v2/country/KEN/indicator/SE.SEC.ENRR"
    f"?date={START_YEAR}:{END_YEAR}&format=json&per_page=100"
)
INDICATOR_CODE = "SE.SEC.ENRR"


def retrieve_data() -> tuple[pd.DataFrame, dict]:
    request = Request(SOURCE_URL, headers={"User-Agent": "GEAA-education-research-demo/1.0"})
    with urlopen(request, timeout=45) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise ValueError("Unexpected World Bank API response; expected metadata and observations.")

    rows = []
    for item in payload[1]:
        rows.append({
            "country": item.get("country", {}).get("value"),
            "country_code": item.get("countryiso3code"),
            "indicator_code": item.get("indicator", {}).get("id"),
            "indicator": item.get("indicator", {}).get("value"),
            "year": int(item["date"]),
            "value": item.get("value"),
            "unit": item.get("unit"),
            "obs_status": item.get("obs_status"),
            "decimal": item.get("decimal"),
        })
    data = pd.DataFrame(rows)
    if data.empty:
        raise ValueError("The API returned no observations for the requested period.")
    if data["indicator_code"].dropna().ne(INDICATOR_CODE).any():
        raise ValueError("API response contains an unexpected indicator code.")
    if data["country_code"].dropna().ne("KEN").any():
        raise ValueError("API response contains an unexpected country.")
    if data["year"].duplicated().any():
        raise ValueError("Duplicate years found in the API response.")
    if not data["year"].between(START_YEAR, END_YEAR).all():
        raise ValueError("Returned years fall outside the requested period.")

    metadata = {
        "dataset_classification": "REAL_OPEN_DATA",
        "publisher": "World Bank, World Development Indicators",
        "source_organisation_in_indicator_metadata": "UNESCO Institute for Statistics (UIS)",
        "indicator_code": INDICATOR_CODE,
        "indicator_name": "School enrollment, secondary (% gross)",
        "country": "Kenya",
        "country_code": "KEN",
        "requested_start_year": START_YEAR,
        "requested_end_year": END_YEAR,
        "source_url": SOURCE_URL,
        "indicator_page": "https://data.worldbank.org/indicator/SE.SEC.ENRR?locations=KE",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "api_response_metadata": payload[0],
        "interpretation_limit": (
            "Gross enrolment ratio is not a direct measure of attendance, completion, learning, or quality."
        ),
    }
    return data.sort_values("year").reset_index(drop=True), metadata


def analyse(data: pd.DataFrame, metadata: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_DIR / "kenya_secondary_enrolment_raw.csv", index=False)

    expected_years = set(range(START_YEAR, END_YEAR + 1))
    observed_years = set(data["year"].astype(int))
    missing_years = sorted(expected_years - observed_years)
    nonmissing = data.dropna(subset=["value"]).sort_values("year")

    summary = {
        "dataset_classification": "REAL_OPEN_DATA",
        "indicator_code": INDICATOR_CODE,
        "requested_period": f"{START_YEAR}-{END_YEAR}",
        "api_rows_returned": int(len(data)),
        "nonmissing_values": int(data["value"].notna().sum()),
        "missing_value_count": int(data["value"].isna().sum()),
        "years_not_returned_by_api": missing_years,
        "first_available_year": int(nonmissing.iloc[0]["year"]) if not nonmissing.empty else None,
        "first_available_value": float(nonmissing.iloc[0]["value"]) if not nonmissing.empty else None,
        "latest_available_year": int(nonmissing.iloc[-1]["year"]) if not nonmissing.empty else None,
        "latest_available_value": float(nonmissing.iloc[-1]["value"]) if not nonmissing.empty else None,
        "difference_latest_minus_first_percentage_points": (
            round(float(nonmissing.iloc[-1]["value"] - nonmissing.iloc[0]["value"]), 3)
            if len(nonmissing) >= 2 else None
        ),
        "no_interpolation_performed": True,
        "causal_inference": "Not performed",
    }
    pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "summary.csv", index=False)
    (OUTPUT_DIR / "provenance.json").write_text(
        json.dumps({**metadata, **summary}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(data["year"], data["value"], marker="o", linewidth=2)
    ax.set_title("Kenya: gross secondary-school enrolment ratio")
    ax.set_xlabel("Year")
    ax.set_ylabel("Enrolment ratio (% gross)")
    ax.grid(True, alpha=0.25)
    ax.set_xticks(list(range(START_YEAR, END_YEAR + 1, 2)))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "kenya_secondary_enrolment_trend.png", dpi=180)
    plt.close(fig)

    if nonmissing.empty:
        trend_text = "No non-missing values were returned; no trend could be described."
    else:
        first = nonmissing.iloc[0]
        last = nonmissing.iloc[-1]
        trend_text = (
            f"The earliest available observation in the requested period was "
            f"{first['value']:.2f}% in {int(first['year'])}; the latest was "
            f"{last['value']:.2f}% in {int(last['year'])}. The descriptive difference "
            f"between those observations was {last['value'] - first['value']:.2f} "
            "percentage points. This is not a causal estimate."
        )

    report = f"""# Kenya Secondary Enrolment: Open-Data Analysis

**Classification:** REAL OPEN DATA  
**Indicator:** {INDICATOR_CODE} — School enrollment, secondary (% gross)  
**Requested period:** {START_YEAR}–{END_YEAR}  
**Retrieved (UTC):** {metadata['retrieved_at_utc']}

## Research question

How did Kenya's reported gross secondary-school enrolment ratio vary across available annual observations from {START_YEAR} to {END_YEAR}?

## Descriptive result

{trend_text}

- API rows returned: {summary['api_rows_returned']}
- Non-missing values: {summary['nonmissing_values']}
- Missing values among returned rows: {summary['missing_value_count']}
- Requested years not returned by the API: {', '.join(map(str, missing_years)) if missing_years else 'None'}

## Interpretation

The gross enrolment ratio compares total enrolment, regardless of age, with the population of the official age group for the education level. It can exceed 100% and should not be interpreted as the proportion of age-appropriate children attending school. It is not a direct measure of completion, learning outcomes, or education quality.

This is a national-level descriptive trend. It cannot reveal county-level or within-county spatial inequality, explain why values changed, or establish causal effects. Missing years were not interpolated.

## Data provenance

- Publisher: World Bank, World Development Indicators.
- Source organisation identified in indicator metadata: UNESCO Institute for Statistics (UIS).
- API URL: {SOURCE_URL}
- Indicator page: https://data.worldbank.org/indicator/SE.SEC.ENRR?locations=KE
- Retrieved at: {metadata['retrieved_at_utc']}

See `kenya_secondary_enrolment_raw.csv`, `summary.csv`, and `provenance.json` for the data and processing record.
"""
    (OUTPUT_DIR / "case_study_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    data, metadata = retrieve_data()
    analyse(data, metadata)
    print("Open-data case study completed.")
    print("Dataset classification: REAL_OPEN_DATA")
    print(f"Outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
