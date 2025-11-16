
"""
Main CLI script for Acme Payments transaction processing.
"""

import argparse
import logging
import sys
import os
from pathlib import Path
from typing import Optional

# Fix the Python path to include the src directory
sys.path.insert(0, os.path.dirname(__file__))

# Now import using absolute imports
from services.csv_processor import CSVProcessor
from services.report_generator import ReportGenerator
from services.data_validator import DataValidator


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Acme Payments Transaction Processing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py data/sample_transactions.csv
  python src/main.py data/sample_transactions.csv -o reports --all-reports
  python src/main.py data/sample_transactions.csv --json --csv --errors
  python src/main.py data/sample_transactions.csv --log-level DEBUG
        """,
    )

    parser.add_argument("input_file", help="Path to input CSV file containing transaction data")
    parser.add_argument("-o", "--output-dir", default="output", help="Output directory for reports")
    parser.add_argument("--json", action="store_true", help="Generate detailed JSON report")
    parser.add_argument("--csv", action="store_true", help="Generate CSV summary report")
    parser.add_argument("--errors", action="store_true", help="Generate detailed error report")
    parser.add_argument("--all-reports", action="store_true", help="Generate all report types")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
    parser.add_argument("--log-file", help="Optional log file path")

    return parser.parse_args()


def main() -> int:
    try:
        args = parse_arguments()
        setup_logging(args.log_level, args.log_file)
        
        logger = logging.getLogger(__name__)
       

        if not os.path.exists(args.input_file):
            logger.error(f"Input file not found: {args.input_file}")
            return 1

        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        validator = DataValidator()
        csv_processor = CSVProcessor(validator=validator)
        
        transaction_processor = csv_processor.process_csv_file(args.input_file)

        report_generator = ReportGenerator(transaction_processor, str(output_dir))

        print("\n" + "="*60)
        print("PROCESSING RESULTS")
        print("="*60)
        report_generator.print_console_report()

        generated_reports = []

        if args.all_reports:
            logger.info("Generating all reports...")
            try:
                reports = report_generator.generate_all_reports()
                generated_reports.extend(reports.values())
                logger.info(f"Generated reports: {list(reports.keys())}")
            except Exception as e:
                logger.error(f"Error generating all reports: {e}")
        else:
            if args.json:
                logger.info("Generating JSON report...")
                try:
                    json_path = report_generator.generate_json_report()
                    generated_reports.append(json_path)
                    logger.info(f"JSON report: {json_path}")
                except Exception as e:
                    logger.error(f"Error generating JSON report: {e}")

            if args.csv:
                logger.info("Generating CSV summary...")
                try:
                    csv_path = report_generator.generate_csv_summary()
                    generated_reports.append(csv_path)
                    logger.info(f"CSV summary: {csv_path}")
                except Exception as e:
                    logger.error(f"Error generating CSV summary: {e}")

            if args.errors:
                logger.info("Generating error report...")
                try:
                    error_path = report_generator.generate_error_report()
                    generated_reports.append(error_path)
                    logger.info(f"Error report: {error_path}")
                except Exception as e:
                    logger.error(f"Error generating error report: {e}")

        if generated_reports:
            print(f"\n📊 Reports generated in '{output_dir}':")
            for report_path in generated_reports:
                print(f"  📄 {Path(report_path).name}")

        logger.info("Transaction processing completed successfully")
        return 0

    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())