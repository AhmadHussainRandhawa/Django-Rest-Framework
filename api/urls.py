from django.urls import path
from .views import (
    ProductListCreateApiView, 
    ProductDetailApiView, 
    ProductInfoApiView,
    OrderViewSet,
    UserListApiView
)
from rest_framework.routers import DefaultRouter

app_name='api'

urlpatterns = [
    path('products/', ProductListCreateApiView.as_view(), name='products'),
    path('products/<int:product_id>', ProductDetailApiView.as_view(), name='product_details'),
    path('products/info', ProductInfoApiView.as_view(), name='product_info'),
    path('users/', UserListApiView.as_view(), name='user'),

]

router = DefaultRouter()
router.register('orders', OrderViewSet)
urlpatterns += router.urls
