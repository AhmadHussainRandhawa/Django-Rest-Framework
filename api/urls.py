from .views import product_list, product_detail
from django.urls import path

app_name='api'

urlpatterns = [
    path('products/', product_list, name='products'),
    path('products/<int:pk>', product_detail, name='product_details'),

]
