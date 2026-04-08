from rest_framework import serializers
from .models import Product, Category, ProductImage, Ingredient, Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.product:
            ret['product_details'] = ProductSerializer(instance.product, context=self.context).data
        return ret


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
