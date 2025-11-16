import csv
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
from decimal import Decimal

# Use absolute imports
from models.transaction import RawTransaction, ProcessedTransaction, Transaction
from constants.currencies import Currency
from constants.status import TransactionStatus
from services.data_cleaner import DataCleaner
from services.data_validator import DataValidator

class CSVProcessor:
    def __init__(self, validator: DataValidator = None):
        self.logger = logging.getLogger(__name__)
        self.validator = validator or DataValidator()
        self.data_cleaner = DataCleaner()
        self._processed_ids = set()
    
    def detect_delimiter(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sample = file.read(1024)
            
            delimiters = [",", ";", "\t", "|"]
            counts = {d: sample.count(d) for d in delimiters}
            best_delimiter = max(counts.keys(), key=lambda d: counts[d])
            return best_delimiter if counts[best_delimiter] > 0 else ","
        except Exception as e:
            self.logger.warning(f"Error detecting delimiter: {e}, defaulting to comma")
            return ","
    
    def read_csv_file(self, file_path: str) -> List[RawTransaction]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline()
            delimiter = self.detect_delimiter(file_path)
            file.seek(0)
            content = file.read()
        
        lines = content.strip().split('\n')
        reader = csv.reader(lines, delimiter=delimiter)
        rows = list(reader)
        
        if not rows: 
            return []
        
        headers = [str(h).lower().strip() for h in rows[0]]
        map_index = {}
        
        for i, header in enumerate(headers):
            if 'transaction' in header and 'id' in header:
                map_index['transaction_id'] = i
            elif 'customer' in header and 'id' in header:
                map_index['customer_id'] = i
            elif 'date' in header:
                map_index['date'] = i
            elif 'amount' in header or 'value' in header:
                map_index['amount'] = i
            elif 'currency' in header or 'curr' in header:
                map_index['currency'] = i
            elif 'status' in header:
                map_index['status'] = i
        
        required_fields = ['transaction_id', 'customer_id', 'date', 'amount', 'currency', 'status']
        for field in required_fields:
            if field not in map_index:
                map_index[field] = -1
        
        transactions = []
        for i in range(1, len(rows)):
            row = rows[i]
            if not any(row): 
                continue
            
            def get_val(field):
                idx = map_index.get(field, -1)
                return row[idx] if 0 <= idx < len(row) and row[idx] is not None else None
            
            transaction = RawTransaction(
                transaction_id=get_val('transaction_id'),
                customer_id=get_val('customer_id'),
                date=get_val('date'),
                amount=get_val('amount'),
                currency=get_val('currency'),
                status=get_val('status')
            )
            transactions.append(transaction)
        
        return transactions

    def process_csv_file(self, file_path: str):
        from services.transaction_processor import TransactionProcessor

        self.logger.info(f"Starting to process CSV file: {file_path}")

        if not Path(file_path).exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        processor = TransactionProcessor()

        try:
            raw_transactions = self.read_csv_file(file_path)

            
            cleaned_data = self.data_cleaner.clean(raw_transactions)
   
            
            valid_data, invalid_data, duplicate_ids = self.validator.validate_dataset(cleaned_data)
          

            # Convert valid ProcessedTransaction to Transaction objects
            valid_count = 0
            for processed in valid_data:
                transaction = Transaction.from_processed(processed)
                if transaction:
                    if transaction.transaction_id in self._processed_ids:
                        processor.add_duplicate_transaction(transaction)
                        print(f"  🔄 Duplicate: {transaction.transaction_id}")
                    else:
                        processor.add_transaction(transaction)
                        self._processed_ids.add(transaction.transaction_id)
                        valid_count += 1
                       
                else:
                    print(f"  ❌ Invalid: {processed.transaction_id} - Missing required fields")

            # Add invalid transactions to processor
            for invalid_txn in invalid_data:
                company_transaction = Transaction.from_processed(invalid_txn)
                if company_transaction:
                    processor.add_invalid_transaction(
                        company_transaction, 
                        invalid_txn.validation_errors
                    )
            return processor

        except Exception as e:
            self.logger.error(f"Error processing CSV file: {e}")
            raise