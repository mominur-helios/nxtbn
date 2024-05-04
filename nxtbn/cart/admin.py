from django.contrib import admin
from nxtbn.cart.models import Cart, CartItem
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('id', 'user')
    list_filter = ('user',)
    search_fields = ('id', 'user')

admin.site.register(Cart, CartAdmin)