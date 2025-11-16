import logging
from decimal import Decimal
from typing import List, Tuple, Set

# Use absolute imports
from models.transaction import ProcessedTransaction
from constants.currencies import VALID_CURRENCIES, Currency
from constants.status import VALID_STATUSES, TransactionStatus

logger = logging.getLogger(__name__)

class DataValidator:
    def validate_dataset(self, transactions: List[ProcessedTransaction]) -> Tuple[
        List[ProcessedTransaction], List[ProcessedTransaction], List[str]
    ]:
        valid_rows = []
        invalid_rows = []
        duplicate_ids = self._find_duplicates(transactions)
        
        for transaction in transactions:
            errors = self._validate_row(transaction)
            if transaction.transaction_id in duplicate_ids:
                errors.append("Duplicate transaction_id")
            
            transaction.is_valid = len(errors) == 0
            transaction.validation_errors = errors
            
            if transaction.is_valid:
                valid_rows.append(transaction)
            else:
                invalid_rows.append(transaction)
        
        return valid_rows, invalid_rows, list(duplicate_ids)
    
    def _validate_row(self, transaction: ProcessedTransaction) -> List[str]:
        errors = []
        
        if not transaction.transaction_id:
            errors.append("Missing transaction_id")
        if not transaction.customer_id:
            errors.append("Missing customer_id")
        if not transaction.date:
            errors.append("Invalid date")
        
        if transaction.amount is None:
            errors.append("Invalid amount")
        elif transaction.amount <= 0:
            errors.append("Amount must be positive")
        
        if not transaction.currency:
            errors.append("Missing currency")
        elif transaction.currency not in VALID_CURRENCIES:
            errors.append(f"Invalid currency: {transaction.currency}")
        
        if not transaction.status:
            errors.append("Missing status")
        elif transaction.status not in VALID_STATUSES:
            errors.append(f"Invalid status: {transaction.status}")
            
        return errors
    
    def _find_duplicates(self, transactions: List[ProcessedTransaction]) -> set:
        seen = set()
        duplicates = set()
        
        for transaction in transactions:
            transaction_id = transaction.transaction_id
            if not transaction_id:
                continue
                
            if transaction_id in seen:
                duplicates.add(transaction_id)
            else:
                seen.add(transaction_id)
                
        return duplicates