from datetime import timezone
from django.db import models

from nxtbn.core.models import  AbstractBaseUUIDModel
from nxtbn.order.models import Order
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError


from nxtbn.payment import PaymentMethod, PaymentStatus
from nxtbn.payment.payment_manager import PaymentManager
from nxtbn.users.admin import User

def validate_payment_getway(value):
    valid_gateways = settings.PAYMENT_GATEWAYS.keys()
    if value not in valid_gateways:
        raise ValidationError(
            f"Invalid payment gateway: '{value}'. Allowed gateways are: {', '.join(valid_gateways)}."
        )

class Payment(AbstractBaseUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)

    # For storing payment gateway references
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)  

    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.AUTHORIZED)
    payment_amount = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal("0.01"))])
    getway_response_raw = models.JSONField(null=True, blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    """
        The `payment_getway_id` field is used to indicate the payment gateway associated with a payment.
        It should contain a valid payment gateway identifier, which must be one of the keys defined 
        in the PAYMENT_GATEWAYS setting. Currently, the allowed value is "stripe".

        If the value of this field is not among the valid payment gateways defined in PAYMENT_GATEWAYS, 
        it is considered invalid and will raise a ValidationError. Ensure that any data stored in this 
        field matches one of the predefined payment gateways to avoid inconsistencies in payment processing.
    """
    payment_getway_id = models.CharField(max_length=100, blank=True, null=True, validators=[validate_payment_getway])

    def authorize_payment(self, amount: Decimal):
        """Authorize payment through the specified gateway."""
        manager = PaymentManager(self.payment_getway_id)
        response = manager.authorize_payment(amount, str(self.order.id))
        # Update model fields based on the response
        if response:
            self.transaction_id = response.transaction_id
            if response.raw_data:
                self.getway_response_raw = response.raw_data
            self.payment_status = PaymentStatus.AUTHORIZED
            self.save()
        return response

    def capture_payment(self, amount: Decimal):
        """Capture authorized payment."""
        manager = PaymentManager(self.payment_getway_id)
        response = manager.capture_payment(amount, str(self.order.id))
        if response:
            self.payment_status = PaymentStatus.CAPTURED
            self.paid_at = timezone.now()
            if response.raw_data:
                self.getway_response_raw = response.raw_data
            self.save()
        return response

    def cancel_payment(self):
        """Cancel authorized payment."""
        manager = PaymentManager(self.payment_getway_id)
        response = manager.cancel_payment(str(self.order.id))
        if response:
            self.payment_status = PaymentStatus.CANCELED
            if response.raw_data:
                self.getway_response_raw = response.raw_data
            self.save()
        return response

    def refund_payment(self, amount: Decimal):
        """Refund captured payment."""
        manager = PaymentManager(self.payment_getway_id)
        response = manager.refund_payment(amount, str(self.order.id))
        if response:
            self.payment_status = PaymentStatus.REFUNDED
            if response.raw_data:
                self.getway_response_raw = response.raw_data
            self.save

