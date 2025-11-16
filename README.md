markdown
# ACME Payments Transaction Processor

A Python application for processing, cleaning, and summarizing transaction data from CSV files.

## Installation

1. Ensure Python 3.8+ is installed on your system
2. Clone this repository
3. Install dependencies:
```bash
pip install -r requirements.txt

Usage
Run the application with a CSV file:

bash
python main.py data/sample_transactions.csv

AI Usage Disclosure
Tools Used:
ChatGPT for code conversion and debugging assistance

Prompts Used:
"Convert this TypeScript/Node.js transaction processor to Python with class structure"

"How to handle Python imports and module structure for a CSV processing application?"

"Python pandas equivalent for TypeScript array operations and data filtering"

"Debugging Python installation and dependency issues with pandas and pytest"

"Convert TypeScript interface definitions to Python classes with validation"

"Python equivalent of TypeScript's date parsing and currency formatting"

"How to structure Python unit tests similar to Jest testing patterns"

"Python error handling and exception patterns for file processing"

Conversion Details:
Original TypeScript Architecture:

TransactionProcessor class with methods for reading CSV, cleaning data, and generating reports

Transaction interface defining the data structure

ValidationResult type for error tracking

Jest tests with mocking for file operations

Python Implementation Approach:

Created TransactionProcessor class mirroring the TypeScript structure

Used dataclasses for Transaction data structure instead of TypeScript interfaces

Replaced TypeScript's array methods with pandas DataFrame operations

Converted Jest tests to pytest with similar test cases and mocking

Maintained the same separation of concerns and error handling patterns

Key Conversion Challenges:

TypeScript's strong typing vs Python's dynamic typing - used type hints and dataclasses

Async file operations in Node.js vs synchronous in Python

Different date parsing libraries (date-fns vs dateutil)

Currency formatting and localization differences

Test mocking patterns (Jest vs pytest-mock)

How AI Helped:
Converted my original TypeScript implementation to Python since I'm more familiar with Node.js

Helped resolve Python import errors and package installation issues

Assisted with Python-specific syntax and pandas library usage

Provided guidance on Python project structure and best practices

Suggested appropriate Python libraries to replace Node.js dependencies (pandas for data manipulation, pytest for testing)

Helped understand Python's context managers for file handling vs TypeScript's async/await patterns

Assisted in converting TypeScript's functional array methods (map, filter, reduce) to pandas DataFrame operations

Design Notes
This solution was originally implemented in TypeScript/Node.js due to my familiarity with that stack, then converted to Python to meet the job requirements. The architecture follows object-oriented principles with separate classes for data processing, validation, and reporting.

The conversion maintained the same core logic and business rules while adapting to Python's ecosystem and conventions.

Project Structure
text
project/
├── src/                 # Source code modules
├── tests/               # Unit tests
├── data/                # Sample data
├── main.py              # CLI entry point
├── requirements.txt     # Dependencies
└── README.md           # This file

Running Tests
bash
pytest tests/
Sample Output
The application generates a comprehensive transaction report showing processing summary, financial totals, and status breakdowns.