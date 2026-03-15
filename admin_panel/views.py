from django.shortcuts import render

from rest_framework import generics
from products.models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer

class ProductCreateView(generics.CreateAPIView):
    """
    API view to create a new Product.
    Follows standard DRF validation behavior through ProductSerializer.
    """
    permission_classes = []
    authentication_classes = []

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing Product.
    Supports partial (PATCH) and full (PUT) updates.
    """
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create Categories.
    """
    permission_classes = []
    authentication_classes = []
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing Category.
    """
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

class ProductDestroyView(generics.DestroyAPIView):
    """
    API view to delete an existing Product.
    """
    permission_classes = []
    queryset = Product.objects.all()
    lookup_field = 'pk'

class CategoryDestroyView(generics.DestroyAPIView):
    """
    API view to delete an existing Category.
    """
    permission_classes = []
    queryset = Category.objects.all()
    lookup_field = 'pk'
