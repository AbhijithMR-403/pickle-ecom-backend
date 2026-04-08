from django.urls import path
from .views import ProductListAPIView, CategoryListAPIView, BannerListAPIView

urlpatterns = [
    path('products', ProductListAPIView.as_view(), name='product-list'),
    path('categories', CategoryListAPIView.as_view(), name='public-category-list'),
    path('banners', BannerListAPIView.as_view(), name='public-banner-list'),
]
