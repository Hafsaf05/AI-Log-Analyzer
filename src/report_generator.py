"""
report_generator.py
-------------------
Takes parsed log entries and the LLM's analysis,
then assembles a clean, human-readable bug report.
Optionally saves the report to a file.
"""

from datetime import datetime
from typing import List
from .parser import LogEntry, summarize_entries


def generate_report(
    entries: List[LogEntry],
    ai_analysis: str,
    log_filepath: str,
    output_filepath: str = None,
) -> str:
    """
    Builds the full bug report string from log issues and AI analysis.

    Args:
        entries:        Parsed LogEntry list (errors + warnings).
        ai_analysis:    The analysis string returned by the LLM.
        log_filepath:   Original log file path (shown in report header).
        output_filepath: If provided, saves the report to this .txt path.

    Returns:
        The full report as a formatted string.
    """
    summary = summarize_entries(entries)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #  Header 
    lines = [
        "=" * 60,
        "          AI LOG ANALYZER — BUG REPORT",
        "=" * 60,
        f"  Generated : {timestamp}",
        f"  Log File  : {log_filepath}",
        f"  Issues    : {summary['errors']} error(s), {summary['warnings']} warning(s)",
        "=" * 60,
        "",
    ]

    #  Detected Issues
    lines.append("── DETECTED ISSUES ──────────────────────────────────────")
    lines.append("")

    errors = [e for e in entries if e.level == "ERROR"]
    warnings = [e for e in entries if e.level == "WARNING"]

    if errors:
        lines.append("  ERRORS:")
        for e in errors:
            lines.append(f"    [Line {e.line_number:>3}] {e.timestamp}  {e.message}")
        lines.append("")

    if warnings:
        lines.append("  WARNINGS:")
        for w in warnings:
            lines.append(f"    [Line {w.line_number:>3}] {w.timestamp}  {w.message}")
        lines.append("")

    # AI Analysis
    lines.append("── AI ANALYSIS ──────────────────────────────────────────")
    lines.append("")
    # Indent TO each line of the AI response for readability
    for ai_line in ai_analysis.splitlines():
        lines.append(f"  {ai_line}")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  End of Report")
    lines.append("=" * 60)

    report = "\n".join(lines)

    # Optionally persist to disk
    if output_filepath:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[✓] Report saved to: {output_filepath}")

    return report