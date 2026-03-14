from rest_framework import serializers
from products.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_discount_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Discount price cannot be negative.")
        return value

    def validate(self, data):
        # We need to account for both update ('price' might not be in data if partial update)
        # and create scenarios. We use self.instance to get existing data if it's an update.
        
        price = data.get('price', getattr(self.instance, 'price', None))
        discount_price = data.get('discount_price', getattr(self.instance, 'discount_price', None))

        if price and discount_price and discount_price >= price:
            raise serializers.ValidationError({
                "discount_price": "Discount price must be less than the actual price."
            })
            
        return data
