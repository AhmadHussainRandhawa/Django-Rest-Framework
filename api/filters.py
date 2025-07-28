import django_filters
from .models import Product


class ProductFilters(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['lt', 'gt', 'range']            
            }