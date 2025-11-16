from decimal import Decimal
from typing import List, Dict, Any

# Use absolute imports
from models.transaction import Transaction, ProcessedTransaction
from constants.status import TransactionStatus
from constants.currencies import Currency

class TransactionProcessor:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.duplicates: List[Transaction] = []
        self.invalid_transactions: List[Dict[str, Any]] = []
    
    def add_transaction(self, transaction: Transaction) -> bool:
        if self._is_duplicate(transaction):
            self.duplicates.append(transaction)
            return False
        self.transactions.append(transaction)
        return True
    
    def add_invalid_transaction(self, transaction: Transaction, errors: List[str]) -> None:
        self.invalid_transactions.append({
            "transaction": transaction.to_dict(),
            "errors": errors
        })
    
    def _is_duplicate(self, transaction: Transaction) -> bool:
        existing_ids = {t.transaction_id for t in self.transactions}
        duplicate_ids = {t.transaction_id for t in self.duplicates}
        return (transaction.transaction_id in existing_ids or 
                transaction.transaction_id in duplicate_ids)
    
    def get_valid_transactions(self) -> List[Transaction]:
        return self.transactions.copy()
    
    def get_invalid_transactions(self) -> List[Dict[str, Any]]:
        return self.invalid_transactions.copy()
    
    def get_duplicate_transactions(self) -> List[Transaction]:
        return self.duplicates.copy()
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        if not self.transactions:
            return {
                "total_processed": len(self.invalid_transactions) + len(self.duplicates),
                "valid_count": 0,
                "invalid_count": len(self.invalid_transactions),
                "duplicate_count": len(self.duplicates),
                "total_amount_usd": 0.0,
                "total_amount_eur": 0.0,
                "completed_count": 0,
                "failed_count": 0,
                "pending_count": 0,
                "cancelled_count": 0,
            }
        
        total_amount_usd = sum(float(t.amount) for t in self.transactions if t.currency == Currency.USD)
        total_amount_eur = sum(float(t.amount) for t in self.transactions if t.currency == Currency.EUR)
        
        status_counts = {
            TransactionStatus.COMPLETED: 0,
            TransactionStatus.FAILED: 0,
            TransactionStatus.PENDING: 0,
            TransactionStatus.CANCELLED: 0
        }
        for t in self.transactions:
            status_counts[t.status] = status_counts.get(t.status, 0) + 1
        
        return {
            "total_processed": len(self.transactions) + len(self.invalid_transactions) + len(self.duplicates),
            "valid_count": len(self.transactions),
            "invalid_count": len(self.invalid_transactions),
            "duplicate_count": len(self.duplicates),
            "total_amount_usd": total_amount_usd,
            "total_amount_eur": total_amount_eur,
            "completed_count": status_counts[TransactionStatus.COMPLETED],
            "failed_count": status_counts[TransactionStatus.FAILED],
            "pending_count": status_counts[TransactionStatus.PENDING],
            "cancelled_count": status_counts[TransactionStatus.CANCELLED],
        }