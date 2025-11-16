from enum import Enum

class TransactionStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    CANCELLED = "cancelled"

STATUS_MAP = {
    "completed": TransactionStatus.COMPLETED, "complete": TransactionStatus.COMPLETED,
    "success": TransactionStatus.COMPLETED, "done": TransactionStatus.COMPLETED, "ok": TransactionStatus.COMPLETED,
    "failed": TransactionStatus.FAILED, "fail": TransactionStatus.FAILED,
    "error": TransactionStatus.FAILED, "rejected": TransactionStatus.FAILED,
    "pending": TransactionStatus.PENDING, "processing": TransactionStatus.PENDING, "ongoing": TransactionStatus.PENDING,
    "cancelled": TransactionStatus.CANCELLED, "canceled": TransactionStatus.CANCELLED, "aborted": TransactionStatus.CANCELLED,
}

VALID_STATUSES = list(TransactionStatus)