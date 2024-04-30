from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from importlib import import_module

import logging

logger = logging.getLogger(__name__)


PAYMENT_GATEWAYS = getattr(settings, 'PAYMENT_GATEWAYS')

class PaymentManager:
    """Manager class to handle payment operations with multiple gateways."""

    def __init__(self, payment_getway: str):
        self.gateway = self.select_gateway(payment_getway)

    def select_gateway(self, payment_getway: str):
        """Select the appropriate gateway based on the payment method."""
        gateway_path = PAYMENT_GATEWAYS.get(payment_getway.lower())
        if not gateway_path:
            if payment_getway.lower() == "cash_on_delivery":
                return None  # Cash on delivery doesn't require a gateway
            else:
                raise ValidationError("Invalid payment method")

        module_name, class_name = gateway_path.rsplit(".", 1)
        module = import_module(module_name)
        gateway_class = getattr(module, class_name)

        return gateway_class()

    def authorize_payment(self, amount: Decimal, order_id: str, **kwargs):
        """Authorize payment."""
        if not self.gateway:
            logger.info("Cash on delivery requires no authorization")
            return None  # Cash on delivery requires no authorization
        return self.gateway.authorize(amount, order_id, **kwargs)

    def capture_payment(self, amount: Decimal, order_id: str, **kwargs):
        """Capture payment."""
        if not self.gateway:
            logger.info("Cash on delivery requires no capture")
            return None  # Cash on delivery requires no capture
        return self.gateway.capture(amount, order_id, **kwargs)

    def cancel_payment(self, order_id: str, **kwargs):
        """Cancel authorization."""
        if not self.gateway:
            logger.info("Cash on delivery requires no cancelation")
            return None  # Cash on delivery requires no cancelation
        return self.gateway.cancel(order_id, **kwargs)

    def refund_payment(self, amount: Decimal, order_id: str, **kwargs):
        """Refund payment."""
        if not self.gateway:
            logger.info("Cash on delivery requires no refund")
            return None  # Cash on delivery requires no refund
        return self.gateway.refund(amount, order_id, **kwargs)
