from django.urls import path
from .views import (
    ProductListCreateApiView, 
    ProductDetailApiView, 
    OrderListApiView, 
    UserOrderListApiView,
    ProductInfoApiView,
    )

app_name='api'

urlpatterns = [
    path('products/', ProductListCreateApiView.as_view(), name='products'),
    path('products/<int:product_id>', ProductDetailApiView.as_view(), name='product_details'),
    path('orders/', OrderListApiView.as_view(), name='orders'),
    path('user-orders/', UserOrderListApiView.as_view(), name='user_orders'),
    path('products/info', ProductInfoApiView.as_view(), name='product_info'),

]
