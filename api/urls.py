from .views import ProductListApiView, ProductDetailApiView, OrderListApiView, product_info
from django.urls import path

app_name='api'

urlpatterns = [
    path('products/', ProductListApiView.as_view(), name='products'),
    path('products/<int:product_id>', ProductDetailApiView.as_view(), name='product_details'),
    path('orders/', OrderListApiView.as_view(), name='orders'),
    path('products/info', product_info, name='product_info'),

]
