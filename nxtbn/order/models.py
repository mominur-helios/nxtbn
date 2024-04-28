from django.db import models

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from nxtbn.core.models import AbstractAddressModels, AbstractBaseModel, AbstractBaseUUIDModel
from nxtbn.order import OrderAuthorizationStatus, OrderChargeStatus, OrderStatus
from nxtbn.payment import PaymentMethod
from nxtbn.product.models import ProductVariant
from nxtbn.users.admin import User
from nxtbn.vendor.models import Vendor


class Address(AbstractAddressModels):

    # Customizable Receiver Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    is_default_delivery_address = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.street_address}, {self.city}, {self.country}"

class Order(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.SET_NULL)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    shipping_address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL, related_name="shipping_orders")
    billing_address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL, related_name="billing_orders")
    total_price = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal("0.01"))])

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    authorize_status = models.CharField(
        max_length=32,
        default=OrderAuthorizationStatus.NONE,
        choices=OrderAuthorizationStatus.choices,
        db_index=True,
    )
    charge_status = models.CharField(
        max_length=32,
        default=OrderChargeStatus.NONE,
        choices=OrderChargeStatus.choices,
        db_index=True,
    )
    

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="+")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal("0.01"))])
    total_price = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(Decimal("0.01"))])

    def __str__(self):
        return f"{self.variant.product.name} - {self.variant.name} - Qty: {self.quantity}"

