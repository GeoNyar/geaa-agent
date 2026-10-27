
"""Create a consolidated Excel workbook for Survey-to-Insight.

The workbook contains descriptive outputs from synthetic demonstration
data. It must not be presented as empirical evidence about real educators.
"""

import argparse
import json
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter


TABLES = {
    "Sample Profile": "categorical_frequencies.csv",
    "Skill Statistics": "familiarity_descriptive_statistics.csv",
    "Skills by Role": "familiarity_means_by_role.csv",
    "Role Counts": "respondent_counts_by_role.csv",
    "Task Frequencies": "q10_task_frequencies.csv",
    "Response Completeness": "q12_response_completeness.csv",
}


def create_workbook(analysis_dir: Path, output_file: Path) -> Path:
    """Combine analysis CSV files and provenance information into Excel."""

    manifest_path = analysis_dir / "analysis_manifest.json"
    validation_path = analysis_dir / "validation_report.json"

    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Analysis manifest not found: {manifest_path}"
        )

    if not validation_path.exists():
        raise FileNotFoundError(
            f"Validation report not found: {validation_path}"
        )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validation = json.loads(
        validation_path.read_text(encoding="utf-8")
    )

    if manifest.get("dataset_type") != "SYNTHETIC_NOT_REAL":
        raise ValueError(
            "This workbook script is configured for the labelled "
            "synthetic demonstration dataset only."
        )

    if not validation.get("analysis_allowed", False):
        raise ValueError(
            "The validation report does not permit analysis."
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        # Clearly identify the purpose and limitations of the workbook.
        overview = pd.DataFrame(
            [
                ("Project", "Survey-to-Insight"),
                ("Dataset status", "SYNTHETIC — NOT REAL RESPONDENT DATA"),
                ("Records analysed", manifest["records_analysed"]),
                ("Validation passed", "Yes"),
                ("Generated on (UTC)", pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M UTC")),
                ("Critical validation errors",
                 manifest["critical_validation_errors"]),
                ("Validation warnings",
                 manifest["validation_warnings"]),
                ("Optional Q12 responses missing",
                 manifest["q12_missing_responses"]),
                (
                    "Interpretation limitation",
                    "Results do not describe actual educators or institutions.",
                ),
                (
                    "Causal limitation",
                    "Descriptive statistics do not establish causation.",
                ),
            ],
            columns=["Item", "Details"],
        )
        overview.to_excel(
            writer, sheet_name="Read Me", index=False
        )

        # Add each available descriptive table as a separate worksheet.
        for sheet_name, filename in TABLES.items():
            csv_path = analysis_dir / filename
            if not csv_path.exists():
                raise FileNotFoundError(
                    f"Required analysis table not found: {csv_path}"
                )

            table = pd.read_csv(csv_path)
            table.to_excel(
                writer, sheet_name=sheet_name, index=False
            )

        # Include validation details for traceability.
        validation_rows = [
            ("Dataset rows", validation.get("dataset_rows")),
            ("Dataset columns", validation.get("dataset_columns")),
            (
                "Analysis allowed",
                validation.get("analysis_allowed"),
            ),
            (
                "Critical error count",
                validation.get("critical_error_count"),
            ),
            ("Warning count", validation.get("warning_count")),
            (
                "Missing required columns",
                json.dumps(
                    validation.get("missing_required_columns", [])
                ),
            ),
            (
                "Unexpected columns",
                json.dumps(validation.get("unexpected_columns", [])),
            ),
            (
                "Errors",
                json.dumps(validation.get("errors", []), ensure_ascii=False),
            ),
            (
                "Warnings",
                json.dumps(
                    validation.get("warnings", []),
                    ensure_ascii=False,
                ),
            ),
        ]

        pd.DataFrame(
            validation_rows, columns=["Check", "Result"]
        ).to_excel(
            writer, sheet_name="Validation", index=False
        )

        # Apply simple, consistent formatting to every worksheet.
        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            worksheet.sheet_view.showGridLines = False
            worksheet.row_dimensions[1].height = 32

            for cell in worksheet[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(
                    fill_type="solid", fgColor="244062"
                )
                cell.alignment = Alignment(
                    vertical="center", wrap_text=True
                )

            for column_cells in worksheet.columns:
                max_length = max(
                    len(str(cell.value)) if cell.value is not None else 0
                    for cell in column_cells
                )
                column_letter = get_column_letter(
                    column_cells[0].column
                )
                worksheet.column_dimensions[column_letter].width = min(
                    max(max_length + 2, 12), 55
                )

            for row in worksheet.iter_rows(min_row=2):
                for cell in row:
                    cell.alignment = Alignment(
                        vertical="top", wrap_text=True
                    )
                    if isinstance(cell.value, float):
                        cell.number_format = "0.00"

            # Add a native Excel table where there is a header and data.
            # The Read Me and Validation sheets are intentionally kept as
            # key-value summaries rather than analysis tables.
            if worksheet.title not in {"Read Me", "Validation"} and worksheet.max_row > 1:
                table_ref = worksheet.dimensions
                safe_name = "".join(ch for ch in worksheet.title if ch.isalnum()) + "Table"
                excel_table = Table(displayName=safe_name[:250], ref=table_ref)
                excel_table.tableStyleInfo = TableStyleInfo(
                    name="TableStyleMedium2",
                    showFirstColumn=False,
                    showLastColumn=False,
                    showRowStripes=True,
                    showColumnStripes=False,
                )
                worksheet.add_table(excel_table)

        # Add simple native Excel charts for quick review.
        if "Skill Statistics" in writer.book.sheetnames:
            skills = writer.book["Skill Statistics"]
            if skills.max_row > 1 and skills.max_column > 1:
                chart = BarChart()
                chart.type = "bar"
                chart.style = 10
                chart.title = "Mean familiarity by skill"
                chart.y_axis.title = "Skill"
                chart.x_axis.title = "Mean rating (1–5)"
                chart.height = 7
                chart.width = 13
                chart.add_data(
                    Reference(skills, min_col=2, min_row=1, max_row=skills.max_row),
                    titles_from_data=True,
                )
                chart.set_categories(
                    Reference(skills, min_col=1, min_row=2, max_row=skills.max_row)
                )
                skills.add_chart(chart, "K2")

        if "Role Counts" in writer.book.sheetnames:
            roles = writer.book["Role Counts"]
            if roles.max_row > 1 and roles.max_column > 1:
                chart = BarChart()
                chart.type = "bar"
                chart.style = 11
                chart.title = "Synthetic records by role"
                chart.y_axis.title = "Professional role"
                chart.x_axis.title = "Record count"
                chart.height = 7
                chart.width = 13
                chart.add_data(
                    Reference(roles, min_col=2, min_row=1, max_row=roles.max_row),
                    titles_from_data=True,
                )
                chart.set_categories(
                    Reference(roles, min_col=1, min_row=2, max_row=roles.max_row)
                )
                roles.add_chart(chart, "D2")

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Create a consolidated Survey-to-Insight workbook."
    )
    parser.add_argument(
        "--analysis-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "analysis_outputs",
        help="Folder containing analysis CSV files and JSON reports.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent
        / "analysis_outputs"
        / "survey_to_insight_workbook.xlsx",
        help="Destination Excel workbook path.",
    )
    args = parser.parse_args()

    output = create_workbook(args.analysis_dir, args.output)
    print("Excel workbook created successfully.")
    print("Dataset status: SYNTHETIC_NOT_REAL")
    print(f"Workbook: {output.resolve()}")


if __name__ == "__main__":
    main()
