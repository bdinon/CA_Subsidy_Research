#!/usr/bin/env python3
"""
Builds output/subsidy_matrix.xlsx and output/subsidy_report.md from data/programs.json.

Usage: python scripts/build_report.py
Requires: pip install pandas openpyxl
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import date

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
PROGRAMS_PATH = ROOT / "data" / "programs.json"
JURISDICTIONS_PATH = ROOT / "data" / "jurisdictions.json"
OUTPUT_DIR = ROOT / "output"

COLUMN_ORDER = [
    "program_name",
    "level",
    "jurisdiction",
    "county_tag",
    "administering_agency",
    "funding_type",
    "typical_award_size",
    "per_unit_cap",
    "affordability_requirement",
    "eligible_project_types",
    "application_cycle",
    "cycle_notes",
    "next_deadline_date",
    "next_deadline",
    "deadline_check",
    "prevailing_wage_trigger",
    "layering_notes",
    "confidence",
    "link_status",
    "last_audited",
    "audit_note",
    "source_url",
    "date_researched",
]

HEADER_LABELS = {
    "program_name": "Program",
    "level": "Level",
    "jurisdiction": "Jurisdiction",
    "county_tag": "County",
    "administering_agency": "Administering Agency",
    "funding_type": "Funding Type",
    "typical_award_size": "Typical Award",
    "per_unit_cap": "Per-Unit Cap",
    "affordability_requirement": "AMI Requirement",
    "eligible_project_types": "Eligible Project Types",
    "application_cycle": "Application Cycle",
    "cycle_notes": "Cycle Notes",
    "next_deadline_date": "Next Deadline Date",
    "next_deadline": "Next Deadline (text)",
    "deadline_check": "Deadline Check",
    "link_status": "Link Status",
    "last_audited": "Last Audited",
    "audit_note": "Audit Note",
    "prevailing_wage_trigger": "Prevailing Wage?",
    "layering_notes": "Layering Notes",
    "confidence": "Confidence",
    "source_url": "Source",
    "date_researched": "Last Researched",
}


def load_data():
    with open(PROGRAMS_PATH, encoding="utf-8") as f:
        programs = json.load(f)
    jurisdictions = {}
    if JURISDICTIONS_PATH.exists():
        with open(JURISDICTIONS_PATH, encoding="utf-8") as f:
            jurisdictions = json.load(f)
    return programs, jurisdictions


def normalize_record(r):
    row = {}
    for col in COLUMN_ORDER:
        val = r.get(col, "")
        if isinstance(val, list):
            val = ", ".join(val)
        if isinstance(val, bool):
            val = "Yes" if val else "No"
        row[col] = val if val is not None else ""
    return row


def build_xlsx(programs):
    OUTPUT_DIR.mkdir(exist_ok=True)
    xlsx_path = OUTPUT_DIR / "subsidy_matrix.xlsx"

    if not programs:
        df = pd.DataFrame(columns=[HEADER_LABELS[c] for c in COLUMN_ORDER])
        df.to_excel(xlsx_path, sheet_name="All Programs", index=False)
        return xlsx_path

    rows = [normalize_record(r) for r in programs]
    df = pd.DataFrame(rows, columns=COLUMN_ORDER).rename(columns=HEADER_LABELS)

    level_order = {"state": 0, "county": 1, "city": 2, "federal": 1, "private": 3}
    df["_sort"] = df["Level"].map(lambda x: level_order.get(x, 9))
    df = df.sort_values(["_sort", "Jurisdiction", "Program"]).drop(columns="_sort")

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="All Programs", index=False)
        for level in ["state", "county", "city", "private"]:
            sub = df[df["Level"] == level]
            if not sub.empty:
                sheet_name = level.capitalize() + " Level"
                sub.to_excel(writer, sheet_name=sheet_name[:31], index=False)

        # Subsidy sources only (excludes requirements, designations, negative findings)
        money = {"tax credit", "bond", "grant", "loan", "rental assistance", "land",
                 "tax abatement", "fee waiver"}
        src = df[df["Funding Type"].isin(money)]
        if not src.empty:
            src.to_excel(writer, sheet_name="Funding Sources Only", index=False)

        # Upcoming deadlines, next 120 days
        dl = df[(df["Deadline Check"] == "future_date") & (df["Next Deadline Date"] != "")].copy()
        if not dl.empty:
            dl["_d"] = pd.to_datetime(dl["Next Deadline Date"], errors="coerce")
            cutoff = pd.Timestamp(date.today()) + pd.Timedelta(days=120)
            dl = dl[(dl["_d"] >= pd.Timestamp(date.today())) & (dl["_d"] <= cutoff)]
            dl = dl.sort_values("_d").drop(columns="_d")
            if not dl.empty:
                dl.to_excel(writer, sheet_name="Deadlines 120d", index=False)

        nc = df[df["Confidence"] == "needs_confirmation"]
        if not nc.empty:
            nc.to_excel(writer, sheet_name="Needs Confirmation", index=False)

        summ = (df.groupby(["County", "Funding Type"]).size().unstack(fill_value=0))
        summ["Total"] = summ.sum(axis=1)
        summ.to_excel(writer, sheet_name="Summary by County")

    _format_workbook(xlsx_path)
    return xlsx_path


def _format_workbook(xlsx_path):
    wb = load_workbook(xlsx_path)
    header_font = Font(name="Arial", bold=True, color="FFFFFF", size=10)
    header_fill = PatternFill(start_color="1F4E5F", end_color="1F4E5F", fill_type="solid")
    body_font = Font(name="Arial", size=10)
    wrap_align = Alignment(wrap_text=True, vertical="top")

    widths = {
        "Program": 28, "Level": 10, "Jurisdiction": 20, "County": 16,
        "Administering Agency": 26, "Funding Type": 16, "Typical Award": 20,
        "Per-Unit Cap": 16, "AMI Requirement": 22, "Eligible Project Types": 24,
        "Application Cycle": 16, "Cycle Notes": 34, "Next Deadline Date": 14,
        "Next Deadline (text)": 34, "Deadline Check": 14, "Link Status": 12,
        "Last Audited": 14, "Audit Note": 30, "Prevailing Wage?": 14,
        "Layering Notes": 40, "Confidence": 16, "Source": 30, "Last Researched": 14,
    }

    for sheet in wb.worksheets:
        max_row = sheet.max_row
        max_col = sheet.max_column
        for col_idx in range(1, max_col + 1):
            cell = sheet.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        for row_idx in range(2, max_row + 1):
            for col_idx in range(1, max_col + 1):
                cell = sheet.cell(row=row_idx, column=col_idx)
                cell.font = body_font
                cell.alignment = wrap_align
        for col_idx in range(1, max_col + 1):
            header_val = sheet.cell(row=1, column=col_idx).value
            sheet.column_dimensions[get_column_letter(col_idx)].width = widths.get(header_val, 18)
        sheet.freeze_panes = "A2"

    wb.save(xlsx_path)


def build_markdown_report(programs, jurisdictions):
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "subsidy_report.md"

    by_level = defaultdict(list)
    for r in programs:
        by_level[r.get("level", "unknown")].append(r)

    counties_in_scope = [c["county"] for c in jurisdictions.get("counties", [])]

    lines = []
    lines.append("# Affordable Housing Subsidy Source Report")
    lines.append(f"\nGenerated {date.today().isoformat()}, {len(programs)} total records\n")
    lines.append(f"**Counties in scope:** {', '.join(counties_in_scope) if counties_in_scope else 'none configured yet'}\n")

    level_titles = {
        "state": "State-Level Programs (California, statewide)",
        "county": "County-Level Programs",
        "city": "City-Level Programs",
        "private": "Private & Philanthropic Sources",
        "federal": "Federal Programs",
    }

    for level in ["state", "county", "city", "private", "federal"]:
        records = by_level.get(level, [])
        if not records:
            continue
        lines.append(f"\n## {level_titles.get(level, level.title())}\n")

        by_juris = defaultdict(list)
        for r in records:
            by_juris[r.get("jurisdiction", "Unknown")].append(r)

        for juris in sorted(by_juris.keys()):
            lines.append(f"\n### {juris}\n")
            for r in sorted(by_juris[juris], key=lambda x: x.get("program_name", "")):
                lines.append(f"**{r.get('program_name', 'Unnamed program')}**")
                lines.append(f"- Agency: {r.get('administering_agency', 'unknown')}")
                lines.append(f"- Type: {r.get('funding_type', 'unknown')}")
                if r.get("typical_award_size"):
                    lines.append(f"- Typical award: {r.get('typical_award_size')}")
                if r.get("affordability_requirement"):
                    lines.append(f"- AMI requirement: {r.get('affordability_requirement')}")
                lines.append(f"- Cycle: {r.get('application_cycle', 'unknown')}"
                             + (f" (next: {r.get('next_deadline')})" if r.get("next_deadline") else ""))
                if r.get("layering_notes"):
                    lines.append(f"- Layering notes: {r.get('layering_notes')}")
                lines.append(f"- Source: {r.get('source_url', 'none')}")
                lines.append(f"- Confidence: {r.get('confidence', 'unknown')} (researched {r.get('date_researched', 'unknown')})")
                lines.append("")

    lines.append("\n## Coverage Check\n")
    researched_counties = set(r.get("county_tag") for r in programs if r.get("level") in ("county", "city"))
    missing = [c for c in counties_in_scope if c not in researched_counties]
    if missing:
        lines.append(f"No county/city-level records yet for: {', '.join(missing)}")
    else:
        lines.append("All configured counties have at least one county or city-level record.")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    programs, jurisdictions = load_data()
    xlsx_path = build_xlsx(programs)
    md_path = build_markdown_report(programs, jurisdictions)
    print(f"Wrote {xlsx_path}")
    print(f"Wrote {md_path}")
    print(f"Total records: {len(programs)}")


if __name__ == "__main__":
    main()
