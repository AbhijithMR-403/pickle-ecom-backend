from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    """
    API view to list products. 
    Supports filtering by category and is_vegetarian via query parameters.
    Also supports searching by name/description and ordering by price/created_date.
    """
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'sub_description']
    ordering_fields = ['price', 'created_date', 'stock_quantity']
    
    def get_queryset(self):
        """
        Optionally restricts the returned products by filtering against query parameters.
        Only active products are returned.
        """
        queryset = Product.objects.filter(is_active=True).prefetch_related('categories')
        
        category = self.request.query_params.get('category')
        is_vegetarian = self.request.query_params.get('is_vegetarian')
        
        if category:
            queryset = queryset.filter(categories__id=category)
            
        if is_vegetarian is not None:
             # Convert to boolean
             is_veg_bool = str(is_vegetarian).lower() in ['true', '1', 't', 'y', 'yes']
             queryset = queryset.filter(is_vegetarian=is_veg_bool)
             
        return queryset
