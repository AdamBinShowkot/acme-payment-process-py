import re
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime, date
from typing import Optional, List
from dateutil import parser

# Use absolute imports
from models.transaction import RawTransaction, ProcessedTransaction
from constants.currencies import Currency, CURRENCY_MAP
from constants.status import TransactionStatus, STATUS_MAP

logger = logging.getLogger(__name__)

class DataCleaner:
    def clean(self, transactions: List[RawTransaction]) -> List[ProcessedTransaction]:
        return [self._clean_transaction(t) for t in transactions]
    
    def _clean_transaction(self, transaction: RawTransaction) -> ProcessedTransaction:
        cleaned = ProcessedTransaction(
            transaction_id=self._clean_string(transaction.transaction_id),
            customer_id=self._clean_string(transaction.customer_id),
            date=self._clean_date(transaction.date),
            amount=self._clean_amount(transaction.amount),
            currency=self._clean_currency(transaction.currency),
            status=self._clean_status(transaction.status)
        )
        return cleaned
    
    def _clean_string(self, value: any) -> str:
        if value is None: 
            return ""
        result = str(value).strip()
        return result if result else ""
    
    def _clean_date(self, date_str: any) -> Optional[date]:
        if date_str is None: 
            return None
        
        date_str_clean = str(date_str).strip()
        if not date_str_clean:
            return None
        
        date_formats = [
            '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%d/%m/%Y', 
            '%d-%m-%y', '%d/%m/%y', '%Y%m%d'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str_clean, fmt).date()
            except ValueError:
                continue
                
        try:
            if date_str_clean.isdigit() and len(date_str_clean) <= 5:
                excel_number = int(date_str_clean)
                excel_epoch = datetime(1899, 12, 30)
                result_date = excel_epoch.replace(day=excel_epoch.day + excel_number)
                return result_date.date()
        except:
            pass
            
        return None
    
    def _clean_amount(self, amount_str: any) -> Optional[Decimal]:
        if amount_str is None: 
            return None
        
        amount_str_clean = str(amount_str).strip()
        if not amount_str_clean: 
            return None
        
        cleaned = re.sub(r'[^\d.,-]', '', amount_str_clean)
        if not cleaned: 
            return None
        
        comma_count = cleaned.count(',')
        dot_count = cleaned.count('.')
        
        if comma_count == 1 and dot_count > 0 and cleaned.find(',') > cleaned.find('.'):
            cleaned = cleaned.replace('.', '').replace(',', '.')
        elif comma_count > 0 and dot_count == 1 and cleaned.find('.') > cleaned.find(','):
            cleaned = cleaned.replace(',', '')
        elif comma_count > 0 and dot_count == 0:
            cleaned = cleaned.replace(',', '')
        elif comma_count == 1 and dot_count == 0:
            cleaned = cleaned.replace(',', '.')
        
        try:
            return Decimal(cleaned)
        except:
            return None
    
    def _clean_currency(self, currency_str: any) -> Optional[Currency]:
        if currency_str is None: 
            return None
        
        currency_clean = str(currency_str).strip().upper()
        if not currency_clean:
            return None
        
        if currency_clean in CURRENCY_MAP:
            return CURRENCY_MAP[currency_clean]
        
        try:
            return Currency(currency_clean)
        except:
            return None
    
    def _clean_status(self, status_str: any) -> Optional[TransactionStatus]:
        if status_str is None: 
            return None
        
        status_clean = str(status_str).strip().lower()
        if not status_clean:
            return None
        
        if status_clean in STATUS_MAP:
            return STATUS_MAP[status_clean]
        
        try:
            return TransactionStatus(status_clean)
        except:
            return None