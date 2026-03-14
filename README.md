# AI Log Analyzer — LLM Powered Automated Debugging System

AI-powered log analyzer that parses application logs and uses the Llama-3 model via the Groq API to generate automated debugging reports with root cause analysis and suggested fixes.

The system automatically detects errors and warnings from raw application logs and produces structured bug reports that help engineers quickly identify the root cause of failures.

---

## System Architecture

           +---------------------+
           |   Application Logs  |
           +----------+----------+
                      |
                      v
            +------------------+
            |    Log Parser     |
            | Extract errors &  |
            | warnings from log |
            +---------+--------+
                      |
                      v
            +------------------+
            |  Error Detector   |
            | Categorizes logs  |
            +---------+--------+
                      |
                      v
           +----------------------+
           | LLM Debug Analyzer   |
           | (Llama-3 via Groq)   |
           | Root cause analysis  |
           +----------+-----------+
                      |
                      v
           +----------------------+
           | Bug Report Generator |
           | Structured report    |
           +----------------------+

---

## Features

• Automatic log parsing and error detection  
• AI-powered root cause analysis using Llama-3  
• Generates structured debugging reports  
• Detects system health issues from logs  
• Helps engineers quickly identify failures  

---

## Installation

Clone the repository

git clone https://github.com/Hafsaf05/AI-Log-Analyzer.git
cd AI-Log-Analyzer

Install dependencies

pip install -r requirements.txt


## Usage

Run the analyzer on the sample log file:

python app.py

To analyze a custom log file:

python app.py --log path/to/logfile.txt

To save the generated bug report:

python app.py --save

## Example Output

AI LOG ANALYZER — BUG REPORT

Issues : 6 errors, 6 warnings

Root Cause:
Configuration issues and dependency injection failures

Severity:
High

Suggested Fix:
Review configuration files and dependency injection setup.




