from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

from nxtbn.core.models import AbstractBaseModel, AbstractBaseUUIDModel
from nxtbn.product.models import ProductVariant


class Cart(AbstractBaseModel):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(AbstractBaseUUIDModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product_variant.name} in Cart {self.cart.id}"
