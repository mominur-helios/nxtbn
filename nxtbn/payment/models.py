from django.db import models

from nxtbn.core.models import AbstractBaseModel
from nxtbn.order.models import Order
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

from nxtbn.payment import PaymentMethod, PaymentStatus
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

