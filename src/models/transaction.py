from dataclasses import dataclass, field
from decimal import Decimal
from datetime import date
from typing import List, Dict, Any, Optional

# Use absolute imports
from constants.currencies import Currency
from constants.status import TransactionStatus

@dataclass
class RawTransaction:
    transaction_id: any
    customer_id: any
    date: any
    amount: any
    currency: any
    status: any

@dataclass
class ProcessedTransaction:
    transaction_id: str
    customer_id: Optional[str]
    date: Optional[date]
    amount: Optional[Decimal]
    currency: Optional[Currency]
    status: Optional[TransactionStatus]
    is_valid: bool = False
    validation_errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "date": self.date.isoformat() if self.date else None,
            "amount": float(self.amount) if self.amount else None,
            "currency": self.currency.value if self.currency else None,
            "status": self.status.value if self.status else None,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors
        }

@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    date: date
    amount: Decimal
    currency: Currency
    status: TransactionStatus
    raw_data: Dict[str, Any] = field(default_factory=dict)
    validation_errors: List[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.amount, (int, float, str)):
            try:
                self.amount = Decimal(str(self.amount))
            except:
                pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "date": self.date.isoformat(),
            "amount": float(self.amount),
            "currency": self.currency.value,
            "status": self.status.value,
            "validation_errors": self.validation_errors,
        }

    @classmethod
    def from_processed(cls, processed: ProcessedTransaction) -> Optional['Transaction']:
        if not all([processed.transaction_id, processed.customer_id, 
                   processed.date, processed.amount is not None,
                   processed.currency, processed.status]):
            return None
            
        return cls(
            transaction_id=processed.transaction_id,
            customer_id=processed.customer_id,
            date=processed.date,
            amount=processed.amount,
            currency=processed.currency,
            status=processed.status,
            raw_data={}
        )