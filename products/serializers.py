from rest_framework import serializers
from .models import Product, Category, ProductImage, Ingredient

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='categories', many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    ingredient_details = IngredientSerializer(source='key_ingredients', many=True, read_only=True)


    class Meta:
        model = Product
        fields = '__all__'
