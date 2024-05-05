from django.urls import path

from nxtbn.order.api.dashboard.views import OrderDetailView, OrderListView


urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<uuid:id>/', OrderDetailView.as_view(), name='order-detail'),
]
