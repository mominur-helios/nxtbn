from datetime import timezone
from django.db import models

from nxtbn.core.models import AbstractBaseModel
from nxtbn.order.models import Order
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

from nxtbn.payment import PaymentMethod, PaymentStatus
from nxtbn.payment.payment_manager import PaymentManager
from nxtbn.users.admin import User


class Payment(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    # For storing payment gateway references
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  
    payment_getway = models.CharField(max_length=100, blank=True, null=True) 

    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_amount = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal("0.01"))])
    paid_at = models.DateTimeField(blank=True, null=True)

    def authorize_payment(self, amount: Decimal):
        """Authorize payment through the specified gateway."""
        manager = PaymentManager(self.payment_getway)
        response = manager.authorize_payment(amount, str(self.order.id))
        # Update model fields based on the response
        if response:
            self.transaction_id = response.transaction_id
            self.payment_status = PaymentStatus.AUTHORIZED
            self.save()
        return response

    def capture_payment(self, amount: Decimal):
        """Capture authorized payment."""
        manager = PaymentManager(self.payment_getway)
        response = manager.capture_payment(amount, str(self.order.id))
        if response:
            self.payment_status = PaymentStatus.CAPTURED
            self.paid_at = timezone.now()
            self.save()
        return response

    def cancel_payment(self):
        """Cancel authorized payment."""
        manager = PaymentManager(self.payment_getway)
        response = manager.cancel_payment(str(self.order.id))
        if response:
            self.payment_status = PaymentStatus.CANCELED
            self.save()
        return response

    def refund_payment(self, amount: Decimal):
        """Refund captured payment."""
        manager = PaymentManager(self.payment_getway)
        response = manager.refund_payment(amount, str(self.order.id))
        if response:
            self.payment_status = PaymentStatus.REFUNDED
            self.save

