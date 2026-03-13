"""
analyzer.py
-----------
Sends extracted log issues to an LLM via LangChain + Groq.
The model identifies root causes, severity, and suggested fixes
for each detected error or warning group.

Groq provides free, fast inference on models like llama-3.3-70b-versatile.
Get a free API key at: https://console.groq.com
"""

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import List
from .parser import LogEntry


# instructs the LLM to act as a senior debugging engineer
ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a senior software engineer specializing in debugging and root cause analysis. "
            "Analyze the provided log errors and warnings, then respond in the following structured format:\n\n"
            "**Root Cause:** <concise explanation of what likely caused these errors>\n"
            "**Severity:** <Critical / High / Medium / Low — with one-line justification>\n"
            "**Affected Components:** <list the services or modules involved>\n"
            "**Suggested Fixes:**\n"
            "  1. <first actionable step>\n"
            "  2. <second actionable step>\n"
            "  3. <third actionable step if applicable>\n\n"
            "Be specific, technical, and concise. Do not repeat the log lines verbatim."
        ),
    ),
    (
        "human",
        "Here are the log issues detected:\n\n{log_entries}\n\nProvide your analysis.",
    ),
])


def _format_entries_for_prompt(entries: List[LogEntry]) -> str:
    """Formats log entries into a clean numbered list for the LLM prompt."""
    lines = []
    for i, entry in enumerate(entries, start=1):
        lines.append(f"{i}. [{entry.level}] {entry.timestamp} — {entry.message}")
    return "\n".join(lines)


def analyze_logs(entries: List[LogEntry], model: str = "llama-3.3-70b-versatile", temperature: float = 0.2) -> str:
    """
    Sends log entries to Groq's LLM and returns a structured analysis string.

    Args:
        entries:     List of parsed LogEntry objects (errors + warnings).
        model:       Groq model name to use (default: llama-3.3-70b-versatile).
        temperature: Lower = more deterministic/factual responses.

    Returns:
        The LLM's analysis as a plain string.
    """
    if not entries:
        return "No errors or warnings detected. System appears healthy."

    # Build the LangChain pipeline: prompt → Groq LLM → string output
    llm = ChatGroq(model=model, temperature=temperature)
    chain = ANALYSIS_PROMPT | llm | StrOutputParser()

    formatted = _format_entries_for_prompt(entries)
    analysis = chain.invoke({"log_entries": formatted})
    return analysis