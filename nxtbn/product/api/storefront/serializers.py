from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction

from nxtbn.product.api.dashboard.serializers import RecursiveCategorySerializer
from nxtbn.product.models import Product, Collection, Category

class CategorySerializer(RecursiveCategorySerializer):
    pass

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'description', 'is_active', 'image',)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'category',
            'brand',
            'type',
            'currency',
        )



class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'brand',
            'type',
            'currency',
            'category',
            'collections',
            'media',
            'created_by',
        )