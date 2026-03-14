from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Categories'

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
    
    # Food Specific Fields
    is_vegetarian = models.BooleanField(default=True)
    net_weight = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 250g, 1kg")
    ingredients = models.TextField(blank=True, null=True)
    nutritional_information = models.TextField(blank=True, null=True)
    shelf_life_days = models.PositiveIntegerField(blank=True, null=True, help_text="Shelf life in days")
    
    # Categories and Topics
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    materials = models.JSONField(default=list, blank=True, help_text="List of materials used in the product")
    
    # Media
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="External URL of the product image")
    
    # Dates
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

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
