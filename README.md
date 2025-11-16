# ACME Payments Transaction Processor

A Python application for processing, cleaning, and summarizing
transaction data from CSV files.

## Installation

1.  Ensure **Python 3.8+** is installed on your system.
2.  Clone this repository.
3.  Install dependencies:

``` bash
pip install -r requirements.txt
```

## Usage

Run the application with a CSV file:

``` bash
python main.py data/sample_transactions.csv
```

## AI Usage Disclosure

### Tools Used

-   ChatGPT for code conversion and debugging assistance.

### Prompts Used

-   "Convert this TypeScript/Node.js transaction processor to Python
    with class structure"
-   "How to handle Python imports and module structure for a CSV
    processing application?"
-   "Python pandas equivalent for TypeScript array operations and data
    filtering"
-   "Debugging Python installation and dependency issues with pandas and
    pytest"
-   "Convert TypeScript interface definitions to Python classes with
    validation"
-   "Python equivalent of TypeScript's date parsing and currency
    formatting"
-   "How to structure Python unit tests similar to Jest testing
    patterns"
-   "Python error handling and exception patterns for file processing"

## Conversion Details

### Original TypeScript Architecture

-   TransactionProcessor class with CSV reading, cleaning, and reporting
-   Transaction interface
-   ValidationResult type
-   Jest tests with mocking

### Python Implementation Approach

-   Mirrored TransactionProcessor class
-   Used dataclasses for Transaction model
-   Replaced array methods with pandas DataFrame operations
-   Converted Jest tests to pytest
-   Maintained architecture and error handling

### Key Conversion Challenges

-   Static typing vs dynamic typing
-   Async Node.js vs synchronous Python
-   date-fns vs dateutil parsing
-   Currency formatting differences
-   Jest mocking vs pytest-mock

## How AI Helped

-   Converted TS → Python
-   Helped resolve import and installation issues
-   Guided pandas usage
-   Provided project structure suggestions
-   Assisted with context managers vs async/await
-   Helped translate map/filter/reduce to pandas

## Design Notes

The solution was originally TypeScript/Node.js and converted to Python
while keeping the same business logic and structure.

## Project Structure

    project/
    ├── src/
    ├── tests/
    ├── data/
    ├── main.py
    ├── requirements.txt
    └── README.md

## Running Tests

``` bash
pytest tests/
```

## Sample Output

The application generates a transaction summary with totals, validation
results, and status breakdowns.
