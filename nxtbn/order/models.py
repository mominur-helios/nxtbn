from django.db import models

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from nxtbn.core.models import AbstractAddressModels, AbstractBaseModel, AbstractBaseUUIDModel
from nxtbn.discount.models import PromoCode
from nxtbn.gift_card.models import GiftCard
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

class Order(AbstractBaseUUIDModel):
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
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    gift_card = models.ForeignKey(GiftCard, on_delete=models.SET_NULL, null=True, blank=True)

    def apply_promo_code(self):
        """
        Apply a promotional code to the order, reducing the total price accordingly.

        If the promo code is valid and active, the discount is calculated based on the type
        of promo code (either a percentage or a fixed amount). The order's total is reduced
        by the calculated discount.

        This method does not automatically save the changes to the database. You must call
        `order.save()` after calling this method to persist changes.

        Returns:
            decimal.Decimal: The amount of the discount applied to the order, or 0 if no discount is applied.
    """
        if self.promo_code and self.promo_code.is_valid():
            if self.promo_code.code_type == 'percentage':
                discount = (self.total * (self.promo_code.value / 100))
            else:
                discount = self.promo_code.value
            self.total -= discount
            return discount
        return 0

    def apply_gift_card(self):
        """
            Apply a gift card to the order, reducing the total price by the balance available on the gift card.

            If the gift card is valid and has sufficient balance, the order's total will be reduced accordingly.
            If the gift card's balance is greater than or equal to the order's total, the order's total is set to
            zero. Otherwise, the order's total is reduced by the gift card's balance.

            This method does not automatically save the changes to the database. You must call `order.save()`
            after calling this method to persist changes.

            Note:
                This method reduces the gift card's balance according to the applied discount.

            Returns:
                None
        """
        if self.gift_card and self.gift_card.is_valid():
            if self.gift_card.current_balance >= self.total:
                self.gift_card.reduce_balance(self.total)
                self.total = 0
            else:
                self.total -= self.gift_card.current_balance
                self.gift_card.reduce_balance(self.gift_card.current_balance)
    

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

