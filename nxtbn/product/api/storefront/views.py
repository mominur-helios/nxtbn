from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from rest_framework import filters
import django_filters

from nxtbn.core.paginator import NxtbnPagination
from nxtbn.product.api.storefront.serializers import CategorySerializer, CollectionSerializer, ProductDetailSerializer, ProductSerializer
from nxtbn.product.models import Category, Collection, Product


class ProductListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CollectionListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer

class CategoryListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = NxtbnPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'