from rest_framework import serializers
from products.models import Product, Category, ProductImage, Ingredient

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        show_on_homepage = data.get('show_on_homepage', getattr(self.instance, 'show_on_homepage', False))
        icon = data.get('icon', getattr(self.instance, 'icon', None))
        color = data.get('color', getattr(self.instance, 'color', None))

        if show_on_homepage:
            errors = {}
            if not icon:
                errors['error'] = "Icon is required when category is shown on homepage."
            if not color:
                errors['error'] = "Color is required when category is shown on homepage."
            
            if errors:
                raise serializers.ValidationError(errors)
                
        return data


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
    ingredients = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="Comma-separated list of ingredient names to add/create."
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
        ingredients_str = validated_data.pop('ingredients', None)
        
        product = super().create(validated_data)
        
        if ingredients_str:
            names = [name.strip() for name in ingredients_str.split(',') if name.strip()]
            for name in names:
                ingredient, _ = Ingredient.objects.get_or_create(name=name)
                product.key_ingredients.add(ingredient)
                
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
        ingredients_str = validated_data.pop('ingredients', None)
        
        instance = super().update(instance, validated_data)
        
        if ingredients_str is not None:
             names = [name.strip() for name in ingredients_str.split(',') if name.strip()]
             instance.key_ingredients.clear()
             for name in names:
                 ingredient, _ = Ingredient.objects.get_or_create(name=name)
                 instance.key_ingredients.add(ingredient)
                 
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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convert key_ingredients to a comma-separated string for the frontend
        ret['ingredients'] = ', '.join([ing.name for ing in instance.key_ingredients.all()])
        return ret
