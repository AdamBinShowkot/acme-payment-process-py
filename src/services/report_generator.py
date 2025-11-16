import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Use absolute imports
from services.transaction_processor import TransactionProcessor

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, processor: TransactionProcessor, output_dir: str = "output"):
        self.processor = processor
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def print_console_report(self) -> None:
        stats = self.processor.get_summary_statistics()
        
        lines = []
        lines.append("=" * 64)
        lines.append("ACME PAYMENTS TRANSACTION PROCESSING REPORT")
        lines.append("=" * 64)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        lines.append("PROCESSING SUMMARY:")
        lines.append(f"Total transactions processed: {stats['total_processed']:,}")
        lines.append(f"Valid transactions: {stats['valid_count']:,}")
        lines.append(f"Invalid transactions: {stats['invalid_count']:,}")
        lines.append(f"Duplicate transactions: {stats['duplicate_count']:,}")
        lines.append("")
        
        lines.append("FINANCIAL SUMMARY:")
        lines.append(f"Total amount (USD): ${stats['total_amount_usd']:,.2f}")
        lines.append(f"Total amount (EUR): €{stats['total_amount_eur']:,.2f}")
        lines.append("")
        
        lines.append("TRANSACTION STATUS BREAKDOWN:")
        lines.append(f"Completed transactions: {stats['completed_count']:,}")
        lines.append(f"Failed transactions: {stats['failed_count']:,}")
        lines.append(f"Pending transactions: {stats['pending_count']:,}")
        lines.append(f"Cancelled transactions: {stats['cancelled_count']:,}")
        
        lines.append("=" * 64)
        
        print("\n".join(lines))
    
    def generate_json_report(self, filename: Optional[str] = None) -> str:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transaction_report_{timestamp}.json"
        
        report_path = self.output_dir / filename
        
        report_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0",
                "report_type": "transaction_analysis",
            },
            "summary": self.processor.get_summary_statistics(),
            "valid_transactions": [t.to_dict() for t in self.processor.get_valid_transactions()],
            "invalid_transactions": self.processor.get_invalid_transactions(),
            "duplicate_transactions": [t.to_dict() for t in self.processor.get_duplicate_transactions()],
        }
        
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, default=str)
            self.logger.info(f"JSON report generated: {report_path}")
            return str(report_path)
        except Exception as e:
            self.logger.error(f"Error generating JSON report: {e}")
            raise
    
    def generate_csv_summary(self, filename: Optional[str] = None) -> str:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transaction_summary_{timestamp}.csv"
        
        report_path = self.output_dir / filename
        
        valid_transactions = self.processor.get_valid_transactions()
        
        try:
            with open(report_path, "w", newline="", encoding="utf-8") as f:
                if valid_transactions:
                    writer = csv.DictWriter(f, fieldnames=[
                        "transaction_id", "customer_id", "date", "amount", "currency", "status"
                    ])
                    writer.writeheader()
                    
                    for transaction in valid_transactions:
                        writer.writerow({
                            "transaction_id": transaction.transaction_id,
                            "customer_id": transaction.customer_id,
                            "date": transaction.date.isoformat(),
                            "amount": float(transaction.amount),
                            "currency": transaction.currency.value,
                            "status": transaction.status.value,
                        })
                else:
                    writer = csv.writer(f)
                    writer.writerow(["transaction_id", "customer_id", "date", "amount", "currency", "status"])
            
            self.logger.info(f"CSV summary report generated: {report_path}")
            return str(report_path)
        except Exception as e:
            self.logger.error(f"Error generating CSV summary: {e}")
            raise
    
    def generate_error_report(self, filename: Optional[str] = None) -> str:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"error_report_{timestamp}.json"
        
        report_path = self.output_dir / filename
        
        error_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "error_analysis",
            },
            "summary": {
                "total_invalid_transactions": len(self.processor.get_invalid_transactions()),
                "total_duplicate_transactions": len(self.processor.get_duplicate_transactions()),
            },
            "invalid_transactions": self.processor.get_invalid_transactions(),
            "duplicate_transactions": [t.to_dict() for t in self.processor.get_duplicate_transactions()],
        }
        
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(error_data, f, indent=2, default=str)
            self.logger.info(f"Error report generated: {report_path}")
            return str(report_path)
        except Exception as e:
            self.logger.error(f"Error generating error report: {e}")
            raise
    
    def generate_all_reports(self) -> Dict[str, str]:
        reports = {}
        reports["json"] = self.generate_json_report()
        reports["csv"] = self.generate_csv_summary()
        reports["errors"] = self.generate_error_report()
        return reports