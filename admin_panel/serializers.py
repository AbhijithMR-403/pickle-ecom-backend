from rest_framework import serializers
from products.models import Product, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ['product']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text="List of additional image files to upload."
    )
    highlight_image = serializers.ImageField(
        write_only=True,
        required=False,
        help_text="The main highlight image file."
    )
    
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
            
        uploaded_images = data.get('uploaded_images', [])
        highlight_image = data.get('highlight_image', None)
        
        total_images = len(uploaded_images) + (1 if highlight_image else 0)
        if total_images > 3:
            raise serializers.ValidationError("A product can have a maximum of 3 images.")
            
        return data

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        highlight_image = validated_data.pop('highlight_image', None)
        product = super().create(validated_data)
        
        if highlight_image:
            ProductImage.objects.create(
                product=product,
                image=highlight_image,
                is_highlight=True
            )
            
        for img in uploaded_images:
            ProductImage.objects.create(
                product=product,
                image=img,
                is_highlight=False
            )
            
        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        highlight_image = validated_data.pop('highlight_image', None)
        
        instance = super().update(instance, validated_data)
        
        if uploaded_images is not None or highlight_image is not None:
            # Recreate all images for this product
            instance.images.all().delete()
            
            if highlight_image:
                ProductImage.objects.create(
                    product=instance,
                    image=highlight_image,
                    is_highlight=True
                )
                
            if uploaded_images is not None:
                for img in uploaded_images:
                    ProductImage.objects.create(
                        product=instance,
                        image=img,
                        is_highlight=False
                    )
                
        return instance
