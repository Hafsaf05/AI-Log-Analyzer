"""
parser.py
---------
Reads a log file and extracts ERROR and WARNING entries.
Returns a structured list of issues for downstream AI analysis.
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class LogEntry:
    """Represents a single parsed log issue."""
    level: str        # ERROR or WARNING
    timestamp: str
    message: str
    line_number: int


# Line Macthing
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>ERROR|WARNING)\s+"
    r"(?P<message>.+)$"
)


def parse_log_file(filepath: str) -> List[LogEntry]:
    """
    Reads a log file line-by-line and returns all ERROR and WARNING entries.

    Args:
        filepath: Path to the .txt log file.

    Returns:
        A list of LogEntry objects, one per matched line.

    Raises:
        FileNotFoundError: If the log file does not exist.
    """
    entries: List[LogEntry] = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            match = LOG_PATTERN.match(line)
            if match:
                entries.append(LogEntry(
                    level=match.group("level"),
                    timestamp=match.group("timestamp"),
                    message=match.group("message"),
                    line_number=line_number,
                ))

    return entries


def summarize_entries(entries: List[LogEntry]) -> dict:
    """Returns a quick count summary of errors vs warnings."""
    return {
        "total": len(entries),
        "errors": sum(1 for e in entries if e.level == "ERROR"),
        "warnings": sum(1 for e in entries if e.level == "WARNING"),
    }
