from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    show_on_homepage = models.BooleanField(default=False, help_text="Show this category on the homepage")
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Categories'

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sub_description = models.CharField(max_length=500, blank=True, null=True, help_text="Short description or tagline")
    
    # Pricing & Stock
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Stock Keeping Unit")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    TASTE_CHOICES = [
        ('Very_Spicy', 'Very Spicy'),
        ('Medium_Spicy', 'Medium Spicy'),
        ('Mild_Spicy', 'Mild Spicy'),
        ('Sour', 'Sour'),
        ('Sweet', 'Sweet'),
        ('Sweet_Sour', 'Sweet & Sour'),
        ('Spicy_Sour', 'Spicy & Sour'),
        ('Spicy_Sweet', 'Spicy & Sweet'),
    ]

    # Food Specific Fields
    is_vegetarian = models.BooleanField(default=True)
    is_preservation_free = models.BooleanField(default=False)
    taste = models.CharField(max_length=50, choices=TASTE_CHOICES, blank=True, null=True)
    net_weight = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 250g, 1kg")
    shelf_life_days = models.PositiveIntegerField(blank=True, null=True, help_text="Shelf life in days")
    
    # Categories and Topics
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    key_ingredients = models.ManyToManyField(Ingredient, related_name='products', blank=True)

    # Dates
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    best_seller = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.sku:
            # Create a base SKU from the name, limited to 80 chars to leave room for a counter
            base_sku = slugify(self.name).upper()[:80]
            sku = base_sku
            counter = 1
            # Check for existing SKUs to avoid UniqueConstraint errors
            while Product.objects.filter(sku=sku).exclude(pk=self.pk).exists():
                sku = f"{base_sku}-{counter}"
                counter += 1
            self.sku = sku
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', help_text="Upload product image")
    is_highlight = models.BooleanField(default=False, help_text="Is this the highlight (main) image?")
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        # Enforce maximum of 3 images per product (max 3 allowed)
        if not self.pk: # Only check when creating a new image
            if self.product.images.count() >= 3:
                raise ValidationError("A product can have a maximum of 3 images.")

    def save(self, *args, **kwargs):
        self.full_clean() # Runs the clean() method validation

        # If this image is set as the highlight, unset any existing highlight for this product
        if self.is_highlight:
            ProductImage.objects.filter(product=self.product, is_highlight=True).exclude(pk=self.pk).update(is_highlight=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"

