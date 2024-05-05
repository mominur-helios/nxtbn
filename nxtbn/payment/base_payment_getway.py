from abc import ABC, abstractmethod
from decimal import Decimal
from django.core.exceptions import ValidationError

from typing import Optional, Any
from dataclasses import dataclass

@dataclass
class PaymentResponse:
    """Unified structure for payment gateway responses."""
    success: bool
    transaction_id: Optional[str] = None # A unique transaction identifier from payment gateway
    message: Optional[str] = None
    raw_data: Optional[Any] = None # the response exactly what we get from payment getway
    meta_data: Optional[Any] = None


class BasePaymentGateway(ABC):
    """Abstract base class for payment gateways."""

    @abstractmethod
    def authorize(self, amount: Decimal, order_id: str, **kwargs):
        """Authorize a payment of the specified amount."""
        pass

    @abstractmethod
    def capture(self, amount: Decimal, order_id: str, **kwargs):
        """Capture an authorized payment."""
        pass

    @abstractmethod
    def cancel(self, order_id: str, **kwargs):
        """Cancel an authorized payment."""
        pass

    @abstractmethod
    def refund(self, amount: Decimal, order_id: str, **kwargs):
        """Refund a captured payment."""
        pass

    @abstractmethod
    def normalize_response(self, raw_response: Any) -> PaymentResponse:
        """Normalize raw response to a consistent PaymentResponse."""
        pass
