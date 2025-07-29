from .models import Product, Order, User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from .filters import ProductFilters, InStockFilterBackend, OrderFilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import viewsets
from .serializers import (
    ProductSerializer, 
    OrderSerializer, 
    ProductInfoSerializer, 
    OrderWriteSerializer,
    UserSerializer
    )


class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('id')
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

    # LimitOffsetPagination OR
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3
    pagination_class.page_query_param = 'page_num'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 5


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


class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(data=serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('items', 'items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilters

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
    
    def get_serializer_class(self):
        # can also handle, request.method == 'POST'
        if self.action == 'create' or self.action == 'update':
            return OrderWriteSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    # @action(detail=False, methods=['get'], url_path='user-orders', permission_classes=[IsAuthenticated])
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=self.request.user)
    #     serializers = self.get_serializer(orders, many=True)
    #     return Response(serializers.data)


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