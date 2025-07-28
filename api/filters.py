import django_filters
from .models import Product, Order
from rest_framework import filters


class ProductFilters(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['lt', 'gt', 'range']            
        }


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class OrderFilters(django_filters.FilterSet):
    
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')

    class Meta: 
        model = Order
        fields = {
            'user': ['exact', 'lt', 'gt'],
            'status': ['iexact', 'icontains'],
            'created_at': ['lt', 'gt']
        }


'''               # Declaring Filters

class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

    manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price', 'release_date', 'manufacturer']

'''