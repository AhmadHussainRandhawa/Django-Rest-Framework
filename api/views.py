from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from .filters import ProductFilters, InStockFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    filterset_class = ProductFilters
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


'''      # ListCreateApiView is a mixture of List and Create Api view.

class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateApiView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer
'''


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.select_related('user').prefetch_related('items', 'items__product').all()
    serializer_class = OrderSerializer


class UserOrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.select_related('user')\
            .prefetch_related('items', 'items__product').all()\
            .filter(user=self.request.user)


class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(data=serializer.data)


'''               # Function Base Views

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.select_related('user').prefetch_related('items', 'items__product').all()
    serializer = OrderSerializer(orders, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),        
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(data=serializer.data)
'''