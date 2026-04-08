from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, Category, Banner
from .serializers import ProductSerializer, CategorySerializer, BannerSerializer

class BannerListAPIView(generics.ListAPIView):
    """
    Public endpoint — returns active banners.
    No authentication required.
    """
    serializer_class = BannerSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        return Banner.objects.filter(is_active=True).order_by('-created_date')


class ProductListAPIView(generics.ListAPIView):
    """
    API view to list products. 
    Supports filtering by category and is_vegetarian via query parameters.
    Also supports searching by name/description and ordering by price/created_date.
    """
    serializer_class = ProductSerializer
    permission_classes = []
    authentication_classes = []  # Ignore any token — fully public
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'sub_description', 'key_ingredients__name']
    ordering_fields = ['price', 'created_date', 'stock_quantity']
    
    def get_queryset(self):
        """
        Optionally restricts the returned products by filtering against query parameters.
        Only active products are returned.
        """
        queryset = Product.objects.filter(is_active=True).prefetch_related('categories', 'key_ingredients', 'images')
        
        product_ids = self.request.query_params.get('id')
        categories = self.request.query_params.get('category')
        is_vegetarian = self.request.query_params.get('is_vegetarian')
        is_preservation_free = self.request.query_params.get('is_preservation_free')
        taste = self.request.query_params.get('taste')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        in_stock = self.request.query_params.get('in_stock')
        
        if product_ids:
            # Handle comma-separated list of product IDs
            id_list = [i.strip() for i in product_ids.split(',')]
            queryset = queryset.filter(id__in=id_list)
            
        if categories:
            # Handle comma-separated list of categories (IDs or names)
            category_list = [c.strip() for c in categories.split(',')]
            # If all are numbers, filter by category ID, otherwise by category name
            if all(c.isdigit() for c in category_list):
                queryset = queryset.filter(categories__id__in=category_list).distinct()
            else:
                queryset = queryset.filter(categories__name__in=category_list).distinct()
            
        if is_vegetarian is not None:
             # Convert to boolean
             is_veg_bool = str(is_vegetarian).lower() in ['true', '1', 't', 'y', 'yes']
             queryset = queryset.filter(is_vegetarian=is_veg_bool)
             
        if is_preservation_free is not None:
             is_pres_free_bool = str(is_preservation_free).lower() in ['true', '1', 't', 'y', 'yes']
             queryset = queryset.filter(is_preservation_free=is_pres_free_bool)
             
        if taste:
             taste_list = [t.strip() for t in taste.split(',')]
             queryset = queryset.filter(taste__in=taste_list)
             
        if min_price is not None:
            try:
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass
                
        if max_price is not None:
            try:
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass
                
        if in_stock is not None:
            is_in_stock = str(in_stock).lower() in ['true', '1', 't', 'y', 'yes']
            if is_in_stock:
                queryset = queryset.filter(stock_quantity__gt=0)
            else:
                queryset = queryset.filter(stock_quantity=0)
             
        return queryset


class CategoryListAPIView(generics.ListAPIView):
    """
    Public endpoint — returns categories where show_on_homepage=True.
    No authentication required.
    """
    serializer_class = CategorySerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        return Category.objects.filter(show_on_homepage=True).order_by('name')
