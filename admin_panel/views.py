from django.shortcuts import render

from rest_framework import generics
from products.models import Product, Category, ProductImage, Banner
from .serializers import ProductSerializer, CategorySerializer, BannerSerializer

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
    # lookup_field = 'pk'

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

class BannerListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create Banners.
    """
    permission_classes = []
    authentication_classes = []
    
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class BannerUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing Banner.
    """
    permission_classes = []
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    lookup_field = 'pk'

class BannerDestroyView(generics.DestroyAPIView):
    """
    API view to delete an existing Banner.
    """
    permission_classes = []
    queryset = Banner.objects.all()
    lookup_field = 'pk'

