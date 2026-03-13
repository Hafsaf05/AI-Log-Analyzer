"""
app.py
------
Main entry point for AI Log Analyzer.

Pipeline:
    Read log file -> Parse errors/warnings -> Analyze with LLM -> Generate report

Usage:
    python app.py                          # uses default sample log
    python app.py --log path/to/app.log    # custom log file
    python app.py --save                   # also saves report to reports/
"""

import argparse
import os
import sys

# Fix: ensure the project root folder is always on Python's module search path.
# This makes 'from src.xxx import ...' work no matter where you run the script from.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
from src.parser import parse_log_file, summarize_entries
from src.analyzer import analyze_logs
from src.report_generator import generate_report

# Load GROQ_API_KEY from .env file
load_dotenv()


def main():
    # -- CLI Arguments ---------------------------------------------------------
    parser = argparse.ArgumentParser(description="AI Log Analyzer & Bug Report Generator")
    parser.add_argument(
        "--log",
        default="logs/sample_log.txt",
        help="Path to the log file to analyze (default: logs/sample_log.txt)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the generated report to the reports/ directory",
    )
    parser.add_argument(
        "--model",
        default="llama-3.3-70b-versatile",
        help="Groq model to use for analysis (default: llama-3.3-70b-versatile)",
    )
    args = parser.parse_args()

    #  Validate API Key
    if not os.getenv("GROQ_API_KEY"):
        print("[x] Error: GROQ_API_KEY not found.")
        print("    1. Get a free key at: https://console.groq.com")
        print("    2. Create a .env file in this folder with: GROQ_API_KEY=your-key-here")
        sys.exit(1)

    # Parse 
    # Resolve log path relative to the project root, not the shell's cwd
    log_path = os.path.join(ROOT_DIR, args.log) if not os.path.isabs(args.log) else args.log
    print(f"\n[1/3] Parsing log file: {log_path}")
    try:
        entries = parse_log_file(log_path)
    except FileNotFoundError:
        print(f"[x] Log file not found: {log_path}")
        sys.exit(1)

    summary = summarize_entries(entries)
    print(f"      Found {summary['errors']} error(s) and {summary['warnings']} warning(s).")

    #Analyze 
    print(f"[2/3] Sending issues to LLM ({args.model}) for analysis...")
    ai_analysis = analyze_logs(entries, model=args.model)
    print("      Analysis complete.")

    # GeneratING Report 
    print("[3/3] Generating bug report...")
    output_path = None
    if args.save:
        reports_dir = os.path.join(ROOT_DIR, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(reports_dir, f"bug_report_{timestamp}.txt")

    report = generate_report(
        entries=entries,
        ai_analysis=ai_analysis,
        log_filepath=args.log,
        output_filepath=output_path,
    )

    # final report to stdout
    print("\n" + report)


if __name__ == "__main__":
    main()